================================================================================
Linux Board Support Package (BSP) Development
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Embedded Linux System Design and Development (2006)
:Focus: Board-specific porting, HAL, memory maps, interrupt handling

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. BSP Overview
================================================================================

1.1 What is a BSP?
--------------------------------------------------------------------------------

A **Board Support Package (BSP)** is the layer of software that contains
board-specific and processor-specific code to initialize hardware and provide
a Hardware Abstraction Layer (HAL) for the operating system.

**BSP Components:**

- Bootloader support
- Hardware initialization (CPU, memory, peripherals)
- Interrupt controller setup
- Timer configuration
- Memory map definitions
- Device tree or platform data
- Board-specific drivers

**Linux BSP vs RTOS BSP:**

+---------------------------+---------------------------+
| RTOS BSP                  | Linux BSP                 |
+===========================+===========================+
| Standard HAL APIs         | Platform-specific HAL     |
+---------------------------+---------------------------+
| Vendor-provided           | Community/vendor mix      |
+---------------------------+---------------------------+
| Minimal configuration     | Extensive configuration   |
+---------------------------+---------------------------+
| Fixed structure           | Flexible architecture     |
+---------------------------+---------------------------+

1.2 Linux BSP Architecture
--------------------------------------------------------------------------------

::

   Kernel Source Tree
   ├── arch/
   │   ├── arm/
   │   │   ├── boot/
   │   │   │   └── dts/          # Device trees
   │   │   ├── configs/          # Board configs
   │   │   ├── kernel/
   │   │   │   ├── head.S        # Early boot
   │   │   │   └── setup.c       # setup_arch()
   │   │   └── mach-<board>/     # Board-specific
   │   │       ├── board-init.c
   │   │       └── <board>.c
   │   ├── mips/
   │   ├── powerpc/
   │   └── x86/
   ├── drivers/               # Device drivers
   └── include/
       └── asm-<arch>/       # Architecture headers

**Supported Architectures:**

- ARM (32-bit and 64-bit)
- MIPS
- PowerPC
- x86/x86_64
- RISC-V
- M68K, SuperH, CRIS, V850

================================================================================
2. BSP Initialization Flow
================================================================================

2.1 Boot Sequence
--------------------------------------------------------------------------------

::

   Power-On Reset
        ↓
   [Bootloader] (U-Boot, GRUB, etc.)
        ↓ Load kernel image
        ↓ Setup initial page tables (optional)
        ↓ Pass boot parameters
        ↓ Jump to kernel entry point
        ↓
   [Kernel Entry] (arch/<arch>/kernel/head.S)
        ↓ MMU setup (if needed)
        ↓ Cache initialization
        ↓ Zero BSS section
        ↓ Setup stack
        ↓ Jump to C code
        ↓
   [start_kernel()] (init/main.c)
        ↓ setup_arch()           ← BSP-specific
        ↓ setup_per_cpu_areas()
        ↓ setup_command_line()
        ↓ parse_early_param()
        ↓ setup_memory()
        ↓ paging_init()
        ↓ init_IRQ()             ← BSP-specific
        ↓ time_init()            ← BSP-specific
        ↓ console_init()
        ↓ rest_init()
        ↓
   [kernel_init()] → /sbin/init

2.2 Early Boot - head.S
--------------------------------------------------------------------------------

**Location:** ``arch/<architecture>/kernel/head.S``

**Responsibilities:**

1. Enable MMU (if disabled by bootloader)
2. Initialize caches
3. Clear BSS section
4. Setup initial stack
5. Jump to ``start_kernel()``

**Example ARM head.S (simplified):**

.. code-block:: asm

   /* arch/arm/kernel/head.S */
   
   .section ".head.text","ax"
   ENTRY(stext)
       /* Disable interrupts */
       cpsid   if
       
       /* Get CPU ID */
       mrc     p15, 0, r9, c0, c0
       
       /* Setup initial page tables */
       bl      __create_page_tables
       
       /* Enable MMU */
       mrc     p15, 0, r0, c1, c0, 0
       orr     r0, r0, #CR_M     /* Enable MMU */
       mcr     p15, 0, r0, c1, c0, 0
       
       /* Clear BSS */
       ldr     r4, =__bss_start
       ldr     r5, =__bss_end
       mov     r6, #0
   1:  cmp     r4, r5
       strcc   r6, [r4], #4
       bcc     1b
       
       /* Setup stack */
       ldr     sp, =init_thread_union + THREAD_START_SP
       
       /* Jump to C code */
       b       start_kernel
   ENDPROC(stext)

**Example MIPS kernel_entry (simplified):**

.. code-block:: asm

   /* arch/mips/kernel/head.S */
   
   NESTED(kernel_entry, 16, sp)
       /* Setup CP0 status register */
       mfc0    t0, CP0_STATUS
       or      t0, ST0_CU0|ST0_BEV
       mtc0    t0, CP0_STATUS
       
       /* Initialize cache */
       jal     cache_init
       
       /* Clear BSS */
       la      t0, __bss_start
       la      t1, __bss_stop
   1:  sw      zero, 0(t0)
       addiu   t0, t0, 4
       bne     t0, t1, 1b
       
       /* Setup stack */
       la      sp, init_thread_union + THREAD_SIZE - 32
       
       /* Jump to start_kernel */
       j       start_kernel
   END(kernel_entry)

2.3 setup_arch() - Platform Initialization
--------------------------------------------------------------------------------

**Location:** ``arch/<architecture>/kernel/setup.c``

**Prototype:**

.. code-block:: c

   void __init setup_arch(char **cmdline_p);

**Responsibilities:**

1. CPU recognition and fixups
2. Board recognition
3. Parse kernel command line
4. Setup memory regions
5. Initialize console
6. Setup I/O mapping
7. Register platform devices

**Example ARM setup_arch():**

.. code-block:: c

   /* arch/arm/kernel/setup.c */
   
   void __init setup_arch(char **cmdline_p)
   {
       const struct machine_desc *mdesc;
       
       /* Detect CPU type */
       setup_processor();
       
       /* Get machine descriptor (board-specific) */
       mdesc = setup_machine_fdt(__atags_pointer);
       if (!mdesc)
           mdesc = setup_machine_tags(__atags_pointer);
       
       machine_desc = mdesc;
       machine_name = mdesc->name;
       
       /* Parse command line */
       parse_early_param();
       
       /* Setup memory banks */
       arm_memblock_init(mdesc);
       
       /* Initialize paging */
       paging_init(mdesc);
       
       /* Request standard resources */
       request_standard_resources(mdesc);
       
       /* Unflatten device tree */
       if (mdesc->dt_compat)
           unflatten_device_tree();
       
       /* Platform-specific initialization */
       if (mdesc->init_early)
           mdesc->init_early();
       
       /* Setup console */
       conswitchp = &dummy_con;
       early_console_setup();
   }

**Board-Specific Machine Descriptor:**

.. code-block:: c

   /* arch/arm/mach-<vendor>/board-<name>.c */
   
   static void __init myboard_init(void)
   {
       /* Register platform devices */
       platform_device_register(&myboard_uart_device);
       platform_device_register(&myboard_eth_device);
       
       /* Initialize GPIOs */
       gpio_request(GPIO_LED, "status-led");
       gpio_direction_output(GPIO_LED, 0);
   }
   
   static void __init myboard_init_early(void)
   {
       /* Early hardware initialization */
       myboard_clock_init();
   }
   
   static void __init myboard_init_irq(void)
   {
       /* Initialize interrupt controller */
       gic_init(0, 29, gic_dist_base, gic_cpu_base);
   }
   
   static const char *myboard_dt_compat[] __initconst = {
       "vendor,myboard",
       NULL,
   };
   
   DT_MACHINE_START(MYBOARD, "My Custom Board")
       .dt_compat  = myboard_dt_compat,
       .init_early = myboard_init_early,
       .init_irq   = myboard_init_irq,
       .init_machine = myboard_init,
       .restart    = myboard_restart,
   MACHINE_END

================================================================================
3. Memory Map Configuration
================================================================================

3.1 Physical vs Virtual Memory
--------------------------------------------------------------------------------

**Memory Regions:**

.. code-block:: c

   /* Typical ARM memory layout */
   
   #define PHYS_RAM_START    0x80000000  /* Physical RAM base */
   #define PHYS_RAM_SIZE     0x10000000  /* 256MB */
   
   #define IO_BASE           0x40000000  /* Peripheral base */
   #define IO_SIZE           0x10000000  /* 256MB */
   
   /* Virtual addresses (after MMU enabled) */
   #define PAGE_OFFSET       0xC0000000  /* Kernel virtual base */
   #define VMALLOC_START     0xE0000000
   #define VMALLOC_END       0xFF000000

**Memory Map Structure:**

.. code-block:: c

   struct meminfo {
       int nr_banks;
       struct membank {
           phys_addr_t start;
           phys_addr_t size;
           unsigned int highmem;
       } bank[NR_BANKS];
   };
   
   /* Define memory banks */
   void __init myboard_fixup(struct tag *tags, char **cmdline)
   {
       /* Override ATAGS memory information if needed */
       tags->u.mem.start = PHYS_RAM_START;
       tags->u.mem.size  = PHYS_RAM_SIZE;
   }

3.2 I/O Memory Mapping
--------------------------------------------------------------------------------

**Static I/O Mapping:**

.. code-block:: c

   /* arch/arm/mach-<vendor>/include/mach/io.h */
   
   #define IO_PHYS_BASE      0x40000000
   #define IO_VIRT_BASE      0xF4000000
   #define IO_SIZE           0x01000000
   
   /* Map table for static mappings */
   static struct map_desc myboard_io_desc[] __initdata = {
       {
           .virtual    = IO_VIRT_BASE,
           .pfn        = __phys_to_pfn(IO_PHYS_BASE),
           .length     = IO_SIZE,
           .type       = MT_DEVICE,
       },
   };
   
   void __init myboard_map_io(void)
   {
       iotable_init(myboard_io_desc, ARRAY_SIZE(myboard_io_desc));
   }

**Dynamic I/O Mapping:**

.. code-block:: c

   #include <linux/io.h>
   
   /* Map peripheral registers */
   void __iomem *uart_base;
   
   uart_base = ioremap(UART_PHYS_BASE, UART_SIZE);
   if (!uart_base) {
       pr_err("Failed to map UART registers\n");
       return -ENOMEM;
   }
   
   /* Access registers */
   writel(value, uart_base + UART_TX_REG);
   
   /* Unmap when done */
   iounmap(uart_base);

3.3 Memory Barriers and Access
--------------------------------------------------------------------------------

.. code-block:: c

   /* Read/write I/O registers with barriers */
   
   /* Write with barrier */
   writel(value, addr);    /* Includes wmb() */
   writew(value, addr);
   writeb(value, addr);
   
   /* Read with barrier */
   value = readl(addr);    /* Includes rmb() */
   value = readw(addr);
   value = readb(addr);
   
   /* Relaxed versions (no barriers) */
   writel_relaxed(value, addr);
   readl_relaxed(addr);
   
   /* Explicit barriers */
   mb();    /* Memory barrier */
   rmb();   /* Read memory barrier */
   wmb();   /* Write memory barrier */
   smp_mb(); /* SMP memory barrier */

================================================================================
4. Interrupt Management
================================================================================

4.1 Interrupt Controller Setup
--------------------------------------------------------------------------------

**init_IRQ() Implementation:**

.. code-block:: c

   /* arch/arm/kernel/irq.c */
   
   void __init init_IRQ(void)
   {
       /* Call machine-specific IRQ initialization */
       if (machine_desc->init_irq)
           machine_desc->init_irq();
       else
           irqchip_init();
   }

**GIC (Generic Interrupt Controller) Setup:**

.. code-block:: c

   /* Board-specific GIC initialization */
   
   #define GIC_DIST_BASE  0x48241000
   #define GIC_CPU_BASE   0x48242000
   
   void __init myboard_init_irq(void)
   {
       void __iomem *gic_dist_base;
       void __iomem *gic_cpu_base;
       
       /* Map GIC registers */
       gic_dist_base = ioremap(GIC_DIST_BASE, SZ_4K);
       gic_cpu_base  = ioremap(GIC_CPU_BASE, SZ_4K);
       
       /* Initialize GIC */
       gic_init(0, 29, gic_dist_base, gic_cpu_base);
       
       /* Additional interrupt sources */
       myboard_init_additional_irqs();
   }

**Custom Interrupt Controller:**

.. code-block:: c

   #define IRQ_BASE       32
   #define NR_IRQS        64
   
   static void myboard_mask_irq(struct irq_data *d)
   {
       unsigned int irq = d->irq - IRQ_BASE;
       u32 mask;
       
       mask = readl(IRQ_MASK_REG);
       mask &= ~(1 << irq);
       writel(mask, IRQ_MASK_REG);
   }
   
   static void myboard_unmask_irq(struct irq_data *d)
   {
       unsigned int irq = d->irq - IRQ_BASE;
       u32 mask;
       
       mask = readl(IRQ_MASK_REG);
       mask |= (1 << irq);
       writel(mask, IRQ_MASK_REG);
   }
   
   static void myboard_ack_irq(struct irq_data *d)
   {
       unsigned int irq = d->irq - IRQ_BASE;
       writel(1 << irq, IRQ_CLEAR_REG);
   }
   
   static struct irq_chip myboard_irq_chip = {
       .name       = "MYBOARD-IRQ",
       .irq_ack    = myboard_ack_irq,
       .irq_mask   = myboard_mask_irq,
       .irq_unmask = myboard_unmask_irq,
   };
   
   void __init myboard_init_irq_controller(void)
   {
       int i;
       
       /* Disable all interrupts */
       writel(0, IRQ_MASK_REG);
       writel(0xFFFFFFFF, IRQ_CLEAR_REG);
       
       /* Setup IRQ descriptors */
       for (i = 0; i < NR_IRQS; i++) {
           irq_set_chip_and_handler(IRQ_BASE + i,
                                   &myboard_irq_chip,
                                   handle_level_irq);
           irq_clear_status_flags(IRQ_BASE + i, IRQ_NOREQUEST);
       }
   }

4.2 IRQ Handling Flow
--------------------------------------------------------------------------------

.. code-block:: c

   /* Top-level IRQ handler */
   asmlinkage void __exception_irq_entry myboard_handle_irq(struct pt_regs *regs)
   {
       u32 irqstat, irqnr;
       
       do {
           /* Read interrupt status */
           irqstat = readl(IRQ_STATUS_REG);
           
           if (irqstat) {
               /* Find first set bit */
               irqnr = __ffs(irqstat);
               irqnr += IRQ_BASE;
               
               /* Handle IRQ */
               handle_IRQ(irqnr, regs);
           }
       } while (irqstat);
   }

================================================================================
5. Timer Configuration
================================================================================

5.1 System Timer Setup
--------------------------------------------------------------------------------

.. code-block:: c

   /* arch/arm/mach-<vendor>/timer.c */
   
   #define TIMER_BASE      0x48040000
   #define TIMER_LOAD      (TIMER_BASE + 0x00)
   #define TIMER_VALUE     (TIMER_BASE + 0x04)
   #define TIMER_CTRL      (TIMER_BASE + 0x08)
   #define TIMER_INTCLR    (TIMER_BASE + 0x0C)
   
   static void __iomem *timer_base;
   
   static irqreturn_t myboard_timer_interrupt(int irq, void *dev_id)
   {
       /* Clear interrupt */
       writel(1, timer_base + TIMER_INTCLR);
       
       /* Update jiffies and call timer handlers */
       timer_tick();
       
       return IRQ_HANDLED;
   }
   
   static struct irqaction myboard_timer_irq = {
       .name    = "myboard-timer",
       .flags   = IRQF_TIMER | IRQF_IRQPOLL,
       .handler = myboard_timer_interrupt,
   };
   
   void __init myboard_timer_init(void)
   {
       u32 ctrl;
       
       timer_base = ioremap(TIMER_BASE, SZ_4K);
       
       /* Setup timer for 100Hz (HZ) */
       writel(CLOCK_FREQ / HZ, timer_base + TIMER_LOAD);
       
       /* Enable timer: periodic, interrupt enabled */
       ctrl = TIMER_CTRL_ENABLE | TIMER_CTRL_PERIODIC | TIMER_CTRL_IE;
       writel(ctrl, timer_base + TIMER_CTRL);
       
       /* Register interrupt */
       setup_irq(IRQ_TIMER, &myboard_timer_irq);
   }

5.2 Clocksource and Clockevent
--------------------------------------------------------------------------------

**Clocksource (for timekeeping):**

.. code-block:: c

   static cycle_t myboard_read_cycles(struct clocksource *cs)
   {
       return (cycle_t)readl(timer_base + TIMER_VALUE);
   }
   
   static struct clocksource myboard_clocksource = {
       .name   = "myboard-timer",
       .rating = 200,
       .read   = myboard_read_cycles,
       .mask   = CLOCKSOURCE_MASK(32),
       .flags  = CLOCK_SOURCE_IS_CONTINUOUS,
   };
   
   void __init myboard_clocksource_init(void)
   {
       clocksource_register_hz(&myboard_clocksource, CLOCK_FREQ);
   }

**Clockevent (for scheduling):**

.. code-block:: c

   static int myboard_set_next_event(unsigned long cycles,
                                     struct clock_event_device *evt)
   {
       writel(cycles, timer_base + TIMER_LOAD);
       return 0;
   }
   
   static struct clock_event_device myboard_clockevent = {
       .name           = "myboard-timer",
       .features       = CLOCK_EVT_FEAT_PERIODIC | CLOCK_EVT_FEAT_ONESHOT,
       .rating         = 200,
       .set_next_event = myboard_set_next_event,
   };
   
   void __init myboard_clockevent_init(void)
   {
       struct clock_event_device *evt = &myboard_clockevent;
       
       evt->cpumask = cpumask_of(0);
       clockevents_config_and_register(evt, CLOCK_FREQ, 1, 0xffffffff);
   }

================================================================================
6. Device Tree Integration
================================================================================

6.1 Device Tree Basics
--------------------------------------------------------------------------------

**Board DTS File:** ``arch/arm/boot/dts/myboard.dts``

.. code-block:: dts

   /dts-v1/;
   
   #include "myvendor-soc.dtsi"
   
   / {
       model = "My Custom Board";
       compatible = "vendor,myboard", "vendor,mysoc";
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x10000000>;  /* 256MB */
       };
       
       chosen {
           bootargs = "console=ttyS0,115200 root=/dev/mmcblk0p2 rootwait";
           stdout-path = &uart0;
       };
       
       leds {
           compatible = "gpio-leds";
           
           status-led {
               label = "status";
               gpios = <&gpio1 5 GPIO_ACTIVE_HIGH>;
               linux,default-trigger = "heartbeat";
           };
       };
   };
   
   &uart0 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&uart0_pins>;
   };
   
   &i2c0 {
       status = "okay";
       clock-frequency = <400000>;
       
       eeprom@50 {
           compatible = "atmel,24c256";
           reg = <0x50>;
       };
   };

6.2 Parsing Device Tree in Driver
--------------------------------------------------------------------------------

.. code-block:: c

   #include <linux/of.h>
   #include <linux/of_device.h>
   
   static int mydriver_probe(struct platform_device *pdev)
   {
       struct device_node *np = pdev->dev.of_node;
       u32 clock_freq;
       const char *label;
       
       /* Read properties */
       if (of_property_read_u32(np, "clock-frequency", &clock_freq))
           clock_freq = 100000;  /* Default 100kHz */
       
       if (of_property_read_string(np, "label", &label))
           label = "default";
       
       pr_info("Clock: %u Hz, Label: %s\n", clock_freq, label);
       
       return 0;
   }
   
   static const struct of_device_id mydriver_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { /* sentinel */ }
   };
   MODULE_DEVICE_TABLE(of, mydriver_of_match);
   
   static struct platform_driver mydriver = {
       .probe  = mydriver_probe,
       .driver = {
           .name = "mydriver",
           .of_match_table = mydriver_of_match,
       },
   };

================================================================================
7. Platform Devices
================================================================================

7.1 Platform Device Registration
--------------------------------------------------------------------------------

**Legacy Platform Data:**

.. code-block:: c

   /* Board file: arch/arm/mach-<vendor>/board-<name>.c */
   
   static struct resource mydevice_resources[] = {
       {
           .start  = 0x48000000,
           .end    = 0x48000fff,
           .flags  = IORESOURCE_MEM,
       },
       {
           .start  = IRQ_MYDEVICE,
           .end    = IRQ_MYDEVICE,
           .flags  = IORESOURCE_IRQ,
       },
   };
   
   static struct mydevice_platform_data mydevice_pdata = {
       .clock_freq = 48000000,
       .mode       = MYDEVICE_MODE_MASTER,
   };
   
   static struct platform_device mydevice = {
       .name           = "mydevice",
       .id             = 0,
       .num_resources  = ARRAY_SIZE(mydevice_resources),
       .resource       = mydevice_resources,
       .dev = {
           .platform_data = &mydevice_pdata,
       },
   };
   
   static struct platform_device *myboard_devices[] __initdata = {
       &mydevice,
       /* ... other devices ... */
   };
   
   static void __init myboard_init(void)
   {
       platform_add_devices(myboard_devices, ARRAY_SIZE(myboard_devices));
   }

7.2 Resource Management
--------------------------------------------------------------------------------

.. code-block:: c

   /* Driver accessing platform resources */
   
   static int mydriver_probe(struct platform_device *pdev)
   {
       struct resource *res;
       void __iomem *base;
       int irq;
       
       /* Get memory resource */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(base))
           return PTR_ERR(base);
       
       /* Get IRQ */
       irq = platform_get_irq(pdev, 0);
       if (irq < 0)
           return irq;
       
       /* Get platform data */
       struct mydevice_platform_data *pdata = dev_get_platdata(&pdev->dev);
       
       return 0;
   }

================================================================================
8. Power Management
================================================================================

8.1 CPU Power States
--------------------------------------------------------------------------------

.. code-block:: c

   /* Implement PM operations */
   
   static int myboard_pm_enter(suspend_state_t state)
   {
       switch (state) {
       case PM_SUSPEND_STANDBY:
           /* Standby mode */
           myboard_enter_standby();
           break;
       case PM_SUSPEND_MEM:
           /* Suspend to RAM */
           myboard_enter_suspend();
           break;
       default:
           return -EINVAL;
       }
       return 0;
   }
   
   static const struct platform_suspend_ops myboard_pm_ops = {
       .enter      = myboard_pm_enter,
       .valid      = suspend_valid_only_mem,
   };
   
   void __init myboard_pm_init(void)
   {
       suspend_set_ops(&myboard_pm_ops);
   }

================================================================================
9. Console Configuration
================================================================================

9.1 Early Console Setup
--------------------------------------------------------------------------------

.. code-block:: c

   /* Early printk for debugging */
   
   #include <linux/console.h>
   
   static void early_uart_write(struct console *con, const char *s,
                                unsigned n)
   {
       while (n--) {
           while (!(readl(UART_BASE + UART_SR) & UART_TX_EMPTY))
               barrier();
           writel(*s++, UART_BASE + UART_TX);
       }
   }
   
   static struct console early_uart_console = {
       .name   = "earlyuart",
       .write  = early_uart_write,
       .flags  = CON_PRINTBUFFER | CON_BOOT,
       .index  = -1,
   };
   
   void __init early_console_setup(void)
   {
       register_console(&early_uart_console);
   }

================================================================================
10. BSP Development Workflow
================================================================================

10.1 Step-by-Step Guide
--------------------------------------------------------------------------------

**Step 1: Prepare Toolchain**

.. code-block:: bash

   # Download cross-compiler
   wget https://developer.arm.com/.../gcc-arm-none-eabi.tar.bz2
   tar xjf gcc-arm-none-eabi.tar.bz2
   export PATH=$PWD/gcc-arm-none-eabi/bin:$PATH
   
   # Verify
   arm-linux-gnueabihf-gcc --version

**Step 2: Configure Kernel**

.. code-block:: bash

   cd linux
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
   
   # Or use existing defconfig
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- myboard_defconfig

**Step 3: Create Board Files**

.. code-block:: bash

   # Create machine directory
   mkdir -p arch/arm/mach-myvendor
   
   # Create files
   touch arch/arm/mach-myvendor/Makefile
   touch arch/arm/mach-myvendor/Kconfig
   touch arch/arm/mach-myvendor/board-myboard.c

**Step 4: Implement BSP**

.. code-block:: c

   /* Minimal board file template */
   
   #include <linux/init.h>
   #include <linux/platform_device.h>
   #include <asm/mach-types.h>
   #include <asm/mach/arch.h>
   
   static void __init myboard_init(void)
   {
       /* Register devices */
   }
   
   MACHINE_START(MYBOARD, "My Board Name")
       .map_io     = myboard_map_io,
       .init_irq   = myboard_init_irq,
       .init_time  = myboard_timer_init,
       .init_machine = myboard_init,
       .restart    = myboard_restart,
   MACHINE_END

**Step 5: Build and Test**

.. code-block:: bash

   # Build kernel
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- dtbs
   
   # Build modules
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules
   
   # Deploy to board
   cp arch/arm/boot/zImage /tftpboot/
   cp arch/arm/boot/dts/myboard.dtb /tftpboot/

10.2 Debugging Tips
--------------------------------------------------------------------------------

**Enable Debug Output:**

.. code-block:: c

   /* Kernel command line */
   console=ttyS0,115200 earlyprintk debug loglevel=8
   
   /* In code */
   #define DEBUG
   #include <linux/kernel.h>
   
   pr_debug("Debug message: %d\n", value);
   dev_dbg(&pdev->dev, "Device debug: %s\n", name);

**JTAG Debugging:**

.. code-block:: bash

   # OpenOCD configuration
   openocd -f board/myboard.cfg
   
   # GDB connection
   arm-linux-gnueabihf-gdb vmlinux
   (gdb) target remote localhost:3333
   (gdb) break start_kernel
   (gdb) continue

================================================================================
11. Best Practices
================================================================================

**Code Organization:**

- Keep board-specific code in ``arch/<arch>/mach-<vendor>/``
- Use device tree for hardware description
- Minimize platform data, prefer device tree
- Follow kernel coding style

**Performance:**

- Map frequently accessed I/O as static
- Use appropriate memory barriers
- Optimize interrupt latency
- Profile boot time

**Maintainability:**

- Document hardware quirks
- Use descriptive names
- Add comments for non-obvious code
- Submit upstream when possible

**Security:**

- Validate all inputs
- Use appropriate memory protections
- Implement secure boot if needed
- Follow security best practices

================================================================================
End of Linux BSP Development Cheatsheet
================================================================================
