==========================================
Linux Kernel Modules Advanced
==========================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Focus: Advanced kernel module programming techniques

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Module Lifecycle
----------------

.. code-block:: text

   Module States:
   
   Source (.c) → Compile → Object (.ko)
       ↓
   insmod/modprobe
       ↓
   module_init() ──→ Initialization
       ↓
   Module LOADED and RUNNING
       ↓
   rmmod
       ↓
   module_exit() ──→ Cleanup
       ↓
   Module UNLOADED

Essential Module Commands
--------------------------

.. code-block:: bash

   # Load module
   insmod mymodule.ko param=value
   modprobe mymodule param=value  # Handles dependencies
   
   # Remove module
   rmmod mymodule
   modprobe -r mymodule
   
   # List modules
   lsmod
   cat /proc/modules
   
   # Module info
   modinfo mymodule.ko
   
   # Module dependencies
   modprobe --show-depends mymodule
   
   # Generate dependencies
   depmod -a

Module Basics
=============

Basic Module Template
---------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/kernel.h>
   #include <linux/init.h>
   
   static int __init mymodule_init(void) {
       pr_info("My module: initialized\n");
       return 0;  // 0 = success, negative = error
   }
   
   static void __exit mymodule_exit(void) {
       pr_info("My module: cleaned up\n");
   }
   
   module_init(mymodule_init);
   module_exit(mymodule_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("A simple kernel module");
   MODULE_VERSION("1.0");

Makefile
--------

.. code-block:: makefile

   obj-m += mymodule.o
   
   all:
       make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
   
   clean:
       make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
   
   # Advanced: Multi-file module
   mydriver-objs := main.o device.o interrupt.o
   obj-m += mydriver.o

Module Parameters
=================

Declaring Parameters
--------------------

.. code-block:: c

   #include <linux/moduleparam.h>
   
   // Simple parameters
   static int count = 1;
   static char *name = "default";
   static bool enabled = true;
   
   module_param(count, int, S_IRUGO);
   MODULE_PARM_DESC(count, "Number of devices (default=1)");
   
   module_param(name, charp, S_IRUGO);
   MODULE_PARM_DESC(name, "Device name (default=default)");
   
   module_param(enabled, bool, S_IRUGO | S_IWUSR);
   MODULE_PARM_DESC(enabled, "Enable feature (default=true)");
   
   // Array parameter
   static int irq[8] = { [0 ... 7] = -1 };
   static int irq_count;
   
   module_param_array(irq, int, &irq_count, S_IRUGO);
   MODULE_PARM_DESC(irq, "IRQ numbers for devices");
   
   // Named parameter (different variable name)
   static int debug_level;
   module_param_named(debug, debug_level, int, S_IRUGO | S_IWUSR);
   MODULE_PARM_DESC(debug, "Debug level (0-5)");

Permission Flags
----------------

.. code-block:: c

   // Parameter permissions (sysfs visibility)
   #define S_IRUGO     (S_IRUSR | S_IRGRP | S_IROTH)  // Read all
   #define S_IWUGO     (S_IWUSR | S_IWGRP | S_IWOTH)  // Write all
   #define S_IXUGO     (S_IXUSR | S_IXGRP | S_IXOTH)  // Execute all
   
   // Common combinations
   0444  // Read-only for all
   0644  // RW for owner, R for others
   0660  // RW for owner and group
   0000  // Not visible in sysfs

Advanced Module Features
========================

Module Aliases
--------------

.. code-block:: c

   // Device alias for automatic loading
   MODULE_ALIAS("platform:my-device");
   MODULE_ALIAS("pci:v00001234d00005678*");
   
   // Usage
   static const struct of_device_id my_of_match[] = {
       { .compatible = "vendor,my-device" },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_of_match);
   
   static const struct pci_device_id my_pci_ids[] = {
       { PCI_DEVICE(0x1234, 0x5678) },
       { }
   };
   MODULE_DEVICE_TABLE(pci, my_pci_ids);

Module Dependencies
-------------------

.. code-block:: c

   // Explicit symbol export
   EXPORT_SYMBOL(my_function);
   EXPORT_SYMBOL_GPL(my_gpl_function);  // GPL-only
   
   // Symbol versioning
   #include <linux/module.h>
   #include <linux/vermagic.h>
   
   MODULE_INFO(vermagic, VERMAGIC_STRING);
   
   // Use symbols from another module
   extern int other_module_function(void);
   
   static int __init mymodule_init(void) {
       int ret = other_module_function();
       return ret;
   }

Module Initialization Levels
=============================

Init Levels
-----------

.. code-block:: c

   // Initialization order (from early to late)
   
   // 1. Pure initcall (before core_initcall)
   pure_initcall(my_pure_init);
   
   // 2. Core initialization
   core_initcall(my_core_init);
   
   // 3. Postcore
   postcore_initcall(my_postcore_init);
   
   // 4. Arch-specific
   arch_initcall(my_arch_init);
   
   // 5. Subsystem
   subsys_initcall(my_subsys_init);
   
   // 6. Filesystem
   fs_initcall(my_fs_init);
   
   // 7. Device
   device_initcall(my_device_init);
   
   // 8. Late initialization
   late_initcall(my_late_init);
   
   // For modules: equivalent to module_init()
   module_init(my_module_init);

Early/Late Init
---------------

.. code-block:: c

   // Early initialization (before module_init)
   static int __init early_setup(char *str) {
       pr_info("Early setup: %s\n", str);
       return 1;
   }
   __setup("mymodule=", early_setup);
   
   // Late initialization
   static int __init my_init(void) {
       pr_info("Regular initialization\n");
       return 0;
   }
   
   static void __init my_late_init(void) {
       pr_info("Late initialization\n");
   }
   
   module_init(my_init);
   late_initcall(my_late_init);

Module Versioning
=================

Version Information
-------------------

.. code-block:: c

   // Module version
   #define DRIVER_VERSION "1.2.3"
   MODULE_VERSION(DRIVER_VERSION);
   
   // Git version (auto-generated)
   MODULE_INFO(gitversion, "$(git describe --always --dirty)");
   
   // Build information
   MODULE_INFO(build_date, __DATE__);
   MODULE_INFO(build_time, __TIME__);
   
   // Firmware version
   MODULE_FIRMWARE("mydevice/firmware.bin");

Symbol Versioning (modversions)
--------------------------------

.. code-block:: c

   // Enable in Kconfig
   CONFIG_MODVERSIONS=y
   
   // CRC checksums automatically generated
   // Prevents loading modules compiled for different kernel version
   
   // Check module version info
   $ modinfo -F vermagic mymodule.ko
   5.15.0-1234 SMP mod_unload modversions
   
   // Force load (dangerous!)
   $ insmod --force mymodule.ko

Dynamic Debug
=============

Debug Macros
------------

.. code-block:: c

   #define DEBUG  // Enable debug messages
   
   #include <linux/module.h>
   #include <linux/kernel.h>
   
   // Print levels (decreasing verbosity)
   pr_emerg("System is unusable\n");
   pr_alert("Action must be taken immediately\n");
   pr_crit("Critical conditions\n");
   pr_err("Error conditions\n");
   pr_warn("Warning conditions\n");
   pr_notice("Normal but significant\n");
   pr_info("Informational\n");
   pr_debug("Debug-level messages\n");  // Only if DEBUG defined
   
   // Device-specific prints
   dev_emerg(&dev->dev, "Device emergency\n");
   dev_err(&dev->dev, "Device error\n");
   dev_warn(&dev->dev, "Device warning\n");
   dev_info(&dev->dev, "Device info\n");
   dev_dbg(&dev->dev, "Device debug\n");

Dynamic Debug Framework
-----------------------

.. code-block:: bash

   # Enable dynamic debug
   CONFIG_DYNAMIC_DEBUG=y
   
   # Control at runtime
   echo 'module mymodule +p' > /sys/kernel/debug/dynamic_debug/control
   echo 'file myfile.c +p' > /sys/kernel/debug/dynamic_debug/control
   echo 'func my_function +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Flags:
   # p = enable pr_debug()
   # f = include function name
   # l = include line number
   # m = include module name
   # t = include thread ID
   
   # View current settings
   cat /sys/kernel/debug/dynamic_debug/control

Module Locking
==============

Module Reference Counting
--------------------------

.. code-block:: c

   // Module uses this_module to track references
   struct module {
       struct list_head list;
       char name[MODULE_NAME_LEN];
       struct module_kobject mkobj;
       struct module_attribute *modinfo_attrs;
       
       unsigned int taints;
       atomic_t refcnt;  // Reference count
       
       // Module state
       enum module_state state;
       
       // Symbols
       Elf_Sym *symtab;
       unsigned int num_syms;
       
       // Init/exit functions
       int (*init)(void);
       void (*exit)(void);
   };
   
   // Prevent module unload
   try_module_get(THIS_MODULE);
   
   // Allow module unload
   module_put(THIS_MODULE);
   
   // Example: file operations
   static int device_open(struct inode *inode, struct file *file) {
       try_module_get(THIS_MODULE);
       return 0;
   }
   
   static int device_release(struct inode *inode, struct file *file) {
       module_put(THIS_MODULE);
       return 0;
   }

Module State
------------

.. code-block:: c

   enum module_state {
       MODULE_STATE_LIVE,        // Module is loaded
       MODULE_STATE_COMING,      // Being loaded
       MODULE_STATE_GOING,       // Being unloaded
       MODULE_STATE_UNFORMED,    // Still setting up
   };
   
   // Check if module can be unloaded
   static inline bool module_is_live(struct module *mod) {
       return mod->state != MODULE_STATE_GOING;
   }

Built-in vs Module
==================

Conditional Compilation
-----------------------

.. code-block:: c

   // Check if built as module
   #ifdef MODULE
       pr_info("Built as module\n");
   #else
       pr_info("Built into kernel\n");
   #endif
   
   // IS_ENABLED macro
   if (IS_ENABLED(CONFIG_MY_FEATURE)) {
       // Feature enabled (either built-in or module)
   }
   
   if (IS_BUILTIN(CONFIG_MY_FEATURE)) {
       // Feature built into kernel
   }
   
   if (IS_MODULE(CONFIG_MY_FEATURE)) {
       // Feature built as module
   }

Kconfig
-------

.. code-block:: kconfig

   config MY_DRIVER
       tristate "My Driver Support"
       depends on PCI && SYSFS
       select CRC32
       help
         This driver supports My Device hardware.
         
         To compile as a module, choose M.
         To compile into kernel, choose Y.
         
   config MY_DRIVER_DEBUG
       bool "My Driver Debugging"
       depends on MY_DRIVER
       help
         Enable debugging features.

Module Signing
==============

Signed Modules
--------------

.. code-block:: bash

   # Enable module signing
   CONFIG_MODULE_SIG=y
   CONFIG_MODULE_SIG_ALL=y
   CONFIG_MODULE_SIG_KEY="certs/signing_key.pem"
   
   # Sign module manually
   scripts/sign-file sha256 kernel-key.priv kernel-key.pub mymodule.ko
   
   # Verify signature
   modinfo mymodule.ko | grep signer
   
   # Load signed module
   insmod mymodule.ko

Debugging Modules
=================

Kernel Debugging
----------------

.. code-block:: c

   // Stack traces
   #include <linux/stacktrace.h>
   dump_stack();
   
   // BUG/WARN macros
   BUG();                        // Kernel panic
   BUG_ON(condition);            // Panic if condition true
   WARN();                       // Warning (not fatal)
   WARN_ON(condition);           // Warning if condition true
   WARN_ON_ONCE(condition);      // Warn only once
   
   // Assertions
   BUILD_BUG_ON(sizeof(struct foo) != 64);  // Compile-time
   
   // Memory debugging
   CONFIG_DEBUG_SLAB=y
   CONFIG_DEBUG_PAGEALLOC=y
   CONFIG_KASAN=y  // AddressSanitizer
   
   // Lock debugging
   CONFIG_DEBUG_MUTEXES=y
   CONFIG_DEBUG_SPINLOCK=y
   CONFIG_LOCKDEP=y

GDB Debugging
-------------

.. code-block:: bash

   # Build kernel with debug symbols
   CONFIG_DEBUG_INFO=y
   CONFIG_GDB_SCRIPTS=y
   
   # QEMU + GDB
   qemu-system-x86_64 -kernel bzImage -s -S
   
   # In another terminal
   gdb vmlinux
   (gdb) target remote :1234
   (gdb) break my_function
   (gdb) continue
   
   # KGDB (kernel debugger)
   CONFIG_KGDB=y
   CONFIG_KGDB_SERIAL_CONSOLE=y

Performance Profiling
=====================

Tracing
-------

.. code-block:: c

   // Tracepoints
   #include <trace/events/mymodule.h>
   
   DECLARE_EVENT_CLASS(mymodule_event,
       TP_PROTO(int value),
       TP_ARGS(value),
       TP_STRUCT__entry(
           __field(int, value)
       ),
       TP_fast_assign(
           __entry->value = value;
       ),
       TP_printk("value=%d", __entry->value)
   );
   
   DEFINE_EVENT(mymodule_event, my_event,
       TP_PROTO(int value),
       TP_ARGS(value)
   );
   
   // Use tracepoint
   trace_my_event(42);

ftrace
------

.. code-block:: bash

   # Enable function tracing
   echo function > /sys/kernel/debug/tracing/current_tracer
   echo my_function > /sys/kernel/debug/tracing/set_ftrace_filter
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   
   # View trace
   cat /sys/kernel/debug/tracing/trace
   
   # Disable
   echo 0 > /sys/kernel/debug/tracing/tracing_on

Best Practices
==============

1. **Check return values** from init functions
2. **Clean up on error** paths in init
3. **Free all resources** in exit
4. **Use EXPORT_SYMBOL_GPL** for GPL-only symbols
5. **Version your module** properly
6. **Document parameters** with MODULE_PARM_DESC
7. **Handle module unload** gracefully
8. **Avoid global state** when possible
9. **Test module loading/unloading** thoroughly
10. **Sign modules** for secure boot

Common Pitfalls
===============

1. **Resource leaks** - not freeing in exit
2. **Use after free** - accessing after cleanup
3. **Missing dependencies** - not declaring required modules
4. **Symbol conflicts** - name clashes with kernel
5. **Incomplete cleanup** on init error
6. **Unsafe module removal** while in use
7. **Tainting kernel** with non-GPL modules

Quick Reference
===============

.. code-block:: c

   // Module basics
   module_init(init_function);
   module_exit(exit_function);
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Name");
   MODULE_DESCRIPTION("Description");
   MODULE_VERSION("1.0");
   
   // Parameters
   module_param(name, type, perm);
   module_param_array(name, type, &count, perm);
   MODULE_PARM_DESC(name, "Description");
   
   // Symbols
   EXPORT_SYMBOL(function);
   EXPORT_SYMBOL_GPL(function);
   
   // Devices
   MODULE_DEVICE_TABLE(type, table);
   MODULE_ALIAS("alias");

See Also
========

- Linux_Kernel_Architecture.rst
- Linux_Driver_Debugging.rst
- Linux_Char_Device_Drivers.rst

References
==========

- kernel/module.c in Linux source
- Documentation/kbuild/ in Linux source
- https://www.kernel.org/doc/html/latest/kbuild/modules.html
