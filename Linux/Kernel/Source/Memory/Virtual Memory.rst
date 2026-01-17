**Linux virtual process memory** from a kernel and user-space perspective (modern kernels 6.x / early 2026 era).

💾 1. Virtual Memory Layout – Typical 64-bit Process (x86_64)

0x0000000000000000  ┌──────────────────────────────┐
                    │  NULL page (access denied)   │  ← guard / trap on null pointer deref
                    └──────────────────────────────┘
~0x00007f0000000000 ┌──────────────────────────────┐
                    │  mmap / libraries / heap     │  ← grows upward (mmap base randomized)
                    │  (shared libs, anon mmap,    │
                    │   file mappings, brk/sbrk)   │
                    └──────────────────────────────┘
                    │           free space         │
                    └──────────────────────────────┘
~0x7fffffffe000     ┌──────────────────────────────┐
                    │  Stack (grows downward)      │  ← per-thread stack (usually 8 MiB default)
                    └──────────────────────────────┘
~0xffffffffff600000 ┌──────────────────────────────┐
                    │  vsyscall / vdso             │  ← legacy / compat vdso page
                    └──────────────────────────────┘
0xffffffffffffffff  └──────────────────────────────┘

- Kernel space starts at ``0xffff888000000000`` (direct map) – not visible to user process
- Address space split: ~47–48 bits usable (canonical hole in middle)

⭐ 💾 2. Key Virtual Memory Regions (Typical /proc/<pid>/maps)

| Region Type              | Typical Address Range          | Permissions | Backing                  | Notes / Source |
|--------------------------|--------------------------------|-------------|--------------------------|----------------|
| Text (code)              | 0x55xxxxxx0000–0x55xxxxxx8000 | r-x         | File (executable)        | mmap PROT_EXEC |
| Data (initialized)       | Next page after text           | rw-         | File (copy-on-write)     | .data section |
| BSS (zero-initialized)   | After data                     | rw-         | Anon (zero pages)        | .bss section |
| Heap                     | After BSS (brk)                | rw-         | Anon                     | grows via brk/sbrk or mmap |
| Thread stacks            | High addresses (downward)      | rw-         | Anon                     | 1 per thread, usually 8 MiB |
| mmap regions             | Above heap or randomized       | rwx / rw-   | File / Anon / huge pages | shared libs, mmap(), shm |
| vdso / vvar              | ~0xffffffffff600000            | r-x / r--   | Kernel provided          | vsyscall replacement |
| vvar (variable page)     | Near vdso                      | r--         | Kernel                   | time, getcpu, etc. |

⭐ 🐧 3. Important Kernel Structures

⭐ | Structure               | Location                          | Represents / Key Fields |
|-------------------------|-----------------------------------|--------------------------|
| ``struct mm_struct``      | ``include/linux/mm_types.h``        | Per-process VM descriptor: pgd, mmap (RB tree), hiwater_rss, map_count, … |
| ``struct vm_area_struct`` | ``include/linux/mm_types.h``        | One contiguous virtual region: vm_start, vm_end, vm_flags, vm_file, vm_ops |
| ``struct page``           | ``include/linux/mm_types.h``        | Physical page metadata (flags, refcount, mapping) |
| ``pte_t`` / ``pmd_t`` etc.  | arch/x86/include/asm/pgtable*.h   | Page table entries (present, rw, user, huge, etc.) |

⚙️ 4. Virtual → Physical Translation Path

1. CPU → CR3 (pgd of current->mm)
2. PML4 (level 4) → PDP (level 3)
3. PDP → PD (level 2) → PT (level 1)
4. PT entry → physical page frame + offset

**Huge pages**:
- 2 MiB (PMD) or 1 GiB (PUD) – fewer TLB misses
- Transparent Huge Pages (THP) – ``khugepaged`` collapses 4 KiB → 2 MiB

📌 5. Common /proc/<pid>/maps Flags & vm_flags

| Flag (maps) | vm_flags equivalent          | Meaning |
|-------------|------------------------------|---------|
| r           | VM_READ                      | Readable |
| w           | VM_WRITE                     | Writable |
| x           | VM_EXEC                      | Executable |
| p           | !VM_SHARED                   | Private (COW) |
| s           | VM_SHARED                    | Shared |
| g           | VM_GROWSUP / VM_GROWSDOWN    | Stack/heap growth direction |
| R           | VM_MAYREAD                   | May become readable |
| W           | VM_MAYWRITE                  | May become writable |
| X           | VM_MAYEXEC                   | May become executable |
| H           | VM_HUGEPAGE / VM_HUGETLB     | Huge page eligible |

💾 6. Memory Allocation APIs (User → Kernel Path)

| API (user)           | Kernel path                          | Backing | Contiguous? | Notes |
|----------------------|--------------------------------------|---------|-------------|-------|
| ``malloc()``           | brk / mmap                           | Anon    | No          | glibc heap |
| ``mmap(anon)``         | ``do_mmap()`` → anon vma               | Anon    | No          | Large allocations |
| ``mmap(file)``         | ``do_mmap()`` → file-backed vma        | Page cache | No       | Shared libs, files |
| ``shm_open()`` / shmget() | ``shm_mmap()`` / ``do_shmat()``       | Anon / file | No       | IPC |
| ``posix_memalign()``   | mmap with alignment                  | Anon    | No          | Page-aligned |
| ``madvise(MADV_HUGEPAGE)`` | Mark region for THP              | —       | —           | Transparent huge pages |

🐛 7. Debugging & Inspection Commands

.. code-block:: bash

================================================================================
💾 Full memory map
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



cat /proc/<pid>/maps

================================================================================
Detailed stats per vma
================================================================================

cat /proc/<pid>/smaps

================================================================================
RSS, PSS, swap, etc.
================================================================================

cat /proc/<pid>/status | grep -E 'Vm|Rss|Pss'

================================================================================
Huge pages usage
================================================================================

cat /proc/meminfo | grep -i huge

================================================================================
Transparent Huge Pages status
================================================================================

cat /sys/kernel/mm/transparent_hugepage/enabled

================================================================================
Per-process huge page stats
================================================================================

cat /proc/<pid>/smaps | grep -i thp

================================================================================
🐛 Kernel page table dump (debug)
================================================================================

echo 1 > /proc/sys/vm/print_pagetables   # very verbose!

📚 8. Quick Reference: Address Space Limits (64-bit)

- Total user virtual address bits: 47–48 (depends on kernel config)
- Max user address: ~0x00007fffffffffff
- Stack default ulimit: 8 MiB (soft), unlimited (hard)
- mmap_min_addr: usually 65536 (protects against null pointer exploits)

This cheatsheet focuses on **virtual memory** from the process perspective (not physical allocation, buddy, slab, or page cache).  
🟢 🟢 Good luck debugging memory layouts, leaks, or OOM killers!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
