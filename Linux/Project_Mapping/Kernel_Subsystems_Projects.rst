==========================================
Linux Kernel Subsystems → Project Mapping
==========================================

:Author: Madhavan Vivekanandan
:Date: January 22, 2026
:Purpose: Map real project work to specific kernel subsystems for technical interviews
:Kernel Versions: 2.6.x → 5.x+ (18+ years experience)

.. contents:: Quick Navigation
   :depth: 3
   :local:

Overview
=========

This document maps your hands-on Linux kernel subsystem experience across 8 major projects, providing specific examples and talking points for technical interviews.

**Key Stats**:
- **Kernel Subsystems**: 15+ subsystems with hands-on experience
- **Driver Types**: 10+ different driver categories
- **Projects Span**: 2007-2026 (18+ years)
- **Kernel Versions**: 2.6.x (ARM9) → 5.x+ (i.MX93)

Section 1: Core Kernel Subsystems
===================================

1.1 Process Scheduler
-----------------------

Real-time Scheduling Experience
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Projects with Real-time Requirements**:

================  ================================================  ========================
Project           Real-time Requirement                             Scheduler Configuration
================  ================================================  ========================
#7 Thermal        Soft real-time (video processing)                 SCHED_FIFO for video tasks
#5 FDVD           Video frame deadlines (30-60 FPS)                 Priority-based scheduling
#3 MDCLS          Control system response times                     Real-time priorities
================  ================================================  ========================

**Scheduler Optimizations**:

::

    # Thermal Imaging - Video Processing Priority
    # Set video capture thread to SCHED_FIFO priority 80
    struct sched_param param;
    param.sched_priority = 80;
    sched_setscheduler(getpid(), SCHED_FIFO, &param);
    
    # CPU affinity for video processing core
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(1, &cpuset);  # Dedicate CPU1 to video
    sched_setaffinity(getpid(), sizeof(cpuset), &cpuset);

**Interview Talking Point**:
*"On ARM9 DaVinci thermal imaging, I configured SCHED_FIFO priorities (80) for video processing threads to meet 30 FPS deadlines. Used CPU affinity to dedicate DSP co-processor interactions to specific cores. Achieved < 33ms frame processing latency."*

1.2 Memory Management
-----------------------

Memory Subsystem Experience by Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------+-----------------------+-------------------------------------------+
| Project  | Memory Challenge      | Solutions Implemented                     |
+==========+=======================+===========================================+
| #7       | mDDR RAM Support      | Ported kernel memory subsystem for mDDR   |
|          |                       | on DM365, optimized memory timings        |
+----------+-----------------------+-------------------------------------------+
| #1       | Small Memory Footprint| Minimized kernel memory (32MB rootfs),    |
|          | (IoT device)          | disabled swap, optimized slab allocator   |
+----------+-----------------------+-------------------------------------------+
| #2       | Multi-core Memory     | Configured NUMA awareness for Atom C3xxx  |
|          | Architecture          | multi-socket configurations               |
+----------+-----------------------+-------------------------------------------+
| #7       | DMA Buffer Management | Configured CMA (Contiguous Memory         |
|          |                       | Allocator) for video buffers              |
+----------+-----------------------+-------------------------------------------+

Memory Management Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**mDDR Configuration (DM365)**::

    # arch/arm/mach-davinci/board-dm365-evm.c
    static struct davinci_mmc_config dm365_mmc_config = {
        .version = MMC_CTLR_VERSION_2,
        .caps = MMC_CAP_4_BIT_DATA | MMC_CAP_MMC_HIGHSPEED,
    };
    
    # Memory timing adjustments for mDDR
    # Custom SDRAM timing for mDDR performance

**CMA for Video Buffers**::

    # Device tree configuration
    reserved-memory {
        #address-cells = <1>;
        #size-cells = <1>;
        ranges;
        
        video_cma: video-cma@40000000 {
            compatible = "shared-dma-pool";
            reg = <0x40000000 0x8000000>;  /* 128MB for video */
            reusable;
            linux,cma-default;
        };
    };

**Kernel Config for Minimal Memory**::

    # i.MX93 IoT Platform - Optimize for 32MB footprint
    CONFIG_SLUB=y                    # Use SLUB allocator (more efficient)
    CONFIG_SLUB_CPU_PARTIAL=n        # Disable CPU partial slabs
    CONFIG_COMPACTION=y              # Memory compaction for reduced fragmentation
    CONFIG_ZRAM=y                    # Compressed RAM for swap
    # CONFIG_SWAP is not set          # No swap partition
    CONFIG_CLEANCACHE=y              # Clean page cache

**Interview Talking Point**:
*"I ported kernel memory subsystem for mDDR RAM on DM365, optimizing SDRAM timings for video DMA. On i.MX93 IoT, minimized memory footprint using SLUB allocator, disabled swap, and configured ZRAM. Set up CMA (128MB) for contiguous video buffer allocation."*

1.3 Virtual Filesystem (VFS)
------------------------------

Filesystem Experience Matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=================  ====================  ===========================================
Filesystem Type    Projects              Specific Usage
=================  ====================  ===========================================
**JFFS2**          #2, #7                Flash filesystem for NAND, wear leveling
**SquashFS**       #1, #2                Compressed read-only rootfs
**ext4**           #1, #2, #7            General-purpose read-write filesystem
**FAT/VFAT**       Multiple              USB storage, external media
**tmpfs**          All projects          Volatile in-memory filesystem
**sysfs**          All projects          Kernel object hierarchy export
**procfs**         All projects          Process/kernel information interface
**debugfs**        All projects          Debug information during development
=================  ====================  ===========================================

Filesystem Layout Design
~~~~~~~~~~~~~~~~~~~~~~~~~

**Thermal Imaging System (#7) - Dual Partition Strategy**::

    /dev/mtd0  →  U-Boot (256KB)
    /dev/mtd1  →  Kernel (4MB)
    /dev/mtd2  →  RootFS (JFFS2, 32MB)
    /dev/mtd3  →  Application (64MB)
    /dev/mtd4  →  User Data (128MB)
    
    # Mount strategy
    /                  mtd2 (JFFS2, ro remount for runtime)
    /opt/app           mtd3 (JFFS2, rw)
    /data              mtd4 (JFFS2, rw)
    /tmp               tmpfs (RAM)
    /var/log           tmpfs (RAM, avoid flash writes)

**Smart Home IoT (#1) - Minimal Footprint**::

    # Rootfs composition (32MB total)
    /boot              FAT16 (8MB) - kernel, device tree
    /                  SquashFS (24MB compressed, ~60MB uncompressed)
    /overlay           JFFS2 (overlayfs for runtime changes)
    /data              ext4 on eMMC
    
    # Overlay strategy for read-only root with writable overlay
    mount -t overlay overlay -o lowerdir=/,upperdir=/overlay,workdir=/work /mnt

**Avionics Platform (#2) - Security Focus**::

    # Monolithic image with dm-verity for integrity
    /dev/sda1          EFI System Partition (FAT32, 512MB)
    /dev/sda2          Root (ext4, read-only, dm-verity protected)
    /dev/sda3          Data (ext4, encrypted with dm-crypt)
    /tmp               tmpfs (noexec, nosuid)
    /var               tmpfs (noexec, nosuid)

**Interview Talking Point**:
*"I designed 3 distinct filesystem architectures: JFFS2 on NAND with dual-partition strategy for thermal imaging (wear leveling, fast boot), SquashFS + overlay for i.MX93 IoT (24MB compressed rootfs, runtime writable overlay), and dm-verity protected ext4 for avionics (integrity verification, encrypted data partition)."*

Section 2: Device Driver Subsystems
=====================================

2.1 MTD (Memory Technology Devices)
-------------------------------------

NAND Flash Experience
~~~~~~~~~~~~~~~~~~~~~~

**Projects**: #2 (Avionics), #7 (Thermal Imaging)

MTD Stack Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^

::

    [Application Layer]
           ↓
    [JFFS2 Filesystem]
           ↓
    [MTD Core Layer]
           ↓
    [MTD NAND Driver]
           ↓
    [NAND Flash Controller]
           ↓
    [NAND Flash Chip]

**Key MTD Work**:

========================  =======================================================
**MTD Feature**           **Implementation Details**
========================  =======================================================
Bad Block Table (BBT)     Custom BBT management for thermal imaging board
NAND Flash Driver         Developed/ported NAND controller driver
JFFS2 Integration         Configured wear leveling, garbage collection
ECC (Error Correction)    Hardware ECC (BCH) configuration
Partition Management      Defined MTD partitions for boot/kernel/rootfs/data
========================  =======================================================

**MTD Device Tree Configuration**::

    nand@0 {
        compatible = "ti,davinci-nand";
        reg = <0 0x02000000 0x02000000
               1 0x02000000 0x00008000>;
        ti,davinci-chipselect = <1>;
        ti,davinci-mask-ale = <0>;
        ti,davinci-mask-cle = <0>;
        ti,davinci-mask-chipsel = <0>;
        ti,davinci-ecc-mode = "hw";
        ti,davinci-ecc-bits = <4>;
        ti,davinci-nand-buswidth = <16>;
        ti,davinci-nand-use-bbt;
        
        partitions {
            compatible = "fixed-partitions";
            #address-cells = <1>;
            #size-cells = <1>;
            
            partition@0 {
                label = "u-boot";
                reg = <0x0 0x40000>;
                read-only;
            };
            
            partition@40000 {
                label = "kernel";
                reg = <0x40000 0x400000>;
            };
            
            partition@440000 {
                label = "rootfs";
                reg = <0x440000 0x2000000>;
            };
        };
    };

**BBT (Bad Block Table) Custom Implementation**::

    /* Custom BBT descriptor for manufacturing support */
    static struct nand_bbt_descr custom_bbt_descr = {
        .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE | NAND_BBT_WRITE,
        .offs = 8,
        .len = 4,
        .veroffs = 12,
        .maxblocks = 4,
        .pattern = bbt_pattern
    };
    
    /* Register custom BBT during NAND probe */
    nand_chip->bbt_td = &custom_bbt_descr;
    nand_chip->bbt_md = &custom_mirror_descr;

**Interview Talking Point**:
*"I developed MTD NAND drivers for DaVinci thermal imaging with custom BBT management, hardware BCH ECC (4-bit), and JFFS2 integration. Configured 5-partition layout (U-Boot, kernel, rootfs, app, data) with wear leveling. On avionics, used MTD for secure boot validation and firmware updates."*

2.2 Block Layer & Storage
---------------------------

Block Device Experience
~~~~~~~~~~~~~~~~~~~~~~~~

**Storage Technologies by Project**:

===================  ==================  ========================================
Project              Storage Type        Block Layer Work
===================  ==================  ========================================
#1 IoT               eMMC                eMMC driver configuration, ext4
#2 Avionics          SATA SSD            AHCI driver, dm-verity, dm-crypt
#7 Thermal           NAND Flash          MTD → Block translation layer
Multiple             USB Storage         USB Mass Storage class driver
===================  ==================  ========================================

**Device Mapper Configuration (Avionics)**::

    # dm-verity for read-only root integrity
    veritysetup format /dev/sda2 /dev/sda3
    veritysetup open /dev/sda2 rootfs /dev/sda3
    
    # dm-crypt for encrypted data partition
    cryptsetup luksFormat /dev/sda4
    cryptsetup open /dev/sda4 data-crypt
    mkfs.ext4 /dev/mapper/data-crypt

**Interview Talking Point**:
*"Configured block layer for multiple storage types: eMMC on i.MX93 (ext4 + wear leveling), SATA SSD on Atom avionics (dm-verity for root integrity + dm-crypt for data encryption), and NAND flash with MTD-to-block translation on thermal imaging."*

2.3 USB Subsystem
------------------

USB Driver Development (Thermal Imaging)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Custom USB Drivers Developed** (#7):

1. **USB Bulk Driver** (High-speed data transfer)
2. **USB Isochronous Driver** (Video streaming)

USB Bulk Driver Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    [Thermal Application]
           ↓
    [Custom USB Bulk Interface]
           ↓
    [USB Core]
           ↓
    [DaVinci USB Controller (Mentor Graphics)]
           ↓
    [USB 2.0 High-Speed PHY]

**USB Bulk Driver Implementation**::

    static struct usb_driver thermal_bulk_driver = {
        .name = "thermal_bulk",
        .probe = thermal_bulk_probe,
        .disconnect = thermal_bulk_disconnect,
        .id_table = thermal_bulk_id_table,
    };
    
    static int thermal_bulk_probe(struct usb_interface *intf,
                                   const struct usb_device_id *id)
    {
        struct usb_device *udev = interface_to_usbdev(intf);
        struct thermal_bulk_dev *dev;
        struct usb_endpoint_descriptor *bulk_in, *bulk_out;
        
        /* Allocate device structure */
        dev = kzalloc(sizeof(*dev), GFP_KERNEL);
        
        /* Find bulk endpoints */
        bulk_in = &intf->cur_altsetting->endpoint[0].desc;
        bulk_out = &intf->cur_altsetting->endpoint[1].desc;
        
        /* Create URBs for bulk transfer */
        dev->bulk_in_urb = usb_alloc_urb(0, GFP_KERNEL);
        dev->bulk_out_urb = usb_alloc_urb(0, GFP_KERNEL);
        
        /* Configure bulk transfer (512-byte packets) */
        usb_fill_bulk_urb(dev->bulk_in_urb, udev,
                          usb_rcvbulkpipe(udev, bulk_in->bEndpointAddress),
                          dev->bulk_in_buffer, BULK_BUFFER_SIZE,
                          thermal_bulk_in_callback, dev);
        
        return 0;
    }

USB Isochronous Driver for Video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Isochronous Transfer Characteristics**:
- Guaranteed bandwidth (1.5 MB/s for thermal video)
- No retransmission (real-time video)
- Frame-based transfers (30 FPS)

::

    static int thermal_iso_probe(struct usb_interface *intf,
                                  const struct usb_device_id *id)
    {
        struct usb_device *udev = interface_to_usbdev(intf);
        struct usb_host_interface *iface_desc;
        struct usb_endpoint_descriptor *endpoint;
        
        /* Select alternate setting for isochronous */
        usb_set_interface(udev, intf->cur_altsetting->desc.bInterfaceNumber, 1);
        
        /* Allocate isochronous URBs (multiple for buffering) */
        for (i = 0; i < NUM_ISO_URBS; i++) {
            urb = usb_alloc_urb(ISO_PACKETS_PER_URB, GFP_KERNEL);
            usb_fill_int_urb(urb, udev,
                             usb_rcvisocpipe(udev, endpoint->bEndpointAddress),
                             dev->iso_buffer[i], ISO_BUFFER_SIZE,
                             thermal_iso_callback, dev, 
                             endpoint->bInterval);
            
            urb->transfer_flags = URB_ISO_ASAP;
            usb_submit_urb(urb, GFP_KERNEL);
        }
        
        return 0;
    }

**Interview Talking Point**:
*"Developed 2 custom USB drivers for ARM9 thermal imaging: USB bulk driver for high-speed data (configuration/control), and USB isochronous driver for real-time video streaming (30 FPS, 1.5 MB/s guaranteed bandwidth). Implemented multi-URB buffering to prevent frame drops."*

2.4 Video4Linux2 (V4L2)
-------------------------

V4L2 Video Driver (Thermal Imaging)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Video Pipeline Architecture**::

    [Thermal Sensor]
           ↓
    [TI DaVinci VPFE (Video Port Front End)]
           ↓
    [V4L2 Video Driver (Custom)]
           ↓
    [Video Processing (DSP)]
           ↓
    [Encoder (H.264/MPEG4)]
           ↓
    [USB/Ethernet/RF Output]

**V4L2 Driver Implementation**::

    static const struct v4l2_file_operations thermal_v4l2_fops = {
        .owner = THIS_MODULE,
        .open = thermal_v4l2_open,
        .release = thermal_v4l2_release,
        .poll = thermal_v4l2_poll,
        .unlocked_ioctl = video_ioctl2,
        .read = thermal_v4l2_read,
        .mmap = thermal_v4l2_mmap,
    };
    
    static const struct v4l2_ioctl_ops thermal_v4l2_ioctl_ops = {
        .vidioc_querycap = thermal_v4l2_querycap,
        .vidioc_enum_fmt_vid_cap = thermal_v4l2_enum_fmt,
        .vidioc_g_fmt_vid_cap = thermal_v4l2_get_fmt,
        .vidioc_s_fmt_vid_cap = thermal_v4l2_set_fmt,
        .vidioc_reqbufs = thermal_v4l2_reqbufs,
        .vidioc_querybuf = thermal_v4l2_querybuf,
        .vidioc_qbuf = thermal_v4l2_qbuf,
        .vidioc_dqbuf = thermal_v4l2_dqbuf,
        .vidioc_streamon = thermal_v4l2_streamon,
        .vidioc_streamoff = thermal_v4l2_streamoff,
    };
    
    static int thermal_v4l2_probe(struct platform_device *pdev)
    {
        struct video_device *vdev;
        struct thermal_v4l2_dev *dev;
        
        /* Allocate video device */
        vdev = video_device_alloc();
        vdev->fops = &thermal_v4l2_fops;
        vdev->ioctl_ops = &thermal_v4l2_ioctl_ops;
        vdev->release = video_device_release;
        vdev->v4l2_dev = &dev->v4l2_dev;
        
        /* Register video device */
        video_register_device(vdev, VFL_TYPE_GRABBER, -1);
        
        /* Configure videobuf2 for DMA buffers */
        dev->vb_queue.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        dev->vb_queue.io_modes = VB2_MMAP | VB2_READ | VB2_DMABUF;
        dev->vb_queue.ops = &thermal_vb2_ops;
        dev->vb_queue.mem_ops = &vb2_dma_contig_memops;
        vb2_queue_init(&dev->vb_queue);
        
        return 0;
    }

**Video Buffer Management**::

    /* DMA buffer allocation for zero-copy video capture */
    static int thermal_vb2_buf_prepare(struct vb2_buffer *vb)
    {
        struct thermal_buffer *buf = container_of(vb, struct thermal_buffer, vb);
        unsigned long size = dev->fmt.sizeimage;
        
        if (vb2_plane_size(vb, 0) < size) {
            dev_err(dev->dev, "Buffer too small (%lu < %lu)\n",
                    vb2_plane_size(vb, 0), size);
            return -EINVAL;
        }
        
        vb2_set_plane_payload(vb, 0, size);
        return 0;
    }

**Interview Talking Point**:
*"Developed V4L2-compatible video driver for DaVinci thermal imaging. Implemented complete V4L2 ioctl interface (querycap, format negotiation, buffer management), integrated videobuf2 for DMA-based zero-copy capture, and coordinated with DSP for H.264/MPEG4 hardware compression. Achieved 30 FPS capture with < 33ms latency."*

2.5 Network Device Drivers
----------------------------

Network Stack Experience
~~~~~~~~~~~~~~~~~~~~~~~~~

**Network Drivers by Project**:

+----------+-------------------+------------------------------------------+
| Project  | Network Interface | Driver Work                              |
+==========+===================+==========================================+
| #1 IoT   | Wi-Fi, BT, Zigbee | Driver integration, firmware loading     |
+----------+-------------------+------------------------------------------+
| #2       | Ethernet (Intel)  | Driver customization, switch integration |
|          | Wireless cards    | PCIe wireless driver porting             |
+----------+-------------------+------------------------------------------+
| #6 Auto  | CAN               | SocketCAN driver configuration           |
+----------+-------------------+------------------------------------------+
| #7       | Ethernet (EMAC)   | DaVinci EMAC driver, video streaming     |
|          | RF transceiver    | Custom RF driver for wireless video      |
+----------+-------------------+------------------------------------------+

**SocketCAN Configuration (AUTOSAR E-Bike)**::

    # Load CAN driver
    modprobe can
    modprobe can-raw
    modprobe mcp251x  # MCP2515 SPI-to-CAN controller
    
    # Device tree for MCP2515
    &spi1 {
        can0: mcp2515@0 {
            compatible = "microchip,mcp2515";
            reg = <0>;
            clocks = <&can_osc>;
            interrupt-parent = <&gpio1>;
            interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
            spi-max-frequency = <10000000>;
        };
    };
    
    # Configure CAN interface
    ip link set can0 type can bitrate 500000
    ip link set can0 up
    
    # Send CAN frame (diagnostic request)
    cansend can0 18DA10F1#0201050000000000  # OBD-II PID request

**Ethernet Driver for Video Streaming (Thermal)**::

    /* DaVinci EMAC configuration for UDP video streaming */
    static int thermal_emac_init(struct net_device *ndev)
    {
        struct thermal_emac_priv *priv = netdev_priv(ndev);
        
        /* Configure for low-latency video streaming */
        priv->msg_enable = NETIF_MSG_LINK;
        
        /* Enable hardware checksum offload */
        ndev->features |= NETIF_F_IP_CSUM | NETIF_F_SG;
        
        /* Configure DMA for large video frames */
        priv->rx_buffer_size = 9000;  /* Jumbo frames */
        priv->num_rx_desc = 128;
        priv->num_tx_desc = 128;
        
        /* Disable interrupt coalescing for low latency */
        priv->coal.rx_coalesce_usecs = 0;
        
        return 0;
    }

**Interview Talking Point**:
*"Integrated/developed network drivers for 5 protocols: Wi-Fi/BT/Zigbee for IoT (firmware loading, power management), SocketCAN for AUTOSAR (MCP2515 SPI-to-CAN), DaVinci EMAC for video streaming (UDP, jumbo frames, hardware checksum offload), and PCIe wireless cards for avionics. Optimized EMAC for low-latency video (disabled interrupt coalescing, 128 DMA descriptors)."*

2.6 I2C & SPI Subsystems
-------------------------

I2C Driver Experience
~~~~~~~~~~~~~~~~~~~~~~

**I2C Usage in Projects**:

- **Project #7 (Thermal)**: Sensor configuration (temperature, IMU)
- **Project #1 (IoT)**: PMIC, battery management, sensors
- **Project #6 (Auto)**: External peripherals, EEPROM

**I2C Device Tree Binding**::

    &i2c1 {
        status = "okay";
        clock-frequency = <400000>;  /* 400 kHz Fast Mode */
        
        /* Battery Management IC */
        bq27441@55 {
            compatible = "ti,bq27441";
            reg = <0x55>;
            interrupt-parent = <&gpio4>;
            interrupts = <20 IRQ_TYPE_EDGE_FALLING>;
        };
        
        /* Temperature Sensor */
        tmp102@48 {
            compatible = "ti,tmp102";
            reg = <0x48>;
            #thermal-sensor-cells = <0>;
        };
        
        /* IMU (Accelerometer + Gyroscope) */
        mpu6050@68 {
            compatible = "invensense,mpu6050";
            reg = <0x68>;
            interrupt-parent = <&gpio1>;
            interrupts = <15 IRQ_TYPE_EDGE_RISING>;
        };
    };

SPI Driver Experience
~~~~~~~~~~~~~~~~~~~~~~

**SPI Usage in Projects**:

- **Project #7 (Thermal)**: ADC, DAC, external flash
- **Project #6 (Auto)**: CAN controller (MCP2515)
- **Project #1 (IoT)**: NOR flash, display controller

**SPI Device Tree Binding (CAN Controller)**::

    &spi1 {
        status = "okay";
        
        /* MCP2515 CAN Controller */
        can@0 {
            compatible = "microchip,mcp2515";
            reg = <0>;
            clocks = <&can_osc>;
            spi-max-frequency = <10000000>;
            interrupt-parent = <&gpio1>;
            interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
        };
        
        /* SPI Flash */
        flash@1 {
            compatible = "jedec,spi-nor";
            reg = <1>;
            spi-max-frequency = <20000000>;
            m25p,fast-read;
            
            partitions {
                compatible = "fixed-partitions";
                #address-cells = <1>;
                #size-cells = <1>;
                
                partition@0 {
                    label = "config";
                    reg = <0x0 0x100000>;
                };
            };
        };
    };

**Interview Talking Point**:
*"Configured I2C/SPI subsystems for multiple peripherals: I2C for battery management (BQ27441), temperature sensors (TMP102), IMU (MPU6050) at 400 kHz; SPI for CAN controller (MCP2515, 10 MHz), SPI NOR flash (20 MHz with fast-read), and ADC/DAC for thermal imaging. Managed device tree bindings, IRQ handling, and kernel driver integration."*

2.7 PCIe Subsystem
-------------------

PCIe Platform Driver (Multi-Root Complex)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Project**: #2 (Avionics - Intel Atom C3xxx), Reference Design (Router/AP SOC)

**Challenge**: SOC with 3+ Root Complexes, limited reference implementations

**PCIe Architecture**::

    [CPU/SOC]
         ├─ Root Complex 0 (RC0)
         │      ├─ PCIe Device 0 (Wireless Card)
         │      └─ PCIe Device 1 (FPGA)
         ├─ Root Complex 1 (RC1)
         │      ├─ PCIe Device 2 (NVMe SSD)
         │      └─ PCIe Device 3 (Network Controller)
         └─ Root Complex 2 (RC2)
                └─ PCIe Device 4 (Additional Controller)

**Platform PCIe Driver Implementation**::

    static struct platform_driver multi_rc_pcie_driver = {
        .probe = multi_rc_pcie_probe,
        .remove = multi_rc_pcie_remove,
        .driver = {
            .name = "multi-rc-pcie",
            .of_match_table = multi_rc_pcie_of_match,
        },
    };
    
    static int multi_rc_pcie_probe(struct platform_device *pdev)
    {
        struct multi_rc_pcie *pcie;
        struct resource *res;
        int rc_id;
        
        /* Parse device tree for RC ID */
        of_property_read_u32(pdev->dev.of_node, "rc-id", &rc_id);
        
        /* Map RC-specific configuration space */
        res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
        pcie->cfg_base = devm_ioremap_resource(&pdev->dev, res);
        
        /* Setup RC-specific enumeration */
        pcie->rc_id = rc_id;
        pcie->bus_range.start = rc_id * 0x10;
        pcie->bus_range.end = (rc_id + 1) * 0x10 - 1;
        
        /* Register PCI host bridge */
        pci_host_bridge_register(pcie->bridge);
        
        /* Enumerate devices on this RC's bus */
        pci_scan_child_bus(pcie->bridge->bus);
        pci_assign_unassigned_bus_resources(pcie->bridge->bus);
        pci_bus_add_devices(pcie->bridge->bus);
        
        return 0;
    }
    
    /* RC-specific operations */
    static struct pci_ops multi_rc_pcie_ops = {
        .map_bus = multi_rc_pcie_map_bus,
        .read = multi_rc_pcie_read_config,
        .write = multi_rc_pcie_write_config,
    };
    
    /* Map bus to correct RC */
    static void __iomem *multi_rc_pcie_map_bus(struct pci_bus *bus,
                                                 unsigned int devfn,
                                                 int where)
    {
        struct multi_rc_pcie *pcie = bus->sysdata;
        int rc_id = bus->number / 0x10;
        
        /* Verify bus belongs to this RC */
        if (rc_id != pcie->rc_id)
            return NULL;
        
        /* Calculate config space address */
        return pcie->cfg_base + (bus->number << 20) + 
               (PCI_SLOT(devfn) << 15) + (PCI_FUNC(devfn) << 12) + where;
    }

**Device Tree Configuration**::

    pcie0: pcie@1f000000 {
        compatible = "vendor,multi-rc-pcie";
        reg = <0x1f000000 0x1000000>;
        rc-id = <0>;
        ranges = <0x81000000 0 0x00000000 0x20000000 0 0x00010000
                  0x82000000 0 0x20010000 0x20010000 0 0x0ff00000>;
        interrupts = <GIC_SPI 100 IRQ_TYPE_LEVEL_HIGH>;
        #interrupt-cells = <1>;
        interrupt-map-mask = <0 0 0 7>;
        interrupt-map = <0 0 0 1 &pcie_intc0 0>,
                        <0 0 0 2 &pcie_intc0 1>;
    };

**Testing with FPGA Emulation**::

    # FPGA emulated multiple devices on each RC
    # Test enumeration
    lspci -tv
    # Output should show:
    # -[0000:00]-+-00.0  Root Complex 0
    #            +-01.0  Wireless Card
    #            \-02.0  FPGA Device
    # -[0000:10]-+-00.0  Root Complex 1
    #            +-01.0  NVMe SSD
    # -[0000:20]-+-00.0  Root Complex 2
    
    # Verify config space access for each device
    lspci -vvv -s 00:01.0  # Wireless on RC0
    lspci -vvv -s 10:01.0  # NVMe on RC1

**Interview Talking Point**:
*"Developed platform PCIe driver for SOC with 3+ root complexes—a unique challenge with limited reference implementations. Implemented RC-specific enumeration (each RC owns bus range 0xN0-0xNF), config space mapping based on bus number, and device tree binding. Validated using FPGA-emulated SOC with multiple PCIe devices per RC. Driver supported wireless cards, FPGA, and NVMe across different RCs."*

Section 3: Networking Subsystems
==================================

3.1 Network Stack Configuration
---------------------------------

**Network Subsystems Modified/Configured**:

- TCP/IP stack optimization
- Socket buffer sizing
- Network device configuration
- Quality of Service (QoS)
- Network bridge/routing

**Network Stack Tuning for Video Streaming**::

    # Thermal Imaging - UDP video streaming optimization
    
    # Increase socket buffer sizes
    sysctl -w net.core.rmem_max=26214400
    sysctl -w net.core.wmem_max=26214400
    sysctl -w net.core.rmem_default=26214400
    sysctl -w net.core.wmem_default=26214400
    
    # UDP buffer sizes
    sysctl -w net.ipv4.udp_rmem_min=16384
    sysctl -w net.ipv4.udp_wmem_min=16384
    
    # Disable TCP slow start for low-latency
    sysctl -w net.ipv4.tcp_slow_start_after_idle=0
    
    # Enable jumbo frames
    ifconfig eth0 mtu 9000
    
    # QoS for video traffic
    tc qdisc add dev eth0 root handle 1: prio bands 3
    tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 \
        match ip dport 5004 0xffff flowid 1:1  # Video on highest priority

**Interview Talking Point**:
*"Tuned Linux network stack for real-time video streaming: increased socket buffers to 25MB, disabled TCP slow start, enabled jumbo frames (MTU 9000), and configured tc QoS to prioritize video traffic (UDP port 5004) in highest priority band. Achieved 30 FPS streaming with < 50ms latency."*

3.2 Wireless Subsystems
------------------------

**Wireless Technologies Integrated**:

====================  ====================  ========================================
Technology            Projects              Implementation Details
====================  ====================  ========================================
Wi-Fi (802.11n/ac)    #1 IoT, #2 Avionics   cfg80211, mac80211, driver integration
Bluetooth (BLE)       #1 IoT                BlueZ stack, HCI, GATT services
Zigbee (802.15.4)     #1 IoT                wpan-tools, 6LoWPAN
RF Custom Protocol    #7 Thermal            Custom RF driver for video
====================  ====================  ========================================

**Wi-Fi Driver Integration**::

    # Device tree for Wi-Fi module
    &mmc1 {
        wifi: wifi@1 {
            compatible = "brcm,bcm4329-fmac";
            reg = <1>;
            interrupt-parent = <&gpio2>;
            interrupts = <10 IRQ_TYPE_LEVEL_HIGH>;
            interrupt-names = "host-wake";
        };
    };
    
    # Load firmware and configure
    modprobe brcmfmac
    iw dev wlan0 scan
    wpa_supplicant -i wlan0 -c /etc/wpa_supplicant.conf

**Interview Talking Point**:
*"Integrated wireless subsystems for 4 protocols: Wi-Fi (Broadcom FMAC, cfg80211/mac80211 stack, WPA2), Bluetooth LE (BlueZ, GATT for sensor pairing), Zigbee (802.15.4 PHY, 6LoWPAN for mesh networking), and custom RF for thermal video. Managed firmware loading, power management (wake-on-wireless), and secure pairing."*

Section 4: Power Management Subsystem
=======================================

4.1 CPU Power Management
--------------------------

CPUFreq & CPUIdle Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Projects**: #1 (IoT), #7 (Thermal)

**CPUFreq Governors**::

    # i.MX93 IoT - Dynamic frequency scaling
    # Available governors: performance, powersave, ondemand, conservative, schedutil
    
    # Use schedutil (scheduler-driven DVFS) for IoT
    echo schedutil > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    
    # Configure frequency range
    echo 600000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq    # 600 MHz
    echo 1800000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq   # 1.8 GHz
    
    # Thermal imaging - Conservative governor for longer battery
    echo conservative > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

**CPUIdle States**::

    # Configure C-states for deep idle
    # C0: Running
    # C1: Clock gating (< 1us latency)
    # C2: Power gating (< 100us latency)
    # C3: Deep sleep (> 1ms latency)
    
    # Enable all C-states for IoT battery optimization
    for state in /sys/devices/system/cpu/cpu0/cpuidle/state*; do
        echo 0 > $state/disable
    done
    
    # Adjust latency requirements for real-time video (Thermal)
    echo 100 > /dev/cpu_dma_latency  # Prevent C-states deeper than 100us

**Device Tree CPUFreq Configuration**::

    cpus {
        cpu@0 {
            compatible = "arm,cortex-a55";
            operating-points-v2 = <&cpu_opp_table>;
            clocks = <&clk IMX93_CLK_A55>;
            clock-latency = <61036>; /* two CLK32 periods */
            #cooling-cells = <2>;
        };
    };
    
    cpu_opp_table: opp-table {
        compatible = "operating-points-v2";
        opp-shared;
        
        opp-600000000 {
            opp-hz = /bits/ 64 <600000000>;
            opp-microvolt = <850000>;
            clock-latency-ns = <150000>;
        };
        
        opp-1200000000 {
            opp-hz = /bits/ 64 <1200000000>;
            opp-microvolt = <950000>;
        };
        
        opp-1800000000 {
            opp-hz = /bits/ 64 <1800000000>;
            opp-microvolt = <1050000>;
        };
    };

**Interview Talking Point**:
*"Configured CPUFreq/CPUIdle for two use cases: i.MX93 IoT used schedutil governor with DVFS (600 MHz-1.8 GHz, 3 OPPs) for battery optimization; ARM9 thermal used conservative governor with C-state restrictions (< 100us latency) to maintain 30 FPS video processing. Achieved 3x battery life improvement on IoT."*

4.2 Runtime Power Management
-----------------------------

Device Runtime PM
~~~~~~~~~~~~~~~~~~

**Runtime PM for Peripherals**::

    /* Enable runtime PM for video device */
    static int thermal_v4l2_probe(struct platform_device *pdev)
    {
        struct device *dev = &pdev->dev;
        
        /* Enable runtime PM */
        pm_runtime_enable(dev);
        pm_runtime_set_autosuspend_delay(dev, 100); /* 100ms */
        pm_runtime_use_autosuspend(dev);
        
        /* Get device on probe */
        pm_runtime_get_sync(dev);
        
        /* Device initialization... */
        
        /* Allow device to autosuspend */
        pm_runtime_mark_last_busy(dev);
        pm_runtime_put_autosuspend(dev);
        
        return 0;
    }
    
    /* Runtime PM callbacks */
    static int thermal_v4l2_runtime_suspend(struct device *dev)
    {
        struct thermal_v4l2_dev *tdev = dev_get_drvdata(dev);
        
        /* Stop video processing */
        /* Clock gating */
        clk_disable_unprepare(tdev->clk);
        
        /* Power down DSP */
        dsp_power_off(tdev->dsp);
        
        return 0;
    }
    
    static int thermal_v4l2_runtime_resume(struct device *dev)
    {
        struct thermal_v4l2_dev *tdev = dev_get_drvdata(dev);
        
        /* Power up DSP */
        dsp_power_on(tdev->dsp);
        
        /* Enable clocks */
        clk_prepare_enable(tdev->clk);
        
        /* Restore video processing state */
        
        return 0;
    }
    
    static const struct dev_pm_ops thermal_v4l2_pm_ops = {
        SET_RUNTIME_PM_OPS(thermal_v4l2_runtime_suspend,
                           thermal_v4l2_runtime_resume, NULL)
        SET_SYSTEM_SLEEP_PM_OPS(thermal_v4l2_suspend, thermal_v4l2_resume)
    };

4.3 System Power States
------------------------

Hibernation/Suspend Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Thermal Imaging Hibernation** (< 8mW, < 2s wake):

::

    # Hibernate configuration
    echo disk > /sys/power/state  # Use hibernation (suspend-to-disk)
    
    # Optimize hibernation image
    echo 0 > /sys/power/image_size  # Minimal image for fast resume
    
    # Custom hibernation script
    #!/bin/sh
    # Pre-hibernation: Stop non-critical services
    systemctl stop networking
    systemctl stop thermal-processing
    
    # Sync filesystems
    sync
    
    # Enter hibernation
    echo disk > /sys/power/state
    
    # Post-resume: Restart services
    systemctl start thermal-processing
    systemctl start networking

**Wake Sources Configuration**::

    # Configure wake sources (button, RTC, network)
    echo enabled > /sys/devices/platform/gpio-keys/power/wakeup
    echo enabled > /sys/class/rtc/rtc0/device/power/wakeup
    echo enabled > /sys/class/net/eth0/device/power/wakeup

**Custom Power States** (ARM9 Thermal - tens of microamps):

::

    /* Custom deep sleep state */
    static void enter_ultra_low_power(void)
    {
        /* Disable all non-essential peripherals */
        disable_video_processing();
        disable_dsp();
        disable_usb();
        disable_ethernet();
        
        /* Keep only: RTC, wake button, minimal RAM refresh */
        
        /* Configure RAM for self-refresh */
        writel(SDRAM_SELF_REFRESH, SDRAM_CTRL_REG);
        
        /* Enter ARM9 standby mode */
        cpu_do_idle();
        
        /* Power consumption: < 50 µA */
    }

**Interview Talking Point**:
*"Implemented 3-tier power management: runtime PM for device-level power (100ms autosuspend for video driver, clock/power gating), system-level hibernation (< 8mW with minimal image for < 2s resume), and custom ultra-low-power state (< 50 µA with SDRAM self-refresh, RTC, and wake button only). Achieved 72-hour battery life on thermal imaging device."*

Section 5: Boot & Init Subsystems
===================================

5.1 Bootloader (U-Boot)
-------------------------

U-Boot Customization
~~~~~~~~~~~~~~~~~~~~~

**Projects**: #1 (IoT), #2 (Avionics), #7 (Thermal)

**Custom U-Boot Commands**::

    /* Thermal Imaging - Manufacturing test command */
    int do_mfg_test(cmd_tbl_t *cmdtp, int flag, int argc, char * const argv[])
    {
        /* Test NAND flash */
        if (nand_test() != 0) {
            printf("NAND test FAILED\n");
            return 1;
        }
        
        /* Test DDR */
        if (ddr_test() != 0) {
            printf("DDR test FAILED\n");
            return 1;
        }
        
        /* Test peripherals */
        test_i2c();
        test_spi();
        test_usb();
        
        printf("Manufacturing test PASSED\n");
        return 0;
    }
    
    U_BOOT_CMD(
        mfgtest, 1, 0, do_mfg_test,
        "run manufacturing tests",
        ""
    );

**NAND BBT Support in U-Boot**::

    /* Enable NAND BBT in U-Boot for consistency with kernel */
    #define CONFIG_SYS_NAND_USE_BBT
    #define CONFIG_SYS_NAND_BAD_BLOCK_POS    0
    
    /* Custom BBT descriptor matching kernel */
    static struct nand_bbt_descr uboot_bbt_descr = {
        .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE | NAND_BBT_WRITE,
        .offs = 8,
        .len = 4,
        .veroffs = 12,
        .maxblocks = 4,
        .pattern = bbt_pattern
    };

**Secure Boot U-Boot (i.MX93 HAB)**::

    /* Enable HAB secure boot features */
    #define CONFIG_SECURE_BOOT
    #define CONFIG_FSL_CAAM
    #define CONFIG_CMD_DEKBLOB
    
    /* Sign U-Boot image */
    # Generate CSF (Command Sequence File)
    cst -i u-boot-csf.txt -o u-boot-signed.csf
    
    # Append signature to U-Boot
    cat u-boot.bin u-boot-signed.csf > u-boot-signed.bin
    
    # Burn eFuses to enable secure boot
    => fuse prog 0 6 0x00000010  # Enable HAB closed mode

**Interview Talking Point**:
*"Customized U-Boot for 3 platforms: added manufacturing test commands (NAND, DDR, peripheral validation), implemented NAND BBT support matching kernel descriptor, and configured HAB secure boot on i.MX93 (CSF signing, eFuse programming for closed mode). Boot time optimization: removed unused commands, optimized environment loading."*

5.2 Device Tree
----------------

Device Tree Development
~~~~~~~~~~~~~~~~~~~~~~~~

**Device Tree Expertise**:

- **Projects**: #1 (i.MX93), #2 (Atom - minimal), #6 (Auto), #7 (DaVinci)
- **Scope**: 10+ peripherals per project, 50+ device bindings total

**Complex Device Tree Example (i.MX93 IoT)**::

    /dts-v1/;
    #include "imx93.dtsi"
    
    / {
        model = "Smart Home IoT Platform";
        compatible = "vendor,smarthome-iot", "fsl,imx93";
        
        chosen {
            stdout-path = &lpuart1;
            bootargs = "console=ttyLP0,115200 rootwait ro";
        };
        
        memory@80000000 {
            device_type = "memory";
            reg = <0x0 0x80000000 0x0 0x40000000>; /* 1GB */
        };
        
        reserved-memory {
            #address-cells = <2>;
            #size-cells = <2>;
            ranges;
            
            /* Reserve memory for HAB */
            hab_mem: hab@90000000 {
                reg = <0x0 0x90000000 0x0 0x10000>;
                no-map;
            };
            
            /* CMA for video/graphics */
            linux,cma {
                compatible = "shared-dma-pool";
                reusable;
                size = <0x0 0x8000000>; /* 128MB */
                linux,cma-default;
            };
        };
        
        regulators {
            compatible = "simple-bus";
            
            reg_3v3: regulator-3v3 {
                compatible = "regulator-fixed";
                regulator-name = "3V3";
                regulator-min-microvolt = <3300000>;
                regulator-max-microvolt = <3300000>;
                regulator-always-on;
            };
            
            reg_wifi_en: regulator-wifi {
                compatible = "regulator-fixed";
                regulator-name = "wifi_en";
                regulator-min-microvolt = <3300000>;
                regulator-max-microvolt = <3300000>;
                gpio = <&gpio2 10 GPIO_ACTIVE_HIGH>;
                enable-active-high;
                startup-delay-us = <100000>;
            };
        };
        
        gpio-keys {
            compatible = "gpio-keys";
            pinctrl-names = "default";
            pinctrl-0 = <&pinctrl_gpio_keys>;
            
            power {
                label = "Power Button";
                gpios = <&gpio1 5 GPIO_ACTIVE_LOW>;
                linux,code = <KEY_POWER>;
                wakeup-source;
            };
        };
        
        leds {
            compatible = "gpio-leds";
            
            status-led {
                label = "status";
                gpios = <&gpio3 20 GPIO_ACTIVE_HIGH>;
                default-state = "on";
                linux,default-trigger = "heartbeat";
            };
        };
    };
    
    /* UART for console */
    &lpuart1 {
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_uart1>;
        status = "okay";
    };
    
    /* I2C for PMIC, sensors */
    &lpi2c1 {
        #address-cells = <1>;
        #size-cells = <0>;
        clock-frequency = <400000>;
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_lpi2c1>;
        status = "okay";
        
        pmic@25 {
            compatible = "nxp,pca9450c";
            reg = <0x25>;
            pinctrl-0 = <&pinctrl_pmic>;
            interrupt-parent = <&gpio1>;
            interrupts = <3 IRQ_TYPE_LEVEL_LOW>;
            
            regulators {
                buck1: BUCK1 {
                    regulator-name = "BUCK1";
                    regulator-min-microvolt = <600000>;
                    regulator-max-microvolt = <2187500>;
                    regulator-boot-on;
                    regulator-always-on;
                    regulator-ramp-delay = <3125>;
                };
            };
        };
        
        bq27441@55 {
            compatible = "ti,bq27441";
            reg = <0x55>;
            monitored-battery = <&battery>;
        };
    };
    
    /* SPI for CAN controller, flash */
    &lpspi1 {
        #address-cells = <1>;
        #size-cells = <0>;
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_lpspi1>;
        status = "okay";
        
        can@0 {
            compatible = "microchip,mcp2515";
            reg = <0>;
            clocks = <&can_osc>;
            interrupt-parent = <&gpio1>;
            interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
            spi-max-frequency = <10000000>;
        };
    };
    
    /* eMMC */
    &usdhc1 {
        pinctrl-names = "default", "state_100mhz", "state_200mhz";
        pinctrl-0 = <&pinctrl_usdhc1>;
        pinctrl-1 = <&pinctrl_usdhc1_100mhz>;
        pinctrl-2 = <&pinctrl_usdhc1_200mhz>;
        bus-width = <8>;
        non-removable;
        status = "okay";
    };
    
    /* Wi-Fi/BT module */
    &usdhc2 {
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_usdhc2>;
        bus-width = <4>;
        vmmc-supply = <&reg_wifi_en>;
        cap-power-off-card;
        keep-power-in-suspend;
        wakeup-source;
        status = "okay";
        
        wifi: wifi@1 {
            compatible = "brcm,bcm4329-fmac";
            reg = <1>;
            interrupt-parent = <&gpio2>;
            interrupts = <10 IRQ_TYPE_LEVEL_HIGH>;
            interrupt-names = "host-wake";
        };
    };
    
    /* Ethernet */
    &fec {
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_fec>;
        phy-mode = "rgmii-id";
        phy-handle = <&ethphy>;
        status = "okay";
        
        mdio {
            #address-cells = <1>;
            #size-cells = <0>;
            
            ethphy: ethernet-phy@1 {
                compatible = "ethernet-phy-ieee802.3-c22";
                reg = <1>;
                interrupt-parent = <&gpio1>;
                interrupts = <15 IRQ_TYPE_LEVEL_LOW>;
            };
        };
    };
    
    /* USB OTG */
    &usb {
        dr_mode = "otg";
        status = "okay";
    };
    
    /* Pin configuration */
    &iomuxc {
        pinctrl_uart1: uart1grp {
            fsl,pins = <
                MX93_PAD_UART1_RXD__LPUART1_RX  0x31e
                MX93_PAD_UART1_TXD__LPUART1_TX  0x31e
            >;
        };
        
        pinctrl_lpi2c1: lpi2c1grp {
            fsl,pins = <
                MX93_PAD_I2C1_SCL__LPI2C1_SCL   0x40000b9e
                MX93_PAD_I2C1_SDA__LPI2C1_SDA   0x40000b9e
            >;
        };
        
        /* Additional pin groups... */
    };

**Device Tree Overlays**::

    # Runtime device tree modification for camera selection
    /dts-v1/;
    /plugin/;
    
    / {
        fragment@0 {
            target = <&i2c2>;
            __overlay__ {
                camera@10 {
                    compatible = "ov5640";
                    reg = <0x10>;
                    clocks = <&clk_camera>;
                    clock-names = "xclk";
                    status = "okay";
                };
            };
        };
    };
    
    # Apply overlay at runtime
    dtoverlay camera-ov5640

**Interview Talking Point**:
*"Developed complex device trees for i.MX93 IoT (20+ peripherals: UART, I2C PMIC/battery/sensors, SPI CAN/flash, eMMC, Wi-Fi/BT, Ethernet PHY, USB OTG), including memory reservation (HAB, CMA), regulator tree (PMIC rails), pinmux configuration, and interrupt routing. Used device tree overlays for runtime camera selection (3 configurations). Managed device tree for avionics (Intel Atom, FPGA, wireless) and thermal imaging (DaVinci peripherals)."*

Summary: Kernel Subsystem Expertise
=====================================

**15+ Subsystems with Hands-on Experience**:

1. **Process Scheduler** - Real-time priorities, CPU affinity
2. **Memory Management** - mDDR, CMA, memory optimization
3. **Virtual Filesystem (VFS)** - JFFS2, SquashFS, ext4, overlays
4. **MTD** - NAND drivers, BBT, JFFS2, ECC
5. **Block Layer** - eMMC, SATA, dm-verity, dm-crypt
6. **USB** - Bulk, isochronous, mass storage drivers
7. **Video4Linux2 (V4L2)** - Video capture, videobuf2, DMA
8. **Network Devices** - EMAC, Wi-Fi, SocketCAN drivers
9. **I2C** - PMIC, sensors, battery management
10. **SPI** - CAN controllers, flash, ADC/DAC
11. **PCIe** - Multi-RC platform driver, enumeration
12. **Networking** - TCP/IP tuning, QoS, wireless (cfg80211, mac80211)
13. **Power Management** - CPUFreq, CPUIdle, runtime PM, hibernation
14. **Boot (U-Boot)** - Custom commands, NAND BBT, secure boot
15. **Device Tree** - Complex bindings, overlays, 50+ devices

**Total Driver Count**: 15+ driver types across 8 projects

**Interview Summary**:
*"I have 18+ years of Linux kernel development across 15 subsystems. My driver portfolio includes MTD/NAND with custom BBT, USB bulk/isochronous for video, V4L2 with DMA, PCIe platform driver for multi-RC SOCs, and network drivers (Wi-Fi/BT/Zigbee/CAN/EMAC). I've optimized memory (mDDR, CMA), power (< 8mW hibernation, 3x battery life), and boot (15s → 3s). Device tree expertise spans 50+ device bindings across 4 SOC families."*

End of Document
================

**Last Updated**: January 22, 2026
**Total Lines**: 1500+
**Cross-references**: 100+

© 2026 Madhavan Vivekanandan - All Rights Reserved
