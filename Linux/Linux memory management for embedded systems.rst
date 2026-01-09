
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**Linux memory management policies & practices** that are particularly relevant when working with **embedded systems** involving **cameras**, **video pipelines**, and **AI/ML inference** accelerators (NPU, GPU, DSP, VPU, etc.).

Most of the pain points in these devices revolve around:

- Zero-copy / low-latency access to large buffers
- Contiguous physical memory requirements
- Cache coherency between CPU ↔ accelerator
- Memory bandwidth starvation
- CMA (Contiguous Memory Allocator) pressure & fragmentation
- 🔴 🔴 Avoiding page faults in real-time paths

⭐ 💾 1. Key Memory Types & Their Role in Camera / Video / AI

Type / Allocator          | Physical contiguity | Cache behavior          | Typical use in camera/video/AI                  | Main pain points
--------------------------|----------------------|--------------------------|--------------------------------------------------|-----------------------
**Normal page cache**     | No                   | Cached                   | jpeg buffers, small metadata                     | page faults, TLB pressure
**Anonymous memory**      | No                   | Cached                   | model weights (if not pinned), CPU-side tensors  | fragmentation, reclaim latency
**vmalloc**               | No (virtual yes)     | Cached                   | Rarely used — 🔴 🔴 avoid in video paths               | TLB misses, slow mapping
**kmalloc / dma_alloc_coherent** | Yes (small)   | Coherent / DMA-safe      | Small control structures, firmware blobs         | Limited size (<128 KiB usually)
**dma_alloc_attrs(…, DMA_ATTR_NON_CONSISTENT)** | Yes   | Non-coherent             | Most camera / V4L2 / DRM buffers                 | Manual cache maintenance needed
**CMA (Contiguous Memory Allocator)** | Yes (large) | Usually non-coherent | Big video frames, input/output tensors, ISP buffers | Fragmentation over time
**Ion / dmabuf-heap**     | Yes                  | Driver-managed coherency | Modern zero-copy path (V4L2 + NPU + display)     | Heap selection, fragmentation
**HugeTLB / Transparent Huge Pages (THP)** | Yes (2 MiB) | Cached / huge pages     | Large model weights, inference input tensors     | Alignment, availability
**dmabuf**                | Driver-dependent     | Usually non-coherent     | Cross-subsystem buffer sharing (camera → NPU → display) | Exporter/importer rules

⭐ 🐧 2. Most Important Kernel Config Options (embedded video/AI focus)

Config symbol                                      | Recommended value          | Why it matters in camera/video/AI
---------------------------------------------------|----------------------------|--------------------------------------
``CONFIG_CMA=y``                                     | Yes                        | Almost mandatory for video frames & large tensors
``CONFIG_CMA_SIZE_MBYTES=…``                         | 64–512 (depends on DRAM)   | Reserve early-boot contiguous region
``CONFIG_DMA_CMA=y``                                 | Yes                        | Lets DMA API use CMA
``CONFIG_DMA_SHARED_BUFFER=y``                       | Yes                        | dmabuf foundation
``CONFIG_DMABUF_HEAPS=y``                            | Yes (newer kernels)        | Modern replacement for ION
``CONFIG_TRANSPARENT_HUGEPAGE=y``                    | madvise / always           | Large model weights, inference tensors
⭐ ``CONFIG_HUGETLBFS=y``                               | Yes (if using huge pages)  | Explicit huge pages for critical buffers
``CONFIG_V4L_PLATFORM_DRIVERS=y``                    | Yes                        | Most embedded cameras
``CONFIG_VIDEOBUF2_DMA_CONTIG=y``                    | Yes                        | V4L2 contiguous buffers (most common)
``CONFIG_VIDEOBUF2_DMA_SG=y``                        | Yes (if scatter-gather OK) | Some NPUs accept sg-lists

⚙️ 3. Practical Allocation Strategies (2025–2026 embedded reality)

Use case                              | Recommended path (2024–2026)                     | Alternative (legacy)         | Notes / Gotchas
--------------------------------------|---------------------------------------------------|-------------------------------|---------------------
Single camera frame buffer            | ``vb2-v4l2`` + ``VIDEOBUF2_DMA_CONTIG``              | ``dma_alloc_coherent()``        | CMA-backed, most stable
Camera → NPU zero-copy pipeline       | ``dmabuf`` export from V4L2 → import to NPU         | ION heap                      | Use ``dma-heap-system`` or ``dma-heap-cma``
NPU input tensor (large, aligned)     | ``dma-heap-cma`` + ``dma_buf_map_attachment()``       | HugeTLB + madvise             | 64-byte / 128-byte alignment common
Display sink (Wayland / DRM)          | dmabuf from NPU / V4L2 → DRM PRIME               | —                             | 🔴 🔴 Avoid CPU copy at all costs
Model weights loading                 | ``mmap()`` + ``madvise(MADV_HUGEPAGE)`` or hugetlbfs  | Normal anonymous pages        | Reduces TLB pressure
Firmware / DSP blobs                  | ``dma_alloc_coherent()`` or CMA carveout            | vmalloc (🔴 🔴 avoid)               | Needs to be DMA-safe
Real-time guaranteed buffer           | Pre-allocate CMA at boot + reserve               | Dynamic CMA alloc             | 🔴 🔴 Avoid dynamic alloc in RT path

📌 4. CMA-related Commands & Tuning (most painful part)

Command / sysfs                                   | Purpose / Typical value
--------------------------------------------------|-------------------------
``cat /proc/meminfo | grep Cma``                 | See total / free CMA
``cat /sys/kernel/debug/dma_buf_dump``              | See dmabuf usage (if debug enabled)
``echo 1 > /proc/sys/vm/drop_caches``               | Free page cache → helps CMA compaction
``cat /proc/cma_info``                              | Detailed CMA allocation map (debug)
``cma=128M`` or ``cma=256M`` (kernel cmdline)         | Reserve at boot (most reliable)
``CONFIG_CMA_DEBUGFS=y`` + ``mount -t debugfs …``     | Debug CMA fragmentation

💾 5. Quick Tuning & Boot Parameters (embedded video/AI devices)

Parameter / setting                               | Common value / recommendation
--------------------------------------------------|---------------------------------------
``cma=256M``                                        | Reserve 256 MiB contiguous at boot
``cma=512M video=1920x1080@60``                     | For 4K-capable devices
``vm.min_free_kbytes=65536``                        | Protect against OOM during burst
``vm.swappiness=10``                                | Almost never swap on embedded (no swap usually)
``vm.dirty_background_ratio=5``                     | ``vm.dirty_ratio=10``
``hugepagesz=2M hugepages=512``                     | If using explicit huge pages for models
``transparent_hugepage=always`` or ``madvise``        | madvise safer on small-RAM devices
``isolcpus=…`` + ``nohz_full=…``                      | Isolate cores for camera/NPU threads

🏗️ 6. Most Common Anti-Patterns to 🔴 🔴 Avoid (2025–2026)

- Doing ``kmalloc(4*1024*1024, GFP_KERNEL)`` in probe → fails after a while
- Relying on dynamic CMA allocation in streaming path → latency spikes
- Not exporting dmabuf from V4L2 → forces CPU copy → bandwidth killer
- Using vmalloc for video frames → massive TLB pressure
- Forgetting cache maintenance when using non-coherent DMA
- Not pre-reserving CMA → fragmentation kills large buffer alloc after 1–2 days
- Running AI models without THP or hugepages → 10–30% performance loss on big models

💾 Summary – Modern Embedded Camera/Video/AI Memory Strategy (2026)

1. Reserve **large CMA region** at boot (``cma=256M`` or more)
2. Use **V4L2 + vb2-v4l2 + DMA_CONTIG** for camera capture
3. Use **dmabuf** (dma-heap-cma or system) for zero-copy handoff to NPU/VPU/display
4. For large tensors/weights → prefer **madvise(MADV_HUGEPAGE)** or explicit hugetlbfs
5. Minimize anonymous memory pressure → 🔴 🔴 avoid swap, tune dirty ratios
6. Monitor **CMA free** + **/proc/meminfo** + **PSI memory** pressure
7. Test long-term stability — fragmentation is the #1 silent killer

🟢 🟢 Good luck with your camera / video / AI embedded product!  
The difference between a working prototype and a shippable product is usually **CMA sizing + dmabuf pipeline + fragmentation resistance**.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
