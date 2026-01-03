**cheatsheet** for **DMA (Direct Memory Access) in the Linux kernel** (as of early 2026, kernels ~6.12–6.16), focusing on the modern **DMA API** (`include/linux/dma-mapping.h`) together with patterns for writing **low-latency, high-bandwidth device drivers** (e.g. networking, storage, accelerators, FPGA PCIe cards, high-speed ADC/DAC, GPU-related, NVMe).

### 1. DMA API Core Concepts

| Concept                  | Description / When to use                                                                 | Coherent? | Typical Latency / Bandwidth Impact |
|--------------------------|-------------------------------------------------------------------------------------------|-----------|-------------------------------------|
| **Coherent DMA**         | CPU & device see the same data without extra flushing/invalidation. Expensive, often page-aligned | Yes       | Higher latency, lower BW overhead   |
| **Streaming DMA**        | One-directional transfers; requires explicit sync (map → use → sync → unmap)             | No        | Lower latency & higher BW possible  |
| **dma_addr_t**           | Bus/device-visible address (may differ from physical/CPU virt addr on IOMMU platforms)    | —         | —                                   |
| **IOMMU / DMA remapping**| Translates device addresses → physical RAM; enables >4 GB DMA on 32-bit capable devices   | —         | Adds ~10–50 ns latency (modern HW)  |
| **Scatter-Gather (SG)**  | Handles non-contiguous buffers via `struct scatterlist`                                   | —         | Essential for high BW (>10 Gbit/s)  |

### 2. Key DMA Allocation & Mapping Functions

| Function / Call                              | Purpose                                                                 | Coherent? | GFP flags allowed? | Notes / Best practice for low-latency/high-BW |
|----------------------------------------------|-------------------------------------------------------------------------|-----------|--------------------|-----------------------------------------------|
| `dma_alloc_coherent(dev, size, &dma_handle, gfp)` | Alloc coherent buffer + map                                            | Yes       | GFP_KERNEL / ATOMIC| Use for control descriptors, rings. Avoid for large data (> few pages) |
| `dma_free_coherent(dev, size, cpu_addr, dma_handle)` | Free above                                                     | Yes       | —                  | Always pair with alloc                        |
| `dma_set_mask_and_coherent(dev, mask)`       | Set both streaming & coherent DMA mask (64-bit preferred)               | —         | —                  | Call in probe(); fail gracefully if !64-bit   |
| `dma_map_single(dev, ptr, size, DMA_TO_DEVICE)` | Map single kernel buffer for device write (→ device)               | No        | —                  | Fastest single-buffer path; check return != DMA_MAPPING_ERROR |
| `dma_unmap_single(dev, dma_addr, size, dir)` | Unmap above                                                            | No        | —                  | Required before CPU reuse                     |
| `dma_sync_single_for_cpu/dev(...)`           | Flush/invalidate cache for streaming mapping                            | No        | —                  | Minimize calls; group operations              |
| `dma_map_sg(dev, sglist, nents, dir)`        | Map scatterlist (most common for high BW)                               | No        | —                  | Preferred for networking/storage drivers      |
| `dma_unmap_sg(...)`                          | Unmap scatter-gather list                                               | No        | —                  | —                                             |
| `dma_pool_create(...)`                       | Create pool of small coherent objects (descriptors)                    | Yes       | —                  | Better than many dma_alloc_coherent() calls   |
| `dma_pool_alloc(pool, gfp, &dma_handle)`     | Allocate from pool                                                      | Yes       | Yes                | Low overhead for frequent small allocations   |

**DMA direction** enum values (critical for correctness & optimization):

- `DMA_BIDIRECTIONAL`
- `DMA_TO_DEVICE`     (CPU → device)
- `DMA_FROM_DEVICE`   (device → CPU)
- `DMA_NONE`          (debug only)

### 3. Low-Latency + High-Bandwidth Driver Patterns (2025–2026 era)

| Goal / Scenario                              | Recommended Pattern / Technique                                                                 | Why it helps latency & bandwidth                                   | Example drivers (kernel tree) |
|----------------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-------------------------------|
| **Descriptor rings / queues**                | Use `dma_pool` for descriptors + coherent or streaming for data payloads                         | Descriptors coherent → no sync; data streaming → optimal cache use | mlx5, ixgbe, nvme, amdgpu     |
| **Zero-copy / high BW networking**           | `build_skb()` + `dma_map_sg()` on user pages (or `page_pool`)                                   | Avoid memcpy; multi-page SG lists for jumbo frames/GRO             | mlx5, ice, i40e, virtio-net   |
| **Ultra-low latency (FPGA / NIC <5 µs)**     | Pre-allocate & pre-map buffers; use polling instead of interrupts; `dmaengine` prep + submit     | Avoid interrupt + scheduler latency; fixed buffers reduce setup    | fpga-mgr, AXI DMA, some DPDK-like kernel drivers |
| **High bandwidth (>100 Gbit/s or GPU/accel)**| Large SG lists + `dma_map_sg()`; use huge pages if device supports; avoid coherent for bulk data | Maximizes PCIe TLP efficiency; reduces IOMMU TLB pressure          | nvme, mlx5, amdgpu, hisi_sas  |
| **Cache-line alignment**                     | Align buffers & descriptors to 64/128 bytes; avoid false sharing                                | Prevents cache ping-pong between CPU cores & device DMA            | Most high-perf drivers        |
| **Interrupt coalescing + napi**              | Moderate coalescing + busy-poll / NAPI gro polling                                              | Reduces interrupt rate while keeping latency acceptable            | mlx5, ice                     |
| **Polling mode / busy-wait**                 | Use `dmaengine` tx/rx submit + poll completion status in tight loop                             | Sub-µs tail latency for critical paths (trading CPU %)             | Custom FPGA drivers, some audio/ADC |
| **Avoid coherent for large data**            | Use streaming + explicit `dma_sync_*` only when needed                                          | Coherent often forces write-back / uncached → big BW penalty       | Almost all high-BW drivers    |
| **IOMMU bypass / passthrough**               | Enable `iommu=pt` kernel cmdline or driver-specific no-iommu mode                               | Removes IOMMU translation latency (~20–100 ns per transaction)     | Some FPGA & storage drivers   |

### 4. Quick Reference: DMAEngine (for offload engines)

Used when hardware has dedicated DMA controller (not PCIe master DMA).

```c
struct dma_chan *chan = dma_request_chan(dev, "rx");     // or "tx"
struct dma_async_tx_descriptor *tx;
dma_cookie_t cookie;

tx = dmaengine_prep_slave_sg(chan, sglist, nents, DMA_DEV_TO_MEM, flags);
cookie = dmaengine_submit(tx);
dma_async_issue_pending(chan);

// Later: dmaengine_terminate_all(chan); or wait via dmaengine_tx_status()
```

### 5. Common Mistakes to Avoid (2026 perspective)

- Forgetting `dma_set_mask_and_coherent()` → 32-bit fallback → fails on >4 GB systems
- Using coherent mappings for large/high-bandwidth data → severe performance loss
- Not checking `dma_mapping_error()` after map calls
- Unmapping with wrong direction or size
- Sharing cache lines between CPU-written control + device DMA data
- Excessive `dma_sync_single_*` calls in fast path

### 6. Debugging & Tools

```bash
# DMA debug (very noisy!)
echo 8192 > /sys/module/dmaengine/parameters/debug
dmesg -w | grep dma

# IOMMU / mapping stats
cat /proc/iommu/sva_mappings   # or /sys/kernel/debug/iommu/

# perf for DMA stalls / PCIe
perf record -e pci:* -e dma:* -- sleep 10
perf report
```

**Best starting points** in kernel source (6.x era):

- `Documentation/core-api/dma-api-howto.rst` (still the canonical guide)
- `include/linux/dma-mapping.h`
- `drivers/net/ethernet/intel/ice/`, `drivers/net/ethernet/mellanox/mlx5/`, `drivers/nvme/host/`
- `drivers/dma/dmaengine.h` for offload engines

Good luck writing high-performance DMA drivers!