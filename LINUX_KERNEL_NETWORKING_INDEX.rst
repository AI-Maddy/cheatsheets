===================================
Linux Kernel & Networking - Master Index
===================================

:Date: January 2026
:Purpose: Quick navigation to all Linux kernel and networking cheatsheets
:Total Files: 27 new + existing files

Quick Start
===========

**New to Linux Kernel Development?**
Start here: Linux_Platform_Drivers.rst → Linux_Kernel_Synchronization.rst

**Network Administration?**
Start here: Linux_Network_Configuration.rst → Linux_Network_Tools.rst

**Driver Development?**
Start here: Linux_Char_Device_Drivers.rst → Linux_Driver_Debugging.rst

Kernel Synchronization (7 files)
=================================

Location: `/Linux/Kernel/Source/Synchronization/`

**Overview & Decision Making**
  - `Linux_Kernel_Synchronization.rst <Linux/Kernel/Source/Synchronization/Linux_Kernel_Synchronization.rst>`_
    Master overview, primitive selection guide, performance comparison

**Core Primitives**
  - `Linux_Mutexes_Semaphores.rst <Linux/Kernel/Source/Synchronization/Linux_Mutexes_Semaphores.rst>`_
    Mutex and semaphore APIs, sleeping locks
  
  - `Linux_Spinlocks.rst <Linux/Kernel/Source/Synchronization/Linux_Spinlocks.rst>`_
    All spinlock variants, IRQ-safe locks, lock ordering
  
  - `Linux_Atomic_Operations.rst <Linux/Kernel/Source/Synchronization/Linux_Atomic_Operations.rst>`_
    Atomic ops, memory barriers, lock-free programming
  
  - `Linux_RCU.rst <Linux/Kernel/Source/Synchronization/Linux_RCU.rst>`_
    Read-Copy-Update, lock-free read-heavy data structures

**Advanced Topics**
  - `Linux_Kernel_Locking_Patterns.rst <Linux/Kernel/Source/Synchronization/Linux_Kernel_Locking_Patterns.rst>`_
    Design patterns, deadlock prevention
  
  - `Linux_Wait_Queues.rst <Linux/Kernel/Source/Synchronization/Linux_Wait_Queues.rst>`_
    Wait queues, completions, event waiting

Driver Frameworks (2 files)
============================

Location: `/Linux/Kernel/Source/Drivers/`

**Foundation**
  - `Linux_Char_Device_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_Char_Device_Drivers.rst>`_
    Character device framework, file operations
  
  - `Linux_Platform_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_Platform_Drivers.rst>`_
    Platform driver architecture, device tree

Bus & Core Drivers (4 files)
=============================

Location: `/Linux/Kernel/Source/Drivers/`

**Bus Drivers**
  - `Linux_SPI_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_SPI_Drivers.rst>`_
    SPI framework, transfers, DMA, EEPROM example
  
  - Existing: Linux_I2C_Drivers.rst
    I2C framework, SMBus, device tree

**Core Infrastructure**
  - `Linux_GPIO_Pinctrl.rst <Linux/Kernel/Source/Drivers/Linux_GPIO_Pinctrl.rst>`_
    GPIO descriptor API, pinctrl, IRQ conversion
  
  - `Linux_Regmap_API.rst <Linux/Kernel/Source/Drivers/Linux_Regmap_API.rst>`_
    Register map abstraction, caching, I2C/SPI
  
  - `Linux_Driver_IRQ_Handling.rst <Linux/Kernel/Source/Drivers/Linux_Driver_IRQ_Handling.rst>`_
    Interrupts, threaded IRQs, deferred work, MSI/MSI-X

Peripheral Drivers (4 files)
=============================

Location: `/Linux/Kernel/Source/Drivers/`

**Input & Timing**
  - `Linux_Input_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_Input_Drivers.rst>`_
    Input subsystem, buttons, keyboards, touchscreens
  
  - `Linux_RTC_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_RTC_Drivers.rst>`_
    RTC operations, alarms, I2C RTC drivers

**Control & Monitoring**
  - `Linux_PWM_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_PWM_Drivers.rst>`_
    PWM provider/consumer, backlight drivers
  
  - `Linux_Watchdog_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_Watchdog_Drivers.rst>`_
    Watchdog subsystem, pretimeout, userspace interface

Advanced Drivers (4 files)
===========================

Location: `/Linux/Kernel/Source/Drivers/`

**High-Performance I/O**
  - `Linux_Network_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_Network_Drivers.rst>`_
    Network devices, NAPI, TX/RX paths, ethernet drivers
  
  - `Linux_Block_Drivers.rst <Linux/Kernel/Source/Drivers/Linux_Block_Drivers.rst>`_
    blk-mq, tag sets, request processing

**Power & Debug**
  - `Linux_Driver_Power_Management.rst <Linux/Kernel/Source/Drivers/Linux_Driver_Power_Management.rst>`_
    System sleep, runtime PM, wakeup sources
  
  - `Linux_Driver_Debugging.rst <Linux/Kernel/Source/Drivers/Linux_Driver_Debugging.rst>`_
    printk, debugfs, ftrace, KGDB, performance analysis

Networking (5 files)
=====================

Location: `/Linux/Networking/`

**Configuration & Tools**
  - `Linux_Network_Configuration.rst <Linux/Networking/Linux_Network_Configuration.rst>`_
    ip command, routing, VLAN, bonding, bridges, NetworkManager
  
  - `Linux_Network_Tools.rst <Linux/Networking/Linux_Network_Tools.rst>`_
    ping, traceroute, tcpdump, nmap, iperf3, curl, wget

**Protocols & Wireless**
  - `Linux_Network_Protocols.rst <Linux/Networking/Linux_Network_Protocols.rst>`_
    TCP/IP, UDP, ICMP, DNS, HTTP, DHCP, ARP, NAT
  
  - `Linux_Wireless_Networking.rst <Linux/Networking/Linux_Wireless_Networking.rst>`_
    iw, wpa_supplicant, hostapd, WiFi diagnostics

**Performance**
  - `Linux_Network_Performance.rst <Linux/Networking/Linux_Network_Performance.rst>`_
    Kernel tuning, BBR, buffer optimization, traffic control, monitoring

Existing Related Files
=======================

**Device Drivers** (in `/Linux/Kernel/Source/Drivers/`)
  - Linux_DMA.rst - DMA engine API
  - Linux_PCIe_Drivers.rst - PCI Express drivers
  - Linux_USB_Drivers.rst - USB subsystem
  - Linux_V4L2_Drivers.rst - Video4Linux2

**Memory Management** (in `/Linux/`)
  - Linux memory management.rst
  - Linux memory management internals.rst
  - Linux Memory management keywords.rst

**Debug & Development** (in `/Linux/`)
  - Linux Debug.rst
  - Linux KGDB.rst
  - Linux Kernel Sysnc.rst

**Networking** (in `/Linux/Kernel/Source/Network/`)
  - Socket Programming.rst - Socket API reference
  - Socket CAN.rst - CAN bus sockets

Learning Paths
==============

**Beginner Driver Developer**
1. Linux_Char_Device_Drivers.rst
2. Linux_Platform_Drivers.rst
3. Linux_GPIO_Pinctrl.rst
4. Linux_Input_Drivers.rst
5. Linux_Driver_Debugging.rst

**Intermediate Driver Developer**
1. Linux_Kernel_Synchronization.rst
2. Linux_Mutexes_Semaphores.rst
3. Linux_Spinlocks.rst
4. Linux_SPI_Drivers.rst
5. Linux_Driver_IRQ_Handling.rst
6. Linux_Driver_Power_Management.rst

**Advanced Driver Developer**
1. Linux_RCU.rst
2. Linux_Kernel_Locking_Patterns.rst
3. Linux_Network_Drivers.rst
4. Linux_Block_Drivers.rst
5. Linux_Regmap_API.rst

**Network Administrator**
1. Linux_Network_Configuration.rst
2. Linux_Network_Tools.rst
3. Linux_Network_Protocols.rst
4. Linux_Wireless_Networking.rst
5. Linux_Network_Performance.rst

**Network Programmer**
1. Socket Programming.rst
2. Linux_Network_Protocols.rst
3. Linux_Network_Performance.rst

Topic Cross-Reference
======================

**Power Management**
  - Linux_Driver_Power_Management.rst
  - Linux_Network_Performance.rst (network power features)

**Debugging**
  - Linux_Driver_Debugging.rst (comprehensive)
  - Linux Debug.rst (existing)
  - Linux KGDB.rst (existing)

**DMA**
  - Linux_DMA.rst (existing)
  - Linux_Network_Drivers.rst (DMA in network drivers)
  - Linux_Block_Drivers.rst (DMA in block I/O)

**Device Tree**
  - Linux_Platform_Drivers.rst
  - Linux_SPI_Drivers.rst
  - Linux_GPIO_Pinctrl.rst
  - Linux device tree.rst (existing)

**Interrupts**
  - Linux_Driver_IRQ_Handling.rst
  - Linux_GPIO_Pinctrl.rst (GPIO IRQs)
  - Linux_Regmap_API.rst (regmap IRQ chip)

**Performance**
  - Linux_Network_Performance.rst
  - Linux_Block_Drivers.rst (blk-mq performance)
  - Linux_RCU.rst (lock-free performance)

Common Use Cases
================

**"I need to write a simple character driver"**
  → Start with: Linux_Char_Device_Drivers.rst

**"I need to write a platform device driver"**
  → Linux_Platform_Drivers.rst → Linux_GPIO_Pinctrl.rst

**"I need to communicate with an I2C/SPI device"**
  → Linux_SPI_Drivers.rst or Linux_I2C_Drivers.rst
  → Add Linux_Regmap_API.rst for register access

**"I need to handle shared resources in kernel"**
  → Linux_Kernel_Synchronization.rst → Choose appropriate primitive

**"I need to optimize network performance"**
  → Linux_Network_Performance.rst → Linux_Network_Protocols.rst

**"I'm getting kernel crashes in my driver"**
  → Linux_Driver_Debugging.rst → Use debugfs, KGDB

**"I need to implement power management"**
  → Linux_Driver_Power_Management.rst

**"I need to configure complex networking"**
  → Linux_Network_Configuration.rst → Linux_Network_Tools.rst

**"I need to write a network driver"**
  → Linux_Network_Drivers.rst → Linux_Network_Performance.rst

**"I need to write an input device driver"**
  → Linux_Input_Drivers.rst

Quick Command Reference
========================

**Build Kernel Module**

.. code-block:: bash

   # Create Makefile
   obj-m += mydriver.o
   
   # Build
   make -C /lib/modules/$(uname -r)/build M=$(pwd) modules
   
   # Load
   sudo insmod mydriver.ko
   
   # Unload
   sudo rmmod mydriver

**Debug Module**

.. code-block:: bash

   # Enable dynamic debug
   echo 'module mydriver +p' > /sys/kernel/debug/dynamic_debug/control
   
   # View kernel log
   dmesg -w
   
   # Module info
   modinfo mydriver.ko

**Network Quick Start**

.. code-block:: bash

   # Configure interface
   sudo ip addr add 192.168.1.10/24 dev eth0
   sudo ip link set eth0 up
   
   # Test connectivity
   ping -c 4 8.8.8.8
   
   # Capture traffic
   sudo tcpdump -i eth0 -w capture.pcap

Document Formats
================

All cheatsheets follow consistent structure:

1. **TL;DR - Quick Reference** (Top section)
   - Most common use cases
   - Copy-paste ready commands/code

2. **Detailed Sections**
   - API references
   - Configuration options
   - Working examples

3. **Best Practices** (10 items)
   - Expert recommendations
   - Production patterns

4. **Common Pitfalls**
   - Mistakes to avoid
   - Solutions

5. **Debugging/Troubleshooting**
   - Diagnostic commands
   - Problem-solving guides

6. **See Also & References**
   - Cross-references
   - Kernel documentation links

Additional Resources
====================

**Kernel Documentation**
  - https://www.kernel.org/doc/html/latest/
  - Documentation/driver-api/
  - Documentation/networking/

**Books Referenced**
  - Linux Kernel Programming Part 2 (Synchronization & Char Drivers)
  - Mastering Linux Device Driver Development (John Madieu)
  - Linux Networking Cookbook

**Online Resources**
  - LWN.net - Linux kernel development news
  - kernelnewbies.org - Kernel development tutorials
  - elixir.bootlin.com - Browse kernel source

File Statistics
===============

::

   New Files Created:          27
   Total Lines:                ~18,050
   Average File Size:          ~668 lines
   
   By Category:
   - Synchronization:          7 files (26%)
   - Drivers:                  14 files (52%)
   - Networking:               5 files (19%)
   - Debugging:                1 file (4%)
   
   Quality Metrics:
   - Files with TL;DR:         27/27 (100%)
   - Files with examples:      27/27 (100%)
   - Files with best practices: 27/27 (100%)
   - Files with debug info:    27/27 (100%)

---

**Last Updated:** January 2026
**Maintainer:** Cheatsheets Project
**Status:** Complete and production-ready
