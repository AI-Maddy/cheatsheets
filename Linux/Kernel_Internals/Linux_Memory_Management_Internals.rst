================================================
Linux Memory Management Internals
================================================

:Author: Linux Kernel Documentation  
:Date: January 2026
:Version: 1.0
:Focus: Deep dive into Linux kernel memory management internals

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Memory Architecture
-------------------

.. code-block:: text

   Physical Memory Layout:
   
   High Memory (32-bit only)
   ├── > 896 MB
   └── Temporarily mapped
   
   Normal Memory
   ├── Direct mapped to kernel space
   ├── 0-896 MB (32-bit) or full range (64-bit)
   └── Most kernel allocations
   
   DMA Zones
   ├── ZONE_DMA32: < 4 GB
   └── ZONE_DMA: < 16 MB (ISA)
   
   Virtual Memory Layout (x86_64):
   
   0xFFFFFFFF_FFFFFFFF  ┌─────────────────┐
                        │ Kernel Code/Data│
   0xFFFFFFFF_80000000  ├─────────────────┤
                        │ Direct Mapping  │
   0xFFFF8880_00000000  ├─────────────────┤
                        │ vmalloc/ioremap │
   0xFFFFC900_00000000  ├─────────────────┤
                        │ Hole            │
   0x00007FFF_FFFFFFFF  ├─────────────────┤
                        │ User Space      │
   0x00000000_00000000  └─────────────────┘

Essential Memory APIs
---------------------

.. code-block:: c

   // Page allocation
   struct page *alloc_pages(gfp_t gfp_mask, unsigned int order);
   void __free_pages(struct page *page, unsigned int order);
   
   // Kernel allocator
   void *kmalloc(size_t size, gfp_t flags);
   void *kzalloc(size_t size, gfp_t flags);
   void kfree(const void *ptr);
   
   // Vmalloc (non-contiguous)
   void *vmalloc(unsigned long size);
   void vfree(const void *addr);
   
   // Slab allocator
   struct kmem_cache *kmem_cache_create(name, size, align, flags, ctor);
   void *kmem_cache_alloc(struct kmem_cache *cachep, gfp_t flags);
   void kmem_cache_free(struct kmem_cache *cachep, void *objp);

Memory Zones and Nodes
=======================

Zone Structure
--------------

.. code-block:: c

   struct zone {
       unsigned long _watermark[NR_WMARK];  // Free page watermarks
       long lowmem_reserve[MAX_NR_ZONES];   // Reserved pages
       
       struct per_cpu_pageset __percpu *pageset;  // Per-CPU page lists
       
       unsigned long zone_start_pfn;        // First page frame number
       unsigned long managed_pages;         // Managed pages
       unsigned long spanned_pages;         // Total pages in zone
       unsigned long present_pages;         // Existing pages
       
       const char *name;                    // Zone name
       
       struct free_area free_area[MAX_ORDER];  // Free page lists
       
       unsigned long flags;                 // Zone flags
       spinlock_t lock;                     // Zone lock
       
       struct pglist_data *zone_pgdat;      // Parent node
   };
   
   // Free area (buddy allocator)
   struct free_area {
       struct list_head free_list[MIGRATE_TYPES];
       unsigned long nr_free;
   };
   
   // Watermarks
   enum zone_watermarks {
       WMARK_MIN,    // Minimum free pages
       WMARK_LOW,    // Start reclaim
       WMARK_HIGH,   // Stop reclaim
       NR_WMARK
   };

NUMA Nodes
----------

.. code-block:: c

   // Node representation
   typedef struct pglist_data {
       struct zone node_zones[MAX_NR_ZONES];
       struct zonelist node_zonelists[MAX_ZONELISTS];
       
       int node_id;
       struct page *node_mem_map;           // Page array
       
       unsigned long node_start_pfn;
       unsigned long node_present_pages;    // Total present pages
       unsigned long node_spanned_pages;    // Total spanned pages
       
       wait_queue_head_t kswapd_wait;       // kswapd wait queue
       struct task_struct *kswapd;          // kswapd kernel thread
       
       int kswapd_order;                    // Order to reclaim
       enum zone_type kswapd_highest_zoneidx;
   } pg_data_t;
   
   // NUMA-aware allocation
   struct page *alloc_pages_node(int nid, gfp_t gfp_mask, unsigned int order);

Page Allocator (Buddy System)
==============================

Buddy Algorithm
---------------

.. code-block:: text

   Buddy System Concept:
   
   Order 0: 4KB pages      [x][x][x][x][x][x][x][x]
   Order 1: 8KB blocks     [  x  ][  x  ][  x  ][  x  ]
   Order 2: 16KB blocks    [     x     ][     x     ]
   Order 3: 32KB blocks    [           x           ]
   
   Allocation (e.g., 8KB = Order 1):
   1. Check Order 1 free list
   2. If empty, check Order 2 and split
   3. Split buddy and add to lower order
   
   Free (8KB block):
   1. Check if buddy is free
   2. If free, coalesce to higher order
   3. Repeat until buddy not free

Page Allocation Implementation
-------------------------------

.. code-block:: c

   // Allocate 2^order contiguous pages
   struct page *alloc_pages(gfp_t gfp_mask, unsigned int order) {
       struct alloc_context ac = { };
       struct page *page;
       
       // Setup allocation context
       prepare_alloc_pages(gfp_mask, order, &ac);
       
       // Fast path - try per-CPU lists
       page = get_page_from_freelist(gfp_mask, order, &ac);
       if (likely(page))
           return page;
       
       // Slow path - zone reclaim, compaction
       page = __alloc_pages_slowpath(gfp_mask, order, &ac);
       return page;
   }
   
   // Free pages
   void __free_pages(struct page *page, unsigned int order) {
       if (put_page_testzero(page))
           free_the_page(page, order);
   }
   
   // Helper functions
   unsigned long __get_free_pages(gfp_t gfp_mask, unsigned int order) {
       struct page *page = alloc_pages(gfp_mask, order);
       if (!page)
           return 0;
       return (unsigned long)page_address(page);
   }
   
   void free_pages(unsigned long addr, unsigned int order) {
       if (addr != 0)
           __free_pages(virt_to_page((void *)addr), order);
   }

GFP Flags
---------

.. code-block:: c

   // GFP (Get Free Pages) flags
   
   // Zone modifiers
   #define __GFP_DMA       0x01  // Allocate from ZONE_DMA
   #define __GFP_HIGHMEM   0x02  // Can use high memory
   #define __GFP_DMA32     0x04  // Allocate from ZONE_DMA32
   
   // Mobility and placement
   #define __GFP_MOVABLE   0x08  // Page is movable
   #define __GFP_RECLAIMABLE 0x10  // Page is reclaimable
   
   // Action modifiers
   #define __GFP_WAIT      0x10  // Can sleep/wait
   #define __GFP_HIGH      0x20  // Use emergency pools
   #define __GFP_IO        0x40  // Can start I/O
   #define __GFP_FS        0x80  // Can call filesystem
   #define __GFP_ZERO      0x8000 // Zero memory
   
   // Common combinations
   #define GFP_ATOMIC  (__GFP_HIGH)           // No sleep, use reserves
   #define GFP_KERNEL  (__GFP_WAIT | __GFP_IO | __GFP_FS)  // Normal kernel
   #define GFP_USER    (__GFP_WAIT | __GFP_IO | __GFP_FS | __GFP_HARDWALL)  // User pages
   #define GFP_HIGHUSER (GFP_USER | __GFP_HIGHMEM)  // User high memory
   #define GFP_NOIO    (__GFP_WAIT)           // No I/O
   #define GFP_NOFS    (__GFP_WAIT | __GFP_IO)  // No FS operations
   #define GFP_DMA     (__GFP_DMA)            // DMA-capable memory

Slab Allocator
==============

Slab Concept
------------

.. code-block:: text

   Slab Allocator Hierarchy:
   
   Cache (e.g., task_struct cache)
   ├── Slab 1 (full)
   │   ├── Object 1 (allocated)
   │   ├── Object 2 (allocated)
   │   └── ...
   ├── Slab 2 (partial)
   │   ├── Object 1 (allocated)
   │   ├── Object 2 (free)
   │   └── ...
   └── Slab 3 (empty)
       └── All objects free
   
   Implementations:
   - SLAB: Original, complex, per-CPU caches
   - SLUB: Simpler, default in most configs
   - SLOB: Minimal, for embedded systems

SLUB Implementation
-------------------

.. code-block:: c

   // Create cache
   struct kmem_cache *kmem_cache_create(const char *name,
                                        unsigned int size,
                                        unsigned int align,
                                        slab_flags_t flags,
                                        void (*ctor)(void *)) {
       return __kmem_cache_create(name, size, align, flags, ctor);
   }
   
   // Example: task_struct cache
   static struct kmem_cache *task_struct_cachep;
   
   task_struct_cachep = kmem_cache_create("task_struct",
                                          sizeof(struct task_struct),
                                          ARCH_MIN_TASKALIGN,
                                          SLAB_PANIC | SLAB_ACCOUNT,
                                          NULL);
   
   // Allocate from cache
   void *kmem_cache_alloc(struct kmem_cache *cachep, gfp_t flags) {
       return slab_alloc(cachep, flags, _RET_IP_);
   }
   
   struct task_struct *task = kmem_cache_alloc(task_struct_cachep, GFP_KERNEL);
   
   // Free to cache
   void kmem_cache_free(struct kmem_cache *cachep, void *objp) {
       slab_free(cachep, objp, _RET_IP_);
   }
   
   kmem_cache_free(task_struct_cachep, task);
   
   // Destroy cache
   void kmem_cache_destroy(struct kmem_cache *cachep);

Kmalloc Implementation
----------------------

.. code-block:: c

   // Kmalloc uses size-specific slab caches
   static struct kmem_cache *kmalloc_caches[KMALLOC_SHIFT_HIGH + 1];
   
   // Names: kmalloc-8, kmalloc-16, kmalloc-32, ...
   
   void *kmalloc(size_t size, gfp_t flags) {
       if (__builtin_constant_p(size)) {
           unsigned int index = kmalloc_index(size);
           if (!index)
               return ZERO_SIZE_PTR;
           return kmem_cache_alloc_trace(kmalloc_caches[index],
                                         flags, size);
       }
       return __kmalloc(size, flags);
   }
   
   void *kzalloc(size_t size, gfp_t flags) {
       return kmalloc(size, flags | __GFP_ZERO);
   }
   
   void kfree(const void *x) {
       struct page *page;
       
       if (unlikely(ZERO_OR_NULL_PTR(x)))
           return;
       
       page = virt_to_head_page(x);
       if (unlikely(!PageSlab(page)))
           __free_pages(page, compound_order(page));
       else
           slab_free(page->slab_cache, page, (void *)x);
   }

Vmalloc
=======

Non-Contiguous Allocation
--------------------------

.. code-block:: c

   // Vmalloc allocates virtually contiguous, physically discontiguous memory
   void *vmalloc(unsigned long size) {
       return __vmalloc_node(size, 1, GFP_KERNEL, NUMA_NO_NODE,
                            __builtin_return_address(0));
   }
   
   void *vzalloc(unsigned long size) {
       return __vmalloc_node(size, 1, GFP_KERNEL | __GFP_ZERO,
                            NUMA_NO_NODE, __builtin_return_address(0));
   }
   
   void vfree(const void *addr) {
       __vfree(addr);
   }
   
   // Example use
   void *large_buffer = vmalloc(1024 * 1024);  // 1 MB
   if (!large_buffer)
       return -ENOMEM;
   
   // Use buffer
   memset(large_buffer, 0, 1024 * 1024);
   
   vfree(large_buffer);

Vmalloc vs Kmalloc
-------------------

.. code-block:: text

   Kmalloc:
   + Faster (direct mapped)
   + DMA capable
   + Better cache locality
   - Limited size (typically < 4MB)
   - Wastes memory (buddy system fragmentation)
   
   Vmalloc:
   + Large allocations possible
   + Less fragmentation impact
   - Slower (TLB overhead)
   - Not DMA capable
   - More page table overhead

Per-CPU Variables
=================

Per-CPU Allocator
-----------------

.. code-block:: c

   // Define per-CPU variable
   DEFINE_PER_CPU(int, my_percpu_var);
   
   // Access on current CPU
   int val = get_cpu_var(my_percpu_var);
   val++;
   put_cpu_var(my_percpu_var);
   
   // Or with preemption disabled
   int val = this_cpu_read(my_percpu_var);
   this_cpu_write(my_percpu_var, val + 1);
   this_cpu_inc(my_percpu_var);
   
   // Access specific CPU (requires locking)
   int val = per_cpu(my_percpu_var, cpu_id);
   
   // Dynamic allocation
   int __percpu *ptr = alloc_percpu(int);
   if (!ptr)
       return -ENOMEM;
   
   *per_cpu_ptr(ptr, cpu) = value;
   
   free_percpu(ptr);

Virtual Memory Areas
====================

VMA Structure
-------------

.. code-block:: c

   // Virtual memory area
   struct vm_area_struct {
       struct mm_struct *vm_mm;         // Parent mm
       unsigned long vm_start;          // Start address
       unsigned long vm_end;            // End address (exclusive)
       
       struct vm_area_struct *vm_next, *vm_prev;  // VMA list
       
       pgprot_t vm_page_prot;           // Access permissions
       unsigned long vm_flags;          // Flags
       
       struct rb_node vm_rb;            // Red-black tree node
       
       struct anon_vma *anon_vma;       // Anonymous VMA
       const struct vm_operations_struct *vm_ops;
       
       unsigned long vm_pgoff;          // Offset in file
       struct file *vm_file;            // Mapped file
       void *vm_private_data;           // Private data
   };
   
   // VMA flags
   #define VM_READ         0x00000001  // Pages can be read
   #define VM_WRITE        0x00000002  // Pages can be written
   #define VM_EXEC         0x00000004  // Pages can be executed
   #define VM_SHARED       0x00000008  // Pages are shared
   #define VM_MAYREAD      0x00000010  // May be readable
   #define VM_MAYWRITE     0x00000020  // May be writable
   #define VM_MAYEXEC      0x00000040  // May be executable
   #define VM_MAYSHARE     0x00000080  // May be shared

Memory Descriptor
-----------------

.. code-block:: c

   // Process memory descriptor
   struct mm_struct {
       struct vm_area_struct *mmap;     // VMA list
       struct rb_root mm_rb;            // VMA red-black tree
       unsigned long mmap_base;         // mmap base address
       unsigned long total_vm;          // Total mapped pages
       unsigned long locked_vm;         // Locked pages
       unsigned long pinned_vm;         // Pinned pages
       unsigned long data_vm;           // Data segment pages
       unsigned long exec_vm;           // Executable pages
       unsigned long stack_vm;          // Stack pages
       
       unsigned long start_code, end_code;      // Code segment
       unsigned long start_data, end_data;      // Data segment
       unsigned long start_brk, brk;            // Heap
       unsigned long start_stack;               // Stack
       unsigned long arg_start, arg_end;        // Arguments
       unsigned long env_start, env_end;        // Environment
       
       pgd_t *pgd;                      // Page global directory
       
       atomic_t mm_users;               // Users count
       atomic_t mm_count;               // Reference count
       
       spinlock_t page_table_lock;      // Page table lock
   };

Page Tables
===========

Page Table Hierarchy
--------------------

.. code-block:: text

   x86_64 Page Table (4-level):
   
   Virtual Address (48-bit):
   | PGD (9) | PUD (9) | PMD (9) | PTE (9) | Offset (12) |
   
   CR3 → PGD (Page Global Directory)
         ├── PUD (Page Upper Directory)
         │   ├── PMD (Page Middle Directory)
         │   │   ├── PTE (Page Table Entry)
         │   │   │   └── Physical Page
         
   5-level (La57):
   | P4D (9) | PGD (9) | PUD (9) | PMD (9) | PTE (9) | Offset (12) |

Page Table Entry
----------------

.. code-block:: c

   // Page table entry (x86_64)
   typedef unsigned long pteval_t;
   typedef struct { pteval_t pte; } pte_t;
   
   // PTE flags
   #define _PAGE_PRESENT   0x001  // Page present in memory
   #define _PAGE_RW        0x002  // Read/write
   #define _PAGE_USER      0x004  // User accessible
   #define _PAGE_PWT       0x008  // Write-through caching
   #define _PAGE_PCD       0x010  // Cache disabled
   #define _PAGE_ACCESSED  0x020  // Accessed (set by CPU)
   #define _PAGE_DIRTY     0x040  // Dirty (set by CPU)
   #define _PAGE_PSE       0x080  // Huge page (2MB/1GB)
   #define _PAGE_GLOBAL    0x100  // Global TLB entry
   #define _PAGE_NX        (1UL << 63)  // No execute
   
   // Page table manipulation
   static inline int pte_present(pte_t pte) {
       return pte_val(pte) & _PAGE_PRESENT;
   }
   
   static inline int pte_dirty(pte_t pte) {
       return pte_val(pte) & _PAGE_DIRTY;
   }
   
   static inline pte_t pte_mkdirty(pte_t pte) {
       return __pte(pte_val(pte) | _PAGE_DIRTY);
   }

Page Fault Handling
===================

Page Fault Flow
---------------

.. code-block:: text

   Page Fault
         |
         | CPU generates fault
         v
   do_page_fault (arch/x86/mm/fault.c)
         |
         | Determine fault address (CR2)
         | Check VMA permissions
         v
   handle_mm_fault
         |
         ├─→ handle_pte_fault
         │   ├─→ do_anonymous_page (anonymous page)
         │   ├─→ do_swap_page (swapped out)
         │   ├─→ do_wp_page (write protect / COW)
         │   └─→ do_fault (file-backed)
         └─→ Allocate page, update PTE

Page Fault Handler
-------------------

.. code-block:: c

   // Simplified page fault handler
   vm_fault_t handle_mm_fault(struct vm_area_struct *vma,
                              unsigned long address,
                              unsigned int flags) {
       pgd_t *pgd;
       p4d_t *p4d;
       pud_t *pud;
       pmd_t *pmd;
       pte_t *pte;
       
       pgd = pgd_offset(vma->vm_mm, address);
       p4d = p4d_alloc(vma->vm_mm, pgd, address);
       if (!p4d)
           return VM_FAULT_OOM;
       
       pud = pud_alloc(vma->vm_mm, p4d, address);
       if (!pud)
           return VM_FAULT_OOM;
       
       pmd = pmd_alloc(vma->vm_mm, pud, address);
       if (!pmd)
           return VM_FAULT_OOM;
       
       pte = pte_alloc(vma->vm_mm, pmd, address);
       if (!pte)
           return VM_FAULT_OOM;
       
       return handle_pte_fault(vma, address, pte, flags);
   }

Copy-on-Write (COW)
-------------------

.. code-block:: c

   // COW page fault
   vm_fault_t do_wp_page(struct vm_fault *vmf) {
       struct vm_area_struct *vma = vmf->vma;
       struct page *old_page = vmf->page;
       struct page *new_page;
       pte_t entry;
       
       // Check if we can reuse the page
       if (page_mapcount(old_page) == 1) {
           // Only reference, reuse
           entry = pte_mkyoung(vmf->orig_pte);
           entry = pte_mkdirty(entry);
           entry = pte_mkwrite(entry);
           set_pte_at(vma->vm_mm, vmf->address, vmf->pte, entry);
           return VM_FAULT_WRITE;
       }
       
       // Multiple references, copy page
       new_page = alloc_page_vma(GFP_HIGHUSER_MOVABLE, vma, vmf->address);
       if (!new_page)
           return VM_FAULT_OOM;
       
       copy_user_highpage(new_page, old_page, vmf->address, vma);
       
       // Update PTE
       entry = mk_pte(new_page, vma->vm_page_prot);
       entry = pte_mkwrite(pte_mkdirty(entry));
       set_pte_at(vma->vm_mm, vmf->address, vmf->pte, entry);
       
       page_add_new_anon_rmap(new_page, vma, vmf->address);
       
       return VM_FAULT_WRITE;
   }

Page Cache
==========

Address Space
-------------

.. code-block:: c

   struct address_space {
       struct inode *host;              // Owner inode
       struct radix_tree_root page_tree;  // Page cache tree
       spinlock_t tree_lock;            // Tree lock
       atomic_t i_mmap_writable;        // Writable mappings count
       struct rb_root_cached i_mmap;    // Private mappings
       unsigned long nrpages;           // Number of pages
       unsigned long nrexceptional;     // Exceptional entries
       pgoff_t writeback_index;         // Writeback cursor
       const struct address_space_operations *a_ops;
       unsigned long flags;
       struct backing_dev_info *backing_dev_info;
       spinlock_t private_lock;
       struct list_head private_list;
       void *private_data;
   };
   
   struct address_space_operations {
       int (*writepage)(struct page *, struct writeback_control *);
       int (*readpage)(struct file *, struct page *);
       int (*writepages)(struct address_space *, struct writeback_control *);
       int (*set_page_dirty)(struct page *);
       int (*readpages)(struct file *, struct address_space *,
                       struct list_head *, unsigned);
       int (*write_begin)(struct file *, struct address_space *,
                         loff_t, unsigned, unsigned, struct page **,
                         void **);
       int (*write_end)(struct file *, struct address_space *,
                       loff_t, unsigned, unsigned, struct page *, void *);
       sector_t (*bmap)(struct address_space *, sector_t);
       void (*invalidatepage)(struct page *, unsigned int, unsigned int);
       int (*releasepage)(struct page *, gfp_t);
       void (*freepage)(struct page *);
       ssize_t (*direct_IO)(struct kiocb *, struct iov_iter *);
   };

Memory Reclaim
==============

Page Reclamation
----------------

.. code-block:: c

   // kswapd - kernel swap daemon
   static int kswapd(void *p) {
       pg_data_t *pgdat = (pg_data_t *)p;
       struct task_struct *tsk = current;
       const struct cpumask *cpumask = cpumask_of_node(pgdat->node_id);
       
       if (!cpumask_empty(cpumask))
           set_cpus_allowed_ptr(tsk, cpumask);
       
       for ( ; ; ) {
           // Wait for wakeup
           prepare_to_wait(&pgdat->kswapd_wait, &wait,
                          TASK_INTERRUPTIBLE);
           
           if (!kswapd_should_run(pgdat))
               schedule();
           
           finish_wait(&pgdat->kswapd_wait, &wait);
           
           // Reclaim pages
           balance_pgdat(pgdat, order, classzone_idx);
       }
   }

LRU Lists
---------

.. code-block:: c

   // Least Recently Used lists
   enum lru_list {
       LRU_INACTIVE_ANON = LRU_BASE,    // Inactive anonymous
       LRU_ACTIVE_ANON,                 // Active anonymous
       LRU_INACTIVE_FILE,               // Inactive file
       LRU_ACTIVE_FILE,                 // Active file
       LRU_UNEVICTABLE,                 // Unevictable (mlock)
       NR_LRU_LISTS
   };
   
   // Per-zone LRU
   struct lruvec {
       struct list_head lists[NR_LRU_LISTS];
       struct zone_reclaim_stat reclaim_stat;
       atomic_long_t nonresident_age;
       unsigned long refaults;
       unsigned long flags;
   };

Out of Memory Killer
====================

OOM Killer
----------

.. code-block:: c

   // OOM victim selection
   static void oom_kill_process(struct oom_control *oc) {
       struct task_struct *p = oc->chosen;
       unsigned int points = oc->totalpages;
       
       // Select victim with highest badness score
       for_each_process(p) {
           unsigned int score = oom_badness(p, NULL, NULL, totalpages);
           if (score > points) {
               points = score;
               victim = p;
           }
       }
       
       // Kill victim
       do_send_sig_info(SIGKILL, SEND_SIG_FORCED, victim, true);
       
       pr_err("Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB\n",
              task_pid_nr(victim), victim->comm,
              K(victim->mm->total_vm),
              K(get_mm_counter(victim->mm, MM_ANONPAGES)),
              K(get_mm_counter(victim->mm, MM_FILEPAGES)));
   }

Best Practices
==============

1. **Use appropriate allocator** (kmalloc vs vmalloc)
2. **Check for NULL** after allocation
3. **Free memory** when done (avoid leaks)
4. **Use GFP flags correctly** (atomic context awareness)
5. **Minimize allocations** in hot paths
6. **Use object caching** (kmem_cache) for frequent allocations
7. **Understand memory zones** for DMA
8. **Monitor memory usage** (/proc/meminfo, slabtop)
9. **Handle OOM** gracefully
10. **Use per-CPU variables** to reduce contention

Common Pitfalls
===============

1. **Memory leaks** - not freeing allocated memory
2. **Double free** - freeing same memory twice
3. **Use after free** - accessing freed memory
4. **Wrong GFP flags** - GFP_KERNEL in atomic context
5. **Fragmentation** - excessive small allocations
6. **No NULL check** - dereferencing NULL pointer
7. **Buffer overflow** - writing beyond allocated size

Quick Reference
===============

.. code-block:: c

   // Page allocator
   __get_free_pages(GFP_KERNEL, order);
   alloc_pages(GFP_KERNEL, order);
   free_pages(addr, order);
   
   // Slab
   kmem_cache_create(name, size, align, flags, ctor);
   kmem_cache_alloc(cache, GFP_KERNEL);
   kmem_cache_free(cache, ptr);
   
   // Kmalloc
   kmalloc(size, GFP_KERNEL);
   kzalloc(size, GFP_KERNEL);
   kfree(ptr);
   
   // Vmalloc
   vmalloc(size);
   vfree(ptr);
   
   // Per-CPU
   DEFINE_PER_CPU(type, var);
   get_cpu_var(var);
   put_cpu_var(var);

See Also
========

- Linux_Kernel_Architecture.rst
- Linux_CPU_Scheduling_Internals.rst
- Linux_Process_Management.rst

References
==========

- mm/ in Linux kernel source
- Understanding the Linux Virtual Memory Manager
- https://www.kernel.org/doc/html/latest/vm/
