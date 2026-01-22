=======================================
OpenBMC Development Guide
=======================================

:Author: Technical Documentation
:Date: January 2026
:Version: 2.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 3
   :local:
   :backlinks: top

🚀 Quick Start Development
===========================

Prerequisites
-------------

**Host System Requirements:**

* **OS**: Ubuntu 20.04/22.04 or Fedora 35+
* **Disk**: 100+ GB free space
* **RAM**: 16+ GB (8GB minimum)
* **CPU**: 4+ cores recommended

**Install Dependencies (Ubuntu):**

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y \
     git python3 python3-pip python3-distutils \
     gcc g++ make diffstat texinfo chrpath socat \
     cpio python3-pexpect xz-utils debianutils \
     iputils-ping python3-git python3-jinja2 \
     libegl1-mesa libsdl1.2-dev pylint3 xterm \
     wget gawk cpio file lz4 zstd

**Install Dependencies (Fedora):**

.. code-block:: bash

   sudo dnf install -y \
     git python3 gcc gcc-c++ diffstat texinfo chrpath \
     SDL-devel xterm cpio make wget gawk lz4 zstd

30-Second Build
---------------

.. code-block:: bash

   # 1. Clone repository
   git clone https://github.com/openbmc/openbmc.git
   cd openbmc
   
   # 2. Choose a machine (example: AST2600 EVB)
   export TEMPLATECONF=meta-aspeed/meta-ast2600-pfr/conf
   . setup ast2600-pfr
   
   # 3. Build (takes 2-4 hours on first build)
   bitbake obmc-phosphor-image
   
   # 4. Find the image
   ls tmp/deploy/images/ast2600-pfr/*.mtd

🏗️ Build System Architecture
==============================

Yocto/OpenEmbedded Structure
-----------------------------

.. code-block:: text

   openbmc/
   ├── meta-layer-name/              # Layer directories
   │   ├── conf/
   │   │   ├── layer.conf            # Layer configuration
   │   │   └── machine/*.conf        # Machine configs
   │   ├── recipes-*/                # Recipe directories
   │   │   └── package-name/
   │   │       └── package_version.bb  # Recipe file
   │   └── classes/                  # Custom classes
   ├── build/                        # Build directory (created)
   │   ├── conf/
   │   │   ├── local.conf            # Local build config
   │   │   └── bblayers.conf         # Layer inclusion
   │   └── tmp/                      # Build artifacts
   │       ├── work/                 # Package build dirs
   │       ├── deploy/images/        # Final images
   │       └── sysroots/             # Cross-compile roots
   └── setup                         # Setup script

Meta Layers
-----------

**Core OpenBMC Layers:**

+----------------------------+------------------------------------------------+
| **Layer**                  | **Purpose**                                    |
+============================+================================================+
| meta-phosphor              | Core OpenBMC infrastructure                    |
+----------------------------+------------------------------------------------+
| meta-openembedded          | OE community layers                            |
+----------------------------+------------------------------------------------+
| meta-aspeed                | ASPEED SoC BSP                                 |
+----------------------------+------------------------------------------------+
| meta-nuvoton               | Nuvoton NPCM7xx BSP                            |
+----------------------------+------------------------------------------------+
| meta-<vendor>              | Vendor-specific (IBM, Facebook, etc.)          |
+----------------------------+------------------------------------------------+
| meta-<machine>             | Machine-specific configurations                |
+----------------------------+------------------------------------------------+

Layer Priority
--------------

.. code-block:: text

   Lower priority ← → Higher priority
   
   poky (base) → meta-openembedded → meta-phosphor → meta-vendor → meta-machine
   
   # Higher priority layers override lower ones
   # Machine layers typically have highest priority

🔨 Building OpenBMC
====================

Choosing a Machine
------------------

**Popular Machines:**

.. code-block:: bash

   # ASPEED AST2500 (common in servers)
   export TEMPLATECONF=meta-ibm/meta-romulus/conf
   . setup romulus
   
   # ASPEED AST2600 (newer)
   export TEMPLATECONF=meta-facebook/meta-yosemite4/conf
   . setup yosemite4
   
   # QEMU x86 (for testing)
   export TEMPLATECONF=meta-x86/meta-x86-power-control/conf
   . setup x86-power-control
   
   # QEMU ARM (for development)
   . setup qemu

**List Available Machines:**

.. code-block:: bash

   # After setup
   ls meta-*/meta-*/conf/machine/*.conf | \
     sed 's|.*/||; s|\.conf||'

Build Configuration
-------------------

**Edit local.conf:**

.. code-block:: bash

   vi conf/local.conf

**Common Configuration Options:**

.. code-block:: python

   # Parallel builds (use CPU cores)
   BB_NUMBER_THREADS = "8"
   PARALLEL_MAKE = "-j 8"
   
   # Download mirror
   PREMIRRORS:prepend = "\
       git://.*/.* https://mirror.example.com/git/MIRRORNAME \n \
       ftp://.*/.* https://mirror.example.com/ftp/MIRRORNAME \n \
   "
   
   # Shared state cache (speeds up rebuilds)
   SSTATE_DIR = "/path/to/shared/sstate-cache"
   
   # Download directory (shared across builds)
   DL_DIR = "/path/to/shared/downloads"
   
   # Enable debug
   EXTRA_IMAGE_FEATURES += "debug-tweaks"
   
   # Add packages to image
   IMAGE_INSTALL:append = " htop vim nano"
   
   # Remove packages
   IMAGE_INSTALL:remove = "phosphor-webui"
   
   # Use systemd
   DISTRO_FEATURES:append = " systemd"
   VIRTUAL-RUNTIME_init_manager = "systemd"

Build Commands
--------------

.. code-block:: bash

   # Build full image
   bitbake obmc-phosphor-image
   
   # Build specific package
   bitbake bmcweb
   
   # Clean package (force rebuild)
   bitbake -c clean bmcweb
   bitbake bmcweb
   
   # Clean everything and rebuild
   bitbake -c cleanall bmcweb
   bitbake bmcweb
   
   # Build SDK (for cross-compilation)
   bitbake -c populate_sdk obmc-phosphor-image
   
   # Show package dependencies
   bitbake -g obmc-phosphor-image
   
   # List all available recipes
   bitbake-layers show-recipes
   
   # Show layers
   bitbake-layers show-layers

Build Output
------------

**Image Locations:**

.. code-block:: bash

   # MTD image (for ASPEED)
   tmp/deploy/images/<machine>/obmc-phosphor-image-<machine>.static.mtd
   
   # U-Boot image
   tmp/deploy/images/<machine>/u-boot.bin
   
   # Kernel
   tmp/deploy/images/<machine>/fitImage
   
   # Root filesystem
   tmp/deploy/images/<machine>/obmc-phosphor-image-<machine>.tar.gz

Incremental Builds
------------------

.. code-block:: bash

   # After changing source code
   bitbake -c compile -f <package>
   bitbake <package>
   
   # After changing recipe
   bitbake -c clean <package>
   bitbake <package>
   
   # Full clean (removes all artifacts)
   rm -rf tmp/

🧪 Testing with QEMU
=====================

Start QEMU Session
------------------

.. code-block:: bash

   # Build QEMU machine
   . setup qemu
   bitbake obmc-phosphor-image
   
   # Run QEMU
   qemu-system-arm \
     -machine romulus-bmc \
     -nographic \
     -drive file=tmp/deploy/images/romulus/obmc-phosphor-image-romulus.static.mtd,format=raw,if=mtd \
     -net nic \
     -net user,hostfwd=tcp::2222-:22,hostfwd=tcp::2443-:443,hostfwd=:2623-:623,hostname=qemu
   
   # Or use helper script
   runqemu

**Access QEMU BMC:**

.. code-block:: bash

   # SSH (from host)
   ssh root@localhost -p 2222
   # Default password: 0penBmc
   
   # Web UI
   https://localhost:2443
   
   # Redfish
   curl -k https://localhost:2443/redfish/v1
   
   # IPMI
   ipmitool -I lanplus -H localhost -p 2623 -U root -P 0penBmc power status

QEMU Network Setup
------------------

.. code-block:: bash

   # Create tap interface (requires root)
   sudo ip tuntap add tap0 mode tap
   sudo ip addr add 192.168.7.1/24 dev tap0
   sudo ip link set tap0 up
   
   # Run QEMU with tap
   qemu-system-arm \
     -machine romulus-bmc \
     -nographic \
     -drive file=obmc-phosphor-image.mtd,format=raw,if=mtd \
     -net nic,macaddr=52:54:00:12:34:56 \
     -net tap,ifname=tap0,script=no,downscript=no
   
   # BMC should be accessible at 192.168.7.2

🔧 Development Workflow
========================

Creating a New Recipe
---------------------

**1. Create recipe file:**

.. code-block:: bash

   mkdir -p meta-custom/recipes-phosphor/my-daemon
   vi meta-custom/recipes-phosphor/my-daemon/my-daemon_1.0.bb

**2. Recipe template:**

.. code-block:: python

   SUMMARY = "My custom BMC daemon"
   DESCRIPTION = "Custom daemon for special hardware monitoring"
   LICENSE = "Apache-2.0"
   LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Apache-2.0;md5=89aea4e17d99a7cacdbeed46a0096b10"
   
   inherit meson systemd
   
   DEPENDS = "systemd sdbusplus"
   
   SRC_URI = "git://github.com/myorg/my-daemon;protocol=https;branch=master"
   SRCREV = "${AUTOREV}"
   
   S = "${WORKDIR}/git"
   
   SYSTEMD_SERVICE:${PN} = "my-daemon.service"
   
   do_install:append() {
       install -d ${D}${systemd_system_unitdir}
       install -m 0644 ${S}/my-daemon.service ${D}${systemd_system_unitdir}/
   }

**3. Add to layer.conf:**

.. code-block:: bash

   echo 'BBPATH .= ":${LAYERDIR}"' > meta-custom/conf/layer.conf
   echo 'BBFILES += "${LAYERDIR}/recipes-*/*/*.bb"' >> meta-custom/conf/layer.conf
   echo 'BBFILE_COLLECTIONS += "custom"' >> meta-custom/conf/layer.conf
   echo 'BBFILE_PATTERN_custom = "^${LAYERDIR}/"' >> meta-custom/conf/layer.conf
   echo 'LAYERSERIES_COMPAT_custom = "kirkstone"' >> meta-custom/conf/layer.conf

**4. Add layer to build:**

.. code-block:: bash

   bitbake-layers add-layer ../meta-custom

Modifying Existing Package
---------------------------

**Using devtool:**

.. code-block:: bash

   # Extract source to workspace
   devtool modify bmcweb
   
   # Source now in workspace/sources/bmcweb
   cd workspace/sources/bmcweb
   
   # Make changes
   vim src/webserver_main.cpp
   
   # Build and test
   devtool build bmcweb
   
   # Deploy to running BMC
   devtool deploy-target bmcweb root@192.168.1.100
   
   # When done, create patch
   devtool finish bmcweb meta-custom

**Manual patching:**

.. code-block:: bash

   # Create patch directory
   mkdir -p meta-custom/recipes-phosphor/bmcweb/bmcweb
   
   # Add patch
   vi meta-custom/recipes-phosphor/bmcweb/bmcweb/my-changes.patch
   
   # Create bbappend
   vi meta-custom/recipes-phosphor/bmcweb/bmcweb_%.bbappend

.. code-block:: python

   FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
   SRC_URI += "file://my-changes.patch"

Local Source Override
---------------------

.. code-block:: bash

   # In conf/local.conf
   echo 'EXTERNALSRC:pn-bmcweb = "/path/to/local/bmcweb"' >> conf/local.conf
   echo 'EXTERNALSRC_BUILD:pn-bmcweb = "/path/to/local/bmcweb/build"' >> conf/local.conf
   
   # Now bitbake uses your local source
   bitbake bmcweb

📦 Creating Custom Phosphor Daemon
===================================

C++ Daemon with sdbusplus
--------------------------

**meson.build:**

.. code-block:: meson

   project('my-daemon', 'cpp',
       version: '1.0',
       default_options: [
           'cpp_std=c++20',
           'warning_level=3',
           'werror=true'
       ]
   )
   
   sdbusplus_dep = dependency('sdbusplus')
   phosphor_dbus_interfaces_dep = dependency('phosphor-dbus-interfaces')
   phosphor_logging_dep = dependency('phosphor-logging')
   
   executable(
       'my-daemon',
       'src/main.cpp',
       'src/sensor_monitor.cpp',
       dependencies: [
           sdbusplus_dep,
           phosphor_dbus_interfaces_dep,
           phosphor_logging_dep
       ],
       install: true,
       install_dir: get_option('bindir')
   )
   
   systemd = dependency('systemd')
   systemd_system_unit_dir = systemd.get_pkgconfig_variable('systemdsystemunitdir')
   
   configure_file(
       input: 'my-daemon.service.in',
       output: 'my-daemon.service',
       configuration: {
           'BINDIR': get_option('prefix') / get_option('bindir')
       },
       install: true,
       install_dir: systemd_system_unit_dir
   )

**src/main.cpp:**

.. code-block:: cpp

   #include <sdbusplus/bus.hpp>
   #include <sdbusplus/server.hpp>
   #include <phosphor-logging/log.hpp>
   #include <iostream>
   
   using namespace phosphor::logging;
   
   class SensorMonitor {
   public:
       SensorMonitor(sdbusplus::bus::bus& bus) : 
           bus(bus),
           interface(bus,
                    "/xyz/openbmc_project/sensors/temperature/cpu0",
                    "xyz.openbmc_project.Sensor.Value",
                    vtable,
                    this)
       {
           log<level::INFO>("SensorMonitor initialized");
       }
       
       void updateValue(double value) {
           currentValue = value;
           // Emit PropertiesChanged signal
           auto msg = bus.new_signal(
               "/xyz/openbmc_project/sensors/temperature/cpu0",
               "org.freedesktop.DBus.Properties",
               "PropertiesChanged");
           msg.append("xyz.openbmc_project.Sensor.Value");
           // ... signal data
           msg.signal_send();
       }
       
   private:
       sdbusplus::bus::bus& bus;
       double currentValue = 0.0;
       sdbusplus::server::interface::interface interface;
       
       static const sdbusplus::vtable::vtable_t vtable[];
   };
   
   int main() {
       auto bus = sdbusplus::bus::new_default();
       
       sdbusplus::server::manager::manager objManager(
           bus,
           "/xyz/openbmc_project/sensors");
       
       SensorMonitor monitor(bus);
       
       // Request service name
       bus.request_name("xyz.openbmc_project.MySensorMonitor");
       
       // Process D-Bus messages
       while (true) {
           bus.process_discard();
           bus.wait();
       }
       
       return 0;
   }

**my-daemon.service.in:**

.. code-block:: ini

   [Unit]
   Description=My Custom Sensor Monitor
   After=mapper-wait@-xyz-openbmc_project-sensors.service
   
   [Service]
   ExecStart=@BINDIR@/my-daemon
   Restart=always
   RestartSec=5
   
   [Install]
   WantedBy=multi-user.target

Python Daemon Example
---------------------

**Recipe (my-python-daemon_1.0.bb):**

.. code-block:: python

   SUMMARY = "Python daemon example"
   LICENSE = "Apache-2.0"
   LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Apache-2.0;md5=89aea4e17d99a7cacdbeed46a0096b10"
   
   inherit setuptools3 systemd
   
   RDEPENDS:${PN} = "python3-dbus python3-pygobject"
   
   SRC_URI = "file://setup.py \
              file://my_daemon.py \
              file://my-daemon.service"
   
   S = "${WORKDIR}"
   
   SYSTEMD_SERVICE:${PN} = "my-daemon.service"
   
   do_install:append() {
       install -d ${D}${systemd_system_unitdir}
       install -m 0644 ${WORKDIR}/my-daemon.service ${D}${systemd_system_unitdir}/
   }

**my_daemon.py:**

.. code-block:: python

   #!/usr/bin/env python3
   import dbus
   import dbus.service
   import dbus.mainloop.glib
   from gi.repository import GLib
   
   DBUS_NAME = 'xyz.openbmc_project.MyDaemon'
   DBUS_PATH = '/xyz/openbmc_project/mydaemon'
   
   class MyDaemon(dbus.service.Object):
       def __init__(self, bus, path):
           super().__init__(bus, path)
           self.value = 0
       
       @dbus.service.method(
           "xyz.openbmc_project.MyDaemon",
           in_signature='i', out_signature='i')
       def SetValue(self, value):
           self.value = value
           self.PropertiesChanged(
               "xyz.openbmc_project.MyDaemon",
               {"Value": value}, [])
           return value
       
       @dbus.service.method(
           "xyz.openbmc_project.MyDaemon",
           out_signature='i')
       def GetValue(self):
           return self.value
       
       @dbus.service.signal(
           "org.freedesktop.DBus.Properties",
           signature='sa{sv}as')
       def PropertiesChanged(self, interface, changed, invalidated):
           pass
   
   def main():
       dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
       
       bus = dbus.SystemBus()
       name = dbus.service.BusName(DBUS_NAME, bus)
       obj = MyDaemon(bus, DBUS_PATH)
       
       mainloop = GLib.MainLoop()
       mainloop.run()
   
   if __name__ == '__main__':
       main()

🔍 Debugging
=============

Enable Debug Output
-------------------

**Build-time debug:**

.. code-block:: bash

   # In conf/local.conf
   EXTRA_IMAGE_FEATURES += "debug-tweaks"
   DEBUG_BUILD = "1"
   
   # Rebuild
   bitbake -c clean obmc-phosphor-image
   bitbake obmc-phosphor-image

**Runtime debug:**

.. code-block:: bash

   # On BMC, set logging level
   busctl call xyz.openbmc_project.Logging \
     /xyz/openbmc_project/logging \
     xyz.openbmc_project.Logging.Settings \
     SetLogLevel s "xyz.openbmc_project" s "Debug"
   
   # View debug logs
   journalctl -f -p debug

GDB Remote Debugging
--------------------

.. code-block:: bash

   # 1. Build with debug symbols
   # In conf/local.conf:
   EXTRA_IMAGE_FEATURES += "dbg-pkgs dev-pkgs tools-debug"
   
   # 2. On BMC, start gdbserver
   gdbserver :9999 /usr/bin/my-daemon
   
   # 3. On host, connect with GDB
   arm-openbmc-linux-gnueabi-gdb \
     tmp/work/.../my-daemon/1.0-r0/image/usr/bin/my-daemon
   
   (gdb) target remote bmc-ip:9999
   (gdb) break main
   (gdb) continue

System Tracing
--------------

.. code-block:: bash

   # Trace system calls
   strace -p $(pidof my-daemon)
   
   # Trace D-Bus messages
   dbus-monitor --system
   
   # Specific interface
   dbus-monitor --system "type='signal',interface='xyz.openbmc_project.Sensor.Value'"
   
   # Network trace
   tcpdump -i eth0 -w /tmp/capture.pcap

Performance Profiling
---------------------

.. code-block:: bash

   # CPU profiling with perf
   perf record -p $(pidof my-daemon)
   perf report
   
   # Memory profiling with valgrind
   valgrind --leak-check=full /usr/bin/my-daemon
   
   # I/O monitoring
   iotop
   iostat -x 1

📝 Documentation & Code Style
==============================

C++ Coding Standards
--------------------

OpenBMC follows Linux kernel style with modifications:

.. code-block:: cpp

   // Good
   void functionName(int parameter)
   {
       if (condition)
       {
           doSomething();
       }
   }
   
   // Member variables
   class MyClass
   {
     private:
       int memberVariable;  // camelCase
       static constexpr int MaxValue = 100;  // PascalCase for constants
   };
   
   // Namespaces
   namespace phosphor
   {
   namespace logging
   {
   // code
   }
   }

**Run clang-format:**

.. code-block:: bash

   clang-format -i src/*.cpp src/*.hpp

Python Coding Standards
-----------------------

Follow PEP 8:

.. code-block:: python

   """Module docstring."""
   
   import sys
   
   def function_name(parameter_one, parameter_two):
       """Function docstring.
       
       Args:
           parameter_one: Description
           parameter_two: Description
       
       Returns:
           Description of return value
       """
       if parameter_one == parameter_two:
           return True
       return False

**Run formatters:**

.. code-block:: bash

   # Black formatter
   black my_script.py
   
   # Pylint
   pylint my_script.py

Commit Messages
---------------

.. code-block:: text

   component: Short summary (50 chars or less)
   
   More detailed explanatory text wrapped at 72 characters. Explain
   the problem that this commit is solving and how. Focus on why you
   are making this change rather than how (the code explains that).
   
   Tested: Description of testing performed
   
   Signed-off-by: Your Name <your.email@example.com>

**Example:**

.. code-block:: text

   bmcweb: Add support for custom sensor readings
   
   This patch adds support for reading custom sensor types from the
   D-Bus interface xyz.openbmc_project.CustomSensor. The values are
   exposed via the Redfish Thermal resource.
   
   Tested: Verified sensor readings appear in GET /redfish/v1/Chassis/
   chassis/Thermal. Tested with curl and Redfish validator.
   
   Signed-off-by: John Doe <john.doe@example.com>

🚢 Deployment
==============

Flashing BMC Firmware
---------------------

**Via TFTP/HTTP Update:**

.. code-block:: bash

   # 1. Start web server on build machine
   cd tmp/deploy/images/<machine>/
   python3 -m http.server 8080
   
   # 2. On BMC or via Redfish
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ImageURI":"http://build-server:8080/obmc-phosphor-image.static.mtd"}' \
     https://bmc-ip/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate

**Via SCP:**

.. code-block:: bash

   # Copy to BMC
   scp obmc-phosphor-image.static.mtd root@bmc-ip:/tmp/
   
   # On BMC, flash manually
   flashcp -v /tmp/obmc-phosphor-image.static.mtd /dev/mtd/image
   reboot

**Via Serial Console (Recovery):**

.. code-block:: bash

   # During boot, press space to enter U-Boot
   # Setup TFTP
   setenv serverip 192.168.1.100
   setenv ipaddr 192.168.1.101
   tftp 0x83000000 obmc-phosphor-image.static.mtd
   sf probe
   sf erase 0 0x4000000
   sf write 0x83000000 0 ${filesize}
   reset

Automated Testing
-----------------

**Robot Framework Tests:**

.. code-block:: bash

   # Clone test repo
   git clone https://github.com/openbmc/openbmc-test-automation.git
   cd openbmc-test-automation
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Run tests
   robot -v OPENBMC_HOST:192.168.1.100 \
         -v OPENBMC_USERNAME:root \
         -v OPENBMC_PASSWORD:0penBmc \
         tests/test_power.robot

**Custom Test Script:**

.. code-block:: python

   #!/usr/bin/env python3
   import redfish
   import sys
   
   def test_power_cycle(bmc_ip, user, password):
       """Test power on/off cycle"""
       client = redfish.redfish_client(
           base_url=f"https://{bmc_ip}",
           username=user,
           password=password
       )
       client.login(auth="session")
       
       # Power off
       client.post(
           "/redfish/v1/Systems/system/Actions/ComputerSystem.Reset",
           body={"ResetType": "ForceOff"}
       )
       time.sleep(10)
       
       # Power on
       client.post(
           "/redfish/v1/Systems/system/Actions/ComputerSystem.Reset",
           body={"ResetType": "On"}
       )
       time.sleep(5)
       
       # Check state
       response = client.get("/redfish/v1/Systems/system")
       state = response.dict["PowerState"]
       
       client.logout()
       
       assert state == "On", f"Expected 'On', got '{state}'"
       print("✓ Power cycle test passed")
       return 0
   
   if __name__ == "__main__":
       sys.exit(test_power_cycle("192.168.1.100", "admin", "password"))

🛠️ Common Customizations
===========================

Adding New Sensor
-----------------

**1. Create configuration file:**

.. code-block:: bash

   mkdir -p meta-custom/recipes-phosphor/sensors/phosphor-hwmon/
   vi meta-custom/recipes-phosphor/sensors/phosphor-hwmon/custom_sensors.conf

.. code-block:: ini

   # I2C bus and address
   LABEL_temp1 = "CPU0 Temp"
   LABEL_temp2 = "CPU1 Temp"
   
   # Thresholds (in millidegrees)
   WARNHI_temp1 = 75000
   CRITHI_temp1 = 90000

**2. Create systemd service:**

.. code-block:: bash

   vi meta-custom/recipes-phosphor/sensors/phosphor-hwmon/custom-sensors.service

.. code-block:: ini

   [Unit]
   Description=Custom Temperature Sensors
   After=multi-user.target
   
   [Service]
   Type=simple
   ExecStart=/usr/bin/phosphor-hwmon-readd \
     --path=/sys/bus/i2c/devices/0-004f/hwmon/hwmon0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target

**3. Create bbappend:**

.. code-block:: bash

   vi meta-custom/recipes-phosphor/sensors/phosphor-hwmon_%.bbappend

.. code-block:: python

   FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
   
   SRC_URI += "file://custom_sensors.conf \
               file://custom-sensors.service"
   
   SYSTEMD_SERVICE:${PN} += "custom-sensors.service"

Custom Fan Control
------------------

.. code-block:: python

   # meta-custom/recipes-phosphor/fans/phosphor-fan-control/fan-config.json
   {
       "profiles": [
           {
               "name": "default",
               "cooling_zones": [
                   {
                       "zone": 0,
                       "fans": ["fan0", "fan1"],
                       "set_point": 50,
                       "increase_delay": 5,
                       "decrease_delay": 10
                   }
               ]
           }
       ],
       "sensors": [
           {"name": "CPU0 Temp", "zone": 0},
           {"name": "CPU1 Temp", "zone": 0}
       ],
       "zones": [
           {
               "zone": 0,
               "full_speed": 100,
               "default_floor": 30,
               "increase_delta": 5,
               "decrease_delta": 3
           }
       ]
   }

Web UI Customization
--------------------

.. code-block:: bash

   # Fork webui
   git clone https://github.com/openbmc/webui-vue.git
   cd webui-vue
   
   # Customize logo
   cp my-logo.svg src/assets/images/
   vi src/components/AppHeader/AppHeader.vue
   
   # Build
   npm install
   npm run build
   
   # Deploy
   scp -r dist/* root@bmc-ip:/usr/share/www/

📚 Advanced Topics
==================

Multi-Host Support
------------------

For systems with multiple hosts (e.g., blade servers):

.. code-block:: python

   # Recipe modification for multi-host
   OBMC_HOST_INSTANCES = "0 1 2 3"
   
   SYSTEMD_SERVICE:${PN} = " \
       phosphor-host-state-manager@0.service \
       phosphor-host-state-manager@1.service \
       phosphor-host-state-manager@2.service \
       phosphor-host-state-manager@3.service \
   "

Custom REST API Endpoint
-------------------------

.. code-block:: cpp

   // In bmcweb source
   BMCWEB_ROUTE(app, "/redfish/v1/Oem/MyCompany/CustomEndpoint")
       .privileges({{"Login"}})
       .methods(boost::beast::http::verb::get)(
           [](const crow::Request& req,
              const std::shared_ptr<bmcweb::AsyncResp>& asyncResp) {
               asyncResp->res.jsonValue["Message"] = "Custom endpoint";
               asyncResp->res.jsonValue["Value"] = 42;
           });

Secure Boot Implementation
---------------------------

.. code-block:: bash

   # Generate keys
   openssl genrsa -out private_key.pem 2048
   openssl rsa -in private_key.pem -pubout -out public_key.pem
   
   # Sign firmware
   openssl dgst -sha256 -sign private_key.pem \
     -out firmware.sig firmware.bin
   
   # Enable secure boot in U-Boot
   setenv secure_boot_enable 1
   saveenv

🔗 Resources
=============

Documentation
-------------

* **GitHub**: https://github.com/openbmc
* **Docs**: https://github.com/openbmc/docs
* **Mailing List**: openbmc@lists.ozlabs.org
* **Discord**: OpenBMC Community Server

Development Tools
-----------------

* **Yocto**: https://www.yoctoproject.org/
* **BitBake**: https://www.yoctoproject.org/docs/current/bitbake-user-manual/
* **D-Bus**: https://www.freedesktop.org/wiki/Software/dbus/
* **Meson**: https://mesonbuild.com/

Useful Commands
---------------

.. code-block:: bash

   # Recipe info
   bitbake -e <recipe> | grep ^WORKDIR
   bitbake -e <recipe> | grep ^S=
   
   # Dependency graph
   bitbake -g <recipe> && dot -Tpng task-depends.dot -o deps.png
   
   # What provides a file
   oe-pkgdata-util find-path /usr/bin/bmcweb
   
   # List recipe files
   bitbake-layers show-recipes -f
   
   # Run specific task
   bitbake -c <task> <recipe>
   # Tasks: fetch, unpack, patch, configure, compile, install, package

========================================
Last Updated: January 2026
Version: 2.0
========================================
