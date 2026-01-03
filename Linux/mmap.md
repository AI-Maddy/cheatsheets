**cheatsheet comparing file-backed mmap vs anonymous mmap** in Linux (kernel perspective, modern kernels 6.x / early 2026).

### 1. Quick Comparison Table

| Aspect                        | File-backed mmap (`MAP_FILE`)                          | Anonymous mmap (`MAP_ANONYMOUS` / `MAP_ANON`)          |
|-------------------------------|--------------------------------------------------------|--------------------------------------------------------|
| **Backing store**             | Regular file on disk (or tmpfs, hugetlbfs, etc.)       | No file — swap space or nothing (demand-zero pages)   |
| **How created**               | `mmap(fd, length, …)` with valid file descriptor       | `mmap(-1, length, …)` or `MAP_ANONYMOUS` flag          |
| **Persistence**               | Changes visible on disk (if `MAP_SHARED`)              | Lost on process exit / unmap (unless swapped out)      |
| **Sharing**                   | `MAP_SHARED` → changes visible to other processes      | `MAP_SHARED` → visible only via fork (copy-on-write)   |
| **Common use cases**          | Shared libraries, memory-mapped files, inter-process shared memory | Heap (`malloc` large blocks), thread stacks, anonymous shared memory |
| **Page fault behavior**       | Read → file → page cache<br>Write → dirty page (if shared) | Read → zero page (demand-zero)<br>Write → private COW page |
| **Swap eligibility**          | File-backed pages usually **not** swapped (file is source) | Anonymous pages **are** swappable (to swap or zswap)   |
| **/proc/<pid>/maps marker**   | Path of file (or `[heap]`, `[stack]`, etc. if special) | `[anon]` or `[heap]`, `[stack]`, `[vdso]`, etc.        |
| **CoW (Copy-on-Write)**       | Yes (for private mappings)                             | Yes (for private mappings)                             |
| **Huge pages support**        | Yes (hugetlbfs or THP)                                 | Yes (THP very common)                                  |
| **Typical flags combo**       | `MAP_SHARED | MAP_POPULATE` (pre-fault)             | `MAP_PRIVATE | MAP_ANONYMOUS`                         |

### 2. Key mmap() Flags Combinations

| Goal                              | Recommended flags & call                                                                 | Result in /proc/<pid>/maps |
|-----------------------------------|------------------------------------------------------------------------------------------|-----------------------------|
| Read-only file mapping            | `mmap(NULL, len, PROT_READ, MAP_SHARED|MAP_POPULATE, fd, 0)`                          | `/path/to/file` r--         |
| Read-write shared file mapping    | `mmap(NULL, len, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0)`                              | `/path/to/file` rw-s        |
| Private COW file mapping          | `mmap(NULL, len, PROT_READ|PROT_WRITE, MAP_PRIVATE, fd, 0)`                             | `/path/to/file` rw-p        |
| Anonymous private memory (heap)   | `mmap(NULL, len, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)`               | `[anon]` or `[heap]` rw-p   |
| Anonymous shared memory           | `mmap(NULL, len, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0)`                | `[anon]` rw-s               |
| Huge page anonymous               | `mmap(…, MAP_HUGETLB|MAP_ANONYMOUS, …)` or use THP + `madvise(MADV_HUGEPAGE)`          | `[anon]` with huge pages    |
| File-backed huge page             | Open hugetlbfs file → `mmap(…, MAP_HUGETLB, hugepage_fd, …)`                            | `/hugepages/file`           |

### 3. Behavior & Kernel Internals Summary

| Scenario                              | File-backed (shared)                     | File-backed (private)                     | Anonymous (private)                     | Anonymous (shared)                     |
|---------------------------------------|------------------------------------------|-------------------------------------------|-----------------------------------------|----------------------------------------|
| First read fault                      | → page cache (or read from disk)         | → page cache (COW break on write)         | → zero page                             | → zero page                            |
| First write fault                     | → dirty page in page cache               | → private COW copy                        | → private COW copy                      | → private COW copy per process         |
| Changes visible to others?            | Yes (immediately)                        | No                                        | No                                      | Only after fork (COW)                  |
| Process exit / munmap                 | Dirty pages flushed to disk (if shared)  | Private pages discarded                   | Pages discarded (or swapped)            | Pages discarded (or swapped)           |
| Under memory pressure                 | Rarely swapped (file is source)          | Swapped if anonymous-like                 | Swapped aggressively                    | Swapped aggressively                   |
| fork() behavior                       | Shared mapping stays shared              | COW (private copy on write)               | COW                                     | COW (each child gets own copy)         |

### 4. Practical Examples

```c
// File-backed shared mapping (IPC / database)
int fd = open("data.dat", O_RDWR);
void *p = mmap(NULL, SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

// Anonymous private (typical malloc large block)
void *heap = mmap(NULL, SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

// Anonymous shared (inter-process without file)
void *shm = mmap(NULL, SIZE, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);

// After fork() — only MAP_SHARED file-backed stays truly shared
```

### 5. Debugging & Inspection

```bash
# See all mappings
cat /proc/<pid>/maps

# Detailed statistics (RSS, PSS, swap, private vs shared, THP…)
cat /proc/<pid>/smaps

# Look for anonymous vs file-backed
grep '\[anon\]' /proc/<pid>/maps
grep '/path/to/file' /proc/<pid>/maps

# Huge page usage per mapping
grep -A1 'KernelPageSize:' /proc/<pid>/smaps

# Transparent Huge Pages global status
cat /sys/kernel/mm/transparent_hugepage/enabled
```

**Quick rule of thumb (2026 perspective)**  
- Want **persistence** / **file content** / **shared across unrelated processes** → file-backed + `MAP_SHARED`  
- Want **fast zero-initialized memory** / **heap-like** / **temporary** → anonymous + `MAP_PRIVATE`  
- Want **shared memory without tmpfile** → anonymous + `MAP_SHARED` (but beware fork COW cost)

This covers the most important behavioral differences and use-cases you encounter when working with `mmap()` in Linux user-space or kernel code.