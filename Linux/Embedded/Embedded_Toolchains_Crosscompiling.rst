================================================================================
Embedded Linux: Cross-Compilation and Toolchains - Complete Guide
================================================================================

:Author: Technical Documentation Team
:Date: January 18, 2026
:Version: 1.0
:Target: Embedded Linux Developers
:Kernel: 4.1+, 6.8+ compatible
:Reference: Linux Embedded Development (Module 1 Ch2, Module 3 Ch2)

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
TL;DR - Quick Reference
================================================================================

**Cross-Compilation Essentials:**

Cross-compilation is building software on one machine (host) for execution on
another machine (target) with different architecture (e.g., x86_64 → ARM).

**Toolchain Components (4 Core Elements):**

1. **GNU Compiler Collection (GCC)** - C/C++ compiler
2. **GNU Binutils** - Assembler, linker, object file utilities
3. **C Standard Library** - glibc, musl, uclibc-ng
4. **Linux Kernel Headers** - System call interface definitions

**Quick Commands:**

.. code-block:: bash

   # Check toolchain
   arm-linux-gnueabihf-gcc --version
   
   # Cross-compile simple program
   ${CROSS_COMPILE}gcc -o hello hello.c
   
   # Build with sysroot
   ${CC} --sysroot=${SYSROOT} -o app app.c -lpthread

**Triple Format:** ``<arch>-<vendor>-<kernel>-<os>``

Example: ``arm-buildroot-linux-gnueabihf``

- arch: arm, aarch64, mips, x86_64
- vendor: buildroot, poky, unknown
- kernel: linux
- os: gnu, gnueabi, gnueabihf, musl

================================================================================
1. Cross-Compilation Fundamentals
================================================================================

1.1 Why Cross-Compilation?
---------------------------

**Native vs Cross Compilation:**

+-------------------+----------------------------------+----------------------------+
| Aspect            | Native Compilation               | Cross Compilation          |
+===================+==================================+============================+
| Host              | x86_64                           | x86_64                     |
+-------------------+----------------------------------+----------------------------+
| Target            | x86_64                           | ARM, MIPS, PowerPC         |
+-------------------+----------------------------------+----------------------------+
| Speed             | Fast (modern CPU)                | Fast (use host power)      |
+-------------------+----------------------------------+----------------------------+
| Resources         | Full RAM/storage                 | Full host resources        |
+-------------------+----------------------------------+----------------------------+
| Use Case          | Desktop/server development       | Embedded systems           |
+-------------------+----------------------------------+----------------------------+

**Reasons for Cross-Compilation:**

1. **Performance** - Host CPU 100-1000x faster than embedded target
2. **Resources** - Embedded targets have limited RAM (32MB-512MB typical)
3. **Storage** - No room for GCC toolchain on target (500MB-2GB)
4. **Convenience** - Better development environment on host
5. **Consistency** - Controlled build environment, reproducible builds

**Example Scenario:**

.. code-block:: text

   Host: Ubuntu 20.04 x86_64
   - CPU: Intel i7 (8 cores, 3.5GHz)
   - RAM: 32GB
   - Storage: 1TB SSD
   
   Target: Raspberry Pi 4 (ARM Cortex-A72)
   - CPU: 4 cores @ 1.5GHz
   - RAM: 2GB
   - Storage: 16GB SD card
   
   Build time comparison:
   - Linux kernel native on target: 4-6 hours
   - Linux kernel cross-compile on host: 15-30 minutes

1.2 Cross-Compilation Workflow
-------------------------------

**Build Process Flow:**

.. code-block:: text

   ┌─────────────┐
   │ Source Code │
   │  (C/C++)    │
   └──────┬──────┘
          │
          v
   ┌────────────────────────────────────────┐
   │ Preprocessor (cpp)                     │
   │ - Expand #include, #define            │
   │ - ${CROSS_COMPILE}cpp                 │
   └──────┬─────────────────────────────────┘
          │
          v
   ┌────────────────────────────────────────┐
   │ Compiler (gcc/g++)                     │
   │ - Generate assembly (.s)              │
   │ - ${CROSS_COMPILE}gcc -S              │
   └──────┬─────────────────────────────────┘
          │
          v
   ┌────────────────────────────────────────┐
   │ Assembler (as)                         │
   │ - Generate object files (.o)          │
   │ - ${CROSS_COMPILE}as                  │
   └──────┬─────────────────────────────────┘
          │
          v
   ┌────────────────────────────────────────┐
   │ Linker (ld)                            │
   │ - Link with libraries                 │
   │ - Create executable (ELF)             │
   │ - ${CROSS_COMPILE}ld                  │
   └──────┬─────────────────────────────────┘
          │
          v
   ┌───────────────────┐
   │ Target Binary     │
   │ (ARM/MIPS/etc)    │
   └───────────────────┘

**Environment Variables:**

.. code-block:: bash

   # Method 1: CROSS_COMPILE prefix
   export CROSS_COMPILE=arm-linux-gnueabihf-
   ${CROSS_COMPILE}gcc -o hello hello.c
   
   # Method 2: Direct CC/CXX/LD
   export CC=arm-linux-gnueabihf-gcc
   export CXX=arm-linux-gnueabihf-g++
   export LD=arm-linux-gnueabihf-ld
   export AR=arm-linux-gnueabihf-ar
   export AS=arm-linux-gnueabihf-as
   export RANLIB=arm-linux-gnueabihf-ranlib
   export STRIP=arm-linux-gnueabihf-strip
   
   # Method 3: Using SDK environment script
   source /opt/sdk/environment-setup-cortexa9hf-neon-poky-linux-gnueabi

1.3 Target Architecture Considerations
---------------------------------------

**Common Embedded Architectures:**

+-------------+------------------+------------------------+-------------------------+
| Architecture| Endianness       | Common Use             | Triple Example          |
+=============+==================+========================+=========================+
| ARM (32-bit)| Little           | Mobile, IoT, Industrial| arm-linux-gnueabihf     |
+-------------+------------------+------------------------+-------------------------+
| ARM64       | Little           | High-end embedded      | aarch64-linux-gnu       |
+-------------+------------------+------------------------+-------------------------+
| MIPS        | Big/Little       | Routers, networking    | mips-linux-gnu          |
+-------------+------------------+------------------------+-------------------------+
| PowerPC     | Big              | Automotive, aerospace  | powerpc-linux-gnu       |
+-------------+------------------+------------------------+-------------------------+
| x86         | Little           | Industrial PC          | i686-linux-gnu          |
+-------------+------------------+------------------------+-------------------------+

**ARM ABI Variants:**

.. code-block:: text

   ARM EABI (gnueabi):
   - Older ABI, software floating point
   - Slower FP operations, more compatible
   - Triple: arm-linux-gnueabi
   
   ARM EABIHF (gnueabihf):
   - Hardware floating point (VFP/NEON)
   - Faster, requires FPU in hardware
   - Triple: arm-linux-gnueabihf
   
   ARM64 (aarch64):
   - 64-bit ARM architecture
   - Always hardware FP
   - Triple: aarch64-linux-gnu

**Checking Binary Architecture:**

.. code-block:: bash

   # Identify binary architecture
   file hello
   # Output: hello: ELF 32-bit LSB executable, ARM, EABI5 version 1...
   
   # Check required dynamic libraries
   arm-linux-gnueabihf-readelf -d hello | grep NEEDED
   #  0x00000001 (NEEDED)    Shared library: [libc.so.6]
   
   # Examine ELF header
   arm-linux-gnueabihf-readelf -h hello
   # Machine:                           ARM
   # Flags:                             0x5000400, Version5 EABI, hard-float ABI

================================================================================
2. Toolchain Components Deep Dive
================================================================================

2.1 GNU Compiler Collection (GCC)
----------------------------------

**GCC Components:**

.. code-block:: text

   GCC Toolchain Suite:
   ├── gcc          - C compiler
   ├── g++          - C++ compiler
   ├── gfortran     - Fortran compiler
   ├── gcov         - Code coverage tool
   ├── cpp          - C preprocessor
   └── libgcc       - GCC runtime library

**Compiler Versions:**

+---------+----------------+---------------------------+------------------------+
| Version | Release        | Key Features              | Recommended For        |
+=========+================+===========================+========================+
| GCC 4.9 | 2014           | C++14, ARM improvements   | Legacy systems         |
+---------+----------------+---------------------------+------------------------+
| GCC 5.x | 2015           | C++14 complete, better    | Stable production      |
|         |                | optimization              |                        |
+---------+----------------+---------------------------+------------------------+
| GCC 7.x | 2017           | C++17, improved warnings  | Balanced choice        |
+---------+----------------+---------------------------+------------------------+
| GCC 9.x | 2019           | C++17 complete, link-time | Modern embedded        |
|         |                | optimization (LTO)        |                        |
+---------+----------------+---------------------------+------------------------+
| GCC 11+ | 2021+          | C++20, better diagnostics | Cutting-edge           |
+---------+----------------+---------------------------+------------------------+

**GCC Cross-Compile Flags:**

.. code-block:: bash

   # Architecture-specific flags
   arm-linux-gnueabihf-gcc \
       -march=armv7-a          # ARM architecture version \
       -mtune=cortex-a9        # Optimize for Cortex-A9 \
       -mfpu=neon              # Enable NEON SIMD \
       -mfloat-abi=hard        # Hardware floating point \
       -O2                     # Optimization level \
       -g                      # Debug symbols \
       -Wall -Wextra           # Enable warnings \
       -o myapp myapp.c
   
   # Common optimization levels
   -O0    # No optimization (debugging)
   -O1    # Basic optimization
   -O2    # Recommended for production
   -O3    # Aggressive optimization (may increase size)
   -Os    # Optimize for size (embedded systems)
   -Og    # Optimize for debugging experience

**GCC Machine-Specific Options:**

.. code-block:: bash

   # ARM-specific
   -mthumb              # Generate Thumb instructions (16/32-bit)
   -marm                # Generate ARM instructions (32-bit)
   -mcpu=cortex-a53     # CPU type (combines -march + -mtune)
   -mfpu=vfpv4          # Floating point unit type
   
   # MIPS-specific
   -march=mips32r2      # MIPS architecture revision
   -msoft-float         # Software floating point
   -mhard-float         # Hardware floating point
   -mabi=32             # ABI type
   
   # x86-specific
   -m32                 # 32-bit x86
   -m64                 # 64-bit x86-64
   -march=native        # Optimize for host CPU (native only)

2.2 GNU Binutils
----------------

**Binutils Tool Suite:**

+-------------------+-----------------------------------------------------+
| Tool              | Purpose                                             |
+===================+=====================================================+
| as                | Assembler - convert assembly to object files       |
+-------------------+-----------------------------------------------------+
| ld                | Linker - combine object files to executable        |
+-------------------+-----------------------------------------------------+
| ar                | Archive manager - create static libraries (.a)     |
+-------------------+-----------------------------------------------------+
| ranlib            | Generate index for archives                         |
+-------------------+-----------------------------------------------------+
| objdump           | Display object file information                     |
+-------------------+-----------------------------------------------------+
| objcopy           | Copy/translate object files                         |
+-------------------+-----------------------------------------------------+
| nm                | List symbols from object files                      |
+-------------------+-----------------------------------------------------+
| strip             | Remove symbols (reduce binary size)                |
+-------------------+-----------------------------------------------------+
| readelf           | Display ELF file information                        |
+-------------------+-----------------------------------------------------+
| size              | Show section sizes                                  |
+-------------------+-----------------------------------------------------+
| strings           | Extract printable strings                           |
+-------------------+-----------------------------------------------------+

**Common Binutils Operations:**

.. code-block:: bash

   # Create static library
   ${CROSS_COMPILE}ar rcs libmylib.a obj1.o obj2.o obj3.o
   ${CROSS_COMPILE}ranlib libmylib.a
   
   # Examine symbols
   ${CROSS_COMPILE}nm libmylib.a
   # 00000000 T my_function
   # 00000010 D my_global_var
   # U printf                 # Undefined - needs linking
   
   # Disassemble binary
   ${CROSS_COMPILE}objdump -d myapp > myapp.asm
   
   # Show section sizes
   ${CROSS_COMPILE}size myapp
   #    text    data     bss     dec     hex filename
   #   12345    2048    1024   15417    3c39 myapp
   
   # Strip debug symbols (reduce size)
   ${CROSS_COMPILE}strip myapp
   # Original: 150KB -> Stripped: 45KB
   
   # Copy and convert formats
   ${CROSS_COMPILE}objcopy -O binary myapp myapp.bin
   ${CROSS_COMPILE}objcopy -O srec myapp myapp.srec

**Linker Scripts:**

.. code-block:: text

   /* Custom linker script for embedded system */
   MEMORY
   {
       FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
       RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
   }
   
   SECTIONS
   {
       .text :
       {
           *(.vectors)          /* Interrupt vectors first */
           *(.text*)           /* Code */
           *(.rodata*)         /* Read-only data */
       } > FLASH
       
       .data :
       {
           *(.data*)           /* Initialized data */
       } > RAM AT> FLASH
       
       .bss :
       {
           *(.bss*)            /* Uninitialized data */
       } > RAM
   }

**Using Custom Linker Script:**

.. code-block:: bash

   # Compile with custom linker script
   ${CROSS_COMPILE}gcc -T custom.ld -o firmware.elf main.o startup.o
   
   # Generate map file for debugging
   ${CROSS_COMPILE}gcc -Wl,-Map=output.map -o myapp myapp.o

2.3 C Standard Library
-----------------------

**C Library Comparison:**

+------------+----------+------------+----------------------+-------------------+
| Library    | Size     | Features   | License              | Best For          |
+============+==========+============+======================+===================+
| glibc      | Large    | Full POSIX | LGPL                 | Desktop, server   |
|            | (2-3 MB) | complete   |                      | full features     |
+------------+----------+------------+----------------------+-------------------+
| musl libc  | Small    | Full POSIX | MIT                  | Modern embedded   |
|            | (600KB)  | clean code |                      | static linking    |
+------------+----------+------------+----------------------+-------------------+
| uClibc-ng  | Smallest | Configura- | LGPL                 | Very small        |
|            | (400KB)  | ble POSIX  |                      | embedded systems  |
+------------+----------+------------+----------------------+-------------------+
| newlib     | Small    | Bare-metal | BSD-like             | No OS, RTOS       |
|            | (500KB)  | embedded   |                      |                   |
+------------+----------+------------+----------------------+-------------------+

**glibc (GNU C Library):**

.. code-block:: text

   Features:
   ✓ Full POSIX.1-2008 compliance
   ✓ Locale support (i18n, l10n)
   ✓ Name Service Switch (NSS)
   ✓ Thread implementation (NPTL - Native POSIX Thread Library)
   ✓ IPv6 support
   ✓ Security features (stack protector, fortify source)
   
   Drawbacks:
   ✗ Large size (2-3 MB base)
   ✗ Slower startup
   ✗ More memory usage
   ✗ Complex configuration

**musl libc:**

.. code-block:: text

   Features:
   ✓ Clean, maintainable codebase
   ✓ Fast performance
   ✓ Excellent static linking support
   ✓ UTF-8 native
   ✓ Thread-safe by design
   ✓ Small footprint (600KB-1MB)
   
   Drawbacks:
   ✗ Limited locale support (UTF-8 only)
   ✗ No NSS support
   ✗ Some glibc extensions missing

**uClibc-ng:**

.. code-block:: text

   Features:
   ✓ Highly configurable
   ✓ Smallest footprint (400KB+)
   ✓ MMU-less support
   ✓ Good for resource-constrained systems
   
   Configuration options:
   - Enable/disable locale
   - Enable/disable wide char
   - Enable/disable threading
   - Custom malloc implementation

**Library Selection Guide:**

.. code-block:: text

   Choose glibc if:
   - RAM > 128MB
   - Need full POSIX compliance
   - Desktop-like functionality
   - Locale/internationalization required
   
   Choose musl if:
   - RAM 32-128MB
   - Need modern, clean implementation
   - Static linking preferred
   - Security-focused
   
   Choose uClibc-ng if:
   - RAM < 32MB
   - Absolute minimum size
   - Need fine-grained control
   - Legacy kernel support

2.4 Linux Kernel Headers
-------------------------

**Purpose of Kernel Headers:**

.. code-block:: text

   Kernel headers provide:
   1. System call numbers and interfaces
   2. ioctl() command definitions
   3. Structure definitions (e.g., sockaddr, input_event)
   4. Constants and macros
   5. Device driver interfaces
   
   Location in toolchain:
   ${SYSROOT}/usr/include/linux/
   ${SYSROOT}/usr/include/asm/
   ${SYSROOT}/usr/include/asm-generic/

**Kernel Version Compatibility:**

.. code-block:: bash

   # Check kernel headers version
   grep LINUX_VERSION_CODE ${SYSROOT}/usr/include/linux/version.h
   # #define LINUX_VERSION_CODE 262656  (4.1.0)
   
   # Calculate version from code
   # Formula: (Major << 16) + (Minor << 8) + Patch
   # 262656 = (4 << 16) + (1 << 8) + 0 = 4.1.0

**Important Consideration:**

.. code-block:: text

   Kernel headers version compatibility:
   
   ✓ SAFE: Headers version <= Running kernel version
      Example: Headers 4.1, Running kernel 5.10 ✓
   
   ✗ RISK: Headers version > Running kernel version
      Example: Headers 5.10, Running kernel 4.1 ✗
      May use features not available in older kernel
   
   Best practice:
   - Use kernel headers matching target kernel version
   - Or use headers from oldest kernel you support

**Installing Kernel Headers:**

.. code-block:: bash

   # From kernel source
   cd linux-4.1/
   make ARCH=arm INSTALL_HDR_PATH=/path/to/sysroot/usr headers_install
   
   # This installs to:
   # /path/to/sysroot/usr/include/linux/
   # /path/to/sysroot/usr/include/asm/

================================================================================
3. Building a Toolchain with Crosstool-NG
================================================================================

3.1 Crosstool-NG Overview
--------------------------

**What is Crosstool-NG?**

Crosstool-NG is a versatile cross-compilation toolchain builder that automates
the complex process of building a complete cross-toolchain.

**Features:**

.. code-block:: text

   ✓ Menu-driven configuration (like kernel menuconfig)
   ✓ Pre-configured samples for common targets
   ✓ Support for multiple C libraries (glibc, musl, uClibc-ng)
   ✓ Automatic downloading of sources
   ✓ Reproducible builds
   ✓ Canadian cross support
   ✓ Multilib support

**Installation:**

.. code-block:: bash

   # Install dependencies (Ubuntu/Debian)
   sudo apt-get install -y \
       build-essential git autoconf bison flex texinfo help2man \
       gawk libtool libtool-bin libncurses5-dev unzip
   
   # Download and build crosstool-NG
   git clone https://github.com/crosstool-ng/crosstool-ng
   cd crosstool-ng
   ./bootstrap
   ./configure --prefix=${HOME}/x-tools/crosstool-ng
   make
   make install
   
   # Add to PATH
   export PATH="${HOME}/x-tools/crosstool-ng/bin:${PATH}"

3.2 Configuring Crosstool-NG
-----------------------------

**List Available Samples:**

.. code-block:: bash

   # Show pre-configured toolchain samples
   ct-ng list-samples
   
   # Output includes:
   # [L...]   arm-cortex_a8-linux-gnueabi
   # [L...]   arm-unknown-linux-gnueabi
   # [L...]   aarch64-unknown-linux-gnu
   # [L.X.]   mips-unknown-linux-gnu
   # [L...]   powerpc-unknown-linux-gnu

**Configuration Workflow:**

.. code-block:: bash

   # Create build directory
   mkdir ~/toolchain-build
   cd ~/toolchain-build
   
   # Method 1: Start with a sample
   ct-ng arm-cortex_a8-linux-gnueabi
   
   # Method 2: Start from scratch
   ct-ng menuconfig
   
   # Customize configuration
   ct-ng menuconfig

**Key Configuration Options:**

.. code-block:: text

   Path and misc options
   ├── Prefix directory: /home/user/x-tools/${CT_TARGET}
   ├── Number of parallel jobs: 8
   └── Maximum log level: DEBUG
   
   Target options
   ├── Target Architecture: arm
   ├── Endianness: Little endian
   ├── Bitness: 32-bit
   ├── Architecture level: armv7-a
   ├── CPU: cortex-a8
   ├── FPU: neon
   └── Floating point: hardware (FPU)
   
   Toolchain options
   ├── Tuple's vendor string: custom (optional)
   └── Tuple's alias: arm-linux (optional)
   
   Operating System
   ├── Target OS: linux
   └── Kernel version: 4.1.52 (or latest LTS)
   
   Binary utilities
   └── binutils version: 2.36.1
   
   C compiler
   ├── gcc version: 9.3.0
   ├── C++: Enable
   ├── Link Time Optimization (LTO): Enable
   └── gcc extra config: (blank or custom flags)
   
   C library
   ├── C library: glibc / musl / uClibc-ng
   └── glibc version: 2.31 (if using glibc)

**Sample Configurations:**

.. code-block:: text

   # Raspberry Pi 3 (Cortex-A53, ARM64)
   Architecture: aarch64
   CPU: cortex-a53
   OS: linux
   C library: glibc 2.31
   Triple: aarch64-rpi3-linux-gnu
   
   # BeagleBone Black (Cortex-A8, ARM)
   Architecture: arm
   Architecture level: armv7-a
   CPU: cortex-a8
   FPU: neon
   Floating point: hardware
   OS: linux
   C library: glibc 2.31
   Triple: arm-bbb-linux-gnueabihf
   
   # MIPS Router (Big-endian)
   Architecture: mips
   Architecture level: mips32r2
   Endianness: Big endian
   OS: linux
   C library: musl
   Triple: mips-openwrt-linux-musl

3.3 Building the Toolchain
---------------------------

**Build Process:**

.. code-block:: bash

   # Review configuration
   ct-ng show-config
   
   # Start build (takes 30-90 minutes)
   ct-ng build
   
   # Build process stages:
   # 1. Download sources (binutils, gcc, glibc, kernel headers)
   # 2. Extract archives
   # 3. Build binutils (pass 1)
   # 4. Install kernel headers
   # 5. Build gcc (core, static)
   # 6. Build C library headers
   # 7. Build gcc (pass 2, with libgcc)
   # 8. Build C library (complete)
   # 9. Build gcc (final, with C++)
   # 10. Build additional libraries

**Build Output:**

.. code-block:: bash

   # Default installation location
   ls ~/x-tools/arm-bbb-linux-gnueabihf/
   # arm-bbb-linux-gnueabihf/  - sysroot
   # bin/                      - toolchain binaries
   # build.log.bz2             - build log
   # include/                  - host headers
   # lib/                      - host libraries
   # libexec/                  - gcc internals
   # share/                    - documentation, man pages
   
   # Toolchain binaries
   ls ~/x-tools/arm-bbb-linux-gnueabihf/bin/
   # arm-bbb-linux-gnueabihf-addr2line
   # arm-bbb-linux-gnueabihf-ar
   # arm-bbb-linux-gnueabihf-as
   # arm-bbb-linux-gnueabihf-cc -> arm-bbb-linux-gnueabihf-gcc
   # arm-bbb-linux-gnueabihf-c++
   # arm-bbb-linux-gnueabihf-gcc
   # arm-bbb-linux-gnueabihf-g++
   # arm-bbb-linux-gnueabihf-ld
   # arm-bbb-linux-gnueabihf-nm
   # arm-bbb-linux-gnueabihf-objcopy
   # arm-bbb-linux-gnueabihf-objdump
   # arm-bbb-linux-gnueabihf-ranlib
   # arm-bbb-linux-gnueabihf-readelf
   # arm-bbb-linux-gnueabihf-size
   # arm-bbb-linux-gnueabihf-strip

**Using the Built Toolchain:**

.. code-block:: bash

   # Add to PATH
   export PATH="${HOME}/x-tools/arm-bbb-linux-gnueabihf/bin:${PATH}"
   
   # Set environment variables
   export CROSS_COMPILE=arm-bbb-linux-gnueabihf-
   export CC=${CROSS_COMPILE}gcc
   export CXX=${CROSS_COMPILE}g++
   export AR=${CROSS_COMPILE}ar
   export LD=${CROSS_COMPILE}ld
   
   # Test compilation
   ${CC} --version
   # arm-bbb-linux-gnueabihf-gcc (crosstool-NG 1.24.0) 9.3.0
   
   ${CC} -o hello hello.c
   file hello
   # hello: ELF 32-bit LSB executable, ARM, EABI5 version 1

3.4 Troubleshooting Crosstool-NG Builds
----------------------------------------

**Common Issues:**

.. code-block:: text

   Problem: Build fails during GCC compilation
   Solution:
   - Check build.log.bz2 for errors
   - Increase system resources (RAM, swap)
   - Disable LTO if memory limited
   - Try older GCC version
   
   Problem: "configure: error: C compiler cannot create executables"
   Solution:
   - Install build-essential, gcc-multilib
   - Check PATH doesn't have spaces
   - Verify write permissions
   
   Problem: Download failures (404, timeouts)
   Solution:
   - Enable mirrors in menuconfig
   - Download manually to ~/src/
   - Check firewall/proxy settings
   
   Problem: Headers installation fails
   Solution:
   - Verify kernel version exists
   - Try LTS kernel version (4.19, 5.4, 5.10)
   - Check kernel.org mirrors

**Debugging Build Issues:**

.. code-block:: bash

   # View detailed log
   bunzip2 -c build.log.bz2 | less
   
   # Search for specific error
   bunzip2 -c build.log.bz2 | grep -i error | tail -50
   
   # Rebuild with more debug info
   ct-ng menuconfig  # Paths and misc -> Max log level: ALL
   rm -rf .build/    # Clean previous build
   ct-ng build
   
   # Keep build directory for inspection
   ct-ng menuconfig  # Paths and misc -> Remove build directories: NO
   ct-ng build

================================================================================
4. Sysroot and SDK Concepts
================================================================================

4.1 Sysroot Architecture
-------------------------

**What is Sysroot?**

The sysroot is a directory that contains a filesystem hierarchy for the target
system, including libraries, headers, and configuration files needed for linking.

**Sysroot Structure:**

.. code-block:: text

   ${SYSROOT}/
   ├── lib/                    # Target libraries
   │   ├── libc.so.6          # C library
   │   ├── libm.so.6          # Math library
   │   ├── libpthread.so.0    # POSIX threads
   │   ├── ld-linux-armhf.so.3  # Dynamic linker
   │   └── ...
   ├── usr/
   │   ├── include/           # Headers
   │   │   ├── stdio.h
   │   │   ├── stdlib.h
   │   │   ├── linux/         # Kernel headers
   │   │   └── sys/
   │   └── lib/               # Additional libraries
   │       ├── crt1.o         # C runtime startup
   │       ├── crti.o
   │       ├── crtn.o
   │       └── libstdc++.so   # C++ standard library
   ├── etc/                   # Configuration files (optional)
   └── var/                   # Variable data (optional)

**Locating Sysroot:**

.. code-block:: bash

   # Find sysroot location
   ${CROSS_COMPILE}gcc -print-sysroot
   # /home/user/x-tools/arm-bbb-linux-gnueabihf/arm-bbb-linux-gnueabihf/sysroot
   
   # List sysroot contents
   SYSROOT=$(${CROSS_COMPILE}gcc -print-sysroot)
   ls -la ${SYSROOT}/lib/
   
   # Find libc version
   ${CROSS_COMPILE}gcc -print-file-name=libc.so.6
   # /path/to/sysroot/lib/libc.so.6
   
   readelf -d ${SYSROOT}/lib/libc.so.6 | grep SONAME
   #  0x0000000e (SONAME)   Library soname: [libc.so.6]

4.2 Using --sysroot Flag
-------------------------

**Why --sysroot?**

.. code-block:: text

   Without --sysroot:
   ✗ Compiler looks for headers/libraries in host /usr/include, /usr/lib
   ✗ Links against wrong architecture libraries
   ✗ May succeed on host but fail on target
   
   With --sysroot:
   ✓ Compiler uses target libraries
   ✓ Correct architecture
   ✓ Proper library versions

**Compilation Examples:**

.. code-block:: bash

   # Explicit sysroot (recommended for clarity)
   arm-linux-gnueabihf-gcc \
       --sysroot=/path/to/sysroot \
       -o hello hello.c
   
   # Using environment variable
   export SYSROOT=/path/to/sysroot
   ${CROSS_COMPILE}gcc --sysroot=${SYSROOT} -o hello hello.c
   
   # Link with specific library
   ${CROSS_COMPILE}gcc \
       --sysroot=${SYSROOT} \
       -o myapp myapp.c \
       -lpthread          # Links with ${SYSROOT}/lib/libpthread.so
   
   # Custom library path
   ${CROSS_COMPILE}gcc \
       --sysroot=${SYSROOT} \
       -L${SYSROOT}/usr/lib/custom \
       -o myapp myapp.c \
       -lmycustomlib

**Sysroot Search Paths:**

.. code-block:: bash

   # Show library search paths
   ${CROSS_COMPILE}gcc --sysroot=${SYSROOT} -print-search-dirs
   
   # Output:
   # install: /home/user/x-tools/.../lib/gcc/arm-linux-gnueabihf/9.3.0/
   # programs: ...
   # libraries: =/home/user/sysroot/lib/:/home/user/sysroot/usr/lib/
   
   # Test library resolution
   ${CROSS_COMPILE}gcc --sysroot=${SYSROOT} -print-file-name=libm.so
   # /path/to/sysroot/lib/libm.so

4.3 SDK (Software Development Kit)
-----------------------------------

**SDK Components:**

.. code-block:: text

   SDK Package:
   ├── toolchain/              # Cross-compiler binaries
   │   └── bin/
   │       ├── arm-linux-gcc
   │       ├── arm-linux-g++
   │       └── ...
   ├── sysroot/                # Target libraries and headers
   │   ├── lib/
   │   └── usr/include/
   ├── environment-setup-*     # Environment script
   ├── site-config-*           # Autotools configuration
   └── version-*               # SDK version info

**Yocto Project SDK:**

.. code-block:: bash

   # Generate SDK with Yocto
   bitbake core-image-minimal -c populate_sdk
   
   # SDK installer created at:
   # tmp/deploy/sdk/poky-glibc-x86_64-core-image-minimal-cortexa9hf-neon-toolchain-2.7.sh
   
   # Install SDK
   ./poky-glibc-x86_64-core-image-minimal-cortexa9hf-neon-toolchain-2.7.sh
   # Enter installation directory: /opt/poky/2.7
   
   # Source environment setup
   source /opt/poky/2.7/environment-setup-cortexa9hf-neon-poky-linux-gnueabi
   
   # Environment variables set:
   # CC=arm-poky-linux-gnueabi-gcc -march=armv7-a -mfpu=neon ...
   # CXX=arm-poky-linux-gnueabi-g++ -march=armv7-a -mfpu=neon ...
   # CPP=arm-poky-linux-gnueabi-gcc -E ...
   # CFLAGS=-O2 -pipe -g ...
   # CXXFLAGS=-O2 -pipe -g ...
   # LDFLAGS=-Wl,-O1 -Wl,--hash-style=gnu ...
   # ARCH=arm
   # CROSS_COMPILE=arm-poky-linux-gnueabi-
   # OECORE_TARGET_SYSROOT=/opt/poky/2.7/sysroots/cortexa9hf-neon-poky-linux-gnueabi

**Buildroot SDK:**

.. code-block:: bash

   # Generate SDK with Buildroot
   make sdk
   
   # SDK created at:
   # output/images/arm-buildroot-linux-gnueabihf_sdk-buildroot.tar.gz
   
   # Extract SDK
   tar -xzf arm-buildroot-linux-gnueabihf_sdk-buildroot.tar.gz -C /opt/
   
   # Relocate SDK (run once after extraction)
   /opt/arm-buildroot-linux-gnueabihf_sdk-buildroot/relocate-sdk.sh
   
   # Add to PATH
   export PATH="/opt/arm-buildroot-linux-gnueabihf_sdk-buildroot/bin:${PATH}"

**Custom SDK Creation:**

.. code-block:: bash

   # Create minimal SDK directory structure
   mkdir -p /opt/my-sdk/{toolchain,sysroot}
   
   # Copy toolchain
   cp -r ~/x-tools/arm-linux-gnueabihf/* /opt/my-sdk/toolchain/
   
   # Create sysroot from target
   rsync -avz target:/lib /opt/my-sdk/sysroot/
   rsync -avz target:/usr/lib /opt/my-sdk/sysroot/usr/
   rsync -avz target:/usr/include /opt/my-sdk/sysroot/usr/
   
   # Create environment setup script
   cat > /opt/my-sdk/environment-setup << 'EOF'
   export SDK_ROOT=/opt/my-sdk
   export PATH="${SDK_ROOT}/toolchain/bin:${PATH}"
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export CC=${CROSS_COMPILE}gcc
   export CXX=${CROSS_COMPILE}g++
   export SYSROOT=${SDK_ROOT}/sysroot
   export CFLAGS="--sysroot=${SYSROOT}"
   export CXXFLAGS="--sysroot=${SYSROOT}"
   export LDFLAGS="--sysroot=${SYSROOT}"
   EOF
   
   # Use SDK
   source /opt/my-sdk/environment-setup
   ${CC} -o hello hello.c

4.4 Multilib Support
--------------------

**What is Multilib?**

Multilib allows a single toolchain to build for multiple library variants
(e.g., soft-float and hard-float, different ARM instruction sets).

**Multilib Example:**

.. code-block:: bash

   # Check multilib configurations
   ${CROSS_COMPILE}gcc -print-multi-lib
   
   # Example output for ARM:
   # .;
   # thumb;@mthumb
   # armv7-a;@march=armv7-a
   # armv7-a/thumb;@march=armv7-a@mthumb
   
   # This means toolchain supports:
   # 1. Default (ARM mode)
   # 2. Thumb mode
   # 3. ARMv7-A architecture
   # 4. ARMv7-A + Thumb

**Using Multilib:**

.. code-block:: bash

   # Compile for default configuration
   ${CROSS_COMPILE}gcc -o app app.c
   
   # Compile for Thumb mode
   ${CROSS_COMPILE}gcc -mthumb -o app_thumb app.c
   
   # Verify instruction set
   file app
   # app: ELF 32-bit LSB executable, ARM, EABI5 version 1
   
   file app_thumb
   # app_thumb: ELF 32-bit LSB executable, ARM, EABI5 version 1
   
   ${CROSS_COMPILE}readelf -A app | grep Tag_THUMB
   ${CROSS_COMPILE}readelf -A app_thumb | grep Tag_THUMB
   # Tag_THUMB_ISA_use: Thumb-2

**Multilib Library Locations:**

.. code-block:: bash

   # Show library paths for different multilib variants
   ${CROSS_COMPILE}gcc -print-multi-directory
   # .
   
   ${CROSS_COMPILE}gcc -mthumb -print-multi-directory
   # thumb
   
   # Libraries located at:
   # ${SYSROOT}/lib/          - default
   # ${SYSROOT}/lib/thumb/    - thumb variant

================================================================================
5. Cross-Compiling Applications and Libraries
================================================================================

5.1 Simple C/C++ Programs
--------------------------

**Basic Compilation:**

.. code-block:: bash

   # hello.c
   cat > hello.c << 'EOF'
   #include <stdio.h>
   
   int main(void) {
       printf("Hello from ARM!\n");
       return 0;
   }
   EOF
   
   # Compile
   ${CROSS_COMPILE}gcc -o hello hello.c
   
   # Verify architecture
   file hello
   # hello: ELF 32-bit LSB executable, ARM, EABI5 version 1
   
   # Check dynamic dependencies
   ${CROSS_COMPILE}readelf -d hello | grep NEEDED
   #  0x00000001 (NEEDED)    Shared library: [libc.so.6]

**Static vs Dynamic Linking:**

.. code-block:: bash

   # Dynamic linking (default)
   ${CROSS_COMPILE}gcc -o hello_dynamic hello.c
   ${CROSS_COMPILE}readelf -d hello_dynamic | grep NEEDED
   #  0x00000001 (NEEDED)    Shared library: [libc.so.6]
   
   ls -lh hello_dynamic
   # -rwxr-xr-x 1 user user 7.2K Jan 18 10:00 hello_dynamic
   
   # Static linking
   ${CROSS_COMPILE}gcc -static -o hello_static hello.c
   ${CROSS_COMPILE}readelf -d hello_static | grep NEEDED
   # (no output - no dynamic dependencies)
   
   ls -lh hello_static
   # -rwxr-xr-x 1 user user 612K Jan 18 10:00 hello_static
   
   # Trade-offs:
   # Dynamic: Small size, needs libraries on target
   # Static: Large size, self-contained, no library deps

**Multi-Source Projects:**

.. code-block:: bash

   # main.c
   cat > main.c << 'EOF'
   #include "utils.h"
   int main(void) {
       print_message();
       return 0;
   }
   EOF
   
   # utils.c
   cat > utils.c << 'EOF'
   #include <stdio.h>
   #include "utils.h"
   void print_message(void) {
       printf("Hello from utils!\n");
   }
   EOF
   
   # utils.h
   cat > utils.h << 'EOF'
   #ifndef UTILS_H
   #define UTILS_H
   void print_message(void);
   #endif
   EOF
   
   # Compile in steps
   ${CROSS_COMPILE}gcc -c main.c -o main.o
   ${CROSS_COMPILE}gcc -c utils.c -o utils.o
   ${CROSS_COMPILE}gcc main.o utils.o -o myapp
   
   # Or all at once
   ${CROSS_COMPILE}gcc main.c utils.c -o myapp

5.2 Cross-Compiling with Makefiles
-----------------------------------

**Simple Makefile:**

.. code-block:: makefile

   # Makefile for cross-compilation
   CROSS_COMPILE ?= arm-linux-gnueabihf-
   CC := $(CROSS_COMPILE)gcc
   CXX := $(CROSS_COMPILE)g++
   LD := $(CROSS_COMPILE)ld
   AR := $(CROSS_COMPILE)ar
   STRIP := $(CROSS_COMPILE)strip
   
   # Compiler flags
   CFLAGS := -Wall -O2 -march=armv7-a -mfpu=neon
   LDFLAGS :=
   LIBS := -lpthread -lm
   
   # Source files
   SRCS := main.c utils.c network.c
   OBJS := $(SRCS:.c=.o)
   TARGET := myapp
   
   # Build rules
   all: $(TARGET)
   
   $(TARGET): $(OBJS)
   	$(CC) $(LDFLAGS) -o $@ $^ $(LIBS)
   	$(STRIP) $@
   
   %.o: %.c
   	$(CC) $(CFLAGS) -c $< -o $@
   
   clean:
   	rm -f $(OBJS) $(TARGET)
   
   .PHONY: all clean

**Usage:**

.. code-block:: bash

   # Build with default toolchain
   make
   
   # Override toolchain
   make CROSS_COMPILE=aarch64-linux-gnu-
   
   # Verbose build
   make V=1
   
   # Parallel build
   make -j8

5.3 Autotools (configure) Projects
-----------------------------------

**Typical Autotools Project:**

.. code-block:: bash

   # Download source
   wget https://example.com/mylib-1.2.3.tar.gz
   tar -xzf mylib-1.2.3.tar.gz
   cd mylib-1.2.3
   
   # Configure for cross-compilation
   ./configure \
       --host=arm-linux-gnueabihf \
       --prefix=/usr \
       --enable-shared \
       --disable-static \
       CC=arm-linux-gnueabihf-gcc \
       CXX=arm-linux-gnueabihf-g++ \
       CFLAGS="-O2 -march=armv7-a" \
       LDFLAGS="-Wl,-rpath-link=${SYSROOT}/lib"
   
   # Build
   make -j$(nproc)
   
   # Install to staging area
   make DESTDIR=/path/to/staging install

**Key Configure Options:**

.. code-block:: text

   --host=<triple>         Target architecture (required for cross)
   --build=<triple>        Build machine (auto-detected)
   --prefix=<path>         Installation prefix (/usr, /usr/local)
   --enable-shared         Build shared libraries
   --disable-static        Don't build static libraries
   --with-sysroot=<path>   Specify sysroot
   CC, CXX, LD, AR         Toolchain executables
   CFLAGS, CXXFLAGS        Compiler flags
   LDFLAGS                 Linker flags

**Common Patterns:**

.. code-block:: bash

   # Using pkg-config for dependencies
   export PKG_CONFIG_PATH="${SYSROOT}/usr/lib/pkgconfig"
   export PKG_CONFIG_SYSROOT_DIR="${SYSROOT}"
   ./configure --host=arm-linux-gnueabihf ...
   
   # Disable features not needed
   ./configure \
       --host=arm-linux-gnueabihf \
       --disable-nls \          # No native language support
       --disable-docs \         # No documentation
       --without-x \            # No X11
       --disable-examples       # No examples

5.4 CMake Projects
------------------

**CMake Toolchain File:**

.. code-block:: cmake

   # arm-linux-toolchain.cmake
   set(CMAKE_SYSTEM_NAME Linux)
   set(CMAKE_SYSTEM_PROCESSOR arm)
   
   # Specify the cross compiler
   set(CMAKE_C_COMPILER   arm-linux-gnueabihf-gcc)
   set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)
   
   # Where to look for the target environment
   set(CMAKE_FIND_ROOT_PATH /path/to/sysroot)
   
   # Search for programs in the build host directories
   set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
   
   # Search for libraries and headers in the target directories
   set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
   set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
   set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
   
   # Compiler flags
   set(CMAKE_C_FLAGS "-march=armv7-a -mfpu=neon" CACHE STRING "" FORCE)
   set(CMAKE_CXX_FLAGS "-march=armv7-a -mfpu=neon" CACHE STRING "" FORCE)

**Build with CMake:**

.. code-block:: bash

   # Create build directory
   mkdir build-arm
   cd build-arm
   
   # Configure with toolchain file
   cmake .. \
       -DCMAKE_TOOLCHAIN_FILE=../arm-linux-toolchain.cmake \
       -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_INSTALL_PREFIX=/usr
   
   # Build
   make -j$(nproc)
   
   # Install to staging
   make DESTDIR=/path/to/staging install

**Inline Toolchain Specification:**

.. code-block:: bash

   # Without separate toolchain file
   cmake .. \
       -DCMAKE_SYSTEM_NAME=Linux \
       -DCMAKE_SYSTEM_PROCESSOR=arm \
       -DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc \
       -DCMAKE_CXX_COMPILER=arm-linux-gnueabihf-g++ \
       -DCMAKE_FIND_ROOT_PATH=/path/to/sysroot

================================================================================
6. Advanced Toolchain Topics
================================================================================

6.1 Canadian Cross
------------------

**What is Canadian Cross?**

Building a cross-compiler on one platform that runs on a second platform
and generates code for a third platform.

.. code-block:: text

   Build:  x86_64 Linux  (where compilation happens)
   Host:   Windows       (where compiler will run)
   Target: ARM Linux     (what compiler produces code for)
   
   Result: Windows executable that cross-compiles for ARM Linux

**Crosstool-NG Canadian Cross:**

.. code-block:: bash

   ct-ng menuconfig
   
   # Canadian Cross options:
   # - Build: x86_64-build_pc-linux-gnu (auto)
   # - Host:  i686-w64-mingw32 (Windows)
   # - Target: arm-unknown-linux-gnueabihf
   
   # Requires:
   # - Host toolchain (MinGW for Windows on Linux)
   # - More build time (3x longer)

6.2 QEMU for Testing
--------------------

**User-Mode QEMU:**

Run ARM binaries on x86_64 host for quick testing.

.. code-block:: bash

   # Install QEMU user-mode
   sudo apt-get install qemu-user-static
   
   # Run ARM binary
   qemu-arm-static -L ${SYSROOT} ./hello_arm
   # Hello from ARM!
   
   # Run with GDB
   qemu-arm-static -g 1234 -L ${SYSROOT} ./hello_arm &
   arm-linux-gnueabihf-gdb hello_arm
   # (gdb) target remote localhost:1234

**System-Mode QEMU:**

.. code-block:: bash

   # Boot ARM Linux in QEMU
   qemu-system-arm \
       -M vexpress-a9 \
       -kernel zImage \
       -dtb vexpress-v2p-ca9.dtb \
       -drive file=rootfs.ext4,if=sd,format=raw \
       -append "console=ttyAMA0 root=/dev/mmcblk0" \
       -nographic \
       -net nic -net user,hostfwd=tcp::2222-:22

6.3 Library Dependencies
------------------------

**Checking Dependencies:**

.. code-block:: bash

   # List dynamic library dependencies
   ${CROSS_COMPILE}readelf -d myapp | grep NEEDED
   #  0x00000001 (NEEDED)    Shared library: [libpthread.so.0]
   #  0x00000001 (NEEDED)    Shared library: [libm.so.6]
   #  0x00000001 (NEEDED)    Shared library: [libc.so.6]
   
   # Alternative: ldd (on target or with QEMU)
   qemu-arm-static -L ${SYSROOT} ldd ./myapp
   # libpthread.so.0 => /lib/libpthread.so.0
   # libm.so.6 => /lib/libm.so.6
   # libc.so.6 => /lib/libc.so.6
   # /lib/ld-linux-armhf.so.3

**Resolving Missing Libraries:**

.. code-block:: bash

   # Error: cannot find -lmylib
   # Solutions:
   
   # 1. Install library in sysroot
   cp libmylib.so ${SYSROOT}/usr/lib/
   
   # 2. Add library path
   ${CROSS_COMPILE}gcc -L/path/to/libs -o myapp myapp.c -lmylib
   
   # 3. Use pkg-config
   export PKG_CONFIG_PATH="${SYSROOT}/usr/lib/pkgconfig"
   ${CROSS_COMPILE}gcc $(pkg-config --cflags --libs mylib) -o myapp myapp.c

6.4 Optimizing for Size
------------------------

**Size Optimization Techniques:**

.. code-block:: bash

   # 1. Use -Os flag
   ${CROSS_COMPILE}gcc -Os -o myapp myapp.c
   
   # 2. Strip debug symbols
   ${CROSS_COMPILE}strip myapp
   
   # 3. Use smaller C library (musl or uClibc-ng)
   # Build with musl toolchain instead of glibc
   
   # 4. Link-Time Optimization (LTO)
   ${CROSS_COMPILE}gcc -Os -flto -o myapp myapp.c
   
   # 5. Remove unused functions
   ${CROSS_COMPILE}gcc -Os -ffunction-sections -fdata-sections \
       -Wl,--gc-sections -o myapp myapp.c
   
   # 6. Static linking with size optimization
   ${CROSS_COMPILE}gcc -Os -static -flto \
       -ffunction-sections -fdata-sections \
       -Wl,--gc-sections -o myapp myapp.c
   
   # Compare sizes:
   # Original (dynamic, -O2):     45 KB
   # -Os (dynamic):               32 KB
   # -Os + strip:                 28 KB
   # -Os + LTO + gc-sections:     18 KB

**Size Analysis:**

.. code-block:: bash

   # Show section sizes
   ${CROSS_COMPILE}size myapp
   #    text    data     bss     dec     hex filename
   #   12345    2048    1024   15417    3c39 myapp
   
   # Detailed section breakdown
   ${CROSS_COMPILE}objdump -h myapp
   
   # Find largest symbols
   ${CROSS_COMPILE}nm --size-sort -S myapp | tail -20

================================================================================
7. Practical Examples
================================================================================

7.1 Complete Build Example: Hello World with Threads
-----------------------------------------------------

**Source Code:**

.. code-block:: c

   // hello_threads.c
   #include <stdio.h>
   #include <pthread.h>
   #include <unistd.h>
   
   void *thread_func(void *arg) {
       int id = *(int *)arg;
       printf("Thread %d running\n", id);
       sleep(1);
       printf("Thread %d exiting\n", id);
       return NULL;
   }
   
   int main(void) {
       pthread_t threads[3];
       int ids[3] = {1, 2, 3};
       
       printf("Hello from ARM with threads!\n");
       
       for (int i = 0; i < 3; i++) {
           pthread_create(&threads[i], NULL, thread_func, &ids[i]);
       }
       
       for (int i = 0; i < 3; i++) {
           pthread_join(threads[i], NULL);
       }
       
       printf("All threads completed\n");
       return 0;
   }

**Build and Test:**

.. code-block:: bash

   # Set up environment
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export SYSROOT=$(${CROSS_COMPILE}gcc -print-sysroot)
   
   # Compile with pthread
   ${CROSS_COMPILE}gcc \
       --sysroot=${SYSROOT} \
       -Wall -O2 \
       -march=armv7-a \
       -o hello_threads hello_threads.c \
       -lpthread
   
   # Verify
   file hello_threads
   # hello_threads: ELF 32-bit LSB executable, ARM, EABI5 version 1
   
   ${CROSS_COMPILE}readelf -d hello_threads | grep NEEDED
   #  0x00000001 (NEEDED)    Shared library: [libpthread.so.0]
   #  0x00000001 (NEEDED)    Shared library: [libc.so.6]
   
   # Test with QEMU
   qemu-arm-static -L ${SYSROOT} ./hello_threads
   # Hello from ARM with threads!
   # Thread 1 running
   # Thread 2 running
   # Thread 3 running
   # Thread 1 exiting
   # Thread 2 exiting
   # Thread 3 exiting
   # All threads completed

7.2 Building Third-Party Library (libpng)
------------------------------------------

**Step-by-Step Build:**

.. code-block:: bash

   # Prerequisites: zlib (libpng depends on it)
   
   # 1. Build zlib
   wget https://zlib.net/zlib-1.2.11.tar.gz
   tar -xzf zlib-1.2.11.tar.gz
   cd zlib-1.2.11
   
   CC=${CROSS_COMPILE}gcc \
   AR=${CROSS_COMPILE}ar \
   RANLIB=${CROSS_COMPILE}ranlib \
   ./configure --prefix=/usr
   
   make -j$(nproc)
   make DESTDIR=${SYSROOT} install
   cd ..
   
   # 2. Build libpng
   wget https://download.sourceforge.net/libpng/libpng-1.6.37.tar.gz
   tar -xzf libpng-1.6.37.tar.gz
   cd libpng-1.6.37
   
   ./configure \
       --host=arm-linux-gnueabihf \
       --prefix=/usr \
       --enable-shared \
       CC=${CROSS_COMPILE}gcc \
       CFLAGS="--sysroot=${SYSROOT} -O2" \
       LDFLAGS="--sysroot=${SYSROOT}"
   
   make -j$(nproc)
   make DESTDIR=${SYSROOT} install
   cd ..
   
   # 3. Use in application
   cat > png_example.c << 'EOF'
   #include <png.h>
   #include <stdio.h>
   
   int main(void) {
       printf("libpng version: %s\n", PNG_LIBPNG_VER_STRING);
       return 0;
   }
   EOF
   
   ${CROSS_COMPILE}gcc \
       --sysroot=${SYSROOT} \
       -o png_example png_example.c \
       -lpng -lz
   
   qemu-arm-static -L ${SYSROOT} ./png_example
   # libpng version: 1.6.37

================================================================================
8. Best Practices and Troubleshooting
================================================================================

8.1 Best Practices
------------------

.. code-block:: text

   ✓ Version Management
   - Use matching toolchain, kernel, and library versions
   - Document toolchain version in project
   - Use version control for toolchain configuration
   
   ✓ Sysroot Management
   - Keep sysroot separate from target rootfs
   - Never modify sysroot manually during build
   - Use DESTDIR for staging installations
   
   ✓ Build Reproducibility
   - Use SDK or documented toolchain build process
   - Set explicit compiler flags in build system
   - Avoid host contamination (check /usr/include, /usr/lib)
   
   ✓ Testing
   - Test on QEMU before hardware
   - Verify library dependencies match target
   - Check binary for correct architecture/ABI
   
   ✓ Size Optimization
   - Use -Os for embedded systems
   - Strip binaries before deployment
   - Consider static linking for single-app systems

8.2 Common Errors and Solutions
--------------------------------

**Error 1: Exec format error**

.. code-block:: bash

   $ ./hello_arm
   bash: ./hello_arm: cannot execute binary file: Exec format error
   
   # Cause: Running ARM binary on x86_64 host
   # Solution: Use QEMU or run on target
   qemu-arm-static -L ${SYSROOT} ./hello_arm

**Error 2: Shared library not found**

.. code-block:: bash

   $ qemu-arm-static ./hello_arm
   /lib/ld-linux-armhf.so.3: No such file or directory
   
   # Cause: Missing sysroot specification
   # Solution: Use -L flag
   qemu-arm-static -L ${SYSROOT} ./hello_arm

**Error 3: Undefined reference**

.. code-block:: bash

   undefined reference to `pthread_create'
   
   # Cause: Missing library link
   # Solution: Add -lpthread
   ${CROSS_COMPILE}gcc -o myapp myapp.c -lpthread

**Error 4: Wrong architecture**

.. code-block:: bash

   ld: error: mylib.a(mylib.o) uses VFP register arguments, 
   myapp.o does not
   
   # Cause: Mismatched ABI (hard-float vs soft-float)
   # Solution: Use consistent toolchain (gnueabihf vs gnueabi)
   # Rebuild all components with same ABI

**Error 5: Configure fails to detect cross-compiler**

.. code-block:: bash

   configure: error: C compiler cannot create executables
   
   # Cause: Wrong --host triple or missing dependencies
   # Solutions:
   # 1. Check --host matches toolchain exactly
   ./configure --host=arm-linux-gnueabihf  # Match `arm-linux-gnueabihf-gcc`
   
   # 2. Verify toolchain in PATH
   which ${CROSS_COMPILE}gcc
   
   # 3. Check config.log for specific error
   tail config.log

8.3 Debugging Cross-Compilation Issues
---------------------------------------

**Verbose Build Output:**

.. code-block:: bash

   # Enable verbose Makefile
   make V=1
   
   # Autotools verbose
   ./configure --host=arm-linux-gnueabihf ...
   make V=1 VERBOSE=1
   
   # CMake verbose
   cmake .. -DCMAKE_VERBOSE_MAKEFILE=ON
   make VERBOSE=1

**Check Compiler Behavior:**

.. code-block:: bash

   # Show preprocessor defines
   ${CROSS_COMPILE}gcc -dM -E - < /dev/null | grep -i arm
   # #define __ARM_ARCH 7
   # #define __ARM_ARCH_7A__ 1
   # #define __ARM_EABI__ 1
   
   # Show include paths
   ${CROSS_COMPILE}gcc -xc -E -v - < /dev/null 2>&1 | grep "^ "
   
   # Show library search paths
   ${CROSS_COMPILE}gcc -print-search-dirs

**Trace Library Loading:**

.. code-block:: bash

   # On target (or QEMU)
   LD_DEBUG=libs ./myapp
   # Shows library search and loading process

================================================================================
9. Exam-Style Questions
================================================================================

**Question 1:** What are the four essential components of a cross-compilation
toolchain?

**Answer:** 1) GCC (compiler), 2) Binutils (as, ld, ar, etc.), 3) C standard
library (glibc/musl/uClibc-ng), 4) Linux kernel headers

---

**Question 2:** Explain the difference between gnueabi and gnueabihf ARM ABIs.

**Answer:** gnueabi uses software floating-point (slower, compatible), gnueabihf
uses hardware floating-point with VFP/NEON (faster, requires FPU in hardware).

---

**Question 3:** What is a sysroot and why is it important?

**Answer:** Sysroot is a directory containing target system's libraries and
headers. It prevents the compiler from accidentally linking against host
libraries, ensuring binaries use correct architecture and library versions.

---

**Question 4:** Write the command to cross-compile a C program using sysroot.

**Answer:**
.. code-block:: bash

   arm-linux-gnueabihf-gcc --sysroot=/path/to/sysroot -o myapp myapp.c -lpthread

---

**Question 5:** How do you determine which dynamic libraries an ELF binary needs?

**Answer:**
.. code-block:: bash

   ${CROSS_COMPILE}readelf -d binary | grep NEEDED
   # or on target/QEMU:
   ldd binary

---

**Question 6:** What is the purpose of the --host flag in autotools configure?

**Answer:** Specifies the target architecture for cross-compilation. Format is
<arch>-<vendor>-<kernel>-<os>, e.g., arm-linux-gnueabihf.

---

**Question 7:** Compare static and dynamic linking for embedded systems.

**Answer:**
- Static: Larger binary, no runtime dependencies, self-contained, easier deployment
- Dynamic: Smaller binary, shared libraries save RAM/storage, easier updates

---

**Question 8:** How do you optimize binary size for embedded systems?

**Answer:** Use -Os flag, strip debug symbols, enable LTO, use --gc-sections,
choose smaller C library (musl/uClibc-ng), consider static linking.

---

**Question 9:** What is Canadian Cross compilation?

**Answer:** Building a cross-compiler on platform A that runs on platform B
and generates code for platform C (e.g., build on Linux, runs on Windows,
compiles for ARM).

---

**Question 10:** How do you verify the architecture of a compiled binary?

**Answer:**
.. code-block:: bash

   file binary  # Shows: ELF 32-bit LSB executable, ARM...
   ${CROSS_COMPILE}readelf -h binary  # Shows detailed ELF header

================================================================================
10. Key Takeaways
================================================================================

.. code-block:: text

   Essential Concepts:
   ==================
   1. Cross-compilation builds on host (fast x86) for target (ARM/MIPS/etc)
   2. Toolchain has 4 parts: GCC, binutils, C library, kernel headers
   3. Triple format: <arch>-<vendor>-<kernel>-<os>
   4. Sysroot contains target libraries/headers, use --sysroot flag
   5. ABI matters: gnueabi (soft-float) vs gnueabihf (hard-float)
   
   Practical Commands:
   ===================
   # Setup
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export SYSROOT=$(${CROSS_COMPILE}gcc -print-sysroot)
   
   # Build
   ${CROSS_COMPILE}gcc --sysroot=${SYSROOT} -o app app.c -lpthread
   
   # Verify
   file app
   ${CROSS_COMPILE}readelf -d app | grep NEEDED
   
   # Test
   qemu-arm-static -L ${SYSROOT} ./app
   
   Toolchain Building:
   ===================
   - Use Crosstool-NG for custom toolchains
   - Use SDK from Yocto/Buildroot for projects
   - Match kernel headers version to target kernel
   - Choose C library based on size/features needed
   
   Build Systems:
   ==============
   - Makefiles: Set CC, CROSS_COMPILE, CFLAGS
   - Autotools: Use --host, CC, --sysroot
   - CMake: Use toolchain file with CMAKE_SYSTEM_NAME
   
   Common Pitfalls:
   ================
   ✗ Linking against host libraries (/usr/lib)
   ✗ ABI mismatch (gnueabi vs gnueabihf)
   ✗ Missing --sysroot flag
   ✗ Kernel headers newer than target kernel
   ✗ Running ARM binary on x86 without QEMU

================================================================================
END OF CHEATSHEET
================================================================================





