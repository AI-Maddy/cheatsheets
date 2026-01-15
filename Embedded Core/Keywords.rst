🔧 **Embedded Core — SOC & ARM Keywords Reference**
═════════════════════════════════════════════════════════════════════

**Quick Reference for System-on-Chip and ARM Architecture Terminology**  
**Domains:** Automotive SOCs 🚗 | ADAS Computing 📡 | Embedded Vision 📷  
**Purpose:** Rapid term lookup, architecture comparison, SOC selection

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════════════

⭐ **ARM CORE ARCHITECTURES**
─────────────────────────────

**ARM Cortex-A Series (Application Processors)**

- **Cortex-A76/A78/A710** – High-performance cores for automotive infotainment, ADAS domain controllers
- **Cortex-A55/A53** – Efficiency cores for low-power applications
- **ARM v8/v9 Architecture** – 64-bit instruction set (AArch64)
- **big.LITTLE** – Heterogeneous multi-processing (performance + efficiency cores)
- **DynamIQ** – Flexible cluster configuration (mix A78 + A55 in single cluster)

**ARM Cortex-R Series (Real-Time)**

- **Cortex-R52/R82** – Safety-critical real-time cores for ASIL D / SIL 3
- **Lockstep Mode** – Dual-core redundant execution for fault detection
- **TCM (Tightly-Coupled Memory)** – Deterministic low-latency memory access
- **MPU (Memory Protection Unit)** – Isolate safety-critical regions

**ARM Cortex-M Series (Microcontrollers)**

- **Cortex-M7/M33/M55** – Mixed-signal control, sensor hubs, motor control
- **M-Profile Vector Extension (MVE / Helium)** – DSP & ML acceleration on M-cores
- **TrustZone-M** – Hardware-based security isolation

════════════════════════════════════════════════════════════════════════════

🚗 **AUTOMOTIVE SOC KEYWORDS**
──────────────────────────────

**SOC Platforms**

- **NVIDIA Orin** – 254 TOPS, Ampere GPU, 12× ARM A78AE cores (ASIL D)
- **NVIDIA Thor** – 2000 TOPS, next-gen unified compute for ADAS + cockpit
- **Qualcomm Snapdragon Ride** – 700 TOPS, automotive-grade ADAS platform
- **TI TDA4** – 8 TOPS, Jacinto processor for camera perception & sensor fusion
- **NXP S32G/S32V** – Automotive vehicle compute, radar/vision processing
- **Renesas R-Car H3/V3U** – Cockpit, gateway, ADAS compute
- **Mobileye EyeQ5/EyeQ6** – Purpose-built vision processing (24 TOPS → 176 TOPS)

**ADAS Compute Requirements**

- **L2/L2+ ADAS** – 10-30 TOPS (highway assist, lane keeping, ACC)
- **L3 Conditional Autonomy** – 100-300 TOPS (traffic jam pilot, hands-off highway)
- **L4 High Autonomy** – 500-2000+ TOPS (robotaxi, urban driving)

**SOC Components**

- **CPU Cluster** – ARM A78/A55 for middleware, OS, control
- **GPU** – Graphics + compute (OpenGL, Vulkan, CUDA/OpenCL)
- **NPU / DLA (Deep Learning Accelerator)** – Dedicated neural network inference
- **ISP (Image Signal Processor)** – RAW image processing, demosaicing, HDR
- **DSP (Digital Signal Processor)** – Sensor fusion, signal processing
- **Video Encoder/Decoder** – H.264, H.265 encode/decode for recording/streaming
- **HSM (Hardware Security Module)** – Crypto acceleration, secure boot, key storage

════════════════════════════════════════════════════════════════════════════

📡 **ADAS & PERCEPTION KEYWORDS**
─────────────────────────────────

**Camera Processing**

- **ISP Pipeline** – Bayer demosaicing, white balance, tone mapping, noise reduction
- **Multi-camera Stitching** – Surround-view 360° (4-6 cameras)
- **HDR (High Dynamic Range)** – Handle high-contrast scenes (bright sun + dark shadows)
- **Lens Distortion Correction** – Fisheye undistortion for wide-angle cameras

**Neural Network Acceleration**

- **INT8 Inference** – Quantized neural networks for efficiency (4× faster than FP16)
- **TOPS (Tera Operations Per Second)** – Performance metric for NN compute
- **TensorRT** – NVIDIA optimization framework for inference
- **ONNX Runtime** – Cross-platform neural network runtime
- **Quantization-Aware Training (QAT)** – Train with INT8 precision in mind

**Sensor Fusion**

- **Early Fusion** – Combine RAW sensor data (camera + radar pixels)
- **Late Fusion** – Combine detected objects from each sensor
- **Deep Fusion** – Neural network learns optimal sensor combination
- **Kalman Filter** – State estimation for object tracking
- **EKF (Extended Kalman Filter)** – Nonlinear sensor fusion

════════════════════════════════════════════════════════════════════════════

🖥️ **GPU & COMPUTE KEYWORDS**
──────────────────────────────

**NVIDIA GPU Architectures**

- **Ampere** – GA10x architecture (Orin SOC, 2020-2024)
- **Hopper** – H100 datacenter GPU (not automotive yet)
- **CUDA Cores** – Parallel processing units for general compute
- **Tensor Cores** – Specialized matrix multiply units for AI (FP16, INT8, INT4)
- **RT Cores** – Ray tracing acceleration (for photorealistic rendering)

**CUDA Programming**

- **Kernel** – Function executed in parallel on GPU
- **Thread Block** – Group of threads sharing shared memory
- **Warp** – 32 threads executing in lockstep (SIMT - Single Instruction Multiple Thread)
- **Occupancy** – Percentage of GPU utilized (maximize for performance)
- **Unified Memory** – Shared address space between CPU & GPU

**Memory Hierarchy**

- **Global Memory** – Large, high-latency DRAM (GB scale)
- **Shared Memory** – Fast, on-chip SRAM per thread block (KB scale)
- **Registers** – Fastest, per-thread storage (limited)
- **L1/L2 Cache** – Automatic caching between shared & global memory

════════════════════════════════════════════════════════════════════════════

🔬 **COMPUTER VISION KEYWORDS**
───────────────────────────────

**Classic Vision Algorithms**

- **Feature Detection** – Harris corners, SIFT, ORB
- **Optical Flow** – Lucas-Kanade, Farneback for motion estimation
- **Stereo Vision** – Depth from binocular cameras (disparity map)
- **Structure from Motion (SfM)** – 3D reconstruction from monocular video

**Deep Learning Models**

- **YOLO (You Only Look Once)** – Real-time object detection (v5, v7, v8, v9, v10)
- **EfficientDet** – Scalable object detection (D0-D7 variants)
- **DETR (Detection Transformer)** – End-to-end object detection without anchors
- **SegFormer** – Semantic segmentation with transformers
- **BEVFormer** – Bird's-eye-view perception from multi-camera
- **Occupancy Networks** – 3D voxel occupancy prediction

**Model Optimization**

- **Pruning** – Remove unnecessary weights to reduce model size
- **Knowledge Distillation** – Train small model to mimic large model
- **TensorRT Optimization** – Layer fusion, precision calibration (FP32→INT8)
- **ONNX Export** – Framework-agnostic model format

════════════════════════════════════════════════════════════════════════════

⚡ **PERFORMANCE METRICS**
─────────────────────────

**Compute Metrics**

- **TOPS** – Tera (trillion) operations per second (AI performance)
- **TFLOPS** – Tera floating-point operations per second (GPU compute)
- **FPS (Frames Per Second)** – Throughput for camera processing
- **Latency** – Time from sensor input to actuator output (critical for L3+)

**Power Metrics**

- **TDP (Thermal Design Power)** – Maximum heat dissipation (Watts)
- **TOPS/W** – AI efficiency (operations per Watt)
- **Power Modes** – High performance, balanced, low power (DVFS scaling)

**Memory Metrics**

- **Bandwidth** – GB/s transfer rate (LPDDR5: 51.2 GB/s typical)
- **Latency** – Access time (ns)
- **Cache Hit Rate** – Percentage of memory accesses served by cache

════════════════════════════════════════════════════════════════════════════

🛡️ **SAFETY & SECURITY KEYWORDS**
──────────────────────────────────

**Functional Safety (ISO 26262)**

- **ASIL B/D Cores** – Safety-certified ARM cores (R52, A78AE with lockstep)
- **Safety Island** – Isolated ASIL D partition for monitoring
- **Lockstep Execution** – Dual-core redundant compute with comparison
- **ECC (Error Correcting Code)** – Detect/correct memory bit flips
- **FTTI (Fault Tolerant Time Interval)** – Max time to detect & respond to faults

**Cybersecurity**

- **Secure Boot** – Verify firmware integrity at startup
- **TrustZone** – Hardware-based secure world isolation
- **HSM (Hardware Security Module)** – Crypto acceleration, key storage
- **OTA Security** – Encrypted, signed over-the-air updates
- **Intrusion Detection** – Monitor CAN bus, Ethernet for attacks

════════════════════════════════════════════════════════════════════════════

🔌 **CONNECTIVITY & INTERFACES**
────────────────────────────────

**Camera Interfaces**

- **MIPI CSI-2** – Mobile camera serial interface (up to 6 Gbps per lane)
- **GMSL (Gigabit Multimedia Serial Link)** – Long-reach camera over coax (up to 15m)
- **FPD-Link III** – Texas Instruments camera serializer/deserializer

**Vehicle Networks**

- **CAN / CAN-FD** – Controller Area Network for vehicle control (1 Mbps / 8 Mbps)
- **Automotive Ethernet** – 100 Mbps, 1 Gbps, 10 Gbps (ADAS sensor data)
- **FlexRay** – Deterministic time-triggered network (safety-critical)

**PCIe & High-Speed**

- **PCIe Gen 3/4/5** – Peripheral Component Interconnect Express (8/16/32 GT/s)
- **NVMe** – High-speed SSD storage over PCIe

════════════════════════════════════════════════════════════════════════════

📊 **SOC COMPARISON TABLE**
───────────────────────────

| SOC | CPU | GPU TOPS | ASIL | TDP | Use Case |
|:----|:----|:---------|:-----|:----|:---------|
| NVIDIA Orin | 12× A78AE | 254 | D | 60W | L3/L4 ADAS, robotaxi |
| NVIDIA Thor | 16× Custom | 2000 | D | 300W | L4/L5, unified compute |
| Qualcomm Ride | 16× Kryo | 700 | D | 65W | L2+/L3 ADAS |
| TI TDA4 | 2× A72 + 6× R5F | 8 | D | 20W | L2 ADAS, camera |
| Mobileye EyeQ6 | 12× Custom | 176 | B(D) | 30W | L2+/L3 vision |
| NXP S32G3 | 8× A53 + 4× M7 | — | D | 25W | Gateway, V2X |
| Renesas V3U | 8× A76 + R52 | 60 | D | 35W | L2 ADAS, cockpit |

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Memorization**
─────────────────────────────────

**ARM Cores:**
- **Cortex-A:** Application processors (Linux, Android)
- **Cortex-R:** Real-time, safety-critical (lockstep)
- **Cortex-M:** Microcontrollers, sensor hubs

**TOPS Scale:**
- **10 TOPS:** L2 ADAS (lane keeping, ACC)
- **100 TOPS:** L2+ / L3 (hands-off highway)
- **500+ TOPS:** L4 (urban autonomy, robotaxi)

**Key SOCs:**
- **NVIDIA Orin:** 254 TOPS, market leader for L3/L4
- **TI TDA4:** 8 TOPS, cost-effective L2
- **Qualcomm Ride:** 700 TOPS, challenger to Orin

**Safety:**
- **Lockstep:** Dual-core redundant execution (ASIL D)
- **Safety Island:** Isolated partition for monitoring
- **ECC:** Memory error correction

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Coverage:** ARM architectures, automotive SOCs, ADAS compute, GPU programming, computer vision, safety/security
