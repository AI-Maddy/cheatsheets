**cheatsheet for Linux kernel-level image processing** with a strong focus on **ADAS (Advanced Driver Assistance Systems)** use cases (2025–2026 perspective).

Covers the most relevant kernel subsystems, drivers, APIs, and patterns used in automotive vision pipelines (cameras → ISP → object detection / lane keeping / fusion).

### 1. Kernel Subsystems & Frameworks (ADAS-Relevant)

| Subsystem / Framework          | Main Location                          | ADAS Use Case / Strength                              | Typical SoC / Vendor Support (2026) |
|--------------------------------|----------------------------------------|-------------------------------------------------------|-------------------------------------|
| **V4L2** (Video4Linux2)        | `drivers/media/v4l2-core/`             | Raw Bayer capture, ISP control, multi-stream          | Almost universal                    |
| **Media Controller**           | `drivers/media/mc/`                    | Complex pipeline routing (sensor ↔ ISP blocks)        | Qualcomm, TI, NXP, Rockchip, Intel IPU6 |
| **libcamera kernel parts**     | `drivers/media/platform/` + V4L2       | Modern sensor/ISP abstraction (upstream trend)        | Raspberry Pi, Intel IPU6, Qualcomm CAMSS |
| **Video Buffer 2 (vb2)**       | `drivers/media/vb2-core/`              | Buffer management (DMA-BUF, MMAP, USERPTR)            | All V4L2 drivers                    |
| **DMA-BUF**                    | `drivers/dma-buf/`                     | Zero-copy sharing → GPU / NPU / DSP                   | Critical for ADAS fusion            |
| **V4L2 Request API**           | `drivers/media/v4l2-core/v4l2-request.c` | Atomic ISP config + capture (per-frame control)     | Modern ADAS pipelines               |
| **V4L2 subdev**                | `include/media/v4l2-subdev.h`          | Sensor, lens, ISP blocks as separate entities         | Standard for complex SoC ISPs       |
| **DRM / KMS**                  | `drivers/gpu/drm/`                     | Display output + GPU compute (if needed)              | Tegra, AMD, Intel (less common)     |

### 2. Typical ADAS Camera → Processing Pipeline (Kernel View)

```
MIPI CSI-2 / GMSL2 → Sensor (raw Bayer 12/14-bit)
          ↓
     SoC CSI-2 receiver (V4L2 subdev)
          ↓
     Hardware ISP blocks (debayer, 3A stats, LSC, DPC, NR, sharpening, tone mapping, gamma, color correction)
          ↓
     Statistics output (histogram, AWB regions, AF contrast) → V4L2 subdev stats node
          ↓
     Processed frames (YUV / RGB / Bayer) → /dev/videoX + DMA-BUF export
          ↓
     Userspace (or kernel module): CV / DNN (OpenCV / TensorFlow Lite / ONNX / custom NPU driver)
          ↓
     Fusion with radar / lidar / map → perception stack
```

### 3. Key Kernel Structures & APIs (ADAS Focus)

| Structure / API                        | Purpose / ADAS Relevance                              | Typical Usage in ADAS Driver |
|----------------------------------------|-------------------------------------------------------|-------------------------------|
| `struct v4l2_subdev`                   | Sensor / ISP block abstraction                        | `v4l2_subdev_call()` for set_fmt, s_ctrl |
| `struct v4l2_mbus_framefmt`            | Bus format negotiation (Bayer RGGB, YUV422, etc.)     | Sensor → ISP format routing   |
| `struct v4l2_ctrl`                     | Exposure, gain, VBLANK, HBLANK, test pattern          | 3A tuning from userspace      |
| `struct media_entity / pad / link`     | Pipeline graph (CSI → debayer → scaler → stats)       | `media_pipeline_start()`      |
| `struct v4l2_request`                  | Atomic configuration + queuing (Request API)          | Per-frame ISP params + capture |
| `vb2_queue` / `vb2_buffer`             | Buffer lifecycle (queue, dequeue, done)               | `vb2_ops` callbacks           |
| `dma_buf_export()` / `dma_buf_import()`| Zero-copy to GPU/NPU/DSP                              | Critical for low-latency fusion |
| `v4l2_subdev_get_format()` / `set_format()` | Format negotiation chain                        | Multi-stream support          |
| `v4l2_subdev_s_ctrl()`                 | Set exposure/gain/white-balance from kernel           | Fast closed-loop 3A           |

### 4. Important V4L2 Controls (ADAS 3A & Tuning)

| Control (V4L2_CID_*)          | Typical Range / Use in ADAS                           | Driver / ISP Block |
|-------------------------------|-------------------------------------------------------|--------------------|
| `V4L2_CID_EXPOSURE_AUTO`      | 0=manual, 1=auto                                      | AEC                |
| `V4L2_CID_EXPOSURE_ABSOLUTE`  | 1–10000 (lines or µs)                                 | AEC                |
| `V4L2_CID_ANALOGUE_GAIN`      | Sensor analog gain                                    | AGC                |
| `V4L2_CID_AUTO_WHITE_BALANCE` | 0=manual, 1=auto                                      | AWB                |
| `V4L2_CID_AUTO_N_PRESET_WHITE_BALANCE` | Preset modes (daylight, cloudy, etc.)          | AWB                |
| `V4L2_CID_AUTOFOCUS`          | Trigger continuous / single AF                        | AF                 |
| `V4L2_CID_TEST_PATTERN`       | Color bars / walking ones (debug/calibration)         | Sensor/ISP         |
| `V4L2_CID_LINK_FREQ`          | CSI-2 link frequency (MIPI clock)                     | CSI receiver       |
| `V4L2_CID_PIXEL_RATE`         | Pixel clock rate (for bandwidth calc)                 | Pipeline tuning    |

### 5. ADAS-Specific Kernel Patterns & Gotchas

| Pattern / Requirement          | Recommended Approach (2026)                          | Why Important in ADAS |
|--------------------------------|------------------------------------------------------|-----------------------|
| **Low-latency capture**        | `vb2_queue` + `DMA_FROM_DEVICE` + `request API`      | <5 ms end-to-end latency target |
| **Zero-copy to NPU/GPU**       | `dma_buf_export()` → import into TensorFlow Lite / ONNX | Avoid memcpy overhead |
| **Multi-camera sync**          | PTP / gPTP timestamp + V4L2 buffer timestamp         | Sensor fusion accuracy |
| **Multi-stream**               | Multiple `/dev/videoX` + Media Controller routing    | Preview + raw + scaled |
| **HDR / multi-exposure**       | Multiple exposures per frame (vendor-specific CCC)   | High dynamic range scenes |
| **ISP bypass / raw-only**      | `V4L2_PIX_FMT_SRGGB12` + userspace ISP               | Custom perception tuning |
| **Power / thermal management** | Runtime PM + `v4l2_subdev_s_power()`                 | Automotive thermal constraints |
| **Safety / ASIL-B/D**          | Lock-step cores, ECC RAM, ASIL-certified drivers     | ISO 26262 compliance |

### 6. Debugging & Inspection Tools (Kernel + Userspace)

```bash
# Show camera devices & capabilities
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext

# Media controller pipeline graph
media-ctl -p -d /dev/media0

# Query current format / controls
v4l2-ctl -d /dev/video0 --get-fmt-video
v4l2-ctl -d /dev/video0 --list-ctrls

# Capture raw Bayer frame
v4l2-ctl --stream-mmap --stream-count=1 --stream-to=frame.raw -d /dev/video0

# Trace media events (faults, queue, done)
echo 1 > /sys/kernel/debug/tracing/events/media/enable
cat /sys/kernel/debug/tracing/trace_pipe

# DMA-BUF stats (if exported)
cat /sys/kernel/debug/dma-buf/*

# Perf for ISP / DMA bottlenecks
perf record -e cycles -e instructions -p <camera-process>
perf record -e dma:* -p <camera-process>
```

### 7. Modern ADAS Kernel Trends (2026)

- **Request API** → almost mandatory for deterministic per-frame control
- **DMA-BUF everywhere** → GPU/NPU fusion without copy
- **libcamera kernel drivers** → upstreaming Qualcomm CAMSS, Intel IPU6, Rockchip ISP
- **V4L2 subdev async probing** → hot-plug GMSL cameras
- **zonal Ethernet + cameras** → higher bandwidth CSI-2 v3 / C-PHY
- **Safety-certified drivers** → growing (TI Jacinto, NXP S32V, Qualcomm SA8xxx)

This cheatsheet focuses on **kernel-level** image processing relevant to ADAS vision pipelines (raw capture → ISP → efficient delivery to perception stack).

Good luck with your ADAS camera bring-up or kernel driver work!