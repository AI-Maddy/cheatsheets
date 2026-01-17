====================================================================
Linux Memory Management — Complete Guide
====================================================================

**Comprehensive coverage of Linux kernel memory subsystem:** Physical memory, virtual memory, page tables, allocators, caches, zones, OOM, DMA, and userspace interfaces.

**Current as of:** Linux 6.12–6.16 (January 2026)  
**Architecture focus:** x86_64 (with ARM64 notes where applicable)

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**Linux Memory Management** is the subsystem responsible for managing physical RAM, virtual address spaces, page allocation, object caching, and memory pressure handling.

**Key Components:**

.. code-block:: text

   Component           Purpose                          Main Files
   ──────────────────  ───────────────────────────────  ─────────────────────
   Buddy Allocator     Physical page allocation         mm/page_alloc.c
   SLUB Allocator      Object caching (kmalloc)         mm/slub.c
   Page Cache          File-backed pages                mm/filemap.c
   Anonymous Memory    Process heap/stack               mm/memory.c
   Virtual Memory      Process address spaces (VMA)     mm/mmap.c
   Swap                Compressed/disk swap             mm/swapfile.c, zswap
   OOM Killer          Out-of-memory handling           mm/oom_kill.c
   Cgroups             Per-container memory limits      mm/memcontrol.c
   Huge Pages          2 MiB/1 GiB pages (THP)          mm/huge_memory.c
   DMA                 Device memory access             kernel/dma/

**Memory Layout (x86_64 userspace):**

.. code-block:: text

   0x00000000_00000000  ← NULL page (trap on access)
   0x55555555_0000      ← Text (code), PIE randomized
   0x55555555_8000      ← Data, BSS
   0x55555556_0000      ← Heap (brk), grows up
   ...
   0x7ffff7dd_0000      ← Shared libraries (mmap)
   0x7fffffff_e000      ← Stack, grows down
   0xffffffff_ff600000  ← vdso/vsyscall
   
   0xffff8880_00000000  ← Kernel direct map (48-bit physical)
   0xffffc900_00000000  ← vmalloc area
   0xffffffffa0000000   ← Kernel modules

**Quick Diagnostic Commands:**

.. code-block:: bash

   # System-wide memory status
   cat /proc/meminfo
   cat /proc/vmstat
   
   # Per-process memory usage
   cat /proc/<pid>/status | grep Vm
   cat /proc/<pid>/smaps_rollup
   
   # Allocator statistics
   cat /proc/buddyinfo      # Buddy allocator fragmentation
   cat /proc/slabinfo       # SLUB object caches
   cat /proc/zoneinfo       # Memory zones, watermarks
   
   # Pressure monitoring (PSI)
   cat /proc/pressure/memory
   
   # Memory cgroup limits
   cat /sys/fs/cgroup/memory.max
   cat /sys/fs/cgroup/memory.current

================================================================================
1. Physical Memory Management
================================================================================

**1.1 Memory Zones**
---------------------

Linux divides physical RAM into **zones** based on hardware constraints and usage:

.. code-block:: text

   Zone          Address Range (x86_64)       Usage
   ────────────  ───────────────────────────  ─────────────────────────────
   ZONE_DMA      0 – 16 MiB                   ISA DMA devices (<16MB)
   ZONE_DMA32    16 MiB – 4 GiB               32-bit DMA devices
   ZONE_NORMAL   4 GiB – MAX_PHYSMEM          Normal allocations
   ZONE_MOVABLE  (dynamic)                    Hotpluggable, CMA, huge pages
   ZONE_DEVICE   (special)                    Persistent memory (PMEM)

**ARM64 zones:**

.. code-block:: text

   ZONE_DMA      0 – 1 GiB (or CONFIG_ZONE_DMA_BITS)
   ZONE_DMA32    1 GiB – 4 GiB
   ZONE_NORMAL   4 GiB – MAX_PHYSMEM

**Check zones:**

.. code-block:: bash

   cat /proc/zoneinfo

**Example output:**

.. code-block:: text

   Node 0, zone   Normal
     pages free     1234567
           min      2048
           low      3072
           high     4096
           spanned  8388608
           present  8388608
           managed  8123456
     nr_free_pages 1234567
     nr_zone_active_anon 500000
     nr_zone_inactive_anon 100000

**Watermarks:**
- **min:** Emergency reserve (atomic allocations only)
- **low:** kswapd wakes up, starts background reclaim
- **high:** kswapd goes back to sleep

**1.2 Buddy Page Allocator**
------------------------------

Manages physical memory in power-of-2 sized blocks (**orders** 0–MAX_ORDER-1, typically 0–10).

**Key Concepts:**

.. code-block:: text

   Order  Pages  Size (4 KiB pages)  Typical Use
   ─────  ─────  ──────────────────  ───────────────────────────
   0      1      4 KiB               Single pages, SLUB slabs
   1      2      8 KiB               Small contiguous buffers
   2      4      16 KiB              DMA buffers
   3      8      32 KiB              Large slab pages
   9      512    2 MiB               Transparent Huge Pages (THP)
   10     1024   4 MiB               Large DMA, reservations

**Buddy Algorithm:**

When freeing a page of order N, the kernel checks if its "buddy" (adjacent block of same size) is also free. If yes, merge into order N+1. Repeat recursively.

**Check fragmentation:**

.. code-block:: bash

   cat /proc/buddyinfo

**Example:**

.. code-block:: text

   Node 0, zone   Normal    4096   2048   1024    512    256    128     64     32     16      8      4
                           order0 order1 order2 order3 order4 order5 order6 order7 order8 order9 order10

**API Functions:**

.. code-block:: c

   // Allocate 2^order contiguous pages
   struct page *alloc_pages(gfp_t gfp, unsigned int order);
   
   // Allocate single page, return virtual address
   unsigned long __get_free_page(gfp_t gfp);
   unsigned long get_zeroed_page(gfp_t gfp);
   
   // Free pages
   void __free_pages(struct page *page, unsigned int order);
   void free_pages(unsigned long addr, unsigned int order);

**GFP Flags (Get Free Pages):**

.. code-block:: text

   Flag                  Meaning
   ────────────────────  ───────────────────────────────────────────
   GFP_KERNEL            Standard kernel allocation (can sleep)
   GFP_ATOMIC            Cannot sleep (interrupt context)
   GFP_USER              User allocation
   GFP_NOWAIT            Don't wait, don't reclaim
   __GFP_DMA             Allocate from ZONE_DMA
   __GFP_DMA32           Allocate from ZONE_DMA32
   __GFP_MOVABLE         Allocate from ZONE_MOVABLE (anti-frag)
   __GFP_ZERO            Zero the allocated memory
   __GFP_RETRY_MAYFAIL   Retry allocation, may fail
   __GFP_NOFAIL          Never fail (dangerous!)

**1.3 Per-CPU Page Cache**
----------------------------

To reduce lock contention on zone->lock, each CPU maintains a **per-CPU page cache (PCP)** of recently freed pages.

**Structure:**

.. code-block:: c

   struct per_cpu_pages {
       int count;        // Number of pages in lists
       int high;         // High watermark (return to buddy)
       int batch;        // Batch size for refilling
       struct list_head lists[MIGRATE_PCPTYPES];
   };

**Benefits:**
- Fast allocation (no zone lock)
- Improved cache locality
- Reduced TLB flushes

================================================================================
2. SLUB Allocator (Object Cache)
================================================================================

**2.1 Overview**
-----------------

**SLUB** (default since 2.6.23, only allocator in 6.12+) provides **object caching** for frequently allocated/freed objects.

**Key Features:**
- Fast allocation from per-CPU freelist (lockless)
- Reduced internal fragmentation vs direct buddy
- Debug features (redzoning, poisoning, tracking)

**Architecture:**

.. code-block:: text

   kmem_cache ──→ kmem_cache_cpu (per-CPU)
                   │
                   ├─→ page (current slab)
                   │    ├─→ object 1 (free)
                   │    ├─→ object 2 (free)
                   │    └─→ object 3 (allocated)
                   │
                   └─→ freelist (linked list of free objects)

**2.2 kmalloc Size Buckets**
------------------------------

.. code-block:: text

   Request Size    Cache Name       Object Size  Pages per Slab
   ──────────────  ───────────────  ───────────  ──────────────
   1–8 bytes       kmalloc-8        8 B          1 page
   9–16 bytes      kmalloc-16       16 B         1 page
   17–32 bytes     kmalloc-32       32 B         1 page
   33–64 bytes     kmalloc-64       64 B         1 page
   65–96 bytes     kmalloc-96       96 B         1 page
   97–128 bytes    kmalloc-128      128 B        1 page
   129–192 bytes   kmalloc-192      192 B        2 pages
   193–256 bytes   kmalloc-256      256 B        1 page
   ...             ...              ...          ...
   4097–8192 bytes kmalloc-8k       8192 B       2 pages

**Large allocations (>8 KiB):** Direct buddy via ``kmalloc_large()``

**2.3 API Functions**
----------------------

.. code-block:: c

   // General allocation
   void *kmalloc(size_t size, gfp_t flags);
   void *kzalloc(size_t size, gfp_t flags);  // Zeroed
   void *kcalloc(size_t n, size_t size, gfp_t flags);  // Array
   
   // Free
   void kfree(const void *ptr);
   
   // Create custom cache
   struct kmem_cache *kmem_cache_create(const char *name, 
                                         unsigned int size,
                                         unsigned int align,
                                         slab_flags_t flags,
                                         void (*ctor)(void *));
   
   // Allocate from custom cache
   void *kmem_cache_alloc(struct kmem_cache *cachep, gfp_t flags);
   void kmem_cache_free(struct kmem_cache *cachep, void *objp);
   
   // Destroy cache
   void kmem_cache_destroy(struct kmem_cache *cachep);

**Example: Custom Cache**

.. code-block:: c

   static struct kmem_cache *my_cache;
   
   struct my_struct {
       int id;
       char data[64];
   };
   
   static int __init my_init(void) {
       my_cache = kmem_cache_create("my_cache",
                                     sizeof(struct my_struct),
                                     0,  // alignment
                                     SLAB_HWCACHE_ALIGN,
                                     NULL);  // no constructor
       if (!my_cache)
           return -ENOMEM;
       return 0;
   }
   
   struct my_struct *obj = kmem_cache_alloc(my_cache, GFP_KERNEL);
   // Use obj...
   kmem_cache_free(my_cache, obj);

**2.4 Slab Debugging**
-----------------------

Enable at boot: ``slub_debug=FZPU``

.. code-block:: text

   Flag  Meaning
   ────  ────────────────────────────────────────────
   F     Sanity checks (freelist validation)
   Z     Red zoning (detect overruns)
   P     Poisoning (fill with 0x5a, detect use-after-free)
   U     User tracking (track alloc/free call sites)
   T     Trace (print every allocation)

**Check slab info:**

.. code-block:: bash

   cat /proc/slabinfo
   
   # Example output:
   # slabinfo - version: 2.1
   # name            <active_objs> <num_objs> <objsize> <objperslab>
   kmalloc-8         12345 12800    8   512
   kmalloc-192       5678  6000  192    21
   dentry            98765 100000 192    21

================================================================================
3. Virtual Memory (VMA) Management
================================================================================

**3.1 Process Address Space**
-------------------------------

Each process has a ``struct mm_struct`` describing its virtual address space.

**Key fields:**

.. code-block:: c

   struct mm_struct {
       struct vm_area_struct *mmap;        // VMA list
       struct rb_root mm_rb;               // VMA red-black tree
       pgd_t *pgd;                         // Page Global Directory (top-level page table)
       atomic_t mm_users;                  // Number of users (threads)
       atomic_t mm_count;                  // Reference count
       unsigned long start_code, end_code; // Text segment
       unsigned long start_data, end_data; // Data segment
       unsigned long start_brk, brk;       // Heap
       unsigned long start_stack;          // Stack
       unsigned long arg_start, arg_end;   // Command-line arguments
       unsigned long env_start, env_end;   // Environment
   };

**3.2 Virtual Memory Areas (VMA)**
------------------------------------

A **VMA** represents a contiguous range of virtual addresses with uniform properties.

.. code-block:: c

   struct vm_area_struct {
       unsigned long vm_start;          // Start address (inclusive)
       unsigned long vm_end;            // End address (exclusive)
       struct vm_area_struct *vm_next;  // Linked list
       struct mm_struct *vm_mm;         // Parent mm_struct
       pgprot_t vm_page_prot;           // Protection bits
       unsigned long vm_flags;          // Flags (VM_READ, VM_WRITE, ...)
       struct file *vm_file;            // Backing file (NULL if anon)
       const struct vm_operations_struct *vm_ops;  // Operations
   };

**Common vm_flags:**

.. code-block:: text

   Flag               Meaning
   ─────────────────  ──────────────────────────────────────────
   VM_READ            Readable
   VM_WRITE           Writable
   VM_EXEC            Executable
   VM_SHARED          Shared mapping (vs private/COW)
   VM_MAYREAD         May be made readable
   VM_MAYWRITE        May be made writable
   VM_MAYEXEC         May be made executable
   VM_GROWSDOWN       Stack (grows downward)
   VM_GROWSUP         Heap (grows upward)
   VM_HUGEPAGE        Eligible for Transparent Huge Pages
   VM_NOHUGEPAGE      Ineligible for THP
   VM_LOCKED          Pages locked in memory (mlock)

**3.3 mmap() System Call Flow**
---------------------------------

.. code-block:: text

   User: mmap(addr, len, prot, flags, fd, offset)
       │
       ▼
   sys_mmap() → ksys_mmap_pgoff()
       │
       ▼
   do_mmap() → get_unmapped_area() (find free space)
       │
       ▼
   mmap_region() → vma_merge() or vm_area_alloc()
       │
       ▼
   vma_link() → insert into RB-tree & linked list
       │
       ▼
   Return virtual address to userspace

**Page fault flow (demand paging):**

.. code-block:: text

   User accesses unmapped address
       │
       ▼
   Page Fault → do_page_fault() (arch-specific)
       │
       ▼
   handle_mm_fault() → __handle_mm_fault()
       │
       ├─→ Anon page: do_anonymous_page() → alloc_zeroed_page()
       │
       └─→ File page: do_fault() → vma->vm_ops->fault()
                       (e.g., filemap_fault() for page cache)
       │
       ▼
   Allocate page, update PTE, return to userspace

**3.4 Example: /proc/\<pid\>/maps**
--------------------------------------

.. code-block:: bash

   cat /proc/self/maps

.. code-block:: text

   55555555_0000-55555555_8000 r-xp 00000000 08:01 123456  /bin/bash  # Text
   55555575_7000-55555575_8000 r--p 00007000 08:01 123456  /bin/bash  # Read-only data
   55555575_8000-55555575_c000 rw-p 00008000 08:01 123456  /bin/bash  # Data/BSS
   55555575_c000-55555577_0000 rw-p 00000000 00:00 0       [heap]     # Heap
   7ffff7dd_0000-7ffff7dd_2000 r--p 00000000 08:01 234567  /lib/libc.so.6
   7ffff7dd_2000-7ffff7f4_7000 r-xp 00002000 08:01 234567  /lib/libc.so.6
   7ffffff_de000-7fffffff_ff00 rw-p 00000000 00:00 0       [stack]    # Stack

**Column meanings:**
- **Address range:** vm_start–vm_end
- **Perms:** r/w/x/p (private) or s (shared)
- **Offset:** File offset (0 for anon)
- **Device:** Major:minor device number
- **Inode:** File inode
- **Path:** File path or special ([heap], [stack], [vdso])

================================================================================
4. Page Tables & Translation
================================================================================

**4.1 Page Table Hierarchy (x86_64, 4-level)**
------------------------------------------------

.. code-block:: text

   Virtual Address (48 bits):
   
   47      39 38      30 29      21 20      12 11         0
   ┌─────────┬─────────┬─────────┬─────────┬──────────────┐
   │  PML4   │   PDP   │   PD    │   PT    │    Offset    │
   └─────────┴─────────┴─────────┴─────────┴──────────────┘
      9 bits    9 bits    9 bits    9 bits      12 bits
   
   Translation:
   1. CR3 → PML4 table (Page Map Level 4)
   2. PML4[47:39] → PDP table (Page Directory Pointer)
   3. PDP[38:30]  → PD table (Page Directory)
   4. PD[29:21]   → PT table (Page Table)
   5. PT[20:12]   → Physical page frame (PFN)
   6. Offset[11:0] → Byte within page (4 KiB)

**5-level paging (recent CPUs):** Adds PML5 (57-bit VA)

**ARM64 (4 KiB pages, 48-bit VA):**

.. code-block:: text

   47      39 38      30 29      21 20      12 11         0
   ┌─────────┬─────────┬─────────┬─────────┬──────────────┐
   │   L0    │   L1    │   L2    │   L3    │    Offset    │
   └─────────┴─────────┴─────────┴─────────┴──────────────┘

**4.2 Page Table Entry (PTE) Flags**
--------------------------------------

.. code-block:: text

   Bit   x86_64 Flag      Meaning
   ────  ────────────────  ────────────────────────────────────
   0     _PAGE_PRESENT     Page is in memory (not swapped)
   1     _PAGE_RW          Writable (0 = read-only)
   2     _PAGE_USER        User-accessible (0 = kernel-only)
   3     _PAGE_PWT         Write-through caching
   4     _PAGE_PCD         Cache disabled
   5     _PAGE_ACCESSED    Page accessed (set by CPU)
   6     _PAGE_DIRTY       Page modified (set by CPU)
   7     _PAGE_PSE         Page Size Extension (2 MiB/1 GiB page)
   8     _PAGE_GLOBAL      Global page (TLB not flushed on CR3 write)
   9-11  Available         Software use
   12-51 PFN               Physical Frame Number (40 bits)
   63    _PAGE_NX          No Execute (NX bit)

**4.3 Huge Pages**
-------------------

**Traditional Huge Pages (hugetlbfs):**

.. code-block:: bash

   # Mount hugetlbfs
   mount -t hugetlbfs none /mnt/huge
   
   # Allocate 1024 × 2 MiB huge pages (2 GiB total)
   echo 1024 > /proc/sys/vm/nr_hugepages
   
   # Check allocation
   cat /proc/meminfo | grep Huge

**Transparent Huge Pages (THP):**

Automatically promotes 4 KiB pages → 2 MiB pages for anonymous memory.

.. code-block:: bash

   # Check THP status
   cat /sys/kernel/mm/transparent_hugepage/enabled
   # [always] madvise never
   
   # Check statistics
   cat /proc/vmstat | grep thp_
   # thp_fault_alloc 12345
   # thp_fault_fallback 678
   # thp_collapse_alloc 500

**khugepaged:** Background daemon that collapses 512 × 4 KiB pages → 1 × 2 MiB page.

================================================================================
5. Page Cache & File-Backed Memory
================================================================================

**5.1 Page Cache Overview**
-----------------------------

Caches file contents in memory to avoid disk I/O.

**Key Operations:**
- **Read:** ``filemap_read()`` → check page cache → disk read if miss
- **Write:** ``filemap_write()`` → update page cache → writeback daemon flushes to disk
- **mmap:** ``filemap_fault()`` → allocate page cache page, map into process

**Check page cache usage:**

.. code-block:: bash

   cat /proc/meminfo | grep Cached
   # Cached: 8192000 kB (file-backed pages)

**5.2 Writeback & Dirty Pages**
---------------------------------

**Dirty pages:** Modified file-backed pages not yet written to disk.

**Writeback daemons:**
- **flush threads (one per device):** Periodically flush dirty pages
- **kswapd:** Reclaims pages when memory pressure occurs

**Tuning:**

.. code-block:: bash

   # Maximum % of RAM for dirty pages before blocking writes
   cat /proc/sys/vm/dirty_ratio  # Default: 20
   
   # Start background writeback at this % of RAM
   cat /proc/sys/vm/dirty_background_ratio  # Default: 10
   
   # Writeback interval (centiseconds)
   cat /proc/sys/vm/dirty_writeback_centisecs  # Default: 500 (5 sec)

**Manual sync:**

.. code-block:: bash

   sync  # Flush all dirty pages

================================================================================
6. Memory Reclaim & OOM Killer
================================================================================

**6.1 Memory Reclaim Mechanisms**
-----------------------------------

When memory pressure occurs, kernel reclaims pages:

.. code-block:: text

   Mechanism            Trigger                  Action
   ───────────────────  ───────────────────────  ─────────────────────────
   kswapd               Low watermark reached    Background reclaim
   Direct reclaim       Allocation fails         Synchronous reclaim (blocks caller)
   Compaction           Fragmentation prevents   Move movable pages to create contiguous blocks
                        high-order allocation
   OOM killer           All reclaim failed       Kill process with highest badness score

**kswapd wake-up:**

.. code-block:: text

   Zone free pages
   
   High ──────────── kswapd sleeps
        ▲
        │ kswapd reclaims
   Low  ──────────── kswapd wakes up
        │
        │ Direct reclaim
   Min  ──────────── Atomic allocations only

**6.2 Page Reclaim Priority**
-------------------------------

.. code-block:: text

   Priority  Reclaim Strategy
   ────────  ────────────────────────────────────────────
   High      Reclaim clean page cache pages (easy)
   Medium    Reclaim dirty page cache pages (writeback)
   Low       Reclaim anonymous pages (swap out)
   Last      OOM killer

**Swappiness:** Controls balance between page cache vs anon reclaim.

.. code-block:: bash

   cat /proc/sys/vm/swappiness  # 0–200, default 60
   # 0   = avoid swapping anon pages (prefer page cache reclaim)
   # 60  = balanced
   # 100 = aggressive swap (prefer keeping page cache)

**6.3 OOM Killer**
-------------------

When all reclaim attempts fail, kernel invokes **OOM killer** to free memory.

**Badness score calculation:**

.. code-block:: c

   badness = (RSS + swap usage) / total_RAM * 1000 + oom_score_adj

**oom_score_adj range:** -1000 to +1000

- **-1000:** Never kill (protected)
- **0:** Normal
- **+1000:** Always prefer killing this process

**Set OOM score:**

.. code-block:: bash

   echo 500 > /proc/<pid>/oom_score_adj  # Make more likely to kill
   echo -500 > /proc/<pid>/oom_score_adj # Protect from OOM

**Check current badness:**

.. code-block:: bash

   cat /proc/<pid>/oom_score

**OOM killer log:**

.. code-block:: bash

   dmesg | grep -i "out of memory"
   # [12345.678] Out of memory: Killed process 1234 (myapp) total-vm:2097152kB

================================================================================
7. DMA & Coherent Memory
================================================================================

**7.1 DMA Zones**
------------------

Some devices can only DMA to specific physical address ranges.

.. code-block:: text

   Zone          Address Range    Devices
   ────────────  ───────────────  ──────────────────────────
   ZONE_DMA      0–16 MiB         ISA DMA (<16 MB)
   ZONE_DMA32    0–4 GiB          32-bit PCI devices
   ZONE_NORMAL   4 GiB+           64-bit DMA capable devices

**7.2 DMA APIs**
-----------------

**Coherent DMA (CPU/device see same data):**

.. code-block:: c

   void *dma_alloc_coherent(struct device *dev, size_t size,
                            dma_addr_t *dma_handle, gfp_t gfp);
   void dma_free_coherent(struct device *dev, size_t size,
                          void *cpu_addr, dma_addr_t dma_handle);

**Streaming DMA (explicit sync required):**

.. code-block:: c

   dma_addr_t dma_map_single(struct device *dev, void *ptr,
                             size_t size, enum dma_data_direction dir);
   void dma_unmap_single(struct device *dev, dma_addr_t dma_addr,
                         size_t size, enum dma_data_direction dir);

**Direction:**

.. code-block:: c

   DMA_TO_DEVICE      // CPU → device (write)
   DMA_FROM_DEVICE    // Device → CPU (read)
   DMA_BIDIRECTIONAL  // Both directions

**Example:**

.. code-block:: c

   struct device *dev = &pdev->dev;
   void *cpu_addr;
   dma_addr_t dma_addr;
   
   // Allocate coherent DMA buffer
   cpu_addr = dma_alloc_coherent(dev, 4096, &dma_addr, GFP_KERNEL);
   if (!cpu_addr)
       return -ENOMEM;
   
   // Device uses dma_addr for DMA
   writel(dma_addr, dev_reg + DMA_ADDR_REG);
   
   // Free buffer
   dma_free_coherent(dev, 4096, cpu_addr, dma_addr);

**7.3 Contiguous Memory Allocator (CMA)**
-------------------------------------------

For large physically contiguous allocations (e.g., camera buffers, GPU memory).

**Configure at boot:**

.. code-block:: bash

   # Reserve 256 MiB for CMA
   cma=256M

**API:**

.. code-block:: c

   struct page *dma_alloc_from_contiguous(struct device *dev,
                                          size_t count, unsigned int align);
   bool dma_release_from_contiguous(struct device *dev,
                                    struct page *pages, size_t count);

**Check CMA status:**

.. code-block:: bash

   cat /proc/meminfo | grep Cma
   # CmaTotal:      262144 kB
   # CmaFree:       200000 kB

================================================================================
8. Memory Cgroups (Control Groups v2)
================================================================================

**8.1 Overview**
-----------------

**Cgroups** limit and isolate memory usage for containers/processes.

**Key files (cgroup v2):**

.. code-block:: bash

   /sys/fs/cgroup/my_container/
   ├── memory.current         # Current usage
   ├── memory.max             # Hard limit (OOM if exceeded)
   ├── memory.high            # Soft limit (throttling)
   ├── memory.min             # Minimum guarantee (protected)
   ├── memory.low             # Best-effort protection
   ├── memory.events          # OOM events, high/max exceeded
   ├── memory.stat            # Detailed statistics
   └── memory.swap.current    # Swap usage

**8.2 Set Memory Limits**
---------------------------

.. code-block:: bash

   # Create cgroup
   mkdir /sys/fs/cgroup/my_container
   
   # Set 512 MiB hard limit
   echo 536870912 > /sys/fs/cgroup/my_container/memory.max
   
   # Set 256 MiB soft limit
   echo 268435456 > /sys/fs/cgroup/my_container/memory.high
   
   # Move process into cgroup
   echo $PID > /sys/fs/cgroup/my_container/cgroup.procs

**8.3 Monitor Memory Usage**
------------------------------

.. code-block:: bash

   cat /sys/fs/cgroup/my_container/memory.current
   # 123456789  (bytes)
   
   cat /sys/fs/cgroup/my_container/memory.stat
   # anon 12345678
   # file 23456789
   # kernel_stack 123456
   # slab 234567

================================================================================
9. Debugging & Profiling Tools
================================================================================

**9.1 /proc/meminfo Deep Dive**
---------------------------------

.. code-block:: bash

   cat /proc/meminfo

**Key fields:**

.. code-block:: text

   Field              Meaning
   ─────────────────  ────────────────────────────────────────
   MemTotal           Total usable RAM
   MemFree            Free memory (not including cache)
   MemAvailable       Estimate of available memory for apps
   Buffers            Disk block device cache
   Cached             Page cache (file-backed pages)
   SwapCached         Swapped pages cached in RAM
   Active             Recently used memory
   Inactive           Not recently used (candidate for reclaim)
   Active(anon)       Recently used anonymous pages
   Inactive(anon)     Anon pages eligible for swap
   Active(file)       Recently used file-backed pages
   Inactive(file)     File-backed pages eligible for reclaim
   Unevictable        Locked pages (mlock, ramfs)
   Shmem              Shared memory (tmpfs, shm)
   Slab               Kernel slab allocator usage
   SReclaimable       Reclaimable slab (dentry, inode caches)
   SUnreclaim         Non-reclaimable slab
   AnonPages          Anonymous pages (heap, stack)
   AnonHugePages      Transparent huge pages (anon)

**9.2 Per-Process Memory Analysis**
-------------------------------------

.. code-block:: bash

   # Quick summary
   cat /proc/<pid>/status | grep Vm
   # VmPeak: Peak virtual memory
   # VmSize: Current virtual memory
   # VmRSS:  Resident Set Size (physical memory)
   # VmData: Data segment
   # VmStk:  Stack size
   
   # Detailed map (expensive!)
   cat /proc/<pid>/smaps
   
   # Rollup (faster)
   cat /proc/<pid>/smaps_rollup
   # Rss:      123456 kB  (total RSS)
   # Pss:      100000 kB  (Proportional Set Size)
   # Private:   80000 kB  (not shared)
   # Shared:    20000 kB  (shared with other processes)

**9.3 Memory Pressure (PSI)**
-------------------------------

**Pressure Stall Information** (since Linux 4.20) tracks memory contention.

.. code-block:: bash

   cat /proc/pressure/memory
   # some avg10=1.23 avg60=0.95 avg300=0.45 total=123456789
   # full avg10=0.12 avg60=0.08 avg300=0.03 total=12345678

- **some:** At least one task stalled on memory
- **full:** All tasks stalled on memory
- **avg10/60/300:** Average % time stalled (10/60/300 seconds)

**9.4 Tools**
--------------

.. code-block:: bash

   # System-wide memory usage
   free -h
   vmstat 1  # Per-second stats
   
   # Per-process
   top -o %MEM
   ps aux --sort=-rss | head -20
   
   # Slab info
   slabtop
   
   # Kernel tracing
   trace-cmd record -e kmem  # Trace all kmem events
   perf record -e kmem:*     # Perf version

================================================================================
10. Exam Preparation — 5 Questions
================================================================================

**Question 1: Buddy Allocator Fragmentation (12 points)**

System has 1024 free pages (order 10 = 4 MiB). Process allocates:
- 256 × 4 KiB pages (order 0)
- Then frees every other page

a) After allocations, what is the highest order with free pages? (4 pts)
b) After frees, can the buddy allocator allocate 1 × 2 MiB page (order 9)? (4 pts)
c) How does compaction help? (4 pts)

**Answer:**

a) **After allocations:**
   - Allocated 256 pages out of 1024
   - Remaining: 768 pages
   - **Highest order:** Still have order 10, 9, 8... (768 pages = order 9 + order 8 + ...)
   - **Actual highest order with free pages:** Depends on allocation pattern, but likely **order 9** (512 pages)

b) **After freeing every other page:**
   - 128 freed pages (non-contiguous, alternating with allocated)
   - **Can allocate order 9 (512 pages)?** **NO** ✗
   - Freed pages are scattered, cannot merge into large contiguous block
   - **External fragmentation problem**

c) **Compaction:**
   - Moves **movable pages** to create contiguous free regions
   - Process:
     1. Scan from both ends of zone
     2. Move allocated pages to lower addresses
     3. Create large free block at higher addresses
   - **After compaction:** Can allocate order 9 ✓
   - **Cost:** Expensive (page copying, TLB flushes)

---

**Question 2: SLUB vs Buddy (10 points)**

Driver needs to allocate 100 objects of 96 bytes each, frequently allocated/freed.

a) Compare kmalloc (SLUB) vs alloc_pages (buddy) for this use case. (5 pts)
b) What are the advantages of creating a custom kmem_cache? (5 pts)

**Answer:**

a) **kmalloc (SLUB) vs alloc_pages:**

.. code-block:: text

   kmalloc (SLUB):
   - Uses kmalloc-96 cache (96-byte objects)
   - Fast: per-CPU freelist (lockless)
   - Efficient: 42 objects per page (4096 / 96 = 42)
   - Low internal fragmentation
   - Best for this use case ✓
   
   alloc_pages (buddy):
   - Allocates full 4 KiB page per object
   - 96 bytes used, 4000 bytes wasted (97.6% waste!)
   - Severe internal fragmentation
   - No caching (every alloc/free hits buddy allocator)
   - Much slower (zone lock contention)
   - DO NOT USE for small objects ✗

b) **Custom kmem_cache advantages:**
   1. **Constructor:** Pre-initialize objects (save time on alloc)
   2. **Alignment:** Optimize for cache-line alignment
   3. **Debugging:** Dedicated redzoning/poisoning for this object type
   4. **Statistics:** Track alloc/free for this specific type
   5. **Performance:** Avoid size-indexed cache lookup overhead

.. code-block:: c

   struct my_obj { char data[96]; };
   
   struct kmem_cache *my_cache = kmem_cache_create(
       "my_obj_cache",
       sizeof(struct my_obj),
       0,  // alignment (0 = default)
       SLAB_HWCACHE_ALIGN,  // align to L1 cache line
       NULL  // no constructor
   );

---

**Question 3: Page Fault Handling (12 points)**

Process accesses address 0x7ffff000 (not mapped). Page fault occurs.

a) Describe the page fault handling flow in kernel. (6 pts)
b) What is the difference between minor and major page faults? (4 pts)
c) How does mmap with MAP_POPULATE avoid page faults? (2 pts)

**Answer:**

a) **Page Fault Flow:**

.. code-block:: text

   1. CPU generates page fault exception
      → do_page_fault() (arch/x86/mm/fault.c)
   
   2. Check if address is valid VMA
      → find_vma(mm, address)
      → If no VMA: SIGSEGV (segmentation fault)
   
   3. Check permissions (read/write/exec)
      → If violation: SIGSEGV
   
   4. Handle fault type:
      a) Anonymous page (heap/stack):
         → do_anonymous_page()
         → alloc_zeroed_page(GFP_HIGHUSER_MOVABLE)
         → Set PTE, mark present
      
      b) File-backed page:
         → do_fault() → vma->vm_ops->fault()
         → filemap_fault() → find in page cache
         → If not in cache: read from disk (I/O)
      
      c) COW (copy-on-write):
         → do_wp_page()
         → Copy page, update PTE
   
   5. Update page table, flush TLB
   
   6. Return to userspace, retry instruction

b) **Minor vs Major Fault:**

.. code-block:: text

   Minor page fault:
   - Page in memory (page cache or swap cache)
   - Just need to update PTE
   - No disk I/O required
   - Fast (~microseconds)
   - Example: File already cached, just map into process
   
   Major page fault:
   - Page NOT in memory
   - Requires disk I/O (read from file or swap)
   - Slow (~milliseconds)
   - Example: First access to file page, or swapped-out page
   
   Check counts:
   $ cat /proc/<pid>/stat | awk '{print "Minor:", $10, "Major:", $12}'

c) **MAP_POPULATE:**

.. code-block:: c

   void *ptr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                    MAP_PRIVATE | MAP_ANONYMOUS | MAP_POPULATE, -1, 0);
   
   // MAP_POPULATE: Pre-fault all pages at mmap() time
   // - Kernel allocates and zeros all pages immediately
   // - Updates all PTEs
   // - No page faults during subsequent access
   // - Trade-off: Slower mmap(), but faster access

---

**Question 4: Memory Reclaim & Swappiness (10 points)**

System has:
- 4 GiB RAM total
- 2 GiB anonymous pages (process heap/stack)
- 1.5 GiB page cache
- 500 MiB free
- vm.swappiness = 60 (default)

Memory pressure occurs (allocation needs 1 GiB).

a) Which pages will kswapd reclaim first? (4 pts)
b) How does changing swappiness to 100 affect reclaim strategy? (3 pts)
c) What happens if swappiness = 0? (3 pts)

**Answer:**

a) **Reclaim priority (swappiness=60):**

.. code-block:: text

   Priority order:
   
   1. Clean page cache (easiest):
      - Unmodified file-backed pages
      - Can be dropped immediately (re-read from disk if needed)
      - Reclaim ~500 MiB page cache
   
   2. Dirty page cache:
      - Modified file-backed pages
      - Writeback to disk first, then drop
      - Reclaim another ~500 MiB page cache (after writeback)
   
   3. Anonymous pages (if needed):
      - Swap out anon pages (write to swap, mark PTE swapped)
      - swappiness=60 → balance between page cache & anon
   
   Result: Likely reclaim 1 GiB page cache, preserve most anon pages

b) **swappiness=100:**
   - **More aggressive swapping** of anonymous pages
   - Reclaim priority:
     1. Dirty page cache (writeback + drop)
     2. **Anonymous pages (swap out aggressively)**
     3. Clean page cache (last resort)
   - **Effect:** Preserve page cache (good for file I/O workloads), swap anon pages early
   - **Use case:** Database servers (keep hot data in page cache)

c) **swappiness=0:**
   - **Avoid swapping anonymous pages**
   - Reclaim only page cache
   - **Risk:** If page cache exhausted and anon pages fill RAM → OOM killer
   - **Use case:** Latency-sensitive apps (avoid swap-induced latency)
   - **Note:** swappiness=0 still allows swap in extreme cases (not absolute)

---

**Question 5: DMA Coherency (10 points)**

Driver allocates DMA buffer for network card (receives packets).

a) When to use dma_alloc_coherent() vs dma_map_single()? (5 pts)
b) Describe cache coherency problem on non-coherent architectures. (5 pts)

**Answer:**

a) **dma_alloc_coherent() vs dma_map_single():**

.. code-block:: text

   dma_alloc_coherent():
   - Use when: CPU and device frequently access same buffer
   - Characteristics:
     * Allocates uncached/write-combined memory
     * CPU writes immediately visible to device (no cache flush needed)
     * Device writes immediately visible to CPU
     * **Trade-off:** Slower CPU access (uncached)
   - Example use cases:
     * Descriptor rings (frequent CPU/device updates)
     * Command/response queues
     * Shared metadata structures
   
   dma_map_single():
   - Use when: Device-only access (CPU sets up once, device uses)
   - Characteristics:
     * Uses normal cacheable memory
     * Requires explicit sync (dma_sync_single_for_device/cpu)
     * **Better CPU performance** (cached)
   - Example use cases:
     * Network RX buffers (device writes, CPU reads once)
     * TX buffers (CPU writes once, device reads)
     * Large data transfers

**Network card example:**

.. code-block:: c

   // Descriptor ring: frequent access → coherent
   ring = dma_alloc_coherent(dev, ring_size, &ring_dma, GFP_KERNEL);
   
   // RX buffers: device writes, CPU reads → streaming
   skb->data = kmalloc(pkt_size, GFP_KERNEL);
   dma_addr = dma_map_single(dev, skb->data, pkt_size, DMA_FROM_DEVICE);
   
   // After device RX complete:
   dma_sync_single_for_cpu(dev, dma_addr, pkt_size, DMA_FROM_DEVICE);
   // Now CPU can read skb->data
   
   dma_unmap_single(dev, dma_addr, pkt_size, DMA_FROM_DEVICE);

b) **Cache coherency problem (ARM, MIPS, etc.):**

.. code-block:: text

   Problem scenario (without coherency):
   
   1. CPU writes data to buffer (cached)
      → Data in CPU cache, NOT in RAM yet
   
   2. dma_map_single() called
      → Kernel must flush cache to RAM
      → Device can now see data
   
   3. Device writes response to buffer
      → Data written to RAM
   
   4. CPU reads buffer (without sync)
      → Reads STALE data from cache! (not device response)
   
   Solution:
   - dma_sync_single_for_cpu() before CPU read
     → Invalidates CPU cache (forces read from RAM)
   
   x86_64 note:
   - Hardware cache coherency (MESI protocol)
   - dma_sync_*() is usually a no-op on x86
   - Still required for portable code!

**Debugging cache coherency issues:**
- Symptom: Driver reads garbage data after DMA
- Fix: Add missing dma_sync_single_for_cpu() calls
- Verification: Enable CONFIG_DMA_API_DEBUG

================================================================================
11. Completion Checklist
================================================================================

□ Understand buddy allocator (orders, zones, watermarks)
□ Use kmalloc/kfree correctly (check GFP flags)
□ Create and use custom kmem_cache for frequently allocated objects
□ Know VMA structure and mmap() flow
□ Understand page fault handling (anon, file, COW)
□ Configure memory cgroups for containers
□ Debug memory issues with /proc/meminfo, /proc/vmstat
□ Use PSI to monitor memory pressure
□ Understand OOM killer and oom_score_adj
□ Implement DMA correctly (coherent vs streaming)
□ Know when to use Transparent Huge Pages
□ Monitor slab allocator with /proc/slabinfo
□ Understand swap and swappiness tuning
□ Use trace-cmd / perf for memory profiling

================================================================================
12. Key Takeaways
================================================================================

1. **Buddy allocator** manages physical pages in power-of-2 blocks (4 KiB – 4 MiB)

2. **SLUB** provides object caching for small allocations (< 8 KiB)

3. **VMA** represents contiguous virtual address ranges (vm_start – vm_end)

4. **Page faults** implement demand paging (allocate on access, not upfront)

5. **Page cache** caches file contents in RAM (avoid disk I/O)

6. **kswapd** performs background memory reclaim at low watermark

7. **OOM killer** is last resort when all reclaim fails

8. **Transparent Huge Pages** reduce TLB misses (4 KiB → 2 MiB)

9. **DMA coherent memory** for frequent CPU/device access, streaming DMA for one-time transfers

10. **Cgroups** isolate and limit memory usage per container

11. **swappiness** controls balance between page cache and anon reclaim

12. **PSI** provides real-time memory pressure metrics

================================================================================
References & Further Reading
================================================================================

**Books:**
- Professional Linux Kernel Architecture (Wolfgang Mauerer)
- Understanding the Linux Virtual Memory Manager (Mel Gorman)
- Linux Kernel Development (Robert Love)

**Kernel Documentation:**
- Documentation/admin-guide/mm/
- Documentation/core-api/memory-allocation.rst
- Documentation/vm/

**Source Code:**
- mm/page_alloc.c (buddy allocator)
- mm/slub.c (SLUB allocator)
- mm/mmap.c (VMA management)
- mm/memory.c (page fault handling)
- mm/oom_kill.c (OOM killer)

**Tools:**
- vmstat, free, top, ps
- /proc/meminfo, /proc/vmstat, /proc/buddyinfo
- trace-cmd, perf (kmem events)
- bpftrace (memory tracing)

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Kernel Version:** Linux 6.12–6.16

================================================================================
