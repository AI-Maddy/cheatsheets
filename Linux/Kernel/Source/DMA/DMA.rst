**Linux DMA cache handling** + **inter-processor (SMP/multi-core) memory coherence & pitfalls** (kernel perspective, modern kernels 6.1–6.14 era, 2025–2026 reality).

🎓 1. DMA Cache Coherency – Core Concepts

| Concept                          | Meaning / When it matters                                      | Coherent? | Typical Latency / BW Impact | Linux API / Flag                     |
|----------------------------------|----------------------------------------------------------------|-----------|------------------------------|--------------------------------------|
| **Hardware coherent DMA**        | CPU caches & device see identical view without driver flushing | Yes       | Higher setup cost, lower BW  | ``dma_set_mask_and_coherent(..., 64)`` |
| **Non-coherent / streaming DMA** | Driver must explicitly sync CPU ↔ device view                  | No        | Lower latency, higher BW     | ``dma_map_single()``, ``dma_sync_single_*()`` |
| **DMA from device → CPU**        | Device wrote → CPU must see data                               | —         | —                            | ``dma_sync_single_for_cpu()``          |
| **DMA from CPU → device**        | CPU wrote → device must see data                               | —         | —                            | ``dma_sync_single_for_device()``       |
| **Bidirectional streaming**      | Both directions — rare & expensive                             | —         | 🔴 🔴 Avoid if possible            | ``DMA_BIDIRECTIONAL``                  |

**Golden rule 2026**:  
**Never use coherent mappings for large/high-bandwidth data**  
→ Use **streaming** + explicit sync → 2–10× better performance on modern ARM/x86 SoCs.

⭐ 📚 2. Most Important DMA Cache APIs

| Function / Call                                      | Purpose                                              | Direction / When to call                     | Common Mistake |
|------------------------------------------------------|------------------------------------------------------|----------------------------------------------|----------------|
| ``dma_alloc_coherent()``                               | Allocate **coherent** buffer + mapping               | Control descriptors, small rings             | Using it for 100+ MiB buffers |
| ``dma_free_coherent()``                                | Free above                                           | —                                            | Forgetting to pair |
| ``dma_map_single()``                                   | Map **streaming** single buffer                      | CPU → device or device → CPU                 | Not checking ``DMA_MAPPING_ERROR`` |
| ``dma_unmap_single()``                                 | Unmap above                                          | After transfer complete                      | Wrong direction |
| ``dma_sync_single_for_cpu()``                          | Invalidate CPU cache after device write              | Device → CPU (RX)                            | Missing → stale data |
| ``dma_sync_single_for_device()``                       | Flush CPU cache before device read                   | CPU → device (TX)                            | Missing → device sees garbage |
| ``dma_map_sg()`` / ``dma_unmap_sg()``                    | Scatter-gather version (most high-perf drivers)      | Networking, NVMe, GPU, camera                | Not using ``sg_dma_len()`` |
| ``dma_set_mask()`` / ``dma_set_mask_and_coherent()``     | Tell DMA engine max address bits                     | Probe time — prefer 64-bit                   | Falling back to 32-bit |
| ``dma_sync_sg_for_cpu()`` / ``…_for_device()``           | Sync entire scatterlist                              | SG-heavy drivers                             | Partial sync only |

⭐ 🛡️ 3. DMA Direction Enum (Critical for Correctness)

| Direction              | Typical Use                              | Sync Needed? | Cache Action on Sync |
|------------------------|------------------------------------------|--------------|----------------------|
| ``DMA_TO_DEVICE``        | CPU → device (TX, outbound)              | Yes          | Flush / write-back   |
| ``DMA_FROM_DEVICE``      | Device → CPU (RX, inbound)               | Yes          | Invalidate           |
| ``DMA_BIDIRECTIONAL``    | Both directions (rare)                   | Yes          | Flush + invalidate   |
| ``DMA_NONE``             | Debug / placeholder                      | —            | —                    |

💾 4. Inter-Processor (SMP) Memory Coherency & Pitfalls

| Concept / Problem              | Description / Symptom                                      | Fix / 🟢 🟢 Best Practice (2026)                          |
|--------------------------------|------------------------------------------------------------|-----------------------------------------------------|
| **False sharing**              | Two CPUs write different variables in same cache line      | ``__cacheline_aligned`` / separate cache lines        |
| **Store buffer / write combining** | CPU write not immediately visible to other cores       | ``smp_wmb()`` / ``smp_store_release()``                 |
| **Missing memory barrier**     | Reordering → stale data / use-after-free                   | ``smp_mb()``, ``smp_rmb()``, ``smp_wmb()``                |
| **this_cpu_* operations**      | Lockless per-CPU counters                                  | ``this_cpu_inc()``, ``this_cpu_add()`` – no barrier needed |
| **per-CPU data races**         | Accessing per-CPU variable from wrong CPU                  | ``migrate_disable()`` / ``get_cpu()`` → ``put_cpu()``     |
| **Cache invalidation storm**   | Too many IPIs for TLB/cache flush                          | Batch flushes, use ``on_each_cpu()`` sparingly        |
| **Coherent DMA on SMP**        | Device write → all CPU caches invalidated                  | Very expensive on large systems → prefer streaming  |
| **Atomic operations**          | ``cmpxchg``, ``xchg``, ``atomic_*``                              | Implicit full barriers on most architectures        |

⭐ **Essential memory barriers cheat-sheet**

| Barrier              | Ensures                              | Use when                                      |
|----------------------|--------------------------------------|-----------------------------------------------|
| ``smp_mb()``           | Full memory barrier                  | Need total order                              |
| ``smp_wmb()``          | Write-write / write-read order       | Before releasing pointer                      |
| ``smp_rmb()``          | Read-read / read-write order         | After acquiring pointer                       |
| ``smp_store_release()``| Store + release barrier              | Publish pointer safely                        |
| ``smp_load_acquire()`` | Load + acquire barrier               | Consume pointer safely                        |
| ``dma_wmb()`` / ``dma_rmb()`` | DMA-specific (ARM mostly)      | DMA sync points (usually ``dma_sync_*`` better) |

⚡ 5. Quick Reference – High-Performance DMA Driver Pattern

.. code-block:: c

/* Probe / init */
if (pci_set_dma_mask(pdev, DMA_BIT_MASK(64)) ||
    pci_set_consistent_dma_mask(pdev, DMA_BIT_MASK(64)))
    /* fallback to 32-bit or fail gracefully */

pci_set_master(pdev);

/* RX path – streaming, device → CPU */
dma_addr = dma_map_single(&pdev->dev, skb->data, len, DMA_FROM_DEVICE);
if (dma_mapping_error(&pdev->dev, dma_addr)) { … }

/* After device signals done (interrupt / poll) */
dma_sync_single_for_cpu(&pdev->dev, dma_addr, len, DMA_FROM_DEVICE);
dma_unmap_single(&pdev->dev, dma_addr, len, DMA_FROM_DEVICE);

/* TX path – CPU → device */
dma_sync_single_for_device(&pdev->dev, dma_addr, len, DMA_TO_DEVICE);
dma_unmap_single(…);   // after TX complete

🐛 6. Debugging Commands (2026-era)

.. code-block:: bash

================================================================================
🐛 DMA debug (very noisy!)
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



echo 1 > /sys/module/dma_debug/parameters/enable
dmesg | grep dma-debug

================================================================================
⚙️ Cache behavior / false sharing
================================================================================

perf stat -e cache-misses,cache-references ./myapp
perf record -e mem_load_uops_retired.l3_miss,name=l3miss ./myapp

================================================================================
⚙️ IOMMU / DMA mapping stats
================================================================================

cat /proc/iommu/sva_mappings   # or debugfs/iommu/

================================================================================
🐛 Per-CPU variables inspection (crash / ftrace)
================================================================================

crash> per_cpu counters cpu0

**Bottom line 2026**:  
- **Streaming DMA** + **explicit sync** is the performance king  
- **Coherent** only for small control structures  
- **False sharing** and **missing barriers** remain top SMP bugs  
- Use ``this_cpu_*`` and ``smp_*`` barriers religiously in lockless code

🟢 🟢 Good luck with your high-performance DMA / SMP kernel code!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
