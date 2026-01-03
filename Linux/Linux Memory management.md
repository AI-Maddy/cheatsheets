**Linux Memory Management Cheat Sheet**  
(focused on modern kernels 5.15–6.12+ as of early 2026 – the concepts that actually matter when writing drivers, debugging OOMs, tuning servers, or understanding container memory behavior)

### 1. Core Concepts – Quick Overview Table

Concept                  | What it is                                      | Managed by             | Typical size / unit     | Key files/commands
------------------------|--------------------------------------------------|------------------------|--------------------------|-----------------------
**Physical pages**      | Smallest unit of memory allocation               | buddy allocator        | 4 KiB (usually)          | /proc/meminfo
**Zones**               | DMA / DMA32 / Normal / HighMem / Movable         | page allocator         | —                        | /proc/zoneinfo
**Buddy allocator**     | Free page management (power-of-2 blocks)         | mm/page_alloc.c        | 4 KiB – 4 MiB+           | /proc/buddyinfo
**Slab / SLUB**         | Object cache for small frequent allocations      | mm/slub.c              | few bytes – few KiB      | /proc/slabinfo
**Page cache**          | File-backed pages (mmap, read/write)             | mm/filemap.c           | —                        | /proc/meminfo Cached
**Anonymous memory**    | Process private memory (heap, stack, anonymous mmap) | mm/memory.c        | —                        | /proc/meminfo AnonPages
**Swap**                | Compressed / zswap + disk swap                   | mm/swapfile.c, zswap   | —                        | swapon -s
**OOM killer**          | Last-resort when memory is exhausted             | mm/oom_kill.c          | —                        | /proc/<pid>/oom_score_adj
**Memory cgroup (cgroups v2)** | Per-container / per-service limits            | mm/memcontrol.c        | —                        | /sys/fs/cgroup/memory.*

### 2. Most Useful /proc and /sys Files (daily debugging)

File / Directory                              | What you get / typical use
----------------------------------------------|-------------------------------------------------------
`/proc/meminfo`                               | High-level summary (MemTotal, MemFree, Cached, SwapTotal, Active(anon), etc.)
`/proc/vmstat`                                | Detailed counters (pgfault, pgmajfault, nr_free_pages, nr_slab_reclaimable, etc.)
`/proc/buddyinfo`                             | Free page blocks per order (buddy allocator fragmentation)
`/proc/slabinfo`                              | Slab cache statistics (active_objs, objects per slab, etc.)
`/proc/pagetypeinfo`                          | Per-zone / per-migratetype page counts (fragmentation info)
`/proc/<pid>/smaps` or `/proc/<pid>/smaps_rollup` | Per-process memory map + PSS / RSS / Private / Shared
`/proc/<pid>/status`                          | Quick summary (VmRSS, VmHWM, HugetlbPages, etc.)
`/sys/kernel/mm/transparent_hugepage/enabled` | always / madvise / never (THP control)
`/sys/kernel/mm/transparent_hugepage/defrag`  | always / defer / defer+madvise / madvise / never
`/proc/sys/vm/overcommit_memory`              | 0 = heuristic, 1 = always allow, 2 = strict (most containers use 1)
`/proc/sys/vm/swappiness`                     | 0–200 (default 60) – how aggressively to swap anon pages
`/proc/sys/vm/vfs_cache_pressure`             | 0–10000 (default 100) – reclaim inode/dentry cache aggressiveness
`/proc/sys/vm/drop_caches`                    | echo 1/2/3 > drop_caches (pagecache / dentries+inode / both) – debugging only!

### 3. Allocation APIs Quick Reference (kernel side)

API                              | Purpose / When to use                              | Can sleep? | GFP flags you usually want
---------------------------------|----------------------------------------------------|------------|-----------------------------
`kmalloc(size, gfp)`             | General small object (< PAGE_SIZE)                 | Depends    | GFP_KERNEL / GFP_ATOMIC
`kzalloc` / `kcalloc`            | Zeroed variant                                     | —          | —
`kmem_cache_alloc(cache, gfp)`   | Slab-allocated object (better for many same-size)  | —          | —
`vmalloc(size)`                  | Virtually contiguous, non-physically contiguous    | Yes        | —
`alloc_pages(gfp, order)`        | Get 2^order contiguous physical pages              | —          | —
`get_zeroed_page(gfp)`           | One zeroed page                                        | —          | —
`dma_alloc_coherent(dev, size, &dma_handle, gfp)` | Coherent DMA memory (for devices) | Yes    | GFP_KERNEL | GFP_DMA32
`memremap()` / `memunmap()`      | ioremap-like but for persistent memory / RAM       | —          | —
`pin_user_pages()`               | Pin user pages for DMA / direct I/O                | Yes        | —

### 4. Common Memory Reclaim & Pressure Signals

Pressure source          | Trigger mechanism                          | Typical symptom / tuning knob
------------------------|--------------------------------------------|--------------------------------
**Direct reclaim**      | Process hits low watermark → synchronous reclaim | High latency, long stalls
**kswapd**              | Background reclaim when below high watermark | Usually invisible
**Direct memory compaction** | When allocation fails due to fragmentation | Can be very expensive
**OOM killer**          | No more reclaim/compaction possible        | Killed process with highest oom_score_adj + badness
**Memory cgroup OOM**   | cgroup memory.max reached                  | Killed inside cgroup (not global OOM)
**PSI (Pressure Stall Info)** | /proc/pressure/memory (since 4.20)     | Monitor avg10/avg60/avg300 for memory pressure

### 5. Modern Tuning Knobs (2025–2026 servers & containers)

Knob / Setting                              | Recommended value (server) | Recommended value (container / workstation)
--------------------------------------------|-----------------------------|--------------------------------------------
`vm.swappiness`                            | 10–60                       | 100 (swap early to avoid OOM)
`vm.dirty_ratio` / `vm.dirty_background_ratio` | 10 / 5                  | 20 / 10
`vm.overcommit_memory`                     | 1                           | 1
`vm.overcommit_ratio`                      | 50–90                       | —
`vm.zone_reclaim_mode`                     | 0 (default)                 | 0
`transparent_hugepage` (sysfs)             | madvise / always            | madvise (safer)
`vm.compaction_proactiveness`              | 20 (default)                | —
`memory cgroup` limits                     | Set memory.max              | Set memory.high + memory.max

### 6. Quick Debugging Workflow (when memory is tight)

```bash
# 1. Where is the memory?
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Cached|Swap|Anon|Active|Inactive"

# 2. Who is using it?
top -o %MEM    # or htop / btop
ps -eo pid,rss,vsz,comm --sort=-rss | head -20

# 3. Per-process detail
for pid in $(pgrep -f myprocess); do cat /proc/$pid/status | grep -E "VmRSS|VmHWM"; done

# 4. Slab cache offenders
sort -k 2 -n /proc/slabinfo | tail -20

# 5. Fragmentation / buddy info
cat /proc/buddyinfo
cat /proc/pagetypeinfo | grep -v "Node.*Unusable"

# 6. Pressure stall info (real pressure)
cat /proc/pressure/memory

# 7. Drop caches (debug only!)
echo 3 > /proc/sys/vm/drop_caches
```

### 7. Modern Rules of Thumb (2026)

- Prefer **GFP_KERNEL** unless atomic context → use **GFP_ATOMIC** / **GFP_NOWAIT**
- Use **slab** (kmem_cache) for repeated same-size allocations
- Avoid **vmalloc** unless > few MiB or you really need virtual contiguity
- Monitor **MemAvailable** (not MemFree) – it includes reclaimable page cache
- In containers → always set **memory.max** + **memory.high** (hard + soft limit)
- THP: **madvise** is safest default in production (avoids huge page fragmentation)
- Use **zswap** (compressed RAM swap) instead of pure disk swap on servers
- Watch **PSI** metrics in monitoring (prometheus node_exporter exposes them)

Good luck debugging memory issues!  
Most real problems come from **slab fragmentation**, **page cache pressure**, **THP + compaction storms**, or **missing cgroup limits** — start with `/proc/meminfo`, `/proc/pressure/memory` and `/proc/slabinfo`.