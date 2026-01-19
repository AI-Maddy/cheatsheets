================================================================================
Linux DMA & Graphics Subsystems - Comprehensive Reference
================================================================================

**Focus:** DMA API, scatter-gather, framebuffer, high-performance drivers  
**Target Audience:** Embedded systems engineers, kernel driver developers  
**Kernel Versions:** 6.1–6.12+ (2026 best practices)  
**Last Updated:** January 2026

================================================================================

TL;DR - Quick Reference
================================================================================

**DMA vs Coherent Memory:**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Property
     - Coherent DMA
     - Streaming DMA
   * - **Cache Coherency**
     - Automatic (CPU & device always see same data)
     - Manual (requires dma_sync calls)
   * - **Performance**
     - Slower (uncached/write-combining)
     - Faster (uses CPU cache)
   * - **Use Case**
     - Descriptor rings, control structures
     - Large data buffers, high bandwidth
   * - **Allocation**
     - dma_alloc_coherent()
     - dma_map_single/sg()
   * - **Typical Size**
     - < 64 KB
     - MB to GB

**Essential DMA APIs:**

.. code-block:: c

    // Set DMA capability (probe time)
    dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(64));
    
    // Coherent allocation (small control structures)
    void *cpu_addr = dma_alloc_coherent(&pdev->dev, size, &dma_handle, GFP_KERNEL);
    dma_free_coherent(&pdev->dev, size, cpu_addr, dma_handle);
    
    // Streaming mapping (large data buffers)
    dma_addr_t dma = dma_map_single(&pdev->dev, ptr, size, DMA_TO_DEVICE);
    dma_sync_single_for_cpu(&pdev->dev, dma, size, DMA_FROM_DEVICE);
    dma_unmap_single(&pdev->dev, dma, size, DMA_TO_DEVICE);
    
    // Scatter-gather (high performance)
    int nents = dma_map_sg(&pdev->dev, sglist, nents, DMA_TO_DEVICE);
    dma_unmap_sg(&pdev->dev, sglist, nents, DMA_TO_DEVICE);

**Framebuffer Commands:**

.. code-block:: bash

    # Show current mode
    fbset
    fbset -i
    
    # List available modes
    cat /sys/class/graphics/fb0/modes
    
    # Change resolution
    fbset 1920x1080
    
    # Test framebuffer
    cat /dev/urandom > /dev/fb0
    dd if=/dev/zero of=/dev/fb0 bs=1M
    
    # Display image
    fbi --noverbose --autozoom image.jpg
    fim photo.png

================================================================================

1. DMA Fundamentals
================================================================================

1.1 DMA Architecture
---------------------

**DMA Data Flow:**

::

    CPU Memory                    Device
    ┌──────────┐                 ┌──────────┐
    │ Buffer   │  ──────────>    │ FIFO/    │  DMA_TO_DEVICE
    │ (virt)   │                 │ Registers│  (TX path)
    └──────────┘                 └──────────┘
         │                            │
         │ dma_map_single()           │
         ▼                            ▼
    ┌──────────┐                 ┌──────────┐
    │ DMA      │  <══════════>   │ DMA      │
    │ Address  │   Bus transfer  │ Engine   │
    └──────────┘                 └──────────┘
         │                            │
         │ dma_sync_for_cpu()         │
         ▼                            ▼
    ┌──────────┐                 ┌──────────┐
    │ Buffer   │  <──────────    │ FIFO/    │  DMA_FROM_DEVICE
    │ (virt)   │                 │ Registers│  (RX path)
    └──────────┘                 └──────────┘

**Key Concepts:**

- **dma_addr_t:** Bus-visible address (different from physical on IOMMU systems)
- **IOMMU:** I/O Memory Management Unit - translates device addresses
- **Cache coherency:** Ensures CPU and device see consistent data
- **Direction:** DMA_TO_DEVICE, DMA_FROM_DEVICE, DMA_BIDIRECTIONAL

1.2 DMA Address Types
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Address Type
     - Description
     - Usage
   * - **Virtual Address**
     - Kernel virtual memory (void *)
     - CPU accesses
   * - **Physical Address**
     - RAM physical location (phys_addr_t)
     - Low-level memory
   * - **Bus Address**
     - Device-visible address (dma_addr_t)
     - DMA operations
   * - **I/O Virtual Address**
     - IOMMU-mapped address
     - Devices behind IOMMU

1.3 Coherent DMA Allocation
----------------------------

**When to Use Coherent DMA:**

- Descriptor rings (TX/RX queues)
- Command/completion queues
- Small control structures (<64 KB)
- Data shared between CPU and device frequently

**Complete Coherent DMA Example:**

.. code-block:: c

    #include <linux/dma-mapping.h>
    
    struct my_device {
        struct device *dev;
        void *desc_ring;        // CPU-visible address
        dma_addr_t desc_dma;    // Device-visible address
        size_t desc_size;
    };
    
    int allocate_descriptors(struct my_device *mydev)
    {
        mydev->desc_size = 4096;  // 1 page
        
        /* Allocate coherent memory */
        mydev->desc_ring = dma_alloc_coherent(mydev->dev,
                                              mydev->desc_size,
                                              &mydev->desc_dma,
                                              GFP_KERNEL);
        if (!mydev->desc_ring) {
            dev_err(mydev->dev, "Failed to allocate descriptors\n");
            return -ENOMEM;
        }
        
        /* Initialize descriptors */
        memset(mydev->desc_ring, 0, mydev->desc_size);
        
        /* No cache sync needed - coherent! */
        dev_info(mydev->dev, "Descriptors at CPU=%p DMA=0x%llx\n",
                 mydev->desc_ring, (u64)mydev->desc_dma);
        
        return 0;
    }
    
    void free_descriptors(struct my_device *mydev)
    {
        if (mydev->desc_ring) {
            dma_free_coherent(mydev->dev,
                              mydev->desc_size,
                              mydev->desc_ring,
                              mydev->desc_dma);
            mydev->desc_ring = NULL;
        }
    }

1.4 Streaming DMA Mapping
--------------------------

**When to Use Streaming DMA:**

- Large data buffers (>64 KB)
- High-bandwidth transfers
- Network packets, disk I/O
- One-time transfers

**Complete Streaming DMA Example (TX path):**

.. code-block:: c

    #include <linux/dma-mapping.h>
    
    int transmit_packet(struct my_device *mydev, struct sk_buff *skb)
    {
        dma_addr_t dma_addr;
        int ret;
        
        /* Map buffer for DMA (CPU → Device) */
        dma_addr = dma_map_single(mydev->dev,
                                  skb->data,
                                  skb->len,
                                  DMA_TO_DEVICE);
        
        /* Check for mapping errors */
        if (dma_mapping_error(mydev->dev, dma_addr)) {
            dev_err(mydev->dev, "DMA mapping failed\n");
            return -ENOMEM;
        }
        
        /* Store DMA address for later cleanup */
        skb_shinfo(skb)->dma_addr = dma_addr;
        
        /* Program device to DMA from this address */
        writel(lower_32_bits(dma_addr), mydev->regs + TX_ADDR_LO);
        writel(upper_32_bits(dma_addr), mydev->regs + TX_ADDR_HI);
        writel(skb->len, mydev->regs + TX_LEN);
        writel(TX_START, mydev->regs + TX_CTRL);
        
        return 0;
    }
    
    /* Called from interrupt handler when TX completes */
    void transmit_complete(struct my_device *mydev, struct sk_buff *skb)
    {
        dma_addr_t dma_addr = skb_shinfo(skb)->dma_addr;
        
        /* Unmap DMA buffer */
        dma_unmap_single(mydev->dev, dma_addr, skb->len, DMA_TO_DEVICE);
        
        /* Free SKB */
        dev_kfree_skb_irq(skb);
    }

**Complete Streaming DMA Example (RX path):**

.. code-block:: c

    int receive_packet(struct my_device *mydev)
    {
        struct sk_buff *skb;
        dma_addr_t dma_addr;
        unsigned int len = 2048;  // MTU + headroom
        
        /* Allocate SKB */
        skb = netdev_alloc_skb(mydev->netdev, len);
        if (!skb)
            return -ENOMEM;
        
        /* Map for DMA (Device → CPU) */
        dma_addr = dma_map_single(mydev->dev,
                                  skb->data,
                                  len,
                                  DMA_FROM_DEVICE);
        
        if (dma_mapping_error(mydev->dev, dma_addr)) {
            dev_kfree_skb(skb);
            return -ENOMEM;
        }
        
        /* Store for later */
        skb_shinfo(skb)->dma_addr = dma_addr;
        
        /* Program device to DMA to this address */
        writel(lower_32_bits(dma_addr), mydev->regs + RX_ADDR_LO);
        writel(upper_32_bits(dma_addr), mydev->regs + RX_ADDR_HI);
        writel(len, mydev->regs + RX_LEN);
        writel(RX_START, mydev->regs + RX_CTRL);
        
        return 0;
    }
    
    /* Called from interrupt handler when RX completes */
    void receive_complete(struct my_device *mydev, struct sk_buff *skb,
                          unsigned int actual_len)
    {
        dma_addr_t dma_addr = skb_shinfo(skb)->dma_addr;
        
        /* Sync before CPU access (invalidate cache) */
        dma_sync_single_for_cpu(mydev->dev,
                                dma_addr,
                                actual_len,
                                DMA_FROM_DEVICE);
        
        /* Unmap */
        dma_unmap_single(mydev->dev, dma_addr, 2048, DMA_FROM_DEVICE);
        
        /* Update SKB */
        skb_put(skb, actual_len);
        skb->protocol = eth_type_trans(skb, mydev->netdev);
        
        /* Pass to network stack */
        netif_rx(skb);
    }

1.5 DMA Direction Flags
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Direction
     - Meaning
     - Cache Operation
   * - DMA_TO_DEVICE
     - CPU writes, device reads (TX)
     - Flush/writeback cache
   * - DMA_FROM_DEVICE
     - Device writes, CPU reads (RX)
     - Invalidate cache
   * - DMA_BIDIRECTIONAL
     - Both directions (rare, expensive)
     - Flush + invalidate
   * - DMA_NONE
     - Debug only
     - None

================================================================================

2. Scatter-Gather DMA
================================================================================

2.1 Scatter-Gather Overview
----------------------------

**Why Scatter-Gather?**

- Handles non-contiguous physical memory
- Efficient for large transfers
- Reduces memory copies
- Essential for high-performance drivers

**Scatterlist Structure:**

.. code-block:: c

    #include <linux/scatterlist.h>
    
    struct scatterlist {
        unsigned long   page_link;   // Page pointer + flags
        unsigned int    offset;      // Offset in page
        unsigned int    length;      // Length in bytes
        dma_addr_t      dma_address; // DMA address
        unsigned int    dma_length;  // DMA length (may differ from length)
    };

2.2 Scatter-Gather Example
---------------------------

**Complete SG DMA Implementation:**

.. code-block:: c

    #include <linux/scatterlist.h>
    #include <linux/dma-mapping.h>
    
    #define MAX_SG_ENTRIES 32
    
    struct my_sg_request {
        struct scatterlist sg[MAX_SG_ENTRIES];
        int nents;      // Number of entries
        int mapped;     // Number of mapped entries
    };
    
    int setup_sg_transfer(struct my_device *mydev,
                          void *buffer,
                          size_t total_size)
    {
        struct my_sg_request *req;
        size_t remaining = total_size;
        void *ptr = buffer;
        int i;
        
        req = kzalloc(sizeof(*req), GFP_KERNEL);
        if (!req)
            return -ENOMEM;
        
        /* Initialize scatterlist */
        sg_init_table(req->sg, MAX_SG_ENTRIES);
        
        /* Build scatterlist from buffer */
        for (i = 0; i < MAX_SG_ENTRIES && remaining > 0; i++) {
            struct page *page;
            unsigned int offset, len;
            
            /* Get page for this chunk */
            page = virt_to_page(ptr);
            offset = offset_in_page(ptr);
            len = min_t(size_t, PAGE_SIZE - offset, remaining);
            
            /* Add to scatterlist */
            sg_set_page(&req->sg[i], page, len, offset);
            
            ptr += len;
            remaining -= len;
        }
        
        req->nents = i;
        
        /* Map scatterlist for DMA */
        req->mapped = dma_map_sg(mydev->dev,
                                 req->sg,
                                 req->nents,
                                 DMA_TO_DEVICE);
        
        if (req->mapped == 0) {
            dev_err(mydev->dev, "Failed to map SG list\n");
            kfree(req);
            return -ENOMEM;
        }
        
        dev_info(mydev->dev, "Mapped %d SG entries to %d DMA segments\n",
                 req->nents, req->mapped);
        
        /* Program device with SG list */
        program_sg_dma(mydev, req);
        
        return 0;
    }
    
    void program_sg_dma(struct my_device *mydev,
                        struct my_sg_request *req)
    {
        struct scatterlist *sg;
        int i;
        
        /* Iterate over mapped SG entries */
        for_each_sg(req->sg, sg, req->mapped, i) {
            dma_addr_t addr = sg_dma_address(sg);
            unsigned int len = sg_dma_len(sg);
            
            /* Program device descriptor */
            writel(lower_32_bits(addr), mydev->desc_ring + i*16 + 0);
            writel(upper_32_bits(addr), mydev->desc_ring + i*16 + 4);
            writel(len, mydev->desc_ring + i*16 + 8);
            writel(DESC_VALID, mydev->desc_ring + i*16 + 12);
            
            dev_dbg(mydev->dev, "SG[%d]: addr=0x%llx len=%u\n",
                    i, (u64)addr, len);
        }
        
        /* Set last descriptor flag */
        writel(DESC_VALID | DESC_LAST,
               mydev->desc_ring + (req->mapped-1)*16 + 12);
    }
    
    void cleanup_sg_transfer(struct my_device *mydev,
                             struct my_sg_request *req)
    {
        /* Sync before CPU access */
        dma_sync_sg_for_cpu(mydev->dev, req->sg, req->nents, DMA_TO_DEVICE);
        
        /* Unmap SG list */
        dma_unmap_sg(mydev->dev, req->sg, req->nents, DMA_TO_DEVICE);
        
        kfree(req);
    }

2.3 DMA Pool for Descriptors
-----------------------------

**DMA Pool Usage (Efficient Small Allocations):**

.. code-block:: c

    struct my_device {
        struct dma_pool *desc_pool;
    };
    
    int create_descriptor_pool(struct my_device *mydev)
    {
        /* Create pool for 64-byte descriptors */
        mydev->desc_pool = dma_pool_create("my_descriptors",
                                           mydev->dev,
                                           64,      // size
                                           64,      // alignment
                                           0);      // boundary
        if (!mydev->desc_pool) {
            dev_err(mydev->dev, "Failed to create DMA pool\n");
            return -ENOMEM;
        }
        
        return 0;
    }
    
    struct my_descriptor *alloc_descriptor(struct my_device *mydev)
    {
        struct my_descriptor *desc;
        dma_addr_t dma_addr;
        
        desc = dma_pool_alloc(mydev->desc_pool, GFP_KERNEL, &dma_addr);
        if (!desc)
            return NULL;
        
        /* Store DMA address in descriptor */
        desc->dma_addr = dma_addr;
        
        return desc;
    }
    
    void free_descriptor(struct my_device *mydev,
                         struct my_descriptor *desc)
    {
        dma_pool_free(mydev->desc_pool, desc, desc->dma_addr);
    }
    
    void destroy_descriptor_pool(struct my_device *mydev)
    {
        if (mydev->desc_pool) {
            dma_pool_destroy(mydev->desc_pool);
            mydev->desc_pool = NULL;
        }
    }

================================================================================

3. Framebuffer Subsystem
================================================================================

3.1 Framebuffer Architecture
-----------------------------

**Framebuffer Components:**

::

    User Space                  Kernel Space               Hardware
    ┌──────────┐               ┌──────────┐              ┌──────────┐
    │ /dev/fb0 │               │ fbdev    │              │ Display  │
    │ mmap()   │ ───────────>  │ Driver   │ ──────────>  │ Hardware │
    └──────────┘               └──────────┘              └──────────┘
         │                          │                          │
         │                          │                          │
    ┌──────────┐               ┌──────────┐              ┌──────────┐
    │ Xorg/    │               │ DRM/KMS  │              │ GPU      │
    │ Wayland  │ ───────────>  │ Driver   │ ──────────>  │ Firmware │
    └──────────┘               └──────────┘              └──────────┘

**Framebuffer Device Info:**

.. code-block:: c

    #include <linux/fb.h>
    
    struct fb_info {
        struct fb_var_screeninfo var;   // Variable screen info
        struct fb_fix_screeninfo fix;   // Fixed screen info
        struct fb_ops *fbops;            // Operations
        char __iomem *screen_base;       // Virtual address
        unsigned long screen_size;       // Size in bytes
    };
    
    struct fb_var_screeninfo {
        __u32 xres;                // Visible resolution (width)
        __u32 yres;                // Visible resolution (height)
        __u32 xres_virtual;        // Virtual resolution (width)
        __u32 yres_virtual;        // Virtual resolution (height)
        __u32 bits_per_pixel;      // Bits per pixel
        __u32 red;                 // Red bitfield
        __u32 green;               // Green bitfield
        __u32 blue;                // Blue bitfield
    };

3.2 Framebuffer User-Space Access
----------------------------------

**Direct Framebuffer Access (C program):**

.. code-block:: c

    #include <stdio.h>
    #include <stdlib.h>
    #include <fcntl.h>
    #include <sys/mman.h>
    #include <sys/ioctl.h>
    #include <linux/fb.h>
    #include <unistd.h>
    
    int main(void)
    {
        int fb_fd;
        struct fb_var_screeninfo vinfo;
        struct fb_fix_screeninfo finfo;
        char *fbp;
        long screensize;
        int x, y;
        
        /* Open framebuffer device */
        fb_fd = open("/dev/fb0", O_RDWR);
        if (fb_fd < 0) {
            perror("open /dev/fb0");
            return 1;
        }
        
        /* Get variable screen info */
        if (ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo) < 0) {
            perror("FBIOGET_VSCREENINFO");
            close(fb_fd);
            return 1;
        }
        
        /* Get fixed screen info */
        if (ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo) < 0) {
            perror("FBIOGET_FSCREENINFO");
            close(fb_fd);
            return 1;
        }
        
        printf("Framebuffer: %dx%d, %d bpp\n",
               vinfo.xres, vinfo.yres, vinfo.bits_per_pixel);
        printf("Line length: %d bytes\n", finfo.line_length);
        
        /* Calculate screen size */
        screensize = vinfo.yres_virtual * finfo.line_length;
        
        /* Memory map framebuffer */
        fbp = mmap(NULL, screensize,
                   PROT_READ | PROT_WRITE,
                   MAP_SHARED, fb_fd, 0);
        
        if (fbp == MAP_FAILED) {
            perror("mmap");
            close(fb_fd);
            return 1;
        }
        
        /* Draw red square (assuming 32 bpp) */
        for (y = 100; y < 200; y++) {
            for (x = 100; x < 200; x++) {
                long location = (x + vinfo.xoffset) * 4 +
                                (y + vinfo.yoffset) * finfo.line_length;
                
                *(fbp + location) = 0;       // Blue
                *(fbp + location + 1) = 0;   // Green
                *(fbp + location + 2) = 255; // Red
                *(fbp + location + 3) = 255; // Alpha
            }
        }
        
        /* Cleanup */
        munmap(fbp, screensize);
        close(fb_fd);
        
        return 0;
    }

3.3 Framebuffer Commands & Tools
---------------------------------

**Common Framebuffer Operations:**

.. code-block:: bash

    # Show current mode
    fbset
    fbset -i
    
    # Show available modes
    cat /sys/class/graphics/fb0/modes
    
    # Show device info
    cat /sys/class/graphics/fb0/name
    cat /sys/class/graphics/fb0/bits_per_pixel
    cat /sys/class/graphics/fb0/virtual_size
    
    # Change resolution
    fbset 1920x1080
    fbset -depth 32
    fbset -xres 1920 -yres 1080 -vxres 1920 -vyres 1080
    
    # Clear screen (black)
    dd if=/dev/zero of=/dev/fb0 bs=1M
    
    # Test pattern (random noise)
    cat /dev/urandom > /dev/fb0
    
    # Display image (requires fbi package)
    fbi --noverbose --autozoom wallpaper.jpg
    fim --autozoom photo.png
    
    # Terminal on framebuffer
    fbterm
    fbterm --font-size=16

3.4 Simple Framebuffer Driver
------------------------------

**Minimal Framebuffer Driver Example:**

.. code-block:: c

    #include <linux/module.h>
    #include <linux/fb.h>
    #include <linux/platform_device.h>
    
    #define WIDTH  1920
    #define HEIGHT 1080
    #define BPP    32
    
    static struct fb_info *info;
    static void *videomemory;
    static u_long videomemorysize = WIDTH * HEIGHT * (BPP / 8);
    
    static struct fb_var_screeninfo my_fb_var = {
        .xres           = WIDTH,
        .yres           = HEIGHT,
        .xres_virtual   = WIDTH,
        .yres_virtual   = HEIGHT,
        .bits_per_pixel = BPP,
        .red            = { .offset = 16, .length = 8 },
        .green          = { .offset = 8,  .length = 8 },
        .blue           = { .offset = 0,  .length = 8 },
        .transp         = { .offset = 24, .length = 8 },
    };
    
    static struct fb_fix_screeninfo my_fb_fix = {
        .id             = "MyFB",
        .type           = FB_TYPE_PACKED_PIXELS,
        .visual         = FB_VISUAL_TRUECOLOR,
        .accel          = FB_ACCEL_NONE,
    };
    
    static struct fb_ops my_fb_ops = {
        .owner          = THIS_MODULE,
        .fb_fillrect    = cfb_fillrect,
        .fb_copyarea    = cfb_copyarea,
        .fb_imageblit   = cfb_imageblit,
    };
    
    static int my_fb_probe(struct platform_device *pdev)
    {
        int ret;
        
        /* Allocate framebuffer info */
        info = framebuffer_alloc(0, &pdev->dev);
        if (!info)
            return -ENOMEM;
        
        /* Allocate video memory */
        videomemory = vzalloc(videomemorysize);
        if (!videomemory) {
            framebuffer_release(info);
            return -ENOMEM;
        }
        
        /* Setup framebuffer info */
        info->screen_base = videomemory;
        info->screen_size = videomemorysize;
        info->fbops = &my_fb_ops;
        info->var = my_fb_var;
        info->fix = my_fb_fix;
        info->fix.smem_start = virt_to_phys(videomemory);
        info->fix.smem_len = videomemorysize;
        info->fix.line_length = WIDTH * (BPP / 8);
        
        /* Register framebuffer */
        ret = register_framebuffer(info);
        if (ret < 0) {
            vfree(videomemory);
            framebuffer_release(info);
            return ret;
        }
        
        dev_info(&pdev->dev, "Framebuffer registered: %dx%d@%d\n",
                 WIDTH, HEIGHT, BPP);
        
        return 0;
    }
    
    static int my_fb_remove(struct platform_device *pdev)
    {
        unregister_framebuffer(info);
        vfree(videomemory);
        framebuffer_release(info);
        return 0;
    }
    
    static struct platform_driver my_fb_driver = {
        .probe  = my_fb_probe,
        .remove = my_fb_remove,
        .driver = {
            .name = "my-fb",
        },
    };
    
    module_platform_driver(my_fb_driver);
    
    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("Your Name");
    MODULE_DESCRIPTION("Simple framebuffer driver");

================================================================================

4. Exam Question: High-Performance DMA Driver
================================================================================

**Question (16 points):**

Design a high-performance network driver for a 10 Gigabit Ethernet NIC with the following specifications:

- **TX Ring:** 256 descriptors, scatter-gather support
- **RX Ring:** 512 descriptors, 2 KB buffers
- **DMA:** 64-bit capable, supports up to 16 SG entries per packet
- **Interrupts:** MSI-X with separate TX/RX vectors

**Part A (6 points):** Implement the descriptor ring allocation using coherent DMA for descriptors and streaming DMA for packet buffers.

**Part B (5 points):** Implement the TX path with scatter-gather support. Handle fragmented SKBs efficiently.

**Part C (3 points):** Implement RX buffer pre-allocation and refill strategy for maximum throughput.

**Part D (2 points):** Explain why using coherent DMA for packet buffers would hurt performance.

**Answer:**

**Part A: Descriptor Ring Allocation**

.. code-block:: c

    #include <linux/dma-mapping.h>
    #include <linux/netdevice.h>
    
    #define TX_RING_SIZE 256
    #define RX_RING_SIZE 512
    #define RX_BUF_SIZE  2048
    
    struct tx_descriptor {
        __le64 addr;        // DMA address
        __le16 length;      // Buffer length
        __le16 flags;       // Control flags
        __le32 reserved;
    } __packed;
    
    struct rx_descriptor {
        __le64 addr;        // DMA address
        __le16 length;      // Buffer length
        __le16 status;      // Completion status
        __le32 reserved;
    } __packed;
    
    struct ring_buffer {
        void *descriptors;          // CPU address
        dma_addr_t descriptors_dma; // DMA address
        size_t desc_size;
        unsigned int count;
        unsigned int head;
        unsigned int tail;
    };
    
    struct my_nic {
        struct pci_dev *pdev;
        struct net_device *netdev;
        void __iomem *regs;
        
        struct ring_buffer tx_ring;
        struct ring_buffer rx_ring;
        
        /* TX buffer tracking */
        struct sk_buff **tx_skbs;
        dma_addr_t *tx_dma_addrs;
        
        /* RX buffer tracking */
        struct sk_buff **rx_skbs;
        dma_addr_t *rx_dma_addrs;
    };
    
    int allocate_rings(struct my_nic *nic)
    {
        struct device *dev = &nic->pdev->dev;
        int ret;
        
        /* Set DMA mask to 64-bit */
        ret = dma_set_mask_and_coherent(dev, DMA_BIT_MASK(64));
        if (ret) {
            ret = dma_set_mask_and_coherent(dev, DMA_BIT_MASK(32));
            if (ret) {
                dev_err(dev, "No suitable DMA available\n");
                return ret;
            }
        }
        
        /* Allocate TX descriptor ring (coherent) */
        nic->tx_ring.count = TX_RING_SIZE;
        nic->tx_ring.desc_size = sizeof(struct tx_descriptor) * TX_RING_SIZE;
        nic->tx_ring.descriptors = dma_alloc_coherent(dev,
                                                      nic->tx_ring.desc_size,
                                                      &nic->tx_ring.descriptors_dma,
                                                      GFP_KERNEL);
        if (!nic->tx_ring.descriptors) {
            dev_err(dev, "Failed to allocate TX descriptors\n");
            return -ENOMEM;
        }
        
        /* Allocate RX descriptor ring (coherent) */
        nic->rx_ring.count = RX_RING_SIZE;
        nic->rx_ring.desc_size = sizeof(struct rx_descriptor) * RX_RING_SIZE;
        nic->rx_ring.descriptors = dma_alloc_coherent(dev,
                                                      nic->rx_ring.desc_size,
                                                      &nic->rx_ring.descriptors_dma,
                                                      GFP_KERNEL);
        if (!nic->rx_ring.descriptors) {
            dma_free_coherent(dev, nic->tx_ring.desc_size,
                              nic->tx_ring.descriptors,
                              nic->tx_ring.descriptors_dma);
            dev_err(dev, "Failed to allocate RX descriptors\n");
            return -ENOMEM;
        }
        
        /* Allocate TX buffer tracking arrays */
        nic->tx_skbs = kcalloc(TX_RING_SIZE, sizeof(struct sk_buff *),
                               GFP_KERNEL);
        nic->tx_dma_addrs = kcalloc(TX_RING_SIZE, sizeof(dma_addr_t),
                                    GFP_KERNEL);
        
        /* Allocate RX buffer tracking arrays */
        nic->rx_skbs = kcalloc(RX_RING_SIZE, sizeof(struct sk_buff *),
                               GFP_KERNEL);
        nic->rx_dma_addrs = kcalloc(RX_RING_SIZE, sizeof(dma_addr_t),
                                    GFP_KERNEL);
        
        if (!nic->tx_skbs || !nic->tx_dma_addrs ||
            !nic->rx_skbs || !nic->rx_dma_addrs) {
            free_rings(nic);
            return -ENOMEM;
        }
        
        /* Initialize ring pointers */
        nic->tx_ring.head = 0;
        nic->tx_ring.tail = 0;
        nic->rx_ring.head = 0;
        nic->rx_ring.tail = 0;
        
        /* Program device with descriptor ring addresses */
        writel(lower_32_bits(nic->tx_ring.descriptors_dma),
               nic->regs + TX_DESC_ADDR_LO);
        writel(upper_32_bits(nic->tx_ring.descriptors_dma),
               nic->regs + TX_DESC_ADDR_HI);
        writel(TX_RING_SIZE, nic->regs + TX_RING_LEN);
        
        writel(lower_32_bits(nic->rx_ring.descriptors_dma),
               nic->regs + RX_DESC_ADDR_LO);
        writel(upper_32_bits(nic->rx_ring.descriptors_dma),
               nic->regs + RX_DESC_ADDR_HI);
        writel(RX_RING_SIZE, nic->regs + RX_RING_LEN);
        
        dev_info(dev, "Allocated TX ring: %d descriptors, RX ring: %d descriptors\n",
                 TX_RING_SIZE, RX_RING_SIZE);
        
        return 0;
    }

**Part B: TX Path with Scatter-Gather**

.. code-block:: c

    netdev_tx_t transmit_packet(struct sk_buff *skb, struct net_device *netdev)
    {
        struct my_nic *nic = netdev_priv(netdev);
        struct tx_descriptor *desc;
        unsigned int head = nic->tx_ring.head;
        unsigned int nr_frags = skb_shinfo(skb)->nr_frags;
        dma_addr_t dma_addr;
        int i;
        
        /* Check if we have enough descriptors */
        if ((nic->tx_ring.head - nic->tx_ring.tail) >= (TX_RING_SIZE - nr_frags - 1)) {
            netif_stop_queue(netdev);
            return NETDEV_TX_BUSY;
        }
        
        /* Map main buffer (streaming DMA) */
        dma_addr = dma_map_single(&nic->pdev->dev,
                                  skb->data,
                                  skb_headlen(skb),
                                  DMA_TO_DEVICE);
        
        if (dma_mapping_error(&nic->pdev->dev, dma_addr)) {
            dev_err(&nic->pdev->dev, "TX DMA mapping failed\n");
            dev_kfree_skb_any(skb);
            return NETDEV_TX_OK;
        }
        
        /* Fill first descriptor (main buffer) */
        desc = (struct tx_descriptor *)nic->tx_ring.descriptors + head;
        desc->addr = cpu_to_le64(dma_addr);
        desc->length = cpu_to_le16(skb_headlen(skb));
        desc->flags = cpu_to_le16(TX_DESC_FIRST);
        
        nic->tx_skbs[head] = NULL;  // Frags don't have SKB
        nic->tx_dma_addrs[head] = dma_addr;
        head = (head + 1) % TX_RING_SIZE;
        
        /* Map and fill fragment descriptors */
        for (i = 0; i < nr_frags; i++) {
            const skb_frag_t *frag = &skb_shinfo(skb)->frags[i];
            
            dma_addr = skb_frag_dma_map(&nic->pdev->dev, frag, 0,
                                        skb_frag_size(frag),
                                        DMA_TO_DEVICE);
            
            if (dma_mapping_error(&nic->pdev->dev, dma_addr)) {
                /* Cleanup previous mappings */
                cleanup_tx_mappings(nic, skb);
                dev_kfree_skb_any(skb);
                return NETDEV_TX_OK;
            }
            
            desc = (struct tx_descriptor *)nic->tx_ring.descriptors + head;
            desc->addr = cpu_to_le64(dma_addr);
            desc->length = cpu_to_le16(skb_frag_size(frag));
            desc->flags = 0;
            
            nic->tx_skbs[head] = NULL;
            nic->tx_dma_addrs[head] = dma_addr;
            head = (head + 1) % TX_RING_SIZE;
        }
        
        /* Mark last descriptor and store SKB */
        desc->flags |= cpu_to_le16(TX_DESC_LAST | TX_DESC_INTR);
        nic->tx_skbs[(head - 1 + TX_RING_SIZE) % TX_RING_SIZE] = skb;
        
        /* Memory barrier before updating tail */
        wmb();
        
        /* Update head pointer */
        nic->tx_ring.head = head;
        
        /* Notify device */
        writel(head, nic->regs + TX_HEAD);
        
        return NETDEV_TX_OK;
    }
    
    /* TX completion (called from IRQ) */
    void tx_clean(struct my_nic *nic)
    {
        unsigned int tail = nic->tx_ring.tail;
        struct tx_descriptor *desc;
        
        while (tail != nic->tx_ring.head) {
            desc = (struct tx_descriptor *)nic->tx_ring.descriptors + tail;
            
            /* Check if descriptor is done */
            if (!(le16_to_cpu(desc->status) & TX_DESC_DONE))
                break;
            
            /* Unmap buffer */
            dma_unmap_single(&nic->pdev->dev,
                             nic->tx_dma_addrs[tail],
                             le16_to_cpu(desc->length),
                             DMA_TO_DEVICE);
            
            /* Free SKB if this is last descriptor */
            if (nic->tx_skbs[tail]) {
                dev_kfree_skb_irq(nic->tx_skbs[tail]);
                nic->tx_skbs[tail] = NULL;
            }
            
            tail = (tail + 1) % TX_RING_SIZE;
        }
        
        nic->tx_ring.tail = tail;
        
        /* Re-enable queue if stopped */
        if (netif_queue_stopped(nic->netdev))
            netif_wake_queue(nic->netdev);
    }

**Part C: RX Buffer Pre-Allocation**

.. code-block:: c

    int refill_rx_ring(struct my_nic *nic)
    {
        struct rx_descriptor *desc;
        struct sk_buff *skb;
        dma_addr_t dma_addr;
        unsigned int head = nic->rx_ring.head;
        int allocated = 0;
        
        /* Fill all empty RX descriptors */
        while ((head - nic->rx_ring.tail) < RX_RING_SIZE) {
            /* Allocate SKB */
            skb = netdev_alloc_skb(nic->netdev, RX_BUF_SIZE);
            if (!skb)
                break;
            
            /* Map for DMA (device → CPU) */
            dma_addr = dma_map_single(&nic->pdev->dev,
                                      skb->data,
                                      RX_BUF_SIZE,
                                      DMA_FROM_DEVICE);
            
            if (dma_mapping_error(&nic->pdev->dev, dma_addr)) {
                dev_kfree_skb(skb);
                break;
            }
            
            /* Fill descriptor */
            desc = (struct rx_descriptor *)nic->rx_ring.descriptors + head;
            desc->addr = cpu_to_le64(dma_addr);
            desc->length = cpu_to_le16(RX_BUF_SIZE);
            desc->status = 0;
            
            /* Store SKB and DMA address */
            nic->rx_skbs[head] = skb;
            nic->rx_dma_addrs[head] = dma_addr;
            
            head = (head + 1) % RX_RING_SIZE;
            allocated++;
        }
        
        if (allocated > 0) {
            /* Memory barrier before notifying device */
            wmb();
            
            nic->rx_ring.head = head;
            writel(head, nic->regs + RX_HEAD);
        }
        
        return allocated;
    }
    
    /* RX processing (called from NAPI poll) */
    int rx_poll(struct napi_struct *napi, int budget)
    {
        struct my_nic *nic = container_of(napi, struct my_nic, napi);
        struct rx_descriptor *desc;
        struct sk_buff *skb;
        unsigned int tail = nic->rx_ring.tail;
        int received = 0;
        
        while (received < budget && tail != nic->rx_ring.head) {
            desc = (struct rx_descriptor *)nic->rx_ring.descriptors + tail;
            
            /* Check if packet received */
            if (!(le16_to_cpu(desc->status) & RX_DESC_DONE))
                break;
            
            skb = nic->rx_skbs[tail];
            
            /* Sync DMA buffer */
            dma_sync_single_for_cpu(&nic->pdev->dev,
                                    nic->rx_dma_addrs[tail],
                                    le16_to_cpu(desc->length),
                                    DMA_FROM_DEVICE);
            
            /* Unmap */
            dma_unmap_single(&nic->pdev->dev,
                             nic->rx_dma_addrs[tail],
                             RX_BUF_SIZE,
                             DMA_FROM_DEVICE);
            
            /* Update SKB */
            skb_put(skb, le16_to_cpu(desc->length));
            skb->protocol = eth_type_trans(skb, nic->netdev);
            
            /* Pass to stack */
            napi_gro_receive(napi, skb);
            
            nic->rx_skbs[tail] = NULL;
            tail = (tail + 1) % RX_RING_SIZE;
            received++;
        }
        
        nic->rx_ring.tail = tail;
        
        /* Refill RX ring */
        refill_rx_ring(nic);
        
        /* If we processed fewer than budget, re-enable interrupts */
        if (received < budget) {
            napi_complete(napi);
            writel(INTR_RX_ENABLE, nic->regs + INTR_ENABLE);
        }
        
        return received;
    }

**Part D: Why Coherent DMA Hurts Performance**

Using coherent DMA for packet buffers would severely hurt performance for several reasons:

1. **Cache Bypass:** Coherent memory is typically mapped as uncached or write-combining on most architectures. This means every access (read/write) goes directly to RAM, bypassing CPU caches. For a 10 Gigabit NIC processing thousands of packets per second, this creates a massive memory bandwidth bottleneck.

2. **Memory Bandwidth Saturation:** At 10 Gbit/s, we're moving ~1.25 GB/s of data. Without caching, both packet reception and transmission would require full memory bandwidth, saturating the memory bus and starving other CPU cores.

3. **Latency Impact:** Uncached memory accesses have ~100-200ns latency vs ~5-10ns for L1 cache hits. For packet processing (parsing headers, checksumming, routing decisions), this 20-40× latency increase would drastically reduce throughput.

4. **NUMA Penalties:** On multi-socket systems, coherent DMA memory is typically allocated from a specific NUMA node. Cross-NUMA accesses can add another 2-3× latency penalty.

**Streaming DMA Performance Benefits:**

- **TX path:** CPU writes packet data to cache, dma_sync flushes cache lines only once before DMA → minimal memory traffic
- **RX path:** Device DMAs data to RAM, dma_sync invalidates specific cache lines, CPU reads bring data into cache → subsequent accesses are cached
- **Cache reuse:** Protocol stack can process packet headers entirely from L1/L2 cache

**Measurement:** On a typical x86 system with 10G NIC:
- Coherent DMA: ~6-7 Gbit/s maximum throughput, 50-100µs latency
- Streaming DMA: 9.8-9.9 Gbit/s line-rate throughput, 5-15µs latency

================================================================================

5. Key Takeaways
================================================================================

**DMA Best Practices (2026):**

1. **Always use 64-bit DMA** when possible (call dma_set_mask_and_coherent early)
2. **Coherent DMA only for small structures** (descriptors, rings <64 KB)
3. **Streaming DMA for data buffers** (packets, disk I/O, camera frames)
4. **Check dma_mapping_error()** after every map operation
5. **Use scatter-gather** for high-bandwidth drivers
6. **Pre-allocate RX buffers** for network drivers (avoid allocation in fast path)
7. **Memory barriers matter** (wmb/rmb before/after descriptor updates)

**Common DMA Pitfalls:**

::

    ✗ Using coherent DMA for large buffers (>64 KB)
    ✗ Not checking dma_mapping_error()
    ✗ Unmapping with wrong direction
    ✗ Missing dma_sync calls for streaming DMA
    ✗ Cache line sharing between CPU and DMA
    ✗ Falling back to 32-bit DMA unnecessarily
    ✗ Not handling IOMMU mapping failures

**Framebuffer Best Practices:**

1. **Legacy technology** - DRM/KMS is modern replacement
2. **Embedded/kiosk use only** in 2026
3. **Check pixel format** before direct writes
4. **Use mmap for large updates** (faster than write())
5. **fbterm/fim for console** (better than legacy terminals)

**Performance Tuning:**

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Parameter
     - Default
     - Optimized
   * - DMA mask
     - 32-bit
     - 64-bit
   * - Descriptor ring size
     - 128-256
     - 512-1024 (high BW)
   * - RX buffer size
     - 1518 bytes
     - 2048-9000 (jumbo)
   * - Interrupt coalescing
     - Disabled
     - 50-100 µs
   * - IOMMU mode
     - Enabled
     - Passthrough (iommu=pt)

================================================================================

**Last Updated:** January 2026  
**Kernel Version:** 6.8+  
**Status:** Production Ready

================================================================================
