🚀 **CUDA Basics Cheatsheet** 🚀 (GPU Parallel Programming)
==============================================================

A **concise guide** to CUDA parallel computing on NVIDIA GPUs (CUDA Toolkit ~13.x, 2025–2026). Master the essential programming model, synchronization, memory hierarchy, and performance patterns.

**Official Reference**: CUDA C++ Programming Guide (v13.1+) at https://docs.nvidia.com/cuda/cuda-c-programming-guide/

---

🏗️ **1. Core Concepts & Execution Hierarchy**
==============================================

🏗️ **1. Core Concepts & Execution Hierarchy**
==============================================

The **CUDA execution model** is hierarchical. Understand these 4 layers:

| 🎯 Concept        | 📖 Description                                        | 📊 Max Limits (GPU-dependent) | 🖥️ Built-in Variables      |
|-------------------|-------------------------------------------------------|-----------------------------|-----------------------|
| **Thread** 🔵      | Single task (smallest unit)                          | —                            | `threadIdx.x/y/z`     |
| **Warp** 📦        | 32 threads executing in lock-step (SIMT)             | —                           | `warpSize` (always 32)|
| **Block** 🧱       | Group of warps (shared memory, sync possible)         | 1024 threads/block          | `blockIdx`, `blockDim` |
| **Grid** 🌐        | Collection of blocks (independent, parallel)          | Millions of blocks          | `gridDim`             |

**Memory Hierarchy Visualization**:

.. code-block:: text

   🌐 Grid
   ├─ 🧱 Block 0 (shared memory, 48 KB)
   │  ├─ 📦 Warp 0 (32 threads)
   │  │  ├─ 🔵 Thread 0 (registers: ~255 bytes)
   │  │  ├─ 🔵 Thread 1
   │  │  └─ ...
   │  └─ 📦 Warp 1
   │
   ├─ 🧱 Block 1
   │  └─ ...
   │
   └─ ... (millions of blocks)
   
   🧠 Global Memory (device DRAM, multiple GB)
   ⚡ Constant Memory (64 KB, read-only cache)

**Key Points**:
   ✅ Threads in a **block** can synchronize via `__syncthreads()` and access shared memory
   ✅ Threads in different **blocks** are independent (no direct sync!)
   ✅ **Warps** execute in lock-step → minimize branch divergence
   ✅ 32 = magic number (warp size = 32 on all modern NVIDIA GPUs)

💻 **2. Kernel Launch Syntax** (The Magic Formula)
==================================================

```cuda
kernelName<<<gridDim, blockDim, sharedMemBytes, stream>>>(args...);
```

**Parameters** 🎯:

   **gridDim** (number of blocks):
   - Type: `dim3` or `int` 
   - Example: `<<<256, ...>>>` → 256 blocks
   - Example: `<<<dim3(32, 32, 1), ...>>>` → 32×32 blocks (2D grid)
   - Can be 1D, 2D, or 3D

   **blockDim** (threads per block):
   - Type: `dim3` or `int`
   - Example: `<<<..., 256>>>` → 256 threads/block
   - Example: `<<<..., dim3(16, 16, 1)>>>` → 16×16 threads (2D block)
   - ⚠️ **Max 1024 threads/block** (product of dimensions)

   **sharedMemBytes** (optional, dynamic shared memory):
   - Size in bytes of shared memory to allocate
   - Default: 0
   - Example: `<<<..., ..., 4096>>>` → 4 KB shared mem/block

   **stream** (optional, async execution):
   - CUDA stream handle (enables async operations)
   - Default: stream 0 (legacy default stream)
   - Example: `<<<..., ..., 0, myStream>>>` → uses custom stream

**Practical Examples** 🔧:

.. code-block:: cuda

   // 1️⃣ Vector addition (1D, 1 million elements)
   int N = 1000000;
   int threadsPerBlock = 256;
   int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
   vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
   // Result: ~3906 blocks × 256 threads = 1M threads total
   
   // 2️⃣ Matrix multiply (2D grid, 2D block)
   dim3 blockDim(16, 16);  // 256 threads/block
   dim3 gridDim((width + 15)/16, (height + 15)/16);
   matmul2D<<<gridDim, blockDim>>>(d_A, d_B, d_C, width, height);
   
   // 3️⃣ With shared memory & stream
   size_t smemBytes = 2048;
   cudaStream_t stream;
   cudaStreamCreate(&stream);
   myKernel<<<256, 128, smemBytes, stream>>>(d_data);
   cudaStreamSynchronize(stream);  // Wait for completion

📍 **3. Thread Indexing Formulas** (Critical for Correctness!)
==============================================================

| 🎯 Purpose                        | 📐 Calculation                    | 💡 When to Use                   |
|-----------------------------------|-----------------------------------|---------------------------------|
| **1D Global Thread ID** 🔵        | `int idx = blockIdx.x * blockDim.x + threadIdx.x;` | Vectors, 1D arrays |
| **1D with Bounds Check** ✅       | `if (idx < N) { ... }`            | **ALWAYS DO THIS!** Prevents out-of-bounds |
| **2D Global (Row-Major)** 🖼️     | `int x = blockIdx.x * blockDim.x + threadIdx.x;`<br>`int y = blockIdx.y * blockDim.y + threadIdx.y;`<br>`int idx = y * width + x;` | Images, matrices |
| **Strided Loop** 🔄              | `for (int i = idx; i < N; i += gridDim.x * blockDim.x)` | Processes all data, good occupancy |

**Key Insight**: Total threads = `gridDim.x * blockDim.x`, so one thread per element:

.. code-block:: cuda

   // ✅ CORRECT: Simple vector kernel
   __global__ void vectorAdd(float *A, float *B, float *C, int N) {
       int idx = blockIdx.x * blockDim.x + threadIdx.x;
       if (idx < N) {
           C[idx] = A[idx] + B[idx];  // One thread per element
       }
   }

   // 🔄 ADVANCED: Strided loop (process more elements if N >> total threads)
   __global__ void vectorAddStrided(float *A, float *B, float *C, int N) {
       int idx = blockIdx.x * blockDim.x + threadIdx.x;
       int stride = gridDim.x * blockDim.x;
       for (int i = idx; i < N; i += stride) {
           C[i] = A[i] + B[i];
       }
   }

   // 2️⃣ 2D Kernel (images)
   __global__ void blur2D(float *input, float *output, int width, int height) {
       int x = blockIdx.x * blockDim.x + threadIdx.x;
       int y = blockIdx.y * blockDim.y + threadIdx.y;
       if (x < width && y < height) {
           int idx = y * width + x;  // Row-major addressing
           output[idx] = ... input calculations ...
       }
   }

💾 **4. Memory Hierarchy & Performance**
========================================

The **memory pyramid** (top = fast but small, bottom = slow but large):

.. code-block:: text

   Speed:   ⚡⚡⚡⚡⚡     Size:    ~256 bytes/thread
   ┌──────────────────┐
   │    Registers     │  Automatic, per-thread
   │   (L1 cache)     │  Fastest! (single cycle)
   └──────────────────┘
           ⬇️
   Speed:   ⚡⚡⚡⚡      Size:    48–96 KB/block
   ┌──────────────────┐
   │  Shared Memory   │  `__shared__` declared
   │   (L2 cache)     │  Fast (4–8 cycles)
   └──────────────────┘
           ⬇️
   Speed:   ⚡⚡⚡       Size:    64 KB (read-only)
   ┌──────────────────┐
   │  Constant Mem    │  `__constant__` declared
   │  (cached)        │  Broadcast to warp
   └──────────────────┘
           ⬇️
   Speed:   ⚡⚡        Size:    8–40 GB
   ┌──────────────────┐
   │   Global Memory  │  Allocated with cudaMalloc
   │   (device DRAM)  │  Slow (100–200 cycles) ⚠️
   └──────────────────┘

**Memory Types** 📊:

| 🧠 Type           | 🔒 Scope / Lifetime       | ⚡ Speed    | 📏 Size | 🖊️ Qualifier / How           | 🔗 Coherent? |
|-------------------|--------------------------|-----------|--------|----------------------------|----|
| **Registers**     | Per thread               | ⚡⚡⚡⚡⚡| ~256 B | Automatic (local variables) | ✅  |
| **Shared**        | Per block                | ⚡⚡⚡⚡  | 48–96 KB | `__shared__ float s[256];` | ✅ (block-level) |
| **Constant**      | Global read-only         | ⚡⚡⚡   | 64 KB | `__constant__ float c[1024];` | ✅ |
| **Global**        | Global (device DRAM)     | ⚡⚡    | ~GB | `cudaMalloc` or kernel param | ✅ (with sync) |
| **Local**         | Per thread (spill)       | ⚡⚡    | Device DRAM | Automatic (overflow from regs) | ✅ |
| **Texture/Read-only** | Read-cached     | ⚡⚡⚡   | Device DRAM | `texture<>` or `__restrict__` | ✅ |

**Unified / Managed Memory** (convenience, slower):

.. code-block:: cuda

   // Accessible from both host & device automatically
   float *ptr;
   cudaMallocManaged(&ptr, size);  // ⚠️ Slower due to page migration
   ptr[0] = 1.0;  // Host access
   kernel<<<...>>>(ptr);  // Device access
   cudaFree(ptr);

**Best Practices**:
   ✅ Keep hot data in **shared memory** (reuse within block)
   ✅ Coalesce **global memory** accesses (threads → sequential addresses)
   ✅ Use **constant memory** for read-only config data
   ✅ Minimize **divergence** to keep threads in sync

🔧 **5. Memory Management API**
==============================

**Allocation & Deallocation** 🛠️:

.. code-block:: cuda

   // Allocate device memory
   float *d_ptr;
   cudaMalloc(&d_ptr, size);  // size in bytes
   if (d_ptr == NULL) { /* error! */ }
   
   // Free device memory (MUST do!)
   cudaFree(d_ptr);
   d_ptr = NULL;  // Good practice

**Host ↔ Device Transfer** 🔄:

.. code-block:: cuda

   // Synchronous (blocks host until done)
   cudaMemcpy(d_ptr, h_ptr, size, cudaMemcpyHostToDevice);
   cudaMemcpy(h_ptr, d_ptr, size, cudaMemcpyDeviceToHost);
   
   // GPU ↔ GPU transfer (P2P)
   cudaMemcpyPeer(d_ptr1, device0, d_ptr2, device1, size);
   
   // Asynchronous (returns immediately, uses stream)
   cudaMemcpyAsync(d_ptr, h_ptr, size, cudaMemcpyHostToDevice, stream);
   cudaStreamSynchronize(stream);  // Wait for completion
   
   // Zero memory (fast)
   cudaMemset(d_ptr, 0, size);

**Streams for Async Operations** ⚡:

.. code-block:: cuda

   cudaStream_t stream;
   cudaStreamCreate(&stream);
   
   // Queue operations (don't wait)
   cudaMemcpyAsync(d_A, h_A, size, cudaMemcpyHostToDevice, stream);
   kernel<<<blocks, threads, 0, stream>>>(d_A);
   cudaMemcpyAsync(h_B, d_B, size, cudaMemcpyDeviceToHost, stream);
   
   // Wait for all ops in this stream
   cudaStreamSynchronize(stream);
   
   cudaStreamDestroy(stream);

🖥️ **6. Kernel Qualifiers & Key Functions**
============================================

**Kernel & Function Qualifiers** 🎯:

.. code-block:: cuda

   // Launched FROM HOST, executes ON DEVICE
   __global__ void kernel_gpu(float *data, int N) {
       int idx = blockIdx.x * blockDim.x + threadIdx.x;
       if (idx < N) data[idx] *= 2.0f;
   }
   
   // Called FROM DEVICE CODE ONLY
   __device__ float helper_gpu(float x) {
       return x * x + 1.0f;
   }
   
   // Callable FROM BOTH HOST & DEVICE
   __host__ __device__ float dual(float x) {
       return x + 1.0f;
   }

**Synchronization & Memory Barriers** 🔒:

.. code-block:: cuda

   // Block-level barrier (all threads in block wait here)
   __syncthreads();
   
   // Memory ordering (thread fence)
   __threadfence();        // Global memory fence
   __threadfence_block();  // Block-level fence
   
   // Warp-level shuffle (communicate within 32-thread warp)
   int result = __shfl_down_sync(0xFFFFFFFF, value, 1);  // Shift right by 1

**Block Primitives** (cooperative operations):

.. code-block:: cuda

   // Warp-level operations
   int warp_sum = __reduce_add_sync(mask, value);  // Reduce across warp
   
   // Block-level operations (requires cooperative groups)
   #include <cooperative_groups.h>
   __global__ void kernel_coop() {
       cg::thread_block block = cg::this_thread_block();
       block.sync();  // Synchronize all threads
   }

🛡️ **7. Error Handling (Essential!)**
======================================

**CUDA Error Checking Macro** 🔴:

.. code-block:: cuda

   #define CUDA_CHECK(call) do { \
       cudaError_t err = (call); \
       if (err != cudaSuccess) { \
           fprintf(stderr, "CUDA Error at %s:%d\n", __FILE__, __LINE__); \
           fprintf(stderr, "  Error: %s\n", cudaGetErrorString(err)); \
           exit(1); \
       } \
   } while(0)
   
   // Usage:
   CUDA_CHECK(cudaMalloc(&d_ptr, size));
   CUDA_CHECK(cudaMemcpy(d_ptr, h_ptr, size, cudaMemcpyHostToDevice));
   CUDA_CHECK(cudaDeviceSynchronize());  // Check kernel errors too!

**Kernel Launch Error Pattern** ✅:

.. code-block:: cuda

   // Kernels return void, check async error separately
   kernel<<<blocks, threads>>>(args);
   CUDA_CHECK(cudaGetLastError());        // Check launch error
   CUDA_CHECK(cudaDeviceSynchronize());   // Check execution error

**Common Errors & Fixes**:

   ❌ **cudaErrorInvalidConfiguration**: Block size > 1024 threads
      ✅ Fix: Reduce `blockDim.x * blockDim.y * blockDim.z ≤ 1024`

   ❌ **cudaErrorMemoryAllocation**: Out of device memory
      ✅ Fix: Reduce allocation size, free unused memory

   ❌ **cudaErrorInvalidResourceHandle**: Accessing invalid memory
      ✅ Fix: Ensure `idx < N` bounds check, no double-free

   ❌ **cudaErrorInvalidMemcpyDirection**: Wrong direction
      ✅ Fix: Use correct `cudaMemcpyHostToDevice` or `cudaMemcpyDeviceToHost`

⚡ **8. Performance Optimization Quick Reference**
==================================================

**Occupancy & Thread Blocks** 🎯:

   🔹 **What is occupancy?** Ratio of active threads to max possible threads
   🔹 **Why? More occupancy = better latency hiding**
   🔹 **Good target: 50–75% occupancy**

   ✅ **Tips**:
      - Block size: Multiple of 32 (warp size)
      - Avoid prime numbers like 65, 128 (use 64 or 128 instead)
      - Use `nvidia-smi` or Nsight Compute to measure actual occupancy

**Memory Coalescing** 📍 (Most Critical!):

   ✅ **Best Case** (coalesced):
      Thread 0 reads from address 0x0000
      Thread 1 reads from address 0x0004 (sequential!)
      Thread 2 reads from address 0x0008
      → Single memory transaction ⚡

   ❌ **Bad Case** (uncoalesced):
      Thread 0 reads from 0x0000
      Thread 1 reads from 0x1000 (random!)
      Thread 2 reads from 0x0010
      → Multiple slow transactions 🐢

   **Fix**: Ensure consecutive threads access consecutive memory addresses

**Shared Memory Optimization** 🧠:

.. code-block:: cuda

   __global__ void matmul_optimized(float *A, float *B, float *C, int N) {
       __shared__ float sA[16][16];  // Shared tile
       __shared__ float sB[16][16];
       
       // Load A tile into shared memory
       sA[threadIdx.y][threadIdx.x] = A[...];
       __syncthreads();  // Wait for all threads
       
       // Compute using fast shared memory
       for (int i = 0; i < 16; i++) {
           sum += sA[threadIdx.y][i] * sB[i][threadIdx.x];
       }
       
       C[...] = sum;
   }

**Common Bottlenecks & Fixes**:

   | 🚫 Problem | 🔧 Solution |
   |-----------|-----------|
   | Low occupancy | Increase block size (if registers allow) |
   | Uncoalesced memory | Reorganize data layout for sequential access |
   | Bank conflicts (shared mem) | Use padding: `__shared__ float s[32][33]` not `[32][32]` |
   | Branch divergence | Minimize `if` statements inside warps |
   | Slow algorithms | Use NVIDIA libraries (cuBLAS, cuDNN, etc.) |

**Profiling Tools** 🔍:

   - **Nsight Compute**: Deep kernel profiling (register usage, memory, etc.)
   - **Nsight Systems**: Whole application timeline
   - **nvprof**: Legacy profiler (still works)
   - **nvidia-smi dmon**: Real-time GPU monitoring

   Command:
   ```bash
   ncu --set full ./my_cuda_app  # Profile with Nsight Compute
   nsys profile ./my_cuda_app     # Profile with Nsight Systems
   ```

This cheatsheet targets everyday CUDA C/C++ usage in 2026 — let me know if you want expansions on cooperative groups, streams, graph execution, or CUDA 13.x+ specifics!
📋 **9. Complete Hello World Example**
======================================

.. code-block:: cuda

   #include <stdio.h>
   #include <cuda_runtime.h>
   
   #define CUDA_CHECK(call) do { \
       cudaError_t err = (call); \
       if (err != cudaSuccess) { \
           printf("CUDA error: %s\n", cudaGetErrorString(err)); \
           exit(1); \
       } \
   } while(0)
   
   // ✅ Simple kernel: add two vectors
   __global__ void vectorAdd(float *A, float *B, float *C, int N) {
       int idx = blockIdx.x * blockDim.x + threadIdx.x;
       if (idx < N) {
           C[idx] = A[idx] + B[idx];
       }
   }
   
   int main() {
       int N = 1000000;
       size_t bytes = N * sizeof(float);
       
       // Host memory
       float *h_A = (float *)malloc(bytes);
       float *h_B = (float *)malloc(bytes);
       float *h_C = (float *)malloc(bytes);
       
       // Initialize host arrays
       for (int i = 0; i < N; i++) {
           h_A[i] = 1.0f;
           h_B[i] = 2.0f;
       }
       
       // Device memory
       float *d_A, *d_B, *d_C;
       CUDA_CHECK(cudaMalloc(&d_A, bytes));
       CUDA_CHECK(cudaMalloc(&d_B, bytes));
       CUDA_CHECK(cudaMalloc(&d_C, bytes));
       
       // Copy host → device
       CUDA_CHECK(cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice));
       CUDA_CHECK(cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice));
       
       // Launch kernel: 256 threads/block, ~3906 blocks
       int threadsPerBlock = 256;
       int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
       vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
       CUDA_CHECK(cudaGetLastError());
       CUDA_CHECK(cudaDeviceSynchronize());
       
       // Copy device → host
       CUDA_CHECK(cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost));
       
       // Verify result
       for (int i = 0; i < 5; i++) {
           printf("C[%d] = %.2f (expected 3.0)\n", i, h_C[i]);
       }
       
       // Cleanup
       cudaFree(d_A);
       cudaFree(d_B);
       cudaFree(d_C);
       free(h_A);
       free(h_B);
       free(h_C);
       
       printf("✅ Success!\n");
       return 0;
   }

**Compilation**:

.. code-block:: bash

   # Compile with nvcc (NVIDIA CUDA Compiler)
   nvcc -o vector_add vector_add.cu
   ./vector_add

---

🎯 **10. Decision Tree: Choosing Block Size**
=============================================

.. code-block:: text

   Start: How much shared memory do you need?
   │
   ├─ NO shared memory?
   │  └─ Pick 256 (very common, good balance)
   │     └─ Performance acceptable?
   │        ├─ YES → Done! 🎉
   │        └─ NO → Try 512 or 128
   │
   ├─ 4 KB shared memory?
   │  └─ Pick 256–512 (allows 2–4 blocks/SM)
   │
   ├─ 16 KB shared memory?
   │  └─ Pick 128–256 (allows 1–2 blocks/SM)
   │
   └─ 32+ KB shared memory?
      └─ Pick 128 or less (serializes blocks)

✅ **Golden Rules**:
   1. Thread block size must be multiple of 32 ✅
   2. Max 1024 threads/block
   3. Aim for 50–75% occupancy
   4. Use Nsight Compute to measure actual occupancy
   5. When in doubt, start with 256 🎯

---

🚀 **11. Key Takeaways (TL;DR)**
==================================

✅ **Hierarchy**: Thread (idx) → Block (shared mem) → Grid (independent)
✅ **Index Formula**: `idx = blockIdx.x * blockDim.x + threadIdx.x`
✅ **Memory**: Registers (fast) → Shared (fast) → Global (slow)
✅ **Coalescing**: Consecutive threads → consecutive addresses = speed! ⚡
✅ **Sync**: `__syncthreads()` only works within a block
✅ **Error Handling**: ALWAYS use CUDA_CHECK macro
✅ **Occupancy**: 50–75% is good, profile with Nsight Compute
✅ **Profiling**: Don't guess, measure with tools!
✅ **Block Size**: Start with 256, multiple of 32
✅ **Shared Memory**: Use for data reuse, avoid bank conflicts

---

📚 **12. Essential Resources**
==============================

🔗 **Official Documentation**:
   - CUDA C++ Programming Guide: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
   - CUDA Runtime API: https://docs.nvidia.com/cuda/cuda-runtime-api/
   - Optimizing CUDA Kernels: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/

📖 **Learning Resources**:
   - "Even Easier Introduction to CUDA" (NVIDIA blog)
   - Udacity FREE course: "Intro to Parallel Programming" (with CUDA)
   - Mark Harris' presentations on CUDA performance

🛠️ **Tools**:
   - **Nsight Compute** (2025.5+): Deep kernel profiling
   - **Nsight Systems**: Full application timeline
   - **NVIDIA Samples**: Code examples in CUDA Toolkit installation

🖥️ **Development**:
   - **NVCC**: NVIDIA C/C++ Compiler (`nvcc file.cu -o output`)
   - **CMake + CUDA**: For complex projects
   - **Conda/pip**: `cupy` or `pycuda` for Python

---

✨ **Final Note**: This cheatsheet covers CUDA 13.x (2025–2026). For latest features (CUDA 12.4+), check the official guide. Happy GPU programming! 🚀

*Last updated: 2026-01-12 | CUDA 13.1+*

