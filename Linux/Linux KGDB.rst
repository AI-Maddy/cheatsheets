================================================================================
🐛 JTAG & KGDB – Linux Kernel Debugging Cheatsheet (Early 2026)
================================================================================

**Comprehensive guide to low-level Linux kernel debugging**

*Kernel ~6.12+ era – covering hardware (JTAG) & software (KGDB) approaches*

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

📖 Introduction to Kernel Debugging Methods
================================================================================

🎯 **Why Two Methods?**

- **JTAG**: Hardware debugger (ICE) – can stop CPU independently, debug bootloader & early kernel
- **KGDB**: Software debugger (GDB stub) – lighter weight, no extra hardware, great for stable systems

**Your Choice Depends On:**

✓ Are you debugging **early boot**? → JTAG
✓ Is **hardware stable**? → KGDB (simpler!)
✓ System **completely hung**? → JTAG (more reliable)
✓ **No hardware available**? → KGDB (only needs serial)


⚖️ Quick Comparison: JTAG vs KGDB
================================================================================

+----------------------------------+--------------------------------------+--------------------------------------+
| **Feature**                      | **🔧 JTAG (Hardware)**               | **📡 KGDB (Software)**               |
+==================================+======================================+======================================+
| **Type**                         | Hardware debugger (ICE)              | Kernel GDB stub (in kernel)          |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Intrusiveness**                | 🟢 Non-intrusive (stops CPU)         | 🟡 Intrusive (requires kernel code)  |
+----------------------------------+--------------------------------------+--------------------------------------+
| **When it works**                | Early boot → bootloader → kernel    | Stable kernel running                |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Hardware needed**              | 🔴 JTAG probe ($50–$2000+)           | 🟢 None (uses serial/Ethernet)       |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Performance impact**           | 🟢 Minimal                           | 🟡 Small (polling + serial overhead) |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Breakpoints (HW/SW)**          | 🟢 🟢 ✅ Unlimited hardware breaks         | 🟢 🟢 ✅ SW breaks (fewer hardware)         |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Trace (ETM/ETB)**              | 🟢 🟢 ✅ Yes (if supported)                | 🔴 🔴 ❌ No                                |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Setup complexity**             | 🟡 Medium (OpenOCD + probe)          | 🟢 Easy (kernel config + serial)     |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Cost (hobby/pro)**             | 💰💰 Medium–High                     | 💰 Free                              |
+----------------------------------+--------------------------------------+--------------------------------------+
| **Reliability on panic**         | 🟢 Excellent                         | 🟡 Moderate (depends on corruption) |
+----------------------------------+--------------------------------------+--------------------------------------+


🐧 ⭐ 🐧 Essential Kernel Configuration (Both Methods)
================================================================================

🛠️ **Base Debug Configuration:**

.. code-block:: bash

⭐    # Symbols & debug info (essential!)
   CONFIG_DEBUG_INFO=y                    # Full DWARF debug symbols
   CONFIG_DEBUG_INFO_REDUCED=n            # 🔴 🔴 Avoid stripped symbols
🐧    CONFIG_GDB_SCRIPTS=y                   # Kernel GDB helpers (lx-*, etc.)
   
   # Address randomization (disable for stable addresses)
   nokaslr                                # Kernel command line

🟢 **Optional but Useful:**

.. code-block:: bash

   CONFIG_KASAN=y                         # Memory sanitizer
   CONFIG_KCSAN=y                         # Concurrency sanitizer
   CONFIG_FRAME_POINTER=y                 # Better backtraces
   CONFIG_DEBUG_KERNEL=y                  # General debug features
   CONFIG_BUG=y                           # Panic on BUG()
⭐    CONFIG_MAGIC_SYSRQ=y                   # Magic SysRq key (for KGDB entry)


🐛 ⭐⭐⭐ KGDB – Software Debugging (Most Common)
================================================================================

**🟢 🟢 Best for:** Normal kernel/driver development when hardware is stable

**Setup: 3 Easy Steps**

🐧 Step 1️⃣ : Kernel Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Minimum config
   CONFIG_KGDB=y
   CONFIG_KGDB_SERIAL_CONSOLE=y          # Main method (serial/USB)
   
   # Optional
   CONFIG_KGDB_KDB=y                     # kdb shell (lightweight alternative)
   CONFIG_KGDB_TESTS=n                   # Self-tests (not needed for production)

🐧 Step 2️⃣ : Boot Kernel with KGDB Enabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Option A: Wait at boot for debugger (most convenient)**

.. code-block:: bash

   # Kernel command line (in bootloader or grub.cfg)
   kgdbwait kgdboc=ttyS0,115200
   
   # Or for USB console
   kgdbwait kgdboc=ttyUSB0,115200
   
   # Network variant (if patched)
   kgdbwait kgdboc=eth0

**Option B: Drop into KGDB manually (after boot)**

.. code-block:: bash

   # From running kernel (if MAGIC_SYSRQ enabled)
   echo g > /proc/sysrq-trigger
   
   # Or press Alt+SysRq+G (if running interactive)
   # Or from userspace:
   sync; echo g > /proc/sysrq-trigger

Step 3️⃣ : Connect GDB from Host
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Terminal 1: Watch serial port (optional, for debug output)
   screen /dev/ttyUSB0 115200
   # or
   minicom -D /dev/ttyUSB0 -b 115200
   
   # Terminal 2: Launch GDB
🐧    arm-linux-gnueabihf-gdb ./vmlinux
   
   (gdb) target remote /dev/ttyUSB0      # Connect to serial device
   # or
   (gdb) target remote :1234             # If using network/socat bridge

**At this point:**

- 🟢 🟢 ✅ Kernel is halted, waiting for debugger commands
- 🟢 🟢 ✅ You can set breakpoints, step, inspect memory
- 🟢 🟢 ✅ Use standard GDB commands (see reference below)


🐛 ⭐⭐⭐⭐ JTAG – Hardware Debugging (Professional / Bring-up)
================================================================================

**🟢 🟢 Best for:** Early boot, bootloader debugging, hard hangs, timing-sensitive code

**Hardware Options (2026 Popular Choices):**

=======================  =====================  ================  =================
**Probe Type**           **Popular Models**     **Cost**          **Support Level**
=======================  =====================  ================  =================
SEGGER J-Link            EDU Mini (~$60)        💰 Budget         ⭐⭐⭐ Excellent
                         Pro ($300–$1000)       💰💰 Professional
ST-Link                  V2 Clones ($5–$15)     💰 Budget         ⭐⭐ 🟢 🟢 Good
                         V3 Official ($25)      💰 Budget
OpenOCD-Compatible       FT2232 (DIY)           💰 Budget         ⭐⭐ 🟢 🟢 Good
                         Tigard / Bus Pirate
Lauterbach TRACE32       —                      💰💰💰 Enterprise  ⭐⭐⭐⭐ Excellent
=======================  =====================  ================  =================

**Setup: 4 Steps (with OpenOCD + GDB)**

🔧 Step 1️⃣ : Hardware Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✓ Connect JTAG probe to board JTAG pins (TCO, TDI, TDO, TMS, GND, VCC)
✓ Ensure JTAG pins NOT muxed to other functions (check device tree / pinctrl)
✓ USB cable from probe to host PC

Step 2️⃣ : Install OpenOCD
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install openocd
   
   # Or build from source
   git clone https://git.code.sf.net/p/openocd/code openocd
   cd openocd && ./bootstrap && ./configure && make && sudo make install

Step 3️⃣ : Start OpenOCD with Your Board Config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Example: STM32H7 board with ST-Link**

.. code-block:: bash

   openocd -f interface/stlink.cfg \
           -f target/stm32h7x.cfg
   
   # OpenOCD output should show:
   # Open On-Chip Debugger 0.12.0 ...
   # Info : Listening on port 6666 for tcl connections
   # Info : Listening on port 4444 for telnet connections
   # Info : Listening on port 3333 for gdb connections

**Example: ARM Cortex-A (Raspberry Pi, BeagleBone, etc.)**

.. code-block:: bash

   # Raspberry Pi 4/5 with GPIO JTAG
   openocd -f interface/raspberrypi-native.cfg -f target/bcm2711.cfg
   
   # Generic ARM Cortex-A with J-Link
   openocd -f interface/jlink.cfg -f target/cortex_a.cfg
   
   # STM32L4 (low-power)
   openocd -f interface/stlink.cfg -f target/stm32l4x.cfg

**Where to find configs:**

.. code-block:: bash

   ls /usr/share/openocd/scripts/interface/   # Available probes
   ls /usr/share/openocd/scripts/target/      # Available targets

🐛 Step 4️⃣ : Connect GDB and Debug
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Terminal 1: OpenOCD running (from Step 3)**

**Terminal 2: Launch GDB**

.. code-block:: bash

🐧    arm-linux-gnueabihf-gdb ./vmlinux
   
   (gdb) target remote :3333              # Connect to OpenOCD GDB server
   (gdb) monitor reset halt               # Reset CPU and halt
   # or
⚙️    (gdb) monitor reset init               # Reset with initialization
   
   # Now set breakpoint at kernel entry
   (gdb) hbreak *0x80000000               # Adjust for your kernel physical address!
   (gdb) monitor reset                    # Reset board again
   # → CPU stops at breakpoint, ready for inspection


💡 🎯 JTAG Pro Tips (Advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Early Kernel Entry (Very Common Pattern):**

.. code-block:: bash

   # Before reset, find your kernel entry point
   # (typically at physical address 0x80000000 for ARM, 0x1000000 for ARM64)
   
   (gdb) file ./vmlinux
   (gdb) info sym *0x80000000            # Check symbol at that address
   (gdb) hbreak *0x80000000              # Hardware breakpoint
   (gdb) target remote :3333
   (gdb) monitor reset                   # Reset board → stops at hbreak
   (gdb) x/10i $pc                       # Disassemble first kernel instructions
   (gdb) stepi                           # Step through head.S / start_kernel

**Load Kernel Binary (if not already in ROM/RAM):**

.. code-block:: bash

   (gdb) load                            # Loads vmlinux to RAM (slow!)
   # Or for faster flash loading:
   (gdb) monitor program ./vmlinux       # OpenOCD-specific

**Debug Bootloader (U-Boot Example):**

.. code-block:: bash

   arm-linux-gnueabihf-gdb u-boot
   (gdb) target remote :3333
   (gdb) monitor reset halt
   (gdb) hbreak *0x87800000              # Typical U-Boot load address
   (gdb) continue
   # → U-Boot starts, stops at hbreak


⭐ Essential GDB Commands (Both KGDB & JTAG)
================================================================================

**Breakpoints & Stepping:**

.. code-block:: bash

   hbreak <symbol>              # Hardware breakpoint (JTAG only, unlimited)
   hbreak *0x80000000          # Hardware BP at address
   break <symbol>               # Software breakpoint (limited)
   watch <expr>                 # Watchpoint (stop if value changes)
   info break                   # List all breakpoints
   delete 1                     # Delete breakpoint #1
   
   continue / c                 # Run until breakpoint
   stepi / si                   # Step 1 instruction
   nexti / ni                   # Next instruction (skip calls)
   finish                       # Run until function returns
   until <line>                 # Run until line reached


**Inspection:**

.. code-block:: bash

   backtrace / bt               # Stack trace
   frame 0                      # Select frame (in backtrace)
   info registers               # Show all registers
   info locals                  # Local variables
   print <var>                  # Print variable value
   x/32x 0x80000000            # Examine 32 words at address (hex)
   x/32xb $sp                   # Examine bytes at stack pointer
   disassemble <func>          # Disassemble function


**State Modification:**

.. code-block:: bash

   set $pc = 0x80008000        # Force program counter
   set $r0 = 0x12345678        # Set register value
   set *(int*)0x80000000 = 0   # Write to memory
   call some_function()         # Call kernel function (risky!)


**Kernel-Specific GDB Scripts (CONFIG_GDB_SCRIPTS=y):**

.. code-block:: bash

   # After connecting, these commands available:
   lx-symbols              # Load module symbols dynamically
   lx-dmesg                # Print kernel dmesg buffer
   lx-ps                   # List processes
   lx-tasks                # Like ps with more detail
   lx-iomem                # I/O memory regions
   lx-modulelist           # Loaded modules
🐧    lx-version              # Kernel version
   
   # Example:
   (gdb) lx-symbols
   (gdb) lx-dmesg

**OpenOCD-Specific Commands (via GDB monitor):**

.. code-block:: bash

   monitor reset halt          # Reset & halt CPU
   monitor reset init          # Reset with board init
   monitor reset run           # Reset & run
   monitor flash info 0        # Flash info (OpenOCD target)
   monitor targets             # List available targets
   monitor reg                 # Show registers (OpenOCD view)
   monitor help                # OpenOCD command help


Quick Troubleshooting
================================================================================

🔴 **KGDB: No connection from GDB**

.. code-block:: bash

   # Check kernel has KGDB enabled
   dmesg | grep -i kgdb
   
   # Verify serial device
   ls -la /dev/ttyUSB0
   
   # Try setting up serial manually
   stty -F /dev/ttyUSB0 115200 raw
   
   # Check if waiting for debugger
   cat /proc/cmdline | grep kgdbwait

🔴 **JTAG: OpenOCD won't connect to probe**

.. code-block:: bash

   # List USB devices
   lsusb
   
   # Check permissions (may need udev rules)
   sudo usermod -a -G dialout,plugdev $USER
   
   # Run OpenOCD with verbose output
   openocd -d 3 -f interface/stlink.cfg -f target/stm32h7x.cfg

🔴 **GDB: Can't read symbols from vmlinux**

.. code-block:: bash

   # Verify vmlinux has debug info
   file ./vmlinux
⚙️    # Should show: ELF 32-bit LSB executable, version 1 (SYSV), dynamically linked...
   
   readelf -S ./vmlinux | grep debug
   # Should show .debug_info, .debug_line, etc.

🔴 **Breakpoint not working**

.. code-block:: bash

   # Use hardware breakpoints (JTAG only)
   hbreak <symbol>        # NOT break
   
   # Check KASLR disabled
   cat /proc/cmdline | grep nokaslr
   
   # Adjust address for actual kernel load
   info symbol 0x80000000


⚙️ Modern Recommendations (Early 2026)
================================================================================

📌 **Scenario-Based Guidance:**

**Scenario 1: Board Bring-up / Very Early Boot**
   → 🔧 **JTAG + OpenOCD + GDB** (🟢 🟢 best reliability)
   → Optional: SEGGER J-Link EDU ($60) or ST-Link ($15)

**Scenario 2: Normal Kernel/Driver Development**
   → 📡 **KGDB** (simpler, no hardware)
   → Serial console + kernel config

**Scenario 3: Timing-Sensitive / Real-Time**
   → 🔧 **JTAG + Trace (ETM/ETB)** if supported
   → Or Lauterbach TRACE32 (professional)

**Scenario 4: QEMU / Virtual Testing**
🔧    → 🟢 **Built-in gdbstub** (no hardware needed!)
   
💻    .. code-block:: bash
   
      qemu-system-arm -S -s -kernel vmlinux -m 512
      # Then: gdb ./vmlinux → target remote :1234

**Scenario 5: Budget / Hobbyist**
   → ST-Link clones ($5–15) + OpenOCD (free)
   → Or invest in J-Link EDU ($60)

**Scenario 6: Professional / Production**
   → 💎 Lauterbach TRACE32 + ETM/ETB
   → Excellent trace, CI integration, support


⚙️ Popular OpenOCD Configurations (Copy-Paste Ready)
================================================================================

**ST-Link + STM32H7:**

.. code-block:: bash

   openocd -f interface/stlink.cfg \
           -f target/stm32h7x.cfg

**J-Link + Cortex-M4:**

.. code-block:: bash

   openocd -f interface/jlink.cfg \
           -f target/cortex_m4.cfg

**Raspberry Pi 4/5 (GPIO JTAG):**

.. code-block:: bash

   openocd -f interface/raspberrypi-native.cfg \
           -f target/bcm2711.cfg

**Generic ARM Cortex-A53:**

.. code-block:: bash

   openocd -f interface/stlink.cfg \
           -f target/cortex_a.cfg

**QEMU ARM (via GDB server in QEMU):**

.. code-block:: bash

   # No OpenOCD needed! QEMU has built-in gdbstub
   qemu-system-arm -S -s -kernel vmlinux
   # Then: gdb vmlinux → target remote :1234


⚙️ Decision Tree: Which Method to Use?
================================================================================

.. code-block:: text

   Need to debug Linux kernel?

   ├── Debugging EARLY BOOT (bootloader/head.S)?
   │   └── → 🔧 JTAG (only way to catch early hangs)
   │
   ├── System completely HUNG (unresponsive)?
   │   └── → 🔧 JTAG (more reliable on panic)
   │
   ├── Debugging RUNNING KERNEL (driver, syscall)?
   │   ├── Have JTAG hardware? → 🔧 JTAG (🟢 🟢 good choice!)
   │   └── No JTAG? → 📡 KGDB (perfectly fine, simpler setup)
   │
   ├── Using QEMU / Virtual environment?
   │   └── → 🟢 Built-in gdbstub (no hardware!)
   │
   └── Need TRACE (cycle-accurate execution)?
       └── → 🔧 JTAG + ETM/ETB (if SoC supports)


⭐ Key Takeaways
================================================================================

✨ **JTAG (🔧 Hardware):**
   🟢 🟢 ✅ Catches early boot, bootloader, hard hangs
   🟢 🟢 ✅ Unlimited hardware breakpoints
   🟢 🟢 ✅ More reliable when kernel is panicked
   🔴 🔴 ❌ Needs probe hardware
   🔴 🔴 ❌ More setup complexity

✨ **KGDB (📡 Software):**
   🟢 🟢 ✅ No extra hardware needed
   🟢 🟢 ✅ Simple serial/USB connection
   🟢 🟢 ✅ Great for stable systems
   🔴 🔴 ❌ Can't debug bootloader
   🔴 🔴 ❌ Less reliable on panic

✨ **Both use standard GDB:**
   → Same commands (break, step, backtrace, print, etc.)
   → Same vmlinux symbols
   → Can switch methods mid-project


================================================================================

**Happy kernel debugging!** ⚡🐧🔧

*References: OpenOCD docs (https://openocd.org), Linux kernel docs, GDB manual*

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
