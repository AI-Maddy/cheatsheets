==============================
Linux Spinlocks Guide
==============================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Spinlock Operations
--------------------------

.. code-block:: c

   #include <linux/spinlock.h>
   
   /* Declaration and initialization */
   DEFINE_SPINLOCK(my_lock);                   // Static
   spinlock_t my_lock;
   spin_lock_init(&my_lock);                   // Dynamic
   
   /* Process context locking */
   spin_lock(&my_lock);
   /* Critical section */
   spin_unlock(&my_lock);
   
   /* Interrupt-safe locking */
   unsigned long flags;
   spin_lock_irqsave(&my_lock, flags);
   /* Critical section */
   spin_unlock_irqrestore(&my_lock, flags);
   
   /* Bottom half safe */
   spin_lock_bh(&my_lock);
   /* Critical section */
   spin_unlock_bh(&my_lock);

Read-Write Spinlock
-------------------

.. code-block:: c

   /* Declaration */
   DEFINE_RWLOCK(my_rwlock);
   
   /* Read lock (multiple readers allowed) */
   read_lock(&my_rwlock);
   /* Read critical section */
   read_unlock(&my_rwlock);
   
   /* Write lock (exclusive access) */
   write_lock(&my_rwlock);
   /* Write critical section */
   write_unlock(&my_rwlock);

Quick Decision Guide
--------------------

**Use spin_lock when:**
- Only process context access
- No interrupt handlers use the lock
- Critical section < 1ms

**Use spin_lock_irqsave when:**
- Lock shared between process and interrupt context
- Need to disable IRQs and save flags

**Use spin_lock_bh when:**
- Lock shared with bottom halves (softirq/tasklet)
- IRQ handlers don't use this lock

**Use spin_lock_irq when:**
- IRQs already disabled
- Know IRQ state precisely

Spinlock Fundamentals
=====================

Introduction
------------

Spinlocks are the most basic synchronization primitive in the Linux kernel. Unlike mutexes, they do not sleep - instead, they busy-wait (spin) in a loop until the lock becomes available.

**Key Characteristics:**

- Busy-waiting lock (CPU spins while waiting)
- Can be used in any context (process, interrupt, NMI)
- Very low overhead for uncontended case
- Must not sleep while holding spinlock
- Critical sections must be short
- No ownership tracking

When to Use Spinlocks
---------------------

**Use spinlocks when:**

- Protection needed in interrupt context
- Critical section is very short (microseconds)
- Lock held across code that cannot sleep
- Preemption must be disabled

**Do NOT use spinlocks when:**

- Critical section is long (> 1ms)
- Need to call sleeping functions
- Only process context access (use mutex)

Spinlock Structure
------------------

.. code-block:: c

   typedef struct spinlock {
       union {
           struct raw_spinlock rlock;
   #ifdef CONFIG_DEBUG_LOCK_ALLOC
           struct {
               u8 __padding[24];
               struct lockdep_map dep_map;
           };
   #endif
       };
   } spinlock_t;

Basic Spinlock Operations
==========================

Initialization
--------------

Static Initialization
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Simple spinlock */
   static DEFINE_SPINLOCK(device_lock);
   
   /* Multiple spinlocks */
   static DEFINE_SPINLOCK(queue_lock);
   static DEFINE_SPINLOCK(hw_lock);

Dynamic Initialization
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   struct my_device {
       spinlock_t lock;
       void *data;
   };
   
   static int device_probe(struct platform_device *pdev) {
       struct my_device *dev;
       
       dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       spin_lock_init(&dev->lock);
       return 0;
   }

Basic Lock/Unlock
-----------------

Simple Spinlock
~~~~~~~~~~~~~~~

.. code-block:: c

   static void update_counter(void) {
       spin_lock(&counter_lock);
       
       global_counter++;
       
       spin_unlock(&counter_lock);
   }

With Return Value
~~~~~~~~~~~~~~~~~

.. code-block:: c

   static int read_and_clear(void) {
       int value;
       
       spin_lock(&data_lock);
       value = shared_value;
       shared_value = 0;
       spin_unlock(&data_lock);
       
       return value;
   }

Interrupt-Safe Spinlocks
=========================

spin_lock_irqsave/irqrestore
-----------------------------

This is the safest variant when lock is shared between process and interrupt context.

.. code-block:: c

   static void safe_update(struct my_device *dev) {
       unsigned long flags;
       
       spin_lock_irqsave(&dev->lock, flags);
       
       /* Critical section - IRQs disabled on this CPU */
       dev->value++;
       update_hardware(dev);
       
       spin_unlock_irqrestore(&dev->lock, flags);
   }

Why Save Flags?
~~~~~~~~~~~~~~~

.. code-block:: c

   /* Example showing why flags are needed */
   void nested_function(void) {
       unsigned long flags1, flags2;
       
       spin_lock_irqsave(&lock1, flags1);  // IRQs disabled, state saved
       
       /* Call function that also uses spinlock */
       spin_lock_irqsave(&lock2, flags2);  // IRQs already disabled
       /* ... */
       spin_unlock_irqrestore(&lock2, flags2);  // Restore to disabled
       
       /* ... */
       spin_unlock_irqrestore(&lock1, flags1);  // Restore original state
   }

Interrupt Handler Usage
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static irqreturn_t device_irq_handler(int irq, void *dev_id) {
       struct my_device *dev = dev_id;
       unsigned long flags;
       u32 status;
       
       spin_lock_irqsave(&dev->lock, flags);
       
       status = read_status_register(dev);
       if (status & DEV_STATUS_READY) {
           process_device_data(dev);
           dev->irq_count++;
       }
       
       spin_unlock_irqrestore(&dev->lock, flags);
       
       return IRQ_HANDLED;
   }
   
   /* Process context function using same lock */
   static int device_ioctl(struct file *filp, unsigned int cmd,
                           unsigned long arg) {
       struct my_device *dev = filp->private_data;
       unsigned long flags;
       int ret;
       
       spin_lock_irqsave(&dev->lock, flags);
       
       /* Safe - IRQs disabled, handler can't interrupt */
       ret = process_command(dev, cmd);
       
       spin_unlock_irqrestore(&dev->lock, flags);
       
       return ret;
   }

spin_lock_irq/unlock_irq
-------------------------

Use when you **know** IRQs are enabled and can unconditionally disable them.

.. code-block:: c

   /* Only safe if you know IRQs are enabled */
   static void conditional_update(void) {
       spin_lock_irq(&data_lock);
       /* IRQs are now disabled */
       update_data();
       spin_unlock_irq(&data_lock);
       /* IRQs are now enabled */
   }

**Warning:** Do not use if caller might have IRQs already disabled!

Bottom Half Spinlocks
=====================

spin_lock_bh/unlock_bh
----------------------

Disables bottom halves (softirqs and tasklets) on local CPU.

.. code-block:: c

   static void update_stats(struct net_device *dev) {
       struct net_stats *stats = &dev->stats;
       
       spin_lock_bh(&stats->lock);
       
       /* Protected from softirqs (including network RX) */
       stats->rx_packets++;
       stats->rx_bytes += len;
       
       spin_unlock_bh(&stats->lock);
   }

Network Driver Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   struct net_driver {
       spinlock_t tx_lock;
       spinlock_t rx_lock;
       struct sk_buff_head tx_queue;
       struct sk_buff_head rx_queue;
   };
   
   /* Called from process context */
   static netdev_tx_t transmit_packet(struct sk_buff *skb,
                                       struct net_device *dev) {
       struct net_driver *priv = netdev_priv(dev);
       
       spin_lock_bh(&priv->tx_lock);
       
       /* Safe from softirq context */
       skb_queue_tail(&priv->tx_queue, skb);
       start_transmission(priv);
       
       spin_unlock_bh(&priv->tx_lock);
       
       return NETDEV_TX_OK;
   }
   
   /* Called from softirq (NAPI) */
   static int poll_rx(struct napi_struct *napi, int budget) {
       struct net_driver *priv = container_of(napi, struct net_driver, napi);
       struct sk_buff *skb;
       
       /* Already in softirq context, use plain spin_lock */
       spin_lock(&priv->rx_lock);
       
       skb = receive_packet(priv);
       if (skb)
           netif_receive_skb(skb);
       
       spin_unlock(&priv->rx_lock);
       
       return 1;
   }

Read-Write Spinlocks
====================

Introduction
------------

Read-write spinlocks allow multiple readers OR one exclusive writer, but not both simultaneously.

.. code-block:: c

   typedef struct {
       arch_rwlock_t raw_lock;
   #ifdef CONFIG_DEBUG_LOCK_ALLOC
       struct lockdep_map dep_map;
   #endif
   } rwlock_t;

Initialization
--------------

.. code-block:: c

   /* Static */
   static DEFINE_RWLOCK(my_rwlock);
   
   /* Dynamic */
   rwlock_t my_rwlock;
   rwlock_init(&my_rwlock);

Reader Lock Operations
----------------------

.. code-block:: c

   struct shared_data {
       rwlock_t lock;
       int value;
       char name[32];
   };
   
   /* Multiple readers can execute concurrently */
   static int read_value(struct shared_data *data) {
       int val;
       
       read_lock(&data->lock);
       val = data->value;
       read_unlock(&data->lock);
       
       return val;
   }
   
   /* With IRQ safety */
   static int read_value_safe(struct shared_data *data) {
       unsigned long flags;
       int val;
       
       read_lock_irqsave(&data->lock, flags);
       val = data->value;
       read_unlock_irqrestore(&data->lock, flags);
       
       return val;
   }

Writer Lock Operations
----------------------

.. code-block:: c

   /* Exclusive write access */
   static void write_value(struct shared_data *data, int new_val) {
       write_lock(&data->lock);
       
       /* No readers or other writers can execute */
       data->value = new_val;
       snprintf(data->name, sizeof(data->name), "Value_%d", new_val);
       
       write_unlock(&data->lock);
   }
   
   /* With IRQ safety */
   static void write_value_safe(struct shared_data *data, int new_val) {
       unsigned long flags;
       
       write_lock_irqsave(&data->lock, flags);
       data->value = new_val;
       write_unlock_irqrestore(&data->lock, flags);
   }

Complete Example: Packet Queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   #define MAX_PACKETS 256
   
   struct packet_queue {
       rwlock_t lock;
       struct packet *packets[MAX_PACKETS];
       int head;
       int tail;
       int count;
   };
   
   /* Many readers */
   static struct packet *find_packet(struct packet_queue *q, int id) {
       struct packet *pkt = NULL;
       int i;
       
       read_lock_bh(&q->lock);
       
       for (i = 0; i < q->count; i++) {
           int idx = (q->head + i) % MAX_PACKETS;
           if (q->packets[idx]->id == id) {
               pkt = q->packets[idx];
               break;
           }
       }
       
       read_unlock_bh(&q->lock);
       return pkt;
   }
   
   /* Single writer */
   static int enqueue_packet(struct packet_queue *q, struct packet *pkt) {
       int ret = 0;
       
       write_lock_bh(&q->lock);
       
       if (q->count >= MAX_PACKETS) {
           ret = -ENOSPC;
           goto unlock;
       }
       
       q->packets[q->tail] = pkt;
       q->tail = (q->tail + 1) % MAX_PACKETS;
       q->count++;
       
   unlock:
       write_unlock_bh(&q->lock);
       return ret;
   }

Spinlock Variants Summary
==========================

.. code-block:: c

   /* Basic variants */
   spin_lock(&lock);              // Disable preemption
   spin_lock_bh(&lock);          // Disable bottom halves
   spin_lock_irq(&lock);         // Disable IRQs
   spin_lock_irqsave(&lock, f);  // Disable IRQs, save flags
   
   /* Try-lock variants */
   spin_trylock(&lock);           // Returns 1 if acquired
   spin_trylock_bh(&lock);
   spin_trylock_irq(&lock);
   spin_trylock_irqsave(&lock, f);
   
   /* Unlock variants */
   spin_unlock(&lock);
   spin_unlock_bh(&lock);
   spin_unlock_irq(&lock);
   spin_unlock_irqrestore(&lock, f);
   
   /* Read-write variants */
   read_lock(&rwlock);
   read_lock_bh(&rwlock);
   read_lock_irqsave(&rwlock, f);
   read_unlock(&rwlock);
   read_unlock_bh(&rwlock);
   read_unlock_irqrestore(&rwlock, f);
   
   write_lock(&rwlock);
   write_lock_bh(&rwlock);
   write_lock_irqsave(&rwlock, f);
   write_unlock(&rwlock);
   write_unlock_bh(&rwlock);
   write_unlock_irqrestore(&rwlock, f);

Try-Lock Operations
===================

.. code-block:: c

   /* Non-blocking lock attempt */
   static int try_update(struct device *dev) {
       if (!spin_trylock(&dev->lock))
           return -EBUSY;  // Lock not available
       
       /* Got the lock */
       perform_update(dev);
       
       spin_unlock(&dev->lock);
       return 0;
   }
   
   /* With IRQ safety */
   static int try_update_safe(struct device *dev) {
       unsigned long flags;
       
       if (!spin_trylock_irqsave(&dev->lock, flags))
           return -EBUSY;
       
       perform_update(dev);
       spin_unlock_irqrestore(&dev->lock, flags);
       return 0;
   }

Nested Spinlocks
================

Lock Ordering
-------------

Always acquire locks in the same order to avoid deadlock.

.. code-block:: c

   static DEFINE_SPINLOCK(lock_a);
   static DEFINE_SPINLOCK(lock_b);
   
   /* Always lock in same order: A then B */
   static void safe_function(void) {
       unsigned long flags_a, flags_b;
       
       spin_lock_irqsave(&lock_a, flags_a);
       spin_lock_irqsave(&lock_b, flags_b);
       
       /* Critical section with both locks */
       
       spin_unlock_irqrestore(&lock_b, flags_b);
       spin_unlock_irqrestore(&lock_a, flags_a);
   }

Dynamic Ordering
----------------

.. code-block:: c

   struct node {
       spinlock_t lock;
       struct node *next;
       int value;
   };
   
   /* Lock nodes in address order to avoid deadlock */
   static void link_nodes(struct node *n1, struct node *n2) {
       unsigned long flags1, flags2;
       
       /* Always lock lower address first */
       if (n1 < n2) {
           spin_lock_irqsave(&n1->lock, flags1);
           spin_lock_irqsave(&n2->lock, flags2);
       } else {
           spin_lock_irqsave(&n2->lock, flags2);
           spin_lock_irqsave(&n1->lock, flags1);
       }
       
       n1->next = n2;
       
       if (n1 < n2) {
           spin_unlock_irqrestore(&n2->lock, flags2);
           spin_unlock_irqrestore(&n1->lock, flags1);
       } else {
           spin_unlock_irqrestore(&n1->lock, flags1);
           spin_unlock_irqrestore(&n2->lock, flags2);
       }
   }

Per-CPU Variables Alternative
==============================

Sometimes you can avoid spinlocks entirely using per-CPU variables.

.. code-block:: c

   #include <linux/percpu.h>
   
   static DEFINE_PER_CPU(unsigned long, cpu_counter);
   
   /* No lock needed - each CPU has its own counter */
   static void increment_counter(void) {
       unsigned long *counter;
       
       /* Disable preemption while accessing per-CPU data */
       counter = get_cpu_ptr(&cpu_counter);
       (*counter)++;
       put_cpu_ptr(&cpu_counter);
   }
   
   /* Read total across all CPUs */
   static unsigned long read_total(void) {
       unsigned long total = 0;
       int cpu;
       
       for_each_possible_cpu(cpu)
           total += per_cpu(cpu_counter, cpu);
       
       return total;
   }

Complete Driver Example
=======================

.. code-block:: c

   #include <linux/module.h>
   #include <linux/interrupt.h>
   #include <linux/spinlock.h>
   #include <linux/platform_device.h>
   
   #define FIFO_SIZE 128
   
   struct fifo_device {
       spinlock_t lock;
       u32 buffer[FIFO_SIZE];
       int head;
       int tail;
       int count;
       wait_queue_head_t wait_queue;
       int irq;
   };
   
   static irqreturn_t fifo_irq_handler(int irq, void *dev_id) {
       struct fifo_device *fifo = dev_id;
       unsigned long flags;
       u32 data;
       
       /* Read data from hardware */
       data = ioread32(fifo->io_base + DATA_REG);
       
       spin_lock_irqsave(&fifo->lock, flags);
       
       if (fifo->count < FIFO_SIZE) {
           fifo->buffer[fifo->tail] = data;
           fifo->tail = (fifo->tail + 1) % FIFO_SIZE;
           fifo->count++;
           wake_up_interruptible(&fifo->wait_queue);
       }
       
       spin_unlock_irqrestore(&fifo->lock, flags);
       
       return IRQ_HANDLED;
   }
   
   static ssize_t fifo_read(struct file *filp, char __user *buf,
                            size_t count, loff_t *f_pos) {
       struct fifo_device *fifo = filp->private_data;
       unsigned long flags;
       u32 data;
       int ret;
       
       /* Wait for data */
       ret = wait_event_interruptible(fifo->wait_queue, fifo->count > 0);
       if (ret)
           return -ERESTARTSYS;
       
       spin_lock_irqsave(&fifo->lock, flags);
       
       if (fifo->count == 0) {
           spin_unlock_irqrestore(&fifo->lock, flags);
           return 0;
       }
       
       data = fifo->buffer[fifo->head];
       fifo->head = (fifo->head + 1) % FIFO_SIZE;
       fifo->count--;
       
       spin_unlock_irqrestore(&fifo->lock, flags);
       
       if (copy_to_user(buf, &data, sizeof(data)))
           return -EFAULT;
       
       return sizeof(data);
   }
   
   static int fifo_probe(struct platform_device *pdev) {
       struct fifo_device *fifo;
       int ret;
       
       fifo = devm_kzalloc(&pdev->dev, sizeof(*fifo), GFP_KERNEL);
       if (!fifo)
           return -ENOMEM;
       
       spin_lock_init(&fifo->lock);
       init_waitqueue_head(&fifo->wait_queue);
       
       fifo->irq = platform_get_irq(pdev, 0);
       ret = devm_request_irq(&pdev->dev, fifo->irq, fifo_irq_handler,
                              0, dev_name(&pdev->dev), fifo);
       if (ret)
           return ret;
       
       platform_set_drvdata(pdev, fifo);
       return 0;
   }

Performance Considerations
==========================

Lock Contention
---------------

.. code-block:: c

   /* Bad: High contention on single lock */
   static DEFINE_SPINLOCK(global_lock);
   
   void bad_example(int index) {
       spin_lock(&global_lock);
       array[index]++;
       spin_unlock(&global_lock);
   }
   
   /* Better: Per-element locks */
   #define NUM_BUCKETS 256
   
   struct hash_table {
       spinlock_t locks[NUM_BUCKETS];
       struct list_head buckets[NUM_BUCKETS];
   };
   
   void better_example(struct hash_table *ht, int key) {
       int bucket = hash(key) % NUM_BUCKETS;
       
       spin_lock(&ht->locks[bucket]);
       /* Only contention within same bucket */
       list_add(&ht->buckets[bucket], new_entry);
       spin_unlock(&ht->locks[bucket]);
   }

Cache Line Bouncing
-------------------

.. code-block:: c

   /* Bad: Locks on same cache line */
   struct bad_layout {
       spinlock_t lock_a;
       spinlock_t lock_b;  // Likely same cache line as lock_a
       int data_a;
       int data_b;
   };
   
   /* Better: Separate cache lines */
   struct good_layout {
       spinlock_t lock_a;
       int data_a;
       char pad1[L1_CACHE_BYTES - sizeof(spinlock_t) - sizeof(int)];
       
       spinlock_t lock_b;
       int data_b;
       char pad2[L1_CACHE_BYTES - sizeof(spinlock_t) - sizeof(int)];
   } __aligned(L1_CACHE_BYTES);

Common Pitfalls
===============

Sleeping While Holding Spinlock
--------------------------------

.. code-block:: c

   /* WRONG - Cannot sleep while holding spinlock! */
   static void bad_function(void) {
       spin_lock(&device_lock);
       
       msleep(100);  // BUG: Sleeping with spinlock held!
       kmalloc(1024, GFP_KERNEL);  // BUG: Can sleep!
       mutex_lock(&other_lock);  // BUG: Can sleep!
       
       spin_unlock(&device_lock);
   }
   
   /* Correct - Don't sleep with spinlock */
   static void good_function(void) {
       void *data;
       
       /* Allocate before taking lock */
       data = kmalloc(1024, GFP_KERNEL);
       if (!data)
           return;
       
       spin_lock(&device_lock);
       use_data(data);
       spin_unlock(&device_lock);
   }

Forgetting IRQ Safety
---------------------

.. code-block:: c

   /* WRONG - Not IRQ safe */
   irqreturn_t irq_handler(int irq, void *dev_id) {
       spin_lock(&shared_lock);  // DEADLOCK RISK!
       /* ... */
       spin_unlock(&shared_lock);
       return IRQ_HANDLED;
   }
   
   void process_function(void) {
       spin_lock(&shared_lock);
       /* If IRQ happens here, deadlock! */
       spin_unlock(&shared_lock);
   }
   
   /* Correct - Use IRQ-safe variant */
   irqreturn_t irq_handler(int irq, void *dev_id) {
       unsigned long flags;
       spin_lock_irqsave(&shared_lock, flags);
       /* ... */
       spin_unlock_irqrestore(&shared_lock, flags);
       return IRQ_HANDLED;
   }
   
   void process_function(void) {
       unsigned long flags;
       spin_lock_irqsave(&shared_lock, flags);
       /* IRQs disabled - safe */
       spin_unlock_irqrestore(&shared_lock, flags);
   }

Debugging
=========

Lock Statistics
---------------

Enable in kernel config:

.. code-block:: text

   CONFIG_LOCK_STAT=y

View statistics:

.. code-block:: bash

   cat /proc/lock_stat

Lockdep
-------

.. code-block:: text

   CONFIG_PROVE_LOCKING=y
   CONFIG_DEBUG_SPINLOCK=y
   CONFIG_DEBUG_LOCK_ALLOC=y

Best Practices
==============

1. **Keep critical sections short** (microseconds, not milliseconds)
2. **Use appropriate variant** (irqsave for IRQ shared, bh for softirq)
3. **Never sleep** while holding spinlock
4. **Consistent lock ordering** to avoid deadlock
5. **Use per-CPU data** or finer-grained locks to reduce contention
6. **Consider RCU** for read-mostly workloads
7. **Profile and measure** lock contention
8. **Document lock ordering** requirements

See Also
========

- Linux_Kernel_Synchronization.rst - Overview of synchronization
- Linux_Mutexes_Semaphores.rst - Sleeping locks
- Linux_RCU.rst - Lock-free reads
- Linux_Atomic_Operations.rst - Lockless operations
- Linux_Kernel_Locking_Patterns.rst - Design patterns

References
==========

- Documentation/locking/spinlocks.rst
- Documentation/locking/locktypes.rst
- include/linux/spinlock.h
- kernel/locking/spinlock.c
