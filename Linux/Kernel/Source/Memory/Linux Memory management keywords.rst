
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **keywords** in **Linux kernel memory management**, each with a concise one-line description (kernel perspective, modern kernels ~6.x):

1. **struct page**  
   Core per-physical-page metadata structure tracking flags, reference count, mapping, and buddy/slab state.

2. **Buddy allocator**  
   Power-of-two page merging/splitting system that manages physically contiguous free memory in zones.

3. **Zone**  
   Logical division of physical memory (DMA, DMA32, NORMAL, MOVABLE, HIGHMEM) with separate watermarks and allocation rules.

4. **Watermarks** (min/low/high)  
   Thresholds per zone that trigger kswapd reclaim, direct reclaim, or allocation throttling.

5. **GFP flags** (Get Free Page)  
   Allocation modifiers (__GFP_DMA, __GFP_HIGHMEM, __GFP_MOVABLE, __GFP_ZERO, __GFP_NOWAIT, __GFP_NOFAIL, etc.).

6. **mm_struct**  
   Per-process memory descriptor containing page tables, VMA tree, RSS statistics, and memory policy.

7. **vm_area_struct (VMA)**  
   Represents one contiguous virtual memory region with its start/end address, flags, file backing, and operations.

8. **Page tables**  
   Multi-level hardware tables (PML4/PDP/PD/PT on x86_64) mapping virtual to physical addresses.

9. **Page fault**  
   CPU exception handled by do_page_fault() → handle_mm_fault() → vma->vm_ops->fault() to bring in or allocate pages.

10. **Demand paging**  
   Lazy allocation: pages are only allocated and loaded on first access (zero pages for anon, read from disk for file-backed).

11. **Anonymous pages**  
   Memory without backing file (heap, stack, anonymous mmap) — managed via swap when under pressure.

12. **Page cache**  
   Unified cache of file-backed pages shared across processes (managed by address_space → radix tree).

13. **SLUB allocator**  
   Default slab allocator using per-CPU freelists and minimal metadata for fast small-object allocation.

14. **kmem_cache**  
   SLUB cache descriptor for a specific object type/size (created by kmem_cache_create()).

15. **kmalloc / kfree**  
   General-purpose kernel small-object allocation/deallocation using size-indexed SLUB caches.

16. **vmalloc**  
   Virtually contiguous but physically non-contiguous allocation using a separate address space and page tables.

17. **Transparent Huge Pages (THP)**  
   Automatic promotion of 4 KiB pages to 2 MiB (or 1 GiB) pages to reduce TLB misses (khugepaged daemon).

18. **kswapd**  
   Per-node background reclaim thread that wakes when zone free memory falls below high watermark.

19. **Direct reclaim**  
   Synchronous memory reclaim performed by the allocating process when allocation cannot wait.

20. **LRU lists**  
   Active/inactive (file + anon) page lists used by page replacement to decide which pages to evict.

21. **Swap**  
   Mechanism to move anonymous and swapcache pages to disk when RAM is scarce (swap_map, swap_info_struct).

22. **memcg (Memory cgroup)**  
   Per-cgroup memory accounting, limiting, and reclaim (used heavily in containers).

23. **NUMA node**  
   Memory locality domain; allocation prefers local node unless __GFP_THISNODE or policy overrides.

24. **Memory policy**  
   NUMA-aware allocation strategy (MPOL_DEFAULT, MPOL_PREFERRED, MPOL_BIND, MPOL_INTERLEAVE).

25. **Compaction**  
   Page migration to create physically contiguous free blocks for higher-order allocations.

26. **Migrate pages**  
   Moving page contents to new physical location (used by compaction, NUMA balancing, CMA).

27. **CMA (Contiguous Memory Allocator)**  
   Reserved memory pool for guaranteed large physically contiguous allocations (used by GPU, camera, etc.).

28. **Direct map**  
   Kernel linear mapping of all physical RAM (usually at high addresses) used for quick phys ↔ virt translation.

29. **vmalloc area**  
   Kernel virtual address range for vmalloc, modules, and ioremap (non-linear physical mappings).

30. **Fixmap / percpu**  
   Permanent and per-CPU fixed virtual addresses used for special kernel mappings (e.g., per-CPU variables).

⭐ These 30 keywords cover the backbone of Linux memory management from physical page allocation to user virtual memory and reclaim.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
