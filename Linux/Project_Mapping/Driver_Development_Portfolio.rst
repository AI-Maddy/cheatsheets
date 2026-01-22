======================================
Linux Driver Development Portfolio
======================================

:Author: Madhavan Vivekanandan
:Date: January 22, 2026
:Purpose: Comprehensive catalog of all driver types developed/integrated across projects
:Scope: Platform, Character, Block, Network, USB, Video, I2C, SPI, PCIe, Power Management

.. contents:: Quick Navigation
   :depth: 3
   :local:

Overview
=========

**Total Driver Experience**: 15+ driver types across 8 projects spanning 18+ years

**Driver Categories Portfolio**:

========================  ===============  ===================================
Driver Category           Count            Complexity Level
========================  ===============  ===================================
Platform Drivers          5+               High (custom SOC peripherals)
Character Drivers         10+              Medium-High
Block Drivers             3                Medium (MTD, eMMC, SATA)
Network Drivers           8+               High (Wi-Fi, CAN, EMAC, RF)
USB Drivers               3                High (bulk, isochronous custom)
Video Drivers (V4L2)      2                High (DMA, hardware codec)
I2C Drivers               10+              Low-Medium (sensors, PMIC)
SPI Drivers               5+               Low-Medium (CAN, flash)
PCIe Drivers              1                Very High (multi-RC platform)
Power Management          Multiple         Medium (CPUFreq, runtime PM)
========================  ===============  ===================================

Section 1: Platform Drivers
=============================

1.1 PCIe Platform Driver (Multi-Root Complex)
-----------------------------------------------

**Project**: #2 Avionics (Intel Atom C3xxx), Reference Design (Router/AP)

**Complexity**: Very High (limited reference material, multi-RC enumeration)

Driver Architecture
~~~~~~~~~~~~~~~~~~~~

::

    Platform Device
         ↓
    [Multi-RC PCIe Platform Driver]
         ├─ Root Complex 0 Management
         ├─ Root Complex 1 Management
         └─ Root Complex 2 Management
         ↓
    [PCI Core - Modified Enumeration]
         ↓
    [PCIe Devices on each RC]

**Key Features**:

==================================  ================================================
Feature                             Implementation
==================================  ================================================
Multi-RC Support                    3+ root complexes, independent bus enumeration
Config Space Mapping                RC-specific address calculation
Bus Range Management                Each RC owns 0xN0-0xNF bus range
Device Enumeration                  Custom enumeration per RC
Interrupt Routing                   RC-specific interrupt controllers
FPGA Validation                     Tested with emulated SOC before silicon
==================================  ================================================

**Code Snapshot** (Simplified)::

    static int multi_rc_pcie_probe(struct platform_device *pdev)
    {
        struct multi_rc_pcie *pcie;
        int rc_id;
        
        /* Get RC ID from device tree */
        of_property_read_u32(pdev->dev.of_node, "rc-id", &rc_id);
        
        /* Map RC-specific configuration space */
        pcie->cfg_base = platform_ioremap_resource(pdev, 0);
        
        /* Setup bus range for this RC */
        pcie->bus_range.start = rc_id * 0x10;
        pcie->bus_range.end = (rc_id + 1) * 0x10 - 1;
        
        /* Register PCI host bridge */
        bridge = devm_pci_alloc_host_bridge(&pdev->dev, sizeof(*pcie));
        bridge->ops = &multi_rc_pcie_ops;
        
        /* Enumerate devices on this RC */
        return pci_host_probe(bridge);
    }

**Interview Highlight**:
"Solved unique multi-RC PCIe challenge with limited reference implementations. Implemented independent enumeration for 3+ root complexes, each managing separate bus ranges and config spaces. Validated using FPGA emulation."

1.2 FPGA Platform Driver
--------------------------

**Project**: #2 Avionics

**Purpose**: Custom FPGA control for specialized avionics hardware

Driver Responsibilities
~~~~~~~~~~~~~~~~~~~~~~~~

- Memory-mapped I/O access to FPGA registers
- Interrupt handling from FPGA
- DMA coordination with FPGA blocks
- FPGA configuration/programming interface

**Platform Driver Structure**::

    static struct platform_driver fpga_driver = {
        .probe = fpga_probe,
        .remove = fpga_remove,
        .driver = {
            .name = "avionics-fpga",
            .of_match_table = fpga_of_match,
        },
    };
    
    static int fpga_probe(struct platform_device *pdev)
    {
        struct fpga_dev *fdev;
        struct resource *res;
        
        /* Map FPGA register space */
        res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
        fdev->regs = devm_ioremap_resource(&pdev->dev, res);
        
        /* Setup interrupts from FPGA */
        fdev->irq = platform_get_irq(pdev, 0);
        devm_request_irq(&pdev->dev, fdev->irq, fpga_isr, 
                         IRQF_SHARED, "fpga", fdev);
        
        /* Create character device interface */
        cdev_init(&fdev->cdev, &fpga_fops);
        cdev_add(&fdev->cdev, fdev->devt, 1);
        
        return 0;
    }

1.3 Power Management Platform Driver
--------------------------------------

**Projects**: #1 (IoT), #7 (Thermal)

**Purpose**: Custom power states, battery management

**Features**:

- Custom deep-sleep modes (< 50 µA)
- Wake source management
- Battery fuel gauge integration
- Power rail control

Section 2: Character Drivers
==============================

2.1 Custom Character Drivers by Project
-----------------------------------------

**Character Device Portfolio**:

+----------+-------------------------+-----------------------------------+
| Project  | Character Driver        | Purpose                           |
+==========+=========================+===================================+
| #1 IoT   | Smart Home Control      | User-space control interface      |
+----------+-------------------------+-----------------------------------+
| #2 Avion | FPGA Control            | FPGA register access              |
+----------+-------------------------+-----------------------------------+
| #7       | Thermal Sensor          | Temperature data acquisition      |
|  Thermal |                         |                                   |
+----------+-------------------------+-----------------------------------+
| #7       | Battery Management      | Battery stats, charging control   |
+----------+-------------------------+-----------------------------------+
| #7       | Custom Power Control    | Power state transitions           |
+----------+-------------------------+-----------------------------------+

2.2 Generic Character Driver Template
---------------------------------------

**Standard Character Driver Pattern** (Used across multiple projects)::

    #include <linux/module.h>
    #include <linux/fs.h>
    #include <linux/cdev.h>
    #include <linux/device.h>
    #include <linux/uaccess.h>
    
    static struct class *dev_class;
    static struct cdev my_cdev;
    static dev_t dev_num;
    
    static int device_open(struct inode *inode, struct file *file)
    {
        pr_info("Device opened\n");
        return 0;
    }
    
    static int device_release(struct inode *inode, struct file *file)
    {
        pr_info("Device closed\n");
        return 0;
    }
    
    static ssize_t device_read(struct file *file, char __user *buf,
                                size_t count, loff_t *ppos)
    {
        /* Read hardware register/data */
        u32 data = readl(dev->regs + REG_OFFSET);
        
        if (copy_to_user(buf, &data, sizeof(data)))
            return -EFAULT;
        
        return sizeof(data);
    }
    
    static ssize_t device_write(struct file *file, const char __user *buf,
                                 size_t count, loff_t *ppos)
    {
        u32 data;
        
        if (copy_from_user(&data, buf, sizeof(data)))
            return -EFAULT;
        
        /* Write to hardware register */
        writel(data, dev->regs + REG_OFFSET);
        
        return sizeof(data);
    }
    
    static long device_ioctl(struct file *file, unsigned int cmd,
                              unsigned long arg)
    {
        switch (cmd) {
        case IOCTL_GET_STATUS:
            /* Get device status */
            break;
        case IOCTL_SET_CONFIG:
            /* Configure device */
            break;
        default:
            return -EINVAL;
        }
        return 0;
    }
    
    static const struct file_operations fops = {
        .owner = THIS_MODULE,
        .open = device_open,
        .release = device_release,
        .read = device_read,
        .write = device_write,
        .unlocked_ioctl = device_ioctl,
    };
    
    static int __init driver_init(void)
    {
        /* Allocate device number */
        alloc_chrdev_region(&dev_num, 0, 1, "mydevice");
        
        /* Create device class */
        dev_class = class_create(THIS_MODULE, "mydevice_class");
        
        /* Initialize cdev */
        cdev_init(&my_cdev, &fops);
        my_cdev.owner = THIS_MODULE;
        cdev_add(&my_cdev, dev_num, 1);
        
        /* Create device file */
        device_create(dev_class, NULL, dev_num, NULL, "mydevice");
        
        return 0;
    }

Section 3: Block Drivers & MTD
================================

3.1 MTD NAND Driver
--------------------

**Projects**: #2 (Avionics), #7 (Thermal - DaVinci)

**Features**:

===========================  ==================================================
MTD Feature                  Implementation
===========================  ==================================================
NAND Controller Driver       DaVinci NAND controller, custom timings
Bad Block Table (BBT)        Custom BBT descriptor for manufacturing
ECC (Error Correction)       Hardware BCH ECC (4-bit, 8-bit)
Partition Management         5-partition layout (U-Boot, kernel, rootfs, etc.)
JFFS2 Integration            Wear leveling, garbage collection tuning
===========================  ==================================================

**Driver Stack**::

    [Applications]
         ↓
    [JFFS2 Filesystem]
         ↓
    [MTD Core Layer (mtdblock, mtdchar)]
         ↓
    [MTD NAND Core]
         ↓
    [Custom NAND Controller Driver]  ← Developed
         ↓
    [NAND Hardware Controller]
         ↓
    [NAND Flash Chip]

**Custom BBT Implementation**::

    static uint8_t bbt_pattern[] = {'B', 'b', 't', '0'};
    static uint8_t mirror_pattern[] = {'1', 't', 'b', 'B'};
    
    static struct nand_bbt_descr custom_bbt_main = {
        .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE | 
                   NAND_BBT_WRITE | NAND_BBT_2BIT | 
                   NAND_BBT_VERSION,
        .offs = 8,
        .len = 4,
        .veroffs = 12,
        .maxblocks = 4,
        .pattern = bbt_pattern
    };
    
    static struct nand_bbt_descr custom_bbt_mirror = {
        .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE | 
                   NAND_BBT_WRITE | NAND_BBT_2BIT | 
                   NAND_BBT_VERSION,
        .offs = 8,
        .len = 4,
        .veroffs = 12,
        .maxblocks = 4,
        .pattern = mirror_pattern
    };
    
    /* NAND initialization */
    static int davinci_nand_probe(struct platform_device *pdev)
    {
        struct nand_chip *nand;
        struct mtd_info *mtd;
        
        /* Allocate structures */
        nand = devm_kzalloc(&pdev->dev, sizeof(*nand), GFP_KERNEL);
        mtd = nand_to_mtd(nand);
        
        /* Configure NAND chip */
        nand->chip_delay = 20;
        nand->options = NAND_USE_FLASH_BBT;
        nand->bbt_td = &custom_bbt_main;
        nand->bbt_md = &custom_bbt_mirror;
        
        /* Setup ECC */
        nand->ecc.mode = NAND_ECC_HW;
        nand->ecc.size = 512;
        nand->ecc.bytes = 10;  /* BCH-8 */
        nand->ecc.strength = 8;
        nand->ecc.hwctl = davinci_nand_ecc_hwctl;
        nand->ecc.calculate = davinci_nand_ecc_calculate;
        nand->ecc.correct = davinci_nand_ecc_correct;
        
        /* Scan NAND chip */
        nand_scan(mtd, 1);
        
        /* Register MTD device */
        mtd_device_register(mtd, partitions, nr_partitions);
        
        return 0;
    }

3.2 eMMC/SD Block Driver Configuration
----------------------------------------

**Projects**: #1 (IoT - i.MX93), #7 (Thermal - SD card)

**Driver Type**: Configuration and optimization of existing drivers (SDHCI)

**Optimizations**:

- HS200/HS400 mode enablement
- DMA configuration for performance
- Power management integration
- Wear leveling awareness

Section 4: Network Drivers
============================

4.1 Network Driver Portfolio
------------------------------

Network Drivers by Protocol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

====================  ================  =======================================
Protocol/Interface    Projects          Driver Type
====================  ================  =======================================
Wi-Fi (802.11)        #1, #2            Integration (Broadcom, Intel)
Bluetooth LE          #1                Integration (BlueZ stack)
Zigbee (802.15.4)     #1                Integration (wpan-tools)
CAN/SocketCAN         #2, #3, #6        Configuration (MCP2515 SPI-to-CAN)
AFDX (Avionics)       #2, #3            Integration & tuning
Ethernet (EMAC)       #7                Driver customization (DaVinci)
RF Custom Protocol    #7                Custom driver development
====================  ================  =======================================

4.2 DaVinci EMAC Driver Customization
---------------------------------------

**Project**: #7 (Thermal Imaging - video streaming)

**Customizations for Video Streaming**::

    static int thermal_emac_init(struct net_device *ndev)
    {
        struct thermal_emac_priv *priv = netdev_priv(ndev);
        
        /* Optimize for low-latency video */
        
        /* 1. Large MTU for video frames */
        ndev->mtu = 9000;  /* Jumbo frames */
        
        /* 2. Hardware offload */
        ndev->features |= NETIF_F_IP_CSUM | NETIF_F_SG | 
                          NETIF_F_TSO | NETIF_F_GSO;
        
        /* 3. Large DMA ring buffers */
        priv->num_rx_desc = 128;
        priv->num_tx_desc = 128;
        priv->rx_buffer_size = 9000;
        
        /* 4. Disable interrupt coalescing for low latency */
        priv->coal.rx_coalesce_usecs = 0;
        priv->coal.tx_coalesce_usecs = 0;
        
        /* 5. NAPI optimization */
        netif_napi_add(ndev, &priv->napi, thermal_emac_poll, 64);
        
        /* 6. Multicast for video streaming */
        ndev->flags |= IFF_MULTICAST;
        
        return 0;
    }
    
    /* Optimized NAPI poll for video packets */
    static int thermal_emac_poll(struct napi_struct *napi, int budget)
    {
        struct thermal_emac_priv *priv = container_of(napi, 
                                          struct thermal_emac_priv, napi);
        int work_done = 0;
        
        /* Process RX packets with priority for video UDP */
        while (work_done < budget) {
            struct sk_buff *skb = thermal_emac_rx(priv);
            if (!skb)
                break;
            
            /* Fast path for UDP video packets */
            if (skb->protocol == htons(ETH_P_IP)) {
                struct iphdr *iph = ip_hdr(skb);
                if (iph->protocol == IPPROTO_UDP) {
                    /* Priority deliver to video application */
                    netif_receive_skb(skb);
                    work_done++;
                    continue;
                }
            }
            
            /* Normal path for other packets */
            netif_receive_skb(skb);
            work_done++;
        }
        
        if (work_done < budget) {
            napi_complete(napi);
            enable_irq(priv->irq);
        }
        
        return work_done;
    }

**Performance Results**:

- **Bandwidth**: 90+ Mbps sustained (near wire speed for 100Mbps)
- **Latency**: < 50ms for video frames
- **Jitter**: < 5ms (critical for smooth video)
- **Packet Loss**: < 0.1% under normal conditions

4.3 SocketCAN Driver Integration
----------------------------------

**Projects**: #2 (Avionics), #3 (MDCLS), #6 (AUTOSAR E-Bike)

**CAN Controller**: MCP2515 (SPI-to-CAN)

**SocketCAN Configuration**::

    /* Device tree binding */
    &spi1 {
        can@0 {
            compatible = "microchip,mcp2515";
            reg = <0>;
            clocks = <&can_osc>;
            interrupt-parent = <&gpio1>;
            interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
            spi-max-frequency = <10000000>;
        };
    };
    
    /* Application: CAN send/receive */
    #include <linux/can.h>
    #include <linux/can/raw.h>
    
    int main()
    {
        int s;
        struct sockaddr_can addr;
        struct ifreq ifr;
        struct can_frame frame;
        
        /* Create CAN socket */
        s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
        
        /* Bind to can0 */
        strcpy(ifr.ifr_name, "can0");
        ioctl(s, SIOCGIFINDEX, &ifr);
        addr.can_family = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;
        bind(s, (struct sockaddr *)&addr, sizeof(addr));
        
        /* Send CAN frame (AUTOSAR diagnostic) */
        frame.can_id = 0x18DA10F1;  /* UDS diagnostic ID */
        frame.can_dlc = 8;
        frame.data[0] = 0x02;  /* Service ID: Read Data by ID */
        frame.data[1] = 0x01;
        frame.data[2] = 0x05;  /* PID */
        write(s, &frame, sizeof(frame));
        
        /* Receive CAN frame */
        read(s, &frame, sizeof(frame));
        
        return 0;
    }

Section 5: USB Drivers
========================

5.1 USB Bulk Driver (Custom)
------------------------------

**Project**: #7 (Thermal Imaging - configuration/control data)

**Purpose**: High-speed bulk transfers for thermal imaging control

**USB Bulk Driver Architecture**::

    [Thermal Control Application]
             ↓
    [Character Device Interface /dev/thermal_bulk]
             ↓
    [USB Bulk Driver] ← Custom developed
             ↓
    [USB Core (linux/usb.h)]
             ↓
    [DaVinci USB Controller (Mentor Graphics)]
             ↓
    [USB 2.0 High-Speed PHY]

**Implementation Details**::

    #define BULK_IN_EP     0x81
    #define BULK_OUT_EP    0x02
    #define BULK_BUF_SIZE  512
    
    struct thermal_bulk_dev {
        struct usb_device *udev;
        struct usb_interface *intf;
        struct usb_anchor submitted;
        
        /* Bulk endpoints */
        __u8 bulk_in_endpointAddr;
        __u8 bulk_out_endpointAddr;
        
        /* URBs for transfers */
        struct urb *bulk_in_urb;
        struct urb *bulk_out_urb;
        
        /* Buffers */
        unsigned char *bulk_in_buffer;
        unsigned char *bulk_out_buffer;
        size_t bulk_in_size;
        
        /* Character device */
        dev_t devt;
        struct cdev cdev;
        struct device *dev;
    };
    
    static int thermal_bulk_probe(struct usb_interface *intf,
                                   const struct usb_device_id *id)
    {
        struct usb_device *udev = interface_to_usbdev(intf);
        struct thermal_bulk_dev *dev;
        struct usb_endpoint_descriptor *bulk_in, *bulk_out;
        int i;
        
        /* Allocate device structure */
        dev = kzalloc(sizeof(*dev), GFP_KERNEL);
        dev->udev = usb_get_dev(udev);
        dev->intf = intf;
        init_usb_anchor(&dev->submitted);
        
        /* Find bulk endpoints */
        for (i = 0; i < intf->cur_altsetting->desc.bNumEndpoints; i++) {
            struct usb_endpoint_descriptor *ep = 
                &intf->cur_altsetting->endpoint[i].desc;
            
            if (usb_endpoint_is_bulk_in(ep))
                dev->bulk_in_endpointAddr = ep->bEndpointAddress;
            if (usb_endpoint_is_bulk_out(ep))
                dev->bulk_out_endpointAddr = ep->bEndpointAddress;
        }
        
        /* Allocate buffers */
        dev->bulk_in_size = BULK_BUF_SIZE;
        dev->bulk_in_buffer = kmalloc(dev->bulk_in_size, GFP_KERNEL);
        dev->bulk_out_buffer = kmalloc(BULK_BUF_SIZE, GFP_KERNEL);
        
        /* Create URBs */
        dev->bulk_in_urb = usb_alloc_urb(0, GFP_KERNEL);
        dev->bulk_out_urb = usb_alloc_urb(0, GFP_KERNEL);
        
        /* Register character device */
        alloc_chrdev_region(&dev->devt, 0, 1, "thermal_bulk");
        cdev_init(&dev->cdev, &thermal_bulk_fops);
        cdev_add(&dev->cdev, dev->devt, 1);
        
        usb_set_intfdata(intf, dev);
        
        return 0;
    }
    
    static ssize_t thermal_bulk_write(struct file *file,
                                       const char __user *user_buffer,
                                       size_t count, loff_t *ppos)
    {
        struct thermal_bulk_dev *dev = file->private_data;
        int retval;
        
        if (count > BULK_BUF_SIZE)
            count = BULK_BUF_SIZE;
        
        if (copy_from_user(dev->bulk_out_buffer, user_buffer, count))
            return -EFAULT;
        
        /* Setup bulk OUT transfer */
        usb_fill_bulk_urb(dev->bulk_out_urb, dev->udev,
                          usb_sndbulkpipe(dev->udev, dev->bulk_out_endpointAddr),
                          dev->bulk_out_buffer, count,
                          thermal_bulk_write_callback, dev);
        
        /* Submit URB */
        usb_anchor_urb(dev->bulk_out_urb, &dev->submitted);
        retval = usb_submit_urb(dev->bulk_out_urb, GFP_KERNEL);
        if (retval) {
            usb_unanchor_urb(dev->bulk_out_urb);
            return retval;
        }
        
        return count;
    }

5.2 USB Isochronous Driver (Custom)
-------------------------------------

**Project**: #7 (Thermal Imaging - real-time video streaming)

**Purpose**: Guaranteed bandwidth video streaming (30 FPS, 1.5 MB/s)

**Isochronous Transfer Characteristics**:

=========================  ================================================
Feature                    Value
=========================  ================================================
Transfer Type              Isochronous (guaranteed bandwidth, no retries)
Bandwidth                  1.5 MB/s sustained
Frame Rate                 30 FPS
Frame Size                 ~50 KB per frame
Packets per Frame          50 (1024 bytes each)
URBs in Flight             4 (for buffering)
Latency                    < 33ms (one frame time)
=========================  ================================================

**Isochronous Driver Implementation**::

    #define ISO_PACKETS_PER_URB  32
    #define NUM_ISO_URBS         4
    #define ISO_BUFFER_SIZE      (1024 * ISO_PACKETS_PER_URB)
    
    struct thermal_iso_dev {
        struct usb_device *udev;
        struct usb_interface *intf;
        
        /* Isochronous endpoint */
        __u8 iso_in_endpointAddr;
        unsigned int iso_packet_size;
        
        /* Multiple URBs for continuous streaming */
        struct urb *iso_urbs[NUM_ISO_URBS];
        unsigned char *iso_buffers[NUM_ISO_URBS];
        
        /* Video frame assembly */
        unsigned char *frame_buffer;
        size_t frame_size;
        int frame_complete;
        
        /* V4L2 integration */
        struct video_device *vdev;
    };
    
    static int thermal_iso_probe(struct usb_interface *intf,
                                  const struct usb_device_id *id)
    {
        struct usb_device *udev = interface_to_usbdev(intf);
        struct thermal_iso_dev *dev;
        struct usb_endpoint_descriptor *endpoint;
        int i, j;
        
        dev = kzalloc(sizeof(*dev), GFP_KERNEL);
        dev->udev = usb_get_dev(udev);
        dev->intf = intf;
        
        /* Find isochronous endpoint */
        endpoint = &intf->cur_altsetting->endpoint[0].desc;
        if (!usb_endpoint_xfer_isoc(endpoint))
            return -ENODEV;
        
        dev->iso_in_endpointAddr = endpoint->bEndpointAddress;
        dev->iso_packet_size = usb_endpoint_maxp(endpoint);
        
        /* Allocate URBs and buffers */
        for (i = 0; i < NUM_ISO_URBS; i++) {
            dev->iso_urbs[i] = usb_alloc_urb(ISO_PACKETS_PER_URB, GFP_KERNEL);
            dev->iso_buffers[i] = kmalloc(ISO_BUFFER_SIZE, GFP_KERNEL);
            
            /* Setup isochronous URB */
            dev->iso_urbs[i]->dev = udev;
            dev->iso_urbs[i]->pipe = usb_rcvisocpipe(udev, 
                                        dev->iso_in_endpointAddr);
            dev->iso_urbs[i]->transfer_flags = URB_ISO_ASAP;
            dev->iso_urbs[i]->transfer_buffer = dev->iso_buffers[i];
            dev->iso_urbs[i]->transfer_buffer_length = ISO_BUFFER_SIZE;
            dev->iso_urbs[i]->complete = thermal_iso_callback;
            dev->iso_urbs[i]->context = dev;
            dev->iso_urbs[i]->interval = 1;
            dev->iso_urbs[i]->number_of_packets = ISO_PACKETS_PER_URB;
            
            /* Setup individual packet descriptors */
            for (j = 0; j < ISO_PACKETS_PER_URB; j++) {
                dev->iso_urbs[i]->iso_frame_desc[j].offset = 
                    j * dev->iso_packet_size;
                dev->iso_urbs[i]->iso_frame_desc[j].length = 
                    dev->iso_packet_size;
            }
        }
        
        /* Submit all URBs to start streaming */
        for (i = 0; i < NUM_ISO_URBS; i++) {
            usb_submit_urb(dev->iso_urbs[i], GFP_KERNEL);
        }
        
        return 0;
    }
    
    static void thermal_iso_callback(struct urb *urb)
    {
        struct thermal_iso_dev *dev = urb->context;
        int i;
        
        if (urb->status != 0) {
            pr_err("ISO URB error: %d\n", urb->status);
            goto resubmit;
        }
        
        /* Process isochronous packets */
        for (i = 0; i < urb->number_of_packets; i++) {
            struct usb_iso_packet_descriptor *desc = 
                &urb->iso_frame_desc[i];
            unsigned char *data = urb->transfer_buffer + desc->offset;
            unsigned int len = desc->actual_length;
            
            if (desc->status != 0)
                continue;
            
            /* Assemble video frame from packets */
            if (len > 0) {
                memcpy(dev->frame_buffer + dev->frame_size, data, len);
                dev->frame_size += len;
                
                /* Check if frame is complete */
                if (thermal_is_frame_complete(dev)) {
                    /* Deliver frame to V4L2 layer */
                    thermal_deliver_frame(dev);
                    dev->frame_size = 0;
                }
            }
        }
        
    resubmit:
        /* Resubmit URB for continuous streaming */
        usb_submit_urb(urb, GFP_ATOMIC);
    }

**Interview Highlight**:
"Developed custom USB isochronous driver for real-time thermal video (30 FPS, 1.5 MB/s). Implemented 4-URB buffering to prevent frame drops, packet assembly into frames, and integration with V4L2. Achieved < 1% frame loss under normal conditions."

Section 6: Video4Linux2 (V4L2) Drivers
========================================

6.1 V4L2 Video Capture Driver
-------------------------------

**Projects**: #5 (FDVD - RTSP), #7 (Thermal - capture)

**V4L2 Driver Components**:

::

    [V4L2 Application (ffmpeg, gstreamer)]
             ↓
    [V4L2 Core (video_device, v4l2_dev)]
             ↓
    [Custom V4L2 Driver] ← Developed
             ├─ video_device registration
             ├─ v4l2_ioctl_ops (format, buffer management)
             ├─ v4l2_file_operations (open, close, mmap)
             └─ videobuf2 (DMA buffer management)
             ↓
    [Video Hardware (DaVinci VPFE, camera sensor)]

**V4L2 Driver Implementation** (Thermal)::

    static const struct v4l2_ioctl_ops thermal_v4l2_ioctl_ops = {
        /* Capability */
        .vidioc_querycap = thermal_v4l2_querycap,
        
        /* Format */
        .vidioc_enum_fmt_vid_cap = thermal_v4l2_enum_fmt,
        .vidioc_g_fmt_vid_cap = thermal_v4l2_get_fmt,
        .vidioc_s_fmt_vid_cap = thermal_v4l2_set_fmt,
        .vidioc_try_fmt_vid_cap = thermal_v4l2_try_fmt,
        
        /* Buffer management */
        .vidioc_reqbufs = vb2_ioctl_reqbufs,
        .vidioc_querybuf = vb2_ioctl_querybuf,
        .vidioc_qbuf = vb2_ioctl_qbuf,
        .vidioc_dqbuf = vb2_ioctl_dqbuf,
        
        /* Streaming */
        .vidioc_streamon = vb2_ioctl_streamon,
        .vidioc_streamoff = vb2_ioctl_streamoff,
        
        /* Controls */
        .vidioc_queryctrl = v4l2_ctrl_queryctrl,
        .vidioc_g_ctrl = v4l2_ctrl_g_ctrl,
        .vidioc_s_ctrl = v4l2_ctrl_s_ctrl,
    };
    
    static int thermal_v4l2_querycap(struct file *file, void *priv,
                                      struct v4l2_capability *cap)
    {
        strscpy(cap->driver, "thermal_v4l2", sizeof(cap->driver));
        strscpy(cap->card, "Thermal Imaging Camera", sizeof(cap->card));
        cap->device_caps = V4L2_CAP_VIDEO_CAPTURE | 
                           V4L2_CAP_STREAMING |
                           V4L2_CAP_READWRITE;
        cap->capabilities = cap->device_caps | V4L2_CAP_DEVICE_CAPS;
        return 0;
    }
    
    /* Videobuf2 queue operations */
    static const struct vb2_ops thermal_vb2_ops = {
        .queue_setup = thermal_vb2_queue_setup,
        .buf_prepare = thermal_vb2_buf_prepare,
        .buf_queue = thermal_vb2_buf_queue,
        .start_streaming = thermal_vb2_start_streaming,
        .stop_streaming = thermal_vb2_stop_streaming,
        .wait_prepare = vb2_ops_wait_prepare,
        .wait_finish = vb2_ops_wait_finish,
    };
    
    /* DMA buffer setup */
    static int thermal_vb2_queue_setup(struct vb2_queue *vq,
                                        unsigned int *nbuffers,
                                        unsigned int *nplanes,
                                        unsigned int sizes[],
                                        struct device *alloc_devs[])
    {
        struct thermal_v4l2_dev *dev = vb2_get_drv_priv(vq);
        unsigned long size = dev->fmt.sizeimage;
        
        if (*nplanes)
            return sizes[0] < size ? -EINVAL : 0;
        
        *nplanes = 1;
        sizes[0] = size;
        
        /* Use CMA for contiguous DMA buffers */
        alloc_devs[0] = dev->dev;
        
        return 0;
    }

**V4L2 Application Integration** (GStreamer pipeline)::

    # Capture thermal video and stream over network
    gst-launch-1.0 \
        v4l2src device=/dev/video0 ! \
        video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! \
        videoconvert ! \
        x264enc tune=zerolatency bitrate=2000 ! \
        rtph264pay ! \
        udpsink host=192.168.1.100 port=5004

Section 7: I2C & SPI Drivers
==============================

7.1 I2C Driver Integration
----------------------------

**I2C Devices Integrated**:

====================  ====================  ====================================
Device Type           Part Number           Projects
====================  ====================  ====================================
PMIC                  PCA9450C, TPS65xxx    #1 (IoT), #7 (Thermal)
Battery Fuel Gauge    BQ27441, MAX17048     #1, #7
Temperature Sensor    TMP102, LM75          #1, #7
IMU (Accel+Gyro)      MPU6050, LSM6DS3      #1, #7
RTC                   DS3231, PCF8563       Multiple projects
EEPROM                AT24Cxx               #2, #7
====================  ====================  ====================================

**Device Tree I2C Configuration** (comprehensive)::

    &lpi2c1 {
        #address-cells = <1>;
        #size-cells = <0>;
        clock-frequency = <400000>;  /* 400 kHz Fast Mode */
        status = "okay";
        
        /* PMIC */
        pmic@25 {
            compatible = "nxp,pca9450c";
            reg = <0x25>;
            pinctrl-0 = <&pinctrl_pmic>;
            interrupt-parent = <&gpio1>;
            interrupts = <3 IRQ_TYPE_LEVEL_LOW>;
            
            regulators {
                buck1: BUCK1 {
                    regulator-name = "VDDARM";
                    regulator-min-microvolt = <600000>;
                    regulator-max-microvolt = <2187500>;
                    regulator-boot-on;
                    regulator-always-on;
                    regulator-ramp-delay = <3125>;
                };
                /* Additional regulators... */
            };
        };
        
        /* Battery Fuel Gauge */
        bq27441@55 {
            compatible = "ti,bq27441";
            reg = <0x55>;
            monitored-battery = <&battery>;
        };
        
        /* Temperature Sensor */
        tmp102@48 {
            compatible = "ti,tmp102";
            reg = <0x48>;
            #thermal-sensor-cells = <0>;
        };
        
        /* IMU */
        mpu6050@68 {
            compatible = "invensense,mpu6050";
            reg = <0x68>;
            interrupt-parent = <&gpio1>;
            interrupts = <15 IRQ_TYPE_EDGE_RISING>;
            vdd-supply = <&reg_3v3>;
            vddio-supply = <&reg_3v3>;
        };
        
        /* RTC with backup battery */
        ds3231@68 {
            compatible = "maxim,ds3231";
            reg = <0x68>;
            interrupt-parent = <&gpio4>;
            interrupts = <5 IRQ_TYPE_EDGE_FALLING>;
        };
        
        /* EEPROM for calibration data */
        eeprom@50 {
            compatible = "atmel,24c256";
            reg = <0x50>;
            pagesize = <64>;
        };
    };

7.2 SPI Driver Integration
----------------------------

**SPI Devices Integrated**:

====================  ====================  ====================================
Device Type           Part Number           Projects
====================  ====================  ====================================
CAN Controller        MCP2515               #2, #6 (AUTOSAR)
SPI Flash             W25Q128, MX25L       #1, #2, #7
ADC                   MCP3008              #7 (analog inputs)
DAC                   MCP4922              #7 (control outputs)
Display Controller    ILI9341              #7 (optional display)
====================  ====================  ====================================

**SPI Device Tree Configuration**::

    &lpspi1 {
        #address-cells = <1>;
        #size-cells = <0>;
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_lpspi1>;
        cs-gpios = <&gpio1 10 GPIO_ACTIVE_LOW>,  /* CS0 */
                   <&gpio1 11 GPIO_ACTIVE_LOW>;  /* CS1 */
        status = "okay";
        
        /* CAN Controller */
        can@0 {
            compatible = "microchip,mcp2515";
            reg = <0>;
            clocks = <&can_osc>;
            interrupt-parent = <&gpio1>;
            interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
            spi-max-frequency = <10000000>;  /* 10 MHz */
        };
        
        /* SPI NOR Flash */
        flash@1 {
            compatible = "jedec,spi-nor";
            reg = <1>;
            spi-max-frequency = <20000000>;  /* 20 MHz */
            m25p,fast-read;
            
            partitions {
                compatible = "fixed-partitions";
                #address-cells = <1>;
                #size-cells = <1>;
                
                partition@0 {
                    label = "config";
                    reg = <0x0 0x100000>;  /* 1MB */
                };
                
                partition@100000 {
                    label = "data";
                    reg = <0x100000 0xf00000>;  /* 15MB */
                };
            };
        };
    };

Section 8: Power Management Drivers
=====================================

8.1 CPUFreq Driver Configuration
----------------------------------

**Projects**: #1 (IoT), #7 (Thermal)

**CPUFreq Governors Used**:

====================  ====================  ====================================
Governor              Projects              Use Case
====================  ====================  ====================================
schedutil             #1 (IoT)              Scheduler-driven DVFS
conservative          #7 (Thermal)          Battery-optimized gradual scaling
ondemand              Multiple              Performance-responsive scaling
performance           Development/debug     Maximum frequency always
powersave             Low-power modes       Minimum frequency always
====================  ====================  ====================================

8.2 Runtime Power Management
------------------------------

**Runtime PM Implementation Pattern**::

    static int device_runtime_suspend(struct device *dev)
    {
        struct my_device *mydev = dev_get_drvdata(dev);
        
        /* Stop device operations */
        device_stop(mydev);
        
        /* Disable clocks */
        clk_disable_unprepare(mydev->clk);
        
        /* Power off hardware */
        regulator_disable(mydev->supply);
        
        return 0;
    }
    
    static int device_runtime_resume(struct device *dev)
    {
        struct my_device *mydev = dev_get_drvdata(dev);
        
        /* Power on hardware */
        regulator_enable(mydev->supply);
        
        /* Enable clocks */
        clk_prepare_enable(mydev->clk);
        
        /* Resume device operations */
        device_start(mydev);
        
        return 0;
    }
    
    static const struct dev_pm_ops device_pm_ops = {
        SET_RUNTIME_PM_OPS(device_runtime_suspend,
                           device_runtime_resume, NULL)
        SET_SYSTEM_SLEEP_PM_OPS(device_suspend, device_resume)
    };

Summary: Driver Development Portfolio
=======================================

**Driver Type Distribution**:

=========================  ==========  =======================================
Driver Category            Count       Complexity
=========================  ==========  =======================================
Platform (custom)          5+          High (PCIe multi-RC, FPGA)
Character                  10+         Medium-High
Block/MTD                  3           High (custom BBT, ECC)
Network                    8+          High (custom protocols, video tuning)
USB                        3           Very High (bulk, isochronous custom)
Video (V4L2)               2           Very High (DMA, DSP integration)
I2C (integrated)           10+         Low-Medium
SPI (integrated)           5+          Low-Medium
Power Management           Multiple    Medium
=========================  ==========  =======================================

**Total Drivers**: 50+ devices integrated/developed

**Interview Summary Statement**:
"I have developed/integrated 50+ Linux device drivers across 15 categories: custom PCIe platform driver for multi-RC SOC, USB bulk/isochronous for thermal video streaming, V4L2 with videobuf2 and DSP integration, MTD/NAND with custom BBT, network drivers (EMAC optimization for video, SocketCAN, Wi-Fi/BT/Zigbee), and 10+ I2C/SPI device integrations. Strong expertise in DMA, interrupt handling, power management, and device tree bindings."

End of Document
================

**Last Updated**: January 22, 2026
**Total Driver Types**: 15+
**Total Devices**: 50+
**Projects Span**: 18+ years

© 2026 Madhavan Vivekanandan - All Rights Reserved
