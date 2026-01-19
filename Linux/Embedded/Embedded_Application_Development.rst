================================================================================
Embedded Linux: Application Development - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 1 Ch12-13, Module 2 Ch5)
:Target: Embedded Linux Application Development
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Build Systems Quick Reference:**

.. code-block:: bash

   # Makefile (Simple)
   CC := arm-linux-gnueabihf-gcc
   CFLAGS := -Wall -O2
   myapp: myapp.c
       $(CC) $(CFLAGS) -o $@ $<
   
   # Autotools
   ./configure --host=arm-linux-gnueabihf --prefix=/usr
   make
   make install DESTDIR=/path/to/rootfs
   
   # CMake
   mkdir build && cd build
   cmake -DCMAKE_TOOLCHAIN_FILE=../toolchain.cmake ..
   make
   make install DESTDIR=/path/to/rootfs
   
   # Meson
   meson setup builddir --cross-file cross-arm.ini
   ninja -C builddir
   meson install -C builddir --destdir=/path/to/rootfs

**CMake Toolchain File:**

.. code-block:: cmake

   # toolchain-arm.cmake
   set(CMAKE_SYSTEM_NAME Linux)
   set(CMAKE_SYSTEM_PROCESSOR arm)
   
   set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
   set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)
   
   set(CMAKE_FIND_ROOT_PATH /path/to/sysroot)
   set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
   set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
   set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

**Yocto Recipe Template:**

.. code-block:: bitbake

   # myapp_1.0.bb
   SUMMARY = "My Application"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://LICENSE;md5=..."
   
   SRC_URI = "git://github.com/user/myapp.git;protocol=https;branch=main"
   SRCREV = "${AUTOREV}"
   S = "${WORKDIR}/git"
   
   inherit cmake
   DEPENDS = "libpng zlib"
   RDEPENDS_${PN} = "libpng zlib"
   
   do_install_append() {
       install -d ${D}${sysconfdir}/myapp
       install -m 0644 ${S}/config.conf ${D}${sysconfdir}/myapp/
   }

================================================================================
1. Build Systems Overview
================================================================================

1.1 Build System Comparison
----------------------------

**Build System Selection:**

.. code-block:: text

   Make:
   ✓ Simple, universal
   ✓ Low overhead
   ✗ Manual dependency tracking
   ✗ Platform-specific
   Use: Small projects, custom builds
   
   Autotools (autoconf/automake):
   ✓ Portable across platforms
   ✓ Feature detection
   ✗ Complex, steep learning curve
   ✗ Slow configure phase
   Use: GNU-style projects, portability needed
   
   CMake:
   ✓ Modern, clean syntax
   ✓ Good IDE support
   ✓ Fast, parallel builds
   ✗ Learning curve
   Use: Cross-platform C/C++ projects
   
   Meson:
   ✓ Very fast
   ✓ Simple syntax
   ✓ Good cross-compilation
   ✗ Newer, less widespread
   Use: Modern projects, performance-critical builds
   
   Yocto/BitBake:
   ✓ Complete system integration
   ✓ Dependency management
   ✓ Reproducible builds
   ✗ Complex infrastructure
   Use: Full embedded Linux distributions

1.2 Cross-Compilation Basics
-----------------------------

**Environment Setup:**

.. code-block:: bash

   # SDK environment
   source /opt/poky/4.0/environment-setup-cortexa8hf-neon-poky-linux-gnueabi
   
   # Manual setup
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export CC=${CROSS_COMPILE}gcc
   export CXX=${CROSS_COMPILE}g++
   export AR=${CROSS_COMPILE}ar
   export LD=${CROSS_COMPILE}ld
   export STRIP=${CROSS_COMPILE}strip
   
   export ARCH=arm
   export SYSROOT=/path/to/sysroot
   export PKG_CONFIG_PATH=$SYSROOT/usr/lib/pkgconfig
   export PKG_CONFIG_SYSROOT_DIR=$SYSROOT

**pkg-config for Cross-Compilation:**

.. code-block:: bash

   # Create pkg-config wrapper: arm-pkg-config
   #!/bin/sh
   export PKG_CONFIG_PATH=/path/to/sysroot/usr/lib/pkgconfig
   export PKG_CONFIG_SYSROOT_DIR=/path/to/sysroot
   exec pkg-config "$@"
   
   # Use in build
   CFLAGS=$(arm-pkg-config --cflags libpng)
   LIBS=$(arm-pkg-config --libs libpng)

================================================================================
2. Makefile-Based Projects
================================================================================

2.1 Simple Makefile
-------------------

**Basic Application:**

.. code-block:: make

   # Makefile
   CC := arm-linux-gnueabihf-gcc
   CFLAGS := -Wall -Werror -O2 -g
   LDFLAGS := -lpthread -lm
   
   TARGET := myapp
   SRCS := main.c utils.c device.c
   OBJS := $(SRCS:.c=.o)
   
   all: $(TARGET)
   
   $(TARGET): $(OBJS)
   	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
   
   %.o: %.c
   	$(CC) $(CFLAGS) -c -o $@ $<
   
   clean:
   	rm -f $(TARGET) $(OBJS)
   
   install: $(TARGET)
   	install -d $(DESTDIR)/usr/bin
   	install -m 0755 $(TARGET) $(DESTDIR)/usr/bin/
   
   .PHONY: all clean install

**Advanced Makefile:**

.. code-block:: make

   # Cross-compilation support
   CROSS_COMPILE ?= arm-linux-gnueabihf-
   CC := $(CROSS_COMPILE)gcc
   CXX := $(CROSS_COMPILE)g++
   AR := $(CROSS_COMPILE)ar
   STRIP := $(CROSS_COMPILE)strip
   
   # Directories
   SRCDIR := src
   BUILDDIR := build
   INCDIR := include
   
   # Compiler flags
   CFLAGS := -Wall -Werror -I$(INCDIR)
   CFLAGS += $(shell pkg-config --cflags libpng zlib)
   
   LDFLAGS := $(shell pkg-config --libs libpng zlib)
   LDFLAGS += -lpthread -lm
   
   # Debug/Release
   DEBUG ?= 0
   ifeq ($(DEBUG), 1)
       CFLAGS += -g -O0 -DDEBUG
   else
       CFLAGS += -O2 -DNDEBUG
   endif
   
   # Source files
   SRCS := $(wildcard $(SRCDIR)/*.c)
   OBJS := $(patsubst $(SRCDIR)/%.c,$(BUILDDIR)/%.o,$(SRCS))
   DEPS := $(OBJS:.o=.d)
   
   TARGET := myapp
   
   all: $(TARGET)
   
   $(TARGET): $(OBJS)
   	$(CC) -o $@ $^ $(LDFLAGS)
   	$(STRIP) $@
   
   $(BUILDDIR)/%.o: $(SRCDIR)/%.c | $(BUILDDIR)
   	$(CC) $(CFLAGS) -MMD -MP -c -o $@ $<
   
   $(BUILDDIR):
   	mkdir -p $@
   
   -include $(DEPS)
   
   clean:
   	rm -rf $(BUILDDIR) $(TARGET)
   
   install: $(TARGET)
   	install -D -m 0755 $(TARGET) $(DESTDIR)/usr/bin/$(TARGET)
   
   .PHONY: all clean install

2.2 Library Creation
---------------------

**Static Library:**

.. code-block:: make

   # Makefile for libmylib.a
   AR := arm-linux-gnueabihf-ar
   CC := arm-linux-gnueabihf-gcc
   CFLAGS := -Wall -O2 -fPIC
   
   SRCS := lib1.c lib2.c lib3.c
   OBJS := $(SRCS:.c=.o)
   
   LIBNAME := libmylib.a
   
   all: $(LIBNAME)
   
   $(LIBNAME): $(OBJS)
   	$(AR) rcs $@ $^
   
   %.o: %.c
   	$(CC) $(CFLAGS) -c -o $@ $<
   
   install: $(LIBNAME)
   	install -D -m 0644 $(LIBNAME) $(DESTDIR)/usr/lib/$(LIBNAME)
   	install -D -m 0644 mylib.h $(DESTDIR)/usr/include/mylib.h
   
   clean:
   	rm -f $(OBJS) $(LIBNAME)

**Shared Library:**

.. code-block:: make

   # Makefile for libmylib.so
   CC := arm-linux-gnueabihf-gcc
   CFLAGS := -Wall -O2 -fPIC
   LDFLAGS := -shared
   
   MAJOR := 1
   MINOR := 0
   PATCH := 0
   
   SRCS := lib1.c lib2.c lib3.c
   OBJS := $(SRCS:.c=.o)
   
   LIBNAME := libmylib.so
   SONAME := $(LIBNAME).$(MAJOR)
   REALNAME := $(SONAME).$(MINOR).$(PATCH)
   
   all: $(REALNAME)
   
   $(REALNAME): $(OBJS)
   	$(CC) $(LDFLAGS) -Wl,-soname,$(SONAME) -o $@ $^
   	ln -sf $(REALNAME) $(SONAME)
   	ln -sf $(SONAME) $(LIBNAME)
   
   %.o: %.c
   	$(CC) $(CFLAGS) -c -o $@ $<
   
   install: $(REALNAME)
   	install -D -m 0755 $(REALNAME) $(DESTDIR)/usr/lib/$(REALNAME)
   	ln -sf $(REALNAME) $(DESTDIR)/usr/lib/$(SONAME)
   	ln -sf $(SONAME) $(DESTDIR)/usr/lib/$(LIBNAME)
   	install -D -m 0644 mylib.h $(DESTDIR)/usr/include/mylib.h
   	ldconfig -n $(DESTDIR)/usr/lib
   
   clean:
   	rm -f $(OBJS) $(REALNAME) $(SONAME) $(LIBNAME)

================================================================================
3. Autotools Projects
================================================================================

3.1 Autotools Structure
------------------------

**Project Layout:**

.. code-block:: text

   myproject/
   ├── configure.ac          # Autoconf input
   ├── Makefile.am           # Automake input
   ├── src/
   │   ├── Makefile.am
   │   ├── main.c
   │   └── utils.c
   ├── include/
   │   └── myapp.h
   ├── lib/
   │   └── Makefile.am
   ├── tests/
   │   └── Makefile.am
   └── README

**configure.ac:**

.. code-block:: autoconf

   AC_INIT([myapp], [1.0], [support@example.com])
   AM_INIT_AUTOMAKE([-Wall -Werror foreign])
   AC_PROG_CC
   AC_CONFIG_HEADERS([config.h])
   AC_CONFIG_FILES([
       Makefile
       src/Makefile
   ])
   
   # Check for libraries
   AC_CHECK_LIB([pthread], [pthread_create])
   AC_CHECK_LIB([m], [sqrt])
   
   # pkg-config checks
   PKG_CHECK_MODULES([LIBPNG], [libpng >= 1.6])
   PKG_CHECK_MODULES([ZLIB], [zlib])
   
   # Optional features
   AC_ARG_ENABLE([debug],
       AS_HELP_STRING([--enable-debug], [Enable debug mode]))
   
   AS_IF([test "x$enable_debug" = "xyes"], [
       AC_DEFINE([DEBUG], [1], [Debug mode])
       CFLAGS="$CFLAGS -g -O0"
   ], [
       CFLAGS="$CFLAGS -O2"
   ])
   
   AC_OUTPUT

**Makefile.am (top-level):**

.. code-block:: automake

   SUBDIRS = src
   
   ACLOCAL_AMFLAGS = -I m4
   
   dist_doc_DATA = README
   
   EXTRA_DIST = autogen.sh

**src/Makefile.am:**

.. code-block:: automake

   bin_PROGRAMS = myapp
   
   myapp_SOURCES = main.c utils.c utils.h
   myapp_CFLAGS = $(LIBPNG_CFLAGS) $(ZLIB_CFLAGS) -I$(top_srcdir)/include
   myapp_LDADD = $(LIBPNG_LIBS) $(ZLIB_LIBS) -lpthread -lm

3.2 Building Autotools Projects
--------------------------------

**Bootstrap and Build:**

.. code-block:: bash

   # Generate configure script
   autoreconf -i
   
   # Native build
   ./configure
   make
   sudo make install
   
   # Cross-compile
   ./configure --host=arm-linux-gnueabihf \
               --prefix=/usr \
               --sysconfdir=/etc
   make
   make install DESTDIR=/path/to/rootfs
   
   # With SDK
   source /opt/poky/4.0/environment-setup-*
   ./configure $CONFIGURE_FLAGS
   make
   make install DESTDIR=/path/to/rootfs

================================================================================
4. CMake Projects
================================================================================

4.1 CMake Basics
----------------

**CMakeLists.txt (Simple):**

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.10)
   project(myapp VERSION 1.0 LANGUAGES C CXX)
   
   # Compiler flags
   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Werror")
   set(CMAKE_C_FLAGS_DEBUG "-g -O0")
   set(CMAKE_C_FLAGS_RELEASE "-O2 -DNDEBUG")
   
   # Find packages
   find_package(Threads REQUIRED)
   find_package(PNG REQUIRED)
   find_package(ZLIB REQUIRED)
   
   # Executable
   add_executable(myapp
       src/main.c
       src/utils.c
       src/device.c
   )
   
   target_include_directories(myapp PRIVATE
       ${CMAKE_SOURCE_DIR}/include
       ${PNG_INCLUDE_DIRS}
       ${ZLIB_INCLUDE_DIRS}
   )
   
   target_link_libraries(myapp
       Threads::Threads
       PNG::PNG
       ZLIB::ZLIB
       m
   )
   
   # Install
   install(TARGETS myapp DESTINATION bin)
   install(FILES config.conf DESTINATION etc/myapp)

**CMakeLists.txt (Advanced):**

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.16)
   project(myapp VERSION 1.0.0 LANGUAGES C CXX)
   
   # Options
   option(BUILD_SHARED_LIBS "Build shared libraries" ON)
   option(ENABLE_TESTS "Enable testing" OFF)
   option(ENABLE_DEBUG "Enable debug mode" OFF)
   
   # C++ standard
   set(CMAKE_CXX_STANDARD 17)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   
   # Build type
   if(ENABLE_DEBUG)
       set(CMAKE_BUILD_TYPE Debug)
   else()
       set(CMAKE_BUILD_TYPE Release)
   endif()
   
   # Find packages
   find_package(PkgConfig REQUIRED)
   pkg_check_modules(LIBPNG REQUIRED libpng>=1.6)
   pkg_check_modules(GLIB REQUIRED glib-2.0)
   
   # Library
   add_library(mylib
       src/lib1.c
       src/lib2.c
   )
   
   target_include_directories(mylib PUBLIC
       $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
       $<INSTALL_INTERFACE:include>
       ${LIBPNG_INCLUDE_DIRS}
   )
   
   target_link_libraries(mylib PUBLIC
       ${LIBPNG_LIBRARIES}
       ${GLIB_LIBRARIES}
   )
   
   # Executable
   add_executable(myapp src/main.c)
   target_link_libraries(myapp PRIVATE mylib)
   
   # Testing
   if(ENABLE_TESTS)
       enable_testing()
       add_subdirectory(tests)
   endif()
   
   # Install
   install(TARGETS myapp mylib
       RUNTIME DESTINATION bin
       LIBRARY DESTINATION lib
       ARCHIVE DESTINATION lib
   )
   
   install(DIRECTORY include/ DESTINATION include)
   install(FILES config.conf DESTINATION etc/myapp)

4.2 Cross-Compiling with CMake
-------------------------------

**Toolchain File:**

.. code-block:: cmake

   # toolchain-arm.cmake
   set(CMAKE_SYSTEM_NAME Linux)
   set(CMAKE_SYSTEM_PROCESSOR arm)
   
   # Toolchain paths
   set(TOOLCHAIN_PREFIX arm-linux-gnueabihf)
   set(TOOLCHAIN_ROOT /opt/toolchain)
   
   set(CMAKE_C_COMPILER ${TOOLCHAIN_PREFIX}-gcc)
   set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}-g++)
   set(CMAKE_ASM_COMPILER ${TOOLCHAIN_PREFIX}-gcc)
   
   # Sysroot
   set(CMAKE_SYSROOT ${TOOLCHAIN_ROOT}/${TOOLCHAIN_PREFIX}/libc)
   set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
   
   # Search paths
   set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
   set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
   set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
   set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
   
   # pkg-config
   set(PKG_CONFIG_EXECUTABLE ${TOOLCHAIN_PREFIX}-pkg-config)
   set(ENV{PKG_CONFIG_PATH} "${CMAKE_SYSROOT}/usr/lib/pkgconfig")
   set(ENV{PKG_CONFIG_SYSROOT_DIR} "${CMAKE_SYSROOT}")

**Building:**

.. code-block:: bash

   # Cross-compile build
   mkdir build && cd build
   cmake -DCMAKE_TOOLCHAIN_FILE=../toolchain-arm.cmake \
         -DCMAKE_INSTALL_PREFIX=/usr \
         ..
   make
   make install DESTDIR=/path/to/rootfs

================================================================================
5. Yocto Application Recipes
================================================================================

5.1 Application Recipe
-----------------------

**Complete Recipe:**

.. code-block:: bitbake

   # recipes-app/myapp/myapp_1.0.bb
   
   SUMMARY = "My custom application"
   DESCRIPTION = "Application for embedded device"
   HOMEPAGE = "https://example.com"
   SECTION = "applications"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://LICENSE;md5=..."
   
   # Dependencies
   DEPENDS = "libpng zlib glib-2.0"
   RDEPENDS_${PN} = "libpng zlib glib-2.0 bash"
   
   # Source
   SRC_URI = " \
       git://github.com/user/myapp.git;protocol=https;branch=main \
       file://myapp.service \
       file://myapp.conf \
       file://0001-fix-cross-compile.patch \
   "
   SRCREV = "${AUTOREV}"
   
   S = "${WORKDIR}/git"
   
   # Build system
   inherit cmake pkgconfig systemd
   
   # CMake options
   EXTRA_OECMAKE = " \
       -DCMAKE_BUILD_TYPE=Release \
       -DENABLE_TESTS=OFF \
   "
   
   # systemd service
   SYSTEMD_SERVICE_${PN} = "myapp.service"
   SYSTEMD_AUTO_ENABLE = "enable"
   
   # Custom install
   do_install_append() {
       # Install config file
       install -d ${D}${sysconfdir}/myapp
       install -m 0644 ${WORKDIR}/myapp.conf ${D}${sysconfdir}/myapp/
       
       # Install systemd service
       install -d ${D}${systemd_system_unitdir}
       install -m 0644 ${WORKDIR}/myapp.service ${D}${systemd_system_unitdir}/
       
       # Create data directory
       install -d ${D}${localstatedir}/lib/myapp
   }
   
   # Package splitting
   PACKAGES =+ "${PN}-tools ${PN}-examples"
   
   FILES_${PN} = " \
       ${bindir}/myapp \
       ${sysconfdir}/myapp/ \
       ${systemd_system_unitdir}/myapp.service \
       ${localstatedir}/lib/myapp \
   "
   
   FILES_${PN}-tools = "${bindir}/myapp-tool"
   FILES_${PN}-examples = "${datadir}/myapp/examples"
   
   RDEPENDS_${PN}-tools = "${PN}"

5.2 Recipe Variations
----------------------

**Autotools Recipe:**

.. code-block:: bitbake

   inherit autotools pkgconfig
   
   EXTRA_OECONF = " \
       --enable-shared \
       --disable-static \
       --with-custom-feature \
   "

**Makefile Recipe:**

.. code-block:: bitbake

   do_compile() {
       oe_runmake ARCH=${TARGET_ARCH} \
                  CROSS_COMPILE=${TARGET_PREFIX} \
                  CC="${CC}" \
                  CFLAGS="${CFLAGS}"
   }
   
   do_install() {
       oe_runmake install DESTDIR=${D} PREFIX=/usr
   }

**Python Application:**

.. code-block:: bitbake

   inherit setuptools3
   
   DEPENDS = "python3-setuptools-native"
   RDEPENDS_${PN} = "python3 python3-requests python3-numpy"

================================================================================
6. Debugging and Optimization
================================================================================

6.1 Debug Builds
-----------------

**Debug Flags:**

.. code-block:: bash

   # GCC debug flags
   CFLAGS="-g -O0 -DDEBUG"
   
   # With symbols but optimized
   CFLAGS="-g -O2"
   
   # Address sanitizer
   CFLAGS="-g -fsanitize=address -fno-omit-frame-pointer"
   LDFLAGS="-fsanitize=address"
   
   # Valgrind-friendly
   CFLAGS="-g -O0 -fno-omit-frame-pointer"

**GDB Remote Debugging:**

.. code-block:: bash

   # On target (run gdbserver)
   gdbserver :1234 ./myapp
   
   # On host
   arm-linux-gnueabihf-gdb myapp
   (gdb) target remote 192.168.1.100:1234
   (gdb) break main
   (gdb) continue

6.2 Optimization
-----------------

**Compiler Optimizations:**

.. code-block:: bash

   # Size optimization
   CFLAGS="-Os -ffunction-sections -fdata-sections"
   LDFLAGS="-Wl,--gc-sections"
   
   # Performance optimization
   CFLAGS="-O3 -march=armv7-a -mfpu=neon -ftree-vectorize"
   
   # Link-time optimization
   CFLAGS="-O2 -flto"
   LDFLAGS="-flto"

**Stripping Binaries:**

.. code-block:: bash

   # Strip symbols
   arm-linux-gnueabihf-strip myapp
   
   # Strip debug symbols only (keep function names)
   arm-linux-gnueabihf-strip --strip-debug myapp
   
   # In Makefile
   install: myapp
   	install -s -m 0755 myapp $(DESTDIR)/usr/bin/

================================================================================
7. Key Takeaways
================================================================================

.. code-block:: text

   Build Systems:
   ==============
   Make:      Simple, manual
   Autotools: Portable, complex
   CMake:     Modern, cross-platform
   Meson:     Fast, simple
   Yocto:     Full system integration
   
   Cross-Compilation:
   ==================
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export CC=${CROSS_COMPILE}gcc
   export SYSROOT=/path/to/sysroot
   
   Makefile:
   =========
   CC := arm-linux-gnueabihf-gcc
   CFLAGS := -Wall -O2
   $(TARGET): $(OBJS)
       $(CC) -o $@ $^ $(LDFLAGS)
   
   Autotools:
   ==========
   ./configure --host=arm-linux-gnueabihf
   make
   make install DESTDIR=/rootfs
   
   CMake:
   ======
   cmake -DCMAKE_TOOLCHAIN_FILE=toolchain.cmake
   make
   make install DESTDIR=/rootfs
   
   Yocto Recipe:
   =============
   inherit cmake
   DEPENDS = "libpng zlib"
   SRC_URI = "git://..."
   SRCREV = "${AUTOREV}"
   
   Debug:
   ======
   CFLAGS="-g -O0"
   gdbserver :1234 ./myapp
   arm-linux-gnueabihf-gdb myapp
   
   Optimize:
   =========
   Size: -Os -Wl,--gc-sections
   Speed: -O3 -march=armv7-a
   LTO: -flto

================================================================================
END OF CHEATSHEET
================================================================================
