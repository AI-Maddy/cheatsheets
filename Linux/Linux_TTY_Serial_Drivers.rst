=====================================
Linux TTY and Serial Drivers Guide
=====================================

:Author: Linux Device Driver Documentation
:Date: January 2026
:Version: 1.0
:Focus: TTY layer and serial port driver development

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Serial Commands
--------------------------

.. code-block:: bash

   # List serial ports
   ls -l /dev/ttyS*  # Standard serial
   ls -l /dev/ttyUSB*  # USB serial
   ls -l /dev/ttyACM*  # ACM (modem)
   
   # Serial port information
   setserial /dev/ttyS0 -a
   dmesg | grep tty
   
   # Configure serial port
   stty -F /dev/ttyS0 115200 cs8 -parenb -cstopb
   
   # Test serial port (loopback)
   stty -F /dev/ttyS0 raw -echo
   cat /dev/ttyS0 &
   echo "test" > /dev/ttyS0
   
   # Monitor serial traffic
   cat /dev/ttyS0

Quick Serial Port Access
-------------------------

.. code-block:: c

   #include <fcntl.h>
   #include <termios.h>
   #include <unistd.h>
   
   int fd = open("/dev/ttyS0", O_RDWR | O_NOCTTY);
   struct termios tty;
   tcgetattr(fd, &tty);
   
   cfsetospeed(&tty, B115200);
   cfsetispeed(&tty, B115200);
   
   tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;  // 8-bit
   tty.c_cflag &= ~PARENB;  // No parity
   tty.c_cflag &= ~CSTOPB;  // 1 stop bit
   
   tcsetattr(fd, TCSANOW, &tty);

TTY Layer Architecture
======================

TTY Subsystem Overview
-----------------------

.. code-block:: text

   TTY Layer Architecture:
   
   User Space
   ├── /dev/tty* devices
   │
   Kernel Space
   ├── TTY Core
   │   ├── TTY Driver Layer
   │   ├── Line Discipline Layer
   │   └── TTY Buffer Management
   │
   ├── Serial Core
   │   ├── UART Driver Interface
   │   └── Port Management
   │
   └── Hardware Layer
       ├── UART Controllers
       └── Serial Port Hardware
   
   Components:
   - TTY Core: Character device interface
   - Line Discipline: Terminal processing (N_TTY, N_HDLC, etc.)
   - Serial Core: UART abstraction layer
   - UART Driver: Hardware-specific implementation

TTY Driver Types
----------------

.. code-block:: text

   1. Console Drivers
      - System console output
      - Early boot messages
      - /dev/console
   
   2. Serial Drivers
      - UART hardware
      - /dev/ttyS* (standard serial)
      - RS-232, RS-485
   
   3. USB Serial Drivers
      - USB-to-serial converters
      - /dev/ttyUSB*, /dev/ttyACM*
   
   4. Pseudo TTY (PTY)
      - Terminal emulators
      - SSH connections
      - /dev/pts/*
   
   5. Virtual Console
      - Text mode consoles
      - /dev/tty[1-6]

TTY Driver Structure
=====================

Basic TTY Driver
----------------

.. code-block:: c

   #include <linux/tty.h>
   #include <linux/tty_driver.h>
   
   #define TINY_TTY_MAJOR      240
   #define TINY_TTY_MINORS     4
   
   struct tiny_serial {
       struct tty_port port;
       struct timer_list timer;
       int open_count;
   };
   
   static struct tiny_serial *tiny_table[TINY_TTY_MINORS];
   
   static int tiny_open(struct tty_struct *tty, struct file *filp) {
       struct tiny_serial *tiny;
       int index = tty->index;
       
       tiny = tiny_table[index];
       if (!tiny) {
           // Allocate new port
           tiny = kzalloc(sizeof(*tiny), GFP_KERNEL);
           if (!tiny)
               return -ENOMEM;
           
           tty_port_init(&tiny->port);
           tiny_table[index] = tiny;
       }
       
       tty->driver_data = tiny;
       tty_port_tty_set(&tiny->port, tty);
       
       tiny->open_count++;
       return tty_port_open(&tiny->port, tty, filp);
   }
   
   static void tiny_close(struct tty_struct *tty, struct file *filp) {
       struct tiny_serial *tiny = tty->driver_data;
       
       if (tiny)
           tty_port_close(&tiny->port, tty, filp);
   }
   
   static int tiny_write(struct tty_struct *tty,
                         const unsigned char *buffer, int count) {
       struct tiny_serial *tiny = tty->driver_data;
       int i;
       
       if (!tiny)
           return -ENODEV;
       
       // Write to hardware (example: just print)
       for (i = 0; i < count; i++)
           pr_debug("%c", buffer[i]);
       
       return count;
   }
   
   static unsigned int tiny_write_room(struct tty_struct *tty) {
       struct tiny_serial *tiny = tty->driver_data;
       
       if (!tiny)
           return -ENODEV;
       
       return 255;  // Available space
   }
   
   static const struct tty_operations tiny_ops = {
       .open         = tiny_open,
       .close        = tiny_close,
       .write        = tiny_write,
       .write_room   = tiny_write_room,
   };
   
   static struct tty_driver *tiny_tty_driver;
   
   static int __init tiny_init(void) {
       int retval;
       
       tiny_tty_driver = tty_alloc_driver(TINY_TTY_MINORS, 0);
       if (IS_ERR(tiny_tty_driver))
           return PTR_ERR(tiny_tty_driver);
       
       tiny_tty_driver->driver_name = "tiny_tty";
       tiny_tty_driver->name = "ttty";
       tiny_tty_driver->major = TINY_TTY_MAJOR;
       tiny_tty_driver->type = TTY_DRIVER_TYPE_SERIAL;
       tiny_tty_driver->subtype = SERIAL_TYPE_NORMAL;
       tiny_tty_driver->flags = TTY_DRIVER_REAL_RAW;
       tiny_tty_driver->init_termios = tty_std_termios;
       tiny_tty_driver->init_termios.c_cflag = B9600 | CS8 | CREAD | HUPCL | CLOCAL;
       
       tty_set_operations(tiny_tty_driver, &tiny_ops);
       
       retval = tty_register_driver(tiny_tty_driver);
       if (retval) {
           pr_err("Failed to register tiny tty driver\n");
           tty_driver_kref_put(tiny_tty_driver);
           return retval;
       }
       
       pr_info("Tiny TTY driver registered\n");
       return 0;
   }
   
   static void __exit tiny_exit(void) {
       tty_unregister_driver(tiny_tty_driver);
       tty_driver_kref_put(tiny_tty_driver);
   }
   
   module_init(tiny_init);
   module_exit(tiny_exit);

TTY Port Operations
-------------------

.. code-block:: c

   static int tiny_port_activate(struct tty_port *port, struct tty_struct *tty) {
       struct tiny_serial *tiny = container_of(port, struct tiny_serial, port);
       
       // Initialize hardware
       pr_info("Activating port\n");
       
       // Start any timers or workqueues
       return 0;
   }
   
   static void tiny_port_shutdown(struct tty_port *port) {
       struct tiny_serial *tiny = container_of(port, struct tiny_serial, port);
       
       // Stop hardware
       pr_info("Shutting down port\n");
   }
   
   static const struct tty_port_operations tiny_port_ops = {
       .activate   = tiny_port_activate,
       .shutdown   = tiny_port_shutdown,
   };
   
   // Set port operations
   static int tiny_init_port(struct tiny_serial *tiny) {
       tty_port_init(&tiny->port);
       tiny->port.ops = &tiny_port_ops;
       return 0;
   }

Serial Core Framework
=====================

UART Driver Structure
---------------------

.. code-block:: c

   #include <linux/serial_core.h>
   #include <linux/console.h>
   
   struct my_uart_port {
       struct uart_port port;
       void __iomem *membase;
       unsigned int irq;
       // Custom fields
   };
   
   static unsigned int my_uart_tx_empty(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int status;
       
       status = readl(up->membase + UART_STATUS_REG);
       return (status & TX_EMPTY) ? TIOCSER_TEMT : 0;
   }
   
   static void my_uart_set_mctrl(struct uart_port *port, unsigned int mctrl) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int control = 0;
       
       if (mctrl & TIOCM_RTS)
           control |= RTS_BIT;
       if (mctrl & TIOCM_DTR)
           control |= DTR_BIT;
       
       writel(control, up->membase + UART_CONTROL_REG);
   }
   
   static unsigned int my_uart_get_mctrl(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int status, mctrl = 0;
       
       status = readl(up->membase + UART_STATUS_REG);
       
       if (status & CTS_BIT)
           mctrl |= TIOCM_CTS;
       if (status & DSR_BIT)
           mctrl |= TIOCM_DSR;
       if (status & DCD_BIT)
           mctrl |= TIOCM_CAR;
       
       return mctrl;
   }
   
   static void my_uart_stop_tx(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int control;
       
       control = readl(up->membase + UART_CONTROL_REG);
       control &= ~TX_ENABLE;
       writel(control, up->membase + UART_CONTROL_REG);
   }
   
   static void my_uart_start_tx(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int control;
       
       control = readl(up->membase + UART_CONTROL_REG);
       control |= TX_ENABLE;
       writel(control, up->membase + UART_CONTROL_REG);
   }
   
   static void my_uart_stop_rx(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int control;
       
       control = readl(up->membase + UART_CONTROL_REG);
       control &= ~RX_ENABLE;
       writel(control, up->membase + UART_CONTROL_REG);
   }
   
   static int my_uart_startup(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       int retval;
       
       // Request IRQ
       retval = request_irq(up->irq, my_uart_interrupt, 0, "my_uart", up);
       if (retval)
           return retval;
       
       // Enable UART
       writel(UART_ENABLE, up->membase + UART_CONTROL_REG);
       
       return 0;
   }
   
   static void my_uart_shutdown(struct uart_port *port) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       
       // Disable UART
       writel(0, up->membase + UART_CONTROL_REG);
       
       // Free IRQ
       free_irq(up->irq, up);
   }
   
   static void my_uart_set_termios(struct uart_port *port,
                                   struct ktermios *termios,
                                   struct ktermios *old) {
       struct my_uart_port *up = container_of(port, struct my_uart_port, port);
       unsigned int baud, quot;
       unsigned int config = 0;
       
       // Get baud rate
       baud = uart_get_baud_rate(port, termios, old, 0, port->uartclk / 16);
       quot = uart_get_divisor(port, baud);
       
       // Data bits
       switch (termios->c_cflag & CSIZE) {
       case CS5:
           config |= DATA_5BIT;
           break;
       case CS6:
           config |= DATA_6BIT;
           break;
       case CS7:
           config |= DATA_7BIT;
           break;
       case CS8:
       default:
           config |= DATA_8BIT;
           break;
       }
       
       // Stop bits
       if (termios->c_cflag & CSTOPB)
           config |= STOP_2BIT;
       else
           config |= STOP_1BIT;
       
       // Parity
       if (termios->c_cflag & PARENB) {
           config |= PARITY_ENABLE;
           if (termios->c_cflag & PARODD)
               config |= PARITY_ODD;
           else
               config |= PARITY_EVEN;
       }
       
       // Hardware flow control
       if (termios->c_cflag & CRTSCTS)
           config |= FLOW_CONTROL;
       
       // Configure UART
       writel(quot, up->membase + UART_BAUD_REG);
       writel(config, up->membase + UART_CONFIG_REG);
       
       // Update timeout
       uart_update_timeout(port, termios->c_cflag, baud);
   }
   
   static const struct uart_ops my_uart_ops = {
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
   };

UART Interrupt Handler
----------------------

.. code-block:: c

   static irqreturn_t my_uart_interrupt(int irq, void *dev_id) {
       struct my_uart_port *up = dev_id;
       struct uart_port *port = &up->port;
       unsigned int status;
       
       status = readl(up->membase + UART_INT_STATUS_REG);
       
       if (status & RX_INT) {
           // Receive data
           while (readl(up->membase + UART_STATUS_REG) & RX_READY) {
               unsigned char ch;
               unsigned int flag = TTY_NORMAL;
               
               ch = readl(up->membase + UART_RX_REG);
               port->icount.rx++;
               
               // Check for errors
               if (status & PARITY_ERROR) {
                   flag = TTY_PARITY;
                   port->icount.parity++;
               } else if (status & FRAME_ERROR) {
                   flag = TTY_FRAME;
                   port->icount.frame++;
               } else if (status & OVERRUN_ERROR) {
                   flag = TTY_OVERRUN;
                   port->icount.overrun++;
               }
               
               uart_insert_char(port, status, OVERRUN_ERROR, ch, flag);
           }
           
           tty_flip_buffer_push(&port->state->port);
       }
       
       if (status & TX_INT) {
           // Transmit data
           struct circ_buf *xmit = &port->state->xmit;
           
           if (uart_circ_empty(xmit) || uart_tx_stopped(port)) {
               my_uart_stop_tx(port);
               goto out;
           }
           
           while (!uart_circ_empty(xmit)) {
               if (!(readl(up->membase + UART_STATUS_REG) & TX_READY))
                   break;
               
               writel(xmit->buf[xmit->tail], up->membase + UART_TX_REG);
               xmit->tail = (xmit->tail + 1) & (UART_XMIT_SIZE - 1);
               port->icount.tx++;
           }
           
           if (uart_circ_chars_pending(xmit) < WAKEUP_CHARS)
               uart_write_wakeup(port);
           
           if (uart_circ_empty(xmit))
               my_uart_stop_tx(port);
       }
       
   out:
       return IRQ_HANDLED;
   }

UART Driver Registration
-------------------------

.. code-block:: c

   static struct uart_driver my_uart_driver = {
       .owner          = THIS_MODULE,
       .driver_name    = "my_uart",
       .dev_name       = "ttyMY",
       .major          = TTY_MAJOR,
       .minor          = 64,
       .nr             = 4,  // Number of ports
   };
   
   static int my_uart_probe(struct platform_device *pdev) {
       struct my_uart_port *up;
       struct resource *mem;
       int irq, ret;
       
       up = devm_kzalloc(&pdev->dev, sizeof(*up), GFP_KERNEL);
       if (!up)
           return -ENOMEM;
       
       mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       up->membase = devm_ioremap_resource(&pdev->dev, mem);
       if (IS_ERR(up->membase))
           return PTR_ERR(up->membase);
       
       irq = platform_get_irq(pdev, 0);
       if (irq < 0)
           return irq;
       up->irq = irq;
       
       // Initialize uart_port
       up->port.dev = &pdev->dev;
       up->port.type = PORT_MY_UART;
       up->port.iotype = UPIO_MEM;
       up->port.membase = up->membase;
       up->port.mapbase = mem->start;
       up->port.irq = irq;
       up->port.uartclk = 48000000;  // Clock frequency
       up->port.fifosize = 16;
       up->port.ops = &my_uart_ops;
       up->port.flags = UPF_BOOT_AUTOCONF;
       up->port.line = pdev->id;
       
       platform_set_drvdata(pdev, up);
       
       ret = uart_add_one_port(&my_uart_driver, &up->port);
       if (ret) {
           dev_err(&pdev->dev, "Failed to add UART port\n");
           return ret;
       }
       
       return 0;
   }
   
   static int my_uart_remove(struct platform_device *pdev) {
       struct my_uart_port *up = platform_get_drvdata(pdev);
       
       uart_remove_one_port(&my_uart_driver, &up->port);
       return 0;
   }
   
   static const struct of_device_id my_uart_of_match[] = {
       { .compatible = "vendor,my-uart" },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_uart_of_match);
   
   static struct platform_driver my_uart_platform_driver = {
       .probe  = my_uart_probe,
       .remove = my_uart_remove,
       .driver = {
           .name           = "my-uart",
           .of_match_table = my_uart_of_match,
       },
   };
   
   static int __init my_uart_init(void) {
       int ret;
       
       ret = uart_register_driver(&my_uart_driver);
       if (ret)
           return ret;
       
       ret = platform_driver_register(&my_uart_platform_driver);
       if (ret)
           uart_unregister_driver(&my_uart_driver);
       
       return ret;
   }
   
   static void __exit my_uart_exit(void) {
       platform_driver_unregister(&my_uart_platform_driver);
       uart_unregister_driver(&my_uart_driver);
   }
   
   module_init(my_uart_init);
   module_exit(my_uart_exit);

Line Disciplines
================

N_TTY (Default)
---------------

.. code-block:: c

   // N_TTY is the default line discipline
   // Provides canonical and raw modes
   
   // Set line discipline
   int ldisc = N_TTY;
   ioctl(fd, TIOCSETD, &ldisc);
   
   // Get line discipline
   int ldisc;
   ioctl(fd, TIOCGETD, &ldisc);

Custom Line Discipline
----------------------

.. code-block:: c

   #include <linux/tty_ldisc.h>
   
   static int my_ldisc_open(struct tty_struct *tty) {
       // Initialize line discipline
       return 0;
   }
   
   static void my_ldisc_close(struct tty_struct *tty) {
       // Cleanup
   }
   
   static ssize_t my_ldisc_read(struct tty_struct *tty, struct file *file,
                                unsigned char __user *buf, size_t nr) {
       // Read implementation
       return 0;
   }
   
   static ssize_t my_ldisc_write(struct tty_struct *tty, struct file *file,
                                 const unsigned char *buf, size_t nr) {
       // Write implementation
       return nr;
   }
   
   static void my_ldisc_receive_buf(struct tty_struct *tty,
                                    const unsigned char *cp,
                                    const char *fp, int count) {
       // Process received data
   }
   
   static struct tty_ldisc_ops my_ldisc_ops = {
       .magic          = TTY_LDISC_MAGIC,
       .name           = "my_ldisc",
       .num            = N_MY_LDISC,
       .open           = my_ldisc_open,
       .close          = my_ldisc_close,
       .read           = my_ldisc_read,
       .write          = my_ldisc_write,
       .receive_buf    = my_ldisc_receive_buf,
       .owner          = THIS_MODULE,
   };
   
   static int __init my_ldisc_init(void) {
       return tty_register_ldisc(&my_ldisc_ops);
   }
   
   static void __exit my_ldisc_exit(void) {
       tty_unregister_ldisc(&my_ldisc_ops);
   }

Console Driver
==============

Basic Console
-------------

.. code-block:: c

   #include <linux/console.h>
   
   static void my_console_write(struct console *co, const char *s, unsigned int count) {
       struct my_uart_port *up = &my_uart_ports[co->index];
       int i;
       
       for (i = 0; i < count; i++) {
           // Wait for TX ready
           while (!(readl(up->membase + UART_STATUS_REG) & TX_READY))
               cpu_relax();
           
           // Write character
           writel(s[i], up->membase + UART_TX_REG);
           
           // Handle newline
           if (s[i] == '\n') {
               while (!(readl(up->membase + UART_STATUS_REG) & TX_READY))
                   cpu_relax();
               writel('\r', up->membase + UART_TX_REG);
           }
       }
   }
   
   static int __init my_console_setup(struct console *co, char *options) {
       struct my_uart_port *up;
       int baud = 115200;
       int bits = 8;
       int parity = 'n';
       int flow = 'n';
       
       if (co->index >= NR_PORTS)
           return -ENODEV;
       
       up = &my_uart_ports[co->index];
       if (!up->membase)
           return -ENODEV;
       
       if (options)
           uart_parse_options(options, &baud, &parity, &bits, &flow);
       
       return uart_set_options(&up->port, co, baud, parity, bits, flow);
   }
   
   static struct console my_console = {
       .name   = "ttyMY",
       .write  = my_console_write,
       .setup  = my_console_setup,
       .flags  = CON_PRINTBUFFER,
       .index  = -1,
       .data   = &my_uart_driver,
   };
   
   // Register console
   static int __init my_console_init(void) {
       register_console(&my_console);
       return 0;
   }
   console_initcall(my_console_init);

Termios Configuration
=====================

Termios Structure
-----------------

.. code-block:: c

   struct termios {
       tcflag_t c_iflag;   // Input modes
       tcflag_t c_oflag;   // Output modes
       tcflag_t c_cflag;   // Control modes
       tcflag_t c_lflag;   // Local modes
       cc_t c_cc[NCCS];    // Control characters
   };
   
   // Input flags (c_iflag)
   IGNBRK   // Ignore BREAK
   BRKINT   // Signal on BREAK
   IGNPAR   // Ignore parity errors
   PARMRK   // Mark parity errors
   INPCK    // Enable input parity check
   ISTRIP   // Strip 8th bit
   INLCR    // Map NL to CR
   IGNCR    // Ignore CR
   ICRNL    // Map CR to NL
   IXON     // Enable XON/XOFF flow control
   IXOFF    // Enable XON/XOFF on input
   
   // Output flags (c_oflag)
   OPOST    // Post-process output
   ONLCR    // Map NL to CR-NL
   OCRNL    // Map CR to NL
   
   // Control flags (c_cflag)
   CSIZE    // Character size mask
   CS5      // 5 bits
   CS6      // 6 bits
   CS7      // 7 bits
   CS8      // 8 bits
   CSTOPB   // 2 stop bits
   CREAD    // Enable receiver
   PARENB   // Enable parity
   PARODD   // Odd parity
   HUPCL    // Hang up on last close
   CLOCAL   // Ignore modem control lines
   CRTSCTS  // Hardware flow control
   
   // Local flags (c_lflag)
   ISIG     // Enable signals
   ICANON   // Canonical mode
   ECHO     // Echo input
   ECHOE    // Echo erase
   ECHOK    // Echo kill
   ECHONL   // Echo NL
   IEXTEN   // Enable extended functions

Setting Termios
---------------

.. code-block:: c

   int set_interface_attribs(int fd, int speed) {
       struct termios tty;
       
       if (tcgetattr(fd, &tty) < 0) {
           perror("tcgetattr");
           return -1;
       }
       
       cfsetospeed(&tty, speed);
       cfsetispeed(&tty, speed);
       
       tty.c_cflag |= (CLOCAL | CREAD);    // Enable receiver, ignore modem
       tty.c_cflag &= ~CSIZE;
       tty.c_cflag |= CS8;                  // 8-bit
       tty.c_cflag &= ~PARENB;              // No parity
       tty.c_cflag &= ~CSTOPB;              // 1 stop bit
       tty.c_cflag &= ~CRTSCTS;             // No hardware flow control
       
       tty.c_lflag = 0;                     // No signaling chars, no echo
       tty.c_oflag = 0;                     // No remapping, no delays
       tty.c_cc[VMIN]  = 0;                 // Non-blocking read
       tty.c_cc[VTIME] = 5;                 // 0.5 seconds read timeout
       
       if (tcsetattr(fd, TCSANOW, &tty) != 0) {
           perror("tcsetattr");
           return -1;
       }
       
       return 0;
   }

Debugging
=========

Serial Port Debugging
---------------------

.. code-block:: bash

   # Check serial port status
   setserial -a /dev/ttyS0
   
   # Enable serial debugging
   echo 8 > /proc/sys/kernel/printk
   dmesg -w | grep -i "tty\|serial"
   
   # Monitor serial traffic
   strace -e trace=read,write cat /dev/ttyS0
   
   # Test loopback
   # Connect TX to RX
   cat /dev/ttyS0 &
   echo "test" > /dev/ttyS0

TTY Layer Debugging
-------------------

.. code-block:: bash

   # TTY statistics
   cat /proc/tty/driver/serial
   cat /proc/tty/ldiscs
   
   # Check TTY device
   ls -l /dev/tty*
   stat /dev/ttyS0

Best Practices
==============

1. **Use serial core** for UART drivers (don't reinvent)
2. **Handle flow control** properly
3. **Implement termios** correctly
4. **Use tty_flip_buffer** for RX data
5. **Check circular buffer** state (empty, full)
6. **Lock appropriately** (port->lock for RX/TX)
7. **Update icount** statistics
8. **Handle modem signals** (CTS, RTS, DTR, DSR)
9. **Implement console** for early debugging
10. **Test different baud rates** and configurations

Common Pitfalls
===============

1. **Buffer overruns** - not checking FIFO status
2. **Missing locking** - race conditions in interrupt handler
3. **Incorrect termios** - wrong baud rate calculations
4. **Flow control issues** - not handling CTS/RTS
5. **Console hangs** - polling too long in console_write
6. **Circular buffer** - incorrect head/tail updates
7. **IRQ storms** - not clearing interrupt status

Quick Reference
===============

.. code-block:: c

   // TTY driver allocation
   tty_alloc_driver(ports, flags);
   tty_register_driver(driver);
   
   // UART driver
   uart_register_driver(&driver);
   uart_add_one_port(&driver, &port);
   
   // RX handling
   uart_insert_char(port, status, ovrrun, ch, flag);
   tty_flip_buffer_push(&port->state->port);
   
   // TX handling
   struct circ_buf *xmit = &port->state->xmit;
   uart_circ_empty(xmit);
   uart_circ_chars_pending(xmit);
   uart_write_wakeup(port);
   
   // Termios
   uart_get_baud_rate(port, termios, old, min, max);
   uart_get_divisor(port, baud);
   uart_update_timeout(port, cflag, baud);

See Also
========

- Linux_USB_Drivers.rst
- Linux_Platform_Drivers.rst
- Linux_Interrupts.rst
- Linux_DMA.rst

References
==========

- Linux Serial Driver API: https://www.kernel.org/doc/html/latest/driver-api/serial/
- Documentation/driver-api/serial/ in kernel source
- drivers/tty/serial/ for examples
