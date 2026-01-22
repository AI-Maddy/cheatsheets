===============================
SOC Platform Development Guide
===============================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Experience: NXP i.MX 93/6, TI DaVinci DM365, Intel Atom C3xxx

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
========

Comprehensive guide to SOC platform development covering heterogeneous multi-core systems, BSP development, peripheral integration, and platform bring-up based on real project experience across multiple SOC families.

SOC Architecture Fundamentals
==============================

Heterogeneous Multi-Core Systems
---------------------------------

**Architecture Patterns:**

.. code-block:: text

   Pattern 1: Application + Real-Time (AMP)
   ┌─────────────────┐     ┌─────────────────┐
   │  Cortex-A (Linux) │◄──►│ Cortex-M (RTOS)  │
   │  - Application    │     │ - Sensor Fusion  │
   │  - UI/Network     │     │ - Motor Control  │
   └─────────────────┘     └─────────────────┘
           │                        │
           └────────┬───────────────┘
                    │
           ┌────────▼────────┐
           │  Shared Memory  │
           │  Message Queue  │
           └─────────────────┘
   
   Pattern 2: SMP + Accelerators
   ┌──────────────────────────────┐
   │   Multi-Core A-Profile        │
   │   ┌───┐ ┌───┐ ┌───┐ ┌───┐    │
   │   │CPU│ │CPU│ │CPU│ │CPU│    │
   │   └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘    │
   └─────┼─────┼─────┼─────┼──────┘
         └─────┴─────┴─────┘
                 │
         ┌───────┴────────┐
         │  GPU/VPU/NPU   │
         │  ML Accelerator │
         └────────────────┘

**Memory Architecture:**

.. code-block:: text

   Typical i.MX 93 Memory Map:
   0x0000_0000 - 0x0010_0000: ROM (1MB)
   0x2020_0000 - 0x2024_0000: M33 TCM (256KB)
   0x4000_0000 - 0x5FFF_FFFF: Peripherals (512MB)
   0x8000_0000 - 0xFFFF_FFFF: LPDDR4 (2GB)
   
   Intel Atom C3xxx:
   0x0000_0000 - 0x7FFF_FFFF: Low RAM (2GB)
   0xE000_0000 - 0xEFFF_FFFF: PCIe MMIO
   0xF000_0000 - 0xFFFF_FFFF: Peripherals
   0x1_0000_0000+: High RAM (>4GB)

NXP i.MX Platform Development
==============================

i.MX 93 (Cortex-A55 + Cortex-M33)
----------------------------------

**Project: Smart Home Automation Hub**

Platform Architecture
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   i.MX 93 SOC Architecture:
   
   ┌──────────────────────────────────────────────┐
   │             Application Cores                 │
   │  ┌────────────────────────────────────────┐  │
   │  │  Dual Cortex-A55 @ 1.7GHz (SMP)       │  │
   │  │  - Linux Application Domain            │  │
   │  │  - 32KB L1 I-Cache, 32KB L1 D-Cache    │  │
   │  │  - 512KB L2 Cache (shared)             │  │
   │  └────────────────────────────────────────┘  │
   │                                               │
   │  ┌────────────────────────────────────────┐  │
   │  │  Cortex-M33 @ 250MHz                   │  │
   │  │  - FreeRTOS/Zephyr                     │  │
   │  │  - 256KB TCM (Tightly Coupled Memory)  │  │
   │  │  - Real-time peripherals control       │  │
   │  └────────────────────────────────────────┘  │
   └──────────────────────────────────────────────┘
   
   ┌──────────────────────────────────────────────┐
   │              Security & Crypto                │
   │  - ARM TrustZone                              │
   │  - EdgeLock Secure Enclave                    │
   │  - HAB (High Assurance Boot)                  │
   │  - CAAM (Cryptographic Accelerator)           │
   └──────────────────────────────────────────────┘
   
   ┌──────────────────────────────────────────────┐
   │           Connectivity Peripherals            │
   │  - 2x Gigabit Ethernet (EQOS)                 │
   │  - USB 2.0 Host/Device                        │
   │  - PCIe Gen3 x1                               │
   │  - 2x FlexCAN                                 │
   │  - SDIO 3.0                                   │
   └──────────────────────────────────────────────┘

**Hardware Bring-Up Sequence:**

.. code-block:: c

   // Step 1: Clock Tree Configuration
   // arch/arm64/boot/dts/freescale/imx93.dtsi
   
   clocks {
       osc_24m: clock-osc-24m {
           compatible = "fixed-clock";
           #clock-cells = <0>;
           clock-frequency = <24000000>;
           clock-output-names = "osc_24m";
       };
   };
   
   &clk {
       assigned-clocks = <&clk IMX93_CLK_A55_SEL>,
                        <&clk IMX93_CLK_A55_CORE>;
       assigned-clock-parents = <&clk IMX93_CLK_ARM_PLL>;
       assigned-clock-rates = <0>, <1700000000>;
   };
   
   // Step 2: Power Domain Configuration
   pgc {
       compatible = "fsl,imx93-gpc";
       reg = <0x44470000 0x10000>;
       
       pgc_m33: power-domain@0 {
           #power-domain-cells = <0>;
           reg = <IMX93_POWER_DOMAIN_M33>;
           clocks = <&clk IMX93_CLK_M33>;
       };
       
       pgc_usb: power-domain@4 {
           #power-domain-cells = <0>;
           reg = <IMX93_POWER_DOMAIN_USB>;
       };
   };
   
   // Step 3: Pin Muxing
   iomuxc: pinctrl@443c0000 {
       compatible = "fsl,imx93-iomuxc";
       reg = <0x443c0000 0x10000>;
       
       pinctrl_uart1: uart1grp {
           fsl,pins = <
               MX93_PAD_UART1_RXD__LPUART1_RX  0x31e
               MX93_PAD_UART1_TXD__LPUART1_TX  0x31e
           >;
       };
       
       pinctrl_eqos: eqosgrp {
           fsl,pins = <
               MX93_PAD_ENET1_MDC__ENET_QOS_MDC        0x51e
               MX93_PAD_ENET1_MDIO__ENET_QOS_MDIO      0x51e
               MX93_PAD_ENET1_RD0__ENET_QOS_RGMII_RD0  0x91e
               MX93_PAD_ENET1_RD1__ENET_QOS_RGMII_RD1  0x91e
               // ... more pins
           >;
       };
   };

**BSP Development:**

.. code-block:: bash

   # Yocto layer structure for i.MX 93
   meta-smart-home/
   ├── conf/
   │   ├── layer.conf
   │   └── machine/
   │       └── imx93-smart-home.conf
   ├── recipes-bsp/
   │   ├── u-boot/
   │   │   ├── u-boot-imx_%.bbappend
   │   │   └── files/
   │   │       ├── 0001-Add-smart-home-board-support.patch
   │   │       └── imx93-smart-home.dts
   │   └── imx-mkimage/
   │       └── imx-boot_%.bbappend
   ├── recipes-kernel/
   │   └── linux/
   │       ├── linux-imx_%.bbappend
   │       └── files/
   │           ├── defconfig
   │           └── 0001-Add-custom-drivers.patch
   └── recipes-core/
       └── images/
           └── smart-home-image.bb

**Machine Configuration:**

.. code-block:: bash

   # conf/machine/imx93-smart-home.conf
   
   require conf/machine/include/imx-base.inc
   require conf/machine/include/arm/armv8-2a/tune-cortexa55.inc
   
   MACHINE_FEATURES += "wifi bluetooth zigbee pci usbhost"
   
   KERNEL_DEVICETREE = " \
       freescale/imx93-smart-home.dtb \
       freescale/imx93-smart-home-m33.dtb \
   "
   
   IMAGE_BOOT_FILES = " \
       ${KERNEL_IMAGETYPE} \
       ${KERNEL_DEVICETREE} \
       imx-boot \
   "
   
   # Cortex-M33 firmware
   MACHINE_FIRMWARE = "imx93-m33-sensor-fusion.elf"
   
   UBOOT_CONFIG = "sd"
   UBOOT_CONFIG[sd] = "imx93_smart_home_defconfig,sdcard"
   
   IMX_BOOT_SEEK = "32"
   
   # Security features
   IMXBOOT_TARGETS = "flash_spl_flexspi"
   UBOOT_SIGN_ENABLE = "1"
   
   WKS_FILE = "imx-uboot-bootpart.wks.in"

**Heterogeneous Processing Implementation:**

.. code-block:: c

   // Linux side: RemoteProc driver for M33
   // drivers/remoteproc/imx_rproc.c
   
   static const struct imx_rproc_dcfg imx_rproc_cfg_imx93 = {
       .src_reg    = IMX93_SRC_M33_RCR,
       .src_mask   = SRC_M33_ENABLE,
       .src_start  = SRC_M33_ENABLE,
       .src_stop   = 0,
       .att_size   = ARRAY_SIZE(imx_rproc_att_imx93),
   };
   
   static int imx_rproc_probe(struct platform_device *pdev)
   {
       struct device *dev = &pdev->dev;
       struct device_node *np = dev->of_node;
       struct imx_rproc *priv;
       struct rproc *rproc;
       const struct imx_rproc_dcfg *dcfg;
       int ret;
       
       dcfg = of_device_get_match_data(dev);
       if (!dcfg)
           return -EINVAL;
       
       rproc = rproc_alloc(dev, "imx-rproc", &imx_rproc_ops,
                          NULL, sizeof(*priv));
       if (!rproc)
           return -ENOMEM;
       
       priv = rproc->priv;
       priv->dcfg = dcfg;
       
       // Map M33 TCM memory
       priv->mem = devm_ioremap_wc(dev, IMX93_M33_TCM_BASE,
                                   IMX93_M33_TCM_SIZE);
       
       // Setup mailbox for communication
       priv->tx_ch = mbox_request_channel_byname(&priv->client, "tx");
       priv->rx_ch = mbox_request_channel_byname(&priv->client, "rx");
       
       ret = rproc_add(rproc);
       if (ret) {
           rproc_free(rproc);
           return ret;
       }
       
       return 0;
   }
   
   // Application layer: Start M33 firmware
   int start_m33_firmware(const char *fw_name)
   {
       int fd;
       
       // Load firmware via sysfs
       fd = open("/sys/class/remoteproc/remoteproc0/firmware", O_WRONLY);
       write(fd, fw_name, strlen(fw_name));
       close(fd);
       
       // Start M33
       fd = open("/sys/class/remoteproc/remoteproc0/state", O_WRONLY);
       write(fd, "start", 5);
       close(fd);
       
       return 0;
   }

**M33 Firmware (FreeRTOS):**

.. code-block:: c

   // M33 side: Sensor fusion application
   #include "FreeRTOS.h"
   #include "task.h"
   #include "rpmsg_lite.h"
   
   #define RPMSG_SHMEM_BASE  0xA4300000
   #define SENSOR_TASK_PRIORITY  (configMAX_PRIORITIES - 1)
   
   // Sensor data structure
   typedef struct {
       uint32_t timestamp;
       float accel[3];
       float gyro[3];
       float mag[3];
   } sensor_data_t;
   
   // High-frequency sensor processing (1kHz)
   void sensor_fusion_task(void *param)
   {
       sensor_data_t sensor_data;
       TickType_t last_wake = xTaskGetTickCount();
       
       while (1) {
           // Read from I2C sensors (IMU, magnetometer)
           read_imu_data(&sensor_data.accel, &sensor_data.gyro);
           read_magnetometer(&sensor_data.mag);
           
           // Sensor fusion algorithm (Kalman filter)
           quaternion_t orientation = fusion_update(&sensor_data);
           
           // Send to A55 via RPMsg (if requested)
           if (a55_requests_data) {
               rpmsg_lite_send(rpmsg_instance, ept, RPMSG_ADDR_ANY,
                              &orientation, sizeof(orientation), 0);
           }
           
           // 1ms period
           vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(1));
       }
   }
   
   // RPMsg communication handler
   int32_t rpmsg_callback(void *payload, uint32_t payload_len,
                         uint32_t src, void *priv)
   {
       // Handle commands from Linux
       uint32_t cmd = *(uint32_t *)payload;
       
       switch (cmd) {
       case CMD_START_STREAMING:
           a55_requests_data = true;
           break;
       case CMD_STOP_STREAMING:
           a55_requests_data = false;
           break;
       case CMD_CALIBRATE:
           calibrate_sensors();
           break;
       }
       
       return RL_RELEASE;
   }

**Performance Optimization:**

.. code-block:: c

   // Cache management for shared memory
   #include <linux/dma-mapping.h>
   
   // Allocate coherent shared memory (uncached)
   struct shared_data *shm = dma_alloc_coherent(dev, PAGE_SIZE,
                                                &phys_addr, GFP_KERNEL);
   
   // For cached regions, explicit cache operations
   void update_shared_buffer(void *buf, size_t len)
   {
       // Write data
       memcpy(buf, data, len);
       
       // Clean cache to ensure M33 sees updated data
       dma_sync_single_for_device(dev, phys_addr, len, DMA_TO_DEVICE);
   }
   
   // M33 side: Cache configuration
   // Enable cache for performance
   SCB_EnableICache();
   SCB_EnableDCache();
   
   // Mark shared memory region as non-cacheable in MPU
   MPU->RBAR = (RPMSG_SHMEM_BASE & MPU_RBAR_ADDR_Msk) | 
               MPU_RBAR_VALID_Msk | 0;  // Region 0
   MPU->RASR = (MPU_RASR_XN_Msk) |       // Execute Never
               (0x3 << MPU_RASR_TEX_Pos) | // Shareable Device
               (MPU_RASR_S_Msk) |
               (MPU_RASR_B_Msk) |
               (0x13 << MPU_RASR_SIZE_Pos) |  // 1MB
               MPU_RASR_ENABLE_Msk;

i.MX 6 Series
-------------

**Key Differences from i.MX 93:**

.. code-block:: text

   i.MX 6 Variants:
   ┌────────────────┬──────────┬─────────┬──────────┐
   │ Variant        │ Cores    │ Clock   │ Use Case │
   ├────────────────┼──────────┼─────────┼──────────┤
   │ i.MX 6Solo     │ 1x A9    │ 1.0 GHz │ Low Cost │
   │ i.MX 6DualLite │ 2x A9    │ 1.0 GHz │ Mid-Range│
   │ i.MX 6Quad     │ 4x A9    │ 1.2 GHz │ High Perf│
   │ i.MX 6QuadPlus │ 4x A9    │ 1.2 GHz │ + PRE/PRG│
   └────────────────┴──────────┴─────────┴──────────┘

**Board Bring-Up Checklist:**

.. code-block:: bash

   # 1. Boot from SD card (development)
   # Set boot mode DIP switches: 00 for SD
   
   # 2. Test basic peripherals
   # UART
   echo "Hello from i.MX6" > /dev/ttymxc0
   
   # I2C scan
   i2cdetect -y 1
   
   # Ethernet
   ifconfig eth0 192.168.1.100
   ping 192.168.1.1
   
   # 3. Display test (IPU)
   echo 0 > /sys/class/graphics/fb0/blank
   cat /dev/urandom > /dev/fb0
   
   # 4. GPU test
   glmark2-es2-drm
   
   # 5. VPU test (video decode)
   gst-launch-1.0 filesrc location=test.mp4 ! \
       qtdemux ! h264parse ! vpudec ! autovideosink

TI DaVinci Platform (DM365, ARM9)
=================================

**Project: Thermal Imaging System (FLIR)**

Platform Architecture
---------------------

.. code-block:: text

   DM365 SOC Architecture:
   
   ┌──────────────────────────────────────┐
   │  ARM926EJ-S @ 300MHz                 │
   │  - 16KB I-Cache, 8KB D-Cache         │
   │  - MMU for Linux                     │
   └──────────────────────────────────────┘
   
   ┌──────────────────────────────────────┐
   │  Video/Image Coprocessors            │
   │  ┌──────────────────────────────┐    │
   │  │ VPSS (Video Processing)      │    │
   │  │ - Preview Engine             │    │
   │  │ - Resizer                    │    │
   │  │ - H.264/MPEG4 Encoder        │    │
   │  │ - JPEG Codec                 │    │
   │  └──────────────────────────────┘    │
   └──────────────────────────────────────┘
   
   ┌──────────────────────────────────────┐
   │  Peripherals                         │
   │  - VPFE (Video Front End)            │
   │  - EMAC (10/100 Ethernet)            │
   │  - USB 2.0 OTG                       │
   │  - MMC/SD Host                       │
   │  - I2C, SPI, UART                    │
   └──────────────────────────────────────┘

**Boot Sequence:**

.. code-block:: text

   ROM Boot → UBL (User Boot Loader) → U-Boot → Linux
   
   NAND Flash Layout:
   0x0000_0000 - 0x0002_0000: UBL (128KB)
   0x0002_0000 - 0x0010_0000: U-Boot (896KB)
   0x0010_0000 - 0x0050_0000: Kernel (4MB)
   0x0050_0000 - 0x0450_0000: RootFS (64MB)
   0x0450_0000 - end:        Data Partition

**U-Boot Customization:**

.. code-block:: c

   // board/ti/dm365/dm365.c
   
   int board_init(void)
   {
       // NAND timing for faster boot
       davinci_configure_pin_mux(nand_pins, ARRAY_SIZE(nand_pins));
       
       // Custom GPIOs for thermal camera control
       gpio_request(GPIO_CAMERA_POWER, "camera_pwr");
       gpio_direction_output(GPIO_CAMERA_POWER, 1);
       
       gpio_request(GPIO_CAMERA_RESET, "camera_rst");
       gpio_direction_output(GPIO_CAMERA_RESET, 0);
       udelay(100);
       gpio_set_value(GPIO_CAMERA_RESET, 1);
       
       return 0;
   }
   
   // Custom commands for DFM
   static int do_thermal_test(cmd_tbl_t *cmdtp, int flag,
                             int argc, char * const argv[])
   {
       printf("Testing thermal camera interface...\n");
       
       // Test I2C communication
       if (i2c_probe(THERMAL_CAMERA_I2C_ADDR)) {
           printf("ERROR: Camera not detected\n");
           return 1;
       }
       
       // Test video interface
       if (test_vpfe_capture()) {
           printf("ERROR: Video capture failed\n");
           return 1;
       }
       
       printf("Thermal camera: OK\n");
       return 0;
   }
   
   U_BOOT_CMD(thermal_test, 1, 0, do_thermal_test,
              "Test thermal imaging system",
              "Run complete thermal camera test");

**NAND Flash Driver with BBT:**

.. code-block:: c

   // drivers/mtd/nand/davinci_nand.c
   
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
   
   static int davinci_nand_probe(struct platform_device *pdev)
   {
       struct davinci_nand_info *info;
       struct nand_chip *nand;
       
       // ... initialization ...
       
       // Configure BBT
       nand->bbt_options = NAND_BBT_USE_FLASH | NAND_BBT_NO_OOB;
       nand->bbt_td = &davinci_bbt_main_descr;
       nand->bbt_md = &davinci_bbt_mirror_descr;
       
       // ECC configuration for better reliability
       nand->ecc.mode = NAND_ECC_HW;
       nand->ecc.size = 512;
       nand->ecc.bytes = 10;  // 4-bit ECC
       nand->ecc.strength = 4;
       
       // Scan for bad blocks
       ret = nand_scan_ident(mtd, 1, NULL);
       ret = nand_scan_tail(mtd);
       
       return 0;
   }

**Video Capture Driver (V4L2):**

.. code-block:: c

   // drivers/media/platform/davinci/vpfe_capture.c
   
   // Custom thermal camera interface
   static int thermal_camera_init(struct vpfe_device *vpfe_dev)
   {
       struct vpfe_config *cfg = vpfe_dev->cfg;
       
       // Configure VPFE for raw thermal data
       regw(vpfe_dev, 0, VPFE_PCR);  // Disable progressive/interlaced
       
       // Input format: 16-bit raw
       regw(vpfe_dev, VPFE_RAW_INPUT | VPFE_DATA_WIDTH_16BIT,
            VPFE_SYNMODE);
       
       // Configure H/V sync
       regw(vpfe_dev, cfg->hdw | (cfg->hd << 16), VPFE_HDW);
       regw(vpfe_dev, cfg->vdw | (cfg->vd << 16), VPFE_VDW);
       
       // Setup DMA for image capture
       vpfe_config_dma(vpfe_dev);
       
       return 0;
   }
   
   // Application layer: Capture thermal frame
   int capture_thermal_frame(int fd, void *buffer, size_t size)
   {
       struct v4l2_buffer buf;
       
       memset(&buf, 0, sizeof(buf));
       buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
       buf.memory = V4L2_MEMORY_MMAP;
       
       // Dequeue filled buffer
       if (ioctl(fd, VIDIOC_DQBUF, &buf) < 0) {
           perror("VIDIOC_DQBUF");
           return -1;
       }
       
       // Process thermal data
       memcpy(buffer, mmap_buffers[buf.index].start, size);
       
       // Requeue buffer
       if (ioctl(fd, VIDIOC_QBUF, &buf) < 0) {
           perror("VIDIOC_QBUF");
           return -1;
       }
       
       return 0;
   }

**Video Encoding (H.264/MPEG4):**

.. code-block:: c

   // Using TI DSP/Video SDK
   #include <ti/sdo/codecs/h264enc/ih264venc.h>
   
   typedef struct {
       VIDENC2_Handle handle;
       XDAS_Int32 width;
       XDAS_Int32 height;
       XDAS_Int32 bitrate;
   } H264Encoder;
   
   int h264_encoder_init(H264Encoder *enc, int width, int height)
   {
       VIDENC2_Params params;
       VIDENC2_DynamicParams dyn_params;
       
       // Set encoding parameters
       params.size = sizeof(VIDENC2_Params);
       params.maxWidth = width;
       params.maxHeight = height;
       params.maxFrameRate = 30000;  // 30 fps
       params.maxBitRate = 2000000;  // 2 Mbps
       params.dataEndianness = XDM_BYTE;
       params.profile = IH264VENC_BASELINE_PROFILE;
       params.level = IH264VENC_LEVEL_30;
       
       // Create encoder instance
       enc->handle = VIDENC2_create(Engine_getEngine("encode"),
                                    "h264enc", &params);
       
       // Set dynamic parameters
       dyn_params.size = sizeof(VIDENC2_DynamicParams);
       dyn_params.targetBitRate = 2000000;
       dyn_params.inputWidth = width;
       dyn_params.inputHeight = height;
       dyn_params.frameRate = 30000;
       dyn_params.intraFrameInterval = 30;
       
       VIDENC2_control(enc->handle, XDM_SETPARAMS,
                      &dyn_params, &status);
       
       return 0;
   }
   
   int h264_encode_frame(H264Encoder *enc, uint8_t *in_buf,
                        uint8_t *out_buf, size_t *out_size)
   {
       VIDENC2_InArgs in_args;
       VIDENC2_OutArgs out_args;
       XDM2_BufDesc in_buf_desc;
       XDM2_BufDesc out_buf_desc;
       
       // Setup input buffer
       in_buf_desc.numBufs = 1;
       in_buf_desc.descs[0].buf = in_buf;
       in_buf_desc.descs[0].bufSize = enc->width * enc->height * 2;
       
       // Setup output buffer
       out_buf_desc.numBufs = 1;
       out_buf_desc.descs[0].buf = out_buf;
       out_buf_desc.descs[0].bufSize = 1024 * 1024;  // 1MB max
       
       // Encode
       in_args.size = sizeof(VIDENC2_InArgs);
       in_args.inputID = 1;
       
       int ret = VIDENC2_process(enc->handle, &in_buf_desc,
                                &out_buf_desc, &in_args, &out_args);
       
       if (ret == VIDENC2_EOK) {
           *out_size = out_args.bytesGenerated;
           return 0;
       }
       
       return -1;
   }

**Power Management (Hibernation <8mW):**

.. code-block:: c

   // arch/arm/mach-davinci/pm.c
   
   #define RTC_SRAM_BASE  0x01C23000
   #define HIBERNATE_MAGIC  0xDEADBEEF
   
   struct davinci_hibernate_context {
       uint32_t magic;
       void (*resume_fn)(void);
       uint32_t arm_regs[16];
       uint32_t cp15_regs[10];
       uint32_t ddr_config[20];
   } __attribute__((packed));
   
   static int davinci_pm_enter_hibernate(void)
   {
       struct davinci_hibernate_context *ctx =
           (struct davinci_hibernate_context *)RTC_SRAM_BASE;
       
       // Save context to battery-backed RTC SRAM
       ctx->magic = HIBERNATE_MAGIC;
       ctx->resume_fn = virt_to_phys(davinci_cpu_resume);
       
       // Save CPU registers
       asm volatile(
           "stmia %0, {r0-r15}\n"
           : : "r" (ctx->arm_regs)
       );
       
       // Save CP15 registers
       ctx->cp15_regs[0] = read_sctlr();
       ctx->cp15_regs[1] = read_ttbr0();
       ctx->cp15_regs[2] = read_ttbr1();
       ctx->cp15_regs[3] = read_dacr();
       
       // Save DDR configuration
       save_ddr_config(ctx->ddr_config);
       
       // Power down peripherals
       davinci_psc_config(DAVINCI_LPSC_USB, 0, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_EMAC, 0, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_VPSS, 0, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_HPI, 0, PSC_SWRSTDISABLE);
       
       // Enter deep sleep
       cpu_suspend(0, davinci_finish_suspend);
       
       // Execution resumes here after wakeup
       return 0;
   }
   
   // Resume path
   static void davinci_cpu_resume(void)
   {
       struct davinci_hibernate_context *ctx =
           (struct davinci_hibernate_context *)RTC_SRAM_BASE;
       
       // Restore DDR
       restore_ddr_config(ctx->ddr_config);
       
       // Restore CP15
       write_sctlr(ctx->cp15_regs[0]);
       write_ttbr0(ctx->cp15_regs[1]);
       write_ttbr1(ctx->cp15_regs[2]);
       write_dacr(ctx->cp15_regs[3]);
       
       // Invalidate caches
       v7_invalidate_l1();
       
       // Power up peripherals
       davinci_psc_config(DAVINCI_LPSC_USB, 1, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_EMAC, 1, PSC_SWRSTDISABLE);
       
       // Resume kernel
       cpu_resume();
   }

Intel Atom C3xxx Platform (x86_64)
==================================

**Project: Avionics Embedded Platform (Rockwell Collins)**

Platform Architecture
---------------------

.. code-block:: text

   Intel Atom C3xxx (Denverton):
   
   ┌─────────────────────────────────────────┐
   │  Atom C3xxx Cores                       │
   │  - Up to 16 cores @ 2.0-2.2 GHz         │
   │  - Out-of-order execution               │
   │  - AVX2, AES-NI instructions            │
   └─────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────┐
   │  Platform Features                      │
   │  - ECC DDR4 (up to 128GB)              │
   │  - Intel QuickAssist (crypto/compress)  │
   │  - 32 PCIe 3.0 lanes                   │
   │  - 12x SATA 3.0                        │
   │  - Quad 10GbE MACs                     │
   └─────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────┐
   │  Security                               │
   │  - Intel Boot Guard                    │
   │  - TXT (Trusted Execution Technology)  │
   │  - SGX (Software Guard Extensions)     │
   └─────────────────────────────────────────┘

**UEFI Firmware Customization:**

.. code-block:: c

   // Platform/Intel/DenvertonBoardPkg/Library/PlatformHookLib/
   
   EFI_STATUS
   EFIAPI
   PlatformHookSerialPortInitialize(VOID)
   {
       // Configure SuperIO for COM ports
       IoWrite8(SUPERIO_CONFIG_PORT, SUPERIO_UNLOCK);
       
       // Select COM1
       IoWrite8(SUPERIO_CONFIG_PORT, 0x07);
       IoWrite8(SUPERIO_DATA_PORT, 0x01);
       
       // Set base address (0x3F8)
       IoWrite8(SUPERIO_CONFIG_PORT, 0x60);
       IoWrite8(SUPERIO_DATA_PORT, 0x03);
       IoWrite8(SUPERIO_CONFIG_PORT, 0x61);
       IoWrite8(SUPERIO_DATA_PORT, 0xF8);
       
       // Enable device
       IoWrite8(SUPERIO_CONFIG_PORT, 0x30);
       IoWrite8(SUPERIO_DATA_PORT, 0x01);
       
       IoWrite8(SUPERIO_CONFIG_PORT, SUPERIO_LOCK);
       
       return EFI_SUCCESS;
   }
   
   // Custom platform init DXE driver
   EFI_STATUS
   EFIAPI
   AvionicsPlatformInit(
       IN EFI_HANDLE        ImageHandle,
       IN EFI_SYSTEM_TABLE  *SystemTable
   )
   {
       EFI_STATUS Status;
       
       // Initialize FPGA
       Status = InitializeFpgaInterface();
       if (EFI_ERROR(Status)) {
           DEBUG((EFI_D_ERROR, "FPGA init failed: %r\n", Status));
           return Status;
       }
       
       // Configure multiple PCIe root complexes
       Status = ConfigureRootComplexes();
       
       // Setup wireless card power
       GpioSetOutputValue(GPIO_WIRELESS_POWER, TRUE);
       MicroSecondDelay(100000);  // 100ms power-on delay
       
       // Configure Ethernet switches
       Status = ConfigureEthernetSwitch();
       
       return EFI_SUCCESS;
   }

**Buildroot Configuration:**

.. code-block:: bash

   # configs/avionics_atom_defconfig
   
   BR2_x86_64=y
   BR2_x86_corei7=y
   
   # Toolchain
   BR2_TOOLCHAIN_BUILDROOT_GLIBC=y
   BR2_GCC_VERSION_10_X=y
   BR2_TOOLCHAIN_BUILDROOT_CXX=y
   
   # Kernel
   BR2_LINUX_KERNEL=y
   BR2_LINUX_KERNEL_CUSTOM_VERSION=y
   BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE="5.10.120"
   BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y
   BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="board/avionics/kernel.config"
   BR2_LINUX_KERNEL_NEEDS_HOST_OPENSSL=y
   
   # UEFI boot
   BR2_TARGET_GRUB2=y
   BR2_TARGET_GRUB2_X86_64_EFI=y
   
   # Security
   BR2_PACKAGE_LIBSELINUX=y
   BR2_PACKAGE_REFPOLICY=y
   BR2_PACKAGE_CRYPTSETUP=y
   
   # Monolithic image
   BR2_TARGET_ROOTFS_SQUASHFS=y
   BR2_TARGET_ROOTFS_SQUASHFS_XZ=y
   
   # Custom packages
   BR2_PACKAGE_AVIONICS_APP=y
   BR2_PACKAGE_FPGA_FIRMWARE=y

**Custom Kernel Drivers:**

.. code-block:: c

   // drivers/fpga/avionics_fpga.c
   
   static int avionics_fpga_probe(struct pci_dev *pdev,
                                  const struct pci_device_id *id)
   {
       struct avionics_fpga *fpga;
       int ret;
       
       fpga = devm_kzalloc(&pdev->dev, sizeof(*fpga), GFP_KERNEL);
       if (!fpga)
           return -ENOMEM;
       
       // Enable PCI device
       ret = pci_enable_device(pdev);
       if (ret)
           return ret;
       
       // Request memory regions
       ret = pci_request_regions(pdev, "avionics-fpga");
       if (ret)
           goto err_disable_device;
       
       // Map FPGA registers
       fpga->regs = pci_ioremap_bar(pdev, 0);
       if (!fpga->regs) {
           ret = -ENOMEM;
           goto err_release_regions;
       }
       
       // Check FPGA version
       u32 version = ioread32(fpga->regs + FPGA_VERSION_REG);
       dev_info(&pdev->dev, "FPGA version: %d.%d\n",
                (version >> 16) & 0xFF, version & 0xFF);
       
       // Setup interrupts
       ret = pci_alloc_irq_vectors(pdev, 1, 4, PCI_IRQ_MSI);
       if (ret < 0)
           goto err_unmap;
       
       ret = request_irq(pci_irq_vector(pdev, 0),
                        avionics_fpga_irq_handler,
                        0, "avionics-fpga", fpga);
       
       // Create char device for userspace access
       fpga->miscdev.minor = MISC_DYNAMIC_MINOR;
       fpga->miscdev.name = "avionics_fpga";
       fpga->miscdev.fops = &avionics_fpga_fops;
       
       ret = misc_register(&fpga->miscdev);
       
       pci_set_drvdata(pdev, fpga);
       
       return 0;
       
   err_unmap:
       iounmap(fpga->regs);
   err_release_regions:
       pci_release_regions(pdev);
   err_disable_device:
       pci_disable_device(pdev);
       return ret;
   }

**PCIe Multiple Root Complex Support:**

.. code-block:: c

   // drivers/pci/controller/pci-atom-c3xxx.c
   
   struct atom_pcie_rc {
       void __iomem *regs;
       int rc_id;  // Root Complex 0-3
       struct pci_host_bridge *bridge;
   };
   
   static int atom_pcie_probe(struct platform_device *pdev)
   {
       struct atom_pcie_rc *rc;
       struct pci_host_bridge *bridge;
       struct resource *res;
       int ret;
       
       bridge = devm_pci_alloc_host_bridge(&pdev->dev, sizeof(*rc));
       if (!bridge)
           return -ENOMEM;
       
       rc = pci_host_bridge_priv(bridge);
       
       // Get RC ID from device tree
       of_property_read_u32(pdev->dev.of_node, "rc-id", &rc->rc_id);
       
       // Map registers
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       rc->regs = devm_ioremap_resource(&pdev->dev, res);
       
       // Configure RC-specific settings
       writel(PCIE_RC_MODE | (rc->rc_id << 8),
              rc->regs + PCIE_CTRL_REG);
       
       // Setup bus range
       bridge->busnr = rc->rc_id * 64;  // Each RC gets 64 buses
       bridge->dev.parent = &pdev->dev;
       bridge->sysdata = rc;
       bridge->ops = &atom_pcie_ops;
       
       // Scan bus
       ret = pci_scan_root_bus_bridge(bridge);
       if (ret)
           return ret;
       
       pci_bus_add_devices(bridge->bus);
       
       return 0;
   }
   
   // Custom ops to identify RC for each access
   static int atom_pcie_read_config(struct pci_bus *bus, unsigned int devfn,
                                   int where, int size, u32 *val)
   {
       struct atom_pcie_rc *rc = bus->sysdata;
       void __iomem *addr;
       
       // Calculate config space address based on RC ID
       addr = rc->regs + PCIE_CFG_BASE +
              (bus->number << 20) + (devfn << 12) + where;
       
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

Multi-SOC Platform Comparison
==============================

.. list-table:: SOC Platform Comparison Matrix
   :header-rows: 1
   :widths: 15 20 20 20 25
   
   * - Feature
     - i.MX 93
     - TI DaVinci
     - Intel Atom C3xxx
     - Notes
   * - CPU Architecture
     - Cortex-A55 + M33
     - ARM926EJ-S
     - x86_64
     - Heterogeneous vs homogeneous
   * - Clock Speed
     - 1.7 GHz / 250 MHz
     - 300 MHz
     - 2.0-2.2 GHz
     - x86 highest throughput
   * - Boot Time
     - 1.8s (optimized)
     - 5.8s
     - 9.2s
     - UEFI adds overhead
   * - Power (Active)
     - 2-3W
     - 1.5W
     - 15-25W
     - ARM most efficient
   * - Power (Sleep)
     - <10mW
     - <8mW
     - ~500mW
     - DaVinci best hibernation
   * - Real-Time
     - M33 + RTOS
     - Soft RT Linux
     - Preempt-RT Linux
     - Dedicated RT core best
   * - Security
     - HAB, TrustZone
     - Limited
     - Boot Guard, SGX
     - x86 most features
   * - Video Encode
     - H.264/5 hardware
     - H.264 DSP
     - Software only
     - Dedicated codec best
   * - Development
     - Yocto/Buildroot
     - Legacy tools
     - Standard Linux
     - x86 easiest
   * - Cost
     - $15-25
     - $8-12
     - $50-150
     - DaVinci lowest
   * - Use Case
     - IoT, Smart Home
     - Imaging, Camera
     - Server, Networking
     - Domain-specific

Best Practices
==============

Platform Selection Criteria
----------------------------

1. **Performance Requirements**
   - Determine compute needs (MIPS/DMIPS)
   - Identify real-time constraints
   - Consider accelerators (GPU, VPU, DSP)

2. **Power Budget**
   - Active power consumption
   - Sleep/hibernate requirements
   - Battery vs mains powered

3. **Connectivity**
   - Required interfaces (USB, Ethernet, PCIe, etc.)
   - Wireless needs (Wi-Fi, BT, cellular)
   - Industrial protocols (CAN, Profibus, etc.)

4. **Software Ecosystem**
   - Vendor BSP support
   - Community activity
   - Long-term availability

5. **Security Requirements**
   - Secure boot capabilities
   - Cryptographic accelerators
   - Security certifications

Development Workflow
--------------------

.. code-block:: text

   Phase 1: Hardware Bring-Up
   ├── Boot ROM verification
   ├── Bootloader porting
   ├── Basic peripheral test (UART, I2C)
   └── DDR calibration
   
   Phase 2: Kernel Enablement
   ├── Device tree creation
   ├── Core driver porting
   ├── Filesystem mounting
   └── Shell access
   
   Phase 3: Peripheral Integration
   ├── Network stack
   ├── Storage devices
   ├── USB subsystem
   └── Custom hardware drivers
   
   Phase 4: Application Layer
   ├── Init system configuration
   ├── Application framework
   ├── Security hardening
   └── OTA update mechanism
   
   Phase 5: Optimization
   ├── Boot time reduction
   ├── Power optimization
   ├── Performance tuning
   └── Memory footprint reduction

Common Pitfalls and Solutions
------------------------------

1. **Device Tree Mismatches**
   - Always validate compatible strings
   - Use correct reg addresses
   - Enable required clocks/power domains

2. **Memory Configuration**
   - DDR timing critical for stability
   - Reserve memory for coprocessors
   - Configure MMU/MPU correctly

3. **Clock Dependencies**
   - Parent-child clock relationships
   - Enable clocks before access
   - Gate unused clocks for power

4. **Interrupt Configuration**
   - GIC/NVIC setup
   - IRQ priorities for RT
   - Shared interrupts

5. **Cache Coherency**
   - DMA buffer alignment
   - Explicit cache operations
   - Non-cacheable regions for shared memory

Tools and Debugging
-------------------

**Hardware Debug:**

.. code-block:: bash
   
   # JTAG/SWD connections
   openocd -f interface/jlink.cfg -f target/imx93.cfg
   
   # Memory dump
   openocd> mdw 0x80000000 256
   
   # Reset and halt
   openocd> reset halt
   openocd> reg
   
   # Load and run
   openocd> load_image u-boot-spl.bin 0x2020_0000
   openocd> resume 0x2020_0000

**Software Debug:**

.. code-block:: bash
   
   # Kernel debugging
   CONFIG_DEBUG_INFO=y
   CONFIG_GDB_SCRIPTS=y
   
   # GDB with kernel
   gdb vmlinux
   (gdb) target remote :1234
   (gdb) lx-dmesg
   
   # ftrace
   echo function > /sys/kernel/debug/tracing/current_tracer
   cat /sys/kernel/debug/tracing/trace

References
==========

- NXP i.MX 93 Reference Manual
- TI DaVinci DM365 Technical Reference Manual
- Intel Atom C3xxx Datasheet
- ARM Cortex-A55/M33 Technical Reference Manuals
- Linux Device Driver Development (LDD3)
- Yocto Project Documentation
- Buildroot User Manual

