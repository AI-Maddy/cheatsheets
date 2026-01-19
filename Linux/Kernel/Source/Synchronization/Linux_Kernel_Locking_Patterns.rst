========================================
Linux Kernel Locking Patterns Guide
========================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Common Patterns
---------------

.. code-block:: c

   /* Pattern 1: Simple Resource Protection */
   struct resource {
       spinlock_t lock;
       int value;
   };
   
   void update(struct resource *r, int val) {
       spin_lock(&r->lock);
       r->value = val;
       spin_unlock(&r->lock);
   }
   
   /* Pattern 2: Lock Ordering (avoid deadlock) */
   void transfer(struct account *from, struct account *to, int amount) {
       if (from < to) {
           spin_lock(&from->lock);
           spin_lock(&to->lock);
       } else {
           spin_lock(&to->lock);
           spin_lock(&from->lock);
       }
       from->balance -= amount;
       to->balance += amount;
       spin_unlock(&to->lock);
       spin_unlock(&from->lock);
   }
   
   /* Pattern 3: Reader-Writer */
   rwlock_t config_lock = __RW_LOCK_UNLOCKED(config_lock);
   
   int read_config(void) {
       int val;
       read_lock(&config_lock);
       val = config->value;
       read_unlock(&config_lock);
       return val;
   }
   
   void write_config(int val) {
       write_lock(&config_lock);
       config->value = val;
       write_unlock(&config_lock);
   }
   
   /* Pattern 4: Per-CPU Data */
   DEFINE_PER_CPU(int, cpu_counter);
   
   void increment_counter(void) {
       int *counter = get_cpu_ptr(&cpu_counter);
       (*counter)++;
       put_cpu_ptr(&cpu_counter);
   }
   
   /* Pattern 5: RCU for Read-Mostly */
   rcu_read_lock();
   ptr = rcu_dereference(global_ptr);
   if (ptr)
       use_data(ptr->data);
   rcu_read_unlock();

Anti-Patterns to Avoid
----------------------

.. code-block:: c

   /* WRONG: Lock inversion (deadlock!) */
   void bad_func1(void) {
       mutex_lock(&mutex_a);
       mutex_lock(&mutex_b);
       /* ... */
   }
   
   void bad_func2(void) {
       mutex_lock(&mutex_b);  // Different order!
       mutex_lock(&mutex_a);
       /* ... */
   }
   
   /* WRONG: Sleeping with spinlock */
   spin_lock(&lock);
   msleep(100);  // BUG!
   spin_unlock(&lock);
   
   /* WRONG: Recursive locking */
   mutex_lock(&mutex);
   function_that_also_locks_mutex();  // Deadlock!
   mutex_unlock(&mutex);

Basic Locking Patterns
=======================

Single Lock Protection
----------------------

**Use Case:** Protecting a single resource or small group of related data.

.. code-block:: c

   struct counter {
       spinlock_t lock;
       unsigned long value;
   };
   
   static void counter_init(struct counter *c) {
       spin_lock_init(&c->lock);
       c->value = 0;
   }
   
   static void counter_inc(struct counter *c) {
       spin_lock(&c->lock);
       c->value++;
       spin_unlock(&c->lock);
   }
   
   static unsigned long counter_read(struct counter *c) {
       unsigned long val;
       
       spin_lock(&c->lock);
       val = c->value;
       spin_unlock(&c->lock);
       
       return val;
   }

**When to Use:**
- Simple data structures
- Low contention expected
- Short critical sections

Lock Per Object
---------------

**Use Case:** Each object has its own lock for fine-grained locking.

.. code-block:: c

   struct device {
       struct mutex lock;
       int state;
       void *data;
       struct list_head list;
   };
   
   static void device_update(struct device *dev, int new_state) {
       mutex_lock(&dev->lock);
       dev->state = new_state;
       update_hardware(dev);
       mutex_unlock(&dev->lock);
   }
   
   /* Multiple devices can be accessed concurrently */
   static void update_all_devices(struct list_head *devices) {
       struct device *dev;
       
       list_for_each_entry(dev, devices, list) {
           device_update(dev);  // Each has its own lock
       }
   }

**Benefits:**
- Better scalability
- Reduced contention
- Concurrent access to different objects

**Drawbacks:**
- More memory overhead
- Must handle multiple-lock ordering

Reader-Writer Pattern
=====================

Simple Reader-Writer
--------------------

.. code-block:: c

   struct config_data {
       rwlock_t lock;
       int timeout;
       int retries;
       char hostname[256];
   };
   
   /* Many readers */
   static int get_timeout(struct config_data *cfg) {
       int timeout;
       
       read_lock(&cfg->lock);
       timeout = cfg->timeout;
       read_unlock(&cfg->lock);
       
       return timeout;
   }
   
   /* Single writer */
   static void update_config(struct config_data *cfg,
                              int timeout, int retries) {
       write_lock(&cfg->lock);
       cfg->timeout = timeout;
       cfg->retries = retries;
       write_unlock(&cfg->lock);
   }

**Use When:**
- Many more reads than writes
- Readers don't need to exclude each other
- Write operations are infrequent

RCU-Based Reader-Writer
------------------------

.. code-block:: c

   struct route_entry {
       u32 dest;
       u32 gateway;
       struct rcu_head rcu;
   };
   
   static struct route_entry __rcu *default_route;
   static DEFINE_SPINLOCK(route_lock);
   
   /* Lock-free read */
   static u32 get_gateway(u32 dest) {
       struct route_entry *route;
       u32 gateway = 0;
       
       rcu_read_lock();
       route = rcu_dereference(default_route);
       if (route && route->dest == dest)
           gateway = route->gateway;
       rcu_read_unlock();
       
       return gateway;
   }
   
   /* Write with update */
   static void route_free(struct rcu_head *rcu) {
       struct route_entry *route;
       route = container_of(rcu, struct route_entry, rcu);
       kfree(route);
   }
   
   static int update_route(u32 dest, u32 gateway) {
       struct route_entry *old, *new;
       
       new = kmalloc(sizeof(*new), GFP_KERNEL);
       if (!new)
           return -ENOMEM;
       
       new->dest = dest;
       new->gateway = gateway;
       
       spin_lock(&route_lock);
       old = rcu_dereference_protected(default_route,
                                       lockdep_is_held(&route_lock));
       rcu_assign_pointer(default_route, new);
       spin_unlock(&route_lock);
       
       if (old)
           call_rcu(&old->rcu, route_free);
       
       return 0;
   }

Lock Ordering Patterns
======================

Fixed Order Locking
-------------------

.. code-block:: c

   /* Define global lock ordering */
   static DEFINE_MUTEX(users_mutex);
   static DEFINE_MUTEX(groups_mutex);
   static DEFINE_MUTEX(perms_mutex);
   
   /* Always acquire in this order: users -> groups -> perms */
   static void update_user_group_perms(int uid, int gid, int perms) {
       mutex_lock(&users_mutex);
       mutex_lock(&groups_mutex);
       mutex_lock(&perms_mutex);
       
       /* Critical section */
       do_update(uid, gid, perms);
       
       mutex_unlock(&perms_mutex);
       mutex_unlock(&groups_mutex);
       mutex_unlock(&users_mutex);
   }

Dynamic Order Locking
---------------------

.. code-block:: c

   struct node {
       struct mutex lock;
       int value;
   };
   
   /* Lock two nodes in address order to avoid deadlock */
   static void link_nodes(struct node *n1, struct node *n2) {
       struct node *first, *second;
       
       /* Determine order by address */
       if (n1 < n2) {
           first = n1;
           second = n2;
       } else {
           first = n2;
           second = n1;
       }
       
       mutex_lock(&first->lock);
       mutex_lock(&second->lock);
       
       /* Safe - always same order */
       n1->value += n2->value;
       
       mutex_unlock(&second->lock);
       mutex_unlock(&first->lock);
   }

Hierarchical Locking
--------------------

.. code-block:: c

   struct filesystem {
       struct mutex lock;  // Level 1
       struct list_head inodes;
   };
   
   struct inode {
       struct mutex lock;  // Level 2
       struct filesystem *fs;
       struct list_head dentries;
   };
   
   struct dentry {
       spinlock_t lock;  // Level 3
       struct inode *inode;
   };
   
   /* Always lock from higher to lower level */
   static void safe_operation(struct filesystem *fs,
                               struct inode *inode,
                               struct dentry *dentry) {
       mutex_lock(&fs->lock);       // Level 1
       mutex_lock(&inode->lock);    // Level 2
       spin_lock(&dentry->lock);    // Level 3
       
       /* Critical section */
       
       spin_unlock(&dentry->lock);
       mutex_unlock(&inode->lock);
       mutex_unlock(&fs->lock);
   }

Try-Lock Pattern
================

Optimistic Locking
------------------

.. code-block:: c

   static int try_update_device(struct device *dev, int new_state) {
       if (!mutex_trylock(&dev->lock))
           return -EBUSY;  // Lock not available
       
       dev->state = new_state;
       update_hardware(dev);
       
       mutex_unlock(&dev->lock);
       return 0;
   }
   
   /* Caller can do something else if busy */
   static void conditional_update(struct device *dev, int state) {
       if (try_update_device(dev, state) == -EBUSY) {
           /* Do non-critical work instead */
           schedule_delayed_work(&dev->update_work, HZ);
       }
   }

Avoiding Deadlock with Try-Lock
--------------------------------

.. code-block:: c

   static int safe_transfer(struct account *from,
                             struct account *to,
                             int amount) {
       mutex_lock(&from->lock);
       
       if (!mutex_trylock(&to->lock)) {
           /* Can't get both locks - release and retry */
           mutex_unlock(&from->lock);
           
           /* Small delay to avoid livelock */
           cpu_relax();
           
           return -EAGAIN;
       }
       
       /* Got both locks */
       from->balance -= amount;
       to->balance += amount;
       
       mutex_unlock(&to->lock);
       mutex_unlock(&from->lock);
       
       return 0;
   }

Caching and Lock-Free Reads
============================

Cached Values
-------------

.. code-block:: c

   struct stats {
       spinlock_t lock;
       unsigned long total;
       unsigned long cached_total;  // Approximate value
       unsigned long last_update;
   };
   
   static void stats_inc(struct stats *s) {
       spin_lock(&s->lock);
       s->total++;
       spin_unlock(&s->lock);
   }
   
   /* Cheap approximate read without lock */
   static unsigned long stats_read_approx(struct stats *s) {
       return READ_ONCE(s->cached_total);
   }
   
   /* Expensive accurate read with lock */
   static unsigned long stats_read_exact(struct stats *s) {
       unsigned long total;
       
       spin_lock(&s->lock);
       total = s->total;
       spin_unlock(&s->lock);
       
       return total;
   }
   
   /* Periodic cache update */
   static void stats_update_cache(struct stats *s) {
       unsigned long total;
       
       spin_lock(&s->lock);
       total = s->total;
       WRITE_ONCE(s->cached_total, total);
       s->last_update = jiffies;
       spin_unlock(&s->lock);
   }

Seqlock Pattern
---------------

.. code-block:: c

   #include <linux/seqlock.h>
   
   struct sensor_data {
       seqlock_t lock;
       int temperature;
       int pressure;
       int humidity;
   };
   
   /* Writer (infrequent updates) */
   static void update_sensors(struct sensor_data *data,
                               int temp, int press, int humid) {
       write_seqlock(&data->lock);
       data->temperature = temp;
       data->pressure = press;
       data->humidity = humid;
       write_sequnlock(&data->lock);
   }
   
   /* Reader (frequent reads) - never blocks */
   static void read_sensors(struct sensor_data *data,
                             int *temp, int *press, int *humid) {
       unsigned int seq;
       
       do {
           seq = read_seqbegin(&data->lock);
           *temp = data->temperature;
           *press = data->pressure;
           *humid = data->humidity;
       } while (read_seqretry(&data->lock, seq));
   }

Per-CPU Patterns
================

Simple Per-CPU Counter
----------------------

.. code-block:: c

   DEFINE_PER_CPU(unsigned long, event_counter);
   
   static void count_event(void) {
       unsigned long *counter;
       
       /* Disable preemption while accessing per-CPU data */
       counter = get_cpu_ptr(&event_counter);
       (*counter)++;
       put_cpu_ptr(&event_counter);
   }
   
   static unsigned long read_total_events(void) {
       unsigned long total = 0;
       int cpu;
       
       for_each_possible_cpu(cpu)
           total += per_cpu(event_counter, cpu);
       
       return total;
   }

Per-CPU with Fallback Lock
---------------------------

.. code-block:: c

   struct percpu_counter {
       atomic64_t count;
       struct percpu_counter_impl __percpu *counters;
       spinlock_t lock;
   };
   
   static void percpu_counter_add(struct percpu_counter *fbc, s64 amount) {
       s64 count;
       s64 *pcount;
       
       preempt_disable();
       pcount = this_cpu_ptr(&fbc->counters->count);
       count = *pcount + amount;
       
       if (abs(count) >= PERCPU_COUNTER_BATCH) {
           /* Flush to global counter */
           spin_lock(&fbc->lock);
           atomic64_add(count, &fbc->count);
           *pcount = 0;
           spin_unlock(&fbc->lock);
       } else {
           *pcount = count;
       }
       preempt_enable();
   }

Lock-Free Patterns
==================

Atomic Reference Counting
--------------------------

.. code-block:: c

   struct shared_object {
       atomic_t refcount;
       void *data;
   };
   
   static struct shared_object *object_get(struct shared_object *obj) {
       if (obj && !atomic_inc_not_zero(&obj->refcount))
           return NULL;
       return obj;
   }
   
   static void object_put(struct shared_object *obj) {
       if (obj && atomic_dec_and_test(&obj->refcount))
           kfree(obj);
   }

Lock-Free Stack
---------------

.. code-block:: c

   struct lf_node {
       void *data;
       struct lf_node *next;
   };
   
   struct lf_stack {
       struct lf_node *head;
   };
   
   static void lf_push(struct lf_stack *stack, struct lf_node *node) {
       struct lf_node *old_head;
       
       do {
           old_head = READ_ONCE(stack->head);
           node->next = old_head;
       } while (cmpxchg(&stack->head, old_head, node) != old_head);
   }
   
   static struct lf_node *lf_pop(struct lf_stack *stack) {
       struct lf_node *head, *next;
       
       do {
           head = READ_ONCE(stack->head);
           if (!head)
               return NULL;
           next = READ_ONCE(head->next);
       } while (cmpxchg(&stack->head, head, next) != head);
       
       return head;
   }

Complex Patterns
================

Double-Checked Locking
----------------------

.. code-block:: c

   static struct config *global_config;
   static DEFINE_MUTEX(config_mutex);
   
   static struct config *get_config(void) {
       struct config *cfg;
       
       /* Fast path - no lock */
       cfg = READ_ONCE(global_config);
       if (cfg)
           return cfg;
       
       /* Slow path - initialize */
       mutex_lock(&config_mutex);
       
       cfg = global_config;
       if (!cfg) {
           cfg = allocate_config();
           smp_store_release(&global_config, cfg);
       }
       
       mutex_unlock(&config_mutex);
       
       return cfg;
   }

State Machine with Locking
---------------------------

.. code-block:: c

   enum device_state {
       STATE_IDLE,
       STATE_BUSY,
       STATE_ERROR,
   };
   
   struct device {
       spinlock_t lock;
       enum device_state state;
       wait_queue_head_t wait;
   };
   
   static int device_start_operation(struct device *dev) {
       int ret = 0;
       
       spin_lock(&dev->lock);
       
       switch (dev->state) {
       case STATE_IDLE:
           dev->state = STATE_BUSY;
           break;
       case STATE_BUSY:
           ret = -EBUSY;
           break;
       case STATE_ERROR:
           ret = -EIO;
           break;
       }
       
       spin_unlock(&dev->lock);
       
       return ret;
   }
   
   static void device_end_operation(struct device *dev, int error) {
       spin_lock(&dev->lock);
       
       if (error)
           dev->state = STATE_ERROR;
       else
           dev->state = STATE_IDLE;
       
       wake_up(&dev->wait);
       
       spin_unlock(&dev->lock);
   }

Producer-Consumer with Multiple Locks
--------------------------------------

.. code-block:: c

   struct queue {
       spinlock_t producer_lock;
       spinlock_t consumer_lock;
       struct list_head items;
       atomic_t count;
       wait_queue_head_t wait;
   };
   
   static int queue_produce(struct queue *q, void *item) {
       struct queue_item *qi;
       
       qi = kmalloc(sizeof(*qi), GFP_KERNEL);
       if (!qi)
           return -ENOMEM;
       
       qi->data = item;
       
       spin_lock(&q->producer_lock);
       list_add_tail(&qi->list, &q->items);
       spin_unlock(&q->producer_lock);
       
       atomic_inc(&q->count);
       wake_up(&q->wait);
       
       return 0;
   }
   
   static void *queue_consume(struct queue *q) {
       struct queue_item *qi;
       void *data;
       
       wait_event(q->wait, atomic_read(&q->count) > 0);
       
       spin_lock(&q->consumer_lock);
       qi = list_first_entry_or_null(&q->items, struct queue_item, list);
       if (qi) {
           list_del(&qi->list);
           data = qi->data;
           kfree(qi);
           atomic_dec(&q->count);
       }
       spin_unlock(&q->consumer_lock);
       
       return data;
   }

Performance Patterns
====================

Batching Updates
----------------

.. code-block:: c

   struct batch_updater {
       spinlock_t lock;
       unsigned long pending[64];
       int pending_count;
   };
   
   static void add_update(struct batch_updater *bu, unsigned long value) {
       spin_lock(&bu->lock);
       
       bu->pending[bu->pending_count++] = value;
       
       if (bu->pending_count >= 64) {
           /* Flush batch */
           apply_updates(bu->pending, bu->pending_count);
           bu->pending_count = 0;
       }
       
       spin_unlock(&bu->lock);
   }

Lock Splitting
--------------

.. code-block:: c

   /* Before: Single lock for everything */
   struct device_bad {
       spinlock_t lock;
       struct list_head tx_queue;
       struct list_head rx_queue;
       int tx_count;
       int rx_count;
   };
   
   /* After: Separate locks for TX and RX */
   struct device_good {
       spinlock_t tx_lock;
       spinlock_t rx_lock;
       struct list_head tx_queue;
       struct list_head rx_queue;
       int tx_count;
       int rx_count;
   };
   
   /* TX and RX can proceed concurrently */

Best Practices
==============

1. **Use simplest locking** that solves the problem
2. **Keep critical sections short**
3. **Document lock ordering** requirements
4. **Use lockdep** for validation
5. **Profile lock contention**
6. **Consider lock-free** alternatives for simple cases
7. **Avoid nested locking** when possible
8. **Use per-CPU or RCU** for read-mostly data
9. **Test under load** to find contention
10. **Review for deadlock** potential

Common Mistakes
===============

1. **Lock inversion** - acquiring locks in different orders
2. **Sleeping while holding spinlock**
3. **Forgetting to unlock** in error paths
4. **Too coarse-grained** locking
5. **Recursive locking**
6. **Not considering interrupt** context
7. **Over-optimization** before measuring

See Also
========

- Linux_Kernel_Synchronization.rst
- Linux_Mutexes_Semaphores.rst
- Linux_Spinlocks.rst
- Linux_RCU.rst
- Linux_Atomic_Operations.rst

References
==========

- Documentation/locking/lockdep-design.rst
- Documentation/locking/locking.rst
- kernel/locking/
