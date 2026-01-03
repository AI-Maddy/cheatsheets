**cheatsheet** for **Linux kernel memory management internals** focusing on:

- **Buddy page allocator** (lowest-level physical page management)
- **Slab/SLUB allocator** (object caching on top of buddy)
- **mmap / vm_area_struct** (user virtual memory mappings)

Current as of early 2026 (Linux ~6.12–6.16 era): **SLUB** remains the **default** slab allocator (SLAB deprecated since ~6.5, removed in later versions; SLOB long gone for tiny systems). No fundamental redesign of buddy or mmap, but ongoing refinements (e.g., MTE, large folios, sheaves proposals still experimental/discussion stage in 2025 LSFMM).

### 1. Buddy Page Allocator (mm/page_alloc.c)

Manages physical memory in power-of-2 sized blocks (pages usually 4 KiB).

| Concept                  | Description / Key Details                                                                 |
|--------------------------|--------------------------------------------------------------------------------------------|
| **Unit**                 | struct page (one per physical page)                                                        |
| **Buddy system**         | Free pages grouped by order 0–MAX_ORDER-1 (~11 on x86_64 → 4 MiB max single block)         |
| **Free lists**           | `free_area[order]` array per zone; each has `free_list` + `nr_free`                        |
| **Zones**                | NODE_ZONES → DMA / DMA32 / NORMAL / MOVABLE / HIGHMEM (32-bit)                             |
| **Main allocation**      | `__alloc_pages()` → `get_page_from_freelist()` → try preferred zone → fallback zones      |
| **Key GFP flags**        | `__GFP_DMA`, `__GFP_HIGHMEM`, `__GFP_MOVABLE`, `__GFP_ZERO`, `__GFP_NOWAIT`, `__GFP_RETRY_MAYFAIL` |
| **Watermarks**           | min / low / high per zone; used for throttling / direct reclaim                        |
| **Compaction**           | Moves movable pages to create higher-order contiguous blocks                              |
| **Important functions**  | `alloc_pages(gfp, order)`<br>`__free_pages(page, order)`<br>`__get_free_pages()`           |
| **Per-CPU caches**       | `pcp` (per-cpu-pages): batch of pages per order to reduce zone lock contention             |

**Quick lookup table: order → size**

| Order | Pages | Bytes (4 KiB page) | Typical use case                  |
|-------|-------|---------------------|-----------------------------------|
| 0     | 1     | 4 KiB               | Most slab objects, single pages   |
| 3     | 8     | 32 KiB              | Larger slab pages                 |
| 9     | 512   | 2 MiB               | Huge pages (THP) fallback         |
| 11    | 2048  | 8 MiB               | Very large kernel allocations     |

### 2. SLUB Allocator (mm/slub.c) — Default since ~2.6.23, still in 2026

Replaced SLAB (deprecated) and SLOB (removed). Focus: simplicity, debuggability, low overhead.

| Concept                  | Description / Key Details                                                                 |
|--------------------------|--------------------------------------------------------------------------------------------|
| **Cache**                | `struct kmem_cache` — one per object type/size (created via `kmem_cache_create()`)        |
| **Slab page**            | Physical page(s) from buddy (usually order 0–3); contains many objects                    |
| **Freelist**             | Single linked list per slab page (stored in object metadata or page->freelist)            |
| **Per-CPU**              | Each CPU has `struct kmem_cache_cpu`: `page` (current slab), `freelist`, `tid`            |
| **Node lists**           | Partial / full / empty slabs per NUMA node (`kmem_cache_node`)                            |
| **Main APIs**            | `kmalloc(size, gfp)` → size-indexed cache<br>`kmem_cache_alloc(cache, gfp)`               |
| **Object layout**        | Metadata (freelist pointer + redzone + last bytes tag) embedded or in page struct         |
| **Debug features**       | `CONFIG_SLUB_DEBUG` → redzoning, poisoning, tracking, freelist randomization              |
| **Fastpath**             | CPU freelist non-empty → lockless alloc/free                                              |
| **Slowpath**             | Get new slab from partial list or allocate from buddy → `new_slab()`                      |
| **Key structures**       | `kmem_cache` → `kmem_cache_cpu` → `page` → objects + freelist                             |

**kmalloc size buckets** (common on x86_64, SLUB)

| Request size range       | Cache name     | Object size (approx) |
|--------------------------|----------------|----------------------|
| 1–8 B                    | kmalloc-8      | 8 B                  |
| 9–16 B                   | kmalloc-16     | 16 B                 |
| …                        | …              | …                    |
| 257–512 B                | kmalloc-512    | 512 B                |
| 513 B – 1 KiB            | kmalloc-1k     | 1024 B               |
| Larger                   | kmalloc-*      | up to ~8 KiB         |

**kmalloc large objects** (> ~PAGE_SIZE/2): directly → buddy via `kmalloc_large()`

### 3. mmap / Virtual Memory Area (VMA) Internals (mm/mmap.c)

User process virtual address space management.

| Concept                  | Description / Key Details                                                                 |
|--------------------------|--------------------------------------------------------------------------------------------|
| **VMA**                  | `struct vm_area_struct` — contiguous virtual range with same attributes                   |
| **mm_struct**            | Per-process: owns `mmap` (red-black tree of VMAs), page tables, hiwater_rss, etc.         |
| **Main tree**            | `mm->mm_rb` (RB-tree ordered by vm_start) + `mm->mmap` (linked list)                      |
| **mmap syscall flow**    | `do_mmap()` → `vm_area_struct` alloc → `find_vma()` check overlap → link into tree        |
| **Flags (vm_flags)**     | `VM_READ`, `VM_WRITE`, `VM_EXEC`, `VM_MAY*`, `VM_SHARED`, `VM_GROWSDOWN`, `VM_HUGEPAGE`   |
| **File-backed mmap**     | `vm_file` → `struct file*`, uses `vm_ops->fault()` (usually `filemap_fault()`)            |
| **Anonymous mmap**       | `vm_file = NULL`, uses demand-zero pages or anonymous COW                                 |
| **Page fault handling**  | `__do_fault()` → vma->vm_ops->fault() → alloc page → `handle_mm_fault()`                  |
| **Key functions**        | `do_mmap()` / `do_munmap()`<br>`find_vma()` / `find_vma_intersection()`<br>`vm_brk()`     |
| **Large / THP**          | Transparent Huge Pages: `khugepaged` collapses 4 KiB → 2 MiB anonymously                  |
| **VMA merging**          | Adjacent VMAs with identical attributes/flags/file are merged automatically               |

**Typical VMA layout (x86_64 user space)**

```
0x0000000000000000          ← null page / guard
... mmap_base (randomized)  ← libraries, mmap()
... heap (grows up via brk)
... stack (grows down)
0x00007fffffffffff          ← stack top
0xffff...                   ← kernel (direct map, vmalloc, modules, fixmap)
```

### 4. Quick Comparison: Allocation Paths

| Allocator       | Physically contiguous? | Virtually contiguous? | Typical size     | Use case examples                     | Backend source          |
|-----------------|------------------------|------------------------|------------------|---------------------------------------|--------------------------|
| Buddy           | Yes                    | No (physical)          | 4 KiB –  several MiB | Large DMA, huge pages, slab pages    | Physical RAM            |
| SLUB / kmalloc  | Yes (small)            | Yes                    | ≤ ~8 KiB         | Kernel objects, small buffers        | Buddy pages             |
| vmalloc         | No                     | Yes                    | Any (large)      | Modules, large non-contig buffers    | Buddy pages + PTEs      |
| mmap (anon)     | No                     | Yes                    | Any              | Process heap, large anon mappings    | Demand-zero / swap      |
| mmap (file)     | No                     | Yes                    | Any              | Shared libraries, file mappings      | Page cache              |

### 5. Debugging & Tracing Tips (2026-era)

```bash
# Slab / SLUB stats
cat /proc/slabinfo
slabtop

# Buddy stats per zone
cat /proc/zoneinfo

# Active VMAs of a process
cat /proc/<pid>/maps
cat /proc/<pid>/smaps

# Trace faults & allocations
trace-cmd record -e kmem:* -e mm:* -e anon_fault -e filemap_fault
perf record -e kmem:*u -e page-faults
```

Good luck kernel hacking — start reading `mm/page_alloc.c`, `mm/slub.c`, and `mm/mmap.c` for deepest understanding!