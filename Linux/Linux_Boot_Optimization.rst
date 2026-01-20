================================================================================
Linux Boot Optimization for Embedded Systems
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Embedded Linux System Design and Development (2006), Appendix A
:Focus: Fast boot, kernel optimization, initialization reduction

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. Boot Time Overview
================================================================================

1.1 Boot Stages
--------------------------------------------------------------------------------

**Three Main Stages:**

::

   Power-On
       ↓
   +--------------------------+  ← STAGE 1: Bootloader
   | Bootloader               |    (U-Boot, GRUB, etc.)
   | - POST                   |    Time: 500ms - 2s
   | - Locate kernel          |
   | - Decompress kernel      |
   | - Copy to RAM            |
   | - Jump to kernel         |
   +--------------------------+
       ↓
   +--------------------------+  ← STAGE 2: Kernel Turn-On
   | Kernel Initialization    |    Time: 1s - 5s
   | - Hardware init          |
   | - Driver init            |
   | - Mount root FS          |
   | - Transfer to user space |
   +--------------------------+
       ↓
   +--------------------------+  ← STAGE 3: User Space Init
   | User Space Startup       |    Time: 2s - 10s
   | - Load modules           |
   | - Start services         |
   | - Launch applications    |
   +--------------------------+
       ↓
   System Ready (Turn-On State)

**Time-Consuming Activities:**

+----------------------+-------------------------+-------------------------+
| Stage                | Activity                | Typical Time            |
+======================+=========================+=========================+
| **Bootloader**       | POST                    | 200-500ms               |
|                      | Kernel location         | 100-200ms               |
|                      | Kernel decompression    | 500ms-1s                |
|                      | Copy to RAM             | 300-800ms               |
+----------------------+-------------------------+-------------------------+
| **Kernel**           | calibrate_delay()       | 200-500ms               |
|                      | Driver initialization   | 500ms-2s                |
|                      | File system mount       | 500ms-3s (JFFS2)        |
+----------------------+-------------------------+-------------------------+
| **User Space**       | Module loading          | 1-3s                    |
|                      | Service startup         | 2-5s                    |
|                      | Application launch      | 1-3s                    |
+----------------------+-------------------------+-------------------------+

1.2 Turn-On State Definition
--------------------------------------------------------------------------------

**System-Dependent "Ready" State:**

**Example 1: Embedded Router**

- All network interfaces configured
- Routing protocols started
- Routing tables populated
- Ready to forward packets

**Example 2: Handheld Device**

- Display initialized
- Touch screen functional
- UI rendered
- User can interact

**Example 3: Industrial Controller**

- Real-time control loop running
- Sensors reading
- Actuators controllable
- Safety systems active

================================================================================
2. Bootloader Optimization
================================================================================

2.1 POST (Power-On Self Test)
--------------------------------------------------------------------------------

**Skip POST on Warm Boot:**

.. code-block:: c

   /* U-Boot modification */
   
   #define WARM_BOOT_FLAG_ADDR  0x80000000
   #define WARM_BOOT_MAGIC      0xDEADBEEF
   
   void board_init(void)
   {
       volatile uint32_t *warm_boot = (uint32_t *)WARM_BOOT_FLAG_ADDR;
       
       if (*warm_boot == WARM_BOOT_MAGIC) {
           /* Warm boot: skip POST */
           printf("Warm boot detected, skipping POST\n");
           goto skip_post;
       }
       
       /* Cold boot: perform POST */
       printf("Cold boot, running POST...\n");
       run_memory_test();
       run_flash_test();
       run_peripheral_test();
       
       /* Set warm boot flag */
       *warm_boot = WARM_BOOT_MAGIC;
       
   skip_post:
       /* Continue with initialization */
   }

**Savings:** 200-500ms

2.2 Kernel Loading Optimization
--------------------------------------------------------------------------------

**Option 1: Store Kernel in Raw Partition (Not in Filesystem)**

**Before (kernel in file system):**

::

   Time Breakdown:
   - Parse file system: 150ms
   - Locate kernel file: 100ms
   - Read ELF headers: 50ms
   - Load kernel: 500ms
   Total: 800ms

**After (raw partition):**

::

   Time Breakdown:
   - Read from fixed offset: 500ms
   Total: 500ms
   
   Savings: 300ms

**U-Boot command:**

.. code-block:: bash

   # Flash kernel to raw partition
   tftp 0x82000000 zImage
   nand erase 0x100000 0x500000
   nand write 0x82000000 0x100000 ${filesize}
   
   # Boot from raw partition
   setenv bootcmd 'nand read 0x82000000 0x100000 0x500000; bootm 0x82000000'
   saveenv
   reset

**Option 2: Store Uncompressed Kernel**

**Trade-off:**

- **Faster boot:** No decompression (save 500ms)
- **More flash:** 2-3x larger image

**When to use:**

- Flash is cheap/plentiful
- Boot time critical
- Image < 4MB

**Option 3: XIP (Execute In Place)**

**Kernel executes directly from flash (no copy to RAM):**

.. code-block:: bash

   # Kernel configuration
   CONFIG_XIP_KERNEL=y
   CONFIG_XIP_PHYS_ADDR=0x00100000

**Advantages:**

- **Faster boot:** No copy time (save 300-800ms)
- **Less RAM used:** Text section stays in flash
- **More RAM for applications**

**Disadvantages:**

- **Slower execution:** Flash slower than RAM (70ns vs 10ns)
- **Larger flash needed:** Can't compress XIP image
- **Flash driver complexity:** Can't erase/write while executing from flash

**Flash Driver Modifications for XIP:**

.. code-block:: c

   /* Copy flash write routine to RAM */
   
   static int (*flash_write_ram)(void *dst, void *src, size_t len);
   
   int flash_driver_init(void)
   {
       /* Allocate RAM for write function */
       flash_write_ram = kmalloc(1024, GFP_KERNEL);
       
       /* Copy flash_write_internal to RAM */
       memcpy(flash_write_ram, flash_write_internal, 1024);
       
       /* Flush caches */
       flush_icache_range((unsigned long)flash_write_ram,
                         (unsigned long)flash_write_ram + 1024);
       
       return 0;
   }
   
   int flash_write(loff_t offset, const void *buf, size_t len)
   {
       unsigned long flags;
       int ret;
       
       /* Disable interrupts (critical!) */
       local_irq_save(flags);
       
       /* Call RAM-resident write function */
       ret = flash_write_ram(flash_base + offset, buf, len);
       
       local_irq_restore(flags);
       
       return ret;
   }

**XIP with Read-Only Root FS (CRAMFS):**

- Flash write not needed after boot
- Simplifies implementation
- Recommended approach

**Option 4: Use DMA for Kernel Copy**

.. code-block:: c

   /* U-Boot: Use DMA to copy kernel from flash to RAM */
   
   void copy_kernel_with_dma(void *src, void *dst, size_t len)
   {
       /* Configure DMA controller */
       DMA_SRC_ADDR = (uint32_t)src;
       DMA_DST_ADDR = (uint32_t)dst;
       DMA_BYTE_COUNT = len;
       DMA_CTRL = DMA_EN | DMA_MEM_TO_MEM | DMA_BURST_16;
       
       /* Start DMA */
       DMA_START = 1;
       
       /* Wait for completion */
       while (DMA_BUSY);
       
       /* Verify */
       flush_cache((uint32_t)dst, len);
   }

**Savings:** 100-300ms (vs memcpy)

2.3 Bootloader Configuration
--------------------------------------------------------------------------------

**Disable Interactive Boot Menu:**

.. code-block:: bash

   # U-Boot: Set bootdelay to 0
   setenv bootdelay 0
   saveenv

**Savings:** 1-3s

**Silent Boot:**

.. code-block:: bash

   setenv silent 1
   setenv bootargs "console=ttyS0,115200 quiet"

**Savings:** 50-200ms (reduce serial prints)

**Direct Boot (Skip Menu):**

.. code-block:: bash

   # U-Boot: autoboot immediately
   setenv bootcmd 'nand read 0x82000000 0x100000 0x500000; bootm 0x82000000'
   setenv bootargs 'console=ttyS0,115200 root=/dev/mtdblock2 ro quiet'
   setenv bootdelay 0
   saveenv

================================================================================
3. Kernel Optimization
================================================================================

3.1 Disable Kernel Prints
--------------------------------------------------------------------------------

**Kernel Command Line:**

.. code-block:: bash

   # Disable all kernel messages to console
   quiet
   
   # Or set log level to errors only
   loglevel=3
   
   # Complete example
   console=ttyS0,115200 root=/dev/mmcblk0p2 quiet

**View messages later:**

.. code-block:: bash

   dmesg | less

**Savings:** 500ms - 2s (depending on console speed)

**Conditional Early Printk:**

.. code-block:: c

   /* Only enable early printk for debugging builds */
   
   #ifdef DEBUG_BOOT
   #define early_printk printk
   #else
   #define early_printk(...)
   #endif

3.2 Hard-Code loops_per_jiffy
--------------------------------------------------------------------------------

**Problem:** ``calibrate_delay()`` takes 200-500ms during boot

.. code-block:: c

   /* init/calibrate.c */
   
   void calibrate_delay(void)
   {
       unsigned long lpj;
       int this_cpu = smp_processor_id();
       
       /* This loop takes 200-500ms! */
       lpj = calibrate_delay_converge();
       
       per_cpu(cpu_data, this_cpu).loops_per_jiffy = lpj;
       pr_info("Calibrating delay loop... %lu.%02lu BogoMIPS\n",
               lpj/(500000/HZ), (lpj/(5000/HZ)) % 100);
   }

**Solution 1: Hard-code value in kernel:**

.. code-block:: c

   /* arch/arm/kernel/setup.c */
   
   void __init setup_arch(char **cmdline_p)
   {
       #ifdef CONFIG_HARDCODE_LOOPS_PER_JIFFY
       /* Skip calibration for known CPU */
       loops_per_jiffy = 500000;  /* Measured value */
       pr_info("Using preset loops_per_jiffy: %lu\n", loops_per_jiffy);
       #else
       calibrate_delay();
       #endif
       /* ... */
   }

**Solution 2: Pass via kernel command line:**

.. code-block:: bash

   # Add to bootargs
   lpj=500000
   
   # Complete example
   console=ttyS0,115200 root=/dev/mmcblk0p2 lpj=500000 quiet

**How to determine correct value:**

.. code-block:: bash

   # Boot once with calibration, check dmesg
   dmesg | grep BogoMIPS
   # Output: Calibrating delay loop... 996.14 BogoMIPS (lpj=4980736)
   
   # Use lpj=4980736 in future boots

**Savings:** 200-500ms

3.3 Optimize Driver Initialization
--------------------------------------------------------------------------------

**Defer Non-Essential Drivers:**

.. code-block:: c

   /* Mark driver as late_initcall instead of module_init */
   
   static int __init mydriver_init(void)
   {
       /* Driver initialization */
       return platform_driver_register(&mydriver);
   }
   
   /* Before: runs early */
   module_init(mydriver_init);
   
   /* After: runs late (after critical drivers) */
   late_initcall(mydriver_init);

**Initcall Order:**

::

   early_initcall    ← Very early (arch-specific)
   pure_initcall     ← Early
   core_initcall     ← Core kernel
   postcore_initcall ← After core
   arch_initcall     ← Architecture
   subsys_initcall   ← Subsystems
   fs_initcall       ← File systems
   device_initcall   ← Devices (default for module_init)
   late_initcall     ← Late drivers

**Remove Unnecessary Delays:**

.. code-block:: c

   /* Bad: arbitrary delays */
   static int mydriver_probe(struct platform_device *pdev)
   {
       /* Reset device */
       writel(RESET, base + CTRL_REG);
       mdelay(100);  /* ← Remove if unnecessary! */
       
       /* Configure device */
       writel(CONFIG, base + CFG_REG);
       mdelay(50);   /* ← Remove if unnecessary! */
       
       return 0;
   }
   
   /* Good: check status instead */
   static int mydriver_probe(struct platform_device *pdev)
   {
       /* Reset device */
       writel(RESET, base + CTRL_REG);
       
       /* Wait for reset complete (with timeout) */
       int timeout = 10000;
       while ((readl(base + STATUS_REG) & RESET_DONE) == 0) {
           if (--timeout == 0)
               return -ETIMEDOUT;
           udelay(10);
       }
       
       return 0;
   }

**Preset Known Hardware:**

.. code-block:: c

   /* Avoid probing when hardware is known */
   
   /* Bad: probe PCI bus (can take 100-500ms) */
   static int find_ethernet_device(void)
   {
       return pci_find_device(VENDOR_ID, DEVICE_ID, NULL);
   }
   
   /* Good: use fixed address if known */
   static int __init board_init(void)
   {
       /* Pre-configure known PCI devices */
       eth_dev.vendor = VENDOR_ID;
       eth_dev.device = DEVICE_ID;
       eth_dev.bus = 0;
       eth_dev.devfn = PCI_DEVFN(1, 0);  /* Bus 0, Dev 1, Func 0 */
       
       platform_device_register(&eth_dev);
       return 0;
   }

**Savings:** 100ms - 1s

3.4 Root File System Selection
--------------------------------------------------------------------------------

**File System Boot Times:**

+-------------------+---------------------------+---------------------------+
| File System       | Mount Time                | Use Case                  |
+===================+===========================+===========================+
| **CRAMFS**        | 50-200ms                  | Read-only root, fast boot |
+-------------------+---------------------------+---------------------------+
| **ROMFS**         | 30-100ms                  | Very small, fast boot     |
+-------------------+---------------------------+---------------------------+
| **JFFS2**         | 2-10s (!)                 | Read-write, slow mount    |
|                   | (scans entire flash)      | (scans journal)           |
+-------------------+---------------------------+---------------------------+
| **UBIFS**         | 500ms-2s                  | Read-write, better than   |
|                   |                           | JFFS2 for large NAND      |
+-------------------+---------------------------+---------------------------+
| **ext2**          | 100-300ms                 | RAM disk, SD card         |
+-------------------+---------------------------+---------------------------+
| **ext4**          | 200-500ms                 | SD card, eMMC             |
+-------------------+---------------------------+---------------------------+

**Recommendation for Fast Boot:**

1. **Use CRAMFS for root filesystem** (read-only, fast)
2. **Mount JFFS2/UBIFS data partition later** (after boot)

**Split Root FS:**

.. code-block:: bash

   # Fast boot: use CRAMFS for root
   root=/dev/mtdblock2 rootfstype=cramfs ro
   
   # Mount writable data partition later in init script
   mount -t jffs2 /dev/mtdblock3 /data

**Create CRAMFS:**

.. code-block:: bash

   mkcramfs /path/to/rootfs rootfs.cramfs
   
   # Flash to device
   flashcp rootfs.cramfs /dev/mtd2

**Savings:** 1-8s (vs JFFS2)

3.5 Minimize Kernel Size
--------------------------------------------------------------------------------

**Remove Unnecessary Features:**

.. code-block:: bash

   # Kernel config
   make menuconfig
   
   # Disable:
   CONFIG_DEBUG_KERNEL=n
   CONFIG_PROFILING=n
   CONFIG_FTRACE=n
   CONFIG_KGDB=n
   CONFIG_SWAP=n           # If no swap
   CONFIG_SYSFS_DEPRECATED=n
   CONFIG_IPV6=n           # If not needed
   CONFIG_WIRELESS=n       # If not needed
   
   # Enable:
   CONFIG_KERNEL_LZMA=y    # Better compression
   CONFIG_CC_OPTIMIZE_FOR_SIZE=y

**Module vs Built-in:**

- **Built-in:** Slightly faster boot (no module loading)
- **Modules:** Smaller kernel image, faster decompression

**Recommendation:** Built-in for critical drivers, modules for others

**Savings:** 100-500ms (smaller kernel = faster decompression)

================================================================================
4. User Space Optimization
================================================================================

4.1 Reduce Module Loading Time
--------------------------------------------------------------------------------

**Combine Multiple Modules:**

.. code-block:: bash

   # Before: Load 10 separate modules (10 x 100ms = 1s)
   modprobe module1
   modprobe module2
   ...
   modprobe module10
   
   # After: Build single combined module (1 x 150ms = 150ms)
   # Savings: 850ms

**Use Built-In Modules:**

.. code-block:: bash

   # Kernel config: make critical modules built-in
   CONFIG_USB_STORAGE=y          # Instead of =m
   CONFIG_MMC=y
   CONFIG_MMC_BLOCK=y

4.2 Parallel Service Startup
--------------------------------------------------------------------------------

**Traditional Init (Sequential):**

.. code-block:: bash

   #!/bin/sh
   # /etc/init.d/rcS
   
   /etc/init.d/S10udev start       # 500ms
   /etc/init.d/S20networking start # 1000ms
   /etc/init.d/S30dropbear start   # 300ms
   /etc/init.d/S40lighttpd start   # 400ms
   
   # Total: 2200ms

**Parallel Startup:**

.. code-block:: bash

   #!/bin/sh
   # /etc/init.d/rcS
   
   # Start independent services in parallel
   /etc/init.d/S10udev start &
   /etc/init.d/S20networking start &
   /etc/init.d/S30dropbear start &
   /etc/init.d/S40lighttpd start &
   
   # Wait for critical services
   wait
   
   # Total: ~1000ms (longest service)
   # Savings: 1200ms

**Handle Dependencies:**

.. code-block:: bash

   #!/bin/sh
   
   # Start udev first (others may depend on it)
   /etc/init.d/S10udev start
   
   # Start independent services in parallel
   /etc/init.d/S20networking start &
   NET_PID=$!
   
   /etc/init.d/S30syslog start &
   LOG_PID=$!
   
   # Dropbear needs network
   wait $NET_PID
   /etc/init.d/S40dropbear start &
   
   # Web server needs network and logging
   wait $LOG_PID
   /etc/init.d/S50lighttpd start &
   
   wait

**Using systemd (Modern Approach):**

.. code-block:: ini

   # /etc/systemd/system/myservice.service
   
   [Unit]
   Description=My Service
   After=network.target
   
   [Service]
   Type=simple
   ExecStart=/usr/bin/myservice
   
   [Install]
   WantedBy=multi-user.target

4.3 Minimize User Space Programs
--------------------------------------------------------------------------------

**Use BusyBox:**

- Single binary for common utilities
- Smaller footprint
- Faster loading

**Static Linking for Critical Apps:**

.. code-block:: bash

   # Dynamic linking: load multiple shared libraries
   $ ldd /bin/myapp
   linux-gate.so.1
   libc.so.6
   libm.so.6
   libpthread.so.0
   
   # Static linking: single binary, faster startup
   gcc -static -o myapp myapp.c

**Trade-off:** Larger binary, but faster startup (no library loading)

4.4 Defer Non-Critical Services
--------------------------------------------------------------------------------

**Start Only Essential Services:**

.. code-block:: bash

   #!/bin/sh
   # /etc/init.d/rcS
   
   # Critical services only
   /etc/init.d/S10udev start
   /etc/init.d/S20networking start
   /etc/init.d/S30myapp start  # Main application
   
   # Mark system as ready
   touch /tmp/system_ready
   
   # Start non-critical services in background
   (
       sleep 5
       /etc/init.d/S40dropbear start
       /etc/init.d/S50lighttpd start
       /etc/init.d/S60nfs start
   ) &

================================================================================
5. Measuring Boot Time
================================================================================

5.1 Instrumented printk
--------------------------------------------------------------------------------

**Enable Timestamp Printing:**

.. code-block:: bash

   # Kernel config
   CONFIG_PRINTK_TIME=y
   
   # Or via kernel command line
   printk.time=1

**Sample Output:**

.. code-block:: text

   [    0.000000] Linux version 5.10.0
   [    0.123456] CPU: ARMv7 Processor
   [    0.234567] Memory: 256MB
   [    0.456789] Mount root filesystem
   [    2.123456] JFFS2: scanning completed  ← 2s spent here!
   [    2.234567] VFS: Mounted root
   [    3.456789] Freeing unused kernel memory
   [    4.123456] Starting init

**Analyze:**

.. code-block:: bash

   dmesg | grep -E "^\[.*\]" | awk '{print $1}' | sed 's/\[//;s/\]//' | \
   awk 'NR>1 {print $1-prev, prev_line} {prev=$1; prev_line=$0}' | \
   sort -rn | head -20

5.2 Bootchart
--------------------------------------------------------------------------------

.. code-block:: bash

   # Install bootchart
   sudo apt-get install bootchart
   
   # Enable in kernel
   init=/sbin/bootchartd
   
   # Or in init script
   /sbin/bootchartd start
   
   # Generate chart
   bootchart /var/log/bootchart.tgz

5.3 Custom Timing Points
--------------------------------------------------------------------------------

.. code-block:: c

   /* Add timing instrumentation */
   
   #include <linux/ktime.h>
   
   static ktime_t boot_start;
   
   void __init time_init(void)
   {
       boot_start = ktime_get();
       printk("[BOOT] Kernel start\n");
   }
   
   void __init measure_point(const char *msg)
   {
       ktime_t now = ktime_get();
       s64 delta_ms = ktime_to_ms(ktime_sub(now, boot_start));
       
       printk("[BOOT] %5lld ms: %s\n", delta_ms, msg);
   }
   
   /* Use throughout boot process */
   measure_point("After driver init");
   measure_point("Before mount root");
   measure_point("After mount root");

================================================================================
6. Summary of Optimizations
================================================================================

**Quick Wins (Easy to Implement):**

+----------------------------------+------------------+----------------------+
| Optimization                     | Savings          | Difficulty           |
+==================================+==================+======================+
| Disable boot delay               | 1-3s             | Easy                 |
| Add quiet to bootargs            | 500ms-2s         | Easy                 |
| Hard-code lpj                    | 200-500ms        | Easy                 |
| Use CRAMFS instead of JFFS2      | 1-8s             | Easy                 |
| Parallel service startup         | 500ms-2s         | Medium               |
+----------------------------------+------------------+----------------------+

**Advanced Optimizations:**

+----------------------------------+------------------+----------------------+
| Optimization                     | Savings          | Difficulty           |
+==================================+==================+======================+
| XIP kernel                       | 300-800ms        | Hard                 |
| Skip POST on warm boot           | 200-500ms        | Medium               |
| Optimize driver init             | 100ms-1s         | Medium-Hard          |
| DMA kernel copy                  | 100-300ms        | Medium               |
| Custom init system               | 1-3s             | Hard                 |
+----------------------------------+------------------+----------------------+

**Typical Boot Time Reduction:**

::

   Before Optimization: 15-30 seconds
   After Basic Optimization: 8-12 seconds
   After Advanced Optimization: 3-6 seconds
   With Splash Screen (perceived): 1-2 seconds

================================================================================
End of Linux Boot Optimization Cheatsheet
================================================================================
