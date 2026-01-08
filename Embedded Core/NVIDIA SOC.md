### NVIDIA DRIVE Orin Cheat Sheet

NVIDIA DRIVE Orin (also known as DRIVE AGX Orin) is a high-performance, automotive-grade SoC designed for **autonomous vehicles (AVs)**, ADAS, and software-defined vehicles. It powers Level 2+ to Level 5 autonomy with functional safety and scalability.

#### Key Performance Specifications
- **AI Compute**: Up to **254 TOPS** (INT8 trillions of operations per second)
- **Performance Multiplier**: ~7x over previous generation (Xavier's ~30 TOPS)
- **Configurations**: Scalable family; single Orin SoC = 254 TOPS; dual setups (e.g., in some vehicles) = up to 508 TOPS
- **Safety Standards**: ISO 26262 ASIL-D (systematic safety for AVs)

#### Core Architecture
- **CPU**: 12-core Arm Cortex-A78AE (safety-certified)
- **GPU**: Next-gen NVIDIA Ampere architecture with Tensor Cores
- **Accelerators**:
  - Deep Learning Accelerators (DLA): 2x for efficient DNN inference
  - Programmable Vision Accelerator (PVA v2): For computer vision tasks (e.g., optical flow)
  - Additional: NVENC/NVDEC for video, safety islands
- **Memory**: High-bandwidth LPDDR5, large unified memory for complex workloads

#### Key Features
- **Software-Defined Platform**: Over-the-air (OTA) updates for continuous improvement
- **Workloads**: Handles multiple concurrent DNNs for perception, planning, sensor fusion, and actuation
- **I/O**: Rich automotive interfaces (e.g., CAN, Ethernet, PCIe, cameras/lidars via mini-SAS)
- **Power Efficiency**: Optimized for in-vehicle use (higher TDP than Jetson equivalents)
- **Software Stack**: NVIDIA DRIVE OS (Linux/QNX), DriveWorks, CUDA, TensorRT, safety-certified libraries

#### Developer Kit
- **DRIVE AGX Orin DevKit**: Includes Orin SoC, automotive I/O, bench/in-vehicle options
- **Availability**: General access with DRIVE OS 6+

#### Vs. Jetson AGX Orin (Common Confusion)
- **Similar SoC Core** — Shared architecture (Ampere GPU, Arm CPU, ~254-275 TOPS max)
- **Differences**:
  | Aspect              | DRIVE Orin                          | Jetson AGX Orin                     |
  |---------------------|-------------------------------------|-------------------------------------|
  | Target              | Automotive (AVs, ADAS)              | Embedded/robotics/general AI        |
  | Safety              | ASIL-D certified                    | No automotive safety rating         |
  | Software            | DRIVE OS (safety-hardened)          | JetPack (general-purpose)           |
  | I/O & Durability    | Automotive-grade interfaces         | General embedded I/O                |
  | Power/Env           | Vehicle-qualified                   | Lower power modes (15-60W)          |

#### Adoption Highlights (as of 2026)
- Used by: Volvo, Toyota, BYD, NIO, Li Auto, JLR, Zeekr, and more
- In production vehicles since ~2022-2023
- Successor: DRIVE Thor (Blackwell-based, higher performance)

For detailed datasheets or dev access, join the NVIDIA DRIVE SDK program on developer.nvidia.com. Specs are based on official NVIDIA announcements and may vary by configuration.