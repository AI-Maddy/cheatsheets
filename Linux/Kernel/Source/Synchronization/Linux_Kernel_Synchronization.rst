=====================================
Linux Kernel Synchronization
=====================================

:Author: Linux Kernel Cheatsheet Project
:Date: January 2026
:Version: 1.0
:Kernel Versions: 5.x, 6.x
:Sources: Linux Kernel Programming Part 2, Kernel Documentation

.. contents:: Table of Contents
   :depth: 3
   :local:

TL;DR - Quick Reference
=======================

Critical Synchronization Primitives
------------------------------------

.. code-block:: c

    /* Mutexes - sleepable, process context only */
    #include <linux/mutex.h>
    DEFINE_MUTEX(my_mutex);
    mutex_lock(&my_mutex);
    mutex_unlock(&my_mutex);
    
    /* Spinlocks - non-sleepable, interrupt-safe */
    #include <linux/spinlock.h>
    DEFINE_SPINLOCK(my_spinlock);
    spin_lock(&my_spinlock);
    spin_unlock(&my_spinlock);
    
    /* Semaphores - counting, sleepable */
    #include <linux/semaphore.h>
    struct semaphore sem;
    sema_init(&sem, 1);
    down(&sem);
    up(&sem);
    
    /* Atomic operations */
    #include <linux/atomic.h>
    atomic_t counter = ATOMIC_INIT(0);
    atomic_inc(&counter);
    atomic_dec_and_test(&counter);
    
    /* RCU - Read-Copy-Update */
    #include <linux/rcupdate.h>
    rcu_read_lock();
    rcu_dereference(ptr);
    rcu_read_unlock();

Quick Decision Guide
--------------------

+------------------+---------------+---------------+------------------+
| Use Case         | Primitive     | Sleep OK?     | Overhead         |
+==================+===============+===============+==================+
| Long critical    | Mutex         | Yes           | Low              |
| section          |               |               |                  |
+------------------+---------------+---------------+------------------+
| Short critical   | Spinlock      | No            | Very Low         |
| section          |               |               |                  |
+------------------+---------------+---------------+------------------+
| Interrupt        | Spinlock IRQ  | No            | Low              |
| context          |               |               |                  |
+------------------+---------------+---------------+------------------+
| Counter ops      | Atomic        | N/A           | Minimal          |
+------------------+---------------+---------------+------------------+
| Read-mostly data | RCU           | No (readers)  | Very Low         |
+------------------+---------------+---------------+------------------+
| Resource count   | Semaphore     | Yes           | Low              |
+------------------+---------------+---------------+------------------+

Introduction
============

Overview of Kernel Synchronization
-----------------------------------

The Linux kernel is a preemptive, SMP (Symmetric Multi-Processing) operating system 
requiring careful synchronization to protect shared data structures. Key challenges:

1. **Multiple CPUs** accessing shared data simultaneously
2. **Kernel preemption** where tasks can be interrupted
3. **Interrupt handlers** running asynchronously
4. **Bottom halves** (softirqs, tasklets) executing concurrently

Synchronization Goals
---------------------

1. **Mutual Exclusion**: Only one execution context accesses critical section
2. **Atomicity**: Operations complete without interruption
3. **Memory Ordering**: Operations visible in correct order across CPUs
4. **Deadlock Prevention**: Avoid circular wait conditions

Critical Sections
-----------------

A critical section is code that:

- Accesses shared data structures
- Must execute atomically
- Requires protection from concurrent access

.. code-block:: c

    /* Example: Critical section in a device driver */
    struct my_device {
        struct mutex lock;
        int shared_counter;
        struct list_head queue;
    };
    
    void update_device(struct my_device *dev, int value)
    {
        mutex_lock(&dev->lock);  /* Enter critical section */
        
        dev->shared_counter += value;
        list_add_tail(&dev->queue, &item->list);
        
        mutex_unlock(&dev->lock); /* Exit critical section */
    }

Synchronization Primitives Overview
====================================

Mutex (Mutual Exclusion)
-------------------------

**Characteristics:**

- Sleepable (process context only)
- Owner can sleep while holding mutex
- Only owner can unlock
- Cannot be used in interrupt context
- Most common synchronization primitive

**When to Use:**

- Long critical sections (>few milliseconds)
- Code that may sleep (memory allocation, I/O)
- Process context only

**Basic Operations:**

.. code-block:: c

    #include <linux/mutex.h>
    
    struct mutex my_lock;
    
    /* Initialization */
    mutex_init(&my_lock);
    
    /* Lock/Unlock */
    mutex_lock(&my_lock);        /* Sleep until available */
    mutex_unlock(&my_lock);
    
    /* Trylock */
    if (mutex_trylock(&my_lock)) {
        /* Got the lock */
        mutex_unlock(&my_lock);
    }
    
    /* Interruptible lock */
    if (mutex_lock_interruptible(&my_lock)) {
        return -ERESTARTSYS;  /* Signal received */
    }

Spinlocks
---------

**Characteristics:**

- Non-sleepable (busy-waiting)
- Fast, minimal overhead
- Can be used in interrupt context (with IRQ variants)
- Preemption disabled while held
- Very short critical sections only

**When to Use:**

- Very short critical sections (<microseconds typically)
- Interrupt handlers
- Code that cannot sleep
- Protecting simple data structures

**Basic Operations:**

.. code-block:: c

    #include <linux/spinlock.h>
    
    spinlock_t my_spinlock;
    
    /* Initialization */
    spin_lock_init(&my_spinlock);
    
    /* Lock/Unlock */
    spin_lock(&my_spinlock);
    spin_unlock(&my_spinlock);
    
    /* IRQ-safe variants */
    unsigned long flags;
    spin_lock_irqsave(&my_spinlock, flags);
    spin_unlock_irqrestore(&my_spinlock, flags);

Semaphores
----------

**Characteristics:**

- Counting semaphore (not just binary)
- Sleepable
- Can allow N concurrent users
- Less common than mutexes in modern kernel

**When to Use:**

- Need to limit concurrent access to N users
- Legacy code (consider mutex for new code)

**Basic Operations:**

.. code-block:: c

    #include <linux/semaphore.h>
    
    struct semaphore sem;
    
    /* Initialize to allow 3 concurrent users */
    sema_init(&sem, 3);
    
    /* Acquire/Release */
    down(&sem);         /* Decrement, sleep if zero */
    up(&sem);           /* Increment */
    
    /* Interruptible */
    if (down_interruptible(&sem))
        return -ERESTARTSYS;

Atomic Operations
-----------------

**Characteristics:**

- Hardware-level atomicity
- No locks needed
- Very fast
- Works for simple integer operations

**When to Use:**

- Simple counters
- Flags and state variables
- Reference counting

**Basic Operations:**

.. code-block:: c

    #include <linux/atomic.h>
    
    atomic_t counter = ATOMIC_INIT(0);
    
    /* Increment/Decrement */
    atomic_inc(&counter);
    atomic_dec(&counter);
    
    /* Test operations */
    if (atomic_dec_and_test(&counter))
        /* Counter reached zero */
    
    /* Read/Set */
    int val = atomic_read(&counter);
    atomic_set(&counter, 10);
    
    /* Add/Sub */
    atomic_add(5, &counter);
    atomic_sub(3, &counter);

RCU (Read-Copy-Update)
----------------------

**Characteristics:**

- Optimized for read-mostly scenarios
- Readers never block
- Writers create new version of data
- Deferred reclamation of old versions

**When to Use:**

- Data structures with frequent reads, rare writes
- List traversal
- Performance-critical paths

**Basic Operations:**

.. code-block:: c

    #include <linux/rcupdate.h>
    
    struct data {
        int value;
        struct rcu_head rcu;
    };
    
    struct data *ptr;
    
    /* Reader */
    rcu_read_lock();
    struct data *p = rcu_dereference(ptr);
    if (p)
        use_data(p->value);
    rcu_read_unlock();
    
    /* Writer */
    struct data *new = kmalloc(sizeof(*new), GFP_KERNEL);
    new->value = 42;
    
    struct data *old = ptr;
    rcu_assign_pointer(ptr, new);
    synchronize_rcu();  /* Wait for readers */
    kfree(old);

Choosing the Right Primitive
=============================

Decision Tree
-------------

.. code-block:: text

    Can the code sleep?
    ├── NO (interrupt context / atomic)
    │   ├── Very short critical section? → Spinlock
    │   ├── Simple counter operation? → Atomic ops
    │   └── Read-mostly data? → RCU
    │
    └── YES (process context)
        ├── Long critical section? → Mutex
        ├── Need counting (N users)? → Semaphore
        └── Short but sleepable? → Mutex (still best)

Context Rules
-------------

+-------------------+--------+-----------+-------+----------+-----+
| Primitive         | Process| Interrupt | Sleep | Preempt  | SMP |
| Context           | OK?    | OK?       | OK?   | Disabled?| Safe|
+===================+========+===========+=======+==========+=====+
| Mutex             | Yes    | No        | Yes   | No       | Yes |
+-------------------+--------+-----------+-------+----------+-----+
| Spinlock          | Yes    | No*       | No    | Yes      | Yes |
+-------------------+--------+-----------+-------+----------+-----+
| Spinlock_irq      | Yes    | Yes       | No    | Yes      | Yes |
+-------------------+--------+-----------+-------+----------+-----+
| Semaphore         | Yes    | No        | Yes   | No       | Yes |
+-------------------+--------+-----------+-------+----------+-----+
| Atomic            | Yes    | Yes       | No    | No       | Yes |
+-------------------+--------+-----------+-------+----------+-----+
| RCU (read)        | Yes    | Yes       | No    | No       | Yes |
+-------------------+--------+-----------+-------+----------+-----+

\* Regular spinlock can be used in softirq/tasklet but not hardirq

Performance Considerations
--------------------------

+---------------+------------+------------------+---------------------+
| Primitive     | Overhead   | Critical Section | Scalability         |
+===============+============+==================+=====================+
| Mutex         | Medium     | Long (ms)        | Good                |
+---------------+------------+------------------+---------------------+
| Spinlock      | Very Low   | Very Short (μs)  | Excellent (no wait) |
+---------------+------------+------------------+---------------------+
| Semaphore     | Medium     | Long (ms)        | Fair                |
+---------------+------------+------------------+---------------------+
| Atomic        | Minimal    | N/A              | Excellent           |
+---------------+------------+------------------+---------------------+
| RCU           | Minimal    | Read: instant    | Excellent (readers) |
|               |            | Write: medium    |                     |
+---------------+------------+------------------+---------------------+

Practical Examples
==================

Example 1: Character Device with Mutex
---------------------------------------

.. code-block:: c

    #include <linux/module.h>
    #include <linux/fs.h>
    #include <linux/cdev.h>
    #include <linux/mutex.h>
    
    struct my_device {
        struct cdev cdev;
        struct mutex lock;
        char buffer[256];
        size_t size;
    };
    
    static struct my_device *my_dev;
    
    static ssize_t my_read(struct file *filp, char __user *buf,
                           size_t count, loff_t *ppos)
    {
        struct my_device *dev = filp->private_data;
        ssize_t ret;
        
        if (mutex_lock_interruptible(&dev->lock))
            return -ERESTARTSYS;
        
        /* Critical section - protected data access */
        if (*ppos >= dev->size) {
            ret = 0;
            goto out;
        }
        
        if (*ppos + count > dev->size)
            count = dev->size - *ppos;
        
        if (copy_to_user(buf, dev->buffer + *ppos, count)) {
            ret = -EFAULT;
            goto out;
        }
        
        *ppos += count;
        ret = count;
        
    out:
        mutex_unlock(&dev->lock);
        return ret;
    }
    
    static int my_open(struct inode *inode, struct file *filp)
    {
        filp->private_data = my_dev;
        return 0;
    }
    
    static struct file_operations fops = {
        .owner = THIS_MODULE,
        .open = my_open,
        .read = my_read,
    };
    
    static int __init my_init(void)
    {
        my_dev = kzalloc(sizeof(*my_dev), GFP_KERNEL);
        if (!my_dev)
            return -ENOMEM;
        
        mutex_init(&my_dev->lock);
        /* Initialize device... */
        
        return 0;
    }

Example 2: Interrupt Handler with Spinlock
-------------------------------------------

.. code-block:: c

    #include <linux/interrupt.h>
    #include <linux/spinlock.h>
    
    struct my_device {
        spinlock_t lock;
        unsigned int status;
        struct list_head pending_requests;
    };
    
    static struct my_device *dev;
    
    /* Interrupt handler - cannot sleep! */
    static irqreturn_t my_interrupt(int irq, void *dev_id)
    {
        struct my_device *dev = dev_id;
        unsigned long flags;
        
        spin_lock_irqsave(&dev->lock, flags);
        
        /* Read hardware status */
        dev->status = ioread32(dev->base + STATUS_REG);
        
        /* Process pending requests */
        if (!list_empty(&dev->pending_requests)) {
            struct request *req;
            req = list_first_entry(&dev->pending_requests,
                                   struct request, list);
            list_del(&req->list);
            /* Handle request */
        }
        
        spin_unlock_irqrestore(&dev->lock, flags);
        
        return IRQ_HANDLED;
    }
    
    /* Process context function */
    void add_request(struct my_device *dev, struct request *req)
    {
        unsigned long flags;
        
        spin_lock_irqsave(&dev->lock, flags);
        list_add_tail(&req->list, &dev->pending_requests);
        spin_unlock_irqrestore(&dev->lock, flags);
    }

Example 3: Reference Counting with Atomic Operations
-----------------------------------------------------

.. code-block:: c

    #include <linux/kref.h>
    #include <linux/slab.h>
    
    struct my_object {
        struct kref refcount;
        char *data;
    };
    
    static void my_object_release(struct kref *ref)
    {
        struct my_object *obj = container_of(ref, struct my_object,
                                              refcount);
        kfree(obj->data);
        kfree(obj);
    }
    
    struct my_object *my_object_create(void)
    {
        struct my_object *obj;
        
        obj = kzalloc(sizeof(*obj), GFP_KERNEL);
        if (!obj)
            return NULL;
        
        kref_init(&obj->refcount);  /* Refcount = 1 */
        obj->data = kzalloc(1024, GFP_KERNEL);
        
        return obj;
    }
    
    void my_object_get(struct my_object *obj)
    {
        kref_get(&obj->refcount);
    }
    
    void my_object_put(struct my_object *obj)
    {
        kref_put(&obj->refcount, my_object_release);
    }
    
    /* Usage */
    void use_object(void)
    {
        struct my_object *obj = my_object_create();
        
        /* Pass to another subsystem */
        my_object_get(obj);  /* Increment refcount */
        other_subsystem_use(obj);
        
        /* Done with our reference */
        my_object_put(obj);
        
        /* other_subsystem will call my_object_put() when done */
    }

Example 4: RCU-Protected List
------------------------------

.. code-block:: c

    #include <linux/list.h>
    #include <linux/rculist.h>
    #include <linux/rcupdate.h>
    
    struct data_node {
        struct list_head list;
        int key;
        int value;
        struct rcu_head rcu;
    };
    
    static LIST_HEAD(data_list);
    static DEFINE_SPINLOCK(data_lock);  /* For writers only */
    
    /* Reader - lockless, very fast */
    int lookup_value(int key)
    {
        struct data_node *node;
        int ret = -ENOENT;
        
        rcu_read_lock();
        list_for_each_entry_rcu(node, &data_list, list) {
            if (node->key == key) {
                ret = node->value;
                break;
            }
        }
        rcu_read_unlock();
        
        return ret;
    }
    
    /* Writer - uses spinlock */
    void update_value(int key, int new_value)
    {
        struct data_node *node, *new_node;
        
        new_node = kmalloc(sizeof(*new_node), GFP_KERNEL);
        if (!new_node)
            return;
        
        new_node->key = key;
        new_node->value = new_value;
        
        spin_lock(&data_lock);
        
        /* Find existing node */
        list_for_each_entry(node, &data_list, list) {
            if (node->key == key) {
                list_replace_rcu(&node->list, &new_node->list);
                spin_unlock(&data_lock);
                
                /* Wait for readers, then free old node */
                synchronize_rcu();
                kfree(node);
                return;
            }
        }
        
        /* Key not found, add new */
        list_add_rcu(&new_node->list, &data_list);
        spin_unlock(&data_lock);
    }

Common Pitfalls and Debugging
==============================

Deadlock Scenarios
------------------

**Problem: Lock Ordering**

.. code-block:: c

    /* Thread 1 */
    mutex_lock(&lock_A);
    mutex_lock(&lock_B);  /* Deadlock! */
    
    /* Thread 2 */
    mutex_lock(&lock_B);
    mutex_lock(&lock_A);  /* Deadlock! */

**Solution: Consistent Lock Ordering**

.. code-block:: c

    /* Always acquire locks in same order */
    /* Thread 1 */
    mutex_lock(&lock_A);
    mutex_lock(&lock_B);
    
    /* Thread 2 */
    mutex_lock(&lock_A);  /* Same order */
    mutex_lock(&lock_B);

**Problem: Sleeping While Atomic**

.. code-block:: c

    /* WRONG - Cannot sleep while holding spinlock */
    spin_lock(&my_lock);
    ptr = kmalloc(size, GFP_KERNEL);  /* May sleep! */
    spin_unlock(&my_lock);

**Solution: Use GFP_ATOMIC or use mutex**

.. code-block:: c

    /* Option 1: Atomic allocation */
    spin_lock(&my_lock);
    ptr = kmalloc(size, GFP_ATOMIC);  /* Won't sleep */
    spin_unlock(&my_lock);
    
    /* Option 2: Use mutex instead */
    mutex_lock(&my_mutex);
    ptr = kmalloc(size, GFP_KERNEL);  /* OK to sleep */
    mutex_unlock(&my_mutex);

Lock Debugging
--------------

**Enable Kernel Lock Debugging:**

.. code-block:: bash

    # In kernel .config
    CONFIG_DEBUG_MUTEXES=y
    CONFIG_DEBUG_SPINLOCK=y
    CONFIG_DEBUG_LOCK_ALLOC=y
    CONFIG_PROVE_LOCKING=y  # Lockdep
    CONFIG_LOCK_STAT=y

**Lockdep - Runtime Deadlock Detection:**

The kernel's lockdep feature detects potential deadlocks at runtime.

.. code-block:: c

    /* Annotate lock ordering */
    static DEFINE_MUTEX(outer_lock);
    static DEFINE_MUTEX(inner_lock);
    
    /* Tell lockdep about nesting */
    mutex_lock(&outer_lock);
    mutex_lock_nested(&inner_lock, SINGLE_DEPTH_NESTING);
    mutex_unlock(&inner_lock);
    mutex_unlock(&outer_lock);

**Checking for Lock Contention:**

.. code-block:: bash

    # View lock statistics
    cat /proc/lock_stat
    
    # Enable/disable lock stats
    echo 0 > /proc/sys/kernel/lock_stat  # disable
    echo 1 > /proc/sys/kernel/lock_stat  # enable

Memory Barriers
===============

Understanding Memory Ordering
------------------------------

Modern CPUs and compilers can reorder memory operations for performance.
Synchronization primitives include appropriate memory barriers.

**Explicit Barriers:**

.. code-block:: c

    #include <asm/barrier.h>
    
    /* Full memory barrier */
    mb();      /* SMP barrier */
    smp_mb();  /* SMP-only barrier */
    
    /* Read/Write barriers */
    rmb();     /* Read memory barrier */
    wmb();     /* Write memory barrier */
    smp_rmb();
    smp_wmb();
    
    /* Compiler barrier (no CPU barrier) */
    barrier();

**Example with Memory Barriers:**

.. code-block:: c

    /* Producer */
    buffer->data = value;
    smp_wmb();  /* Ensure data written before flag */
    buffer->ready = 1;
    
    /* Consumer */
    while (!buffer->ready)
        cpu_relax();
    smp_rmb();  /* Ensure flag read before data */
    value = buffer->data;

**Note:** Most synchronization primitives include appropriate barriers,
so explicit barriers are rarely needed in normal driver code.

Best Practices
==============

General Guidelines
------------------

1. **Keep Critical Sections Short**
   
   - Minimize code between lock/unlock
   - Don't call other functions while holding locks
   - Consider lock-free algorithms for hot paths

2. **Consistent Lock Ordering**
   
   - Document lock hierarchy
   - Always acquire locks in the same order
   - Use lockdep to verify

3. **Choose the Right Primitive**
   
   - Mutex for normal process context
   - Spinlock for interrupt context or very short sections
   - Atomic ops for simple counters
   - RCU for read-mostly data

4. **Avoid Holding Locks Across User Copies**

.. code-block:: c

    /* BAD - lock held during copy_to_user */
    mutex_lock(&dev->lock);
    copy_to_user(buf, dev->data, len);  /* May sleep/fault! */
    mutex_unlock(&dev->lock);
    
    /* GOOD - copy to temporary buffer */
    mutex_lock(&dev->lock);
    memcpy(tmp, dev->data, len);
    mutex_unlock(&dev->lock);
    copy_to_user(buf, tmp, len);

5. **Document Locking Strategy**

.. code-block:: c

    /**
     * struct my_device - Device state
     * @lock: Protects buffer, size, and status fields
     * @buffer: Data buffer
     * @size: Current buffer size
     * @status: Device status flags
     */
    struct my_device {
        struct mutex lock;
        char *buffer;
        size_t size;
        u32 status;
    };

Performance Optimization
------------------------

**Lock Granularity:**

.. code-block:: c

    /* Coarse-grained - one lock for everything */
    struct device {
        struct mutex lock;
        int counter;
        struct list_head queue;
        char buffer[256];
    };
    
    /* Fine-grained - separate locks for independent data */
    struct device {
        struct mutex counter_lock;
        int counter;
        
        struct mutex queue_lock;
        struct list_head queue;
        
        struct mutex buffer_lock;
        char buffer[256];
    };

**Lock-Free Techniques:**

.. code-block:: c

    /* Per-CPU variables - no locking needed */
    DEFINE_PER_CPU(int, cpu_counter);
    
    void increment_counter(void)
    {
        int *counter = get_cpu_var(cpu_counter);
        (*counter)++;
        put_cpu_var(cpu_counter);
    }

Cross-References
================

Related Cheatsheets
-------------------

- `Linux_Mutexes_Semaphores.rst` - Detailed mutex and semaphore guide
- `Linux_Spinlocks.rst` - Comprehensive spinlock reference
- `Linux_Atomic_Operations.rst` - Atomic operations and barriers
- `Linux_RCU.rst` - Read-Copy-Update mechanisms
- `Linux_Kernel_Locking_Patterns.rst` - Common locking patterns
- `Linux_Wait_Queues.rst` - Wait queues and completion
- `Linux_Char_Device_Drivers.rst` - Character device synchronization
- `Linux Interrupts.rst` - Interrupt handling and synchronization

Kernel Documentation
--------------------

- Documentation/locking/mutex-design.rst
- Documentation/locking/spinlocks.rst
- Documentation/RCU/
- Documentation/atomic_t.txt
- Documentation/memory-barriers.txt

Troubleshooting
===============

Common Issues
-------------

**Issue: "BUG: sleeping function called from invalid context"**

.. code-block:: text

    Cause: Called a sleeping function while holding spinlock or in interrupt
    Solution: Use mutex instead, or use GFP_ATOMIC allocations

**Issue: Soft lockup detected**

.. code-block:: text

    Cause: Held spinlock too long, blocking other CPUs
    Solution: Reduce critical section size, use mutex for long operations

**Issue: Deadlock detected by lockdep**

.. code-block:: text

    Cause: Inconsistent lock ordering
    Solution: Review lock ordering, use mutex_lock_nested() if appropriate

**Issue: High lock contention**

.. code-block:: text

    Cause: Too many threads competing for same lock
    Solution: Use finer-grained locking, per-CPU variables, or RCU

Debugging Commands
------------------

.. code-block:: bash

    # Check for lock debugging in running kernel
    grep LOCK /boot/config-$(uname -r)
    
    # View lock statistics
    cat /proc/lock_stat
    
    # Check for hung tasks
    dmesg | grep "hung task"
    
    # Enable/disable lockdep
    echo 1 > /proc/sys/kernel/lock_stat

References
==========

Books and Documentation
-----------------------

- Linux Kernel Programming Part 2 (Kaiwan N Billimoria)
- Linux Device Drivers, 3rd Edition (LDD3)
- Linux Kernel Development (Robert Love)
- Kernel Documentation: Documentation/locking/

Online Resources
----------------

- https://www.kernel.org/doc/Documentation/locking/
- https://lwn.net/Kernel/Index/ (LWN kernel articles)
- https://www.kernel.org/doc/html/latest/core-api/

Author & Updates
================

:Author: Linux Kernel Cheatsheet Project
:Created: January 2026
:Last Updated: January 2026
:Kernel Version: 6.x
:License: GPL v2

For corrections or updates, see the main repository.
