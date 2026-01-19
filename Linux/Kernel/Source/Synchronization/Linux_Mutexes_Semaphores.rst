======================================
Linux Mutexes and Semaphores Guide
======================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Mutex Operations
----------------

.. code-block:: c

   #include <linux/mutex.h>
   
   /* Declaration and initialization */
   DEFINE_MUTEX(my_mutex);                    // Static
   struct mutex my_mutex;
   mutex_init(&my_mutex);                      // Dynamic
   
   /* Lock operations */
   mutex_lock(&my_mutex);                      // Blocking
   mutex_lock_interruptible(&my_mutex);        // Can be interrupted
   mutex_trylock(&my_mutex);                   // Non-blocking (returns 1 on success)
   mutex_unlock(&my_mutex);                    // Release
   
   /* Check if locked */
   mutex_is_locked(&my_mutex);

Semaphore Operations
--------------------

.. code-block:: c

   #include <linux/semaphore.h>
   
   /* Declaration and initialization */
   DEFINE_SEMAPHORE(my_sem);                   // Binary (count=1)
   struct semaphore my_sem;
   sema_init(&my_sem, count);                  // Counting semaphore
   
   /* Operations */
   down(&my_sem);                              // P operation (blocking)
   down_interruptible(&my_sem);                // Can be interrupted
   down_trylock(&my_sem);                      // Non-blocking (returns 0 on success)
   down_timeout(&my_sem, jiffies);             // With timeout
   up(&my_sem);                                // V operation (release)

Quick Decision Guide
--------------------

**Use Mutex when:**
- Only one task can hold the lock
- Lock holder must unlock
- Recursive locking not needed
- Lock held for short duration
- Process context only

**Use Semaphore when:**
- Counting resource access needed
- Different task can unlock
- Signaling between tasks
- Resource counting required

Mutexes in Detail
=================

Introduction
------------

Mutexes (mutual exclusion locks) are sleeping locks that provide mutual exclusion in process context. They are the preferred locking mechanism for most kernel code.

**Key Characteristics:**

- Only one task can hold the mutex at a time
- Lock owner must unlock (strict ownership)
- Cannot be acquired in interrupt context
- Task sleeps if lock unavailable
- Supports priority inheritance (PI)
- Debug support available (CONFIG_DEBUG_MUTEXES)

Mutex Structure
---------------

.. code-block:: c

   struct mutex {
       atomic_long_t       owner;
       spinlock_t          wait_lock;
       struct list_head    wait_list;
   #ifdef CONFIG_MUTEX_SPIN_ON_OWNER
       struct optimistic_spin_queue osq;
   #endif
   #ifdef CONFIG_DEBUG_MUTEXES
       void                *magic;
       struct lockdep_map  dep_map;
   #endif
   };

Mutex Initialization
--------------------

Static Initialization
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Simple mutex */
   static DEFINE_MUTEX(device_mutex);
   
   /* With lockdep class */
   static struct mutex port_mutex;
   static struct lock_class_key port_mutex_key;
   
   static int __init init_module(void) {
       mutex_init(&port_mutex);
       lockdep_set_class(&port_mutex, &port_mutex_key);
       return 0;
   }

Dynamic Initialization
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   struct my_device {
       struct mutex lock;
       /* ... other fields ... */
   };
   
   static int device_probe(struct platform_device *pdev) {
       struct my_device *dev;
       
       dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
           
       mutex_init(&dev->lock);
       /* ... */
       return 0;
   }

Mutex Lock Operations
---------------------

Basic Locking
~~~~~~~~~~~~~

.. code-block:: c

   void device_operation(struct my_device *dev) {
       mutex_lock(&dev->lock);
       
       /* Critical section - protected code */
       dev->state = NEW_STATE;
       device_hardware_update(dev);
       
       mutex_unlock(&dev->lock);
   }

Interruptible Lock
~~~~~~~~~~~~~~~~~~

.. code-block:: c

   int device_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
       struct my_device *dev = filp->private_data;
       int ret;
       
       ret = mutex_lock_interruptible(&dev->lock);
       if (ret)
           return -ERESTARTSYS;  // Signal interrupted
       
       /* Critical section */
       ret = perform_ioctl(dev, cmd, arg);
       
       mutex_unlock(&dev->lock);
       return ret;
   }

Trylock (Non-blocking)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   int device_try_operation(struct my_device *dev) {
       if (!mutex_trylock(&dev->lock))
           return -EBUSY;  // Lock not available
       
       /* Got the lock - critical section */
       perform_operation(dev);
       
       mutex_unlock(&dev->lock);
       return 0;
   }

Lock with Timeout
~~~~~~~~~~~~~~~~~

.. code-block:: c

   #include <linux/jiffies.h>
   
   int device_operation_timeout(struct my_device *dev) {
       unsigned long timeout = jiffies + msecs_to_jiffies(1000);
       
       while (!mutex_trylock(&dev->lock)) {
           if (time_after(jiffies, timeout))
               return -ETIMEDOUT;
           schedule_timeout_interruptible(1);
       }
       
       /* Got lock */
       perform_operation(dev);
       mutex_unlock(&dev->lock);
       return 0;
   }

Mutex Usage Patterns
--------------------

Device State Protection
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   struct sensor_device {
       struct mutex lock;
       int state;
       int value;
       bool enabled;
   };
   
   static int sensor_read(struct sensor_device *sensor, int *value) {
       int ret = 0;
       
       mutex_lock(&sensor->lock);
       
       if (!sensor->enabled) {
           ret = -ENODEV;
           goto unlock;
       }
       
       *value = sensor->value;
       sensor->state = STATE_IDLE;
       
   unlock:
       mutex_unlock(&sensor->lock);
       return ret;
   }

List Protection
~~~~~~~~~~~~~~~

.. code-block:: c

   struct device_manager {
       struct mutex lock;
       struct list_head device_list;
   };
   
   static int add_device(struct device_manager *mgr, struct device *dev) {
       mutex_lock(&mgr->lock);
       list_add_tail(&dev->list, &mgr->device_list);
       mutex_unlock(&mgr->lock);
       return 0;
   }
   
   static struct device *find_device(struct device_manager *mgr, int id) {
       struct device *dev, *found = NULL;
       
       mutex_lock(&mgr->lock);
       list_for_each_entry(dev, &mgr->device_list, list) {
           if (dev->id == id) {
               found = dev;
               break;
           }
       }
       mutex_unlock(&mgr->lock);
       return found;
   }

Multiple Mutex Ordering
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Always acquire mutexes in the same order to avoid deadlock */
   struct resource_pair {
       struct mutex *lock_a;
       struct mutex *lock_b;
   };
   
   void safe_update_both(struct resource_pair *pair) {
       /* Always lock in address order */
       if (pair->lock_a < pair->lock_b) {
           mutex_lock(pair->lock_a);
           mutex_lock(pair->lock_b);
       } else {
           mutex_lock(pair->lock_b);
           mutex_lock(pair->lock_a);
       }
       
       /* Critical section with both locks held */
       update_resources();
       
       /* Unlock in reverse order */
       if (pair->lock_a < pair->lock_b) {
           mutex_unlock(pair->lock_b);
           mutex_unlock(pair->lock_a);
       } else {
           mutex_unlock(pair->lock_a);
           mutex_unlock(pair->lock_b);
       }
   }

Semaphores in Detail
====================

Introduction
------------

Semaphores are counting synchronization primitives that can be used for:

- Mutual exclusion (binary semaphore, count=1)
- Resource counting (counting semaphore, count>1)
- Signaling between tasks

**Key Characteristics:**

- Can be acquired/released by different tasks
- Supports counting (multiple concurrent accesses)
- Tasks sleep when unavailable
- No ownership semantics
- Can be used for producer-consumer patterns

Semaphore Structure
-------------------

.. code-block:: c

   struct semaphore {
       raw_spinlock_t      lock;
       unsigned int        count;
       struct list_head    wait_list;
   };

Semaphore Initialization
------------------------

.. code-block:: c

   /* Binary semaphore (mutex-like) */
   static DEFINE_SEMAPHORE(my_sem);  // count = 1
   
   /* Counting semaphore */
   struct semaphore resource_sem;
   sema_init(&resource_sem, 5);  // Allow 5 concurrent accesses
   
   /* Zero-initialized (for signaling) */
   struct semaphore completion_sem;
   sema_init(&completion_sem, 0);

Binary Semaphore Usage
----------------------

.. code-block:: c

   struct shared_resource {
       struct semaphore sem;
       void *data;
   };
   
   static int resource_init(struct shared_resource *res) {
       sema_init(&res->sem, 1);  // Binary semaphore
       res->data = allocate_data();
       return res->data ? 0 : -ENOMEM;
   }
   
   static int access_resource(struct shared_resource *res) {
       int ret;
       
       /* Acquire semaphore */
       ret = down_interruptible(&res->sem);
       if (ret)
           return -ERESTARTSYS;
       
       /* Critical section */
       process_data(res->data);
       
       /* Release semaphore */
       up(&res->sem);
       return 0;
   }

Counting Semaphore Usage
------------------------

.. code-block:: c

   #define MAX_CONNECTIONS 10
   
   struct connection_pool {
       struct semaphore available;
       struct connection connections[MAX_CONNECTIONS];
   };
   
   static int pool_init(struct connection_pool *pool) {
       sema_init(&pool->available, MAX_CONNECTIONS);
       return 0;
   }
   
   static struct connection *acquire_connection(struct connection_pool *pool) {
       int ret, i;
       
       /* Wait for available connection */
       ret = down_interruptible(&pool->available);
       if (ret)
           return ERR_PTR(-ERESTARTSYS);
       
       /* Find and return free connection */
       for (i = 0; i < MAX_CONNECTIONS; i++) {
           if (!pool->connections[i].in_use) {
               pool->connections[i].in_use = true;
               return &pool->connections[i];
           }
       }
       
       up(&pool->available);  // Should never happen
       return ERR_PTR(-ENOENT);
   }
   
   static void release_connection(struct connection_pool *pool,
                                   struct connection *conn) {
       conn->in_use = false;
       up(&pool->available);  // Increment available count
   }

Producer-Consumer Pattern
--------------------------

.. code-block:: c

   #define BUFFER_SIZE 32
   
   struct producer_consumer {
       struct semaphore empty;  // Count of empty slots
       struct semaphore full;   // Count of filled slots
       struct mutex lock;       // Protect buffer access
       char buffer[BUFFER_SIZE];
       int read_pos;
       int write_pos;
   };
   
   static int pc_init(struct producer_consumer *pc) {
       sema_init(&pc->empty, BUFFER_SIZE);  // All slots empty
       sema_init(&pc->full, 0);              // No slots filled
       mutex_init(&pc->lock);
       pc->read_pos = 0;
       pc->write_pos = 0;
       return 0;
   }
   
   static int produce_item(struct producer_consumer *pc, char item) {
       int ret;
       
       /* Wait for empty slot */
       ret = down_interruptible(&pc->empty);
       if (ret)
           return -ERESTARTSYS;
       
       mutex_lock(&pc->lock);
       pc->buffer[pc->write_pos] = item;
       pc->write_pos = (pc->write_pos + 1) % BUFFER_SIZE;
       mutex_unlock(&pc->lock);
       
       /* Signal item available */
       up(&pc->full);
       return 0;
   }
   
   static int consume_item(struct producer_consumer *pc, char *item) {
       int ret;
       
       /* Wait for filled slot */
       ret = down_interruptible(&pc->full);
       if (ret)
           return -ERESTARTSYS;
       
       mutex_lock(&pc->lock);
       *item = pc->buffer[pc->read_pos];
       pc->read_pos = (pc->read_pos + 1) % BUFFER_SIZE;
       mutex_unlock(&pc->lock);
       
       /* Signal slot empty */
       up(&pc->empty);
       return 0;
   }

Semaphore Operations
--------------------

Down Operations (Acquire)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Blocking - sleep until available */
   down(&sem);
   
   /* Interruptible - can be interrupted by signal */
   ret = down_interruptible(&sem);
   if (ret)
       return -ERESTARTSYS;
   
   /* Non-blocking - returns immediately */
   ret = down_trylock(&sem);  // Returns 0 on success, 1 if unavailable
   if (ret) {
       pr_info("Semaphore not available\n");
       return -EAGAIN;
   }
   
   /* With timeout */
   ret = down_timeout(&sem, msecs_to_jiffies(1000));
   if (ret)
       return -ETIMEDOUT;
   
   /* Killable - can be interrupted only by fatal signal */
   ret = down_killable(&sem);
   if (ret)
       return -EINTR;

Up Operation (Release)
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Release semaphore - increment count */
   up(&sem);

Reader-Writer Semaphores
========================

Introduction
------------

Reader-writer semaphores (rw_semaphore) allow multiple concurrent readers OR one exclusive writer.

.. code-block:: c

   #include <linux/rwsem.h>
   
   /* Declaration */
   DECLARE_RWSEM(my_rwsem);
   
   struct rw_semaphore my_rwsem;
   init_rwsem(&my_rwsem);

Read Lock Operations
--------------------

.. code-block:: c

   void read_data(struct data_structure *data) {
       down_read(&data->rwsem);
       
       /* Multiple readers can execute concurrently */
       value = data->value;
       process_value(value);
       
       up_read(&data->rwsem);
   }
   
   int read_data_interruptible(struct data_structure *data) {
       int ret;
       
       ret = down_read_interruptible(&data->rwsem);
       if (ret)
           return -ERESTARTSYS;
       
       value = data->value;
       up_read(&data->rwsem);
       return value;
   }
   
   /* Try read lock */
   if (down_read_trylock(&data->rwsem)) {
       /* Got read lock */
       value = data->value;
       up_read(&data->rwsem);
   }

Write Lock Operations
---------------------

.. code-block:: c

   void write_data(struct data_structure *data, int new_value) {
       down_write(&data->rwsem);
       
       /* Exclusive access - no other readers or writers */
       data->value = new_value;
       update_related_fields(data);
       
       up_write(&data->rwsem);
   }
   
   int write_data_interruptible(struct data_structure *data, int new_value) {
       int ret;
       
       ret = down_write_interruptible(&data->rwsem);
       if (ret)
           return -ERESTARTSYS;
       
       data->value = new_value;
       up_write(&data->rwsem);
       return 0;
   }
   
   /* Try write lock */
   if (down_write_trylock(&data->rwsem)) {
       data->value = new_value;
       up_write(&data->rwsem);
       return 0;
   }
   return -EBUSY;

Lock Upgrade/Downgrade
-----------------------

.. code-block:: c

   /* Downgrade write lock to read lock */
   void downgrade_example(struct data_structure *data) {
       down_write(&data->rwsem);
       
       /* Perform write operation */
       data->value = compute_new_value();
       
       /* Downgrade to read lock */
       downgrade_write(&data->rwsem);
       
       /* Now have read lock - others can read too */
       validate_value(data->value);
       
       up_read(&data->rwsem);
   }

Complete Driver Example
=======================

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/mutex.h>
   #include <linux/semaphore.h>
   #include <linux/cdev.h>
   #include <linux/uaccess.h>
   
   #define DEVICE_NAME "syncdev"
   #define BUFFER_SIZE 4096
   
   struct sync_device {
       struct cdev cdev;
       struct mutex read_mutex;
       struct semaphore write_sem;
       char buffer[BUFFER_SIZE];
       size_t buffer_len;
       int open_count;
   };
   
   static struct sync_device *sync_dev;
   static dev_t dev_num;
   
   static int syncdev_open(struct inode *inode, struct file *filp) {
       struct sync_device *dev;
       
       dev = container_of(inode->i_cdev, struct sync_device, cdev);
       filp->private_data = dev;
       
       mutex_lock(&dev->read_mutex);
       dev->open_count++;
       mutex_unlock(&dev->read_mutex);
       
       return 0;
   }
   
   static ssize_t syncdev_read(struct file *filp, char __user *buf,
                                size_t count, loff_t *f_pos) {
       struct sync_device *dev = filp->private_data;
       size_t to_copy;
       int ret;
       
       ret = mutex_lock_interruptible(&dev->read_mutex);
       if (ret)
           return -ERESTARTSYS;
       
       if (*f_pos >= dev->buffer_len) {
           mutex_unlock(&dev->read_mutex);
           return 0;  /* EOF */
       }
       
       to_copy = min(count, dev->buffer_len - (size_t)*f_pos);
       
       if (copy_to_user(buf, dev->buffer + *f_pos, to_copy)) {
           mutex_unlock(&dev->read_mutex);
           return -EFAULT;
       }
       
       *f_pos += to_copy;
       mutex_unlock(&dev->read_mutex);
       
       return to_copy;
   }
   
   static ssize_t syncdev_write(struct file *filp, const char __user *buf,
                                 size_t count, loff_t *f_pos) {
       struct sync_device *dev = filp->private_data;
       int ret;
       
       /* Only one writer at a time */
       ret = down_interruptible(&dev->write_sem);
       if (ret)
           return -ERESTARTSYS;
       
       if (count > BUFFER_SIZE)
           count = BUFFER_SIZE;
       
       if (copy_from_user(dev->buffer, buf, count)) {
           up(&dev->write_sem);
           return -EFAULT;
       }
       
       dev->buffer_len = count;
       up(&dev->write_sem);
       
       return count;
   }
   
   static int syncdev_release(struct inode *inode, struct file *filp) {
       struct sync_device *dev = filp->private_data;
       
       mutex_lock(&dev->read_mutex);
       dev->open_count--;
       mutex_unlock(&dev->read_mutex);
       
       return 0;
   }
   
   static const struct file_operations syncdev_fops = {
       .owner = THIS_MODULE,
       .open = syncdev_open,
       .read = syncdev_read,
       .write = syncdev_write,
       .release = syncdev_release,
   };
   
   static int __init syncdev_init(void) {
       int ret;
       
       /* Allocate device number */
       ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
       if (ret < 0)
           return ret;
       
       /* Allocate device structure */
       sync_dev = kzalloc(sizeof(*sync_dev), GFP_KERNEL);
       if (!sync_dev) {
           unregister_chrdev_region(dev_num, 1);
           return -ENOMEM;
       }
       
       /* Initialize synchronization primitives */
       mutex_init(&sync_dev->read_mutex);
       sema_init(&sync_dev->write_sem, 1);
       
       /* Initialize cdev */
       cdev_init(&sync_dev->cdev, &syncdev_fops);
       sync_dev->cdev.owner = THIS_MODULE;
       
       /* Add character device */
       ret = cdev_add(&sync_dev->cdev, dev_num, 1);
       if (ret) {
           kfree(sync_dev);
           unregister_chrdev_region(dev_num, 1);
           return ret;
       }
       
       pr_info("Sync device initialized: major=%d, minor=%d\n",
               MAJOR(dev_num), MINOR(dev_num));
       
       return 0;
   }
   
   static void __exit syncdev_exit(void) {
       cdev_del(&sync_dev->cdev);
       kfree(sync_dev);
       unregister_chrdev_region(dev_num, 1);
       pr_info("Sync device removed\n");
   }
   
   module_init(syncdev_init);
   module_exit(syncdev_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Kernel Developer");
   MODULE_DESCRIPTION("Mutex and Semaphore Example Driver");

Performance Considerations
==========================

Mutex vs Semaphore Performance
-------------------------------

**Mutex Advantages:**

- Faster in uncontended case (optimized fast path)
- Better debugging support
- Priority inheritance support
- Smaller memory footprint

**Semaphore Advantages:**

- Supports counting
- No ownership requirements
- Can signal across tasks

Lock Contention
---------------

.. code-block:: c

   /* Bad: High contention */
   void bad_example(void) {
       mutex_lock(&global_lock);
       small_operation();  // Very short critical section
       mutex_unlock(&global_lock);
   }
   
   /* Better: Reduce contention with finer-grained locking */
   struct partitioned_data {
       struct mutex locks[16];
       struct data_entry entries[1024];
   };
   
   void better_example(struct partitioned_data *pd, int index) {
       int lock_idx = index % 16;
       
       mutex_lock(&pd->locks[lock_idx]);
       process_entry(&pd->entries[index]);
       mutex_unlock(&pd->locks[lock_idx]);
   }

Debugging and Troubleshooting
==============================

Lock Debugging
--------------

Enable in kernel config:

.. code-block:: text

   CONFIG_DEBUG_MUTEXES=y
   CONFIG_DEBUG_LOCK_ALLOC=y
   CONFIG_PROVE_LOCKING=y
   CONFIG_LOCKDEP=y

Deadlock Detection
------------------

.. code-block:: c

   /* Lockdep will detect this potential deadlock */
   void task1(void) {
       mutex_lock(&lock_a);
       mutex_lock(&lock_b);  // Order: A -> B
       /* ... */
       mutex_unlock(&lock_b);
       mutex_unlock(&lock_a);
   }
   
   void task2(void) {
       mutex_lock(&lock_b);
       mutex_lock(&lock_a);  // Order: B -> A (DEADLOCK!)
       /* ... */
       mutex_unlock(&lock_a);
       mutex_unlock(&lock_b);
   }

Common Pitfalls
---------------

**Forgetting to Unlock**

.. code-block:: c

   /* Bad */
   int bad_function(void) {
       mutex_lock(&lock);
       if (error_condition)
           return -EINVAL;  // LOCK LEAK!
       mutex_unlock(&lock);
       return 0;
   }
   
   /* Good */
   int good_function(void) {
       int ret = 0;
       
       mutex_lock(&lock);
       if (error_condition) {
           ret = -EINVAL;
           goto unlock;
       }
       /* ... */
   unlock:
       mutex_unlock(&lock);
       return ret;
   }

**Using Mutex in Interrupt Context**

.. code-block:: c

   /* WRONG - mutexes cannot be used in interrupt context */
   irqreturn_t bad_irq_handler(int irq, void *dev_id) {
       mutex_lock(&device_lock);  // BUG: will sleep!
       /* ... */
       mutex_unlock(&device_lock);
       return IRQ_HANDLED;
   }
   
   /* Correct - use spinlock */
   irqreturn_t good_irq_handler(int irq, void *dev_id) {
       unsigned long flags;
       spin_lock_irqsave(&device_lock, flags);
       /* ... */
       spin_unlock_irqrestore(&device_lock, flags);
       return IRQ_HANDLED;
   }

Best Practices
==============

1. **Prefer mutexes over semaphores** for mutual exclusion
2. **Use interruptible variants** in user-facing code
3. **Always unlock in error paths**
4. **Keep critical sections short**
5. **Document lock ordering** for multiple locks
6. **Use lockdep** for validation
7. **Consider lock-free alternatives** for simple cases
8. **Use try-lock for optional optimizations**

See Also
========

- Linux_Kernel_Synchronization.rst - Overview of all synchronization primitives
- Linux_Spinlocks.rst - Spinlock implementation and usage
- Linux_RCU.rst - Read-Copy-Update synchronization
- Linux_Atomic_Operations.rst - Atomic operations and barriers
- Linux_Kernel_Locking_Patterns.rst - Common locking patterns

References
==========

- Documentation/locking/mutex-design.rst
- Documentation/locking/semaphore.rst
- include/linux/mutex.h
- include/linux/semaphore.h
- kernel/locking/mutex.c
