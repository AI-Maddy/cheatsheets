================================================================================
Linux Device Drivers - Comprehensive Catalog
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Essential Linux Device Drivers (850 pages, 23 chapters)
:Target: Linux Kernel 5.x/6.x Driver Development
:Version: 1.0

================================================================================
TL;DR - Quick Driver Reference
================================================================================

**Complete Driver Type Reference:**

.. code-block:: text

   Driver Type          | Registration API              | Key Structure        | Device Examples
   =============================================================================================================
   Character            | alloc_chrdev_region()        | file_operations      | /dev/null, /dev/random
   Block                | blk_mq_alloc_disk()          | block_device_ops     | Hard disks, SSDs, SD cards
   Network              | register_netdev()            | net_device_ops       | Ethernet, WiFi cards
   Serial/UART          | uart_register_driver()       | uart_ops             | RS-232, Serial consoles
   TTY                  | tty_register_driver()        | tty_operations       | Terminals, modems
   Input                | input_register_device()      | input_dev            | Keyboards, mice, touchscreens
   I2C                  | i2c_add_driver()             | i2c_driver           | EEPROMs, RTCs, sensors
   SPI                  | spi_register_driver()        | spi_driver           | Flash memory, ADCs
   Platform             | platform_driver_register()   | platform_driver      | SoC peripherals
   PCI                  | pci_register_driver()        | pci_driver           | Graphics cards, NICs
   USB                  | usb_register_driver()        | usb_driver           | USB storage, HID devices
   PCMCIA/CardBus       | pcmcia_register_driver()     | pcmcia_driver        | PCMCIA modems, WiFi
   Video/Framebuffer    | register_framebuffer()       | fb_ops               | Display controllers
   V4L2 (Video4Linux2)  | video_register_device()      | v4l2_file_operations | Cameras, video capture
   ALSA (Audio)         | snd_card_new()               | snd_pcm_ops          | Sound cards, codecs
   MTD (Flash)          | mtd_device_register()        | mtd_info             | NAND/NOR flash, DataFlash
   RTC                  | rtc_register_device()        | rtc_class_ops        | Real-time clocks
   Watchdog             | watchdog_register_device()   | watchdog_ops         | Watchdog timers
   LED                  | led_classdev_register()      | led_classdev         | LEDs, GPIO LEDs
   PWM                  | pwm_chip_add()               | pwm_ops              | PWM controllers
   Regulator            | regulator_register()         | regulator_ops        | Voltage regulators
   GPIO                 | gpiochip_add_data()          | gpio_chip            | GPIO controllers
   IIO (Industrial I/O) | iio_device_register()        | iio_info             | ADCs, DACs, accelerometers
   Hwmon (Hardware Mon) | hwmon_device_register()      | hwmon_ops            | Temperature sensors, fans
   Bluetooth            | hci_register_dev()           | hci_dev              | Bluetooth adapters
   WiFi                 | ieee80211_register_hw()      | ieee80211_ops        | WiFi adapters
   IrDA                 | register_netdev() + IrDA     | net_device_ops       | Infrared transceivers

**Quick Code Templates:**

*Character Driver (5 lines):*

.. code-block:: c

   alloc_chrdev_region(&dev, 0, 1, "name");
   cdev_init(&cdev, &fops); cdev_add(&cdev, dev, 1);
   class = class_create(THIS_MODULE, "class");
   device_create(class, NULL, dev, NULL, "name");

*Platform Driver (3 lines):*

.. code-block:: c

   static struct platform_driver my_driver = {
       .probe = my_probe, .remove = my_remove,
       .driver = { .name = "mydev", .of_match_table = of_match },
   };
   module_platform_driver(my_driver);

*I2C Driver (3 lines):*

.. code-block:: c

   static struct i2c_driver my_driver = {
       .probe = my_probe, .remove = my_remove,
       .id_table = my_id, .driver.of_match_table = of_match,
   };
   module_i2c_driver(my_driver);

*USB Driver (3 lines):*

.. code-block:: c

   static struct usb_driver my_driver = {
       .name = "mydriver", .probe = my_probe, .disconnect = my_disconnect,
       .id_table = my_usb_table,
   };
   module_usb_driver(my_driver);

*Network Driver (3 lines):*

.. code-block:: c

   ndev = alloc_etherdev(sizeof(struct priv));
   ndev->netdev_ops = &my_netdev_ops;
   register_netdev(ndev);

*Block Driver (3 lines):*

.. code-block:: c

   disk = blk_mq_alloc_disk(&tag_set, priv);
   disk->fops = &my_block_ops;
   add_disk(disk);

================================================================================
TABLE OF CONTENTS
================================================================================

1.  Kernel Module Basics
2.  Character Device Drivers
3.  Serial/UART/TTY Drivers
4.  Input Subsystem Drivers
5.  I2C Bus Drivers
6.  SPI Bus Drivers
7.  Platform Drivers
8.  PCI/PCIe Drivers
9.  USB Drivers
10. PCMCIA/CardBus Drivers
11. Block Device Drivers
12. Network Device Drivers
13. Wireless Drivers (WiFi/Bluetooth/IrDA)
14. MTD (Flash Memory) Drivers
15. Video Drivers (Framebuffer/V4L2)
16. Audio (ALSA) Drivers
17. Miscellaneous Drivers (RTC/Watchdog/LED/PWM/Regulator/GPIO/Hwmon/IIO)
18. Driver Development Workflow
19. Driver Debugging Techniques
20. Driver Reference Tables

================================================================================
1. Kernel Module Basics
================================================================================

1.1 Module Structure
--------------------

**Minimal Module:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/kernel.h>
   #include <linux/init.h>
   
   static int __init mymodule_init(void) {
       pr_info("Module loaded\n");
       return 0;  // 0 = success, negative errno on failure
   }
   
   static void __exit mymodule_exit(void) {
       pr_info("Module unloaded\n");
   }
   
   module_init(mymodule_init);
   module_exit(mymodule_exit);
   
   MODULE_LICENSE("GPL");              // Required!
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("My driver");
   MODULE_VERSION("1.0");

**Module Parameters:**

.. code-block:: c

   static int debug = 0;
   module_param(debug, int, 0644);
   MODULE_PARM_DESC(debug, "Enable debug (0=off, 1=on)");
   
   static char *name = "default";
   module_param(name, charp, 0644);
   
   static int ports[4] = {0};
   static int ports_count = 0;
   module_param_array(ports, int, &ports_count, 0644);
   
   // Usage: insmod mymodule.ko debug=1 name="test" ports=0x300,0x310

**Module Build (Makefile):**

.. code-block:: make

   obj-m := mymodule.o
   
   # Multiple source files
   # mymodule-objs := file1.o file2.o file3.o
   
   KDIR := /lib/modules/$(shell uname -r)/build
   
   all:
   	$(MAKE) -C $(KDIR) M=$(PWD) modules
   
   clean:
   	$(MAKE) -C $(KDIR) M=$(PWD) clean
   
   install:
   	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

**Loading/Unloading:**

.. code-block:: bash

   # Load module
   sudo insmod mymodule.ko
   sudo modprobe mymodule  # Auto-load dependencies
   
   # Unload module
   sudo rmmod mymodule
   sudo modprobe -r mymodule
   
   # List loaded modules
   lsmod | grep mymodule
   cat /proc/modules | grep mymodule
   
   # Module information
   modinfo mymodule.ko
   
   # View kernel messages
   dmesg | tail -20
   journalctl -k -f

1.2 Printk and Logging
-----------------------

**Kernel Print Levels:**

.. code-block:: c

   #include <linux/printk.h>
   
   // Traditional printk with log levels
   printk(KERN_EMERG "System is unusable\n");    // LOG_LEVEL 0
   printk(KERN_ALERT "Action must be taken\n");  // LOG_LEVEL 1
   printk(KERN_CRIT "Critical conditions\n");    // LOG_LEVEL 2
   printk(KERN_ERR "Error conditions\n");        // LOG_LEVEL 3
   printk(KERN_WARNING "Warning\n");             // LOG_LEVEL 4
   printk(KERN_NOTICE "Normal significant\n");   // LOG_LEVEL 5
   printk(KERN_INFO "Informational\n");          // LOG_LEVEL 6
   printk(KERN_DEBUG "Debug-level\n");           // LOG_LEVEL 7
   
   // Modern pr_* macros (recommended)
   pr_emerg("System unusable\n");
   pr_alert("Action required\n");
   pr_crit("Critical\n");
   pr_err("Error\n");
   pr_warn("Warning\n");
   pr_notice("Notice\n");
   pr_info("Info\n");
   pr_debug("Debug\n");  // Only if DEBUG defined
   
   // Device-specific logging (best practice)
   dev_emerg(&dev->dev, "Device error\n");
   dev_alert(&dev->dev, "Device alert\n");
   dev_crit(&dev->dev, "Device critical\n");
   dev_err(&dev->dev, "Device error\n");
   dev_warn(&dev->dev, "Device warning\n");
   dev_notice(&dev->dev, "Device notice\n");
   dev_info(&dev->dev, "Device info\n");
   dev_dbg(&dev->dev, "Device debug\n");

**Dynamic Debug:**

.. code-block:: bash

   # Enable/disable debug messages at runtime
   echo 'module mymodule +p' > /sys/kernel/debug/dynamic_debug/control
   echo 'file myfile.c +p' > /sys/kernel/debug/dynamic_debug/control
   echo 'func my_function +p' > /sys/kernel/debug/dynamic_debug/control
   
   # View current settings
   cat /sys/kernel/debug/dynamic_debug/control | grep mymodule

================================================================================
2. Character Device Drivers
================================================================================

2.1 Character Device Registration
----------------------------------

**Complete Character Driver:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/device.h>
   #include <linux/uaccess.h>
   
   static dev_t dev_num;
   static struct cdev my_cdev;
   static struct class *my_class;
   
   static int my_open(struct inode *inode, struct file *file) {
       pr_info("Device opened\n");
       return 0;
   }
   
   static int my_release(struct inode *inode, struct file *file) {
       pr_info("Device closed\n");
       return 0;
   }
   
   static ssize_t my_read(struct file *file, char __user *buf,
                          size_t len, loff_t *offset) {
       char msg[] = "Hello from kernel\n";
       size_t msg_len = strlen(msg);
       
       if (*offset >= msg_len)
           return 0;  // EOF
       
       if (len > msg_len - *offset)
           len = msg_len - *offset;
       
       if (copy_to_user(buf, msg + *offset, len))
           return -EFAULT;
       
       *offset += len;
       return len;
   }
   
   static ssize_t my_write(struct file *file, const char __user *buf,
                           size_t len, loff_t *offset) {
       char kbuf[256];
       
       if (len > sizeof(kbuf) - 1)
           len = sizeof(kbuf) - 1;
       
       if (copy_from_user(kbuf, buf, len))
           return -EFAULT;
       
       kbuf[len] = '\0';
       pr_info("Received: %s\n", kbuf);
       return len;
   }
   
   static long my_ioctl(struct file *file, unsigned int cmd,
                        unsigned long arg) {
       switch (cmd) {
       case 0:
           pr_info("IOCTL command 0\n");
           break;
       default:
           return -ENOTTY;
       }
       return 0;
   }
   
   static struct file_operations fops = {
       .owner = THIS_MODULE,
       .open = my_open,
       .release = my_release,
       .read = my_read,
       .write = my_write,
       .unlocked_ioctl = my_ioctl,
   };
   
   static int __init chardev_init(void) {
       int ret;
       
       // Allocate device number
       ret = alloc_chrdev_region(&dev_num, 0, 1, "mychardev");
       if (ret < 0)
           return ret;
       
       pr_info("Allocated major: %d, minor: %d\n",
               MAJOR(dev_num), MINOR(dev_num));
       
       // Initialize and add cdev
       cdev_init(&my_cdev, &fops);
       ret = cdev_add(&my_cdev, dev_num, 1);
       if (ret < 0)
           goto fail_cdev;
       
       // Create class
       my_class = class_create(THIS_MODULE, "myclass");
       if (IS_ERR(my_class)) {
           ret = PTR_ERR(my_class);
           goto fail_class;
       }
       
       // Create device node (/dev/mychardev)
       if (IS_ERR(device_create(my_class, NULL, dev_num,
                                NULL, "mychardev"))) {
           ret = PTR_ERR(my_class);
           goto fail_device;
       }
       
       pr_info("Character device registered\n");
       return 0;
   
   fail_device:
       class_destroy(my_class);
   fail_class:
       cdev_del(&my_cdev);
   fail_cdev:
       unregister_chrdev_region(dev_num, 1);
       return ret;
   }
   
   static void __exit chardev_exit(void) {
       device_destroy(my_class, dev_num);
       class_destroy(my_class);
       cdev_del(&my_cdev);
       unregister_chrdev_region(dev_num, 1);
       pr_info("Character device unregistered\n");
   }
   
   module_init(chardev_init);
   module_exit(chardev_exit);
   MODULE_LICENSE("GPL");

**IOCTL Definition:**

.. code-block:: c

   #include <linux/ioctl.h>
   
   #define MY_IOCTL_MAGIC 'k'
   
   #define MY_IOCTL_RESET      _IO(MY_IOCTL_MAGIC, 0)
   #define MY_IOCTL_GET_VAL    _IOR(MY_IOCTL_MAGIC, 1, int)
   #define MY_IOCTL_SET_VAL    _IOW(MY_IOCTL_MAGIC, 2, int)
   #define MY_IOCTL_EXCHANGE   _IOWR(MY_IOCTL_MAGIC, 3, int)
   
   // Usage in driver:
   static long my_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
       int val;
       
       switch (cmd) {
       case MY_IOCTL_GET_VAL:
           val = get_hardware_value();
           if (copy_to_user((int __user *)arg, &val, sizeof(val)))
               return -EFAULT;
           break;
       case MY_IOCTL_SET_VAL:
           if (copy_from_user(&val, (int __user *)arg, sizeof(val)))
               return -EFAULT;
           set_hardware_value(val);
           break;
       default:
           return -ENOTTY;
       }
       return 0;
   }


================================================================================
3. Serial/UART/TTY Drivers
================================================================================

3.1 UART Driver Framework
--------------------------

**UART Driver Structure:**

.. code-block:: c

   #include <linux/serial_core.h>
   #include <linux/console.h>
   
   #define MY_UART_NR  2  // Number of ports
   
   struct my_uart_port {
       struct uart_port port;
       void __iomem *base;
       // Private data
   };
   
   // UART operations
   static unsigned int my_uart_tx_empty(struct uart_port *port) {
       // Return TIOCSER_TEMT if TX FIFO empty
       return readl(port->membase + STATUS_REG) & TX_EMPTY ? TIOCSER_TEMT : 0;
   }
   
   static void my_uart_set_mctrl(struct uart_port *port, unsigned int mctrl) {
       // Set modem control lines (DTR, RTS)
       u32 val = 0;
       if (mctrl & TIOCM_RTS)
           val |= RTS_BIT;
       if (mctrl & TIOCM_DTR)
           val |= DTR_BIT;
       writel(val, port->membase + MODEM_CTRL_REG);
   }
   
   static unsigned int my_uart_get_mctrl(struct uart_port *port) {
       // Get modem control lines (CTS, DSR, DCD, RI)
       u32 status = readl(port->membase + MODEM_STATUS_REG);
       unsigned int ret = 0;
       
       if (status & CTS_BIT)
           ret |= TIOCM_CTS;
       if (status & DSR_BIT)
           ret |= TIOCM_DSR;
       if (status & DCD_BIT)
           ret |= TIOCM_CAR;
       if (status & RI_BIT)
           ret |= TIOCM_RNG;
       
       return ret;
   }
   
   static void my_uart_start_tx(struct uart_port *port) {
       struct circ_buf *xmit = &port->state->xmit;
       
       while (!uart_circ_empty(xmit)) {
           if (readl(port->membase + STATUS_REG) & TX_FULL)
               break;
           
           writel(xmit->buf[xmit->tail], port->membase + TX_REG);
           xmit->tail = (xmit->tail + 1) & (UART_XMIT_SIZE - 1);
           port->icount.tx++;
       }
       
       if (uart_circ_empty(xmit))
           my_uart_stop_tx(port);
   }
   
   static void my_uart_stop_tx(struct uart_port *port) {
       u32 ier = readl(port->membase + IER_REG);
       writel(ier & ~TX_INT_ENABLE, port->membase + IER_REG);
   }
   
   static void my_uart_stop_rx(struct uart_port *port) {
       u32 ier = readl(port->membase + IER_REG);
       writel(ier & ~RX_INT_ENABLE, port->membase + IER_REG);
   }
   
   static int my_uart_startup(struct uart_port *port) {
       int ret;
       
       // Request IRQ
       ret = request_irq(port->irq, my_uart_interrupt, 0,
                         "my_uart", port);
       if (ret)
           return ret;
       
       // Enable RX/TX
       writel(RX_ENABLE | TX_ENABLE, port->membase + CTRL_REG);
       writel(RX_INT_ENABLE, port->membase + IER_REG);
       
       return 0;
   }
   
   static void my_uart_shutdown(struct uart_port *port) {
       free_irq(port->irq, port);
       writel(0, port->membase + CTRL_REG);
   }
   
   static void my_uart_set_termios(struct uart_port *port,
                                    struct ktermios *new,
                                    struct ktermios *old) {
       unsigned long flags;
       unsigned int baud, quot;
       
       baud = uart_get_baud_rate(port, new, old, 0, port->uartclk / 16);
       quot = uart_get_divisor(port, baud);
       
       spin_lock_irqsave(&port->lock, flags);
       
       // Set baud rate
       writel(quot, port->membase + BAUD_REG);
       
       // Set data bits, parity, stop bits
       u32 lcr = 0;
       switch (new->c_cflag & CSIZE) {
       case CS5: lcr |= DATA_5BIT; break;
       case CS6: lcr |= DATA_6BIT; break;
       case CS7: lcr |= DATA_7BIT; break;
       case CS8: lcr |= DATA_8BIT; break;
       }
       
       if (new->c_cflag & CSTOPB)
           lcr |= STOP_2BIT;
       if (new->c_cflag & PARENB)
           lcr |= PARITY_ENABLE;
       if (!(new->c_cflag & PARODD))
           lcr |= PARITY_EVEN;
       
       writel(lcr, port->membase + LCR_REG);
       
       uart_update_timeout(port, new->c_cflag, baud);
       spin_unlock_irqrestore(&port->lock, flags);
   }
   
   static const char *my_uart_type(struct uart_port *port) {
       return port->type == PORT_MY_UART ? "MY_UART" : NULL;
   }
   
   static void my_uart_config_port(struct uart_port *port, int flags) {
       if (flags & UART_CONFIG_TYPE) {
           port->type = PORT_MY_UART;
           my_uart_request_port(port);
       }
   }
   
   static int my_uart_request_port(struct uart_port *port) {
       return request_mem_region(port->mapbase, UART_REGION_SIZE,
                                 "my_uart") ? 0 : -EBUSY;
   }
   
   static void my_uart_release_port(struct uart_port *port) {
       release_mem_region(port->mapbase, UART_REGION_SIZE);
   }
   
   static struct uart_ops my_uart_ops = {
       .tx_empty     = my_uart_tx_empty,
       .set_mctrl    = my_uart_set_mctrl,
       .get_mctrl    = my_uart_get_mctrl,
       .stop_tx      = my_uart_stop_tx,
       .start_tx     = my_uart_start_tx,
       .stop_rx      = my_uart_stop_rx,
       .startup      = my_uart_startup,
       .shutdown     = my_uart_shutdown,
       .set_termios  = my_uart_set_termios,
       .type         = my_uart_type,
       .config_port  = my_uart_config_port,
       .request_port = my_uart_request_port,
       .release_port = my_uart_release_port,
   };
   
   // IRQ handler
   static irqreturn_t my_uart_interrupt(int irq, void *dev_id) {
       struct uart_port *port = dev_id;
       u32 status = readl(port->membase + ISR_REG);
       
       if (status & RX_INT) {
           while (!(readl(port->membase + STATUS_REG) & RX_EMPTY)) {
               u32 ch = readl(port->membase + RX_REG);
               port->icount.rx++;
               uart_insert_char(port, status, OE_BIT, ch, TTY_NORMAL);
           }
           tty_flip_buffer_push(&port->state->port);
       }
       
       if (status & TX_INT) {
           my_uart_start_tx(port);
       }
       
       return IRQ_HANDLED;
   }
   
   static struct uart_driver my_uart_driver = {
       .owner       = THIS_MODULE,
       .driver_name = "my_uart",
       .dev_name    = "ttyMY",
       .major       = MY_UART_MAJOR,
       .minor       = 0,
       .nr          = MY_UART_NR,
       .cons        = NULL,  // Console support (optional)
   };
   
   static int __init my_uart_init(void) {
       int ret;
       
       ret = uart_register_driver(&my_uart_driver);
       if (ret)
           return ret;
       
       // Register each port
       for (i = 0; i < MY_UART_NR; i++) {
           ret = uart_add_one_port(&my_uart_driver, &my_uart_ports[i]);
           if (ret) {
               uart_unregister_driver(&my_uart_driver);
               return ret;
           }
       }
       
       return 0;
   }
   
   static void __exit my_uart_exit(void) {
       for (i = 0; i < MY_UART_NR; i++)
           uart_remove_one_port(&my_uart_driver, &my_uart_ports[i]);
       uart_unregister_driver(&my_uart_driver);
   }

3.2 TTY Drivers
---------------

**TTY Driver Example:**

.. code-block:: c

   #include <linux/tty.h>
   #include <linux/tty_driver.h>
   #include <linux/tty_flip.h>
   
   #define MY_TTY_MINORS 4
   
   static struct tty_driver *my_tty_driver;
   
   static int my_tty_open(struct tty_struct *tty, struct file *file) {
       pr_info("TTY opened\n");
       return 0;
   }
   
   static void my_tty_close(struct tty_struct *tty, struct file *file) {
       pr_info("TTY closed\n");
   }
   
   static int my_tty_write(struct tty_struct *tty,
                            const unsigned char *buf, int count) {
       int i;
       
       for (i = 0; i < count; i++) {
           // Write to hardware
           write_char_to_hw(buf[i]);
       }
       
       return count;
   }
   
   static int my_tty_write_room(struct tty_struct *tty) {
       return 256;  // Available space in TX buffer
   }
   
   static int my_tty_chars_in_buffer(struct tty_struct *tty) {
       return 0;  // Number of chars in TX buffer
   }
   
   static void my_tty_set_termios(struct tty_struct *tty,
                                   struct ktermios *old) {
       // Handle termios changes
       u32 baud = tty_get_baud_rate(tty);
       pr_info("Baud rate: %u\n", baud);
   }
   
   static int my_tty_ioctl(struct tty_struct *tty,
                            unsigned int cmd, unsigned long arg) {
       switch (cmd) {
       case TIOCMGET:
           // Get modem status
           break;
       case TIOCMSET:
           // Set modem control
           break;
       default:
           return -ENOIOCTLCMD;
       }
       return 0;
   }
   
   static struct tty_operations my_tty_ops = {
       .open            = my_tty_open,
       .close           = my_tty_close,
       .write           = my_tty_write,
       .write_room      = my_tty_write_room,
       .chars_in_buffer = my_tty_chars_in_buffer,
       .set_termios     = my_tty_set_termios,
       .ioctl           = my_tty_ioctl,
   };
   
   static int __init my_tty_init(void) {
       my_tty_driver = tty_alloc_driver(MY_TTY_MINORS, 0);
       if (IS_ERR(my_tty_driver))
           return PTR_ERR(my_tty_driver);
       
       my_tty_driver->driver_name = "my_tty";
       my_tty_driver->name = "ttyMY";
       my_tty_driver->major = 0;  // Dynamic allocation
       my_tty_driver->minor_start = 0;
       my_tty_driver->type = TTY_DRIVER_TYPE_SERIAL;
       my_tty_driver->subtype = SERIAL_TYPE_NORMAL;
       my_tty_driver->init_termios = tty_std_termios;
       my_tty_driver->init_termios.c_cflag = B9600 | CS8 | CREAD | HUPCL | CLOCAL;
       
       tty_set_operations(my_tty_driver, &my_tty_ops);
       
       return tty_register_driver(my_tty_driver);
   }
   
   static void __exit my_tty_exit(void) {
       tty_unregister_driver(my_tty_driver);
       tty_driver_kref_put(my_tty_driver);
   }

**Sending Data to TTY:**

.. code-block:: c

   // From interrupt handler or elsewhere
   void receive_data_from_hw(struct tty_struct *tty) {
       char data[128];
       int len = read_from_hw(data, sizeof(data));
       
       // Push data to TTY layer
       tty_insert_flip_string(&tty->port, data, len);
       tty_flip_buffer_push(&tty->port);
   }

3.3 Line Disciplines
--------------------

**Line Discipline (LDISC) Example:**

.. code-block:: c

   #include <linux/tty.h>
   
   #define N_MY_LDISC 30  // Get a unique N_ number
   
   static int my_ldisc_open(struct tty_struct *tty) {
       pr_info("Line discipline opened\n");
       return 0;
   }
   
   static void my_ldisc_close(struct tty_struct *tty) {
       pr_info("Line discipline closed\n");
   }
   
   static ssize_t my_ldisc_read(struct tty_struct *tty, struct file *file,
                                 unsigned char __user *buf, size_t count) {
       // Read from TTY, process, return to userspace
       return 0;
   }
   
   static ssize_t my_ldisc_write(struct tty_struct *tty, struct file *file,
                                  const unsigned char *buf, size_t count) {
       // Get data from userspace, process, send to TTY
       return count;
   }
   
   static void my_ldisc_receive_buf(struct tty_struct *tty,
                                     const unsigned char *cp,
                                     const char *fp, int count) {
       // Process received data from TTY driver
       int i;
       for (i = 0; i < count; i++) {
           // Process each character
           process_char(cp[i]);
       }
   }
   
   static struct tty_ldisc_ops my_ldisc = {
       .magic          = TTY_LDISC_MAGIC,
       .name           = "my_ldisc",
       .num            = N_MY_LDISC,
       .open           = my_ldisc_open,
       .close          = my_ldisc_close,
       .read           = my_ldisc_read,
       .write          = my_ldisc_write,
       .receive_buf    = my_ldisc_receive_buf,
   };
   
   static int __init my_ldisc_init(void) {
       return tty_register_ldisc(N_MY_LDISC, &my_ldisc);
   }
   
   static void __exit my_ldisc_exit(void) {
       tty_unregister_ldisc(N_MY_LDISC);
   }

**Userspace Usage:**

.. code-block:: c

   // Set line discipline from userspace
   int fd = open("/dev/ttyS0", O_RDWR);
   int ldisc = N_MY_LDISC;
   ioctl(fd, TIOCSETD, &ldisc);

================================================================================
4. Input Subsystem Drivers
================================================================================

4.1 Input Device Framework
---------------------------

**Input Device Registration:**

.. code-block:: c

   #include <linux/input.h>
   
   struct my_input_dev {
       struct input_dev *input;
       void __iomem *base;
       int irq;
   };
   
   static irqreturn_t my_input_irq(int irq, void *dev_id) {
       struct my_input_dev *mydev = dev_id;
       u32 key_status = readl(mydev->base + KEY_STATUS_REG);
       
       // Report key press/release
       if (key_status & KEY_1_PRESSED) {
           input_report_key(mydev->input, KEY_1, 1);  // Pressed
           input_sync(mydev->input);
       }
       if (key_status & KEY_1_RELEASED) {
           input_report_key(mydev->input, KEY_1, 0);  // Released
           input_sync(mydev->input);
       }
       
       return IRQ_HANDLED;
   }
   
   static int my_input_probe(struct platform_device *pdev) {
       struct my_input_dev *mydev;
       int ret;
       
       mydev = devm_kzalloc(&pdev->dev, sizeof(*mydev), GFP_KERNEL);
       if (!mydev)
           return -ENOMEM;
       
       // Allocate input device
       mydev->input = devm_input_allocate_device(&pdev->dev);
       if (!mydev->input)
           return -ENOMEM;
       
       // Set input device properties
       mydev->input->name = "My Input Device";
       mydev->input->id.bustype = BUS_HOST;
       mydev->input->id.vendor  = 0x0001;
       mydev->input->id.product = 0x0001;
       mydev->input->id.version = 0x0100;
       
       // Declare supported events
       __set_bit(EV_KEY, mydev->input->evbit);
       __set_bit(KEY_1, mydev->input->keybit);
       __set_bit(KEY_2, mydev->input->keybit);
       __set_bit(KEY_ESC, mydev->input->keybit);
       
       // Get resources
       mydev->base = devm_platform_ioremap_resource(pdev, 0);
       if (IS_ERR(mydev->base))
           return PTR_ERR(mydev->base);
       
       mydev->irq = platform_get_irq(pdev, 0);
       ret = devm_request_irq(&pdev->dev, mydev->irq, my_input_irq,
                              0, "my_input", mydev);
       if (ret)
           return ret;
       
       // Register input device
       ret = input_register_device(mydev->input);
       if (ret)
           return ret;
       
       platform_set_drvdata(pdev, mydev);
       return 0;
   }
   
   static int my_input_remove(struct platform_device *pdev) {
       struct my_input_dev *mydev = platform_get_drvdata(pdev);
       input_unregister_device(mydev->input);
       return 0;
   }

4.2 Keyboard Driver
-------------------

**Keyboard Input Driver:**

.. code-block:: c

   static int keyboard_probe(struct platform_device *pdev) {
       struct input_dev *input;
       int i, ret;
       
       input = devm_input_allocate_device(&pdev->dev);
       if (!input)
           return -ENOMEM;
       
       input->name = "My Keyboard";
       input->id.bustype = BUS_HOST;
       
       // Set as keyboard
       __set_bit(EV_KEY, input->evbit);
       __set_bit(EV_REP, input->evbit);  // Auto-repeat
       
       // Set all keyboard keys
       for (i = 0; i < 128; i++)
           __set_bit(i, input->keybit);
       
       ret = input_register_device(input);
       if (ret)
           return ret;
       
       return 0;
   }
   
   // Report key events
   void report_key_event(struct input_dev *input, unsigned int keycode, int value) {
       input_event(input, EV_KEY, keycode, value);  // value: 1=press, 0=release
       input_sync(input);
   }

4.3 Mouse/Touchpad Driver
-------------------------

**Mouse Input Driver:**

.. code-block:: c

   static int mouse_probe(struct platform_device *pdev) {
       struct input_dev *input;
       int ret;
       
       input = devm_input_allocate_device(&pdev->dev);
       if (!input)
           return -ENOMEM;
       
       input->name = "My Mouse";
       input->id.bustype = BUS_HOST;
       
       // Set mouse capabilities
       __set_bit(EV_KEY, input->evbit);
       __set_bit(EV_REL, input->evbit);  // Relative movement
       
       // Mouse buttons
       __set_bit(BTN_LEFT, input->keybit);
       __set_bit(BTN_RIGHT, input->keybit);
       __set_bit(BTN_MIDDLE, input->keybit);
       
       // Relative axes
       __set_bit(REL_X, input->relbit);
       __set_bit(REL_Y, input->relbit);
       __set_bit(REL_WHEEL, input->relbit);
       
       ret = input_register_device(input);
       if (ret)
           return ret;
       
       return 0;
   }
   
   // Report mouse movement
   void report_mouse_movement(struct input_dev *input, int dx, int dy) {
       input_report_rel(input, REL_X, dx);
       input_report_rel(input, REL_Y, dy);
       input_sync(input);
   }
   
   // Report button click
   void report_mouse_button(struct input_dev *input, unsigned int button, int pressed) {
       input_report_key(input, button, pressed);
       input_sync(input);
   }

4.4 Touchscreen Driver
----------------------

**Touchscreen Input Driver:**

.. code-block:: c

   static int touchscreen_probe(struct platform_device *pdev) {
       struct input_dev *input;
       int ret;
       
       input = devm_input_allocate_device(&pdev->dev);
       if (!input)
           return -ENOMEM;
       
       input->name = "My Touchscreen";
       input->id.bustype = BUS_I2C;
       
       // Set touchscreen capabilities
       __set_bit(EV_KEY, input->evbit);
       __set_bit(EV_ABS, input->evbit);  // Absolute position
       
       __set_bit(BTN_TOUCH, input->keybit);
       
       // Set absolute axes with min/max values
       input_set_abs_params(input, ABS_X, 0, 1023, 0, 0);
       input_set_abs_params(input, ABS_Y, 0, 767, 0, 0);
       input_set_abs_params(input, ABS_PRESSURE, 0, 255, 0, 0);
       
       ret = input_register_device(input);
       if (ret)
           return ret;
       
       return 0;
   }
   
   // Report touch event
   void report_touch_event(struct input_dev *input, int x, int y, int pressure) {
       if (pressure > 0) {
           input_report_key(input, BTN_TOUCH, 1);
           input_report_abs(input, ABS_X, x);
           input_report_abs(input, ABS_Y, y);
           input_report_abs(input, ABS_PRESSURE, pressure);
       } else {
           input_report_key(input, BTN_TOUCH, 0);
       }
       input_sync(input);
   }

4.5 Multi-Touch Protocol
-------------------------

**Multi-Touch Touchscreen:**

.. code-block:: c

   static int multitouch_probe(struct platform_device *pdev) {
       struct input_dev *input;
       int ret;
       
       input = devm_input_allocate_device(&pdev->dev);
       if (!input)
           return -ENOMEM;
       
       input->name = "Multi-Touch Screen";
       
       // Multi-touch capabilities
       __set_bit(EV_ABS, input->evbit);
       __set_bit(EV_KEY, input->evbit);
       __set_bit(BTN_TOUCH, input->keybit);
       
       // MT Protocol B (tracking IDs)
       input_mt_init_slots(input, 10, 0);  // Up to 10 simultaneous touches
       
       input_set_abs_params(input, ABS_MT_POSITION_X, 0, 1920, 0, 0);
       input_set_abs_params(input, ABS_MT_POSITION_Y, 0, 1080, 0, 0);
       input_set_abs_params(input, ABS_MT_PRESSURE, 0, 255, 0, 0);
       
       ret = input_register_device(input);
       if (ret)
           return ret;
       
       return 0;
   }
   
   // Report multi-touch events (Protocol B)
   void report_multitouch(struct input_dev *input) {
       int i;
       struct touch_point {
           int id, x, y, pressure;
       } touches[10];
       
       int num_touches = get_touches_from_hw(touches, 10);
       
       for (i = 0; i < num_touches; i++) {
           input_mt_slot(input, touches[i].id);
           input_mt_report_slot_state(input, MT_TOOL_FINGER, true);
           input_report_abs(input, ABS_MT_POSITION_X, touches[i].x);
           input_report_abs(input, ABS_MT_POSITION_Y, touches[i].y);
           input_report_abs(input, ABS_MT_PRESSURE, touches[i].pressure);
       }
       
       input_mt_sync_frame(input);
       input_sync(input);
   }


================================================================================
5. I2C and SPI Drivers (Bus Drivers)
================================================================================

**Note:** See existing Embedded_Device_Drivers.rst for detailed I2C/SPI sections.
Quick reference provided here.

5.1 I2C Driver Quick Reference
-------------------------------

.. code-block:: c

   // Minimal I2C driver
   static struct i2c_driver my_driver = {
       .driver = {
           .name = "mydev",
           .of_match_table = my_of_match,
       },
       .probe = my_probe,
       .remove = my_remove,
       .id_table = my_id,
   };
   module_i2c_driver(my_driver);
   
   // I2C transfer
   i2c_smbus_read_byte_data(client, reg);
   i2c_smbus_write_byte_data(client, reg, val);

5.2 SPI Driver Quick Reference
-------------------------------

.. code-block:: c

   // Minimal SPI driver
   static struct spi_driver my_driver = {
       .driver.name = "mydev",
       .probe = my_probe,
       .remove = my_remove,
   };
   module_spi_driver(my_driver);
   
   // SPI transfer
   spi_write_then_read(spi, tx_buf, 2, rx_buf, 2);

================================================================================
6. Platform Drivers
================================================================================

**Note:** See existing Embedded_Device_Drivers.rst for detailed platform driver section.

.. code-block:: c

   // Minimal platform driver
   static struct platform_driver my_pdrv = {
       .probe = my_probe,
       .remove = my_remove,
       .driver = {
           .name = "mydev",
           .of_match_table = my_of_match,
       },
   };
   module_platform_driver(my_pdrv);

================================================================================
7. PCI/PCIe Drivers
================================================================================

7.1 PCI Driver Registration
----------------------------

**PCI Driver Structure:**

.. code-block:: c

   #include <linux/pci.h>
   
   static const struct pci_device_id my_pci_ids[] = {
       { PCI_DEVICE(VENDOR_ID, DEVICE_ID) },
       { PCI_DEVICE(VENDOR_ID, DEVICE_ID2) },
       { 0, }  // Terminator
   };
   MODULE_DEVICE_TABLE(pci, my_pci_ids);
   
   static int my_pci_probe(struct pci_dev *pdev,
                           const struct pci_device_id *id) {
       int ret;
       
       dev_info(&pdev->dev, "Probing PCI device\n");
       
       // Enable PCI device
       ret = pci_enable_device(pdev);
       if (ret)
           return ret;
       
       // Request PCI regions
       ret = pci_request_regions(pdev, "my_driver");
       if (ret)
           goto err_disable;
       
       // Set DMA mask
       ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(64));
       if (ret)
           goto err_release;
       
       // Enable bus mastering
       pci_set_master(pdev);
       
       // Read BAR addresses
       unsigned long mmio_start = pci_resource_start(pdev, 0);
       unsigned long mmio_len = pci_resource_len(pdev, 0);
       
       void __iomem *base = pci_iomap(pdev, 0, mmio_len);
       if (!base) {
           ret = -ENOMEM;
           goto err_release;
       }
       
       // Save private data
       pci_set_drvdata(pdev, base);
       
       // Request MSI/MSI-X interrupts
       ret = pci_alloc_irq_vectors(pdev, 1, 1, PCI_IRQ_MSI | PCI_IRQ_MSIX);
       if (ret < 0)
           goto err_iounmap;
       
       int irq = pci_irq_vector(pdev, 0);
       ret = request_irq(irq, my_irq_handler, 0, "my_driver", pdev);
       if (ret)
           goto err_free_irq_vectors;
       
       dev_info(&pdev->dev, "PCI device initialized\n");
       return 0;
   
   err_free_irq_vectors:
       pci_free_irq_vectors(pdev);
   err_iounmap:
       pci_iounmap(pdev, base);
   err_release:
       pci_release_regions(pdev);
   err_disable:
       pci_disable_device(pdev);
       return ret;
   }
   
   static void my_pci_remove(struct pci_dev *pdev) {
       void __iomem *base = pci_get_drvdata(pdev);
       int irq = pci_irq_vector(pdev, 0);
       
       free_irq(irq, pdev);
       pci_free_irq_vectors(pdev);
       pci_iounmap(pdev, base);
       pci_release_regions(pdev);
       pci_disable_device(pdev);
   }
   
   static struct pci_driver my_pci_driver = {
       .name = "my_pci_driver",
       .id_table = my_pci_ids,
       .probe = my_pci_probe,
       .remove = my_pci_remove,
   };
   module_pci_driver(my_pci_driver);

7.2 PCI Configuration Space
----------------------------

.. code-block:: c

   // Read/write PCI config space
   u16 vendor, device;
   pci_read_config_word(pdev, PCI_VENDOR_ID, &vendor);
   pci_read_config_word(pdev, PCI_DEVICE_ID, &device);
   
   u8 lat;
   pci_read_config_byte(pdev, PCI_LATENCY_TIMER, &lat);
   pci_write_config_byte(pdev, PCI_LATENCY_TIMER, 32);

================================================================================
8. USB Drivers
================================================================================

8.1 USB Driver Framework
-------------------------

**USB Driver Structure:**

.. code-block:: c

   #include <linux/usb.h>
   
   static const struct usb_device_id my_usb_table[] = {
       { USB_DEVICE(VENDOR_ID, PRODUCT_ID) },
       { }  // Terminator
   };
   MODULE_DEVICE_TABLE(usb, my_usb_table);
   
   static int my_usb_probe(struct usb_interface *intf,
                           const struct usb_device_id *id) {
       struct usb_device *udev = interface_to_usbdev(intf);
       struct usb_host_interface *iface_desc;
       struct usb_endpoint_descriptor *endpoint;
       int i;
       
       dev_info(&intf->dev, "USB device plugged\n");
       dev_info(&intf->dev, "ID: %04X:%04X\n",
                le16_to_cpu(udev->descriptor.idVendor),
                le16_to_cpu(udev->descriptor.idProduct));
       
       // Get interface descriptor
       iface_desc = intf->cur_altsetting;
       dev_info(&intf->dev, "Interface %d endpoints: %d\n",
                iface_desc->desc.bInterfaceNumber,
                iface_desc->desc.bNumEndpoints);
       
       // Iterate endpoints
       for (i = 0; i < iface_desc->desc.bNumEndpoints; i++) {
           endpoint = &iface_desc->endpoint[i].desc;
           dev_info(&intf->dev, "EP %d: addr=0x%02X type=%d\n",
                    i, endpoint->bEndpointAddress,
                    endpoint->bmAttributes & USB_ENDPOINT_XFERTYPE_MASK);
       }
       
       return 0;
   }
   
   static void my_usb_disconnect(struct usb_interface *intf) {
       dev_info(&intf->dev, "USB device unplugged\n");
   }
   
   static struct usb_driver my_usb_driver = {
       .name = "my_usb_driver",
       .id_table = my_usb_table,
       .probe = my_usb_probe,
       .disconnect = my_usb_disconnect,
   };
   module_usb_driver(my_usb_driver);

8.2 USB URBs (USB Request Blocks)
----------------------------------

**URB Operations:**

.. code-block:: c

   #include <linux/usb.h>
   
   // Allocate URB
   struct urb *urb = usb_alloc_urb(0, GFP_KERNEL);
   if (!urb)
       return -ENOMEM;
   
   // Fill bulk URB
   unsigned int pipe = usb_rcvbulkpipe(udev, endpoint_addr);
   usb_fill_bulk_urb(urb, udev, pipe, buffer, length,
                     my_complete_callback, context);
   
   // Submit URB
   ret = usb_submit_urb(urb, GFP_KERNEL);
   
   // Completion callback
   static void my_complete_callback(struct urb *urb) {
       if (urb->status) {
           pr_err("URB failed: %d\n", urb->status);
           return;
       }
       
       pr_info("Transferred %d bytes\n", urb->actual_length);
       // Process data in urb->transfer_buffer
   }
   
   // Control transfer (synchronous)
   ret = usb_control_msg(udev,
                         usb_rcvctrlpipe(udev, 0),
                         request,
                         requesttype,
                         value,
                         index,
                         data,
                         size,
                         timeout);
   
   // Bulk transfer (synchronous)
   int actual_length;
   ret = usb_bulk_msg(udev,
                      usb_rcvbulkpipe(udev, endpoint),
                      buffer,
                      length,
                      &actual_length,
                      timeout);

================================================================================
9. PCMCIA/CardBus Drivers
================================================================================

**PCMCIA Driver Example:**

.. code-block:: c

   #include <pcmcia/cistpl.h>
   #include <pcmcia/ds.h>
   
   static const struct pcmcia_device_id my_pcmcia_ids[] = {
       PCMCIA_DEVICE_MANF_CARD(0x0000, 0x0000),
       PCMCIA_DEVICE_NULL,
   };
   MODULE_DEVICE_TABLE(pcmcia, my_pcmcia_ids);
   
   static int my_pcmcia_probe(struct pcmcia_device *link) {
       dev_info(&link->dev, "PCMCIA card inserted\n");
       
       link->config_flags |= CONF_ENABLE_IRQ | CONF_AUTO_SET_IO;
       link->config_index = 1;
       
       return pcmcia_enable_device(link);
   }
   
   static void my_pcmcia_remove(struct pcmcia_device *link) {
       pcmcia_disable_device(link);
   }
   
   static struct pcmcia_driver my_pcmcia_driver = {
       .name = "my_pcmcia",
       .probe = my_pcmcia_probe,
       .remove = my_pcmcia_remove,
       .id_table = my_pcmcia_ids,
   };
   module_pcmcia_driver(my_pcmcia_driver);

================================================================================
10. Block Device Drivers
================================================================================

10.1 Block Driver Framework
----------------------------

**Block Device Driver:**

.. code-block:: c

   #include <linux/blkdev.h>
   #include <linux/blk-mq.h>
   #include <linux/hdreg.h>
   
   #define SECTOR_SIZE 512
   #define NSECTORS 1024
   
   struct my_block_dev {
       struct gendisk *gd;
       struct blk_mq_tag_set tag_set;
       u8 *data;  // RAM disk
   };
   
   static blk_status_t my_queue_rq(struct blk_mq_hw_ctx *hctx,
                                    const struct blk_mq_queue_data *bd) {
       struct request *req = bd->rq;
       struct my_block_dev *dev = req->q->queuedata;
       struct bio_vec bvec;
       struct req_iterator iter;
       sector_t pos = blk_rq_pos(req);
       void *buffer;
       
       blk_mq_start_request(req);
       
       // Process each segment
       rq_for_each_segment(bvec, req, iter) {
           size_t len = bvec.bv_len;
           buffer = page_address(bvec.bv_page) + bvec.bv_offset;
           
           if (rq_data_dir(req) == WRITE)
               memcpy(dev->data + pos * SECTOR_SIZE, buffer, len);
           else
               memcpy(buffer, dev->data + pos * SECTOR_SIZE, len);
           
           pos += len / SECTOR_SIZE;
       }
       
       blk_mq_end_request(req, BLK_STS_OK);
       return BLK_STS_OK;
   }
   
   static int my_getgeo(struct block_device *bdev, struct hd_geometry *geo) {
       geo->heads = 4;
       geo->sectors = 16;
       geo->cylinders = NSECTORS / (geo->heads * geo->sectors);
       return 0;
   }
   
   static const struct block_device_operations my_fops = {
       .owner = THIS_MODULE,
       .getgeo = my_getgeo,
   };
   
   static struct blk_mq_ops my_mq_ops = {
       .queue_rq = my_queue_rq,
   };
   
   static int __init my_block_init(void) {
       struct my_block_dev *dev;
       int ret;
       
       dev = kzalloc(sizeof(struct my_block_dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       // Allocate data storage
       dev->data = vzalloc(NSECTORS * SECTOR_SIZE);
       if (!dev->data) {
           kfree(dev);
           return -ENOMEM;
       }
       
       // Set up tag set
       dev->tag_set.ops = &my_mq_ops;
       dev->tag_set.nr_hw_queues = 1;
       dev->tag_set.queue_depth = 128;
       dev->tag_set.numa_node = NUMA_NO_NODE;
       dev->tag_set.cmd_size = 0;
       dev->tag_set.flags = BLK_MQ_F_SHOULD_MERGE;
       
       ret = blk_mq_alloc_tag_set(&dev->tag_set);
       if (ret)
           goto err_data;
       
       // Allocate disk
       dev->gd = blk_mq_alloc_disk(&dev->tag_set, dev);
       if (IS_ERR(dev->gd)) {
           ret = PTR_ERR(dev->gd);
           goto err_tagset;
       }
       
       dev->gd->major = 0;  // Dynamic
       dev->gd->first_minor = 0;
       dev->gd->minors = 1;
       dev->gd->fops = &my_fops;
       dev->gd->private_data = dev;
       strcpy(dev->gd->disk_name, "myblkdev");
       set_capacity(dev->gd, NSECTORS);
       
       // Add disk
       ret = add_disk(dev->gd);
       if (ret)
           goto err_disk;
       
       pr_info("Block device registered\n");
       return 0;
   
   err_disk:
       blk_cleanup_disk(dev->gd);
   err_tagset:
       blk_mq_free_tag_set(&dev->tag_set);
   err_data:
       vfree(dev->data);
       kfree(dev);
       return ret;
   }

================================================================================
11. Network Device Drivers
================================================================================

11.1 Network Driver Framework
------------------------------

**Network Device Driver:**

.. code-block:: c

   #include <linux/netdevice.h>
   #include <linux/etherdevice.h>
   #include <linux/skbuff.h>
   
   struct my_net_priv {
       struct net_device *ndev;
       struct napi_struct napi;
       void __iomem *base;
       int irq;
   };
   
   static int my_net_open(struct net_device *ndev) {
       struct my_net_priv *priv = netdev_priv(ndev);
       
       // Request IRQ
       request_irq(priv->irq, my_net_interrupt, 0, ndev->name, ndev);
       
       // Enable NAPI
       napi_enable(&priv->napi);
       
       // Start hardware
       writel(ENABLE_BIT, priv->base + CTRL_REG);
       
       netif_start_queue(ndev);
       return 0;
   }
   
   static int my_net_stop(struct net_device *ndev) {
       struct my_net_priv *priv = netdev_priv(ndev);
       
       netif_stop_queue(ndev);
       napi_disable(&priv->napi);
       free_irq(priv->irq, ndev);
       writel(0, priv->base + CTRL_REG);
       
       return 0;
   }
   
   static netdev_tx_t my_net_start_xmit(struct sk_buff *skb,
                                         struct net_device *ndev) {
       struct my_net_priv *priv = netdev_priv(ndev);
       
       // Check if TX queue full
       if (tx_queue_full(priv)) {
           netif_stop_queue(ndev);
           return NETDEV_TX_BUSY;
       }
       
       // Write packet to hardware
       write_packet_to_hw(priv, skb->data, skb->len);
       
       // Update statistics
       ndev->stats.tx_packets++;
       ndev->stats.tx_bytes += skb->len;
       
       dev_kfree_skb(skb);
       return NETDEV_TX_OK;
   }
   
   static int my_net_poll(struct napi_struct *napi, int budget) {
       struct my_net_priv *priv = container_of(napi, struct my_net_priv, napi);
       struct net_device *ndev = priv->ndev;
       int work_done = 0;
       
       while (work_done < budget && has_rx_packet(priv)) {
           struct sk_buff *skb = netdev_alloc_skb(ndev, 1600);
           if (!skb)
               break;
           
           // Read packet from hardware
           int len = read_packet_from_hw(priv, skb->data);
           skb_put(skb, len);
           skb->protocol = eth_type_trans(skb, ndev);
           
           // Pass to network stack
           netif_receive_skb(skb);
           
           ndev->stats.rx_packets++;
           ndev->stats.rx_bytes += len;
           work_done++;
       }
       
       if (work_done < budget) {
           napi_complete(napi);
           // Re-enable interrupts
           enable_rx_interrupt(priv);
       }
       
       return work_done;
   }
   
   static irqreturn_t my_net_interrupt(int irq, void *dev_id) {
       struct net_device *ndev = dev_id;
       struct my_net_priv *priv = netdev_priv(ndev);
       u32 status = readl(priv->base + INT_STATUS_REG);
       
       if (status & RX_INT) {
           // Disable RX interrupt
           disable_rx_interrupt(priv);
           // Schedule NAPI poll
           napi_schedule(&priv->napi);
       }
       
       if (status & TX_INT) {
           // TX complete
           netif_wake_queue(ndev);
       }
       
       return IRQ_HANDLED;
   }
   
   static const struct net_device_ops my_netdev_ops = {
       .ndo_open = my_net_open,
       .ndo_stop = my_net_stop,
       .ndo_start_xmit = my_net_start_xmit,
   };
   
   static int my_net_probe(struct platform_device *pdev) {
       struct net_device *ndev;
       struct my_net_priv *priv;
       int ret;
       
       // Allocate ethernet device
       ndev = alloc_etherdev(sizeof(struct my_net_priv));
       if (!ndev)
           return -ENOMEM;
       
       priv = netdev_priv(ndev);
       priv->ndev = ndev;
       
       // Get resources
       priv->base = devm_platform_ioremap_resource(pdev, 0);
       if (IS_ERR(priv->base)) {
           ret = PTR_ERR(priv->base);
           goto err_free;
       }
       
       priv->irq = platform_get_irq(pdev, 0);
       
       // Set MAC address
       eth_hw_addr_random(ndev);
       
       // Set operations
       ndev->netdev_ops = &my_netdev_ops;
       ndev->watchdog_timeo = 5 * HZ;
       
       // Initialize NAPI
       netif_napi_add(ndev, &priv->napi, my_net_poll, 64);
       
       // Register network device
       ret = register_netdev(ndev);
       if (ret)
           goto err_free;
       
       platform_set_drvdata(pdev, ndev);
       return 0;
   
   err_free:
       free_netdev(ndev);
       return ret;
   }

================================================================================
12. Wireless Drivers (WiFi/Bluetooth/IrDA)
================================================================================

12.1 WiFi Driver (cfg80211/mac80211)
-------------------------------------

**WiFi Driver Example:**

.. code-block:: c

   #include <net/cfg80211.h>
   #include <net/mac80211.h>
   
   static struct ieee80211_ops my_wifi_ops = {
       .tx = my_wifi_tx,
       .start = my_wifi_start,
       .stop = my_wifi_stop,
       .add_interface = my_wifi_add_interface,
       .remove_interface = my_wifi_remove_interface,
       .config = my_wifi_config,
       .configure_filter = my_wifi_configure_filter,
   };
   
   static int my_wifi_probe(struct platform_device *pdev) {
       struct ieee80211_hw *hw;
       int ret;
       
       // Allocate hardware structure
       hw = ieee80211_alloc_hw(sizeof(struct my_wifi_priv), &my_wifi_ops);
       if (!hw)
           return -ENOMEM;
       
       // Set hardware capabilities
       hw->flags = IEEE80211_HW_SIGNAL_DBM |
                   IEEE80211_HW_SUPPORTS_PS;
       hw->wiphy->interface_modes = BIT(NL80211_IFTYPE_STATION) |
                                    BIT(NL80211_IFTYPE_AP);
       
       // Set supported bands
       hw->wiphy->bands[NL80211_BAND_2GHZ] = &my_band_2ghz;
       
       // Register with mac80211
       ret = ieee80211_register_hw(hw);
       if (ret) {
           ieee80211_free_hw(hw);
           return ret;
       }
       
       return 0;
   }

12.2 Bluetooth Driver
---------------------

**Bluetooth HCI Driver:**

.. code-block:: c

   #include <net/bluetooth/bluetooth.h>
   #include <net/bluetooth/hci_core.h>
   
   static int my_bt_open(struct hci_dev *hdev) {
       // Initialize hardware
       return 0;
   }
   
   static int my_bt_close(struct hci_dev *hdev) {
       // Shutdown hardware
       return 0;
   }
   
   static int my_bt_send(struct hci_dev *hdev, struct sk_buff *skb) {
       // Send to hardware
       kfree_skb(skb);
       return 0;
   }
   
   static int my_bt_probe(struct platform_device *pdev) {
       struct hci_dev *hdev;
       
       // Allocate HCI device
       hdev = hci_alloc_dev();
       if (!hdev)
           return -ENOMEM;
       
       hdev->bus = HCI_UART;
       hdev->open = my_bt_open;
       hdev->close = my_bt_close;
       hdev->send = my_bt_send;
       
       // Register HCI device
       if (hci_register_dev(hdev) < 0) {
           hci_free_dev(hdev);
           return -ENODEV;
       }
       
       return 0;
   }

================================================================================
13. MTD (Flash Memory) Drivers
================================================================================

**MTD Driver Example:**

.. code-block:: c

   #include <linux/mtd/mtd.h>
   #include <linux/mtd/partitions.h>
   
   static int my_mtd_read(struct mtd_info *mtd, loff_t from, size_t len,
                          size_t *retlen, u_char *buf) {
       // Read from flash
       *retlen = len;
       return 0;
   }
   
   static int my_mtd_write(struct mtd_info *mtd, loff_t to, size_t len,
                           size_t *retlen, const u_char *buf) {
       // Write to flash
       *retlen = len;
       return 0;
   }
   
   static int my_mtd_erase(struct mtd_info *mtd, struct erase_info *instr) {
       // Erase flash sector
       return 0;
   }
   
   static int my_mtd_probe(struct platform_device *pdev) {
       struct mtd_info *mtd;
       
       mtd = devm_kzalloc(&pdev->dev, sizeof(*mtd), GFP_KERNEL);
       if (!mtd)
           return -ENOMEM;
       
       mtd->name = "my_flash";
       mtd->type = MTD_NORFLASH;
       mtd->flags = MTD_CAP_NORFLASH;
       mtd->size = 0x1000000;  // 16MB
       mtd->erasesize = 0x10000;  // 64KB
       mtd->writesize = 1;
       mtd->_read = my_mtd_read;
       mtd->_write = my_mtd_write;
       mtd->_erase = my_mtd_erase;
       
       return mtd_device_register(mtd, NULL, 0);
   }

================================================================================
14. Video Drivers (Framebuffer/V4L2)
================================================================================

14.1 Framebuffer Driver
------------------------

**Framebuffer Driver Example:**

.. code-block:: c

   #include <linux/fb.h>
   
   static struct fb_ops my_fb_ops = {
       .owner = THIS_MODULE,
       .fb_check_var = my_fb_check_var,
       .fb_set_par = my_fb_set_par,
       .fb_setcolreg = my_fb_setcolreg,
       .fb_fillrect = cfb_fillrect,
       .fb_copyarea = cfb_copyarea,
       .fb_imageblit = cfb_imageblit,
   };
   
   static int my_fb_probe(struct platform_device *pdev) {
       struct fb_info *info;
       int ret;
       
       info = framebuffer_alloc(sizeof(struct my_fb_par), &pdev->dev);
       if (!info)
           return -ENOMEM;
       
       info->fbops = &my_fb_ops;
       info->var.xres = 1920;
       info->var.yres = 1080;
       info->var.bits_per_pixel = 32;
       info->fix.line_length = 1920 * 4;
       info->fix.smem_len = 1920 * 1080 * 4;
       
       // Allocate framebuffer memory
       info->screen_base = dma_alloc_coherent(&pdev->dev,
                                              info->fix.smem_len,
                                              &info->fix.smem_start,
                                              GFP_KERNEL);
       if (!info->screen_base) {
           ret = -ENOMEM;
           goto err_free;
       }
       
       ret = register_framebuffer(info);
       if (ret)
           goto err_dma;
       
       return 0;
   
   err_dma:
       dma_free_coherent(&pdev->dev, info->fix.smem_len,
                         info->screen_base, info->fix.smem_start);
   err_free:
       framebuffer_release(info);
       return ret;
   }

14.2 V4L2 (Video4Linux2) Driver
--------------------------------

**V4L2 Camera Driver:**

.. code-block:: c

   #include <media/v4l2-device.h>
   #include <media/v4l2-ioctl.h>
   #include <media/videobuf2-vmalloc.h>
   
   static const struct v4l2_file_operations my_v4l2_fops = {
       .owner = THIS_MODULE,
       .open = v4l2_fh_open,
       .release = vb2_fop_release,
       .read = vb2_fop_read,
       .poll = vb2_fop_poll,
       .unlocked_ioctl = video_ioctl2,
       .mmap = vb2_fop_mmap,
   };
   
   static const struct v4l2_ioctl_ops my_v4l2_ioctl_ops = {
       .vidioc_querycap = my_querycap,
       .vidioc_enum_fmt_vid_cap = my_enum_fmt_vid_cap,
       .vidioc_g_fmt_vid_cap = my_g_fmt_vid_cap,
       .vidioc_s_fmt_vid_cap = my_s_fmt_vid_cap,
       .vidioc_reqbufs = vb2_ioctl_reqbufs,
       .vidioc_querybuf = vb2_ioctl_querybuf,
       .vidioc_qbuf = vb2_ioctl_qbuf,
       .vidioc_dqbuf = vb2_ioctl_dqbuf,
       .vidioc_streamon = vb2_ioctl_streamon,
       .vidioc_streamoff = vb2_ioctl_streamoff,
   };

================================================================================
15. Audio (ALSA) Drivers
================================================================================

**ALSA Driver Example:**

.. code-block:: c

   #include <sound/core.h>
   #include <sound/pcm.h>
   #include <sound/initval.h>
   
   static struct snd_pcm_ops my_pcm_ops = {
       .open = my_pcm_open,
       .close = my_pcm_close,
       .ioctl = snd_pcm_lib_ioctl,
       .hw_params = my_pcm_hw_params,
       .hw_free = my_pcm_hw_free,
       .prepare = my_pcm_prepare,
       .trigger = my_pcm_trigger,
       .pointer = my_pcm_pointer,
   };
   
   static int my_audio_probe(struct platform_device *pdev) {
       struct snd_card *card;
       struct snd_pcm *pcm;
       int ret;
       
       // Create sound card
       ret = snd_card_new(&pdev->dev, -1, "myaudio", THIS_MODULE,
                          0, &card);
       if (ret < 0)
           return ret;
       
       strcpy(card->driver, "My Audio");
       strcpy(card->shortname, "My Audio Card");
       strcpy(card->longname, "My Audio Sound Card");
       
       // Create PCM device
       ret = snd_pcm_new(card, "My PCM", 0, 1, 1, &pcm);
       if (ret < 0)
           goto err_free;
       
       pcm->private_data = card;
       strcpy(pcm->name, "My PCM");
       
       // Set PCM ops
       snd_pcm_set_ops(pcm, SNDRV_PCM_STREAM_PLAYBACK, &my_pcm_ops);
       snd_pcm_set_ops(pcm, SNDRV_PCM_STREAM_CAPTURE, &my_pcm_ops);
       
       // Register card
       ret = snd_card_register(card);
       if (ret)
           goto err_free;
       
       platform_set_drvdata(pdev, card);
       return 0;
   
   err_free:
       snd_card_free(card);
       return ret;
   }

================================================================================
16. Miscellaneous Drivers
================================================================================

16.1 RTC (Real-Time Clock)
---------------------------

.. code-block:: c

   #include <linux/rtc.h>
   
   static int my_rtc_read_time(struct device *dev, struct rtc_time *tm) {
       // Read time from hardware
       return 0;
   }
   
   static int my_rtc_set_time(struct device *dev, struct rtc_time *tm) {
       // Set time to hardware
       return 0;
   }
   
   static const struct rtc_class_ops my_rtc_ops = {
       .read_time = my_rtc_read_time,
       .set_time = my_rtc_set_time,
   };
   
   static int my_rtc_probe(struct platform_device *pdev) {
       struct rtc_device *rtc;
       
       rtc = devm_rtc_allocate_device(&pdev->dev);
       if (IS_ERR(rtc))
           return PTR_ERR(rtc);
       
       rtc->ops = &my_rtc_ops;
       
       return devm_rtc_register_device(rtc);
   }

16.2 Watchdog
-------------

.. code-block:: c

   #include <linux/watchdog.h>
   
   static int my_wdt_start(struct watchdog_device *wdd) {
       // Start watchdog
       return 0;
   }
   
   static int my_wdt_stop(struct watchdog_device *wdd) {
       // Stop watchdog
       return 0;
   }
   
   static int my_wdt_ping(struct watchdog_device *wdd) {
       // Ping/refresh watchdog
       return 0;
   }
   
   static const struct watchdog_ops my_wdt_ops = {
       .owner = THIS_MODULE,
       .start = my_wdt_start,
       .stop = my_wdt_stop,
       .ping = my_wdt_ping,
   };
   
   static const struct watchdog_info my_wdt_info = {
       .options = WDIOF_KEEPALIVEPING | WDIOF_MAGICCLOSE,
       .identity = "My Watchdog",
   };
   
   static struct watchdog_device my_wdt = {
       .info = &my_wdt_info,
       .ops = &my_wdt_ops,
       .timeout = 30,
   };

16.3 LED
--------

.. code-block:: c

   #include <linux/leds.h>
   
   static void my_led_brightness_set(struct led_classdev *led_cdev,
                                      enum led_brightness value) {
       // Set LED brightness (0-255)
       if (value)
           gpio_set_value(led_gpio, 1);
       else
           gpio_set_value(led_gpio, 0);
   }
   
   static struct led_classdev my_led = {
       .name = "my:green:status",
       .brightness_set = my_led_brightness_set,
       .max_brightness = 255,
   };
   
   static int my_led_probe(struct platform_device *pdev) {
       return devm_led_classdev_register(&pdev->dev, &my_led);
   }

16.4 PWM
--------

.. code-block:: c

   #include <linux/pwm.h>
   
   static int my_pwm_config(struct pwm_chip *chip, struct pwm_device *pwm,
                            int duty_ns, int period_ns) {
       // Configure PWM duty cycle and period
       return 0;
   }
   
   static int my_pwm_enable(struct pwm_chip *chip, struct pwm_device *pwm) {
       // Enable PWM output
       return 0;
   }
   
   static void my_pwm_disable(struct pwm_chip *chip, struct pwm_device *pwm) {
       // Disable PWM output
   }
   
   static const struct pwm_ops my_pwm_ops = {
       .config = my_pwm_config,
       .enable = my_pwm_enable,
       .disable = my_pwm_disable,
       .owner = THIS_MODULE,
   };
   
   static struct pwm_chip my_pwm_chip = {
       .ops = &my_pwm_ops,
       .npwm = 4,  // 4 PWM channels
   };

16.5 Regulator
--------------

.. code-block:: c

   #include <linux/regulator/driver.h>
   
   static int my_regulator_enable(struct regulator_dev *rdev) {
       // Enable regulator
       return 0;
   }
   
   static int my_regulator_disable(struct regulator_dev *rdev) {
       // Disable regulator
       return 0;
   }
   
   static int my_regulator_get_voltage(struct regulator_dev *rdev) {
       // Return voltage in microvolts
       return 3300000;  // 3.3V
   }
   
   static int my_regulator_set_voltage(struct regulator_dev *rdev,
                                       int min_uV, int max_uV,
                                       unsigned *selector) {
       // Set output voltage
       return 0;
   }
   
   static const struct regulator_ops my_regulator_ops = {
       .enable = my_regulator_enable,
       .disable = my_regulator_disable,
       .get_voltage = my_regulator_get_voltage,
       .set_voltage = my_regulator_set_voltage,
   };

16.6 GPIO Controller
--------------------

.. code-block:: c

   #include <linux/gpio/driver.h>
   
   static int my_gpio_get(struct gpio_chip *gc, unsigned offset) {
       // Read GPIO value
       return readl(base + GPIO_DATA_REG) & BIT(offset) ? 1 : 0;
   }
   
   static void my_gpio_set(struct gpio_chip *gc, unsigned offset, int value) {
       u32 reg = readl(base + GPIO_DATA_REG);
       if (value)
           reg |= BIT(offset);
       else
           reg &= ~BIT(offset);
       writel(reg, base + GPIO_DATA_REG);
   }
   
   static int my_gpio_direction_input(struct gpio_chip *gc, unsigned offset) {
       // Set GPIO as input
       return 0;
   }
   
   static int my_gpio_direction_output(struct gpio_chip *gc,
                                       unsigned offset, int value) {
       // Set GPIO as output
       my_gpio_set(gc, offset, value);
       return 0;
   }
   
   static struct gpio_chip my_gpio_chip = {
       .label = "my-gpio",
       .get = my_gpio_get,
       .set = my_gpio_set,
       .direction_input = my_gpio_direction_input,
       .direction_output = my_gpio_direction_output,
       .base = -1,  // Dynamic
       .ngpio = 32,  // 32 GPIO pins
   };

16.7 Hardware Monitor (Hwmon)
------------------------------

.. code-block:: c

   #include <linux/hwmon.h>
   
   static umode_t my_hwmon_is_visible(const void *data,
                                       enum hwmon_sensor_types type,
                                       u32 attr, int channel) {
       return 0444;  // Read-only
   }
   
   static int my_hwmon_read(struct device *dev,
                            enum hwmon_sensor_types type,
                            u32 attr, int channel, long *val) {
       switch (type) {
       case hwmon_temp:
           if (attr == hwmon_temp_input)
               *val = 25000;  // 25°C in millidegrees
           break;
       default:
           return -EOPNOTSUPP;
       }
       return 0;
   }
   
   static const struct hwmon_ops my_hwmon_ops = {
       .is_visible = my_hwmon_is_visible,
       .read = my_hwmon_read,
   };

================================================================================
17. Driver Development Workflow
================================================================================

17.1 Development Cycle
-----------------------

.. code-block:: bash

   # 1. Create driver source
   vim my_driver.c
   
   # 2. Create Makefile
   echo "obj-m := my_driver.o" > Makefile
   
   # 3. Build
   make -C /lib/modules/$(uname -r)/build M=$PWD modules
   
   # 4. Load
   sudo insmod my_driver.ko
   
   # 5. Check dmesg
   dmesg | tail
   
   # 6. Test driver
   ls /dev/mydevice
   echo "test" > /dev/mydevice
   cat /dev/mydevice
   
   # 7. Unload
   sudo rmmod my_driver
   
   # 8. Clean
   make -C /lib/modules/$(uname -r)/build M=$PWD clean

17.2 Driver Testing
-------------------

.. code-block:: bash

   # Check driver loaded
   lsmod | grep my_driver
   
   # View module info
   modinfo my_driver.ko
   
   # Check sysfs
   ls /sys/class/myclass/
   ls /sys/devices/platform/mydevice/
   
   # Check device nodes
   ls -l /dev/mydevice*
   
   # Monitor interrupts
   cat /proc/interrupts | grep mydevice
   
   # Check DMA
   cat /proc/dma

17.3 Common Issues
------------------

.. code-block:: text

   Issue: "insmod: ERROR: could not insert module"
   Solution: Check dmesg for error messages
   
   Issue: "Unknown symbol"
   Solution: Missing MODULE_LICENSE("GPL") or module dependencies
   
   Issue: "/dev/mydevice not created"
   Solution: Check udev rules, use device_create()
   
   Issue: "Kernel oops/panic"
   Solution: Check for NULL pointers, use pr_info() for debug

================================================================================
18. Driver Debugging Techniques
================================================================================

18.1 Printk Debugging
----------------------

.. code-block:: c

   // Basic printk
   printk(KERN_INFO "Value: %d\n", value);
   
   // Modern pr_* macros
   pr_info("Driver loaded\n");
   pr_err("Error occurred: %d\n", ret);
   pr_warn("Warning: low memory\n");
   pr_debug("Debug: value=%d\n", val);  // Only if DEBUG defined
   
   // Device-specific
   dev_info(&pdev->dev, "Device initialized\n");
   dev_err(&pdev->dev, "Failed to allocate: %d\n", ret);
   
   // Conditional compilation
   #ifdef DEBUG
   pr_info("Debug mode enabled\n");
   #endif

18.2 Dynamic Debug
-------------------

.. code-block:: bash

   # Enable debug for specific module
   echo 'module my_driver +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug for specific file
   echo 'file my_driver.c +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug for specific function
   echo 'func my_probe +p' > /sys/kernel/debug/dynamic_debug/control
   
   # View settings
   cat /sys/kernel/debug/dynamic_debug/control

18.3 ftrace
-----------

.. code-block:: bash

   # Enable function tracer
   echo function > /sys/kernel/debug/tracing/current_tracer
   
   # Filter specific functions
   echo my_driver_* > /sys/kernel/debug/tracing/set_ftrace_filter
   
   # Start tracing
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   
   # View trace
   cat /sys/kernel/debug/tracing/trace
   
   # Stop tracing
   echo 0 > /sys/kernel/debug/tracing/tracing_on

18.4 KGDB (Kernel Debugger)
----------------------------

.. code-block:: bash

   # Kernel command line
   kgdboc=ttyS0,115200 kgdbwait
   
   # On host (GDB)
   gdb vmlinux
   (gdb) target remote /dev/ttyS0
   (gdb) b my_driver_probe
   (gdb) c

================================================================================
19. Driver Reference Quick Tables
================================================================================

19.1 Driver Type Summary
-------------------------

.. code-block:: text

   Driver Type     | Main API              | Key Structure       | Use Case
   ================================================================================
   Character       | alloc_chrdev_region   | file_operations     | Serial, terminals
   Block           | blk_mq_alloc_disk     | block_device_ops    | Disks, flash
   Network         | register_netdev       | net_device_ops      | Ethernet, WiFi
   UART            | uart_register_driver  | uart_ops            | Serial ports
   Input           | input_register_device | input_dev           | Keyboards, mice
   I2C             | i2c_add_driver        | i2c_driver          | Sensors, EEPROMs
   SPI             | spi_register_driver   | spi_driver          | Flash, ADCs
   Platform        | platform_driver_reg   | platform_driver     | SoC peripherals
   PCI             | pci_register_driver   | pci_driver          | PCIe cards
   USB             | usb_register_driver   | usb_driver          | USB devices
   MTD             | mtd_device_register   | mtd_info            | Flash memory
   Framebuffer     | register_framebuffer  | fb_ops              | Display
   ALSA            | snd_card_new          | snd_pcm_ops         | Audio
   RTC             | rtc_register_device   | rtc_class_ops       | Clocks
   Watchdog        | watchdog_register_dev | watchdog_ops        | Watchdog timers
   LED             | led_classdev_register | led_classdev        | LEDs
   PWM             | pwm_chip_add          | pwm_ops             | PWM controllers
   Regulator       | regulator_register    | regulator_ops       | Voltage regs
   GPIO            | gpiochip_add_data     | gpio_chip           | GPIO controllers
   Hwmon           | hwmon_device_register | hwmon_ops           | Sensors

19.2 Common Header Files
-------------------------

.. code-block:: c

   // Module basics
   #include <linux/module.h>
   #include <linux/kernel.h>
   #include <linux/init.h>
   
   // Character devices
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/device.h>
   #include <linux/uaccess.h>
   
   // Platform drivers
   #include <linux/platform_device.h>
   #include <linux/of.h>
   #include <linux/of_device.h>
   
   // I/O and memory
   #include <linux/io.h>
   #include <linux/ioport.h>
   #include <linux/slab.h>
   
   // Interrupts
   #include <linux/interrupt.h>
   #include <linux/irq.h>
   
   // I2C
   #include <linux/i2c.h>
   #include <linux/regmap.h>
   
   // SPI
   #include <linux/spi/spi.h>
   
   // GPIO
   #include <linux/gpio/consumer.h>
   #include <linux/gpio/driver.h>
   
   // PCI
   #include <linux/pci.h>
   
   // USB
   #include <linux/usb.h>
   
   // Network
   #include <linux/netdevice.h>
   #include <linux/etherdevice.h>
   #include <linux/skbuff.h>
   
   // Block devices
   #include <linux/blkdev.h>
   #include <linux/blk-mq.h>
   
   // Input
   #include <linux/input.h>

19.3 Useful Kernel Functions
-----------------------------

.. code-block:: c

   // Memory allocation
   kmalloc(size, GFP_KERNEL);
   kzalloc(size, GFP_KERNEL);  // Zero-initialized
   vmalloc(size);  // Virtual memory
   devm_kzalloc(&dev, size, GFP_KERNEL);  // Managed
   
   // DMA
   dma_alloc_coherent(&dev, size, &dma_addr, GFP_KERNEL);
   dma_map_single(&dev, ptr, size, direction);
   
   // I/O memory
   ioremap(phys_addr, size);
   devm_ioremap(&dev, phys_addr, size);
   readl(addr);
   writel(val, addr);
   
   // Delay
   udelay(usecs);   // Busy wait (< 1ms)
   mdelay(msecs);   // Busy wait (milliseconds)
   msleep(msecs);   // Sleep (can't be used in atomic context)
   usleep_range(min, max);  // Sleep range
   
   // Timers
   timer_setup(&timer, callback, flags);
   mod_timer(&timer, jiffies + HZ);  // 1 second
   del_timer_sync(&timer);
   
   // Workqueues
   INIT_WORK(&work, work_func);
   schedule_work(&work);
   flush_work(&work);
   
   // Wait queues
   init_waitqueue_head(&wq);
   wait_event(wq, condition);
   wake_up(&wq);
   
   // Locking
   DEFINE_MUTEX(my_mutex);
   mutex_lock(&my_mutex);
   mutex_unlock(&my_mutex);
   
   DEFINE_SPINLOCK(my_spinlock);
   spin_lock(&my_spinlock);
   spin_unlock(&my_spinlock);
   spin_lock_irqsave(&lock, flags);
   spin_unlock_irqrestore(&lock, flags);

================================================================================
20. Conclusion and Best Practices
================================================================================

**Best Practices:**

1. **Use devm_* functions** for automatic resource cleanup
2. **Always check return values** from kernel functions
3. **Use proper locking** (mutexes for sleep, spinlocks for atomic context)
4. **Zero-initialize structures** to avoid random data
5. **Test error paths** - simulate failures
6. **Follow kernel coding style** - checkpatch.pl
7. **Document your code** - use kernel-doc format
8. **Use appropriate log levels** - don't spam dmesg
9. **Handle hotplug properly** - support device removal
10. **Test on multiple architectures** if possible

**Common Mistakes to Avoid:**

- Forgetting MODULE_LICENSE("GPL")
- Not handling NULL pointers
- Sleeping in atomic context
- Not freeing resources
- Hardcoding device numbers
- Ignoring return values
- Race conditions
- Buffer overflows

**Resources:**

- Linux Device Drivers (LDD3): https://lwn.net/Kernel/LDD3/
- Kernel documentation: Documentation/driver-api/
- Linux kernel source: https://kernel.org
- Mailing list: linux-kernel@vger.kernel.org

================================================================================
END OF COMPREHENSIVE LINUX DEVICE DRIVERS CATALOG
================================================================================

