=======================================
Linux Kernel Architecture
=======================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Focus: Linux kernel structure, components, and design

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Kernel Structure
----------------

.. code-block:: text

   Linux Kernel Architecture:
   
   User Space
   ├── Applications
   ├── Libraries (glibc, etc.)
   └── System Call Interface
   
   Kernel Space
   ├── System Call Layer
   ├── Process Management
   │   ├── Scheduler
   │   ├── Process Creation/Termination
   │   └── Signal Handling
   ├── Memory Management
   │   ├── Virtual Memory
   │   ├── Page Allocation
   │   └── Slab Allocator
   ├── File Systems
   │   ├── VFS (Virtual File System)
   │   ├── Specific FS (ext4, XFS, etc.)
   │   └── Block Layer
   ├── Device Drivers
   │   ├── Character Devices
   │   ├── Block Devices
   │   └── Network Devices
   ├── Network Stack
   │   ├── Protocol Layers (TCP/IP)
   │   ├── Socket Interface
   │   └── Network Devices
   └── Architecture-Specific Code
       ├── CPU Management
       ├── MMU Handling
       └── Interrupt Handling
   
   Hardware
   ├── CPU
   ├── Memory
   ├── Devices
   └── Buses

Essential Kernel Paths
----------------------

.. code-block:: text

   Kernel Source Tree:
   
   arch/           # Architecture-specific code
   block/          # Block layer
   crypto/         # Cryptographic API
   Documentation/  # Kernel documentation
   drivers/        # Device drivers
   fs/             # File systems
   include/        # Header files
   init/           # Initialization code
   ipc/            # Inter-process communication
   kernel/         # Core kernel code
   lib/            # Library routines
   mm/             # Memory management
   net/            # Networking
   scripts/        # Build scripts
   security/       # Security modules (SELinux, etc.)
   sound/          # Sound subsystem
   tools/          # Kernel tools
   usr/            # Built-in initramfs
   virt/           # Virtualization (KVM)

Kernel Components Overview
===========================

Core Subsystems
---------------

.. code-block:: text

   1. Process Scheduler
      - Completely Fair Scheduler (CFS)
      - Real-time schedulers (FIFO, RR, DEADLINE)
      - Load balancing
      - CPU affinity
   
   2. Memory Management
      - Virtual memory
      - Page cache
      - Slab allocator
      - Out-of-memory killer
      - Memory compaction
   
   3. Virtual File System (VFS)
      - File system abstraction
      - Dentry cache
      - Inode cache
      - Page cache
   
   4. Block I/O Layer
      - Request queues
      - I/O schedulers
      - Device mapper
      - Multi-queue block layer
   
   5. Network Stack
      - Socket layer
      - Protocol families (IPv4, IPv6)
      - Network device interface
      - Packet scheduling
   
   6. Device Model
      - kobjects
      - sysfs
      - Device/driver binding
      - Hot-plug events
   
   7. Inter-Process Communication
      - Signals
      - Pipes
      - Message queues
      - Shared memory
      - Semaphores

System Call Interface
=====================

System Call Flow
----------------

.. code-block:: text

   User Space Application
         |
         | Library call (glibc)
         v
   System Call Wrapper
         |
         | Software interrupt (int 0x80 or syscall)
         v
   System Call Handler (entry_64.S)
         |
         | sys_call_table lookup
         v
   Specific System Call (kernel space)
         |
         | Execute kernel function
         v
   Return to User Space

System Call Implementation
--------------------------

.. code-block:: c

   // Define system call
   SYSCALL_DEFINE3(read, unsigned int, fd, char __user *, buf, size_t, count)
   {
       struct fd f = fdget_pos(fd);
       ssize_t ret = -EBADF;
       
       if (f.file) {
           loff_t pos = file_pos_read(f.file);
           ret = vfs_read(f.file, buf, count, &pos);
           if (ret >= 0)
               file_pos_write(f.file, pos);
           fdput_pos(f);
       }
       return ret;
   }
   
   // System call table entry (auto-generated)
   // arch/x86/entry/syscalls/syscall_64.tbl
   // 0     common  read    sys_read

User Space to Kernel Transition
--------------------------------

.. code-block:: c

   // User space (glibc)
   ssize_t read(int fd, void *buf, size_t count) {
       return syscall(__NR_read, fd, buf, count);
   }
   
   // Kernel entry (arch/x86/entry/entry_64.S)
   ENTRY(entry_SYSCALL_64)
       swapgs                  // Swap GS register
       movq %rsp, PER_CPU_VAR(rsp_scratch)
       movq PER_CPU_VAR(cpu_current_top_of_stack), %rsp
       
       pushq $__USER_DS
       pushq PER_CPU_VAR(rsp_scratch)
       pushq %r11              // RFLAGS
       pushq $__USER_CS
       pushq %rcx              // Return address
       
       // Save registers
       pushq %rax
       pushq %rdi
       // ... more registers
       
       call do_syscall_64      // Call system call handler
       
       // Restore and return
   END(entry_SYSCALL_64)

Process Management
==================

Process Representation
----------------------

.. code-block:: c

   // include/linux/sched.h
   struct task_struct {
       volatile long state;          // Process state
       void *stack;                  // Kernel stack pointer
       unsigned int flags;           // Process flags
       int prio, static_prio, normal_prio;  // Priority
       
       struct mm_struct *mm, *active_mm;  // Memory descriptor
       
       pid_t pid;                    // Process ID
       pid_t tgid;                   // Thread group ID
       
       struct task_struct *parent;   // Parent process
       struct list_head children;    // List of children
       struct list_head sibling;     // Sibling processes
       
       struct fs_struct *fs;         // File system info
       struct files_struct *files;   // Open files
       struct signal_struct *signal; // Signal handlers
       
       struct sched_entity se;       // Scheduler entity
       struct sched_rt_entity rt;    // Real-time entity
       struct sched_dl_entity dl;    // Deadline entity
       
       cpumask_t cpus_allowed;       // CPU affinity
       
       struct thread_struct thread;  // CPU-specific state
       
       // ... many more fields
   };

Process States
--------------

.. code-block:: c

   // Process states (state field)
   #define TASK_RUNNING            0  // Running or runnable
   #define TASK_INTERRUPTIBLE      1  // Sleeping, can be interrupted
   #define TASK_UNINTERRUPTIBLE    2  // Sleeping, cannot be interrupted
   #define __TASK_STOPPED          4  // Stopped (SIGSTOP)
   #define __TASK_TRACED           8  // Being traced (ptrace)
   #define EXIT_ZOMBIE            16  // Zombie (exited, parent not waited)
   #define EXIT_DEAD              32  // Dead (being removed)
   
   // Check states
   #define task_is_running(task)        (READ_ONCE((task)->__state) == TASK_RUNNING)
   #define task_is_stopped(task)        ((task)->__state & __TASK_STOPPED)
   #define task_is_traced(task)         ((task)->__state & __TASK_TRACED)

Process Creation
----------------

.. code-block:: c

   // Fork system call
   SYSCALL_DEFINE0(fork)
   {
       return _do_fork(SIGCHLD, 0, 0, NULL, NULL, 0);
   }
   
   // Generic fork implementation
   long _do_fork(unsigned long clone_flags,
                 unsigned long stack_start,
                 unsigned long stack_size,
                 int __user *parent_tidptr,
                 int __user *child_tidptr,
                 unsigned long tls)
   {
       struct task_struct *p;
       int trace = 0;
       long nr;
       
       // Copy process descriptor and set up new process
       p = copy_process(clone_flags, stack_start, stack_size,
                       parent_tidptr, child_tidptr, tls);
       
       if (IS_ERR(p))
           return PTR_ERR(p);
       
       // Get new PID
       nr = task_pid_vnr(p);
       
       // Wake up new process
       wake_up_new_task(p);
       
       return nr;
   }

Kernel Threads
--------------

.. code-block:: c

   #include <linux/kthread.h>
   
   // Kernel thread function
   static int my_kthread_func(void *data) {
       while (!kthread_should_stop()) {
           // Do work
           pr_info("Kernel thread running\n");
           
           // Sleep
           schedule_timeout_interruptible(HZ);  // 1 second
       }
       
       return 0;
   }
   
   // Create kernel thread
   static struct task_struct *my_kthread;
   
   my_kthread = kthread_create(my_kthread_func, NULL, "my_kthread");
   if (IS_ERR(my_kthread)) {
       pr_err("Failed to create kernel thread\n");
       return PTR_ERR(my_kthread);
   }
   
   wake_up_process(my_kthread);
   
   // Or use helper
   my_kthread = kthread_run(my_kthread_func, NULL, "my_kthread");
   
   // Stop kernel thread
   kthread_stop(my_kthread);

Memory Management Basics
=========================

Memory Zones
------------

.. code-block:: c

   // Memory zones
   enum zone_type {
       ZONE_DMA,        // < 16 MB (ISA DMA)
       ZONE_DMA32,      // < 4 GB (32-bit DMA)
       ZONE_NORMAL,     // Normal memory
       ZONE_HIGHMEM,    // > 896 MB (32-bit only)
       ZONE_MOVABLE,    // Hot-pluggable memory
       ZONE_DEVICE,     // Device memory
       __MAX_NR_ZONES
   };
   
   // Node (NUMA)
   struct pglist_data {
       struct zone node_zones[MAX_NR_ZONES];
       int node_id;
       struct page *node_mem_map;
       unsigned long node_start_pfn;  // Page frame number
       unsigned long node_present_pages;
       unsigned long node_spanned_pages;
   };

Page Structure
--------------

.. code-block:: c

   // struct page represents a physical page
   struct page {
       unsigned long flags;          // Page flags (PG_locked, PG_dirty, etc.)
       atomic_t _refcount;           // Reference count
       atomic_t _mapcount;           // Page table references
       
       union {
           struct address_space *mapping;  // File mapping
           void *s_mem;                    // Slab cache
       };
       
       pgoff_t index;                // Offset in file
       
       struct list_head lru;         // LRU list
       
       // ... architecture-specific fields
   };
   
   // Page flags
   #define PG_locked        0  // Page is locked
   #define PG_error         1  // I/O error
   #define PG_referenced    2  // Recently accessed
   #define PG_uptodate      3  // Page data valid
   #define PG_dirty         4  // Page modified
   #define PG_lru           5  // On LRU list
   #define PG_active        6  // On active list
   #define PG_slab          7  // Slab page
   #define PG_reserved      9  // Reserved page

Virtual File System
===================

VFS Objects
-----------

.. code-block:: c

   // Superblock - represents a mounted filesystem
   struct super_block {
       struct list_head s_list;          // List of superblocks
       dev_t s_dev;                      // Device identifier
       unsigned long s_blocksize;        // Block size
       unsigned char s_blocksize_bits;   // Block size in bits
       loff_t s_maxbytes;                // Max file size
       struct file_system_type *s_type;  // Filesystem type
       const struct super_operations *s_op;
       unsigned long s_flags;
       unsigned long s_magic;
       struct dentry *s_root;            // Root dentry
       struct list_head s_inodes;        // All inodes
       struct list_head s_dirty;         // Dirty inodes
   };
   
   // Inode - represents a file
   struct inode {
       umode_t i_mode;                   // File permissions
       unsigned int i_flags;
       uid_t i_uid;                      // Owner
       gid_t i_gid;                      // Group
       loff_t i_size;                    // File size
       struct timespec i_atime;          // Access time
       struct timespec i_mtime;          // Modification time
       struct timespec i_ctime;          // Change time
       unsigned long i_blkbits;          // Block size in bits
       unsigned int i_nlink;             // Hard link count
       dev_t i_rdev;                     // Device number
       struct super_block *i_sb;         // Superblock
       const struct inode_operations *i_op;
       const struct file_operations *i_fop;
       struct address_space *i_mapping;  // Page cache
       struct address_space i_data;      // Private page cache
   };
   
   // Dentry - directory entry (path component)
   struct dentry {
       unsigned int d_flags;
       struct inode *d_inode;            // Associated inode
       struct dentry *d_parent;          // Parent dentry
       struct qstr d_name;               // Entry name
       struct list_head d_child;         // Child entries
       struct list_head d_subdirs;       // Subdirectories
       const struct dentry_operations *d_op;
       struct super_block *d_sb;
       void *d_fsdata;                   // FS-specific data
   };
   
   // File - represents an open file
   struct file {
       struct path f_path;               // Dentry and vfsmount
       struct inode *f_inode;            // Cached inode
       const struct file_operations *f_op;
       atomic_long_t f_count;            // Reference count
       unsigned int f_flags;             // Open flags (O_RDONLY, etc.)
       fmode_t f_mode;                   // File mode
       loff_t f_pos;                     // File position
       void *private_data;               // Driver-specific data
   };

VFS Operations
--------------

.. code-block:: c

   struct file_operations {
       struct module *owner;
       loff_t (*llseek) (struct file *, loff_t, int);
       ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
       ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
       __poll_t (*poll) (struct file *, struct poll_table_struct *);
       long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
       int (*mmap) (struct file *, struct vm_area_struct *);
       int (*open) (struct inode *, struct file *);
       int (*release) (struct inode *, struct file *);
       int (*fsync) (struct file *, loff_t, loff_t, int);
   };
   
   struct inode_operations {
       int (*create) (struct inode *,struct dentry *, umode_t, bool);
       struct dentry * (*lookup) (struct inode *,struct dentry *, unsigned int);
       int (*link) (struct dentry *,struct inode *,struct dentry *);
       int (*unlink) (struct inode *,struct dentry *);
       int (*mkdir) (struct inode *,struct dentry *,umode_t);
       int (*rmdir) (struct inode *,struct dentry *);
       int (*rename) (struct inode *, struct dentry *,
                      struct inode *, struct dentry *, unsigned int);
       int (*setattr) (struct dentry *, struct iattr *);
       int (*getattr) (const struct path *, struct kstat *, u32, unsigned int);
   };

Block Layer
===========

Block Device Representation
----------------------------

.. code-block:: c

   // Block device (gendisk)
   struct gendisk {
       int major;                        // Major number
       int first_minor;                  // First minor number
       int minors;                       // Number of minors
       char disk_name[DISK_NAME_LEN];    // Device name
       struct disk_part_tbl *part_tbl;   // Partition table
       struct block_device_operations *fops;
       struct request_queue *queue;      // Request queue
       void *private_data;               // Driver data
       sector_t capacity;                // Size in sectors
   };
   
   // Request queue
   struct request_queue {
       struct request *last_merge;
       struct elevator_queue *elevator;  // I/O scheduler
       make_request_fn *make_request_fn;
       softirq_done_fn *softirq_done_fn;
       unsigned long queue_flags;
       unsigned int queue_depth;
       spinlock_t queue_lock;
   };
   
   // I/O request
   struct request {
       struct request_queue *q;
       unsigned int cmd_flags;           // Command flags
       enum req_op cmd_op;               // Operation (read/write)
       sector_t __sector;                // Start sector
       unsigned int __data_len;          // Data length
       struct bio *bio;                  // BIO list
       struct bio *biotail;
       void *special;                    // Driver-specific data
   };

Network Stack
=============

Socket Buffer (sk_buff)
-----------------------

.. code-block:: c

   // Network packet representation
   struct sk_buff {
       struct sk_buff *next;             // Next in list
       struct sk_buff *prev;             // Previous in list
       struct sock *sk;                  // Socket
       ktime_t tstamp;                   // Timestamp
       struct net_device *dev;           // Network device
       
       unsigned int len;                 // Actual data length
       unsigned int data_len;            // Data length in frags
       __u16 mac_len;                    // MAC header length
       __u16 hdr_len;                    // cloned header length
       
       // Pointers to protocol headers
       __u8 *data;                       // Data head
       __u8 *tail;
       __u8 *end;
       __u8 *head;                       // Buffer head
       
       __be16 protocol;                  // Protocol (ETH_P_IP, etc.)
       __u16 transport_header;
       __u16 network_header;
       __u16 mac_header;
       
       __u32 priority;                   // Packet priority
       __u8 pkt_type;                    // Packet class
       __u8 ip_summed;                   // Checksum status
   };

Network Device
--------------

.. code-block:: c

   struct net_device {
       char name[IFNAMSIZ];              // Interface name
       unsigned long state;              // Device state
       struct list_head dev_list;        // Global device list
       
       unsigned int flags;               // Interface flags
       unsigned int mtu;                 // Maximum transmission unit
       unsigned short type;              // Hardware type
       unsigned short hard_header_len;   // Hardware header length
       
       unsigned char *dev_addr;          // Hardware address
       unsigned char addr_len;           // Hardware address length
       
       const struct net_device_ops *netdev_ops;
       const struct ethtool_ops *ethtool_ops;
       
       struct netdev_queue *_tx;         // TX queues
       unsigned int num_tx_queues;
       unsigned int real_num_tx_queues;
       
       struct Qdisc *qdisc;              // Packet scheduler
       
       unsigned long tx_queue_len;       // TX queue length
       
       void *priv;                       // Private data
   };

Interrupt Handling
==================

Interrupt Flow
--------------

.. code-block:: text

   Hardware Interrupt
         |
         | CPU interrupt
         v
   IRQ Handler (arch-specific)
         |
         | Call generic handler
         v
   Generic IRQ Handler (__handle_irq_event_percpu)
         |
         | Call registered handler
         v
   Device Driver IRQ Handler
         |
         | Return IRQ_HANDLED/IRQ_NONE
         v
   Schedule softirq if needed
         |
         v
   Softirq execution (later)

IRQ Handling
------------

.. code-block:: c

   // IRQ handler
   static irqreturn_t my_irq_handler(int irq, void *dev_id) {
       struct my_device *dev = dev_id;
       u32 status;
       
       // Read interrupt status
       status = readl(dev->base + STATUS_REG);
       
       if (!(status & MY_IRQ_MASK))
           return IRQ_NONE;  // Not our interrupt
       
       // Clear interrupt
       writel(status, dev->base + STATUS_REG);
       
       // Schedule bottom half
       tasklet_schedule(&dev->tasklet);
       
       return IRQ_HANDLED;
   }
   
   // Request IRQ
   ret = request_irq(irq, my_irq_handler, IRQF_SHARED, "my_device", dev);

Locking and Synchronization
============================

Lock Types
----------

.. code-block:: c

   // Spinlock - busy-waiting lock
   spinlock_t my_lock;
   spin_lock_init(&my_lock);
   
   spin_lock(&my_lock);
   // Critical section (interrupts enabled)
   spin_unlock(&my_lock);
   
   // IRQ-safe spinlock
   unsigned long flags;
   spin_lock_irqsave(&my_lock, flags);
   // Critical section (interrupts disabled)
   spin_unlock_irqrestore(&my_lock, flags);
   
   // Mutex - sleeping lock
   struct mutex my_mutex;
   mutex_init(&my_mutex);
   
   mutex_lock(&my_mutex);
   // Critical section (can sleep)
   mutex_unlock(&my_mutex);
   
   // Semaphore
   struct semaphore my_sem;
   sema_init(&my_sem, 1);  // Binary semaphore
   
   down(&my_sem);
   // Critical section
   up(&my_sem);
   
   // RCU (Read-Copy-Update)
   rcu_read_lock();
   ptr = rcu_dereference(global_ptr);
   // Use ptr
   rcu_read_unlock();
   
   // Update
   new_ptr = kmalloc(...);
   // Initialize new_ptr
   rcu_assign_pointer(global_ptr, new_ptr);
   synchronize_rcu();  // Wait for readers
   kfree(old_ptr);

Kernel Configuration
====================

Build System
------------

.. code-block:: bash

   # Configure kernel
   make menuconfig      # Text-based menu
   make xconfig         # Qt-based GUI
   make gconfig         # GTK-based GUI
   make oldconfig       # Update old config
   make defconfig       # Default config
   make allmodconfig    # All modules
   
   # Build
   make -j$(nproc)      # Parallel build
   make modules         # Build modules only
   make dtbs            # Build device trees
   
   # Install
   sudo make modules_install
   sudo make install
   
   # Clean
   make clean           # Remove build artifacts
   make mrproper        # Remove all generated files
   make distclean       # Remove editor backup files too

Kconfig
-------

.. code-block:: kconfig

   # drivers/mydriver/Kconfig
   config MY_DRIVER
       tristate "My Driver Support"
       depends on PCI
       select CRC32
       help
         This driver supports the My Device hardware.
         
         To compile this driver as a module, choose M here.
   
   config MY_DRIVER_DEBUG
       bool "My Driver Debugging"
       depends on MY_DRIVER
       help
         Enable debugging features for My Driver.

Makefile
--------

.. code-block:: makefile

   # drivers/mydriver/Makefile
   obj-$(CONFIG_MY_DRIVER) += mydriver.o
   
   mydriver-y := main.o device.o interrupt.o
   mydriver-$(CONFIG_MY_DRIVER_DEBUG) += debug.o
   
   # Subdirectory
   obj-$(CONFIG_MY_SUBSYSTEM) += subsystem/
   
   # Module parameters
   ccflags-y += -DDEBUG
   ccflags-$(CONFIG_MY_DRIVER_DEBUG) += -DVERBOSE_DEBUG

Best Practices
==============

1. **Understand kernel APIs** before using them
2. **Follow coding style** (checkpatch.pl)
3. **Handle errors properly** (check return values)
4. **Use appropriate locks** (spin vs mutex)
5. **Minimize interrupt context time**
6. **Document your code** (kernel-doc format)
7. **Test thoroughly** (different configs, architectures)
8. **Review existing code** for patterns
9. **Keep patches small** and focused
10. **Submit to maintainers** properly

Common Pitfalls
===============

1. **Sleeping in atomic context** (spinlock, interrupt)
2. **Deadlocks** (lock ordering, recursive locking)
3. **Memory leaks** (missing kfree, reference counting)
4. **Race conditions** (missing locks, wrong lock type)
5. **Buffer overflows** (unchecked sizes)
6. **Use-after-free** (dangling pointers)
7. **Uninitialized variables**

Quick Reference
===============

.. code-block:: c

   // Memory allocation
   kmalloc(size, GFP_KERNEL);    // Kernel allocation
   kzalloc(size, GFP_KERNEL);    // Zero-initialized
   kfree(ptr);                   // Free memory
   
   // Lists
   LIST_HEAD(my_list);
   list_add(&entry->list, &my_list);
   list_for_each_entry(pos, &my_list, list) { }
   
   // Wait queues
   DECLARE_WAIT_QUEUE_HEAD(my_queue);
   wait_event(my_queue, condition);
   wake_up(&my_queue);
   
   // Timers
   timer_setup(&my_timer, callback, 0);
   mod_timer(&my_timer, jiffies + HZ);
   del_timer(&my_timer);
   
   // Work queues
   INIT_WORK(&my_work, work_func);
   schedule_work(&my_work);

See Also
========

- Linux_Memory_Management_Internals.rst
- Linux_CPU_Scheduling_Internals.rst
- Linux_Process_Management.rst
- Linux_Kernel_Modules_Advanced.rst

References
==========

- Linux Kernel Documentation: https://www.kernel.org/doc/html/latest/
- Understanding the Linux Kernel (O'Reilly)
- Linux Kernel Development (Robert Love)
- kernel/ and include/ in kernel source
