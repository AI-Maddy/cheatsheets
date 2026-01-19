===================================
Linux USB Drivers Guide
===================================

:Author: Linux Device Driver Documentation
:Date: January 2026
:Version: 1.0
:Focus: USB device driver development in Linux

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential USB Commands
----------------------

.. code-block:: bash

   # List USB devices
   lsusb
   lsusb -v -d 1234:5678  # Vendor:Product ID
   
   # USB device tree
   lsusb -t
   
   # USB device information
   cat /sys/kernel/debug/usb/devices
   usb-devices
   
   # Monitor USB events
   udevadm monitor --subsystem-match=usb
   
   # Check USB driver binding
   ls /sys/bus/usb/drivers/
   cat /sys/bus/usb/devices/1-1/driver

Quick USB Driver Template
--------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/usb.h>
   
   #define VENDOR_ID   0x1234
   #define PRODUCT_ID  0x5678
   
   static struct usb_device_id usb_table[] = {
       { USB_DEVICE(VENDOR_ID, PRODUCT_ID) },
       { }
   };
   MODULE_DEVICE_TABLE(usb, usb_table);
   
   static int usb_probe(struct usb_interface *interface,
                        const struct usb_device_id *id) {
       pr_info("USB device connected\n");
       return 0;
   }
   
   static void usb_disconnect(struct usb_interface *interface) {
       pr_info("USB device disconnected\n");
   }
   
   static struct usb_driver usb_driver = {
       .name       = "my_usb_driver",
       .probe      = usb_probe,
       .disconnect = usb_disconnect,
       .id_table   = usb_table,
   };
   
   module_usb_driver(usb_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("USB Driver Example");

USB Basics
==========

USB Architecture
----------------

.. code-block:: text

   USB Hierarchy:
   
   Host Controller (HC)
   ├── Root Hub
   │   ├── Hub (optional)
   │   │   ├── Device
   │   │   └── Device
   │   └── Device
   
   Components:
   - Host Controller: UHCI, OHCI, EHCI (USB 2.0), xHCI (USB 3.0)
   - Hub: Expands USB ports
   - Device: USB peripheral
   
   USB Speeds:
   - Low Speed (LS):  1.5 Mbps   (USB 1.0)
   - Full Speed (FS): 12 Mbps    (USB 1.1)
   - High Speed (HS): 480 Mbps   (USB 2.0)
   - SuperSpeed (SS): 5 Gbps     (USB 3.0)
   - SuperSpeed+:     10 Gbps    (USB 3.1)

USB Descriptors
---------------

.. code-block:: c

   // Device Descriptor
   struct usb_device_descriptor {
       __u8  bLength;
       __u8  bDescriptorType;      // 0x01
       __le16 bcdUSB;              // USB version
       __u8  bDeviceClass;
       __u8  bDeviceSubClass;
       __u8  bDeviceProtocol;
       __u8  bMaxPacketSize0;
       __le16 idVendor;            // Vendor ID
       __le16 idProduct;           // Product ID
       __le16 bcdDevice;           // Device version
       __u8  iManufacturer;
       __u8  iProduct;
       __u8  iSerialNumber;
       __u8  bNumConfigurations;
   } __attribute__((packed));
   
   // Configuration Descriptor
   struct usb_config_descriptor {
       __u8  bLength;
       __u8  bDescriptorType;      // 0x02
       __le16 wTotalLength;
       __u8  bNumInterfaces;
       __u8  bConfigurationValue;
       __u8  iConfiguration;
       __u8  bmAttributes;
       __u8  bMaxPower;            // In 2mA units
   } __attribute__((packed));
   
   // Interface Descriptor
   struct usb_interface_descriptor {
       __u8  bLength;
       __u8  bDescriptorType;      // 0x04
       __u8  bInterfaceNumber;
       __u8  bAlternateSetting;
       __u8  bNumEndpoints;
       __u8  bInterfaceClass;
       __u8  bInterfaceSubClass;
       __u8  bInterfaceProtocol;
       __u8  iInterface;
   } __attribute__((packed));
   
   // Endpoint Descriptor
   struct usb_endpoint_descriptor {
       __u8  bLength;
       __u8  bDescriptorType;      // 0x05
       __u8  bEndpointAddress;     // Bit 7: 0=OUT, 1=IN
       __u8  bmAttributes;         // Bits 0-1: Transfer type
       __le16 wMaxPacketSize;
       __u8  bInterval;            // Polling interval
   } __attribute__((packed));

Endpoint Types
--------------

.. code-block:: text

   Control Endpoints (Type 0):
   - Bidirectional
   - Used for device configuration
   - Every device has endpoint 0
   
   Bulk Endpoints (Type 2):
   - Unidirectional (IN or OUT)
   - Large data transfers
   - No guaranteed bandwidth
   - Used for: Mass storage, printers
   
   Interrupt Endpoints (Type 3):
   - Unidirectional
   - Small, periodic transfers
   - Guaranteed latency
   - Used for: HID devices (keyboard, mouse)
   
   Isochronous Endpoints (Type 1):
   - Unidirectional
   - Periodic, guaranteed bandwidth
   - No error correction
   - Used for: Audio, video

USB Driver Structure
====================

Driver Registration
-------------------

.. code-block:: c

   #include <linux/usb.h>
   
   static struct usb_device_id device_table[] = {
       // Match specific vendor and product
       { USB_DEVICE(0x1234, 0x5678) },
       
       // Match vendor only
       { USB_DEVICE_VER(0x1234, 0x5678, 0x0100, 0x0200) },
       
       // Match by class
       { USB_DEVICE_INFO(USB_CLASS_MASS_STORAGE, 0x06, 0x50) },
       
       // Match interface
       { USB_INTERFACE_INFO(USB_CLASS_HID, 0, 0) },
       
       { }  // Terminating entry
   };
   MODULE_DEVICE_TABLE(usb, device_table);
   
   static struct usb_driver my_driver = {
       .name       = "my_usb_driver",
       .probe      = usb_probe,
       .disconnect = usb_disconnect,
       .suspend    = usb_suspend,
       .resume     = usb_resume,
       .id_table   = device_table,
   };
   
   // Register driver
   static int __init usb_init(void) {
       return usb_register(&my_driver);
   }
   
   static void __exit usb_exit(void) {
       usb_deregister(&my_driver);
   }
   
   module_init(usb_init);
   module_exit(usb_exit);
   
   // Or use helper macro
   module_usb_driver(my_driver);

Probe Function
--------------

.. code-block:: c

   static int usb_probe(struct usb_interface *interface,
                        const struct usb_device_id *id) {
       struct usb_device *udev = interface_to_usbdev(interface);
       struct usb_host_interface *iface_desc = interface->cur_altsetting;
       struct usb_endpoint_descriptor *endpoint;
       struct my_device *dev;
       int i, retval;
       
       pr_info("USB device connected: %04x:%04x\n",
               id->idVendor, id->idProduct);
       
       // Allocate device structure
       dev = kzalloc(sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       dev->udev = usb_get_dev(udev);
       dev->interface = interface;
       
       // Parse endpoints
       for (i = 0; i < iface_desc->desc.bNumEndpoints; i++) {
           endpoint = &iface_desc->endpoint[i].desc;
           
           if (usb_endpoint_is_bulk_in(endpoint)) {
               dev->bulk_in_endpointAddr = endpoint->bEndpointAddress;
               dev->bulk_in_size = le16_to_cpu(endpoint->wMaxPacketSize);
           }
           
           if (usb_endpoint_is_bulk_out(endpoint)) {
               dev->bulk_out_endpointAddr = endpoint->bEndpointAddress;
           }
       }
       
       // Save device structure
       usb_set_intfdata(interface, dev);
       
       // Register character device (optional)
       retval = usb_register_dev(interface, &my_class);
       if (retval) {
           pr_err("Failed to register USB device\n");
           usb_set_intfdata(interface, NULL);
           kfree(dev);
           return retval;
       }
       
       pr_info("USB device attached to minor %d\n", interface->minor);
       return 0;
   }

Disconnect Function
-------------------

.. code-block:: c

   static void usb_disconnect(struct usb_interface *interface) {
       struct my_device *dev = usb_get_intfdata(interface);
       int minor = interface->minor;
       
       usb_set_intfdata(interface, NULL);
       
       // Deregister character device
       usb_deregister_dev(interface, &my_class);
       
       // Cleanup
       usb_put_dev(dev->udev);
       kfree(dev);
       
       pr_info("USB device #%d disconnected\n", minor);
   }

URB (USB Request Block)
=======================

URB Basics
----------

.. code-block:: c

   #include <linux/usb.h>
   
   // Allocate URB
   struct urb *urb = usb_alloc_urb(0, GFP_KERNEL);
   if (!urb)
       return -ENOMEM;
   
   // Fill URB for bulk transfer
   usb_fill_bulk_urb(urb,
                     dev->udev,
                     usb_sndbulkpipe(dev->udev, dev->bulk_out_endpointAddr),
                     buffer,
                     count,
                     write_bulk_callback,
                     dev);
   
   // Submit URB
   retval = usb_submit_urb(urb, GFP_KERNEL);
   if (retval) {
       pr_err("Failed to submit URB: %d\n", retval);
       usb_free_urb(urb);
       return retval;
   }
   
   // URB will be freed in callback

Bulk Transfer
-------------

.. code-block:: c

   static void write_bulk_callback(struct urb *urb) {
       struct my_device *dev = urb->context;
       
       if (urb->status) {
           pr_err("Bulk write failed: %d\n", urb->status);
       } else {
           pr_info("Wrote %d bytes\n", urb->actual_length);
       }
       
       usb_free_urb(urb);
       kfree(urb->transfer_buffer);
   }
   
   static ssize_t device_write(struct file *file, const char __user *user_buffer,
                               size_t count, loff_t *ppos) {
       struct my_device *dev = file->private_data;
       struct urb *urb;
       char *buf;
       int retval;
       
       // Allocate buffer
       buf = kmalloc(count, GFP_KERNEL);
       if (!buf)
           return -ENOMEM;
       
       if (copy_from_user(buf, user_buffer, count)) {
           kfree(buf);
           return -EFAULT;
       }
       
       // Allocate URB
       urb = usb_alloc_urb(0, GFP_KERNEL);
       if (!urb) {
           kfree(buf);
           return -ENOMEM;
       }
       
       // Fill and submit URB
       usb_fill_bulk_urb(urb, dev->udev,
                         usb_sndbulkpipe(dev->udev, dev->bulk_out_endpointAddr),
                         buf, count, write_bulk_callback, dev);
       
       retval = usb_submit_urb(urb, GFP_KERNEL);
       if (retval) {
           usb_free_urb(urb);
           kfree(buf);
           return retval;
       }
       
       return count;
   }

Interrupt Transfer
------------------

.. code-block:: c

   static void interrupt_callback(struct urb *urb) {
       struct my_device *dev = urb->context;
       int retval;
       
       switch (urb->status) {
       case 0:
           // Success
           process_interrupt_data(urb->transfer_buffer, urb->actual_length);
           break;
       case -ENOENT:
       case -ECONNRESET:
       case -ESHUTDOWN:
           // URB killed
           return;
       default:
           pr_err("Interrupt URB error: %d\n", urb->status);
           break;
       }
       
       // Resubmit URB for continuous polling
       retval = usb_submit_urb(urb, GFP_ATOMIC);
       if (retval)
           pr_err("Failed to resubmit interrupt URB: %d\n", retval);
   }
   
   static int start_interrupt_polling(struct my_device *dev) {
       struct urb *urb;
       void *buffer;
       
       buffer = kmalloc(dev->int_in_size, GFP_KERNEL);
       if (!buffer)
           return -ENOMEM;
       
       urb = usb_alloc_urb(0, GFP_KERNEL);
       if (!urb) {
           kfree(buffer);
           return -ENOMEM;
       }
       
       usb_fill_int_urb(urb, dev->udev,
                        usb_rcvintpipe(dev->udev, dev->int_in_endpointAddr),
                        buffer, dev->int_in_size,
                        interrupt_callback, dev,
                        dev->int_in_interval);
       
       dev->int_in_urb = urb;
       return usb_submit_urb(urb, GFP_KERNEL);
   }

Control Transfer
----------------

.. code-block:: c

   // Synchronous control transfer
   int usb_control_msg(struct usb_device *dev,
                       unsigned int pipe,
                       __u8 request,
                       __u8 requesttype,
                       __u16 value,
                       __u16 index,
                       void *data,
                       __u16 size,
                       int timeout);
   
   // Example: Vendor-specific request
   static int send_vendor_request(struct my_device *dev, u8 request, u16 value) {
       int retval;
       
       retval = usb_control_msg(dev->udev,
                                usb_sndctrlpipe(dev->udev, 0),
                                request,
                                USB_DIR_OUT | USB_TYPE_VENDOR | USB_RECIP_DEVICE,
                                value,
                                0,  // index
                                NULL,  // data
                                0,  // size
                                USB_CTRL_SET_TIMEOUT);
       
       if (retval < 0)
           pr_err("Control message failed: %d\n", retval);
       
       return retval;
   }
   
   // Read device descriptor
   static int read_device_descriptor(struct usb_device *udev) {
       struct usb_device_descriptor desc;
       int retval;
       
       retval = usb_get_descriptor(udev, USB_DT_DEVICE, 0,
                                   &desc, sizeof(desc));
       if (retval < 0) {
           pr_err("Failed to read device descriptor: %d\n", retval);
           return retval;
       }
       
       pr_info("Device: %04x:%04x, USB %x.%02x\n",
               le16_to_cpu(desc.idVendor),
               le16_to_cpu(desc.idProduct),
               desc.bcdUSB >> 8, desc.bcdUSB & 0xff);
       
       return 0;
   }

Character Device Interface
==========================

File Operations
---------------

.. code-block:: c

   static int device_open(struct inode *inode, struct file *file) {
       struct usb_interface *interface;
       struct my_device *dev;
       int subminor;
       
       subminor = iminor(inode);
       
       interface = usb_find_interface(&my_driver, subminor);
       if (!interface) {
           pr_err("Can't find device for minor %d\n", subminor);
           return -ENODEV;
       }
       
       dev = usb_get_intfdata(interface);
       if (!dev)
           return -ENODEV;
       
       file->private_data = dev;
       return 0;
   }
   
   static int device_release(struct inode *inode, struct file *file) {
       return 0;
   }
   
   static ssize_t device_read(struct file *file, char __user *buffer,
                              size_t count, loff_t *ppos) {
       struct my_device *dev = file->private_data;
       int retval;
       char *buf;
       
       buf = kmalloc(count, GFP_KERNEL);
       if (!buf)
           return -ENOMEM;
       
       // Synchronous bulk read
       retval = usb_bulk_msg(dev->udev,
                             usb_rcvbulkpipe(dev->udev, dev->bulk_in_endpointAddr),
                             buf, min(dev->bulk_in_size, count),
                             &count, HZ*10);
       
       if (retval) {
           pr_err("Bulk read failed: %d\n", retval);
           kfree(buf);
           return retval;
       }
       
       if (copy_to_user(buffer, buf, count)) {
           kfree(buf);
           return -EFAULT;
       }
       
       kfree(buf);
       return count;
   }
   
   static const struct file_operations fops = {
       .owner   = THIS_MODULE,
       .open    = device_open,
       .release = device_release,
       .read    = device_read,
       .write   = device_write,
   };
   
   static struct usb_class_driver my_class = {
       .name       = "usb/mydev%d",
       .fops       = &fops,
       .minor_base = USB_MINOR_BASE,
   };

Power Management
================

Suspend/Resume
--------------

.. code-block:: c

   static int usb_suspend(struct usb_interface *intf, pm_message_t message) {
       struct my_device *dev = usb_get_intfdata(intf);
       
       pr_info("USB device suspended\n");
       
       // Stop any ongoing transfers
       if (dev->int_in_urb)
           usb_kill_urb(dev->int_in_urb);
       
       return 0;
   }
   
   static int usb_resume(struct usb_interface *intf) {
       struct my_device *dev = usb_get_intfdata(intf);
       int retval;
       
       pr_info("USB device resumed\n");
       
       // Restart transfers
       if (dev->int_in_urb) {
           retval = usb_submit_urb(dev->int_in_urb, GFP_KERNEL);
           if (retval)
               pr_err("Failed to restart interrupt URB: %d\n", retval);
       }
       
       return 0;
   }

Autosuspend
-----------

.. code-block:: c

   static int usb_probe(struct usb_interface *interface,
                        const struct usb_device_id *id) {
       struct usb_device *udev = interface_to_usbdev(interface);
       
       // Enable autosuspend
       usb_enable_autosuspend(udev);
       
       // Set autosuspend delay (ms)
       pm_runtime_set_autosuspend_delay(&udev->dev, 2000);
       
       return 0;
   }

USB Serial Drivers
==================

USB-to-Serial Converter
-----------------------

.. code-block:: c

   #include <linux/tty.h>
   #include <linux/tty_driver.h>
   #include <linux/usb/serial.h>
   
   static struct usb_serial_driver my_serial_device = {
       .driver = {
           .owner = THIS_MODULE,
           .name  = "my_serial",
       },
       .description         = "My USB Serial",
       .id_table           = id_table,
       .num_ports          = 1,
       .open               = serial_open,
       .close              = serial_close,
       .write              = serial_write,
       .write_room         = serial_write_room,
       .throttle           = serial_throttle,
       .unthrottle         = serial_unthrottle,
       .attach             = serial_attach,
       .release            = serial_release,
       .port_probe         = serial_port_probe,
       .port_remove        = serial_port_remove,
   };
   
   static struct usb_serial_driver * const serial_drivers[] = {
       &my_serial_device,
       NULL
   };
   
   module_usb_serial_driver(serial_drivers, id_table);

Debugging
=========

USB Core Debugging
------------------

.. code-block:: bash

   # Enable USB core debugging
   echo -n 'module usbcore =p' > /sys/kernel/debug/dynamic_debug/control
   echo -n 'module usb_storage =p' > /sys/kernel/debug/dynamic_debug/control
   
   # View USB debug messages
   dmesg -w | grep usb
   
   # USB device tree
   cat /sys/kernel/debug/usb/devices
   
   # Monitor usbmon (USB traffic)
   modprobe usbmon
   cat /sys/kernel/debug/usb/usbmon/0u

usbmon - USB Monitoring
-----------------------

.. code-block:: bash

   # Capture USB traffic
   sudo modprobe usbmon
   sudo tcpdump -i usbmon0 -w usb_capture.pcap
   
   # Or use Wireshark
   sudo wireshark &
   # Select usbmon0 interface
   
   # Text output
   sudo cat /sys/kernel/debug/usb/usbmon/1u

Best Practices
==============

1. **Always check return values** from USB functions
2. **Use GFP_ATOMIC** in interrupt context
3. **Free URBs** in completion callbacks
4. **Handle disconnection** gracefully
5. **Use reference counting** (usb_get_dev/usb_put_dev)
6. **Implement power management** (suspend/resume)
7. **Lock endpoints** during transfers
8. **Check endpoint direction** before use
9. **Validate descriptors** from device
10. **Test with different USB speeds**

Common Pitfalls
===============

1. **Memory leaks** - not freeing URBs/buffers
2. **Race conditions** - disconnect during transfer
3. **Wrong GFP flags** - GFP_KERNEL in atomic context
4. **Endpoint mismatch** - using wrong direction
5. **Missing error handling** - not checking usb_submit_urb
6. **Buffer alignment** - DMA buffer requirements
7. **Timeout issues** - too short timeouts

Quick Reference
===============

.. code-block:: c

   // URB submission
   urb = usb_alloc_urb(0, GFP_KERNEL);
   usb_fill_bulk_urb(urb, udev, pipe, buf, len, callback, ctx);
   usb_submit_urb(urb, GFP_KERNEL);
   
   // Synchronous transfer
   usb_bulk_msg(udev, pipe, buf, len, &actual, timeout);
   usb_control_msg(udev, pipe, req, reqtype, val, idx, buf, len, timeout);
   
   // Pipes
   usb_sndbulkpipe(udev, endpoint)
   usb_rcvbulkpipe(udev, endpoint)
   usb_sndintpipe(udev, endpoint)
   usb_rcvintpipe(udev, endpoint)
   usb_sndctrlpipe(udev, endpoint)
   usb_rcvctrlpipe(udev, endpoint)

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Device_Tree.rst
- Linux_Driver_Debugging.rst

References
==========

- Linux USB Driver API: https://www.kernel.org/doc/html/latest/driver-api/usb/
- USB 2.0 Specification: https://www.usb.org/documents
- man usb
- drivers/usb/ in Linux kernel source
