================================================================================
Yocto Project Recipes and Layers
================================================================================

**TL;DR**: Deep dive into Yocto recipe creation (.bb files), bbappend files, 
layer management, custom recipes, and advanced BitBake features for building 
custom embedded Linux distributions.

**Related Cheatsheets**: 
:doc:`Yocto Basics </Linux/Linux_Yocto_Basics>`, 
:doc:`Buildroot </Linux/buildroot>`,
:doc:`Linux Kernel </Linux/Linux Kernel>`,
:doc:`Embedded C </Languages/Embedded C>`

================================================================================
1. Recipe Fundamentals
================================================================================

1.1 Recipe Structure
--------------------------------------------------------------------------------

**Complete Recipe Example** (myapp_1.0.bb):

.. code-block:: bash

    # Recipe metadata
    SUMMARY = "My custom application"
    DESCRIPTION = "A custom C application for embedded systems"
    HOMEPAGE = "http://example.com/myapp"
    SECTION = "applications"
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123def456..."
    
    # Dependencies
    DEPENDS = "zlib openssl"
    RDEPENDS:${PN} = "bash libz1 libssl1.1"
    
    # Source location
    SRC_URI = "http://example.com/myapp-${PV}.tar.gz \
               file://0001-fix-build.patch \
               file://myapp.service \
               file://myapp.conf \
              "
    
    # Checksums for source verification
    SRC_URI[md5sum] = "abc123..."
    SRC_URI[sha256sum] = "def456..."
    
    # Source directory (defaults to ${WORKDIR}/${PN}-${PV})
    S = "${WORKDIR}/${PN}-${PV}"
    
    # Inherit build system class
    inherit autotools systemd
    
    # systemd service
    SYSTEMD_SERVICE:${PN} = "myapp.service"
    SYSTEMD_AUTO_ENABLE = "enable"
    
    # Configure options
    EXTRA_OECONF = "--enable-ssl --with-zlib"
    
    # Compile flags
    EXTRA_OEMAKE = "CFLAGS='${CFLAGS}' LDFLAGS='${LDFLAGS}'"
    
    # Custom configure
    do_configure() {
        ./configure ${EXTRA_OECONF}
    }
    
    # Custom compile
    do_compile() {
        oe_runmake
    }
    
    # Custom install
    do_install() {
        # Install binary
        install -d ${D}${bindir}
        install -m 0755 myapp ${D}${bindir}/
        
        # Install configuration
        install -d ${D}${sysconfdir}
        install -m 0644 ${WORKDIR}/myapp.conf ${D}${sysconfdir}/
        
        # Install systemd service
        install -d ${D}${systemd_system_unitdir}
        install -m 0644 ${WORKDIR}/myapp.service ${D}${systemd_system_unitdir}/
    }
    
    # Package files
    FILES:${PN} = "${bindir}/myapp ${sysconfdir}/myapp.conf"
    FILES:${PN} += "${systemd_system_unitdir}/myapp.service"

1.2 Recipe Naming Convention
--------------------------------------------------------------------------------

**File Naming**:

.. code-block:: bash

    # Standard format: <name>_<version>.bb
    bash_5.1.bb
    linux-yocto_5.15.bb
    myapp_1.0.bb
    
    # Version with revision: <name>_<version>-<revision>.bb
    glibc_2.35-r0.bb
    
    # Git recipes: <name>_git.bb
    myapp_git.bb
    
    # Append files: <name>_<version>.bbappend or <name>_%.bbappend
    linux-yocto_5.15.bbappend      # Specific version
    linux-yocto_%.bbappend         # All versions

**Version Variables**:

.. code-block:: bash

    PN = "myapp"           # Package Name
    PV = "1.0"             # Package Version (from filename)
    PR = "r0"              # Package Revision
    P  = "myapp-1.0"       # ${PN}-${PV}
    PF = "myapp-1.0-r0"    # ${PN}-${PV}-${PR}

================================================================================
2. Source Management
================================================================================

2.1 SRC_URI Patterns
--------------------------------------------------------------------------------

**HTTP/HTTPS Sources**:

.. code-block:: bash

    # Simple tarball
    SRC_URI = "https://example.com/myapp-${PV}.tar.gz"
    
    # Multiple source files
    SRC_URI = "https://example.com/myapp-${PV}.tar.gz \
               https://example.com/data.bin \
              "
    
    # With checksums
    SRC_URI[md5sum] = "abc123..."
    SRC_URI[sha256sum] = "def456..."
    
    # Named checksums for multiple files
    SRC_URI = "https://example.com/myapp.tar.gz;name=app \
               https://example.com/data.bin;name=data \
              "
    SRC_URI[app.md5sum] = "abc..."
    SRC_URI[data.md5sum] = "def..."

**Git Sources**:

.. code-block:: bash

    # Git repository with tag
    SRC_URI = "git://github.com/user/repo.git;protocol=https;tag=v${PV}"
    
    # Git with branch
    SRC_URI = "git://github.com/user/repo.git;protocol=https;branch=master"
    SRCREV = "abc123def456..."  # Specific commit
    
    # Git with AUTOREV (always latest)
    SRC_URI = "git://github.com/user/repo.git;protocol=https;branch=main"
    SRCREV = "${AUTOREV}"
    PV = "1.0+git${SRCPV}"
    
    # Multiple git repositories
    SRC_URI = "git://github.com/user/app.git;protocol=https;name=app;destsuffix=app \
               git://github.com/user/lib.git;protocol=https;name=lib;destsuffix=lib \
              "
    SRCREV_app = "abc123..."
    SRCREV_lib = "def456..."

**Local Files**:

.. code-block:: bash

    # Files from recipe directory
    SRC_URI = "file://myapp.c \
               file://myapp.h \
               file://Makefile \
              "
    
    # Files are searched in:
    # 1. files/ directory next to recipe
    # 2. <recipe-name>/ directory
    # 3. ${PN}/ directory
    
    # Subdirectories
    SRC_URI = "file://src/main.c \
               file://config/default.conf \
              "

**Patches**:

.. code-block:: bash

    # Apply patches in order
    SRC_URI += "file://0001-fix-compilation.patch \
                file://0002-add-feature.patch \
               "
    
    # Patches with striplevel
    SRC_URI += "file://my.patch;striplevel=0"
    
    # Patches with conditional application
    SRC_URI += "file://arm-only.patch;apply=no"
    do_patch:append:arm() {
        patch -p1 < ${WORKDIR}/arm-only.patch
    }

2.2 Fetcher Parameters
--------------------------------------------------------------------------------

**Common URI Parameters**:

.. code-block:: bash

    # Download to specific directory
    SRC_URI = "http://example.com/file.tar.gz;downloadfilename=custom-name.tar.gz"
    
    # Subpath extraction
    SRC_URI = "http://example.com/file.tar.gz;subdir=myapp"
    
    # Unpack control
    SRC_URI = "http://example.com/file.tar.gz;unpack=false"
    
    # Name for multi-file checksums
    SRC_URI = "http://example.com/file.tar.gz;name=source"

================================================================================
3. Dependencies
================================================================================

3.1 Build vs Runtime Dependencies
--------------------------------------------------------------------------------

**DEPENDS** (Build-time):

.. code-block:: bash

    # Packages needed to compile
    DEPENDS = "zlib openssl cmake-native"
    
    # Add dependency
    DEPENDS += "libfoo"
    
    # Append (safer in bbappend)
    DEPENDS:append = " libbar"
    
    # Architecture-specific
    DEPENDS:append:arm = " arm-specific-lib"

**RDEPENDS** (Runtime):

.. code-block:: bash

    # Packages needed at runtime
    RDEPENDS:${PN} = "bash python3 libz1"
    
    # For specific package splits
    RDEPENDS:${PN}-dev = "${PN} (= ${EXTENDPV})"
    RDEPENDS:${PN}-dbg = "${PN} (= ${EXTENDPV})"
    
    # Dynamic dependencies (from shared library analysis)
    # Automatically added by BitBake

**Task Dependencies**:

.. code-block:: bash

    # Task depends on another recipe's task
    do_compile[depends] += "zlib:do_populate_sysroot"
    
    # Multiple dependencies
    do_install[depends] += "mylib:do_populate_sysroot"
    do_install[depends] += "mytools:do_populate_sysroot"
    
    # Task ordering within same recipe
    do_custom_task[depends] = "do_compile"

3.2 Virtual Packages
--------------------------------------------------------------------------------

**Providers and Virtuals**:

.. code-block:: bash

    # Recipe provides virtual package
    PROVIDES = "virtual/kernel"
    PROVIDES += "virtual/bootloader"
    
    # Depend on virtual package
    DEPENDS = "virtual/kernel virtual/libc"
    
    # Prefer specific provider
    # In local.conf or distro.conf:
    PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
    PREFERRED_PROVIDER_virtual/bootloader = "u-boot"
    
    # Prefer version
    PREFERRED_VERSION_linux-yocto = "5.15%"

================================================================================
4. Tasks and Functions
================================================================================

4.1 Standard Tasks
--------------------------------------------------------------------------------

**Task Execution Order**:

.. code-block:: bash

    do_fetch          # Fetch sources
    do_unpack         # Extract sources
    do_patch          # Apply patches
    do_configure      # Configure build
    do_compile        # Build
    do_install        # Install to ${D}
    do_package        # Split into packages
    do_package_write_rpm  # Create RPM packages
    do_rootfs         # (Image recipes) Create root filesystem

**Custom Tasks**:

.. code-block:: bash

    # Define custom task
    do_mytask() {
        echo "Running custom task"
        # Task code here
    }
    
    # Add task to task graph
    addtask mytask after do_compile before do_install
    
    # Run manually
    bitbake -c mytask myrecipe

**Overriding Tasks**:

.. code-block:: bash

    # Replace entire task
    do_install() {
        # Completely new implementation
        install -d ${D}${bindir}
        install -m 0755 myapp ${D}${bindir}/
    }
    
    # Prepend to task
    do_compile:prepend() {
        echo "Before compile"
    }
    
    # Append to task
    do_compile:append() {
        echo "After compile"
    }
    
    # Architecture-specific append
    do_install:append:arm() {
        # ARM-specific installation
    }

4.2 Python vs Shell Functions
--------------------------------------------------------------------------------

**Shell Functions** (default):

.. code-block:: bash

    do_compile() {
        oe_runmake
    }

**Python Functions**:

.. code-block:: python

    python do_custom_task() {
        import os
        
        workdir = d.getVar('WORKDIR')
        pn = d.getVar('PN')
        
        bb.note(f"Building {pn} in {workdir}")
        
        # Run shell command
        bb.build.exec_func('do_compile', d)
    }
    
    addtask custom_task after do_configure before do_compile

**Inline Python**:

.. code-block:: bash

    # Python expression
    MY_VAR = "${@d.getVar('OTHER_VAR').upper()}"
    
    # Python code
    PARALLEL_MAKE = "-j ${@oe.utils.cpu_count()}"

================================================================================
5. Variables and Overrides
================================================================================

5.1 Variable Assignment
--------------------------------------------------------------------------------

**Assignment Operators**:

.. code-block:: bash

    # Simple assignment
    VAR = "value"
    
    # Immediate expansion
    VAR := "value with ${OTHER_VAR}"
    
    # Default value (only if not set)
    VAR ?= "default"
    
    # Weak default (overridden by ?=)
    VAR ??= "weak default"
    
    # Append with space
    VAR += "more"
    
    # Prepend with space
    VAR =+ "before"
    
    # Append without space
    VAR .= "appended"
    
    # Prepend without space
    VAR =. "prepended"
    
    # Append/prepend (safest for bbappend)
    VAR:append = " value"
    VAR:prepend = "value "
    
    # Remove
    VAR:remove = "unwanted"

5.2 Overrides
--------------------------------------------------------------------------------

**Common Overrides**:

.. code-block:: bash

    # Architecture overrides
    SRC_URI:append:arm = " file://arm-patch.patch"
    CFLAGS:append:x86 = " -march=i686"
    
    # Machine overrides
    KERNEL_DEVICETREE:append:beaglebone = " am335x-boneblack.dtb"
    
    # Distribution overrides
    DISTRO_FEATURES:append:poky = " systemd"
    
    # Class overrides
    RDEPENDS:${PN}:class-target = "bash"
    RDEPENDS:${PN}:class-native = ""
    
    # Custom overrides
    OVERRIDES .= ":myfeature"
    SRC_URI:append:myfeature = " file://extra.patch"

**Override Order** (specific to general):

.. code-block:: bash

    # Most specific to least specific
    VAR:machine:arch:distro = "value"
    
    # Example
    VAR = "default"
    VAR:x86 = "x86 value"
    VAR:qemux86 = "qemux86 value"
    
    # On qemux86, VAR = "qemux86 value"

================================================================================
6. Classes
================================================================================

6.1 Common Classes
--------------------------------------------------------------------------------

**inherit Statement**:

.. code-block:: bash

    # Inherit single class
    inherit autotools
    
    # Inherit multiple classes
    inherit cmake pkgconfig systemd

**Popular Classes**:

.. code-block:: bash

    # autotools (./configure, make, make install)
    inherit autotools
    EXTRA_OECONF = "--enable-feature"
    
    # CMake
    inherit cmake
    EXTRA_OECMAKE = "-DENABLE_FEATURE=ON"
    
    # Meson
    inherit meson
    EXTRA_OEMESON = "-Dfeature=enabled"
    
    # Python setuptools
    inherit setuptools3
    
    # systemd
    inherit systemd
    SYSTEMD_SERVICE:${PN} = "myapp.service"
    SYSTEMD_AUTO_ENABLE = "enable"
    
    # kernel
    inherit kernel
    
    # module (kernel module)
    inherit module
    
    # pkgconfig
    inherit pkgconfig
    
    # update-rc.d (SysV init)
    inherit update-rc.d
    INITSCRIPT_NAME = "myapp"
    INITSCRIPT_PARAMS = "defaults 99"

6.2 Custom Classes
--------------------------------------------------------------------------------

**Creating a Class** (meta-custom/classes/myclass.bbclass):

.. code-block:: bash

    # Custom class for common functionality
    
    # Variables
    MY_CUSTOM_DIR = "${datadir}/mycustom"
    
    # Functions
    myclass_do_extra_install() {
        install -d ${D}${MY_CUSTOM_DIR}
        install -m 0644 ${WORKDIR}/data/* ${D}${MY_CUSTOM_DIR}/
    }
    
    # Hook into tasks
    do_install[postfuncs] += "myclass_do_extra_install"

**Using Custom Class**:

.. code-block:: bash

    inherit myclass
    
    # Class functions and variables are now available

================================================================================
7. Packaging
================================================================================

7.1 Package Splitting
--------------------------------------------------------------------------------

**Default Packages**:

.. code-block:: bash

    # Automatic package splits
    ${PN}           # Main package
    ${PN}-dev       # Development files (headers, .so symlinks)
    ${PN}-dbg       # Debug symbols
    ${PN}-doc       # Documentation
    ${PN}-locale    # Localization files
    ${PN}-staticdev # Static libraries

**Custom Package Splits**:

.. code-block:: bash

    # Create additional packages
    PACKAGES =+ "${PN}-extra ${PN}-tools"
    
    # Define files for each package
    FILES:${PN} = "${bindir}/myapp ${sysconfdir}/myapp.conf"
    FILES:${PN}-extra = "${datadir}/myapp/plugins/*"
    FILES:${PN}-tools = "${bindir}/myapp-tool"
    
    # Dependencies for split packages
    RDEPENDS:${PN}-extra = "${PN}"
    RDEPENDS:${PN}-tools = "${PN} bash"

**File Patterns**:

.. code-block:: bash

    # Common file locations
    FILES:${PN} = "${bindir}/* ${sbindir}/*"
    FILES:${PN} += "${libdir}/lib*.so.*"
    FILES:${PN} += "${sysconfdir}/${PN}/*"
    FILES:${PN} += "${datadir}/${PN}/*"
    
    FILES:${PN}-dev = "${includedir}/* ${libdir}/lib*.so"
    FILES:${PN}-dev += "${libdir}/pkgconfig/*.pc"

7.2 Package Control
--------------------------------------------------------------------------------

**Package Metadata**:

.. code-block:: bash

    # Package description
    DESCRIPTION = "Detailed package description"
    SUMMARY = "Short one-line summary"
    
    # Section
    SECTION = "devel"
    # Common sections: base, console, devel, libs, net, x11
    
    # Priority
    PRIORITY = "optional"
    # Priorities: required, important, standard, optional, extra
    
    # Maintainer
    MAINTAINER = "Name <email@example.com>"

**Package Installation**:

.. code-block:: bash

    # Pre/post install scripts
    pkg_postinst:${PN}() {
        #!/bin/sh
        if [ -n "$D" ]; then
            # Installing to image, not target
            exit 0
        fi
        # Target-side post-install
        systemctl daemon-reload
        systemctl enable myapp.service
    }
    
    pkg_prerm:${PN}() {
        #!/bin/sh
        systemctl stop myapp.service
        systemctl disable myapp.service
    }

================================================================================
8. bbappend Files
================================================================================

8.1 Extending Recipes
--------------------------------------------------------------------------------

**bbappend Structure**:

.. code-block:: bash

    # File: meta-custom/recipes-core/bash/bash_%.bbappend
    
    # Extend FILESEXTRAPATHS for local files
    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
    
    # Add patch
    SRC_URI += "file://custom.patch"
    
    # Modify configuration
    EXTRA_OECONF:append = " --enable-custom-feature"
    
    # Add runtime dependency
    RDEPENDS:${PN}:append = " custom-lib"

**Directory Structure**:

.. code-block:: text

    meta-custom/recipes-core/bash/
    ├── bash_%.bbappend
    └── bash/
        ├── custom.patch
        └── custom.sh

8.2 Common bbappend Patterns
--------------------------------------------------------------------------------

**Kernel Configuration**:

.. code-block:: bash

    # meta-custom/recipes-kernel/linux/linux-yocto_%.bbappend
    
    FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
    
    SRC_URI += "file://custom.cfg \
                file://custom.scc \
               "
    
    # files/custom.cfg:
    # CONFIG_MYDRIVER=m
    # CONFIG_FEATURE=y

**Image Customization**:

.. code-block:: bash

    # meta-custom/recipes-core/images/core-image-minimal.bbappend
    
    # Add packages to image
    IMAGE_INSTALL:append = " myapp vim openssh"
    
    # Add custom post-processing
    do_rootfs:append() {
        # Custom filesystem modifications
        echo "Custom configuration" > ${IMAGE_ROOTFS}/etc/custom.conf
    }

**Systemd Service**:

.. code-block:: bash

    # meta-custom/recipes-myapp/myapp/myapp_1.0.bbappend
    
    FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
    
    inherit systemd
    
    SRC_URI += "file://myapp.service"
    
    SYSTEMD_SERVICE:${PN} = "myapp.service"
    SYSTEMD_AUTO_ENABLE = "enable"
    
    do_install:append() {
        install -d ${D}${systemd_system_unitdir}
        install -m 0644 ${WORKDIR}/myapp.service ${D}${systemd_system_unitdir}/
    }

================================================================================
9. Advanced Recipe Patterns
================================================================================

9.1 Git Recipes
--------------------------------------------------------------------------------

**Git Version Recipe**:

.. code-block:: bash

    # myapp_git.bb
    
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=..."
    
    SRC_URI = "git://github.com/user/myapp.git;protocol=https;branch=main"
    
    # Pin to specific commit
    SRCREV = "abc123def456..."
    
    # Or use latest (not recommended for production)
    # SRCREV = "${AUTOREV}"
    
    # Version with git hash
    PV = "1.0+git${SRCPV}"
    
    S = "${WORKDIR}/git"
    
    inherit autotools

9.2 Native and Cross Recipes
--------------------------------------------------------------------------------

**Native Recipe** (runs on build host):

.. code-block:: bash

    # mytool-native_1.0.bb
    
    inherit native
    
    SRC_URI = "http://example.com/mytool-${PV}.tar.gz"
    
    do_compile() {
        ${CC} -o mytool mytool.c
    }
    
    do_install() {
        install -d ${D}${bindir}
        install -m 0755 mytool ${D}${bindir}/
    }
    
    # Used in other recipes:
    # DEPENDS += "mytool-native"

**Cross Recipe** (runs on target, built with cross-compiler):

.. code-block:: bash

    # Normal target recipe (default)
    
    inherit cross
    
    # Cross-compilation happens automatically

9.3 Multilib Support
--------------------------------------------------------------------------------

**32-bit Libraries on 64-bit System**:

.. code-block:: bash

    # In local.conf:
    require conf/multilib.conf
    MULTILIBS = "multilib:lib32"
    DEFAULTTUNE:virtclass-multilib-lib32 = "x86"
    
    # Install both 64-bit and 32-bit versions
    IMAGE_INSTALL:append = " lib32-glibc"

================================================================================
10. Debugging Recipes
================================================================================

10.1 Development Shell
--------------------------------------------------------------------------------

**devshell**:

.. code-block:: bash

    # Drop into development shell
    bitbake -c devshell myapp
    
    # Environment is set up for building
    # Can run configure, make, etc. manually
    echo $CC        # Cross-compiler
    echo $CFLAGS    # Compiler flags
    echo $S         # Source directory
    echo $D         # Destination (install) directory

10.2 Recipe Variables
--------------------------------------------------------------------------------

**Inspect Variables**:

.. code-block:: bash

    # Show all variables for a recipe
    bitbake -e myapp > myapp-env.txt
    
    # Show specific variable
    bitbake -e myapp | grep ^SRC_URI=
    bitbake -e myapp | grep ^DEPENDS=
    
    # Show package files
    oe-pkgdata-util list-pkg-files myapp

================================================================================
11. Best Practices
================================================================================

11.1 Recipe Guidelines
--------------------------------------------------------------------------------

**DO**:

- Use ``:append`` and ``:prepend`` instead of ``+=`` in bbappend
- Keep recipes simple and focused
- Document custom variables and functions
- Use FILESEXTRAPATHS:prepend for file paths
- Verify checksums for downloaded sources
- Use SRCREV for git recipes (don't use AUTOREV in production)
- Split large packages appropriately
- Include LICENSE and LIC_FILES_CHKSUM
- Test recipes in clean build

**DON'T**:

- Modify recipes in meta/ layer
- Use absolute paths
- Hardcode version numbers
- Forget dependencies
- Use ${S} == ${WORKDIR} (set S explicitly if needed)
- Ignore license compliance
- Create recipes with side effects

11.2 Common Pitfalls
--------------------------------------------------------------------------------

**Wrong Variable Expansion**:

.. code-block:: bash

    # WRONG - += evaluated immediately
    SRC_URI += "file://patch.patch"  # May not find THISDIR
    
    # CORRECT - :append evaluated after all parsing
    SRC_URI:append = " file://patch.patch"

**Missing FILESEXTRAPATHS**:

.. code-block:: bash

    # WRONG - files not found
    SRC_URI += "file://custom.patch"
    
    # CORRECT
    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
    SRC_URI += "file://custom.patch"

**Install to Wrong Directory**:

.. code-block:: bash

    # WRONG - installs to build host
    do_install() {
        install -d /usr/bin
        install myapp /usr/bin/
    }
    
    # CORRECT - installs to ${D} (staging for target)
    do_install() {
        install -d ${D}${bindir}
        install -m 0755 myapp ${D}${bindir}/
    }

================================================================================
See Also
================================================================================

- :doc:`Yocto Basics </Linux/Linux_Yocto_Basics>`
- :doc:`Buildroot </Linux/buildroot>`
- :doc:`Linux Kernel </Linux/Linux Kernel>`
- :doc:`Embedded C </Languages/Embedded C>`
- :doc:`Linux Device Tree </Linux/Linux device tree>`
