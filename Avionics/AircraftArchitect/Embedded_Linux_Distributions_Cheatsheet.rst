🐧 **EMBEDDED LINUX DISTRIBUTIONS — Custom OS for Avionics**
═══════════════════════════════════════════════════════════════════

**Context:** Custom Linux for avionics hardware and IFE systems
**Focus:** Wind River Linux, Yocto, Buildroot, Device Tree
**Standards:** DO-178C compatible, PREEMPT_RT real-time patches

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — EMBEDDED LINUX IN 60 SECONDS**
────────────────────────────────────────────

**Distribution Comparison:**

+-------------------+---------------+-------------+----------------+
| **Feature**       | **Wind River**| **Yocto**   | **Buildroot**  |
+===================+===============+=============+================+
| DO-178C certify   | ✅ Yes        | ⚠️ Possible | ❌ No          |
+-------------------+---------------+-------------+----------------+
| Commercial support| ✅ Yes        | ❌ No       | ❌ No          |
+-------------------+---------------+-------------+----------------+
| Real-time (RT)    | ✅ Native     | ✅ Patches  | ✅ Patches     |
+-------------------+---------------+-------------+----------------+
| Build time        | Fast          | Slow        | Fast           |
+-------------------+---------------+-------------+----------------+
| Flexibility       | Medium        | High        | Medium         |
+-------------------+---------------+-------------+----------------+
| Learning curve    | Low           | High        | Low            |
+-------------------+---------------+-------------+----------------+

**Quick Decision:**

- **Safety-critical (DAL A/B):** Wind River Linux
- **Custom IFE/Entertainment:** Yocto Project
- **Quick prototypes:** Buildroot

════════════════════════════════════════════════════════════════════

📖 **1. WIND RIVER LINUX**
══════════════════════════

**1.1 Overview**
---------------

**Purpose:** Commercial Linux for safety-critical avionics

**Key Features:**

- DO-178C DAL A certification available
- PREEMPT_RT patches integrated
- Long-term support (10+ years)
- Hardware enablement for avionics boards
- Commercial support from Wind River

**Typical Use Cases:**

- Flight Management Systems (FMS)
- Primary Flight Displays (PFD)
- Engine control systems
- ARINC 653 partitioning support (VxWorks 653)

**1.2 Installation**
-------------------

::

    # Download from Wind River (requires license)
    tar xzf WRL-10.21.03.0.tar.gz
    cd WRL-10.21.03.0
    
    # Setup environment
    source environment-setup-x86_64-wrl-linux
    
    # Create project
    wrlinux-configure --enable-board=intel-x86-64 \
                     --enable-kernel=preempt-rt \
                     --enable-rootfs=glibc-std
    
    # Build
    make

**1.3 Configuration**
--------------------

**Enable Real-Time:**

::

    wrlinux-configure --enable-kernel=preempt-rt \
                     --with-template=feature/preempt-rt

**Add Custom Drivers:**

::

    wrlinux-configure --with-layer=/path/to/meta-avionics

**1.4 Certification Process**
-----------------------------

**DO-178C Artifacts:**

1. **Software Configuration Index (SCI)** - All source files
2. **Tool Qualification** - Compiler, linker certification
3. **Traceability Matrix** - Requirements → code
4. **Test Coverage** - MC/DC for DAL A

**Wind River provides:**

- Pre-certified kernel configuration
- Qualification kits
- DO-178C process documentation

════════════════════════════════════════════════════════════════════

📖 **2. YOCTO PROJECT**
═══════════════════════

**2.1 Overview**
---------------

**Purpose:** Build custom Linux distributions

**Architecture:**

::

    meta-layers (recipes)
          ↓
    BitBake (build engine)
          ↓
    Linux kernel + rootfs
          ↓
    Custom image

**Key Concepts:**

- **Recipe:** Instructions to build package (.bb file)
- **Layer:** Collection of recipes (meta-*)
- **Image:** Final bootable system

**2.2 Setup**
------------

::

    # Install dependencies (Ubuntu)
    sudo apt install gawk wget git diffstat unzip texinfo \
        gcc build-essential chrpath socat cpio python3 \
        python3-pip python3-pexpect xz-utils debianutils \
        iputils-ping python3-git python3-jinja2 libegl1-mesa \
        libsdl1.2-dev pylint3 xterm
    
    # Clone Yocto (Kirkstone LTS)
    git clone -b kirkstone git://git.yoctoproject.org/poky.git
    cd poky
    
    # Initialize environment
    source oe-init-build-env build-ife
    
    # Edit conf/local.conf
    # MACHINE = "qemux86-64"
    # DISTRO = "poky"

**2.3 Recipe Example**
---------------------

**File:** `meta-ife/recipes-apps/ife-player/ife-player_1.0.bb`

.. code-block:: bitbake

    SUMMARY = "IFE Media Player"
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."
    
    SRC_URI = "git://github.com/airline/ife-player.git;protocol=https;branch=main"
    SRCREV = "${AUTOREV}"
    
    S = "${WORKDIR}/git"
    
    inherit cmake
    
    DEPENDS = "ffmpeg gstreamer1.0 qt5"
    
    do_install() {
        install -d ${D}${bindir}
        install -m 0755 ife-player ${D}${bindir}/
    }
    
    FILES_${PN} = "${bindir}/ife-player"

**2.4 Layer Structure**
----------------------

::

    meta-ife/
    ├── conf/
    │   └── layer.conf              # Layer configuration
    ├── recipes-kernel/
    │   └── linux/
    │       └── linux-yocto_%.bbappend  # Kernel customization
    ├── recipes-apps/
    │   └── ife-player/
    │       └── ife-player_1.0.bb   # Application recipe
    └── recipes-core/
        └── images/
            └── ife-image.bb        # Custom image

**2.5 Build Image**
------------------

.. code-block:: bash

    # Add custom layer
    bitbake-layers add-layer ../meta-ife
    
    # Build image
    bitbake ife-image
    
    # Output: tmp/deploy/images/qemux86-64/ife-image-qemux86-64.wic
    
    # Test with QEMU
    runqemu qemux86-64 nographic

**2.6 Device Tree Configuration**
---------------------------------

**File:** `linux-yocto_%.bbappend`

.. code-block:: bitbake

    FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
    
    SRC_URI += "file://ife-board.dts"
    
    do_configure_append() {
        cp ${WORKDIR}/ife-board.dts ${S}/arch/arm64/boot/dts/
    }

**Device Tree Example (`ife-board.dts`):**

.. code-block:: dts

    /dts-v1/;
    
    / {
        model = "IFE Seat Unit Board";
        compatible = "airline,ife-seat";
        
        chosen {
            bootargs = "console=ttyS0,115200";
        };
        
        memory@80000000 {
            device_type = "memory";
            reg = <0x80000000 0x40000000>;  /* 1GB RAM */
        };
        
        i2c@1000 {
            compatible = "snps,designware-i2c";
            reg = <0x1000 0x100>;
            
            touchscreen@38 {
                compatible = "edt,edt-ft5406";
                reg = <0x38>;
                interrupt-parent = <&gpio>;
                interrupts = <42 IRQ_TYPE_EDGE_FALLING>;
            };
        };
        
        display@2000 {
            compatible = "simple-framebuffer";
            reg = <0x2000 0x500000>;
            width = <1920>;
            height = <1080>;
            stride = <7680>;
            format = "a8r8g8b8";
        };
    };

════════════════════════════════════════════════════════════════════

📖 **3. BUILDROOT**
═══════════════════

**3.1 Overview**
---------------

**Purpose:** Fast, simple embedded Linux builder

**Advantages:**

- Quick compilation (30 mins vs 4 hours for Yocto)
- Easy to understand (Makefiles)
- Suitable for prototypes

**Disadvantages:**

- Less flexible than Yocto
- No package management on target
- Not suitable for DO-178C certification

**3.2 Setup**
------------

::

    # Download
    wget https://buildroot.org/downloads/buildroot-2023.02.tar.gz
    tar xzf buildroot-2023.02.tar.gz
    cd buildroot-2023.02
    
    # Configure
    make menuconfig
    
    # Select:
    # - Target Architecture: ARM64
    # - Toolchain: External (Linaro)
    # - Kernel: Linux 5.15 LTS
    # - Root filesystem: ext4
    
    # Build
    make -j$(nproc)
    
    # Output: output/images/

**3.3 Custom Package**
---------------------

**File:** `package/ife-player/Config.in`

::

    config BR2_PACKAGE_IFE_PLAYER
        bool "ife-player"
        depends on BR2_PACKAGE_FFMPEG
        help
          IFE media player application

**File:** `package/ife-player/ife-player.mk`

::

    IFE_PLAYER_VERSION = 1.0
    IFE_PLAYER_SITE = $(call github,airline,ife-player,v$(IFE_PLAYER_VERSION))
    IFE_PLAYER_DEPENDENCIES = ffmpeg
    IFE_PLAYER_LICENSE = MIT
    
    define IFE_PLAYER_BUILD_CMDS
        $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D)
    endef
    
    define IFE_PLAYER_INSTALL_TARGET_CMDS
        $(INSTALL) -D -m 0755 $(@D)/ife-player $(TARGET_DIR)/usr/bin/
    endef
    
    $(eval $(generic-package))

════════════════════════════════════════════════════════════════════

📖 **4. DEVICE TREE**
═════════════════════

**4.1 Syntax**
-------------

.. code-block:: dts

    /dts-v1/;
    
    / {
        compatible = "airline,ife-board";
        #address-cells = <1>;
        #size-cells = <1>;
        
        cpus {
            #address-cells = <1>;
            #size-cells = <0>;
            
            cpu@0 {
                device_type = "cpu";
                compatible = "arm,cortex-a53";
                reg = <0>;
            };
        };
        
        soc {
            #address-cells = <1>;
            #size-cells = <1>;
            ranges;
            
            uart0: serial@10000000 {
                compatible = "ns16550a";
                reg = <0x10000000 0x1000>;
                interrupts = <1>;
                clock-frequency = <115200>;
            };
            
            arinc429@20000000 {
                compatible = "airline,arinc429";
                reg = <0x20000000 0x1000>;
                interrupts = <5>;
                tx-channels = <4>;
                rx-channels = <4>;
            };
        };
    };

**4.2 Overlay (Runtime Modification)**
--------------------------------------

**Base DTS:**

.. code-block:: dts

    / {
        gpio: gpio@30000000 {
            compatible = "gpio-controller";
            reg = <0x30000000 0x1000>;
        };
    };

**Overlay (`led-overlay.dts`):**

.. code-block:: dts

    /dts-v1/;
    /plugin/;
    
    / {
        fragment@0 {
            target = <&gpio>;
            __overlay__ {
                led@42 {
                    compatible = "gpio-led";
                    gpios = <&gpio 42 0>;
                    label = "seat-occupied";
                };
            };
        };
    };

**Apply Overlay:**

::

    dtc -I dts -O dtb -o led-overlay.dtbo led-overlay.dts
    mkdir /sys/kernel/config/device-tree/overlays/led
    cat led-overlay.dtbo > /sys/kernel/config/device-tree/overlays/led/dtbo

════════════════════════════════════════════════════════════════════

📖 **5. KERNEL CONFIGURATION**
═══════════════════════════════

**5.1 menuconfig**
-----------------

::

    cd linux-5.15
    make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig
    
    # Navigate:
    # General setup → Preemption Model → Fully Preemptible Kernel
    # Device Drivers → Network device support → Ethernet (1000 Mbit)
    # Device Drivers → Serial ATA and Parallel ATA drivers
    # File systems → ext4

**5.2 Config Fragment**
----------------------

**File:** `ife.config`

::

    CONFIG_PREEMPT_RT=y
    CONFIG_HIGH_RES_TIMERS=y
    CONFIG_NO_HZ_FULL=y
    
    # Networking
    CONFIG_NET=y
    CONFIG_INET=y
    CONFIG_TCP_CONG_BBR=y
    
    # Filesystems
    CONFIG_EXT4_FS=y
    CONFIG_VFAT_FS=y
    CONFIG_NFS_FS=y
    
    # Avionics buses
    CONFIG_CAN=y
    CONFIG_CAN_RAW=y
    CONFIG_ARINC429=m

**Merge Config:**

::

    ./scripts/kconfig/merge_config.sh .config ife.config

**5.3 Real-Time Configuration**
-------------------------------

**PREEMPT_RT Kernel:**

::

    # Download RT patches
    wget https://cdn.kernel.org/pub/linux/kernel/projects/rt/5.15/patch-5.15.10-rt24.patch.xz
    
    # Apply
    cd linux-5.15.10
    xzcat ../patch-5.15.10-rt24.patch.xz | patch -p1
    
    # Configure
    make menuconfig
    # → General setup → Preemption Model → Fully Preemptible Kernel (RT)

**Verify RT:**

::

    uname -a
    # Should show "PREEMPT_RT"

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
═════════════════════════

**Q1:** When should you use Wind River Linux vs Yocto Project?

**A1:**

**Wind River Linux:**

- ✅ Safety-critical (DO-178C DAL A/B)
- ✅ Need commercial support
- ✅ Long-term maintenance (10+ years)
- ✅ Fast time-to-market (pre-configured)
- ❌ Expensive licensing

**Yocto Project:**

- ✅ Custom IFE systems (non-safety-critical)
- ✅ Full control over every component
- ✅ Open source (no licensing fees)
- ✅ Large community
- ❌ Steep learning curve
- ❌ Long build times

**Decision:** DAL A/B → Wind River; IFE/Entertainment → Yocto

────────────────────────────────────────────────────────────────────

**Q2:** What is the Device Tree and why is it used?

**A2:**

**Device Tree:** Hardware description file (.dts) that tells Linux about 
hardware without hardcoding in kernel

**Format:** Tree structure with nodes representing hardware

.. code-block:: dts

    i2c@1000 {
        touchscreen@38 {
            compatible = "edt,edt-ft5406";
            reg = <0x38>;
        };
    };

**Benefits:**

- Single kernel binary for multiple boards
- No recompilation for hardware changes
- Runtime overlays (add/remove devices)
- Clear hardware documentation

**Alternative:** Hardcoded in kernel (old way, inflexible)

────────────────────────────────────────────────────────────────────

**Q3:** Explain PREEMPT_RT and why it's needed for avionics.

**A3:**

**PREEMPT_RT:** Real-time patches for Linux kernel

**What it does:**

- Makes kernel fully preemptible (interrupt any task)
- Converts spinlocks to mutexes (allows sleeping)
- Reduces interrupt latency (<100 µs)

**Why needed:**

- **Deterministic response** - Critical for flight control
- **Bounded latency** - Must respond within deadline
- **Priority inversion prevention** - High-priority tasks run first

**Without PREEMPT_RT:**

- Latency spikes (10+ ms)
- Non-deterministic behavior
- Not suitable for DAL A/B

**Verify:**

::

    cyclictest -p 99 -m -n -i 1000
    # Should show max latency < 100 µs

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Choose distribution (Wind River vs Yocto vs Buildroot)
- [ ] Set up build environment
- [ ] Create custom Yocto layer (if using Yocto)
- [ ] Write recipes for custom applications
- [ ] Configure Device Tree for hardware
- [ ] Apply PREEMPT_RT patches
- [ ] Enable kernel options (menuconfig)
- [ ] Test real-time performance (cyclictest)
- [ ] Create root filesystem image
- [ ] Set up cross-compilation toolchain
- [ ] Configure bootloader (U-Boot/GRUB)
- [ ] Test on target hardware
- [ ] Document build process
- [ ] Create DO-178C artifacts (if safety-critical)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Wind River for safety-critical** → DO-178C certifiable, commercial 
support, expensive

2️⃣ **Yocto for flexibility** → Full control, open source, steep learning 
curve

3️⃣ **Buildroot for prototypes** → Fast builds, simple, not production-ready

4️⃣ **Device Tree describes hardware** → Single kernel for multiple boards, 
no recompilation

5️⃣ **PREEMPT_RT enables real-time** → <100 µs latency, deterministic, 
required for flight-critical

6️⃣ **BitBake builds Yocto** → Recipes define packages, layers organize 
recipes

7️⃣ **Kernel config is critical** → Enable real-time, drivers, filesystems 
via menuconfig

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **EMBEDDED LINUX DISTRIBUTIONS COMPLETE**
**Created:** January 14, 2026
**Coverage:** Wind River, Yocto, Buildroot, Device Tree, Kernel Config

════════════════════════════════════════════════════════════════════
