🐧 **Linux Kernel Programming for Aircraft Systems**
════════════════════════════════════════════════════

**Last Updated:** January 2026  
**Target Role:** Aircraft Services Architect  
**Relevance:** 2026+ aircraft running embedded Linux (IFE, avionics, EFB)

════════════════════════════════════════════════════════════════════

📋 **TABLE OF CONTENTS**
────────────────────────

1. Overview & Context
2. Linux Distributions for Aviation
3. Real-Time Linux (PREEMPT_RT)
4. Device Driver Development
5. Kernel Modules for Avionics Buses
6. Security: SELinux & AppArmor
7. Network Stack Customization
8. Power Management & Boot Optimization
9. Debugging & Diagnostics
10. Certification Considerations
11. Practical Examples
12. Common Pitfalls
13. Quick Reference Card
14. Exam Questions
15. Further Reading

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — Quick Takeaways**
──────────────────────────────

✅ **Wind River Linux** (DO-178C pre-qualified), **Yocto Project** (customizable), **Embedded Debian** (general-purpose)  
✅ **PREEMPT_RT** patches reduce worst-case latency from ~200ms to <100µs (critical for ARINC 664 traffic)  
✅ **Kernel modules** (.ko) for CAN, ARINC 429, MIL-STD-1553 buses (avoid out-of-tree drivers for certification)  
✅ **SELinux** (mandatory access control) for DAL B+, **AppArmor** for passenger services  
✅ **Device Tree** (.dtb) describes hardware (no hardcoded addresses), required for ARM/RISC-V  
✅ **Kdump/kexec** for crash dumps, **KGDB** for remote debugging  
✅ **Secure Boot** with signed kernel images (UEFI Secure Boot + IMA/EVM)

════════════════════════════════════════════════════════════════════

🏢 **1. OVERVIEW & CONTEXT**
────────────────────────────

**Why Linux in Aircraft?**

+--------------------------+------------------------------------+
| Traditional RTOS         | Modern Embedded Linux              |
+==========================+====================================+
| VxWorks, QNX, Integrity  | Yocto, Wind River, Debian          |
| Proprietary, expensive   | Open-source, cost-effective        |
| Limited ecosystem        | Rich ecosystem (Docker, systemd)   |
| Hard real-time (µs)      | Soft real-time with PREEMPT_RT     |
| Small footprint (MB)     | Medium footprint (10-100 MB)       |
+--------------------------+------------------------------------+

**Aircraft Use Cases:**

🎥 **IFE Systems**:
   - Video streaming (4K, 8K codecs)
   - Passenger connectivity (Wi-Fi, Bluetooth)
   - Entertainment libraries (MySQL, SQLite)

✈️ **Avionics (Non-Flight-Critical)**:
   - Electronic Flight Bags (EFB)
   - Aircraft Condition Monitoring Systems (ACMS)
   - Ground maintenance terminals

🛰️ **Connectivity Gateways**:
   - Satellite modem controllers
   - ARINC 664 switches (network management plane only, not data plane)

════════════════════════════════════════════════════════════════════

🏭 **2. LINUX DISTRIBUTIONS FOR AVIATION**
──────────────────────────────────────────

**Wind River Linux**
~~~~~~~~~~~~~~~~~~~~

- **DO-178C pre-qualified** (DAL A-C with VxWorks Cert Edition, Linux for DAL D-E)
- PREEMPT_RT patches integrated
- Commercial support (SLA, long-term maintenance)
- **Cost:** ~$50K-$200K per aircraft program

**Yocto Project (OpenEmbedded)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Highly customizable** (build only what you need)
- Layer-based architecture (meta-oe, meta-avionics)
- Reproducible builds (BitBake recipes)
- **Free** but requires in-house expertise
- Example: Airbus A350 uses Yocto-based Linux for IFE

**Embedded Debian/Ubuntu**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Rapid prototyping (apt-get ecosystem)
- **NOT suitable for DAL B+** (too many packages, attack surface)
- Good for development boards, ground test equipment

**Buildroot**
~~~~~~~~~~~~~

- Simpler than Yocto (Makefiles, not Python)
- Faster builds (~20 min vs. ~2 hours for Yocto)
- Less flexible (monolithic config)

════════════════════════════════════════════════════════════════════

⏱️ **3. REAL-TIME LINUX (PREEMPT_RT)**
───────────────────────────────────────

**What is PREEMPT_RT?**

- **Patch set** that makes Linux fully preemptible (no unbounded critical sections)
- Reduces **worst-case latency** from ~200ms (stock kernel) to <100µs
- Required for:
  - ARINC 664 packet processing (1ms deadlines)
  - CAN bus frame transmission (<10ms jitter)
  - Audio/video synchronization (±20ms A/V sync)

**Key Changes:**

1. **Spinlocks → RT Mutexes**
   - Spinlocks are preemptible (priority inheritance)
   
2. **Interrupt Handlers → Kernel Threads**
   - Hard IRQ handlers run as `irq/N-<device>` threads
   - Example: `irq/45-i2c`, `irq/78-can0`

3. **Priority-Based Scheduling**
   - `chrt` command: Set real-time priority (0-99)
   - SCHED_FIFO, SCHED_RR policies

**Example: Setting RT Priority**

.. code-block:: bash

   # Make process PID 1234 real-time with priority 50
   sudo chrt -f -p 50 1234
   
   # Check priorities
   ps -eo pid,cls,pri,rtprio,cmd | grep -E "FF|RR"

**Configuration:**

.. code-block:: text

   # Kernel config for PREEMPT_RT
   CONFIG_PREEMPT_RT=y
   CONFIG_NO_HZ_FULL=y         # Tickless kernel (reduce interrupts)
   CONFIG_RCU_NOCB_CPU=y       # Offload RCU callbacks
   CONFIG_IRQ_TIME_ACCOUNTING=y

**Benchmark Example:**

+-----------------------+--------------+------------------+
| Workload              | Stock Kernel | PREEMPT_RT       |
+=======================+==============+==================+
| Avg latency           | 50µs         | 20µs             |
| 99.9th percentile     | 2ms          | 80µs             |
| **Worst case**        | **200ms**    | **95µs** ✅      |
+-----------------------+--------------+------------------+

════════════════════════════════════════════════════════════════════

🔌 **4. DEVICE DRIVER DEVELOPMENT**
───────────────────────────────────

**Character Device Example (CAN Interface)**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/can.h>
   
   static int major;
   static struct cdev can_cdev;
   
   static ssize_t can_read(struct file *file, char __user *buf,
                           size_t len, loff_t *offset) {
       struct can_frame frame;
       // Read from CAN hardware
       if (copy_to_user(buf, &frame, sizeof(frame)))
           return -EFAULT;
       return sizeof(frame);
   }
   
   static struct file_operations fops = {
       .owner = THIS_MODULE,
       .read = can_read,
       .write = can_write,
       .open = can_open,
       .release = can_release,
   };
   
   static int __init can_driver_init(void) {
       major = register_chrdev(0, "can_device", &fops);
       printk(KERN_INFO "CAN driver loaded, major=%d\n", major);
       return 0;
   }
   
   module_init(can_driver_init);
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Aircraft Architect");

**Device Tree (ARM/RISC-V)**

.. code-block:: dts

   /* ARINC 429 device tree node */
   arinc429@40010000 {
       compatible = "vendor,arinc429-v1";
       reg = <0x40010000 0x1000>;
       interrupts = <GIC_SPI 45 IRQ_TYPE_LEVEL_HIGH>;
       clock-frequency = <100000>;  /* 100 kHz word rate */
       status = "okay";
   };

**Driver Types:**

🟢 **In-Tree Drivers** (mainline kernel):
   - Maintained by kernel community
   - Easier for certification (evidence of peer review)
   - Examples: `can.ko`, `i2c-core.ko`

🟡 **Out-of-Tree Drivers** (vendor-provided):
   - Proprietary interfaces (ARINC 429 chips)
   - Requires extra documentation for DO-178C
   - Must be signed for Secure Boot

════════════════════════════════════════════════════════════════════

🚌 **5. KERNEL MODULES FOR AVIONICS BUSES**
───────────────────────────────────────────

**CAN Bus (SocketCAN)**

.. code-block:: bash

   # Load CAN driver
   modprobe can
   modprobe vcan  # Virtual CAN for testing
   
   # Create virtual CAN interface
   ip link add dev vcan0 type vcan
   ip link set up vcan0
   
   # Send CAN frame
   cansend vcan0 123#DEADBEEF
   
   # Monitor CAN traffic
   candump vcan0

**ARINC 429**

.. code-block:: c

   /* ARINC 429 word structure (32-bit) */
   struct arinc429_word {
       uint8_t label;       /* Bits 1-8 (reversed) */
       uint8_t sdi;         /* Source/Destination Identifier */
       uint32_t data : 19;  /* Bits 11-29 */
       uint8_t ssm;         /* Sign/Status Matrix */
       uint8_t parity;      /* Bit 32 (odd parity) */
   };
   
   /* Driver sends word to hardware FIFO */
   ioctl(fd, ARINC429_SEND, &word);

**MIL-STD-1553**

.. code-block:: bash

   # Load 1553 driver (vendor-specific)
   insmod /lib/modules/$(uname -r)/extra/mil1553.ko
   
   # Create Bus Controller (BC) device
   echo "bc" > /sys/class/mil1553/mil0/mode
   
   # Send command/data word
   echo "1A 1234 5678" > /sys/class/mil1553/mil0/tx

════════════════════════════════════════════════════════════════════

🛡️ **6. SECURITY: SELINUX & APPARMOR**
───────────────────────────────────────

**SELinux (Security-Enhanced Linux)**

- **Mandatory Access Control (MAC)** (vs. DAC = Discretionary Access Control)
- Policies define what processes can access (files, sockets, capabilities)
- Required for DAL B+ systems

**SELinux Modes:**

+----------------+-----------------------------------------------+
| Mode           | Description                                   |
+================+===============================================+
| **Enforcing**  | Policies are enforced (default for prod)      |
| **Permissive** | Log violations but don't block (testing)      |
| **Disabled**   | SELinux off (NOT ALLOWED for DAL B+)         |
+----------------+-----------------------------------------------+

**Example Policy (IFE Media Player):**

.. code-block:: text

   # Only allow media_player_t to read from /data/media
   allow media_player_t media_data_t:file { read open };
   
   # Deny network access
   neverallow media_player_t internet_t:tcp_socket connect;

**AppArmor (Alternative to SELinux)**

- **Profile-based** (simpler than SELinux policies)
- Used in Ubuntu-based aircraft systems

**Example Profile:**

.. code-block:: text

   #include <tunables/global>
   
   /usr/bin/ife-player {
     #include <abstractions/base>
     #include <abstractions/video>
     
     /data/media/** r,              # Read-only media
     /dev/video0 rw,                # Access video device
     deny network inet,             # No network access
   }

**Commands:**

.. code-block:: bash

   # Load AppArmor profile
   apparmor_parser -r /etc/apparmor.d/ife-player
   
   # Check status
   aa-status

════════════════════════════════════════════════════════════════════

🌐 **7. NETWORK STACK CUSTOMIZATION**
──────────────────────────────────────

**ARINC 664 AFDX (Avionics Full-Duplex Ethernet)**

- Deterministic Ethernet (100 Mbps, switched)
- Virtual Links (VL) = guaranteed bandwidth

**Kernel Configuration:**

.. code-block:: text

   CONFIG_NET_SCHED=y           # Traffic control
   CONFIG_NET_SCH_PRIO=y        # Priority queuing
   CONFIG_NET_SCH_TBF=y         # Token bucket filter
   CONFIG_VLAN_8021Q=y          # VLAN tagging

**Traffic Shaping (tc command):**

.. code-block:: bash

   # Create VLAN for avionics (VL 100)
   ip link add link eth0 name eth0.100 type vlan id 100
   
   # Set bandwidth limit (1 Mbps for VL 100)
   tc qdisc add dev eth0.100 root tbf rate 1mbit burst 10kb latency 50ms
   
   # Priority queuing (avionics > passenger traffic)
   tc qdisc add dev eth0 root handle 1: prio bands 3
   tc filter add dev eth0 parent 1:0 protocol ip prio 1 u32 \
       match ip protocol 17 0xff flowid 1:1  # UDP = high priority

**Network Namespace (Isolation):**

.. code-block:: bash

   # Create namespace for passenger Wi-Fi
   ip netns add passenger
   
   # Move interface to namespace
   ip link set wlan0 netns passenger
   
   # Verify isolation (cannot ping from default namespace)
   ping 10.1.1.1  # Fails (wlan0 not visible)

════════════════════════════════════════════════════════════════════

🔋 **8. POWER MANAGEMENT & BOOT OPTIMIZATION**
───────────────────────────────────────────────

**CPU Frequency Scaling**

.. code-block:: bash

   # Set CPU governor (performance = max frequency)
   echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
   
   # Disable CPU idle states (reduce latency)
   cpupower idle-set -D 0

**Fast Boot (<5 seconds):**

1. **Disable unnecessary services:**

.. code-block:: bash

   systemctl disable bluetooth.service
   systemctl disable avahi-daemon.service

2. **Use initramfs (skip full filesystem check):**

.. code-block:: bash

   # Kernel command line
   rootwait ro init=/sbin/init quiet

3. **Parallel init (systemd):**

.. code-block:: text

   # /etc/systemd/system.conf
   DefaultTimeoutStartSec=5s

**Power Budget:**

+---------------------+---------------+---------------+
| Component           | Active        | Idle          |
+=====================+===============+===============+
| ARM Cortex-A53 (4x) | 2.5 W         | 0.5 W         |
| Display (10" LCD)   | 5 W           | 0.1 W (sleep) |
| eMMC storage        | 0.8 W         | 0.05 W        |
| **Total**           | **8.3 W**     | **0.65 W**    |
+---------------------+---------------+---------------+

════════════════════════════════════════════════════════════════════

🐛 **9. DEBUGGING & DIAGNOSTICS**
──────────────────────────────────

**Kdump (Crash Dumps)**

.. code-block:: bash

   # Reserve memory for crash kernel
   crashkernel=128M
   
   # Load crash kernel
   kexec -p /boot/vmlinuz --initrd=/boot/initrd.img --append="root=/dev/sda1"
   
   # Analyze dump with crash utility
   crash /usr/lib/debug/vmlinux /var/crash/vmcore

**KGDB (Kernel Debugger)**

.. code-block:: bash

   # Kernel command line
   kgdboc=ttyS0,115200 kgdbwait
   
   # Connect from another machine
   (gdb) target remote /dev/ttyS0
   (gdb) break schedule
   (gdb) continue

**ftrace (Function Tracing)**

.. code-block:: bash

   # Trace all kernel functions
   echo function > /sys/kernel/debug/tracing/current_tracer
   
   # Filter by function name
   echo "can_*" > /sys/kernel/debug/tracing/set_ftrace_filter
   
   # Read trace
   cat /sys/kernel/debug/tracing/trace

**perf (Performance Analysis)**

.. code-block:: bash

   # CPU profiling
   perf record -a -g sleep 10
   perf report
   
   # Measure context switches
   perf stat -e sched:sched_switch ./my_app

════════════════════════════════════════════════════════════════════

✈️ **10. CERTIFICATION CONSIDERATIONS**
────────────────────────────────────────

**DO-178C Applicability:**

+-------------+-------------------+-----------------------------------+
| DAL         | Linux Kernel?     | Rationale                         |
+=============+===================+===================================+
| **A**       | ❌ NO             | Too complex (20M+ LOC)            |
| **B**       | ❌ NO             | Insufficient determinism          |
| **C**       | ⚠️ POSSIBLE       | With PREEMPT_RT + partitioning    |
| **D**       | ✅ YES            | IFE, EFB (non-safety-critical)    |
| **E**       | ✅ YES            | Ground test equipment             |
+-------------+-------------------+-----------------------------------+

**Evidence Required (DAL D):**

1. **Software Configuration Index (SCI)**
   - Kernel version, config (.config file)
   - List of loaded modules (lsmod output)
   
2. **Tool Qualification (if using custom toolchain)**
   - GCC version, flags (e.g., `-O2`, `-fstack-protector`)
   
3. **Verification Evidence**
   - Test logs (LTP = Linux Test Project)
   - Static analysis (Coverity, CodeSonar)

**Hypervisor Approach (Higher DAL):**

::

   +-----------------------------------------------------------+
   |               Hypervisor (Jailhouse, Xen)                 |
   +-----------------------------------------------------------+
   | DAL A Partition       | DAL D Partition                   |
   | (VxWorks, Integrity)  | (Linux for IFE)                   |
   | Flight Control        | Entertainment, Wi-Fi              |
   +-----------------------------------------------------------+

════════════════════════════════════════════════════════════════════

💻 **11. PRACTICAL EXAMPLES**
──────────────────────────────

**Example 1: CAN Bus Driver (Minimal)**

.. code-block:: c

   // can_driver.c
   #include <linux/module.h>
   #include <linux/can.h>
   #include <linux/can/dev.h>
   
   static int can_probe(struct platform_device *pdev) {
       struct net_device *dev;
       struct can_priv *priv;
       
       dev = alloc_candev(sizeof(*priv), 1);
       if (!dev)
           return -ENOMEM;
       
       priv = netdev_priv(dev);
       priv->bittiming.bitrate = 500000;  /* 500 kbps */
       
       register_candev(dev);
       return 0;
   }
   
   static struct platform_driver can_driver = {
       .probe = can_probe,
       .driver = {
           .name = "aircraft-can",
       },
   };
   
   module_platform_driver(can_driver);

**Example 2: Yocto Recipe (Custom Kernel Module)**

.. code-block:: bitbake

   # meta-avionics/recipes-kernel/arinc429/arinc429-driver_1.0.bb
   DESCRIPTION = "ARINC 429 kernel module"
   LICENSE = "GPLv2"
   
   SRC_URI = "file://arinc429.c \
              file://Makefile"
   
   S = "${WORKDIR}"
   
   inherit module
   
   do_install() {
       install -d ${D}${base_libdir}/modules/${KERNEL_VERSION}/extra
       install -m 0644 arinc429.ko ${D}${base_libdir}/modules/${KERNEL_VERSION}/extra/
   }

**Example 3: Systemd Service (IFE Application)**

.. code-block:: ini

   # /etc/systemd/system/ife-player.service
   [Unit]
   Description=In-Flight Entertainment Player
   After=network.target
   Wants=mysql.service
   
   [Service]
   Type=simple
   ExecStart=/usr/bin/ife-player --config /etc/ife/config.yml
   Restart=always
   RestartSec=5s
   
   # Security hardening
   PrivateTmp=yes
   NoNewPrivileges=yes
   ProtectSystem=strict
   ProtectHome=yes
   
   [Install]
   WantedBy=multi-user.target

════════════════════════════════════════════════════════════════════

⚠️ **12. COMMON PITFALLS**
───────────────────────────

❌ **Pitfall 1: Using Stock Kernel for Real-Time**
   - **Problem:** Missed deadlines, high latency
   - **Solution:** Apply PREEMPT_RT patches

❌ **Pitfall 2: Out-of-Tree Drivers Without Documentation**
   - **Problem:** Certification blockers (unknown behavior)
   - **Solution:** Mainline drivers or vendor-provided docs

❌ **Pitfall 3: Hardcoded Device Addresses**
   - **Problem:** Not portable across hardware revisions
   - **Solution:** Use Device Tree (.dtb)

❌ **Pitfall 4: Disabling SELinux for "Convenience"**
   - **Problem:** Fails ED-203A security audit
   - **Solution:** Fix SELinux policies, don't disable

❌ **Pitfall 5: Large initramfs (>100 MB)**
   - **Problem:** Slow boot times (>20 seconds)
   - **Solution:** Compress with XZ, remove unused modules

════════════════════════════════════════════════════════════════════

📇 **13. QUICK REFERENCE CARD**
────────────────────────────────

**Essential Commands**

.. code-block:: bash

   # Kernel info
   uname -r                        # Kernel version
   cat /proc/cmdline               # Boot parameters
   
   # Module management
   lsmod                           # List loaded modules
   modinfo can                     # Module details
   insmod /path/to/module.ko       # Load module
   rmmod module_name               # Unload module
   
   # Device tree
   dtc -I dtb -O dts /boot/system.dtb   # Decompile DTB
   
   # Real-time
   chrt -f -p 90 1234              # Set FIFO priority
   
   # Network
   tc qdisc show dev eth0          # Show traffic control
   ip netns list                   # List namespaces
   
   # Debugging
   dmesg | tail -n 50              # Kernel log
   cat /proc/interrupts            # IRQ stats
   
   # Security
   getenforce                      # SELinux status
   aa-status                       # AppArmor status

**Key Files**

+-------------------------------------------+-----------------------------------+
| File                                      | Purpose                           |
+===========================================+===================================+
| `/proc/cmdline`                           | Kernel boot parameters            |
| `/sys/kernel/debug/tracing/`              | Ftrace interface                  |
| `/etc/selinux/config`                     | SELinux configuration             |
| `/boot/config-$(uname -r)`                | Kernel build config               |
| `/lib/modules/$(uname -r)/extra/`         | Out-of-tree modules               |
+-------------------------------------------+-----------------------------------+

════════════════════════════════════════════════════════════════════

📝 **14. EXAM QUESTIONS**
──────────────────────────

**Q1:** Why is PREEMPT_RT required for ARINC 664 packet processing?

**A1:** ARINC 664 has strict timing constraints (1ms frame deadlines). Stock Linux has worst-case latencies of ~200ms (due to non-preemptible sections), which violates these deadlines. PREEMPT_RT reduces latency to <100µs by making the kernel fully preemptible.

────────────────────────────────────────────────────────────────────

**Q2:** What's the difference between in-tree and out-of-tree drivers for DO-178C?

**A2:**  
- **In-tree:** Part of mainline kernel, peer-reviewed by kernel community (easier certification, documented behavior)  
- **Out-of-tree:** Vendor-provided, requires extra documentation (design specs, test evidence) for certification

────────────────────────────────────────────────────────────────────

**Q3:** How does SELinux prevent a compromised IFE app from accessing avionics data?

**A3:** SELinux uses mandatory access control (MAC) policies that label processes and files (e.g., `ife_app_t`, `avionics_data_t`). Even if the IFE app runs as root, the policy prevents `ife_app_t` from reading `avionics_data_t`.

────────────────────────────────────────────────────────────────────

**Q4:** Explain Device Tree and why it's required for ARM/RISC-V aircraft computers.

**A4:** Device Tree is a data structure (compiled as .dtb) that describes hardware (memory addresses, interrupts, clocks) to the kernel at boot. ARM/RISC-V CPUs don't have firmware-based device discovery (like x86 ACPI), so Device Tree is mandatory.

────────────────────────────────────────────────────────────────────

**Q5:** You see "Kernel panic - not syncing: VFS: Unable to mount root fs". What's wrong?

**A5:** The kernel can't find the root filesystem. Causes:  
1. Wrong `root=` parameter in `/proc/cmdline` (e.g., `/dev/sda1` vs. `/dev/mmcblk0p1`)  
2. Missing filesystem driver (e.g., ext4 not compiled in)  
3. Corrupted filesystem (run `fsck`)

════════════════════════════════════════════════════════════════════

📚 **15. FURTHER READING**
───────────────────────────

**Books:**
- *Linux Device Drivers* (3rd Edition) — Jonathan Corbet, Alessandro Rubini
- *Linux Kernel Development* (3rd Edition) — Robert Love
- *Real-Time Linux App Development* — John Ogness (OSADL)

**Standards:**
- DO-178C § 11.13 (Partitioning)
- ED-203A § 3.2 (OS Security Requirements)

**Online:**
- https://kernel.org (official docs)
- https://yoctoproject.org/docs (Yocto mega-manual)
- https://wiki.linuxfoundation.org/realtime/start (PREEMPT_RT)

**Courses:**
- Linux Foundation: LFD450 (Embedded Linux Development)
- Wind River University: WR-LINUX-101

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand PREEMPT_RT vs. stock kernel tradeoffs
- [ ] Write a basic character device driver (CAN/ARINC 429)
- [ ] Configure SELinux policy for an aircraft application
- [ ] Build a custom Yocto image with avionics drivers
- [ ] Debug a kernel panic with kdump/KGDB
- [ ] Set up network namespaces for domain segregation
- [ ] Measure worst-case latency with cyclictest

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ COMPLETE  
**Created:** January 14, 2026  
**For:** Aircraft Services Architect Role (Portland, PAC)  
**Next:** Review [Cloud_Native_Cheatsheet.rst](Cloud_Native_Cheatsheet.rst)
