================================================================================
Linux Camera & Multimedia Subsystem - Comprehensive Reference
================================================================================

**V4L2, Camera HAL, MIPI CSI-2/DSI, Image Processing**

**Last Updated:** January 2026

**Author:** Comprehensive consolidation from kernel sources

================================================================================

TL;DR - Quick Reference
================================================================================

**Video4Linux2 (V4L2) - The Standard (2026)**

::

    V4L2 = Unified API for video capture/output/codec devices
    
    User Space: open → QUERYCAP → S_FMT → REQBUFS → mmap
                → QBUF (all) → STREAMON → DQBUF loop → STREAMOFF
    
    Kernel: video_device + v4l2_ioctl_ops + videobuf2 framework
    
    Most Common: MMAP buffers (fastest), MJPEG/YUYV/NV12 formats

**Quick V4L2 Capture Workflow**

.. code-block:: c

    // 1. Open device
    int fd = open("/dev/video0", O_RDWR);
    
    // 2. Check capabilities
    struct v4l2_capability cap;
    ioctl(fd, VIDIOC_QUERYCAP, &cap);
    
    // 3. Set format (1920x1080 MJPEG)
    struct v4l2_format fmt = {0};
    fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.width = 1920;
    fmt.fmt.pix.height = 1080;
    fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_MJPEG;
    ioctl(fd, VIDIOC_S_FMT, &fmt);
    
    // 4. Request buffers (MMAP)
    struct v4l2_requestbuffers req = {0};
    req.count = 4;
    req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory = V4L2_MEMORY_MMAP;
    ioctl(fd, VIDIOC_REQBUFS, &req);
    
    // 5. mmap + queue buffers
    for (i = 0; i < 4; i++) {
        struct v4l2_buffer buf = {0};
        buf.type = req.type;
        buf.memory = req.memory;
        buf.index = i;
        ioctl(fd, VIDIOC_QUERYBUF, &buf);
        buffers[i] = mmap(NULL, buf.length, PROT_READ | PROT_WRITE,
                         MAP_SHARED, fd, buf.m.offset);
        ioctl(fd, VIDIOC_QBUF, &buf);
    }
    
    // 6. Start streaming
    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ioctl(fd, VIDIOC_STREAMON, &type);
    
    // 7. Capture loop
    while (running) {
        struct v4l2_buffer buf = {0};
        buf.type = type;
        buf.memory = V4L2_MEMORY_MMAP;
        ioctl(fd, VIDIOC_DQBUF, &buf);  // Get filled buffer
        process_frame(buffers[buf.index], buf.bytesused);
        ioctl(fd, VIDIOC_QBUF, &buf);   // Return buffer
    }
    
    // 8. Stop + cleanup
    ioctl(fd, VIDIOC_STREAMOFF, &type);
    close(fd);

**Critical V4L2 IOCTLs**

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - IOCTL
     - Purpose
     - Typical Usage
   * - **VIDIOC_QUERYCAP**
     - Get device capabilities
     - Must be first call
   * - **VIDIOC_ENUM_FMT**
     - List supported formats
     - Iterate with index++
   * - **VIDIOC_S_FMT**
     - Set format
     - Width/height/pixelformat
   * - **VIDIOC_REQBUFS**
     - Request buffers
     - count=0 to free
   * - **VIDIOC_QBUF**
     - Queue buffer
     - Give buffer to driver
   * - **VIDIOC_DQBUF**
     - Dequeue buffer
     - Get filled buffer (blocks)
   * - **VIDIOC_STREAMON**
     - Start capture
     - After buffers queued
   * - **VIDIOC_STREAMOFF**
     - Stop capture
     - Drains buffers

**Common Pixel Formats**

::

    MJPEG (MJPG): Motion JPEG (compressed) - USB webcams
    YUYV (YUY2): 4:2:2 packed - Universal fallback
    NV12: Y + UV interleaved (4:2:0) - Hardware encoders
    NV21: Y + VU interleaved - Android
    RGB3/RGB4: 24/32-bit RGB - Display
    GREY: 8-bit grayscale

**MIPI CSI-2 (Camera Serial Interface)**

::

    CSI-2 = High-speed serial interface for cameras
    
    Architecture:
    Camera Sensor → MIPI CSI-2 TX (D-PHY lanes)
                  → CSI-2 RX (SoC)
                  → ISP (Image Signal Processor)
                  → Memory (V4L2 buffers)
    
    Key Points:
    - 1-4 data lanes + 1 clock lane
    - Packet-based protocol (SOT, header, data, checksum, EOT)
    - Data rates: 80 Mbps - 2.5 Gbps per lane
    - Virtual channels: 4 per physical link

**MIPI DSI (Display Serial Interface)**

::

    DSI = High-speed serial interface for displays
    
    Architecture:
    GPU/DPU → MIPI DSI TX (D-PHY lanes)
            → DSI RX (Display Panel)
            → Panel Controller
    
    Key Points:
    - Similar to CSI-2 but for display
    - Command mode (low power) vs Video mode (continuous)
    - DCS (Display Command Set) for panel control
    - Typically 2-4 data lanes

**Essential Command-Line Tools**

.. code-block:: bash

    # V4L2 device info
    v4l2-ctl --list-devices
    v4l2-ctl -d /dev/video0 --all
    
    # List formats
    v4l2-ctl --list-formats-ext
    
    # Capture frame
    v4l2-ctl --set-fmt-video=width=1280,height=720,pixelformat=MJPG \\
             --stream-mmap --stream-to=frame.jpg --stream-count=1
    
    # Media controller topology
    media-ctl -p -d /dev/media0
    
    # Set media pipeline
    media-ctl -d /dev/media0 --set-v4l2 '"sensor":0[fmt:SBGGR10_1X10/1920x1080]'
    
    # Compliance test
    v4l2-compliance -d /dev/video0

**Camera Pipeline (Typical SoC)**

::

    Sensor → CSI-2 RX → ISP Pipeline → Memory
                       ├─ Debayer (RAW to RGB)
                       ├─ 3A (Auto Exposure/Focus/White Balance)
                       ├─ Denoise
                       ├─ Color correction
                       ├─ Scaling/cropping
                       └─ Format conversion (RGB→YUV)
    
    V4L2 Subdevices:
    /dev/v4l-subdev0 → Sensor
    /dev/v4l-subdev1 → CSI-2 receiver
    /dev/v4l-subdev2 → ISP
    /dev/video0 → Output (capture interface)

**Key Kernel Structures**

.. code-block:: c

    struct video_device        // Main device node
    struct v4l2_device         // Top-level device
    struct v4l2_subdev         // Pipeline component (sensor, ISP)
    struct vb2_queue           // Videobuf2 buffer queue
    struct v4l2_ctrl_handler   // Control handler (brightness, etc.)
    struct v4l2_fh             // File handle

================================================================================

1. V4L2 Framework Deep Dive
================================================================================

1.1 Architecture Overview
--------------------------

**V4L2 Layers:**

.. code-block:: text

    User Space Application
           ↓ (ioctl, read/write, mmap)
    /dev/videoN (character device)
           ↓
    V4L2 Core (video_device)
           ├─ IOCTL handling (v4l2_ioctl_ops)
           ├─ Buffer management (videobuf2)
           └─ Control framework (v4l2_ctrl)
           ↓
    Driver Implementation
           ├─ Hardware access
           ├─ DMA setup
           └─ Interrupt handling
           ↓
    Hardware (Camera, Capture Card, Codec)

**Device Types:**

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Type
     - Node
     - Purpose
   * - **Video Capture**
     - /dev/videoN
     - Cameras, TV tuners, capture cards
   * - **Video Output**
     - /dev/videoN
     - Display devices, encoders
   * - **Video M2M**
     - /dev/videoN
     - Memory-to-memory (codecs, scalers)
   * - **V4L2 Subdev**
     - /dev/v4l-subdevN
     - Pipeline components (sensors, ISP)
   * - **Media Controller**
     - /dev/mediaN
     - Topology management

1.2 Kernel Driver Structure
----------------------------

**Minimal V4L2 Driver Template:**

.. code-block:: c

    #include <media/v4l2-device.h>
    #include <media/v4l2-ioctl.h>
    #include <media/v4l2-ctrls.h>
    #include <media/videobuf2-v4l2.h>
    #include <media/videobuf2-dma-contig.h>
    
    struct my_camera_dev {
        struct v4l2_device v4l2_dev;
        struct video_device vdev;
        struct v4l2_ctrl_handler ctrl_handler;
        struct vb2_queue queue;
        
        void __iomem *regs;
        int irq;
        
        struct mutex lock;
        spinlock_t qlock;
        
        u32 width;
        u32 height;
        u32 pixelformat;
    };
    
    // Videobuf2 operations
    static int queue_setup(struct vb2_queue *vq,
                          unsigned int *nbuffers,
                          unsigned int *nplanes,
                          unsigned int sizes[],
                          struct device *alloc_devs[]) {
        struct my_camera_dev *dev = vb2_get_drv_priv(vq);
        
        *nplanes = 1;
        sizes[0] = dev->width * dev->height * 2;  // YUYV = 2 bytes/pixel
        
        return 0;
    }
    
    static int buffer_prepare(struct vb2_buffer *vb) {
        struct my_camera_dev *dev = vb2_get_drv_priv(vb->vb2_queue);
        unsigned long size = dev->width * dev->height * 2;
        
        if (vb2_plane_size(vb, 0) < size)
            return -EINVAL;
        
        vb2_set_plane_payload(vb, 0, size);
        return 0;
    }
    
    static void buffer_queue(struct vb2_buffer *vb) {
        struct my_camera_dev *dev = vb2_get_drv_priv(vb->vb2_queue);
        struct vb2_v4l2_buffer *vbuf = to_vb2_v4l2_buffer(vb);
        
        spin_lock(&dev->qlock);
        list_add_tail(&vbuf->list, &dev->buf_list);
        spin_unlock(&dev->qlock);
    }
    
    static int start_streaming(struct vb2_queue *vq, unsigned int count) {
        struct my_camera_dev *dev = vb2_get_drv_priv(vq);
        
        // Enable hardware interrupts
        writel(CAM_IRQ_ENABLE, dev->regs + CAM_IRQ_REG);
        
        // Start DMA
        writel(CAM_DMA_START, dev->regs + CAM_DMA_CTRL);
        
        return 0;
    }
    
    static void stop_streaming(struct vb2_queue *vq) {
        struct my_camera_dev *dev = vb2_get_drv_priv(vq);
        
        // Stop hardware
        writel(CAM_DMA_STOP, dev->regs + CAM_DMA_CTRL);
        writel(CAM_IRQ_DISABLE, dev->regs + CAM_IRQ_REG);
        
        // Return all buffers
        while (!list_empty(&dev->buf_list)) {
            struct vb2_v4l2_buffer *buf = list_first_entry(&dev->buf_list,
                                            struct vb2_v4l2_buffer, list);
            list_del(&buf->list);
            vb2_buffer_done(&buf->vb2_buf, VB2_BUF_STATE_ERROR);
        }
    }
    
    static const struct vb2_ops my_vb2_ops = {
        .queue_setup     = queue_setup,
        .buf_prepare     = buffer_prepare,
        .buf_queue       = buffer_queue,
        .start_streaming = start_streaming,
        .stop_streaming  = stop_streaming,
        .wait_prepare    = vb2_ops_wait_prepare,
        .wait_finish     = vb2_ops_wait_finish,
    };
    
    // V4L2 IOCTL operations
    static int vidioc_querycap(struct file *file, void *priv,
                              struct v4l2_capability *cap) {
        struct my_camera_dev *dev = video_drvdata(file);
        
        strscpy(cap->driver, "my_camera", sizeof(cap->driver));
        strscpy(cap->card, "My Camera Device", sizeof(cap->card));
        snprintf(cap->bus_info, sizeof(cap->bus_info),
                 "platform:%s", dev_name(&dev->pdev->dev));
        
        cap->capabilities = V4L2_CAP_VIDEO_CAPTURE |
                           V4L2_CAP_STREAMING |
                           V4L2_CAP_DEVICE_CAPS;
        cap->device_caps = V4L2_CAP_VIDEO_CAPTURE | V4L2_CAP_STREAMING;
        
        return 0;
    }
    
    static int vidioc_enum_fmt(struct file *file, void *priv,
                              struct v4l2_fmtdesc *f) {
        static const struct {
            u32 fourcc;
            const char *description;
        } formats[] = {
            { V4L2_PIX_FMT_YUYV, "YUYV 4:2:2" },
            { V4L2_PIX_FMT_MJPEG, "Motion-JPEG" },
            { V4L2_PIX_FMT_NV12, "Y/CbCr 4:2:0" },
        };
        
        if (f->index >= ARRAY_SIZE(formats))
            return -EINVAL;
        
        f->pixelformat = formats[f->index].fourcc;
        strscpy(f->description, formats[f->index].description,
                sizeof(f->description));
        
        return 0;
    }
    
    static int vidioc_g_fmt(struct file *file, void *priv,
                           struct v4l2_format *f) {
        struct my_camera_dev *dev = video_drvdata(file);
        
        f->fmt.pix.width = dev->width;
        f->fmt.pix.height = dev->height;
        f->fmt.pix.pixelformat = dev->pixelformat;
        f->fmt.pix.field = V4L2_FIELD_NONE;
        f->fmt.pix.bytesperline = dev->width * 2;  // YUYV
        f->fmt.pix.sizeimage = dev->width * dev->height * 2;
        f->fmt.pix.colorspace = V4L2_COLORSPACE_SRGB;
        
        return 0;
    }
    
    static int vidioc_s_fmt(struct file *file, void *priv,
                           struct v4l2_format *f) {
        struct my_camera_dev *dev = video_drvdata(file);
        
        if (vb2_is_busy(&dev->queue))
            return -EBUSY;
        
        // Validate and adjust
        if (f->fmt.pix.width < 640)
            f->fmt.pix.width = 640;
        if (f->fmt.pix.width > 1920)
            f->fmt.pix.width = 1920;
        
        if (f->fmt.pix.height < 480)
            f->fmt.pix.height = 480;
        if (f->fmt.pix.height > 1080)
            f->fmt.pix.height = 1080;
        
        // Set format
        dev->width = f->fmt.pix.width;
        dev->height = f->fmt.pix.height;
        dev->pixelformat = f->fmt.pix.pixelformat;
        
        // Configure hardware
        writel(dev->width, dev->regs + CAM_WIDTH_REG);
        writel(dev->height, dev->regs + CAM_HEIGHT_REG);
        
        return vidioc_g_fmt(file, priv, f);
    }
    
    static const struct v4l2_ioctl_ops my_ioctl_ops = {
        .vidioc_querycap          = vidioc_querycap,
        .vidioc_enum_fmt_vid_cap  = vidioc_enum_fmt,
        .vidioc_g_fmt_vid_cap     = vidioc_g_fmt,
        .vidioc_s_fmt_vid_cap     = vidioc_s_fmt,
        .vidioc_try_fmt_vid_cap   = vidioc_s_fmt,
        
        // Videobuf2 helpers
        .vidioc_reqbufs           = vb2_ioctl_reqbufs,
        .vidioc_querybuf          = vb2_ioctl_querybuf,
        .vidioc_qbuf              = vb2_ioctl_qbuf,
        .vidioc_dqbuf             = vb2_ioctl_dqbuf,
        .vidioc_streamon          = vb2_ioctl_streamon,
        .vidioc_streamoff         = vb2_ioctl_streamoff,
    };
    
    // Interrupt handler
    static irqreturn_t my_camera_irq(int irq, void *dev_id) {
        struct my_camera_dev *dev = dev_id;
        u32 status = readl(dev->regs + CAM_IRQ_STATUS);
        
        if (!(status & CAM_IRQ_FRAME_DONE))
            return IRQ_NONE;
        
        // Clear interrupt
        writel(status, dev->regs + CAM_IRQ_STATUS);
        
        // Get next buffer
        spin_lock(&dev->qlock);
        if (!list_empty(&dev->buf_list)) {
            struct vb2_v4l2_buffer *buf = list_first_entry(&dev->buf_list,
                                            struct vb2_v4l2_buffer, list);
            list_del(&buf->list);
            
            // Mark buffer as done
            buf->vb2_buf.timestamp = ktime_get_ns();
            buf->sequence = dev->sequence++;
            vb2_buffer_done(&buf->vb2_buf, VB2_BUF_STATE_DONE);
        }
        spin_unlock(&dev->qlock);
        
        return IRQ_HANDLED;
    }
    
    // Probe function
    static int my_camera_probe(struct platform_device *pdev) {
        struct my_camera_dev *dev;
        struct vb2_queue *q;
        int ret;
        
        dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
        if (!dev)
            return -ENOMEM;
        
        dev->pdev = pdev;
        mutex_init(&dev->lock);
        spin_lock_init(&dev->qlock);
        INIT_LIST_HEAD(&dev->buf_list);
        
        // Get resources
        dev->regs = devm_platform_ioremap_resource(pdev, 0);
        if (IS_ERR(dev->regs))
            return PTR_ERR(dev->regs);
        
        dev->irq = platform_get_irq(pdev, 0);
        if (dev->irq < 0)
            return dev->irq;
        
        ret = devm_request_irq(&pdev->dev, dev->irq, my_camera_irq,
                              0, dev_name(&pdev->dev), dev);
        if (ret)
            return ret;
        
        // Register V4L2 device
        ret = v4l2_device_register(&pdev->dev, &dev->v4l2_dev);
        if (ret)
            return ret;
        
        // Initialize videobuf2 queue
        q = &dev->queue;
        q->type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        q->io_modes = VB2_MMAP | VB2_USERPTR | VB2_DMABUF;
        q->drv_priv = dev;
        q->buf_struct_size = sizeof(struct vb2_v4l2_buffer);
        q->ops = &my_vb2_ops;
        q->mem_ops = &vb2_dma_contig_memops;
        q->timestamp_flags = V4L2_BUF_FLAG_TIMESTAMP_MONOTONIC;
        q->lock = &dev->lock;
        q->dev = &pdev->dev;
        
        ret = vb2_queue_init(q);
        if (ret)
            goto err_unreg_v4l2;
        
        // Initialize video device
        dev->vdev.v4l2_dev = &dev->v4l2_dev;
        dev->vdev.queue = q;
        dev->vdev.fops = &my_fops;
        dev->vdev.ioctl_ops = &my_ioctl_ops;
        dev->vdev.release = video_device_release_empty;
        dev->vdev.lock = &dev->lock;
        dev->vdev.device_caps = V4L2_CAP_VIDEO_CAPTURE | V4L2_CAP_STREAMING;
        strscpy(dev->vdev.name, "my_camera", sizeof(dev->vdev.name));
        video_set_drvdata(&dev->vdev, dev);
        
        // Set default format
        dev->width = 1280;
        dev->height = 720;
        dev->pixelformat = V4L2_PIX_FMT_YUYV;
        
        // Register video device
        ret = video_register_device(&dev->vdev, VFL_TYPE_VIDEO, -1);
        if (ret)
            goto err_unreg_v4l2;
        
        platform_set_drvdata(pdev, dev);
        
        dev_info(&pdev->dev, "V4L2 device registered as %s\n",
                 video_device_node_name(&dev->vdev));
        
        return 0;
        
    err_unreg_v4l2:
        v4l2_device_unregister(&dev->v4l2_dev);
        return ret;
    }

1.3 Control Framework
----------------------

**Adding Camera Controls (Brightness, Contrast, etc.):**

.. code-block:: c

    // In probe function after v4l2_device_register
    v4l2_ctrl_handler_init(&dev->ctrl_handler, 4);
    
    v4l2_ctrl_new_std(&dev->ctrl_handler, &my_ctrl_ops,
                     V4L2_CID_BRIGHTNESS, 0, 255, 1, 128);
    v4l2_ctrl_new_std(&dev->ctrl_handler, &my_ctrl_ops,
                     V4L2_CID_CONTRAST, 0, 255, 1, 128);
    v4l2_ctrl_new_std(&dev->ctrl_handler, &my_ctrl_ops,
                     V4L2_CID_SATURATION, 0, 255, 1, 128);
    v4l2_ctrl_new_std(&dev->ctrl_handler, &my_ctrl_ops,
                     V4L2_CID_HUE, -180, 180, 1, 0);
    
    if (dev->ctrl_handler.error) {
        ret = dev->ctrl_handler.error;
        goto err_ctrl;
    }
    
    dev->v4l2_dev.ctrl_handler = &dev->ctrl_handler;
    dev->vdev.ctrl_handler = &dev->ctrl_handler;
    
    // Control operations
    static const struct v4l2_ctrl_ops my_ctrl_ops = {
        .s_ctrl = my_s_ctrl,
    };
    
    static int my_s_ctrl(struct v4l2_ctrl *ctrl) {
        struct my_camera_dev *dev = container_of(ctrl->handler,
                                struct my_camera_dev, ctrl_handler);
        
        switch (ctrl->id) {
        case V4L2_CID_BRIGHTNESS:
            writel(ctrl->val, dev->regs + CAM_BRIGHTNESS_REG);
            break;
        case V4L2_CID_CONTRAST:
            writel(ctrl->val, dev->regs + CAM_CONTRAST_REG);
            break;
        default:
            return -EINVAL;
        }
        
        return 0;
    }

================================================================================

2. MIPI CSI-2 & DSI Protocols
================================================================================

2.1 MIPI CSI-2 (Camera Serial Interface)
-----------------------------------------

**Architecture:**

.. code-block:: text

    Camera Sensor → CSI-2 TX (Transmitter)
                  ↓
    D-PHY Physical Layer (1-4 data lanes + 1 clock lane)
                  ↓
    CSI-2 RX (Receiver in SoC) → ISP → Memory

**Key Characteristics:**

- **Data rates:** 80 Mbps to 2.5 Gbps per lane
- **Lanes:** 1, 2, or 4 data lanes (D0-D3) + 1 clock lane
- **Virtual channels:** 4 per physical link (VC0-VC3)
- **Packet-based:** SOT → Header → Payload → Checksum → EOT

**Device Tree Example:**

.. code-block:: dts

    &mipi_csi {
        status = "okay";
        #address-cells = <1>;
        #size-cells = <0>;
        
        port@0 {
            reg = <0>;
            mipi_csi_in: endpoint {
                remote-endpoint = <&ov5640_out>;
                data-lanes = <1 2>;
                clock-lanes = <0>;
                link-frequencies = /bits/ 64 <297000000>;
            };
        };
    };
    
    &i2c1 {
        ov5640: camera@3c {
            compatible = "ovti,ov5640";
            reg = <0x3c>;
            clocks = <&clk_cam_mclk>;
            
            port {
                ov5640_out: endpoint {
                    remote-endpoint = <&mipi_csi_in>;
                    clock-lanes = <0>;
                    data-lanes = <1 2>;
                };
            };
        };
    };

2.2 MIPI DSI (Display Serial Interface)
----------------------------------------

**Architecture:**

.. code-block:: text

    GPU/Display Controller → DSI TX
                           ↓
    D-PHY (2-4 data lanes)
                           ↓
    DSI RX (in panel) → Panel Controller → LCD

**Operating Modes:**

1. **Video Mode:** Continuous pixel stream (like HDMI)
2. **Command Mode:** Send commands + data packets (low power)

**DCS Commands (Display Command Set):**

.. code-block:: c

    MIPI_DCS_SOFT_RESET       = 0x01
    MIPI_DCS_GET_DISPLAY_ID   = 0x04
    MIPI_DCS_SET_DISPLAY_ON   = 0x29
    MIPI_DCS_SET_DISPLAY_OFF  = 0x28
    MIPI_DCS_WRITE_MEMORY     = 0x2C
    MIPI_DCS_SET_BRIGHTNESS   = 0x51

**Example Driver Snippet:**

.. code-block:: c

    struct mipi_dsi_device *dsi;
    
    // Send DCS command
    mipi_dsi_dcs_write(dsi, MIPI_DCS_SET_DISPLAY_ON, NULL, 0);
    
    // Generic write
    u8 data[] = {0x00, 0x01};
    mipi_dsi_generic_write(dsi, data, sizeof(data));

================================================================================

3. Camera Pipeline & Image Processing
================================================================================

3.1 Typical ISP Pipeline
-------------------------

::

    RAW Sensor Data (Bayer pattern)
           ↓
    [1] Defect Pixel Correction
           ↓
    [2] Black Level Correction
           ↓
    [3] Lens Shading Correction
           ↓
    [4] Demosaic (Bayer → RGB)
           ↓
    [5] White Balance
           ↓
    [6] Color Correction Matrix (CCM)
           ↓
    [7] Gamma Correction
           ↓
    [8] Noise Reduction (spatial + temporal)
           ↓
    [9] Sharpening / Edge Enhancement
           ↓
    [10] Color Space Conversion (RGB → YUV)
           ↓
    [11] Scaling / Cropping
           ↓
    Output (YUYV, NV12, MJPEG, etc.)

3.2 Media Controller Framework
-------------------------------

**Purpose:** Manage complex camera pipelines with multiple subdevices

**Example Topology:**

.. code-block:: bash

    media-ctl -p
    
    # Output:
    - entity 1: ov5640 (sensor)
        [fmt:SBGGR10_1X10/1920x1080]
        pad0: Source → csi2_rx
    
    - entity 2: csi2_rx
        pad0: Sink ← ov5640
        pad1: Source → isp
    
    - entity 3: isp
        pad0: Sink ← csi2_rx
        pad1: Source → video0
    
    - entity 4: video0 (capture)
        pad0: Sink ← isp

**Configure Pipeline:**

.. code-block:: bash

    # Set sensor format
    media-ctl -V '"ov5640":0[fmt:SBGGR10_1X10/1920x1080]'
    
    # Set CSI-2 format
    media-ctl -V '"csi2_rx":1[fmt:SBGGR10_1X10/1920x1080]'
    
    # Set ISP output
    media-ctl -V '"isp":1[fmt:YUYV8_1X16/1920x1080]'

================================================================================

4. Debugging & Monitoring
================================================================================

4.1 Essential Commands
-----------------------

.. code-block:: bash

    # List all V4L2 devices
    v4l2-ctl --list-devices
    
    # Get detailed info
    v4l2-ctl -d /dev/video0 --all
    
    # List supported formats
    v4l2-ctl -d /dev/video0 --list-formats-ext
    
    # List controls
    v4l2-ctl -d /dev/video0 --list-ctrls
    
    # Set control
    v4l2-ctl -d /dev/video0 -c brightness=150
    
    # Capture test frame
    v4l2-ctl -d /dev/video0 --set-fmt-video=width=1280,height=720,pixelformat=MJPG \\
             --stream-mmap=3 --stream-count=1 --stream-to=test.jpg
    
    # Compliance test
    v4l2-compliance -d /dev/video0 -s
    
    # Media controller info
    media-ctl -d /dev/media0 -p
    
    # List subdevices
    ls -l /dev/v4l-subdev*
    
    # Kernel logs
    dmesg | grep -i v4l2
    dmesg | grep -i video

4.2 Common Issues
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Issue
     - Symptoms
     - Solution
   * - **No frames**
     - DQBUF times out
     - Check STREAMON, verify buffers queued, check IRQ
   * - **Format not supported**
     - S_FMT fails
     - Use ENUM_FMT to list supported formats
   * - **Buffer allocation fails**
     - REQBUFS returns error
     - Check CMA size (cma= kernel parameter)
   * - **Media pipeline error**
     - -EPIPE on STREAMON
     - Configure all subdevs in chain (media-ctl)
   * - **Poor image quality**
     - Dark/color cast
     - Tune ISP (white balance, gamma, CCM)

================================================================================

5. Exam Question: Complete V4L2 Driver
================================================================================

**Question (15 points):**

You need to implement a V4L2 driver for a simple camera sensor connected via platform bus. The sensor:
- Supports 640x480 and 1280x720 resolutions
- Outputs YUYV format only
- Generates frame-done interrupt
- Has brightness control register (0-255)

**Part A (8 points):** Implement the probe function including V4L2 device registration, videobuf2 queue initialization, and control handler setup.

**Part B (4 points):** Implement the interrupt handler that marks buffers as done.

**Part C (3 points):** What happens if you forget to call vb2_buffer_done() in the IRQ handler? How would you debug it?

**Answer:**

**Part A: Probe Function**

.. code-block:: c

    static int sensor_probe(struct platform_device *pdev) {
        struct sensor_dev *sensor;
        struct vb2_queue *q;
        int ret;
        
        sensor = devm_kzalloc(&pdev->dev, sizeof(*sensor), GFP_KERNEL);
        if (!sensor)
            return -ENOMEM;
        
        sensor->pdev = pdev;
        mutex_init(&sensor->lock);
        spin_lock_init(&sensor->qlock);
        INIT_LIST_HEAD(&sensor->buf_list);
        
        // Get MMIO registers
        sensor->regs = devm_platform_ioremap_resource(pdev, 0);
        if (IS_ERR(sensor->regs))
            return PTR_ERR(sensor->regs);
        
        // Get IRQ
        sensor->irq = platform_get_irq(pdev, 0);
        if (sensor->irq < 0)
            return sensor->irq;
        
        ret = devm_request_irq(&pdev->dev, sensor->irq,
                              sensor_irq_handler, 0,
                              "sensor", sensor);
        if (ret)
            return ret;
        
        // Register V4L2 device
        ret = v4l2_device_register(&pdev->dev, &sensor->v4l2_dev);
        if (ret)
            return ret;
        
        // Initialize control handler
        v4l2_ctrl_handler_init(&sensor->ctrl_hdl, 1);
        v4l2_ctrl_new_std(&sensor->ctrl_hdl, &sensor_ctrl_ops,
                         V4L2_CID_BRIGHTNESS, 0, 255, 1, 128);
        
        if (sensor->ctrl_hdl.error) {
            ret = sensor->ctrl_hdl.error;
            goto err_unreg_v4l2;
        }
        
        sensor->v4l2_dev.ctrl_handler = &sensor->ctrl_hdl;
        
        // Initialize videobuf2 queue
        q = &sensor->queue;
        q->type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        q->io_modes = VB2_MMAP | VB2_DMABUF;
        q->drv_priv = sensor;
        q->buf_struct_size = sizeof(struct vb2_v4l2_buffer);
        q->ops = &sensor_vb2_ops;
        q->mem_ops = &vb2_dma_contig_memops;
        q->timestamp_flags = V4L2_BUF_FLAG_TIMESTAMP_MONOTONIC;
        q->lock = &sensor->lock;
        q->dev = &pdev->dev;
        
        ret = vb2_queue_init(q);
        if (ret)
            goto err_ctrl;
        
        // Initialize video_device
        sensor->vdev.v4l2_dev = &sensor->v4l2_dev;
        sensor->vdev.queue = q;
        sensor->vdev.fops = &sensor_fops;
        sensor->vdev.ioctl_ops = &sensor_ioctl_ops;
        sensor->vdev.release = video_device_release_empty;
        sensor->vdev.lock = &sensor->lock;
        sensor->vdev.ctrl_handler = &sensor->ctrl_hdl;
        strscpy(sensor->vdev.name, "sensor", sizeof(sensor->vdev.name));
        video_set_drvdata(&sensor->vdev, sensor);
        
        // Default format: 640x480 YUYV
        sensor->width = 640;
        sensor->height = 480;
        sensor->pixelformat = V4L2_PIX_FMT_YUYV;
        
        // Register video device
        ret = video_register_device(&sensor->vdev, VFL_TYPE_VIDEO, -1);
        if (ret)
            goto err_ctrl;
        
        platform_set_drvdata(pdev, sensor);
        
        dev_info(&pdev->dev, "Registered as %s\n",
                 video_device_node_name(&sensor->vdev));
        
        return 0;
        
    err_ctrl:
        v4l2_ctrl_handler_free(&sensor->ctrl_hdl);
    err_unreg_v4l2:
        v4l2_device_unregister(&sensor->v4l2_dev);
        return ret;
    }

**Part B: Interrupt Handler**

.. code-block:: c

    static irqreturn_t sensor_irq_handler(int irq, void *dev_id) {
        struct sensor_dev *sensor = dev_id;
        u32 status = readl(sensor->regs + SENSOR_IRQ_STATUS);
        
        // Check if frame-done interrupt
        if (!(status & SENSOR_IRQ_FRAME_DONE))
            return IRQ_NONE;
        
        // Clear interrupt
        writel(SENSOR_IRQ_FRAME_DONE, sensor->regs + SENSOR_IRQ_STATUS);
        
        // Get next buffer from queue
        spin_lock(&sensor->qlock);
        if (!list_empty(&sensor->buf_list)) {
            struct vb2_v4l2_buffer *vbuf;
            
            vbuf = list_first_entry(&sensor->buf_list,
                                   struct vb2_v4l2_buffer, list);
            list_del(&vbuf->list);
            
            // Fill buffer metadata
            vbuf->vb2_buf.timestamp = ktime_get_ns();
            vbuf->sequence = sensor->sequence++;
            vbuf->field = V4L2_FIELD_NONE;
            
            // Mark buffer as filled successfully
            vb2_buffer_done(&vbuf->vb2_buf, VB2_BUF_STATE_DONE);
        }
        spin_unlock(&sensor->qlock);
        
        return IRQ_HANDLED;
    }

**Part C: Missing vb2_buffer_done() Analysis**

**What happens:**

1. **User space blocks indefinitely** on VIDIOC_DQBUF
2. Buffers stay in driver queue, never returned to application
3. After 4-8 buffers (typical queue depth), REQBUFS exhausted
4. Subsequent frames dropped (no free buffers)
5. Application sees timeout or no new frames

**Debugging steps:**

.. code-block:: bash

    # 1. Check if IRQ is firing
    cat /proc/interrupts | grep sensor
    # Count should increase each frame (~30/sec for 30 FPS)
    
    # 2. Check dmesg for videobuf2 errors
    dmesg | grep vb2
    # May show "timeout waiting for buffer" or similar
    
    # 3. Add debug prints in IRQ handler
    printk(KERN_DEBUG "IRQ: status=0x%x, buf_list=%s\n",
           status, list_empty(&sensor->buf_list) ? "empty" : "has bufs");
    
    # 4. Check if buffers are queued
    # In user space, verify QBUF succeeds before STREAMON
    
    # 5. Use ftrace to trace vb2_buffer_done calls
    echo 1 > /sys/kernel/debug/tracing/events/vb2/vb2_buf_done/enable
    cat /sys/kernel/debug/tracing/trace_pipe
    # Should see one event per frame

**Root cause:** IRQ fires, buffer is dequeued from list, but vb2_buffer_done() never called → buffer "leaked" in kernel, never returned to application.

**Fix:** Always call vb2_buffer_done(), even on error (use VB2_BUF_STATE_ERROR).

================================================================================

6. Key Takeaways
================================================================================

**V4L2 Best Practices (2026):**

1. **Use Videobuf2 Framework**
   - Don't implement buffer management manually
   - vb2_ioctl_* helpers for standard ioctls
   - DMA-contiguous memory for best performance

2. **Media Controller for Complex Pipelines**
   - Sensors, ISP, encoders as separate entities
   - User space configures entire pipeline
   - V4L2 subdev interface for components

3. **Control Framework**
   - v4l2_ctrl for standard controls (brightness, etc.)
   - Automatic validation and caching
   - Cluster controls for related settings

4. **Always Handle Errors**
   - Return buffers with VB2_BUF_STATE_ERROR on failure
   - Check vb2_is_busy() before format changes
   - Validate user parameters

**Common Pixel Formats:**

::

    Compressed:  MJPEG (USB webcams)
    Packed YUV:  YUYV (universal), UYVY
    Planar YUV:  NV12 (encoders), NV21 (Android), YUV420
    RAW:         SBGGR8/10/12 (Bayer patterns)
    RGB:         RGB24, BGR32

**Quick Command Reference:**

.. code-block:: bash

    v4l2-ctl --list-devices
    v4l2-ctl -d /dev/video0 --all
    v4l2-ctl --list-formats-ext
    media-ctl -p
    v4l2-compliance -d /dev/video0

================================================================================

**Last Updated:** January 2026  
**Kernel Version:** 6.8+  
**Status:** Production Ready

================================================================================

