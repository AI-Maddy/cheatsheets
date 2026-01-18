================================================================================
Linux VFS and Filesystems - Comprehensive Cheatsheet
================================================================================

:Author: Linux Kernel Documentation Team
:Date: January 17, 2026
:Version: 1.0
:Target Audience: Kernel developers, filesystem engineers, storage architects
:Scope: VFS layer, ext4, tmpfs, procfs, sysfs, page cache, dentry cache

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
TL;DR - Quick Reference
================================================================================

**VFS Architecture (3-Layer Model)**:

.. code-block:: text

    ┌──────────────────────────────────────┐
    │  User Space                          │
    │  open(), read(), write(), stat()     │
    └─────────────┬────────────────────────┘
                  │ syscalls
                  ↓
    ┌──────────────────────────────────────┐
    │  VFS (Virtual Filesystem Switch)     │
    │  - struct inode (metadata)           │
    │  - struct dentry (directory entry)   │
    │  - struct file (open file)           │
    │  - struct super_block (filesystem)   │
    └─────┬────────┬────────┬──────────────┘
          │        │        │
          ↓        ↓        ↓
    ┌─────────┬────────┬────────┐
    │  ext4   │ tmpfs  │ procfs │  ... (filesystem implementations)
    └─────┬───┴────┬───┴────┬───┘
          │        │        │
          ↓        ↓        ↓
    ┌──────────────────────────────────────┐
    │  Block Layer / Memory / Virtual      │
    └──────────────────────────────────────┘

**Essential VFS Data Structures**:

+-------------------+-------------------------------------------------------+
| **Structure**     | **Purpose**                                           |
+===================+=======================================================+
| inode             | File metadata (permissions, size, timestamps, blocks) |
+-------------------+-------------------------------------------------------+
| dentry            | Directory entry (name → inode mapping, cached)        |
+-------------------+-------------------------------------------------------+
| file              | Open file instance (position, flags, reference)       |
+-------------------+-------------------------------------------------------+
| super_block       | Filesystem instance (mount point, root inode)         |
+-------------------+-------------------------------------------------------+
| file_operations   | File methods (read, write, ioctl, mmap)               |
+-------------------+-------------------------------------------------------+
| inode_operations  | Inode methods (create, lookup, link, unlink)          |
+-------------------+-------------------------------------------------------+

**Key VFS Operations**:

.. code-block:: c

    // File operations
    struct file_operations {
        ssize_t (*read)(struct file *, char __user *, size_t, loff_t *);
        ssize_t (*write)(struct file *, const char __user *, size_t, loff_t *);
        int (*open)(struct inode *, struct file *);
        int (*release)(struct inode *, struct file *);
        loff_t (*llseek)(struct file *, loff_t, int);
        int (*mmap)(struct file *, struct vm_area_struct *);
        long (*unlocked_ioctl)(struct file *, unsigned int, unsigned long);
    };
    
    // Inode operations
    struct inode_operations {
        struct dentry *(*lookup)(struct inode *, struct dentry *, unsigned int);
        int (*create)(struct inode *, struct dentry *, umode_t, bool);
        int (*link)(struct dentry *, struct inode *, struct dentry *);
        int (*unlink)(struct inode *, struct dentry *);
        int (*mkdir)(struct inode *, struct dentry *, umode_t);
        int (*rmdir)(struct inode *, struct dentry *);
    };

**Common Filesystem Commands**:

.. code-block:: bash

    # ext4 filesystem
    mkfs.ext4 -L mylabel -O ^has_journal /dev/sdb1    # Create without journal
    tune2fs -l /dev/sdb1                               # Show filesystem info
    tune2fs -O ^has_journal /dev/sdb1                  # Disable journal
    e2fsck -f /dev/sdb1                                # Force check
    dumpe2fs /dev/sdb1 | head -20                      # Show superblock
    
    # Mount options
    mount -t ext4 -o noatime,data=writeback /dev/sdb1 /mnt
    
    # tmpfs (memory filesystem)
    mount -t tmpfs -o size=1G,mode=0755 tmpfs /tmp
    
    # procfs/sysfs
    cat /proc/filesystems                              # List registered FS
    cat /proc/mounts                                   # Current mounts
    cat /sys/block/sda/queue/scheduler                 # I/O scheduler

**Dentry Cache (dcache)**:

.. code-block:: bash

    # View dcache statistics
    cat /proc/sys/fs/dentry-state
    # Output: nr_dentry  nr_unused  age_limit  want_pages
    #         123456     45678      45         0
    
    # Drop dcache (debug only!)
    echo 2 > /proc/sys/vm/drop_caches

**Inode Cache (icache)**:

.. code-block:: bash

    # View inode statistics
    cat /proc/sys/fs/inode-state
    # Output: nr_inodes  nr_free_inodes
    #         234567     123456
    
    # Drop icache and dcache
    echo 3 > /proc/sys/vm/drop_caches

**Page Cache**:

.. code-block:: bash

    # View page cache usage
    cat /proc/meminfo | grep -i cache
    # Cached:         12345678 kB
    # SwapCached:          123 kB
    
    # Per-file page cache (requires tools)
    pcstat /path/to/file               # Show % cached
    
    # Clear page cache only
    echo 1 > /proc/sys/vm/drop_caches

**Filesystem Comparison**:

+------------+----------+----------+----------+-----------+-----------+
| **Feature**| **ext4** | **XFS**  | **Btrfs**| **tmpfs** | **procfs**|
+============+==========+==========+==========+===========+===========+
| Journal    | Yes      | Yes      | CoW      | No        | No        |
+------------+----------+----------+----------+-----------+-----------+
| Max size   | 1 EB     | 8 EB     | 16 EB    | RAM limit | Virtual   |
+------------+----------+----------+----------+-----------+-----------+
| Snapshots  | No       | No       | Yes      | No        | No        |
+------------+----------+----------+----------+-----------+-----------+
| Online     | resize   | grow only| Yes      | remount   | N/A       |
| resize     |          |          |          |           |           |
+------------+----------+----------+----------+-----------+-----------+
| Use case   | General  | Large    | Advanced | Temporary | Kernel    |
|            | purpose  | files    | features | storage   | info      |
+------------+----------+----------+----------+-----------+-----------+

================================================================================
Section 1: VFS Architecture and Core Concepts
================================================================================

1.1 VFS Overview
================================================================================

**Purpose of VFS**:

The Virtual Filesystem Switch (VFS) provides:
1. **Unified interface** for all filesystem types
2. **Abstraction layer** between syscalls and filesystem implementations
3. **Caching** (dentry cache, inode cache, page cache)
4. **Namespace management** (mount points, file descriptors)

**Key Principle**: "Everything is a file"
- Regular files → read/write operations
- Directories → lookup/create operations
- Devices → device-specific ioctl
- Pipes/sockets → stream operations
- procfs/sysfs → virtual data

**VFS Object Model**:

.. code-block:: text

    Syscall: open("/home/user/file.txt", O_RDONLY)
           ↓
    ┌──────────────────────────────────────────────┐
    │ VFS Layer                                    │
    │                                              │
    │  1. Path Resolution                          │
    │     "/" → "home" → "user" → "file.txt"       │
    │     (uses dentry cache)                      │
    │                                              │
    │  2. Inode Lookup                             │
    │     dentry → inode (metadata)                │
    │     (uses inode cache)                       │
    │                                              │
    │  3. Open File Table Entry                    │
    │     Allocate struct file                     │
    │     Set file position = 0                    │
    │                                              │
    │  4. File Descriptor                          │
    │     Assign fd number (e.g., 3)               │
    │     Add to process fd table                  │
    └─────────────┬────────────────────────────────┘
                  │
                  ↓
            Return fd=3 to userspace

1.2 Core Data Structures
================================================================================

**struct inode** (File Metadata):

.. code-block:: c

    struct inode {
        umode_t         i_mode;       // File type + permissions (0644, S_IFREG)
        unsigned short  i_opflags;    // Inode operation flags
        kuid_t          i_uid;        // Owner UID
        kgid_t          i_gid;        // Owner GID
        unsigned int    i_flags;      // Filesystem flags
        
        // Operations
        const struct inode_operations   *i_op;
        struct super_block              *i_sb;
        
        // Size and blocks
        loff_t          i_size;       // File size in bytes
        struct timespec64 i_atime;    // Access time
        struct timespec64 i_mtime;    // Modification time
        struct timespec64 i_ctime;    // Status change time
        unsigned short  i_bytes;      // Bytes consumed (last block)
        unsigned int    i_blkbits;    // Block size in bits
        blkcnt_t        i_blocks;     // File size in blocks
        
        // File-specific data
        union {
            struct pipe_inode_info  *i_pipe;  // Pipe
            struct cdev             *i_cdev;  // Character device
            char                    *i_link;  // Symbolic link
        };
        
        // Address space (page cache)
        struct address_space    *i_mapping;
        struct address_space    i_data;
        
        // Inode cache
        struct hlist_node       i_hash;
        struct list_head        i_io_list;
        struct list_head        i_lru;
        
        // Inode number
        unsigned long           i_ino;
        atomic_t                i_count;    // Reference count
        unsigned int            i_nlink;    // Hard link count
    };

**Key Fields**:
- **i_mode**: File type (S_IFREG, S_IFDIR, S_IFLNK) + permissions (rwxrwxrwx)
- **i_size**: File size (important for read/write bounds)
- **i_blocks**: Number of 512-byte blocks allocated
- **i_mapping**: Pointer to page cache for this file
- **i_op**: Inode operations (lookup, create, unlink, etc.)

**struct dentry** (Directory Entry):

.. code-block:: c

    struct dentry {
        unsigned int            d_flags;        // Dentry flags
        seqcount_spinlock_t     d_seq;          // Sequence lock
        struct hlist_bl_node    d_hash;         // Lookup hash list
        struct dentry           *d_parent;      // Parent directory dentry
        struct qstr             d_name;         // Dentry name
        struct inode            *d_inode;       // Inode (NULL if negative)
        unsigned char           d_iname[DNAME_INLINE_LEN];  // Short names
        
        // Reference counting
        struct lockref          d_lockref;
        
        // Operations
        const struct dentry_operations *d_op;
        struct super_block      *d_sb;          // Superblock
        
        // Children
        struct list_head        d_child;        // Child of parent list
        struct list_head        d_subdirs;      // Our children
        
        // Aliasing (hard links)
        union {
            struct hlist_node   d_alias;        // Inode alias list
            struct hlist_bl_node d_in_lookup_hash;
            struct rcu_head     d_rcu;
        } d_u;
    };

**Dentry States**:
- **Positive**: d_inode != NULL (points to valid inode)
- **Negative**: d_inode == NULL (cached lookup failure)
- **Unhashed**: Not in dcache (temporary)

**struct file** (Open File Description):

.. code-block:: c

    struct file {
        union {
            struct llist_node   f_llist;
            struct rcu_head     f_rcuhead;
            unsigned int        f_iocb_flags;
        };
        
        struct path             f_path;         // Dentry + mount
        struct inode            *f_inode;       // Cached inode pointer
        const struct file_operations *f_op;
        
        // File position
        loff_t                  f_pos;          // Read/write position
        
        // Flags
        unsigned int            f_flags;        // O_RDONLY, O_WRONLY, etc.
        fmode_t                 f_mode;         // FMODE_READ, FMODE_WRITE
        
        // Reference counting
        atomic_long_t           f_count;
        
        // Credentials
        const struct cred       *f_cred;
        
        // Private data (filesystem-specific)
        void                    *private_data;
        
        // Address space
        struct address_space    *f_mapping;
    };

**struct super_block** (Filesystem Instance):

.. code-block:: c

    struct super_block {
        struct list_head        s_list;         // List of all superblocks
        dev_t                   s_dev;          // Device identifier
        unsigned char           s_blocksize_bits;
        unsigned long           s_blocksize;
        loff_t                  s_maxbytes;     // Max file size
        struct file_system_type *s_type;
        const struct super_operations *s_op;
        const struct dquot_operations *dq_op;
        const struct quotactl_ops *s_qcop;
        
        unsigned long           s_flags;        // Mount flags (MS_RDONLY)
        unsigned long           s_magic;        // Filesystem magic number
        struct dentry           *s_root;        // Root dentry
        
        int                     s_count;        // Reference count
        atomic_t                s_active;
        
        // Inode/dentry lists
        struct list_head        s_inodes;       // All inodes
        struct hlist_bl_head    s_roots;        // Dentry roots
        
        // Filesystem-specific data
        void                    *s_fs_info;
        
        // Writeback
        struct backing_dev_info *s_bdi;
        struct list_head        s_mounts;       // Mount instances
    };

1.3 VFS Operations
================================================================================

**file_operations** (File Methods):

.. code-block:: c

    struct file_operations {
        struct module *owner;
        
        // Position
        loff_t (*llseek)(struct file *, loff_t, int);
        
        // I/O
        ssize_t (*read)(struct file *, char __user *, size_t, loff_t *);
        ssize_t (*write)(struct file *, const char __user *, size_t, loff_t *);
        ssize_t (*read_iter)(struct kiocb *, struct iov_iter *);
        ssize_t (*write_iter)(struct kiocb *, struct iov_iter *);
        
        // Polling
        __poll_t (*poll)(struct file *, struct poll_table_struct *);
        
        // Control
        long (*unlocked_ioctl)(struct file *, unsigned int, unsigned long);
        long (*compat_ioctl)(struct file *, unsigned int, unsigned long);
        
        // Memory mapping
        int (*mmap)(struct file *, struct vm_area_struct *);
        
        // Open/close
        int (*open)(struct inode *, struct file *);
        int (*release)(struct inode *, struct file *);
        int (*flush)(struct file *, fl_owner_t id);
        
        // Synchronization
        int (*fsync)(struct file *, loff_t, loff_t, int datasync);
        
        // Directory
        int (*iterate_shared)(struct file *, struct dir_context *);
        
        // Locking
        int (*flock)(struct file *, int, struct file_lock *);
        int (*setlease)(struct file *, long, struct file_lock **, void **);
    };

**inode_operations** (Inode Methods):

.. code-block:: c

    struct inode_operations {
        // Lookup
        struct dentry *(*lookup)(struct inode *, struct dentry *, unsigned int);
        const char *(*get_link)(struct dentry *, struct inode *, struct delayed_call *);
        
        // Permissions
        int (*permission)(struct inode *, int);
        struct posix_acl *(*get_acl)(struct inode *, int);
        
        // File creation
        int (*create)(struct inode *, struct dentry *, umode_t, bool);
        int (*link)(struct dentry *, struct inode *, struct dentry *);
        int (*unlink)(struct inode *, struct dentry *);
        int (*symlink)(struct inode *, struct dentry *, const char *);
        int (*mkdir)(struct inode *, struct dentry *, umode_t);
        int (*rmdir)(struct inode *, struct dentry *);
        int (*mknod)(struct inode *, struct dentry *, umode_t, dev_t);
        int (*rename)(struct inode *, struct dentry *,
                      struct inode *, struct dentry *, unsigned int);
        
        // Attributes
        int (*setattr)(struct dentry *, struct iattr *);
        int (*getattr)(const struct path *, struct kstat *, u32, unsigned int);
        
        // Extended attributes
        ssize_t (*listxattr)(struct dentry *, char *, size_t);
        
        // Misc
        int (*update_time)(struct inode *, struct timespec64 *, int);
        int (*fiemap)(struct inode *, struct fiemap_extent_info *, u64 start, u64 len);
    };

**super_operations** (Superblock Methods):

.. code-block:: c

    struct super_operations {
        // Inode allocation
        struct inode *(*alloc_inode)(struct super_block *sb);
        void (*destroy_inode)(struct inode *);
        void (*free_inode)(struct inode *);
        
        // Writeback
        void (*dirty_inode)(struct inode *, int flags);
        int (*write_inode)(struct inode *, struct writeback_control *wbc);
        int (*drop_inode)(struct inode *);
        void (*evict_inode)(struct inode *);
        
        // Superblock operations
        void (*put_super)(struct super_block *);
        int (*sync_fs)(struct super_block *sb, int wait);
        int (*freeze_fs)(struct super_block *);
        int (*unfreeze_fs)(struct super_block *);
        int (*statfs)(struct dentry *, struct kstatfs *);
        int (*remount_fs)(struct super_block *, int *, char *);
        
        // Quotas
        int (*quota_read)(struct super_block *, int, char *, size_t, loff_t);
        int (*quota_write)(struct super_block *, int, const char *, size_t, loff_t);
    };

1.4 Path Resolution
================================================================================

**Path Lookup Algorithm**:

.. code-block:: text

    Example: open("/home/user/file.txt", O_RDONLY)
    
    Step 1: Start from root
    ├── current = root dentry ("/")
    └── remaining = "home/user/file.txt"
    
    Step 2: Lookup "home"
    ├── Search dcache for child "home" of "/"
    │   └── HIT: dentry cached
    ├── current = dentry("/home")
    └── remaining = "user/file.txt"
    
    Step 3: Lookup "user"
    ├── Search dcache for child "user" of "/home"
    │   └── HIT: dentry cached
    ├── current = dentry("/home/user")
    └── remaining = "file.txt"
    
    Step 4: Lookup "file.txt"
    ├── Search dcache for child "file.txt" of "/home/user"
    │   └── MISS: not in cache
    ├── Call inode->i_op->lookup()
    │   └── Filesystem reads directory block
    │       └── Finds entry: "file.txt" → inode 12345
    ├── Create dentry, link to inode
    ├── Add to dcache
    └── Return dentry("/home/user/file.txt")
    
    Step 5: Open file
    ├── Allocate struct file
    ├── file->f_path.dentry = found dentry
    ├── file->f_inode = dentry->d_inode
    ├── Call inode->i_fop->open()
    └── Return fd

**Dentry Cache Optimization**:

Frequently accessed paths are cached in dcache (hash table):
- **Key**: (parent_dentry, name_hash)
- **Value**: dentry pointer
- **Eviction**: LRU (least recently used)

**Negative Dentries**:

Failed lookups are also cached (negative dentry):
- d_inode == NULL
- Prevents repeated disk lookups for non-existent files
- Example: checking if config file exists

.. code-block:: c

    // Example: stat("/etc/nonexistent.conf")
    // First call: Disk lookup → not found → create negative dentry
    // Second call: Dcache hit (negative) → return -ENOENT immediately

1.5 File Descriptor Table
================================================================================

**Per-Process File Table**:

.. code-block:: c

    struct files_struct {
        atomic_t count;                    // Reference count
        struct fdtable __rcu *fdt;         // File descriptor table
        struct fdtable fdtab;              // Embedded table
        
        spinlock_t file_lock;
        unsigned int next_fd;              // Next available fd
        unsigned long close_on_exec_init[1];
        unsigned long open_fds_init[1];
        unsigned long full_fds_bits_init[1];
        struct file __rcu *fd_array[NR_OPEN_DEFAULT];  // fd → file mapping
    };

**File Descriptor Allocation**:

.. code-block:: c

    int get_unused_fd_flags(unsigned flags)
    {
        struct files_struct *files = current->files;
        int fd;
        
        spin_lock(&files->file_lock);
        fd = __alloc_fd(files, 0, rlimit(RLIMIT_NOFILE), flags);
        spin_unlock(&files->file_lock);
        
        return fd;
    }

**FD → File Mapping**:

.. code-block:: text

    Process A:
    fd_table[3] → struct file → dentry → inode (/tmp/file.txt)
    fd_table[4] → struct file → dentry → inode (/dev/null)
    
    Process B:
    fd_table[3] → struct file → dentry → inode (/var/log/app.log)
    fd_table[4] → struct file → dentry → inode (/tmp/file.txt)  [shared inode!]

**Shared vs. Private**:
- **Shared inode**: Multiple processes open same file → share inode/dentry
- **Private file**: Each open() creates new struct file (unique f_pos)
- **Inherited fd**: fork() duplicates fd table → children share struct file

================================================================================
Section 2: ext4 Filesystem
================================================================================

2.1 ext4 Overview
================================================================================

**Evolution**:

.. code-block:: text

    ext → ext2 → ext3 → ext4
    (1992) (1993)  (2001) (2008)
    
    ext2: Basic Unix filesystem (no journal)
    ext3: Added journaling (metadata + data)
    ext4: Extents, large files, delayed allocation, faster fsck

**Key Features**:
- **Extents**: Contiguous block ranges (not block lists)
- **Delayed allocation**: Block allocation deferred until writeback
- **Multi-block allocation**: Allocate many blocks at once (less fragmentation)
- **Journal checksumming**: Detect corruption in journal
- **Online defragmentation**: e4defrag while mounted
- **Large filesystem support**: Up to 1 exabyte (1 EB = 1,000,000 TB)

**ext4 Disk Layout**:

.. code-block:: text

    ┌───────────────┬──────────────┬──────────────┬─────────────┐
    │ Boot Block    │ Block Group 0│ Block Group 1│ ... Group N │
    │ (1024 bytes)  │              │              │             │
    └───────────────┴──────────────┴──────────────┴─────────────┘
    
    Each Block Group:
    ┌──────────────┬─────────────────┬────────────────┬──────────────────┐
    │ Super Block  │ Group Descriptor│ Block Bitmap   │ Inode Bitmap     │
    │ (backup)     │ Table           │ (data blocks)  │ (inode usage)    │
    └──────────────┴─────────────────┴────────────────┴──────────────────┘
    
    ┌──────────────┬──────────────────────────────────────────────────────┐
    │ Inode Table  │ Data Blocks                                          │
    │ (metadata)   │ (file contents)                                      │
    └──────────────┴──────────────────────────────────────────────────────┘

2.2 ext4 Extents
================================================================================

**Traditional vs Extent-Based**:

.. code-block:: text

    Traditional (ext2/3): Block list
    ┌────────┬────────┬────────┬────────┐
    │ Block 1│ Block 2│ Block 3│ Block 4│ ... (inefficient for large files)
    └────────┴────────┴────────┴────────┘
    
    Extent-based (ext4): Range
    ┌────────────────────────────┐
    │ Start: Block 1000          │
    │ Length: 1000 blocks        │  (single extent)
    └────────────────────────────┘

**ext4_extent Structure**:

.. code-block:: c

    struct ext4_extent {
        __le32  ee_block;        // First logical block number
        __le16  ee_len;          // Number of blocks covered
        __le16  ee_start_hi;     // High 16 bits of physical block
        __le32  ee_start_lo;     // Low 32 bits of physical block
    };

**Benefits**:
- Fewer metadata blocks needed
- Faster file access (fewer indirections)
- Better locality (contiguous allocation)

2.3 ext4 Journaling
================================================================================

**Journal Modes**:

+-------------------+-------------------------------+------------------------------+
| **Mode**          | **What's Journaled**          | **Performance vs Safety**    |
+===================+===============================+==============================+
| journal           | Metadata + data               | Slowest, safest              |
+-------------------+-------------------------------+------------------------------+
| ordered (default) | Metadata (data written first) | Balanced                     |
+-------------------+-------------------------------+------------------------------+
| writeback         | Metadata only                 | Fastest, less safe           |
+-------------------+-------------------------------+------------------------------+

**Mount Options**:

.. code-block:: bash

    # Ordered mode (default)
    mount -t ext4 -o data=ordered /dev/sdb1 /mnt
    
    # Writeback mode (faster, less safe)
    mount -t ext4 -o data=writeback /dev/sdb1 /mnt
    
    # Journal mode (slowest, safest)
    mount -t ext4 -o data=journal /dev/sdb1 /mnt
    
    # Disable journal (like ext2, for read-mostly filesystems)
    tune2fs -O ^has_journal /dev/sdb1

**Journal Commit Interval**:

.. code-block:: bash

    # Default: 5 seconds
    mount -t ext4 -o commit=30 /dev/sdb1 /mnt    # 30 second commits (more risk, better performance)

2.4 ext4 Commands
================================================================================

**Create Filesystem**:

.. code-block:: bash

    # Basic
    mkfs.ext4 /dev/sdb1
    
    # With options
    mkfs.ext4 -L mylabel -m 1 -O ^has_journal /dev/sdb1
    # -L: Label
    # -m: Reserved blocks % (default 5%, use 1% for large data disks)
    # -O: Enable/disable features (^feature disables)

**Filesystem Information**:

.. code-block:: bash

    # Show superblock
    dumpe2fs /dev/sdb1 | less
    
    # Key fields:
    # Filesystem volume name, UUID, magic number
    # Inode count, block count, free blocks
    # Block size, fragment size
    # Blocks per group, inodes per group
    # Journal size, journal inode

**Tune Filesystem**:

.. code-block:: bash

    # Change label
    tune2fs -L newlabel /dev/sdb1
    
    # Adjust reserved blocks
    tune2fs -m 1 /dev/sdb1
    
    # Enable/disable features
    tune2fs -O extent /dev/sdb1              # Enable extents
    tune2fs -O ^has_journal /dev/sdb1        # Disable journal
    
    # Set mount options (default)
    tune2fs -o user_xattr,acl /dev/sdb1

**Filesystem Check**:

.. code-block:: bash

    # Force check (unmounted!)
    e2fsck -f /dev/sdb1
    
    # Fix errors automatically
    e2fsck -fy /dev/sdb1
    
    # Check without fixing
    e2fsck -n /dev/sdb1

**Resize Filesystem**:

.. code-block:: bash

    # Grow (can be done online)
    resize2fs /dev/sdb1 50G
    
    # Grow to fill partition
    resize2fs /dev/sdb1
    
    # Shrink (must be offline!)
    umount /mnt
    e2fsck -f /dev/sdb1
    resize2fs /dev/sdb1 30G

**Defragmentation**:

.. code-block:: bash

    # Check fragmentation
    e4defrag -c /mnt/myfile
    # Output shows: fragmentation score
    
    # Defragment file
    e4defrag /mnt/myfile
    
    # Defragment directory recursively
    e4defrag /mnt/data/

================================================================================
Section 3: Virtual Filesystems
================================================================================

3.1 tmpfs (Temporary Filesystem in RAM)
================================================================================

**Overview**:

tmpfs stores files in virtual memory (RAM + swap):
- Very fast (no disk I/O)
- Volatile (data lost on reboot)
- Dynamic size (grows/shrinks with usage)
- Swappable (can use swap space)

**Common Uses**:
- /tmp directory (temporary files)
- /run directory (runtime data, systemd)
- Shared memory (/dev/shm)
- Build directories (fast compilation)

**Mount tmpfs**:

.. code-block:: bash

    # Basic mount
    mount -t tmpfs tmpfs /tmp
    
    # With size limit
    mount -t tmpfs -o size=2G tmpfs /tmp
    
    # With permissions
    mount -t tmpfs -o size=1G,mode=1777,uid=1000,gid=1000 tmpfs /home/user/temp
    
    # With inode limit
    mount -t tmpfs -o size=512M,nr_inodes=10k tmpfs /tmp

**tmpfs Options**:

+-------------------+--------------------------------------------------------+
| **Option**        | **Purpose**                                            |
+===================+========================================================+
| size=N            | Maximum size (default: 50% of RAM)                     |
+-------------------+--------------------------------------------------------+
| nr_inodes=N       | Maximum number of inodes                               |
+-------------------+--------------------------------------------------------+
| mode=M            | Permissions (octal, e.g., 1777 for sticky bit)         |
+-------------------+--------------------------------------------------------+
| uid=U, gid=G      | Owner                                                  |
+-------------------+--------------------------------------------------------+
| mpol=policy       | NUMA memory policy (default, prefer, bind, interleave) |
+-------------------+--------------------------------------------------------+

**Resize tmpfs** (online):

.. code-block:: bash

    # Increase size
    mount -o remount,size=4G /tmp
    
    # Check current usage
    df -h /tmp

**tmpfs vs ramfs**:

+-------------------+---------------------------+---------------------------+
| **Feature**       | **tmpfs**                 | **ramfs**                 |
+===================+===========================+===========================+
| Size limit        | Yes (configurable)        | No (can use all RAM!)     |
+-------------------+---------------------------+---------------------------+
| Swappable         | Yes                       | No                        |
+-------------------+---------------------------+---------------------------+
| Use case          | /tmp, /run, /dev/shm      | Initramfs only            |
+-------------------+---------------------------+---------------------------+

3.2 procfs (Process Information Filesystem)
================================================================================

**Overview**:

procfs provides kernel/process information as virtual files:
- Read-only (mostly) virtual files
- Generated on-the-fly (no disk storage)
- Standard interface for kernel data

**Common procfs Entries**:

.. code-block:: bash

    # Process information
    /proc/[pid]/cmdline          # Command line
    /proc/[pid]/exe              # Executable symlink
    /proc/[pid]/cwd              # Current working directory
    /proc/[pid]/environ          # Environment variables
    /proc/[pid]/fd/              # Open file descriptors
    /proc/[pid]/maps             # Memory mappings
    /proc/[pid]/stat             # Process statistics
    /proc/[pid]/status           # Human-readable status
    
    # System information
    /proc/cpuinfo                # CPU info
    /proc/meminfo                # Memory usage
    /proc/version                # Kernel version
    /proc/uptime                 # System uptime
    /proc/loadavg                # Load average
    /proc/stat                   # System statistics
    /proc/interrupts             # Interrupt counts
    /proc/diskstats              # Disk I/O statistics
    
    # Filesystem information
    /proc/mounts                 # Mounted filesystems
    /proc/filesystems            # Supported filesystems
    
    # Kernel parameters
    /proc/sys/kernel/            # Kernel tunables
    /proc/sys/vm/                # VM tunables
    /proc/sys/fs/                # Filesystem tunables
    /proc/sys/net/               # Network tunables

**Example Uses**:

.. code-block:: bash

    # Find process using file
    lsof /path/to/file
    # Or manually:
    grep -l "/path/to/file" /proc/*/maps
    
    # Check process memory
    cat /proc/12345/status | grep -i mem
    
    # Tune kernel parameter
    echo 1 > /proc/sys/net/ipv4/ip_forward    # Enable IP forwarding
    
    # View system load
    cat /proc/loadavg
    # Output: 0.52 0.43 0.39 2/345 12345
    #         1min 5min 15min running/total last_pid

**procfs Permissions**:

.. code-block:: bash

    # Some files are restricted
    ls -l /proc/1/
    # Most files owned by root (process owner)
    
    # Hide process info from other users (mount option)
    mount -o remount,hidepid=2 /proc
    # hidepid=0: Everyone can see all processes (default)
    # hidepid=1: Users can't access /proc/[pid]/ of other users
    # hidepid=2: Users can't even see PIDs of other users

3.3 sysfs (Device and Driver Information)
================================================================================

**Overview**:

sysfs exposes kernel objects (devices, drivers, buses) as files:
- Unified device model
- Read/write attributes
- Hierarchical structure (buses → devices → drivers)

**sysfs Structure**:

.. code-block:: text

    /sys/
    ├── block/                  # Block devices (sda, mmcblk0, etc.)
    ├── bus/                    # Buses (pci, usb, i2c, spi, etc.)
    ├── class/                  # Device classes (net, input, leds, etc.)
    ├── devices/                # Device hierarchy (by bus)
    ├── firmware/               # Firmware interfaces (acpi, efi)
    ├── fs/                     # Filesystem information
    ├── kernel/                 # Kernel parameters (mm, slab, etc.)
    ├── module/                 # Loaded modules
    └── power/                  # Power management

**Common sysfs Uses**:

.. code-block:: bash

    # Network interface info
    cat /sys/class/net/eth0/address           # MAC address
    cat /sys/class/net/eth0/speed             # Link speed (Mbps)
    cat /sys/class/net/eth0/carrier           # Link status (1=up, 0=down)
    cat /sys/class/net/eth0/statistics/rx_bytes
    
    # Block device info
    cat /sys/block/sda/size                   # Sectors
    cat /sys/block/sda/queue/scheduler        # I/O scheduler
    cat /sys/block/sda/queue/read_ahead_kb    # Read-ahead
    
    # LED control
    echo 1 > /sys/class/leds/led0/brightness  # Turn on
    echo 0 > /sys/class/leds/led0/brightness  # Turn off
    echo timer > /sys/class/leds/led0/trigger # Blink mode
    
    # CPU frequency scaling
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    
    # Module parameters
    cat /sys/module/printk/parameters/time    # printk timestamps
    echo Y > /sys/module/printk/parameters/time

**sysfs Permissions**:

Most sysfs files are:
- Read-only for regular users
- Writable by root (or specific groups via udev rules)

.. code-block:: bash

    # Udev rule to allow users to control LED
    # /etc/udev/rules.d/99-led.rules
    SUBSYSTEM=="leds", RUN+="/bin/chmod 666 /sys/class/leds/%k/brightness"

3.4 debugfs (Kernel Debugging Filesystem)
================================================================================

**Overview**:

debugfs is for kernel debugging/tracing data:
- Not for production use
- Requires root access
- Used by ftrace, kprobes, etc.

**Mount debugfs**:

.. code-block:: bash

    # Usually auto-mounted
    mount -t debugfs none /sys/kernel/debug
    
    # Or check if already mounted
    mount | grep debugfs

**Common debugfs Uses**:

.. code-block:: bash

    # ftrace (covered in Debug & Security cheatsheet)
    /sys/kernel/debug/tracing/
    
    # Block layer debugging
    /sys/kernel/debug/block/sda/
    
    # DRM (graphics) debugging
    /sys/kernel/debug/dri/0/
    
    # GPIO debugging
    /sys/kernel/debug/gpio

================================================================================
Section 4: Page Cache and Dentry Cache
================================================================================

4.1 Page Cache
================================================================================

**Purpose**:

Cache file contents in RAM to avoid disk I/O:
- Transparently caches read/write operations
- Writeback (delayed writes to disk)
- Read-ahead (prefetch sequential reads)

**Page Cache Structure**:

.. code-block:: c

    struct address_space {
        struct inode            *host;          // Owner inode
        struct xarray           i_pages;        // Page cache tree
        atomic_t                i_mmap_writable;
        
        const struct address_space_operations *a_ops;
        unsigned long           flags;
        spinlock_t              tree_lock;
        
        // Writeback
        struct list_head        i_mmap;         // Memory mappings
        unsigned long           nrpages;        // Number of pages
        pgoff_t                 writeback_index;
    };

**Page Cache Operations**:

.. code-block:: c

    struct address_space_operations {
        int (*writepage)(struct page *page, struct writeback_control *wbc);
        int (*readpage)(struct file *, struct page *);
        int (*write_begin)(struct file *, struct address_space *,
                           loff_t, unsigned len, unsigned flags,
                           struct page **, void **fsdata);
        int (*write_end)(struct file *, struct address_space *,
                         loff_t, unsigned len, unsigned copied,
                         struct page *, void *fsdata);
        sector_t (*bmap)(struct address_space *, sector_t);
        void (*invalidatepage)(struct page *, unsigned int, unsigned int);
        int (*releasepage)(struct page *, gfp_t);
        void (*freepage)(struct page *);
    };

**Read-Ahead**:

.. code-block:: bash

    # Check current read-ahead
    blockdev --getra /dev/sda
    # Output: 256 (sectors = 128 KB)
    
    # Set read-ahead (sectors)
    blockdev --setra 512 /dev/sda    # 256 KB
    
    # Per-file read-ahead hint (posix_fadvise)
    posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL);  // Large read-ahead
    posix_fadvise(fd, 0, 0, POSIX_FADV_RANDOM);      // Disable read-ahead

4.2 Dentry Cache (dcache)
================================================================================

**Purpose**:

Cache directory entries to speed up path lookups:
- Positive dentries (valid name → inode)
- Negative dentries (cached lookup failures)
- LRU eviction when memory pressure

**Dentry Hash Table**:

.. code-block:: text

    Hash Function: hash(parent_dentry, qstr_hash(name))
    
    Example: lookup("/home/user/file.txt")
    
    ┌─────────────────────────────────────────┐
    │ Dentry Hash Table                       │
    ├─────────────────────────────────────────┤
    │ hash(/, "home")     → dentry("/home")   │
    │ hash(/home, "user") → dentry("/home/user") │
    │ hash(/home/user, "file.txt") → dentry(...) │
    └─────────────────────────────────────────┘

**Dentry Cache Statistics**:

.. code-block:: bash

    cat /proc/sys/fs/dentry-state
    # Output: 123456 45678 45 0 0 0
    #         ^^^^^^ ^^^^^
    #         total  unused
    
    # Fields:
    # 1. nr_dentry:     Total dentry objects
    # 2. nr_unused:     Dentries not currently in use
    # 3. age_limit:     Age in seconds before reclaim (unused)
    # 4. want_pages:    Reclaim target (unused)
    # 5-6. dummy

**Reclaim Dentries**:

.. code-block:: bash

    # Drop dcache (debug only!)
    echo 2 > /proc/sys/vm/drop_caches
    
    # Drop page cache, dentries, and inodes
    echo 3 > /proc/sys/vm/drop_caches

**Negative Dentry Example**:

.. code-block:: c

    // First access: /etc/nonexistent.conf
    // 1. Lookup in dcache → miss
    // 2. Call filesystem lookup → returns -ENOENT
    // 3. Create negative dentry (d_inode = NULL)
    // 4. Add to dcache
    
    // Second access: /etc/nonexistent.conf
    // 1. Lookup in dcache → HIT (negative dentry)
    // 2. Return -ENOENT immediately (no disk I/O!)

================================================================================
Section 5: Exam Question
================================================================================

**Question (16 points): High-Performance Data Logger Filesystem Design**

You are designing a data logging system for an automotive black box that writes high-frequency sensor data (1000 samples/sec, 1 KB each) to storage. Requirements:

1. Data must survive power loss (crash consistency)
2. Minimize write amplification (flash wear)
3. Fast sequential writes
4. Minimal overhead (embedded system, limited RAM)
5. Separate metadata directory for quick queries

**Part A (5 points): Filesystem Selection and Configuration**

Given these requirements, choose between ext4, tmpfs (with periodic sync), and a custom filesystem approach. For your choice:

1. Justify filesystem selection
2. Specify mount options for optimal performance
3. Explain journal configuration (if applicable)
4. Describe data/metadata separation strategy

**Part B (5 points): VFS Integration**

Design the file operations structure for the data logger:

1. Implement write operation with:
   - Page cache usage (write-through vs writeback?)
   - Alignment requirements (block size matching)
   - Batch writes to reduce syscall overhead
   - Error handling for disk full scenarios

2. Implement mmap support:
   - Should the logger use mmap for zero-copy writes?
   - Pros/cons vs regular write()
   - Memory consistency guarantees

3. Implement fsync strategy:
   - When to call fsync (every N writes? timer-based?)
   - Performance impact analysis

**Part C (4 points): Caching Strategy**

Design caching to balance performance and crash consistency:

1. Page cache configuration:
   - Writeback delay tuning
   - Dirty page limits
   - Should logger use O_DIRECT? Why?

2. Dentry cache:
   - Impact of creating many files vs single large file
   - Negative dentry issue if checking for file existence

3. Inode cache:
   - Pre-allocating inodes to avoid allocation overhead

**Part D (2 points): Crash Recovery**

Describe recovery mechanism:

1. How to identify last valid entry after crash
2. Journal replay vs manual consistency check
3. Testing strategy to verify crash resilience

--------------------------------------------------------------------------------
**Answer:**
--------------------------------------------------------------------------------

**Part A: Filesystem Selection (5 points)**

**1. Filesystem Selection** (2 points):

**Choice: ext4 with optimized configuration**

**Justification**:

.. code-block:: text

    ✓ Crash Consistency:
      - Journal ensures metadata consistency
      - data=ordered guarantees writes before metadata
      - Survives unexpected power loss
    
    ✓ Flash Wear Reduction:
      - Extents reduce metadata updates
      - Delayed allocation coalesces writes
      - Large block sizes reduce fragmentation
    
    ✓ Sequential Write Performance:
      - Extents enable contiguous allocation
      - Multi-block allocator reduces overhead
      - Journal batching reduces commits
    
    ✗ tmpfs Rejected:
      - Volatile (data lost on crash) - violates requirement #1
      - Even with periodic sync, crash window exists
      - Better for temporary data only

**2. Mount Options** (2 points):

.. code-block:: bash

    # Optimal configuration for data logger
    mount -t ext4 -o \
        noatime,nodiratime,\        # Disable access time updates (reduces writes)
        data=writeback,\            # Fast mode (metadata journaled, data not)
        commit=30,\                 # Longer journal commit interval (less overhead)
        barrier=1,\                 # Enable write barriers (flash crash safety)
        delalloc,\                  # Delayed allocation (better contiguity)
        stripe=256,\                # Stripe size for RAID/flash alignment
        inode_readahead_blks=64 \   # Prefetch inodes (faster metadata access)
        /dev/mmcblk0p1 /var/log/blackbox

**Explanation**:
- **noatime**: Saves 33% writes (no atime updates on reads)
- **data=writeback**: Metadata journaled, data written directly (faster)
- **commit=30**: 30-second journal commits (vs default 5s) - reduces overhead
- **barrier=1**: Ensures flash completes writes before proceeding (crash safety)
- **delalloc**: Accumulates writes before allocation (better layout)

**3. Journal Configuration** (1 point):

.. code-block:: bash

    # Create filesystem with optimized journal
    mkfs.ext4 -J size=256 -b 4096 -E stride=64,stripe-width=256 /dev/mmcblk0p1
    
    # Journal size: 256 MB (larger = fewer commits, more buffering)
    # Block size: 4 KB (matches typical flash erase block sub-page)
    # Stride/stripe: Flash geometry alignment

**Part B: VFS Integration (5 points)**

**1. Write Operation Implementation** (2 points):

.. code-block:: c

    // file_operations for data logger
    static const struct file_operations blackbox_fops = {
        .owner = THIS_MODULE,
        .write_iter = blackbox_write_iter,
        .open = blackbox_open,
        .release = blackbox_release,
        .fsync = blackbox_fsync,
    };
    
    // Optimized write implementation
    static ssize_t blackbox_write_iter(struct kiocb *iocb, struct iov_iter *from)
    {
        struct file *file = iocb->ki_filp;
        struct inode *inode = file_inode(file);
        ssize_t ret;
        size_t count = iov_iter_count(from);
        
        // Alignment check (4 KB blocks)
        if (count % 4096 != 0) {
            pr_warn("blackbox: Unaligned write %zu bytes, padding to 4K\n", count);
            count = ALIGN(count, 4096);
        }
        
        // Use page cache (writeback mode)
        // NOT O_DIRECT - let kernel batch writes
        ret = generic_file_write_iter(iocb, from);
        if (ret < 0) {
            if (ret == -ENOSPC) {
                // Disk full - critical error!
                pr_err("blackbox: Storage full, data loss imminent\n");
                // Could trigger emergency mode: stop new logs, sync critical data
                blackbox_emergency_sync(inode);
            }
            return ret;
        }
        
        // Update file size metadata
        if (ret > 0)
            blackbox_update_stats(inode, ret);
        
        return ret;
    }
    
    // Batch write from userspace (1000 samples/sec × 1 KB = 1 MB/sec)
    int blackbox_log_samples(int fd, struct sample *samples, int count)
    {
        // Write in 1 MB batches (1000 samples)
        ssize_t written = write(fd, samples, count * sizeof(struct sample));
        if (written < 0)
            return -errno;
        
        return written / sizeof(struct sample);
    }

**Strategy**:
- **Use page cache** (not O_DIRECT): Kernel batches writes, better performance
- **Writeback mode**: Async writes to disk, fsync() controls persistence
- **4 KB alignment**: Matches filesystem block size, reduces RMW cycles
- **Batch writes**: Userspace writes 1000 samples at once (reduces syscalls)

**2. mmap Support** (2 points):

.. code-block:: c

    static int blackbox_mmap(struct file *file, struct vm_area_struct *vma)
    {
        // Allow mmap for shared memory producer-consumer pattern
        return generic_file_mmap(file, vma);
    }
    
    // Userspace usage (alternative design)
    int use_mmap_logger(const char *path)
    {
        int fd = open(path, O_RDWR | O_CREAT, 0644);
        size_t size = 100 * 1024 * 1024;  // 100 MB ring buffer
        
        ftruncate(fd, size);
        void *buf = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
        if (buf == MAP_FAILED)
            return -1;
        
        // Ring buffer: write position tracked separately
        struct sample *ring = buf;
        int pos = 0;
        
        while (1) {
            struct sample s = get_sensor_data();
            ring[pos % (size / sizeof(struct sample))] = s;
            pos++;
            
            // Periodic msync for persistence
            if (pos % 10000 == 0) {
                msync(buf, size, MS_ASYNC);
            }
        }
    }

**Pros vs Cons**:

+---------------------+---------------------------------------+---------------------------------------+
| **Aspect**          | **mmap (MS_ASYNC)**                   | **write() + fsync()**                 |
+=====================+=======================================+=======================================+
| Performance         | ✓ Zero-copy (no user-kernel copy)     | ✗ Copy to page cache                  |
+---------------------+---------------------------------------+---------------------------------------+
| Crash consistency   | ✗ Weak (need explicit msync)          | ✓ Strong (fsync guarantees)           |
+---------------------+---------------------------------------+---------------------------------------+
| Memory overhead     | ✗ Large (entire file mapped)          | ✓ Small (only dirty pages)            |
+---------------------+---------------------------------------+---------------------------------------+
| Complexity          | ✗ Higher (ring buffer logic)          | ✓ Simple sequential writes            |
+---------------------+---------------------------------------+---------------------------------------+

**Recommendation**: Use **write() + periodic fsync()** for automotive safety:
- Explicit control over persistence
- Better error handling (write failures immediately visible)
- Lower memory footprint (100 MB mmap vs few MB page cache)

**3. fsync Strategy** (1 point):

.. code-block:: c

    // Option 1: Time-based fsync (every N seconds)
    static void blackbox_fsync_timer(struct timer_list *t)
    {
        struct blackbox_file *bf = from_timer(bf, t, sync_timer);
        
        vfs_fsync(bf->file, 0);  // Full fsync (data + metadata)
        
        // Re-arm timer for next interval (e.g., 5 seconds)
        mod_timer(&bf->sync_timer, jiffies + msecs_to_jiffies(5000));
    }
    
    // Option 2: Count-based fsync (every N writes)
    #define FSYNC_INTERVAL 10000  // Sync every 10,000 samples (10 seconds @ 1000 Hz)
    
    static ssize_t blackbox_write_iter(...)
    {
        // ... write logic ...
        
        atomic_inc(&bf->write_count);
        if (atomic_read(&bf->write_count) >= FSYNC_INTERVAL) {
            vfs_fsync(file, 0);
            atomic_set(&bf->write_count, 0);
        }
    }

**Performance Impact**:

.. code-block:: text

    fsync() cost: ~50 ms (flash storage, depends on dirty data amount)
    
    Without fsync:
    - Throughput: 1 MB/s (1000 samples/sec × 1 KB)
    - Latency: <1 ms (page cache write)
    
    With fsync every 5 seconds:
    - Throughput: 1 MB/s (unchanged, async)
    - Latency spike: 50 ms every 5 seconds (acceptable for logger)
    - Data loss window: Max 5 seconds of data on crash
    
    With fsync every write:
    - Throughput: ~20 KB/s (50 ms per 1 KB write = 20 writes/sec)
    - 50x slowdown - UNACCEPTABLE

**Chosen Strategy**: **5-second timer-based fsync**
- Balances crash resilience (max 5s data loss) with performance
- Allows page cache to batch writes
- Predictable sync intervals

**Part C: Caching Strategy (4 points)**

**1. Page Cache Configuration** (2 points):

.. code-block:: bash

    # Tune writeback parameters for logger workload
    
    # Writeback delay: How long dirty pages stay in cache before writeback
    echo 3000 > /proc/sys/vm/dirty_expire_centisecs    # 30 seconds (default: 30s)
    
    # Dirty page limits
    echo 10 > /proc/sys/vm/dirty_background_ratio      # Start writeback at 10% RAM
    echo 20 > /proc/sys/vm/dirty_ratio                 # Block writes at 20% RAM
    
    # Writeback aggressiveness
    echo 10 > /proc/sys/vm/dirty_writeback_centisecs   # Wake flusher every 0.1s (default: 5s)

**O_DIRECT Analysis**:

.. code-block:: c

    // Should logger use O_DIRECT?
    int fd = open("/var/log/blackbox/data.bin", O_WRONLY | O_CREAT | O_DIRECT, 0644);

**Pros**:
- ✓ Bypasses page cache (no RAM overhead)
- ✓ Predictable latency (no writeback storms)
- ✓ Suitable for write-once data (no re-read benefit from cache)

**Cons**:
- ✗ Must align writes to block size (4 KB)
- ✗ No kernel write batching (more syscalls)
- ✗ Harder to implement correctly

**Verdict**: **Use buffered I/O (no O_DIRECT)**
- Page cache batching improves throughput
- Writeback tuning controls RAM usage
- Periodic fsync() provides persistence guarantees
- Simpler code (kernel handles alignment)

**2. Dentry Cache Impact** (1 point):

.. code-block:: text

    Design Option 1: Many small files
    /var/log/blackbox/
        data_20260117_100000.bin  (1000 samples = 1 MB)
        data_20260117_100001.bin
        ...
        data_20260117_235959.bin  (86400 files per day!)
    
    Dentry cache overhead:
    - 86,400 dentries × ~192 bytes = 16 MB RAM
    - Frequent open/close overhead
    - Negative dentry pollution (checking for existing files)
    
    Design Option 2: Single large file (ring buffer)
    /var/log/blackbox/data.bin  (e.g., 10 GB, overwrite oldest)
    
    Dentry cache overhead:
    - 1 dentry = 192 bytes RAM
    - Open once, keep fd open
    - No lookup overhead
    
    Verdict: Single large file (ring buffer)

**3. Inode Cache** (1 point):

.. code-block:: bash

    # Pre-allocate inodes (ext4 defaults)
    mkfs.ext4 -N 100000 /dev/mmcblk0p1
    # Allocates 100,000 inodes upfront (vs default calculation)
    
    # Benefit: Avoids inode allocation overhead during writes
    # Cost: More disk space for inode table

**Part D: Crash Recovery (2 points)**

**1. Last Valid Entry Identification** (1 point):

.. code-block:: c

    // Data structure with sequence numbers
    struct blackbox_sample {
        uint64_t seq;          // Monotonic sequence number
        uint64_t timestamp;    // Microseconds since boot
        uint32_t crc32;        // CRC of data + seq + timestamp
        uint8_t  data[1024 - 20];
    };
    
    // Recovery: Find last valid sample
    int blackbox_recover(const char *path)
    {
        int fd = open(path, O_RDONLY);
        struct blackbox_sample sample;
        uint64_t last_valid_seq = 0;
        
        while (read(fd, &sample, sizeof(sample)) == sizeof(sample)) {
            // Verify CRC
            uint32_t computed_crc = crc32(0, &sample, sizeof(sample) - 4);
            if (computed_crc != sample.crc32) {
                // Corruption detected - last_valid_seq is latest
                break;
            }
            
            // Check sequence monotonicity
            if (sample.seq != last_valid_seq + 1) {
                pr_warn("blackbox: Sequence gap %llu -> %llu\n", 
                        last_valid_seq, sample.seq);
                break;
            }
            
            last_valid_seq = sample.seq;
        }
        
        printf("Last valid sequence: %llu\n", last_valid_seq);
        return 0;
    }

**2. Journal Replay** (1/2 point):

ext4 journal automatically replays on mount:
- Ensures filesystem metadata consistency
- Recovers in-flight metadata operations
- **Does NOT** recover application data (that's our CRC job)

**3. Testing Strategy** (1/2 point):

.. code-block:: bash

    # Crash resilience testing
    
    # Test 1: Power-loss simulation during writes
    while true; do
        # Write data
        ./blackbox_logger &
        sleep $((RANDOM % 10 + 1))  # Random 1-10 seconds
        
        # Simulate power loss
        echo b > /proc/sysrq-trigger  # Emergency reboot
        
        # After reboot: verify recovery
        ./blackbox_verify
    done
    
    # Test 2: Disk full scenario
    dd if=/dev/zero of=/var/log/blackbox/fill bs=1M count=10000
    ./blackbox_logger  # Should handle ENOSPC gracefully
    
    # Test 3: Filesystem corruption
    umount /var/log/blackbox
    dd if=/dev/urandom of=/dev/mmcblk0p1 bs=4096 count=1 seek=1000  # Corrupt random block
    mount /var/log/blackbox
    ./blackbox_verify  # Should detect corruption via CRC

================================================================================
Section 6: Best Practices
================================================================================

**VFS Development**:
✓ Always use VFS helper functions (generic_file_read_iter, etc.)
✓ Implement reference counting correctly (iget/iput, dget/dput)
✓ Use RCU for lockless path lookups
✓ Validate userspace pointers (copy_from_user/copy_to_user)
✓ Handle EINTR/ERESTARTSYS for interruptible operations
✓ Set file_operations.owner = THIS_MODULE

**Filesystem Implementation**:
✓ Use established patterns (ext4, XFS as reference)
✓ Test with xfstests suite (filesystem stress tests)
✓ Implement fsync/sync properly (don't ignore!)
✓ Handle disk full (ENOSPC) gracefully
✓ Use extent-based allocation (not block lists)
✓ Implement read-ahead for sequential workloads

**Performance**:
✓ Use page cache for frequently accessed data
✓ Tune writeback parameters for workload
✓ Minimize dentry cache pollution (reuse dentries)
✓ Batch operations (don't create many small files)
✓ Align I/O to block sizes
✓ Consider O_DIRECT only for specialized workloads (databases)

**Crash Consistency**:
✓ Use journaling for metadata (ext4, XFS)
✓ Implement application-level checksums (CRC32)
✓ Test with power-loss scenarios
✓ Use write barriers on flash/RAID
✓ fsync() before closing critical files

**Security**:
✓ Validate permissions in inode_operations
✓ Use namespaces for isolation
✓ Implement quotas for multi-user systems
✓ Sanitize extended attributes
✓ Check file size limits

================================================================================
Section 7: Key Takeaways
================================================================================

**VFS Architecture**:
✓ VFS provides unified interface for all filesystems
✓ 4 core objects: inode (metadata), dentry (name), file (open instance), super_block (filesystem)
✓ Path lookup uses dentry cache (dcache) for performance
✓ File content cached in page cache
✓ Each open() creates new struct file (unique position), but shares inode/dentry

**ext4 Filesystem**:
✓ Evolution: ext → ext2 (no journal) → ext3 (journal) → ext4 (extents)
✓ Extents: Contiguous block ranges (more efficient than block lists)
✓ Journal modes: journal (safest), ordered (default), writeback (fastest)
✓ Max file size: 16 TB (with 4 KB blocks)
✓ Max filesystem size: 1 EB

**Virtual Filesystems**:
✓ tmpfs: RAM-based, fast, volatile (perfect for /tmp, /run)
✓ procfs: Kernel/process information (read-only virtual files)
✓ sysfs: Device model (hierarchical device tree)
✓ debugfs: Debugging/tracing data (ftrace, kprobes)

**Caching**:
✓ Dentry cache: Speeds up path lookups (positive + negative dentries)
✓ Inode cache: Cached inode structures
✓ Page cache: File content cache (read/write buffering)
✓ Writeback: Delayed writes to disk (tunable via /proc/sys/vm)
✓ drop_caches: Debug tool (1=page, 2=dentry/inode, 3=all)

**Best Practices**:
✓ Use buffered I/O unless strong reason for O_DIRECT
✓ Tune writeback for workload (dirty_ratio, dirty_expire_centisecs)
✓ Single large file > many small files (dentry cache efficiency)
✓ fsync() controls persistence (don't rely on page cache timing)
✓ Test crash scenarios (power loss, disk full, corruption)

================================================================================
References
================================================================================

- Documentation/filesystems/vfs.rst
- Documentation/filesystems/ext4/
- "Understanding the Linux Kernel" - Bovet & Cesati
- "Professional Linux Kernel Architecture" - Wolfgang Mauerer (Chapters 8-11)
- "Linux Kernel Development" - Robert Love
- ext4 wiki: https://ext4.wiki.kernel.org
- xfstests: https://git.kernel.org/pub/scm/fs/xfs/xfstests-dev.git

================================================================================
End of Document
================================================================================

