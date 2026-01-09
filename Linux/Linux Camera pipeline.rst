**cheatsheet for camera pipelines in Linux** (kernel + userspace frameworks, 2025–2026 perspective).

Focus: embedded & mobile SoCs (Qualcomm, MediaTek, Rockchip, NXP i.MX, TI, Raspberry Pi, Intel IPU6, etc.), automotive, drones, security cameras, industrial vision.

🐧 1. Main Camera Stacks in Linux (2024–2026)

| Framework / Stack       | Kernel Driver Type       | Userspace API              | Main Use Cases                          | Maturity / Adoption (2026) | Maintained by / Notes |
|--------------------------|---------------------------|-----------------------------|------------------------------------------|-----------------------------|-----------------------|
| **V4L2 (classic)**       | V4L2 sensor + bridge     | libv4l2 / v4l-utils        | Simple sensors, USB cams, legacy         | Very high                   | Kernel community      |
| **V4L2 + Media Controller** | Media Controller (MC) | libcamera / gstreamer      | Complex pipelines, ISP control           | High                        | Standard for SoCs     |
| **libcamera**            | V4L2 + MC + proprietary  | libcamera API / libcamera-apps | Phones, Raspberry Pi, embedded vision   | Very high (2024+)           | Raspberry Pi + collab |
| **Android Camera HAL3**  | V4L2 + proprietary       | Camera2 / CameraX API      | Android phones/tablets                   | Dominant on mobile          | Google + SoC vendors  |
| **GStreamer pipelines**  | Any V4L2 / libcamera src   | gst-launch / apps          | Streaming, recording, processing         | Very high                   | GStreamer community   |
| **OpenCV VideoCapture**  | V4L2 / libcamera backend   | cv::VideoCapture           | CV/ML prototyping                        | High                        | OpenCV                |
| **IPU6 / IPU3 / Rockchip ISP** | Vendor-specific MC   | libcamera / custom         | Intel laptops, Rockchip SoCs             | Medium–high                 | Vendor + community    |

📡 2. Typical Modern Camera Pipeline (2025–2026)

CSI-2 / MIPI → Sensor (raw Bayer) 
          ↓
     [C-PHY / D-PHY]
          ↓
     SoC CSI-2 receiver
          ↓
     [ISP hardware blocks]
          ├─ Bayer → RGB (debayer / demosaic)
          ├─ Auto Exposure / Auto White Balance / Auto Focus (3A)
          ├─ Noise reduction / sharpening / gamma / color correction
          ├─ Statistics output (for 3A algorithms)
          ↓
     [Memory buffers – MMAP or DMABUF]
          ↓
     V4L2 subdev (sensor) ← Media Controller routing
          ↓
     V4L2 main device (/dev/videoX) or libcamera IPA
          ↓
     Userspace: libcamera / GStreamer / Android HAL / OpenCV
          ↓
     Application: preview, still capture, video encode (h264/hevc/av1)

⭐ 🎓 3. Key Kernel Structures & Concepts

| Concept / Structure              | Location                          | Purpose / Notes |
|----------------------------------|-----------------------------------|-----------------|
| ``struct v4l2_subdev``             | ``include/media/v4l2-subdev.h``     | Sensor, lens, flash, CSI-2 receiver |
| ``struct media_entity``            | ``include/media/media-entity.h``    | Graph node (pads, links) |
| ``struct media_pad``               | —                                 | Input/output port of entity |
| ``struct media_link``              | —                                 | Connection between pads |
| ``struct v4l2_mbus_framefmt``      | ``include/uapi/linux/v4l2-mediabus.h`` | Bus format (Bayer, YUV, RGB, resolution) |
| ``V4L2_CID_*`` controls            | ``include/uapi/linux/v4l2-controls.h`` | Exposure, gain, VBLANK, HBLANK, test pattern… |
| ``media_request``                  | ``include/media/media-request.h``   | Request API – atomic configuration + queuing (since ~5.3) |
| ``vb2_v4l2_buffer``                | ``include/media/videobuf2-v4l2.h``  | Buffer with timestamp, flags, request_fd |
| ``DMABUF`` import/export           | ``drivers/media/v4l2-core/videobuf2-dma-contig.c`` | Zero-copy sharing with GPU/encoder/NPU |

⭐ 🔧 4. Important Device Nodes

| Node                     | Typical Meaning                                   | Framework |
|--------------------------|---------------------------------------------------|-----------|
| ``/dev/video0``–``/dev/videoN`` | Main video capture node                           | V4L2      |
| ``/dev/media0``–``/dev/mediaN`` | Media Controller graph control                    | MC        |
| ``/dev/v4l-subdevX``       | Individual sub-device (sensor, ISP block)         | MC + libcamera |
| ``/dev/videoY`` (statistics) | 3A stats output (histogram, AWB regions…)        | libcamera / vendor |

📌 5. Quick Comparison Table – Which to Use When

| Requirement                              | Recommended Stack (2026)              | Why / Trade-offs |
|------------------------------------------|----------------------------------------|------------------|
| Simple USB webcam                        | V4L2 + libv4l2                         | Plug & play      |
| Raspberry Pi HQ / Camera Module          | libcamera (rpicam-apps / Picamera2)    | 🟢 🟢 Best integration |
| Android phone / tablet                   | Android Camera HAL3 + vendor ISP       | Google policy    |
| Embedded product (non-Android)           | libcamera or pure Media-Controller + GStreamer | Flexible, upstream-friendly |
| Real-time CV/ML (Jetson, RK3588, etc.)   | GStreamer + nvarguscamerasrc / rkaiq / libcamera | Lowest latency path |
| Automotive / ASIL                        | Custom V4L2 + Safety extensions        | ISO 26262        |
| Intel MIPI cameras (laptops)             | libcamera + ipu6 driver                | Upstream effort ongoing |

🐛 6. Debugging & Tools (2026 era)

.. code-block:: bash

================================================================================
🔧 List devices & capabilities
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext
media-ctl -p -d /dev/media0                # show graph

================================================================================
Query controls
================================================================================

v4l2-ctl -d /dev/video0 --list-ctrls

================================================================================
Set manual exposure
================================================================================

v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=200

================================================================================
💾 Capture single frame (libcamera)
================================================================================

libcamera-still -o test.jpg

================================================================================
Capture raw Bayer
================================================================================

libcamera-raw -o test.raw --mode 4056:3040:12:P

================================================================================
GStreamer simple pipeline
================================================================================

gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,width=1920,height=1080 ! videoconvert ! autovideosink

================================================================================
📡 libcamera + GStreamer
================================================================================

gst-launch-1.0 libcamerasrc ! video/x-raw,width=1920,height=1080 ! videoconvert ! autovideosink

================================================================================
🐛 Trace media controller events
================================================================================

echo 1 > /sys/kernel/debug/tracing/events/media/enable
cat /sys/kernel/debug/tracing/trace_pipe

📌 7. Current Trends (early 2026)

- **libcamera** becoming de-facto standard for non-Android embedded Linux
- **Request API** (media requests) widely used for atomic 3A + capture
- **DMABUF** everywhere for zero-copy → GPU / NPU / encoder
- **CSI-2 D-PHY → C-PHY** transition on newer SoCs
- **Raw capture + userspace ISP** gaining traction (libcamera IPA modules)
- **Upstream effort**: Intel IPU6, Qualcomm CAMSS, Rockchip ISP, Mediatek ISP all improving

Use this cheatsheet when choosing stack, writing drivers, integrating sensors, or debugging ISP pipelines on modern Linux embedded systems.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
