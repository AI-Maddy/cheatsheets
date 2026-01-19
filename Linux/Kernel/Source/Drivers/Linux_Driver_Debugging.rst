===================================
Linux Driver Debugging Guide
===================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

printk Debug
------------

.. code-block:: c

   #include <linux/kernel.h>
   
   /* Basic printk */
   printk(KERN_INFO "Value: %d\n", value);
   
   /* Device-specific logging */
   dev_dbg(&pdev->dev, "Debug message\n");
   dev_info(&pdev->dev, "Info message\n");
   dev_warn(&pdev->dev, "Warning message\n");
   dev_err(&pdev->dev, "Error message\n");
   
   /* Dynamic debug (runtime control) */
   pr_debug("Debug message\n");  // Enable via debugfs
   
   /* Rate-limited */
   dev_info_ratelimited(&pdev->dev, "Repeating message\n");

Dynamic Debug
-------------

.. code-block:: bash

   # Enable debug for specific file
   echo 'file mydriver.c +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug for specific function
   echo 'func myfunction +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable all debug in module
   echo 'module mymodule +p' > /sys/kernel/debug/dynamic_debug/control
   
   # View current settings
   cat /sys/kernel/debug/dynamic_debug/control

debugfs Usage
-------------

.. code-block:: c

   #include <linux/debugfs.h>
   
   static struct dentry *debug_dir;
   static u32 debug_value;
   
   /* Create debugfs directory */
   debug_dir = debugfs_create_dir("mydriver", NULL);
   
   /* Create file */
   debugfs_create_u32("value", 0644, debug_dir, &debug_value);
   
   /* Read from userspace */
   cat /sys/kernel/debug/mydriver/value
   
   /* Write from userspace */
   echo 42 > /sys/kernel/debug/mydriver/value

Logging and printk
==================

printk Log Levels
-----------------

.. code-block:: c

   #include <linux/printk.h>
   
   printk(KERN_EMERG   "System is unusable\n");      // 0
   printk(KERN_ALERT   "Action must be taken\n");    // 1
   printk(KERN_CRIT    "Critical conditions\n");     // 2
   printk(KERN_ERR     "Error conditions\n");        // 3
   printk(KERN_WARNING "Warning conditions\n");      // 4
   printk(KERN_NOTICE  "Normal but significant\n");  // 5
   printk(KERN_INFO    "Informational\n");           // 6
   printk(KERN_DEBUG   "Debug-level messages\n");    // 7
   
   /* Convenience macros */
   pr_emerg("Emergency message\n");
   pr_alert("Alert message\n");
   pr_crit("Critical message\n");
   pr_err("Error message\n");
   pr_warn("Warning message\n");
   pr_notice("Notice message\n");
   pr_info("Info message\n");
   pr_debug("Debug message\n");

Device-Specific Logging
------------------------

.. code-block:: c

   struct device *dev = &pdev->dev;
   
   dev_emerg(dev, "Emergency\n");
   dev_alert(dev, "Alert\n");
   dev_crit(dev, "Critical\n");
   dev_err(dev, "Error\n");
   dev_warn(dev, "Warning\n");
   dev_notice(dev, "Notice\n");
   dev_info(dev, "Info\n");
   dev_dbg(dev, "Debug\n");  // Controlled by dynamic debug
   
   /* With device name in output */
   dev_info(&pdev->dev, "Probe successful\n");
   // Output: mydevice: Probe successful

Rate-Limited Logging
--------------------

.. code-block:: c

   /* Print at most once per second */
   printk_ratelimited(KERN_INFO "Frequent event\n");
   
   dev_info_ratelimited(&pdev->dev, "Repeating message\n");
   
   /* Once only */
   printk_once(KERN_INFO "One-time message\n");
   dev_info_once(&pdev->dev, "First time only\n");

Hexdump
-------

.. code-block:: c

   /* Dump buffer */
   print_hex_dump(KERN_INFO, "Buffer: ", DUMP_PREFIX_ADDRESS,
                   16, 1, buffer, length, true);
   
   /* Simpler version */
   print_hex_dump_bytes("Data: ", DUMP_PREFIX_NONE, buffer, length);

Dynamic Debug
=============

Using pr_debug
--------------

.. code-block:: c

   #define DEBUG  // Enable all pr_debug in this file
   #include <linux/kernel.h>
   
   static int mydriver_probe(struct platform_device *pdev) {
       pr_debug("Entering probe\n");
       
       // ... code ...
       
       pr_debug("Register value: 0x%08x\n", value);
       
       return 0;
   }

Runtime Control
---------------

.. code-block:: bash

   # Enable debug for specific file
   echo 'file mydriver.c +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable for function
   echo 'func mydriver_probe +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable for module
   echo 'module mydriver +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable for specific line
   echo 'file mydriver.c line 100 +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Disable
   echo 'module mydriver -p' > /sys/kernel/debug/dynamic_debug/control
   
   # Add function name to output
   echo 'module mydriver +pf' > /sys/kernel/debug/dynamic_debug/control
   
   # Add line number
   echo 'module mydriver +pl' > /sys/kernel/debug/dynamic_debug/control
   
   # Add module name
   echo 'module mydriver +pm' > /sys/kernel/debug/dynamic_debug/control

debugfs
=======

Creating debugfs Files
----------------------

.. code-block:: c

   #include <linux/debugfs.h>
   
   struct mydev_data {
       struct dentry *debug_dir;
       u32 debug_reg;
       bool debug_enabled;
   };
   
   static int mydev_init_debugfs(struct mydev_data *data) {
       /* Create directory */
       data->debug_dir = debugfs_create_dir("mydriver", NULL);
       if (!data->debug_dir)
           return -ENOMEM;
       
       /* Create u32 file */
       debugfs_create_u32("register", 0644, data->debug_dir,
                           &data->debug_reg);
       
       /* Create bool file */
       debugfs_create_bool("enabled", 0644, data->debug_dir,
                            &data->debug_enabled);
       
       /* Create u8, u16, u64, etc. */
       debugfs_create_u8("value8", 0644, data->debug_dir, &data->val8);
       debugfs_create_x32("hex32", 0644, data->debug_dir, &data->hex);
       
       return 0;
   }
   
   static void mydev_cleanup_debugfs(struct mydev_data *data) {
       debugfs_remove_recursive(data->debug_dir);
   }

Custom debugfs Operations
--------------------------

.. code-block:: c

   static ssize_t mydev_debug_read(struct file *file, char __user *buf,
                                    size_t count, loff_t *ppos) {
       struct mydev_data *data = file->private_data;
       char tmp[32];
       int len;
       
       len = snprintf(tmp, sizeof(tmp), "Value: 0x%08x\n",
                       readl(data->regs + DEBUG_REG));
       
       return simple_read_from_buffer(buf, count, ppos, tmp, len);
   }
   
   static ssize_t mydev_debug_write(struct file *file,
                                     const char __user *buf,
                                     size_t count, loff_t *ppos) {
       struct mydev_data *data = file->private_data;
       u32 value;
       int ret;
       
       ret = kstrtou32_from_user(buf, count, 0, &value);
       if (ret)
           return ret;
       
       writel(value, data->regs + DEBUG_REG);
       
       return count;
   }
   
   static const struct file_operations mydev_debug_fops = {
       .owner = THIS_MODULE,
       .open = simple_open,
       .read = mydev_debug_read,
       .write = mydev_debug_write,
   };
   
   /* Create custom file */
   debugfs_create_file("control", 0644, data->debug_dir,
                        data, &mydev_debug_fops);

Register Dump
-------------

.. code-block:: c

   static int mydev_regs_show(struct seq_file *s, void *unused) {
       struct mydev_data *data = s->private;
       
       seq_printf(s, "CTRL:   0x%08x\n", readl(data->regs + CTRL_REG));
       seq_printf(s, "STATUS: 0x%08x\n", readl(data->regs + STATUS_REG));
       seq_printf(s, "CONFIG: 0x%08x\n", readl(data->regs + CONFIG_REG));
       
       return 0;
   }
   
   DEFINE_SHOW_ATTRIBUTE(mydev_regs);
   
   /* Create file */
   debugfs_create_file("registers", 0444, data->debug_dir,
                        data, &mydev_regs_fops);

ftrace and Tracing
==================

Function Tracing
----------------

.. code-block:: bash

   # Trace all kernel functions
   echo function > /sys/kernel/debug/tracing/current_tracer
   
   # Filter to specific module
   echo ':mod:mydriver' > /sys/kernel/debug/tracing/set_ftrace_filter
   
   # Start tracing
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   
   # View trace
   cat /sys/kernel/debug/tracing/trace
   
   # Stop tracing
   echo 0 > /sys/kernel/debug/tracing/tracing_on

Custom Tracepoints
------------------

.. code-block:: c

   #include <linux/tracepoint.h>
   #include <trace/events/mydriver.h>
   
   /* In include/trace/events/mydriver.h */
   TRACE_EVENT(mydriver_event,
       TP_PROTO(int value, const char *name),
       TP_ARGS(value, name),
       TP_STRUCT__entry(
           __field(int, value)
           __string(name, name)
       ),
       TP_fast_assign(
           __entry->value = value;
           __assign_str(name, name);
       ),
       TP_printk("value=%d name=%s",
                  __entry->value, __get_str(name))
   );
   
   /* In driver */
   #define CREATE_TRACE_POINTS
   #include <trace/events/mydriver.h>
   
   static void mydriver_func(void) {
       trace_mydriver_event(42, "test");
   }

Kernel Debugging Tools
======================

KGDB
----

.. code-block:: bash

   # Kernel command line
   kgdboc=ttyS0,115200 kgdbwait
   
   # In GDB
   (gdb) target remote /dev/ttyS0
   (gdb) break mydriver_probe
   (gdb) continue

KDB (Kernel Debugger)
---------------------

.. code-block:: bash

   # Trigger via sysrq
   echo g > /proc/sysrq-trigger
   
   # KDB commands
   kdb> lsmod
   kdb> bt
   kdb> md <address>  # Memory dump
   kdb> go            # Continue

Oops Analysis
-------------

.. code-block:: bash

   # Decode oops with symbols
   ./scripts/decode_stacktrace.sh vmlinux < oops.txt
   
   # Disassemble function
   objdump -d mydriver.ko | less

Memory Debugging
================

KASAN (Kernel Address Sanitizer)
---------------------------------

.. code-block:: c

   /* Enable in kernel config */
   CONFIG_KASAN=y
   
   /* Detects:
    * - Use-after-free
    * - Out-of-bounds accesses
    * - Use-after-return
    * - Double-free
    */

SLUB Debug
----------

.. code-block:: bash

   # Boot parameter
   slub_debug=FPZ
   
   # F - Sanity checks
   # P - Poisoning
   # Z - Red zoning
   
   # Check specific cache
   slub_debug=FPZ,kmalloc-256

kmemleak
--------

.. code-block:: bash

   # Enable in config
   CONFIG_DEBUG_KMEMLEAK=y
   
   # Trigger scan
   echo scan > /sys/kernel/debug/kmemleak
   
   # View leaks
   cat /sys/kernel/debug/kmemleak
   
   # Clear
   echo clear > /sys/kernel/debug/kmemleak

Lock Debugging
==============

Lockdep
-------

.. code-block:: c

   /* Enable in config */
   CONFIG_PROVE_LOCKING=y
   CONFIG_DEBUG_LOCK_ALLOC=y
   CONFIG_LOCKDEP=y
   
   /* Detects:
    * - Deadlocks
    * - Lock inversions
    * - Circular dependencies
    * - IRQ context violations
    */

Lock Statistics
---------------

.. code-block:: bash

   # Enable
   CONFIG_LOCK_STAT=y
   
   # View stats
   cat /proc/lock_stat

Performance Analysis
====================

perf
----

.. code-block:: bash

   # Record events
   perf record -a -g sleep 10
   
   # View report
   perf report
   
   # Probe specific function
   perf probe mydriver_probe
   perf record -e probe:mydriver_probe -a
   
   # Trace function
   perf trace -e mydriver_probe

eBPF/bpftrace
-------------

.. code-block:: bash

   # Trace function calls
   bpftrace -e 'kprobe:mydriver_probe { @[comm] = count(); }'
   
   # Trace with arguments
   bpftrace -e 'kprobe:mydriver_write { printf("%s wrote\n", comm); }'

Complete Debug Example
=======================

Driver with Full Debug Support
-------------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/debugfs.h>
   #include <linux/io.h>
   
   struct mydev_data {
       struct device *dev;
       void __iomem *regs;
       struct dentry *debug_dir;
       
       /* Debug counters */
       u32 irq_count;
       u32 tx_count;
       u32 rx_count;
       u32 error_count;
   };
   
   static int mydev_regs_show(struct seq_file *s, void *unused) {
       struct mydev_data *data = s->private;
       
       seq_puts(s, "=== Register Dump ===\n");
       seq_printf(s, "CTRL:   0x%08x\n", readl(data->regs + 0x00));
       seq_printf(s, "STATUS: 0x%08x\n", readl(data->regs + 0x04));
       seq_printf(s, "CONFIG: 0x%08x\n", readl(data->regs + 0x08));
       
       seq_puts(s, "\n=== Statistics ===\n");
       seq_printf(s, "IRQ count:   %u\n", data->irq_count);
       seq_printf(s, "TX count:    %u\n", data->tx_count);
       seq_printf(s, "RX count:    %u\n", data->rx_count);
       seq_printf(s, "Error count: %u\n", data->error_count);
       
       return 0;
   }
   
   DEFINE_SHOW_ATTRIBUTE(mydev_regs);
   
   static ssize_t mydev_debug_write(struct file *file,
                                     const char __user *buf,
                                     size_t count, loff_t *ppos) {
       struct mydev_data *data = file->private_data;
       char cmd[32];
       
       if (count >= sizeof(cmd))
           return -EINVAL;
       
       if (copy_from_user(cmd, buf, count))
           return -EFAULT;
       
       cmd[count] = '\0';
       
       if (strncmp(cmd, "reset", 5) == 0) {
           data->irq_count = 0;
           data->tx_count = 0;
           data->rx_count = 0;
           data->error_count = 0;
           dev_info(data->dev, "Statistics reset\n");
       } else if (strncmp(cmd, "dump", 4) == 0) {
           dev_info(data->dev, "CTRL=0x%08x STATUS=0x%08x\n",
                    readl(data->regs + 0x00),
                    readl(data->regs + 0x04));
       }
       
       return count;
   }
   
   static const struct file_operations mydev_debug_fops = {
       .owner = THIS_MODULE,
       .open = simple_open,
       .write = mydev_debug_write,
   };
   
   static void mydev_init_debugfs(struct mydev_data *data) {
       data->debug_dir = debugfs_create_dir("mydriver", NULL);
       
       debugfs_create_file("registers", 0444, data->debug_dir,
                            data, &mydev_regs_fops);
       
       debugfs_create_file("control", 0200, data->debug_dir,
                            data, &mydev_debug_fops);
       
       debugfs_create_u32("irq_count", 0444, data->debug_dir,
                           &data->irq_count);
       debugfs_create_u32("tx_count", 0444, data->debug_dir,
                           &data->tx_count);
       debugfs_create_u32("rx_count", 0444, data->debug_dir,
                           &data->rx_count);
       debugfs_create_u32("error_count", 0444, data->debug_dir,
                           &data->error_count);
   }
   
   static irqreturn_t mydev_irq(int irq, void *dev_data) {
       struct mydev_data *data = dev_data;
       
       data->irq_count++;
       
       dev_dbg(data->dev, "IRQ #%u\n", data->irq_count);
       
       return IRQ_HANDLED;
   }
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       
       dev_dbg(&pdev->dev, "Probe starting\n");
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       data->dev = &pdev->dev;
       
       /* ... setup hardware ... */
       
       mydev_init_debugfs(data);
       
       dev_info(&pdev->dev, "Device probed successfully\n");
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_data *data = platform_get_drvdata(pdev);
       
       debugfs_remove_recursive(data->debug_dir);
       
       dev_info(&pdev->dev, "Device removed\n");
       return 0;
   }
   
   module_platform_driver(mydev_driver);
   MODULE_LICENSE("GPL");

Best Practices
==============

1. **Use dev_dbg()** for debug messages
2. **Create debugfs** interface for debugging
3. **Add statistics counters**
4. **Use dynamic debug** for runtime control
5. **Implement proper error handling**
6. **Add WARN_ON()** for unexpected conditions
7. **Use BUG_ON()** sparingly
8. **Test with debug options** enabled
9. **Document debug interfaces**
10. **Clean up debug code** before release

Common Pitfalls
===============

1. **Too much printk** in fast paths
2. **Not using dev_* helpers**
3. **Forgetting to remove debugfs**
4. **printk in interrupt** context
5. **Not testing with lockdep**
6. **Leaving BUG_ON()** in production

Debugging Commands
==================

.. code-block:: bash

   # View kernel log
   dmesg
   dmesg -w  # Follow
   
   # Set console log level
   dmesg -n 8
   
   # Check module
   lsmod | grep mydriver
   modinfo mydriver.ko
   
   # View debugfs
   ls /sys/kernel/debug/
   cat /sys/kernel/debug/mydriver/registers
   
   # Enable dynamic debug
   echo 'module mydriver +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Trace
   trace-cmd record -p function_graph -g mydriver_probe
   trace-cmd report

See Also
========

- Linux_Kernel_Synchronization.rst
- Linux_Platform_Drivers.rst
- Linux_Driver_IRQ_Handling.rst

References
==========

- Documentation/admin-guide/dynamic-debug-howto.rst
- Documentation/trace/ftrace.rst
- Documentation/dev-tools/kasan.rst
