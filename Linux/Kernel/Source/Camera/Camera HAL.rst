**cheatsheet for Android Camera HAL3** (as of early 2026 – Android 15/16 era, AOSP mainline perspective).  
HAL3 remains the **standard** camera hardware abstraction layer for Camera2 API (deprecated HAL1 since Android 9+). It uses a **request → pipeline → result** model with per-frame control.

📖 1. Architecture Overview

App → Camera2 API (CaptureRequest / CaptureResult)
      ↓
Camera Service (framework) → ICameraDevice (open/close)
      ↓ (Binder / AIDL since Android 13+)
Camera HAL3 process (vendor implementation)
      ├─ ICameraDevice → openSession() → ICameraDeviceSession
      └─ Pipeline (sensor → ISP → 3A → processing → buffers)

- **Process separation** (since Android 8.0 Treble): HAL runs in its own process (``cuttlefish`` / vendor binaries).
- **Interface evolution**:
  - HIDL (Android 8–12): ``android.hardware.camera.device@3.x``
  - AIDL (Android 13+): Stable AIDL interfaces
⭐ - **Key principle**: **Stateless pipeline** – each ``CaptureRequest`` fully specifies config (sensor, 3A, ISP settings, output streams).

📌 2. Core HAL3 Components & Interfaces

⭐ | Component / Interface              | Purpose / Key Methods                                                                 | Called by Framework When? |
|------------------------------------|---------------------------------------------------------------------------------------|----------------------------|
| ``ICameraDevice``                    | Device-level entry point (open/close)                                                 | App opens camera           |
|                                    | ``getCameraInfo()``, ``open()`` → returns ``ICameraDeviceSession``                          | —                          |
| ``ICameraDeviceSession``             | **Active session** – main control interface                                           | After open()               |
|                                    | ``configureStreams()``<br>``processCaptureRequest()``<br>``processCaptureResult()`` callback<br>``notify()`` (shutter/error)<br>``close()``<br>``constructDefaultRequestSettings()`` | Config change / capture    |
| ``ICameraDeviceCallback``            | HAL → framework callbacks                                                             | —                          |
|                                    | ``processCaptureResult()`` – metadata + filled buffers<br>``notify()`` – shutter / error  | HAL has result             |
| ``Camera3Device`` / ``camera3_device_t`` (legacy struct) | Internal wrapper (still referenced in some docs)                               | —                          |

📌 3. Capture Pipeline Flow (Request → Result)

1. Framework calls ``configureStreams()``  
   → HAL validates/adjusts stream list (preview/video/still/raw/…)  
   → Returns max buffers needed per stream (``max_buffers``)

2. Framework builds ``CaptureRequest``  
⭐    - Sets keys: ``SENSOR_EXPOSURE_TIME``, ``CONTROL_AF_MODE``, ``STATISTICS_FACE_DETECT_MODE``, …  
   - Attaches output ``StreamBuffer``s (targets)

3. ``processCaptureRequest(request, /*repeating*/)``  
   - HAL queues request (FIFO pipeline, depth reported via ``getPipelineDepth()`` or caps)  
   - Returns immediately (non-blocking)

4. HAL processes internally  
   - Sensor capture → ISP blocks (debayer, 3A stats, noise reduction, color correction, …)  
   - Fills buffers (YUV/JPEG/RAW/…)  
   - Generates metadata (``CaptureResult``)

5. HAL calls ``processCaptureResult()`` (in order of submission)  
   - Includes partial results (e.g. 3A stats early) or full  
   - Buffers marked ``CAMERA3_BUFFER_STATUS_OK`` / ``ERROR``

6. Optional: ``notify()`` for events (shutter time, error, reprocess)

7. ``close()`` / ``flush()`` → drain pipeline, return buffers with error status if needed

⭐ 🎓 4. Key Concepts & Behaviors

⭐ | Concept                     | Description / Important Notes (2026)                                                                 |
|-----------------------------|------------------------------------------------------------------------------------------------------|
| **Pipeline Depth**          | How many requests can be in flight (reported in caps) – typically 3–10 depending on ISP             |
| **Repeating Request**       | ``setRepeatingRequest()`` for preview/video – high priority, low jitter required                      |
| **Manual Control**          | ``MANUAL_SENSOR`` capability → app controls exposure/gain/white-balance/black-level …                 |
| **RAW Support**             | ``RAW_SENSOR`` output → app can implement full ISP pipeline (slow for preview)                        |
⭐ | **3A (Auto Exposure / Focus / White Balance)** | HAL usually handles; app can override via ``CONTROL_*`` keys or use stats output for custom 3A |
| **Partial Results**         | HAL can return metadata in stages (e.g. AE results before full image)                               |
| **Buffer Management API**   | Optional since Android 10: ``requestStreamBuffers()``, ``returnStreamBuffers()`` – reduces memory waste (decouples buffers from requests) |
| **Reprocessing**            | Input stream (e.g. RAW) + request → re-run ISP (for better JPEG from RAW)                           |
⭐ | **Vendor Tags**             | Custom ``CaptureRequest`` / ``CaptureResult`` keys (e.g. Qualcomm bayer stats, exposure metering)      |

📌 5. HAL3 vs HAL1 Quick Comparison

| Feature                     | HAL1 (deprecated)                          | HAL3 (current)                              |
|-----------------------------|--------------------------------------------|---------------------------------------------|
| Control granularity         | Coarse modes (preview/video/still)         | Per-frame full control                      |
| Pipeline model              | Push-based, opaque                         | Pull-based, request/result FIFO             |
| Latency & jitter            | Higher / variable                          | Lower / predictable                         |
| Custom 3A possible?         | No                                         | Yes (via stats + vendor extensions)         |
| Android requirement         | Deprecated since Android 9                 | Mandatory for new devices                   |

🐛 6. Debugging & Development Tips (2026)

.. code-block:: bash

================================================================================
📡 Enable verbose camera logging
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



adb shell setprop persist.camera.hal.debug 1
adb logcat -s CameraService CameraDeviceSession

================================================================================
📡 Dump current camera state
================================================================================

adb shell dumpsys media.camera

================================================================================
List capabilities & characteristics
================================================================================

adb shell dumpsys media.camera | grep "Camera .* characteristics"

================================================================================
CTS verifier / VTS for HAL3
================================================================================

atest CtsCameraITS
VTS tests: android.hardware.camera*

================================================================================
📚 AOSP reference HAL (emulator / cuttlefish)
================================================================================

hardware/interfaces/camera/device/

================================================================================
💻 Common vendor implementations
================================================================================

Qualcomm: vendor/qcom/proprietary/camera
MediaTek: vendor/mediatek/proprietary/camera

HAL3 remains the foundation for high-performance camera apps (burst, manual controls, computational photography). For new devices in 2026, focus on AIDL interfaces, buffer management APIs, and low-latency repeating requests.

🟢 🟢 Good luck with your Android camera HAL / Camera2 development!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
