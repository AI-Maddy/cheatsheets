===============================================
Linux Kernel Driver Development - By Domain
===============================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Experience: Multi-domain embedded systems development

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
========

Comprehensive guide to Linux kernel driver development organized by functional domains, covering video capture, networking, storage, USB, PCIe, and peripheral interfaces based on real project implementations across avionics, thermal imaging, and IoT platforms.

Video Subsystem Drivers (V4L2)
===============================

Video4Linux2 Framework Overview
--------------------------------

**Architecture:**

.. code-block:: text

   Application Layer
   ├── /dev/video*
   └── V4L2 API (ioctl)
          ↓
   V4L2 Core
   ├── videobuf2 (buffer management)
   ├── v4l2-device (device registration)
   ├── v4l2-subdev (sensor/codec drivers)
   └── Media Controller
          ↓
   Hardware Driver
   ├── Camera Sensor I2C
   ├── CSI/MIPI Interface
   ├── ISP (Image Signal Processor)
   └── DMA Engine

Thermal Camera Driver (Project: FLIR)
--------------------------------------

**TI DaVinci VPFE Driver for Thermal Imaging:**

.. code-block:: c

   // drivers/media/platform/davinci/thermal_vpfe.c
   
   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <media/v4l2-device.h>
   #include <media/videobuf2-dma-contig.h>
   
   #define THERMAL_WIDTH   640
   #define THERMAL_HEIGHT  480
   #define THERMAL_FPS     30
   
   struct thermal_vpfe_device {
       struct v4l2_device v4l2_dev;
       struct video_device vdev;
       struct vb2_queue queue;
       
       void __iomem *regs;
       struct clk *vpss_clk;
       
       /* Buffer management */
       struct list_head dma_queue;
       spinlock_t dma_queue_lock;
       
       /* Format */
       struct v4l2_format fmt;
       u32 sequence;
   };
   
   /* Buffer operations */
   static int thermal_queue_setup(struct vb2_queue *vq,
                                  unsigned int *nbuffers,
                                  unsigned int *nplanes,
                                  unsigned int sizes[],
                                  struct device *alloc_devs[])
   {
       struct thermal_vpfe_device *vpfe = vb2_get_drv_priv(vq);
       
       *nplanes = 1;
       sizes[0] = THERMAL_WIDTH * THERMAL_HEIGHT * 2;  // 16-bit raw
       
       if (*nbuffers < 3)
           *nbuffers = 3;  // Minimum buffers
       
       return 0;
   }
   
   static int thermal_buffer_prepare(struct vb2_buffer *vb)
   {
       struct thermal_vpfe_device *vpfe = vb2_get_drv_priv(vb->vb2_queue);
       unsigned long size = THERMAL_WIDTH * THERMAL_HEIGHT * 2;
       
       if (vb2_plane_size(vb, 0) < size) {
           dev_err(&vpfe->vdev.dev, "Buffer too small\n");
           return -EINVAL;
       }
       
       vb2_set_plane_payload(vb, 0, size);
       return 0;
   }
   
   static void thermal_buffer_queue(struct vb2_buffer *vb)
   {
       struct thermal_vpfe_device *vpfe = vb2_get_drv_priv(vb->vb2_queue);
       struct vb2_v4l2_buffer *vbuf = to_vb2_v4l2_buffer(vb);
       unsigned long flags;
       
       spin_lock_irqsave(&vpfe->dma_queue_lock, flags);
       list_add_tail(&vbuf->list, &vpfe->dma_queue);
       spin_unlock_irqrestore(&vpfe->dma_queue_lock, flags);
   }
   
   /* Hardware configuration */
   static int thermal_vpfe_configure(struct thermal_vpfe_device *vpfe)
   {
       u32 val;
       
       /* Disable progressive/interlaced */
       writel(0, vpfe->regs + VPFE_PCR);
       
       /* Configure for 16-bit raw input */
       val = VPFE_RAW_INPUT | VPFE_DATA_WIDTH_16BIT;
       writel(val, vpfe->regs + VPFE_SYNMODE);
       
       /* Set image dimensions */
       val = THERMAL_WIDTH | (THERMAL_HEIGHT << 16);
       writel(val, vpfe->regs + VPFE_HDW);
       writel(val, vpfe->regs + VPFE_VDW);
       
       /* Configure CCDC for raw mode */
       val = VPFE_CCDC_RAW_MODE | VPFE_CCDC_ENABLE;
       writel(val, vpfe->regs + VPFE_CCDC_CFG);
       
       return 0;
   }
   
   /* Start streaming */
   static int thermal_start_streaming(struct vb2_queue *vq, unsigned int count)
   {
       struct thermal_vpfe_device *vpfe = vb2_get_drv_priv(vq);
       
       /* Enable clocks */
       clk_prepare_enable(vpfe->vpss_clk);
       
       /* Configure hardware */
       thermal_vpfe_configure(vpfe);
       
       /* Enable VPFE */
       writel(VPFE_ENABLE, vpfe->regs + VPFE_PCR);
       
       vpfe->sequence = 0;
       
       return 0;
   }
   
   /* IRQ handler for frame completion */
   static irqreturn_t thermal_vpfe_isr(int irq, void *dev_id)
   {
       struct thermal_vpfe_device *vpfe = dev_id;
       struct vb2_v4l2_buffer *vbuf;
       u32 status;
       
       status = readl(vpfe->regs + VPFE_IRQ_STATUS);
       
       if (status & VPFE_IRQ_VDINT0) {
           /* Frame complete */
           spin_lock(&vpfe->dma_queue_lock);
           
           if (!list_empty(&vpfe->dma_queue)) {
               vbuf = list_first_entry(&vpfe->dma_queue,
                                      struct vb2_v4l2_buffer, list);
               list_del(&vbuf->list);
               
               vbuf->vb2_buf.timestamp = ktime_get_ns();
               vbuf->sequence = vpfe->sequence++;
               vbuf->field = V4L2_FIELD_NONE;
               
               vb2_buffer_done(&vbuf->vb2_buf, VB2_BUF_STATE_DONE);
           }
           
           spin_unlock(&vpfe->dma_queue_lock);
           
           /* Clear interrupt */
           writel(VPFE_IRQ_VDINT0, vpfe->regs + VPFE_IRQ_CLEAR);
       }
       
       return IRQ_HANDLED;
   }
   
   static const struct vb2_ops thermal_vb2_ops = {
       .queue_setup     = thermal_queue_setup,
       .buf_prepare     = thermal_buffer_prepare,
       .buf_queue       = thermal_buffer_queue,
       .start_streaming = thermal_start_streaming,
       .stop_streaming  = thermal_stop_streaming,
   };
   
   /* V4L2 file operations */
   static int thermal_querycap(struct file *file, void *priv,
                               struct v4l2_capability *cap)
   {
       strscpy(cap->driver, "thermal-vpfe", sizeof(cap->driver));
       strscpy(cap->card, "Thermal Camera", sizeof(cap->card));
       cap->device_caps = V4L2_CAP_VIDEO_CAPTURE | V4L2_CAP_STREAMING;
       cap->capabilities = cap->device_caps | V4L2_CAP_DEVICE_CAPS;
       
       return 0;
   }
   
   static const struct v4l2_ioctl_ops thermal_ioctl_ops = {
       .vidioc_querycap          = thermal_querycap,
       .vidioc_enum_fmt_vid_cap  = thermal_enum_fmt,
       .vidioc_g_fmt_vid_cap     = thermal_g_fmt,
       .vidioc_s_fmt_vid_cap     = thermal_s_fmt,
       .vidioc_reqbufs           = vb2_ioctl_reqbufs,
       .vidioc_querybuf          = vb2_ioctl_querybuf,
       .vidioc_qbuf              = vb2_ioctl_qbuf,
       .vidioc_dqbuf             = vb2_ioctl_dqbuf,
       .vidioc_streamon          = vb2_ioctl_streamon,
       .vidioc_streamoff         = vb2_ioctl_streamoff,
   };

**Userspace Application:**

.. code-block:: c

   // Application to capture thermal frames
   
   #include <stdio.h>
   #include <fcntl.h>
   #include <sys/ioctl.h>
   #include <sys/mman.h>
   #include <linux/videodev2.h>
   
   #define DEVICE "/dev/video0"
   #define FRAME_COUNT 4
   
   struct buffer {
       void *start;
       size_t length;
   };
   
   int main(void)
   {
       int fd;
       struct v4l2_format fmt;
       struct v4l2_requestbuffers req;
       struct buffer buffers[FRAME_COUNT];
       
       /* Open device */
       fd = open(DEVICE, O_RDWR);
       
       /* Set format */
       memset(&fmt, 0, sizeof(fmt));
       fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
       fmt.fmt.pix.width = 640;
       fmt.fmt.pix.height = 480;
       fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_GREY;  // 16-bit raw
       fmt.fmt.pix.field = V4L2_FIELD_NONE;
       
       ioctl(fd, VIDIOC_S_FMT, &fmt);
       
       /* Request buffers */
       memset(&req, 0, sizeof(req));
       req.count = FRAME_COUNT;
       req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
       req.memory = V4L2_MEMORY_MMAP;
       ioctl(fd, VIDIOC_REQBUFS, &req);
       
       /* Map buffers */
       for (int i = 0; i < FRAME_COUNT; i++) {
           struct v4l2_buffer buf;
           
           memset(&buf, 0, sizeof(buf));
           buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
           buf.memory = V4L2_MEMORY_MMAP;
           buf.index = i;
           
           ioctl(fd, VIDIOC_QUERYBUF, &buf);
           
           buffers[i].length = buf.length;
           buffers[i].start = mmap(NULL, buf.length,
                                   PROT_READ | PROT_WRITE,
                                   MAP_SHARED, fd, buf.m.offset);
           
           /* Queue buffer */
           ioctl(fd, VIDIOC_QBUF, &buf);
       }
       
       /* Start streaming */
       enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
       ioctl(fd, VIDIOC_STREAMON, &type);
       
       /* Capture frames */
       for (int frame = 0; frame < 100; frame++) {
           struct v4l2_buffer buf;
           
           memset(&buf, 0, sizeof(buf));
           buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
           buf.memory = V4L2_MEMORY_MMAP;
           
           /* Dequeue filled buffer */
           ioctl(fd, VIDIOC_DQBUF, &buf);
           
           /* Process thermal data */
           process_thermal_frame(buffers[buf.index].start,
                                buffers[buf.index].length);
           
           /* Requeue buffer */
           ioctl(fd, VIDIOC_QBUF, &buf);
       }
       
       /* Stop streaming */
       ioctl(fd, VIDIOC_STREAMOFF, &type);
       
       /* Cleanup */
       for (int i = 0; i < FRAME_COUNT; i++)
           munmap(buffers[i].start, buffers[i].length);
       
       close(fd);
       return 0;
   }

Network Drivers
===============

CAN Bus Driver
--------------

**SocketCAN Framework:**

.. code-block:: c

   // drivers/net/can/flexcan.c (i.MX platform)
   
   #include <linux/netdevice.h>
   #include <linux/can/dev.h>
   #include <linux/can/error.h>
   
   struct flexcan_priv {
       struct can_priv can;
       struct net_device *dev;
       void __iomem *regs;
       struct clk *clk_ipg;
       struct clk *clk_per;
       u32 mb_count;
   };
   
   /* Transmit CAN frame */
   static netdev_tx_t flexcan_start_xmit(struct sk_buff *skb,
                                         struct net_device *dev)
   {
       struct flexcan_priv *priv = netdev_priv(dev);
       struct can_frame *cf = (struct can_frame *)skb->data;
       u32 can_id, data;
       int i;
       
       /* Get message buffer */
       int mb_idx = flexcan_get_mb_tx(priv);
       void __iomem *mb = priv->regs + FLEXCAN_MB_OFFSET(mb_idx);
       
       /* Prepare CAN ID */
       if (cf->can_id & CAN_EFF_FLAG) {
           /* Extended frame */
           can_id = (cf->can_id & CAN_EFF_MASK) | FLEXCAN_MB_CNT_IDE;
       } else {
           /* Standard frame */
           can_id = (cf->can_id & CAN_SFF_MASK) << 18;
       }
       
       if (cf->can_id & CAN_RTR_FLAG)
           can_id |= FLEXCAN_MB_CNT_RTR;
       
       /* Write message buffer */
       writel(FLEXCAN_MB_CNT_CODE(0x8) | FLEXCAN_MB_CNT_LENGTH(cf->len),
              mb + FLEXCAN_MB_CNT_OFFSET);
       writel(can_id, mb + FLEXCAN_MB_ID_OFFSET);
       
       /* Write data */
       for (i = 0; i < cf->len; i += 4) {
           data = *(u32 *)(cf->data + i);
           writel(cpu_to_be32(data), mb + FLEXCAN_MB_DATA_OFFSET + i);
       }
       
       /* Trigger transmission */
       writel(FLEXCAN_MB_CNT_CODE(0xC),
              mb + FLEXCAN_MB_CNT_OFFSET);
       
       can_put_echo_skb(skb, dev, mb_idx);
       
       return NETDEV_TX_OK;
   }
   
   /* Receive interrupt handler */
   static void flexcan_read_fifo(struct net_device *dev)
   {
       struct flexcan_priv *priv = netdev_priv(dev);
       struct can_frame *cf;
       struct sk_buff *skb;
       u32 reg_ctrl, reg_id, reg_data;
       
       skb = alloc_can_skb(dev, &cf);
       if (!skb) {
           dev->stats.rx_dropped++;
           return;
       }
       
       /* Read message buffer */
       reg_ctrl = readl(priv->regs + FLEXCAN_MB0_CNT);
       reg_id = readl(priv->regs + FLEXCAN_MB0_ID);
       
       /* Extract CAN ID */
       if (reg_ctrl & FLEXCAN_MB_CNT_IDE) {
           /* Extended ID */
           cf->can_id = (reg_id & CAN_EFF_MASK) | CAN_EFF_FLAG;
       } else {
           /* Standard ID */
           cf->can_id = (reg_id >> 18) & CAN_SFF_MASK;
       }
       
       if (reg_ctrl & FLEXCAN_MB_CNT_RTR)
           cf->can_id |= CAN_RTR_FLAG;
       
       /* Get data length */
       cf->len = (reg_ctrl >> 16) & 0xF;
       
       /* Read data */
       for (int i = 0; i < cf->len; i += 4) {
           reg_data = readl(priv->regs + FLEXCAN_MB0_DATA + i);
           *(u32 *)(cf->data + i) = be32_to_cpu(reg_data);
       }
       
       /* Update statistics */
       dev->stats.rx_packets++;
       dev->stats.rx_bytes += cf->len;
       
       netif_receive_skb(skb);
   }

**CAN Application Example:**

.. code-block:: c

   // Userspace CAN communication
   
   #include <stdio.h>
   #include <string.h>
   #include <unistd.h>
   #include <net/if.h>
   #include <sys/ioctl.h>
   #include <sys/socket.h>
   #include <linux/can.h>
   #include <linux/can/raw.h>
   
   int main(void)
   {
       int s;
       struct sockaddr_can addr;
       struct ifreq ifr;
       struct can_frame frame;
       
       /* Create CAN socket */
       s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
       
       /* Specify CAN interface */
       strcpy(ifr.ifr_name, "can0");
       ioctl(s, SIOCGIFINDEX, &ifr);
       
       /* Bind socket */
       addr.can_family = AF_CAN;
       addr.can_ifindex = ifr.ifr_ifindex;
       bind(s, (struct sockaddr *)&addr, sizeof(addr));
       
       /* Send CAN frame */
       frame.can_id = 0x123;
       frame.can_dlc = 8;
       memcpy(frame.data, "CANDATA!", 8);
       
       write(s, &frame, sizeof(frame));
       
       /* Receive CAN frame */
       read(s, &frame, sizeof(frame));
       
       printf("Received: ID=0x%X Data=", frame.can_id);
       for (int i = 0; i < frame.can_dlc; i++)
           printf("%02X ", frame.data[i]);
       printf("\n");
       
       close(s);
       return 0;
   }

AFDX/ARINC 664 Network Driver
------------------------------

**AFDX Virtual Link Implementation:**

.. code-block:: c

   // drivers/net/ethernet/afdx/afdx_core.c
   
   struct afdx_vl {
       u16 vl_id;
       u32 bag;  // Bandwidth Allocation Gap (μs)
       u16 max_frame_size;
       u8 priority;
       
       /* Rate limiting */
       ktime_t last_tx;
       struct hrtimer timer;
   };
   
   struct afdx_priv {
       struct net_device *ndev;
       struct afdx_vl vl_table[256];
       
       /* Redundancy */
       struct net_device *network_a;
       struct net_device *network_b;
   };
   
   /* AFDX frame transmission with BAG enforcement */
   static netdev_tx_t afdx_start_xmit(struct sk_buff *skb,
                                      struct net_device *dev)
   {
       struct afdx_priv *priv = netdev_priv(dev);
       struct ethhdr *eth = eth_hdr(skb);
       u16 vl_id;
       struct afdx_vl *vl;
       ktime_t now, diff;
       
       /* Extract VL ID from destination MAC */
       vl_id = (eth->h_dest[4] << 8) | eth->h_dest[5];
       vl = &priv->vl_table[vl_id];
       
       /* Enforce BAG timing */
       now = ktime_get();
       diff = ktime_sub(now, vl->last_tx);
       
       if (ktime_to_us(diff) < vl->bag) {
           /* Too soon, drop frame */
           dev_kfree_skb(skb);
           dev->stats.tx_dropped++;
           return NETDEV_TX_OK;
       }
       
       vl->last_tx = now;
       
       /* Send on both networks (redundancy) */
       if (priv->network_a) {
           struct sk_buff *skb_a = skb_clone(skb, GFP_ATOMIC);
           dev_queue_xmit(skb_a);
       }
       
       if (priv->network_b) {
           struct sk_buff *skb_b = skb_clone(skb, GFP_ATOMIC);
           dev_queue_xmit(skb_b);
       }
       
       dev_kfree_skb(skb);
       
       return NETDEV_TX_OK;
   }

Ethernet Switch Driver
-----------------------

**Multi-Port Switch Configuration:**

.. code-block:: c

   // drivers/net/ethernet/switch/eth_switch.c
   
   struct eth_switch {
       void __iomem *regs;
       struct phy_device *port_phy[8];
       u32 port_mask;
   };
   
   /* Configure VLAN for port isolation */
   static int eth_switch_config_vlan(struct eth_switch *sw,
                                     int port, u16 vlan_id)
   {
       u32 val;
       
       /* VLAN membership */
       val = readl(sw->regs + VLAN_TABLE(vlan_id));
       val |= BIT(port);
       writel(val, sw->regs + VLAN_TABLE(vlan_id));
       
       /* Port VLAN ID */
       val = readl(sw->regs + PORT_CTRL(port));
       val &= ~PORT_PVID_MASK;
       val |= (vlan_id << PORT_PVID_SHIFT);
       writel(val, sw->regs + PORT_CTRL(port));
       
       return 0;
   }
   
   /* Port mirroring for debugging */
   static int eth_switch_mirror_port(struct eth_switch *sw,
                                     int src_port, int dst_port)
   {
       u32 val;
       
       val = MIRROR_ENABLE | MIRROR_SRC(src_port) | MIRROR_DST(dst_port);
       writel(val, sw->regs + MIRROR_CTRL);
       
       return 0;
   }

Storage Drivers
===============

MTD/NAND Flash Driver
---------------------

**NAND Driver with Bad Block Table:**

.. code-block:: c

   // drivers/mtd/nand/raw/davinci_nand.c
   
   struct davinci_nand_info {
       struct nand_chip chip;
       struct device *dev;
       void __iomem *base;
       void __iomem *vaddr;
       
       uint32_t mask_ale;
       uint32_t mask_cle;
       uint32_t mask_chipsel;
       
       /* Bad block table */
       struct nand_bbt_descr *bbt_td;
       struct nand_bbt_descr *bbt_md;
   };
   
   /* BBT pattern for scanning */
   static uint8_t bbt_pattern[] = {'B', 'b', 't', '0' };
   static uint8_t mirror_pattern[] = {'1', 't', 'b', 'B' };
   
   static struct nand_bbt_descr davinci_bbt_main_descr = {
       .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE |
                  NAND_BBT_WRITE | NAND_BBT_2BIT |
                  NAND_BBT_VERSION | NAND_BBT_PERCHIP,
       .offs = 8,
       .len = 4,
       .veroffs = 12,
       .maxblocks = 4,
       .pattern = bbt_pattern
   };
   
   static struct nand_bbt_descr davinci_bbt_mirror_descr = {
       .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE |
                  NAND_BBT_WRITE | NAND_BBT_2BIT |
                  NAND_BBT_VERSION | NAND_BBT_PERCHIP,
       .offs = 8,
       .len = 4,
       .veroffs = 12,
       .maxblocks = 4,
       .pattern = mirror_pattern
   };
   
   /* Hardware ECC calculation */
   static int davinci_nand_calculate_ecc(struct nand_chip *chip,
                                         const u_char *dat, u_char *ecc_code)
   {
       struct davinci_nand_info *info = nand_get_controller_data(chip);
       u32 val;
       
       /* Read ECC from hardware registers */
       val = readl(info->base + NAND_4BIT_ECC1);
       ecc_code[0] = val & 0xFF;
       ecc_code[1] = (val >> 8) & 0xFF;
       ecc_code[2] = (val >> 16) & 0xFF;
       ecc_code[3] = (val >> 24) & 0xFF;
       
       val = readl(info->base + NAND_4BIT_ECC2);
       ecc_code[4] = val & 0xFF;
       ecc_code[5] = (val >> 8) & 0xFF;
       ecc_code[6] = (val >> 16) & 0xFF;
       ecc_code[7] = (val >> 24) & 0xFF;
       
       val = readl(info->base + NAND_4BIT_ECC3);
       ecc_code[8] = val & 0xFF;
       ecc_code[9] = (val >> 8) & 0xFF;
       
       return 0;
   }
   
   /* Correct bit errors */
   static int davinci_nand_correct_ecc(struct nand_chip *chip,
                                       u_char *dat,
                                       u_char *read_ecc,
                                       u_char *calc_ecc)
   {
       struct davinci_nand_info *info = nand_get_controller_data(chip);
       u32 error_count, error_loc[4];
       int i;
       
       /* Load calculated and read ECC */
       for (i = 0; i < 10; i += 4) {
           writel(*(u32 *)(calc_ecc + i),
                  info->base + NAND_4BIT_ECC_LOAD + i);
       }
       
       /* Start error detection */
       writel(NAND_ECC_START, info->base + NAND_ECC_CTRL);
       
       /* Wait for completion */
       while (!(readl(info->base + NAND_ECC_STATUS) & NAND_ECC_DONE))
           cpu_relax();
       
       error_count = readl(info->base + NAND_ERR_NUM);
       
       if (error_count == 0)
           return 0;
       
       if (error_count > 4)
           return -EBADMSG;  // Uncorrectable
       
       /* Read error locations */
       for (i = 0; i < error_count; i++) {
           u32 err_addr = readl(info->base + NAND_ERR_ADDR(i));
           u32 byte_pos = err_addr / 8;
           u32 bit_pos = err_addr % 8;
           
           dat[byte_pos] ^= BIT(bit_pos);
       }
       
       return error_count;
   }
   
   static int davinci_nand_probe(struct platform_device *pdev)
   {
       struct davinci_nand_info *info;
       struct nand_chip *chip;
       struct mtd_info *mtd;
       int ret;
       
       info = devm_kzalloc(&pdev->dev, sizeof(*info), GFP_KERNEL);
       if (!info)
           return -ENOMEM;
       
       chip = &info->chip;
       mtd = nand_to_mtd(chip);
       
       /* Map registers */
       info->base = devm_platform_ioremap_resource(pdev, 0);
       
       /* Setup chip */
       chip->legacy.chip_delay = 0;
       chip->options = NAND_USE_FLASH_BBT;
       
       /* ECC configuration */
       chip->ecc.mode = NAND_ECC_HW;
       chip->ecc.size = 512;
       chip->ecc.bytes = 10;  // 4-bit ECC
       chip->ecc.strength = 4;
       chip->ecc.calculate = davinci_nand_calculate_ecc;
       chip->ecc.correct = davinci_nand_correct_ecc;
       
       /* BBT descriptors */
       chip->bbt_td = &davinci_bbt_main_descr;
       chip->bbt_md = &davinci_bbt_mirror_descr;
       chip->bbt_options = NAND_BBT_USE_FLASH | NAND_BBT_NO_OOB;
       
       /* Scan NAND */
       ret = nand_scan(chip, 1);
       if (ret)
           return ret;
       
       /* Register MTD */
       ret = mtd_device_register(mtd, NULL, 0);
       
       return ret;
   }

JFFS2 Filesystem Usage
----------------------

.. code-block:: bash

   # Create JFFS2 image
   mkfs.jffs2 -r rootfs/ -o rootfs.jffs2 -e 128KiB -l -n
   
   # Flash to NAND
   flash_eraseall /dev/mtd2
   nandwrite -p /dev/mtd2 rootfs.jffs2
   
   # Mount
   mount -t jffs2 /dev/mtdblock2 /mnt

USB Drivers
===========

USB Bulk Transfer Driver
-------------------------

**Custom USB Device Driver:**

.. code-block:: c

   // drivers/usb/misc/custom_bulk.c
   
   #include <linux/usb.h>
   
   #define VENDOR_ID  0x1234
   #define PRODUCT_ID 0x5678
   
   struct usb_bulk_dev {
       struct usb_device *udev;
       struct usb_interface *interface;
       
       /* Bulk endpoints */
       u8 bulk_in_endpointAddr;
       u8 bulk_out_endpointAddr;
       size_t bulk_in_size;
       
       /* Buffers */
       char *bulk_in_buffer;
       struct urb *bulk_in_urb;
   };
   
   /* URB completion callback */
   static void bulk_read_callback(struct urb *urb)
   {
       struct usb_bulk_dev *dev = urb->context;
       
       if (urb->status) {
           dev_err(&dev->interface->dev,
                   "Bulk read failed: %d\n", urb->status);
           return;
       }
       
       /* Process received data */
       process_bulk_data(dev->bulk_in_buffer, urb->actual_length);
       
       /* Resubmit URB for continuous reading */
       usb_submit_urb(urb, GFP_ATOMIC);
   }
   
   /* Write to bulk endpoint */
   static ssize_t bulk_write(struct file *file, const char __user *user_buffer,
                             size_t count, loff_t *ppos)
   {
       struct usb_bulk_dev *dev = file->private_data;
       char *buf;
       int retval;
       
       buf = kmalloc(count, GFP_KERNEL);
       if (!buf)
           return -ENOMEM;
       
       if (copy_from_user(buf, user_buffer, count)) {
           kfree(buf);
           return -EFAULT;
       }
       
       /* Synchronous bulk transfer */
       retval = usb_bulk_msg(dev->udev,
                            usb_sndbulkpipe(dev->udev,
                                           dev->bulk_out_endpointAddr),
                            buf, count, NULL, 5000);
       
       kfree(buf);
       
       return (retval < 0) ? retval : count;
   }
   
   static int bulk_probe(struct usb_interface *interface,
                        const struct usb_device_id *id)
   {
       struct usb_bulk_dev *dev;
       struct usb_endpoint_descriptor *endpoint;
       int i;
       
       dev = kzalloc(sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       dev->udev = usb_get_dev(interface_to_usbdev(interface));
       dev->interface = interface;
       
       /* Find endpoints */
       for (i = 0; i < interface->cur_altsetting->desc.bNumEndpoints; i++) {
           endpoint = &interface->cur_altsetting->endpoint[i].desc;
           
           if (usb_endpoint_is_bulk_in(endpoint)) {
               dev->bulk_in_endpointAddr = endpoint->bEndpointAddress;
               dev->bulk_in_size = endpoint->wMaxPacketSize;
           }
           
           if (usb_endpoint_is_bulk_out(endpoint)) {
               dev->bulk_out_endpointAddr = endpoint->bEndpointAddress;
           }
       }
       
       /* Allocate buffer for bulk read */
       dev->bulk_in_buffer = kmalloc(dev->bulk_in_size, GFP_KERNEL);
       
       /* Create URB */
       dev->bulk_in_urb = usb_alloc_urb(0, GFP_KERNEL);
       usb_fill_bulk_urb(dev->bulk_in_urb, dev->udev,
                        usb_rcvbulkpipe(dev->udev,
                                       dev->bulk_in_endpointAddr),
                        dev->bulk_in_buffer, dev->bulk_in_size,
                        bulk_read_callback, dev);
       
       /* Submit URB */
       usb_submit_urb(dev->bulk_in_urb, GFP_KERNEL);
       
       usb_set_intfdata(interface, dev);
       
       return 0;
   }
   
   static const struct usb_device_id bulk_table[] = {
       { USB_DEVICE(VENDOR_ID, PRODUCT_ID) },
       {}
   };
   MODULE_DEVICE_TABLE(usb, bulk_table);
   
   static struct usb_driver bulk_driver = {
       .name       = "usb_bulk",
       .probe      = bulk_probe,
       .disconnect = bulk_disconnect,
       .id_table   = bulk_table,
   };
   
   module_usb_driver(bulk_driver);

USB Isochronous Transfer (Video/Audio)
---------------------------------------

**Isochronous Video Capture:**

.. code-block:: c

   // USB video streaming with isochronous transfers
   
   #define NUM_ISOC_URBS  4
   #define ISOC_PACKETS   32
   
   struct usb_video_dev {
       struct usb_device *udev;
       struct urb *isoc_urbs[NUM_ISOC_URBS];
       u8 *isoc_buffers[NUM_ISOC_URBS];
       int isoc_packet_size;
   };
   
   static void isoc_complete(struct urb *urb)
   {
       struct usb_video_dev *video = urb->context;
       int i;
       
       for (i = 0; i < urb->number_of_packets; i++) {
           if (urb->iso_frame_desc[i].status == 0) {
               void *data = urb->transfer_buffer +
                           urb->iso_frame_desc[i].offset;
               int len = urb->iso_frame_desc[i].actual_length;
               
               /* Process video frame data */
               process_video_packet(data, len);
           }
       }
       
       /* Resubmit URB */
       usb_submit_urb(urb, GFP_ATOMIC);
   }
   
   static int start_isoc_transfer(struct usb_video_dev *video)
   {
       int i, j;
       
       for (i = 0; i < NUM_ISOC_URBS; i++) {
           struct urb *urb = usb_alloc_urb(ISOC_PACKETS, GFP_KERNEL);
           
           video->isoc_buffers[i] = kmalloc(
               video->isoc_packet_size * ISOC_PACKETS, GFP_KERNEL);
           
           urb->dev = video->udev;
           urb->context = video;
           urb->pipe = usb_rcvisocpipe(video->udev, 0x81);  // EP1 IN
           urb->transfer_flags = URB_ISO_ASAP;
           urb->interval = 1;  // Every microframe (125μs)
           urb->transfer_buffer = video->isoc_buffers[i];
           urb->transfer_buffer_length =
               video->isoc_packet_size * ISOC_PACKETS;
           urb->complete = isoc_complete;
           urb->number_of_packets = ISOC_PACKETS;
           
           for (j = 0; j < ISOC_PACKETS; j++) {
               urb->iso_frame_desc[j].offset =
                   j * video->isoc_packet_size;
               urb->iso_frame_desc[j].length =
                   video->isoc_packet_size;
           }
           
           video->isoc_urbs[i] = urb;
           usb_submit_urb(urb, GFP_KERNEL);
       }
       
       return 0;
   }

PCIe Drivers
============

PCIe Platform Driver
--------------------

**FPGA PCIe Device Driver (Project: Avionics):**

.. code-block:: c

   // drivers/fpga/avionics_fpga_pcie.c
   
   #define VENDOR_ID  0x10EE  // Xilinx
   #define DEVICE_ID  0x7024  // Custom FPGA
   
   struct fpga_device {
       struct pci_dev *pdev;
       void __iomem *bar0;
       void __iomem *bar2;
       
       /* DMA */
       dma_addr_t dma_handle;
       void *dma_buffer;
       size_t dma_size;
       
       /* Interrupts */
       int irq_count;
       struct msix_entry msix_entries[4];
       
       /* Character device */
       struct cdev cdev;
       dev_t devt;
   };
   
   /* DMA transfer to/from FPGA */
   static int fpga_dma_transfer(struct fpga_device *fpga,
                               void *buffer, size_t size,
                               int direction)
   {
       dma_addr_t dma_addr;
       u32 status;
       
       /* Map buffer for DMA */
       dma_addr = dma_map_single(&fpga->pdev->dev, buffer, size,
                                direction ? DMA_TO_DEVICE : DMA_FROM_DEVICE);
       
       /* Program DMA controller */
       iowrite32(lower_32_bits(dma_addr), fpga->bar0 + DMA_SRC_ADDR_LO);
       iowrite32(upper_32_bits(dma_addr), fpga->bar0 + DMA_SRC_ADDR_HI);
       iowrite32(size, fpga->bar0 + DMA_LENGTH);
       iowrite32(DMA_START | (direction ? DMA_WRITE : DMA_READ),
                fpga->bar0 + DMA_CTRL);
       
       /* Wait for completion (interrupt or poll) */
       wait_event_interruptible(fpga->dma_wait_queue,
                               ioread32(fpga->bar0 + DMA_STATUS) & DMA_DONE);
       
       /* Check errors */
       status = ioread32(fpga->bar0 + DMA_STATUS);
       if (status & DMA_ERROR) {
           dev_err(&fpga->pdev->dev, "DMA error: 0x%x\n", status);
           return -EIO;
       }
       
       dma_unmap_single(&fpga->pdev->dev, dma_addr, size,
                       direction ? DMA_TO_DEVICE : DMA_FROM_DEVICE);
       
       return 0;
   }
   
   /* MSI-X interrupt handler */
   static irqreturn_t fpga_irq_handler(int irq, void *dev_id)
   {
       struct fpga_device *fpga = dev_id;
       u32 status;
       
       status = ioread32(fpga->bar0 + IRQ_STATUS);
       
       if (status & IRQ_DMA_DONE) {
           wake_up_interruptible(&fpga->dma_wait_queue);
           iowrite32(IRQ_DMA_DONE, fpga->bar0 + IRQ_CLEAR);
       }
       
       if (status & IRQ_ERROR) {
           dev_err(&fpga->pdev->dev, "FPGA error interrupt\n");
           iowrite32(IRQ_ERROR, fpga->bar0 + IRQ_CLEAR);
       }
       
       return IRQ_HANDLED;
   }
   
   static int fpga_probe(struct pci_dev *pdev,
                        const struct pci_device_id *id)
   {
       struct fpga_device *fpga;
       int ret, i;
       
       fpga = devm_kzalloc(&pdev->dev, sizeof(*fpga), GFP_KERNEL);
       if (!fpga)
           return -ENOMEM;
       
       fpga->pdev = pdev;
       
       /* Enable device */
       ret = pci_enable_device(pdev);
       if (ret)
           return ret;
       
       /* Request regions */
       ret = pci_request_regions(pdev, "avionics-fpga");
       if (ret)
           goto err_disable;
       
       /* Map BARs */
       fpga->bar0 = pci_ioremap_bar(pdev, 0);
       fpga->bar2 = pci_ioremap_bar(pdev, 2);
       
       if (!fpga->bar0 || !fpga->bar2) {
           ret = -ENOMEM;
           goto err_release;
       }
       
       /* Enable bus mastering for DMA */
       pci_set_master(pdev);
       
       /* Set DMA mask */
       ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(64));
       if (ret)
           ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(32));
       
       /* Allocate DMA buffer */
       fpga->dma_size = 4 * 1024 * 1024;  // 4MB
       fpga->dma_buffer = dma_alloc_coherent(&pdev->dev,
                                             fpga->dma_size,
                                             &fpga->dma_handle,
                                             GFP_KERNEL);
       
       /* Enable MSI-X */
       for (i = 0; i < 4; i++)
           fpga->msix_entries[i].entry = i;
       
       ret = pci_enable_msix_exact(pdev, fpga->msix_entries, 4);
       if (ret) {
           dev_warn(&pdev->dev, "MSI-X failed, trying MSI\n");
           ret = pci_enable_msi(pdev);
       }
       
       /* Register interrupt handlers */
       for (i = 0; i < 4; i++) {
           ret = request_irq(fpga->msix_entries[i].vector,
                           fpga_irq_handler, 0,
                           "avionics-fpga", fpga);
       }
       
       /* Create character device */
       alloc_chrdev_region(&fpga->devt, 0, 1, "fpga");
       cdev_init(&fpga->cdev, &fpga_fops);
       cdev_add(&fpga->cdev, fpga->devt, 1);
       
       pci_set_drvdata(pdev, fpga);
       
       dev_info(&pdev->dev, "FPGA device initialized\n");
       
       return 0;
       
   err_release:
       pci_release_regions(pdev);
   err_disable:
       pci_disable_device(pdev);
       return ret;
   }
   
   static const struct pci_device_id fpga_id_table[] = {
       { PCI_DEVICE(VENDOR_ID, DEVICE_ID) },
       { 0, }
   };
   MODULE_DEVICE_TABLE(pci, fpga_id_table);
   
   static struct pci_driver fpga_driver = {
       .name     = "avionics-fpga",
       .id_table = fpga_id_table,
       .probe    = fpga_probe,
       .remove   = fpga_remove,
   };
   
   module_pci_driver(fpga_driver);

Multiple PCIe Root Complex Support
-----------------------------------

**Platform-Specific RC Configuration:**

.. code-block:: c

   // drivers/pci/controller/pcie-atom-c3xxx.c
   
   struct atom_pcie_rc {
       void __iomem *dbi_base;
       void __iomem *cfg_base;
       int rc_id;  // 0-3
       struct pci_host_bridge *bridge;
   };
   
   /* Custom config access for multi-RC */
   static void __iomem *atom_pcie_map_bus(struct pci_bus *bus,
                                          unsigned int devfn,
                                          int where)
   {
       struct atom_pcie_rc *rc = bus->sysdata;
       
       /* Calculate config space address based on RC ID */
       return rc->cfg_base + ((bus->number - rc->bridge->busnr) << 20) +
              (devfn << 12) + where;
   }
   
   static int atom_pcie_rd_conf(struct pci_bus *bus, u32 devfn,
                               int where, int size, u32 *val)
   {
       void __iomem *addr = atom_pcie_map_bus(bus, devfn, where);
       
       if (!addr) {
           *val = ~0;
           return PCIBIOS_DEVICE_NOT_FOUND;
       }
       
       switch (size) {
       case 1:
           *val = readb(addr);
           break;
       case 2:
           *val = readw(addr);
           break;
       case 4:
           *val = readl(addr);
           break;
       }
       
       return PCIBIOS_SUCCESSFUL;
   }

I2C and SPI Drivers
===================

I2C Sensor Driver
-----------------

**IMU Sensor Driver:**

.. code-block:: c

   // drivers/iio/imu/custom_imu.c
   
   #include <linux/i2c.h>
   #include <linux/iio/iio.h>
   
   #define IMU_REG_ACCEL_X  0x28
   #define IMU_REG_GYRO_X   0x42
   
   struct imu_data {
       struct i2c_client *client;
       struct mutex lock;
       s16 accel[3];
       s16 gyro[3];
   };
   
   static int imu_read_sensor(struct imu_data *imu)
   {
       struct i2c_client *client = imu->client;
       u8 buf[12];
       int ret;
       
       mutex_lock(&imu->lock);
       
       /* Read accelerometer (6 bytes) */
       ret = i2c_smbus_read_i2c_block_data(client, IMU_REG_ACCEL_X,
                                           6, buf);
       if (ret < 0)
           goto out;
       
       imu->accel[0] = (s16)(buf[1] << 8 | buf[0]);
       imu->accel[1] = (s16)(buf[3] << 8 | buf[2]);
       imu->accel[2] = (s16)(buf[5] << 8 | buf[4]);
       
       /* Read gyroscope (6 bytes) */
       ret = i2c_smbus_read_i2c_block_data(client, IMU_REG_GYRO_X,
                                           6, buf + 6);
       if (ret < 0)
           goto out;
       
       imu->gyro[0] = (s16)(buf[7] << 8 | buf[6]);
       imu->gyro[1] = (s16)(buf[9] << 8 | buf[8]);
       imu->gyro[2] = (s16)(buf[11] << 8 | buf[10]);
       
       ret = 0;
       
   out:
       mutex_unlock(&imu->lock);
       return ret;
   }
   
   static int imu_read_raw(struct iio_dev *indio_dev,
                          struct iio_chan_spec const *chan,
                          int *val, int *val2, long mask)
   {
       struct imu_data *imu = iio_priv(indio_dev);
       int ret;
       
       ret = imu_read_sensor(imu);
       if (ret)
           return ret;
       
       switch (mask) {
       case IIO_CHAN_INFO_RAW:
           if (chan->type == IIO_ACCEL)
               *val = imu->accel[chan->channel2];
           else if (chan->type == IIO_ANGL_VEL)
               *val = imu->gyro[chan->channel2];
           return IIO_VAL_INT;
       }
       
       return -EINVAL;
   }
   
   static const struct iio_info imu_info = {
       .read_raw = imu_read_raw,
   };
   
   static int imu_probe(struct i2c_client *client,
                       const struct i2c_device_id *id)
   {
       struct iio_dev *indio_dev;
       struct imu_data *imu;
       
       indio_dev = devm_iio_device_alloc(&client->dev, sizeof(*imu));
       if (!indio_dev)
           return -ENOMEM;
       
       imu = iio_priv(indio_dev);
       imu->client = client;
       mutex_init(&imu->lock);
       
       indio_dev->name = "custom-imu";
       indio_dev->info = &imu_info;
       indio_dev->modes = INDIO_DIRECT_MODE;
       
       return devm_iio_device_register(&client->dev, indio_dev);
   }

SPI Flash Driver
----------------

**SPI NOR Flash:**

.. code-block:: c

   // drivers/mtd/spi-nor/custom-spi.c
   
   #include <linux/spi/spi.h>
   #include <linux/mtd/spi-nor.h>
   
   #define SPINOR_OP_READ_FAST  0x0B
   #define SPINOR_OP_PP         0x02
   #define SPINOR_OP_SE         0xD8  // Sector erase
   
   struct spi_nor_dev {
       struct spi_device *spi;
       struct spi_nor nor;
       struct mtd_info mtd;
   };
   
   static int spi_nor_read(struct spi_nor *nor, loff_t from,
                          size_t len, u_char *buf)
   {
       struct spi_nor_dev *dev = nor->priv;
       struct spi_transfer t[2];
       struct spi_message m;
       u8 cmd[5];
       
       cmd[0] = SPINOR_OP_READ_FAST;
       cmd[1] = (from >> 16) & 0xFF;
       cmd[2] = (from >> 8) & 0xFF;
       cmd[3] = from & 0xFF;
       cmd[4] = 0;  // Dummy byte
       
       spi_message_init(&m);
       
       memset(t, 0, sizeof(t));
       t[0].tx_buf = cmd;
       t[0].len = 5;
       spi_message_add_tail(&t[0], &m);
       
       t[1].rx_buf = buf;
       t[1].len = len;
       spi_message_add_tail(&t[1], &m);
       
       return spi_sync(dev->spi, &m);
   }
   
   static int spi_nor_write(struct spi_nor *nor, loff_t to,
                           size_t len, const u_char *buf)
   {
       struct spi_nor_dev *dev = nor->priv;
       u8 cmd[4];
       
       /* Enable write */
       spi_nor_write_enable(nor);
       
       cmd[0] = SPINOR_OP_PP;
       cmd[1] = (to >> 16) & 0xFF;
       cmd[2] = (to >> 8) & 0xFF;
       cmd[3] = to & 0xFF;
       
       /* Write data */
       struct spi_transfer t[2] = {
           { .tx_buf = cmd, .len = 4 },
           { .tx_buf = buf, .len = len }
       };
       struct spi_message m;
       
       spi_message_init_with_transfers(&m, t, 2);
       spi_sync(dev->spi, &m);
       
       /* Wait for completion */
       return spi_nor_wait_till_ready(nor);
   }

Wireless Drivers
================

**Wi-Fi Driver Integration:**

.. code-block:: c

   // Platform-specific Wi-Fi power control
   
   static int wifi_power_on(struct device *dev)
   {
       struct gpio_desc *power_gpio;
       struct gpio_desc *reset_gpio;
       
       power_gpio = devm_gpiod_get(dev, "power", GPIOD_OUT_LOW);
       reset_gpio = devm_gpiod_get(dev, "reset", GPIOD_OUT_LOW);
       
       /* Power on sequence */
       gpiod_set_value(power_gpio, 1);
       msleep(100);
       
       /* Release reset */
       gpiod_set_value(reset_gpio, 1);
       msleep(200);
       
       return 0;
   }

Best Practices
==============

Driver Development Guidelines
------------------------------

1. **Error Handling**
   - Always check return values
   - Use appropriate error codes
   - Clean up resources on error paths

2. **Locking**
   - Protect shared data structures
   - Use appropriate lock types (spinlock vs mutex)
   - Avoid deadlocks

3. **Memory Management**
   - Use devm_* functions when possible
   - Free all allocated memory
   - Handle DMA coherency correctly

4. **Power Management**
   - Implement runtime PM callbacks
   - Support system suspend/resume

5. **Device Tree**
   - Document bindings
   - Use standard properties
   - Support multiple board configurations

Debugging Techniques
--------------------

.. code-block:: bash

   # Dynamic debug
   echo "file drivers/video/vpfe.c +p" > /sys/kernel/debug/dynamic_debug/control
   
   # ftrace
   echo function_graph > /sys/kernel/debug/tracing/current_tracer
   echo your_driver_function > /sys/kernel/debug/tracing/set_ftrace_filter
   
   # KGDB
   CONFIG_KGDB=y
   CONFIG_KGDB_SERIAL_CONSOLE=y

Testing
-------

.. code-block:: bash

   # Load module with parameters
   insmod custom_driver.ko debug=1
   
   # Check logs
   dmesg | tail -50
   
   # Test with debugfs
   cat /sys/kernel/debug/custom_driver/status
   
   # Stress test
   while true; do
       dd if=/dev/video0 of=/dev/null bs=1M count=100
   done

References
==========

- Linux Device Drivers (LDD3)
- Linux Kernel Documentation
- V4L2 API Specification
- USB 2.0/3.0 Specification
- PCIe Base Specification
- I2C Specification
- SPI Protocol
- SocketCAN Documentation

