==================================
Linux RCU (Read-Copy-Update) Guide
==================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic RCU Operations
--------------------

.. code-block:: c

   #include <linux/rcupdate.h>
   
   /* Reader side */
   rcu_read_lock();
   ptr = rcu_dereference(shared_ptr);
   if (ptr) {
       /* Use ptr - safe from deletion */
       value = ptr->data;
   }
   rcu_read_unlock();
   
   /* Writer side - update */
   new_ptr = kmalloc(sizeof(*new_ptr), GFP_KERNEL);
   new_ptr->data = new_value;
   old_ptr = rcu_dereference_protected(shared_ptr, lockdep_is_held(&update_lock));
   rcu_assign_pointer(shared_ptr, new_ptr);
   synchronize_rcu();
   kfree(old_ptr);
   
   /* Writer side - deletion */
   spin_lock(&list_lock);
   list_del_rcu(&node->list);
   spin_unlock(&list_lock);
   synchronize_rcu();
   kfree(node);

RCU List Operations
-------------------

.. code-block:: c

   #include <linux/rculist.h>
   
   /* Add to list */
   list_add_rcu(&new_node->list, &head);
   
   /* Delete from list */
   list_del_rcu(&node->list);
   
   /* Iterate - reader */
   rcu_read_lock();
   list_for_each_entry_rcu(node, &head, list) {
       process_node(node);
   }
   rcu_read_unlock();
   
   /* Replace in list */
   list_replace_rcu(&old->list, &new->list);

Call RCU (Deferred Free)
------------------------

.. code-block:: c

   struct my_node {
       int data;
       struct rcu_head rcu;
   };
   
   static void my_node_free(struct rcu_head *rcu) {
       struct my_node *node = container_of(rcu, struct my_node, rcu);
       kfree(node);
   }
   
   /* Schedule deferred free */
   call_rcu(&node->rcu, my_node_free);

Quick Decision Guide
--------------------

**Use RCU when:**
- Read-mostly workload (10:1 or better ratio)
- Readers can tolerate stale data briefly
- Updates are infrequent
- Lock-free reads needed

**Do NOT use RCU when:**
- Write-heavy workload
- Readers need immediate consistency
- Simple data structures (use atomic ops)

RCU Fundamentals
================

Introduction
------------

RCU (Read-Copy-Update) is a synchronization mechanism that allows lock-free reads while supporting concurrent updates.

**Core Principles:**

1. **Readers** can access data without locks
2. **Writers** create new versions instead of updating in-place
3. **Deferred reclamation** waits for all readers to finish before freeing old data

**Key Characteristics:**

- Extremely fast reads (no locks, no atomic ops)
- More expensive writes
- Grace period mechanism ensures safety
- Perfect for read-mostly data structures

RCU Components
--------------

.. code-block:: text

   Reader Side:
   ┌─────────────────┐
   │ rcu_read_lock() │
   ├─────────────────┤
   │ Read data       │
   │ (may be stale)  │
   ├─────────────────┤
   │rcu_read_unlock()│
   └─────────────────┘
   
   Writer Side:
   ┌──────────────────────┐
   │ Allocate new version │
   ├──────────────────────┤
   │ Update pointer       │
   │ (rcu_assign_pointer) │
   ├──────────────────────┤
   │ Wait grace period    │
   │ (synchronize_rcu)    │
   ├──────────────────────┤
   │ Free old version     │
   └──────────────────────┘

Grace Period
------------

A grace period is the time during which all pre-existing RCU readers complete.

.. code-block:: text

   Time  →
   
   Reader 1:  [===read===]
   Reader 2:       [===read===]
   Reader 3:            [===read===]
   
   Update:     ^
   Grace:      |--------GP--------|
   Free old:                      ^

Basic RCU Usage
===============

Reader Side
-----------

Simple Read
~~~~~~~~~~~

.. code-block:: c

   struct config {
       int timeout;
       int retries;
   };
   
   static struct config __rcu *global_config;
   
   static int get_timeout(void) {
       struct config *cfg;
       int timeout;
       
       rcu_read_lock();
       cfg = rcu_dereference(global_config);
       timeout = cfg ? cfg->timeout : DEFAULT_TIMEOUT;
       rcu_read_unlock();
       
       return timeout;
   }

**Important:** Don't dereference RCU pointer outside RCU read-side critical section!

.. code-block:: c

   /* WRONG */
   static int bad_example(void) {
       struct config *cfg;
       
       rcu_read_lock();
       cfg = rcu_dereference(global_config);
       rcu_read_unlock();
       
       return cfg->timeout;  // BUG: May be freed!
   }
   
   /* CORRECT */
   static int good_example(void) {
       struct config *cfg;
       int timeout;
       
       rcu_read_lock();
       cfg = rcu_dereference(global_config);
       timeout = cfg ? cfg->timeout : 0;
       rcu_read_unlock();
       
       return timeout;
   }

Writer Side - Update
--------------------

.. code-block:: c

   static DEFINE_SPINLOCK(config_lock);
   
   static int update_config(int new_timeout, int new_retries) {
       struct config *old_cfg, *new_cfg;
       
       /* Allocate new config */
       new_cfg = kmalloc(sizeof(*new_cfg), GFP_KERNEL);
       if (!new_cfg)
           return -ENOMEM;
       
       new_cfg->timeout = new_timeout;
       new_cfg->retries = new_retries;
       
       /* Update pointer */
       spin_lock(&config_lock);
       old_cfg = rcu_dereference_protected(global_config,
                                            lockdep_is_held(&config_lock));
       rcu_assign_pointer(global_config, new_cfg);
       spin_unlock(&config_lock);
       
       /* Wait for all readers to complete */
       synchronize_rcu();
       
       /* Safe to free old config */
       kfree(old_cfg);
       
       return 0;
   }

Writer Side - Deletion
----------------------

.. code-block:: c

   static void delete_config(void) {
       struct config *old_cfg;
       
       spin_lock(&config_lock);
       old_cfg = rcu_dereference_protected(global_config,
                                            lockdep_is_held(&config_lock));
       rcu_assign_pointer(global_config, NULL);
       spin_unlock(&config_lock);
       
       synchronize_rcu();
       kfree(old_cfg);
   }

RCU Lists
=========

List Operations
---------------

.. code-block:: c

   #include <linux/rculist.h>
   
   struct device_node {
       int id;
       char name[32];
       struct list_head list;
       struct rcu_head rcu;
   };
   
   static LIST_HEAD(device_list);
   static DEFINE_SPINLOCK(device_list_lock);

Add to List
~~~~~~~~~~~

.. code-block:: c

   static int add_device(int id, const char *name) {
       struct device_node *node;
       
       node = kmalloc(sizeof(*node), GFP_KERNEL);
       if (!node)
           return -ENOMEM;
       
       node->id = id;
       strncpy(node->name, name, sizeof(node->name) - 1);
       
       spin_lock(&device_list_lock);
       list_add_rcu(&node->list, &device_list);
       spin_unlock(&device_list_lock);
       
       return 0;
   }

Remove from List
~~~~~~~~~~~~~~~~

.. code-block:: c

   static void device_free_rcu(struct rcu_head *rcu) {
       struct device_node *node;
       node = container_of(rcu, struct device_node, rcu);
       kfree(node);
   }
   
   static int remove_device(int id) {
       struct device_node *node;
       
       spin_lock(&device_list_lock);
       
       list_for_each_entry(node, &device_list, list) {
           if (node->id == id) {
               list_del_rcu(&node->list);
               spin_unlock(&device_list_lock);
               
               call_rcu(&node->rcu, device_free_rcu);
               return 0;
           }
       }
       
       spin_unlock(&device_list_lock);
       return -ENOENT;
   }

Iterate List (Read)
~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static struct device_node *find_device(int id) {
       struct device_node *node, *found = NULL;
       
       rcu_read_lock();
       
       list_for_each_entry_rcu(node, &device_list, list) {
           if (node->id == id) {
               /* Can't return pointer - would escape RCU read-side */
               /* Instead, copy data */
               found = node;
               break;
           }
       }
       
       rcu_read_unlock();
       return found;
   }
   
   static void print_all_devices(void) {
       struct device_node *node;
       
       rcu_read_lock();
       
       list_for_each_entry_rcu(node, &device_list, list) {
           pr_info("Device %d: %s\n", node->id, node->name);
       }
       
       rcu_read_unlock();
   }

Replace in List
~~~~~~~~~~~~~~~

.. code-block:: c

   static int update_device(int id, const char *new_name) {
       struct device_node *old_node, *new_node;
       int ret = -ENOENT;
       
       new_node = kmalloc(sizeof(*new_node), GFP_KERNEL);
       if (!new_node)
           return -ENOMEM;
       
       new_node->id = id;
       strncpy(new_node->name, new_name, sizeof(new_node->name) - 1);
       
       spin_lock(&device_list_lock);
       
       list_for_each_entry(old_node, &device_list, list) {
           if (old_node->id == id) {
               list_replace_rcu(&old_node->list, &new_node->list);
               ret = 0;
               break;
           }
       }
       
       spin_unlock(&device_list_lock);
       
       if (ret == 0) {
           synchronize_rcu();
           kfree(old_node);
       } else {
           kfree(new_node);
       }
       
       return ret;
   }

Hash Tables with RCU
====================

.. code-block:: c

   #include <linux/rculist.h>
   #include <linux/hashtable.h>
   
   #define HASH_BITS 8
   
   struct cache_entry {
       int key;
       void *data;
       struct hlist_node hash;
       struct rcu_head rcu;
   };
   
   static DEFINE_HASHTABLE(cache_table, HASH_BITS);
   static DEFINE_SPINLOCK(cache_lock);
   
   /* Insert */
   static int cache_insert(int key, void *data) {
       struct cache_entry *entry;
       
       entry = kmalloc(sizeof(*entry), GFP_KERNEL);
       if (!entry)
           return -ENOMEM;
       
       entry->key = key;
       entry->data = data;
       
       spin_lock(&cache_lock);
       hash_add_rcu(cache_table, &entry->hash, key);
       spin_unlock(&cache_lock);
       
       return 0;
   }
   
   /* Lookup */
   static void *cache_lookup(int key) {
       struct cache_entry *entry;
       void *data = NULL;
       
       rcu_read_lock();
       
       hash_for_each_possible_rcu(cache_table, entry, hash, key) {
           if (entry->key == key) {
               data = entry->data;
               break;
           }
       }
       
       rcu_read_unlock();
       return data;
   }
   
   /* Delete */
   static void cache_entry_free(struct rcu_head *rcu) {
       struct cache_entry *entry;
       entry = container_of(rcu, struct cache_entry, rcu);
       kfree(entry);
   }
   
   static int cache_delete(int key) {
       struct cache_entry *entry;
       int ret = -ENOENT;
       
       spin_lock(&cache_lock);
       
       hash_for_each_possible(cache_table, entry, hash, key) {
           if (entry->key == key) {
               hash_del_rcu(&entry->hash);
               ret = 0;
               break;
           }
       }
       
       spin_unlock(&cache_lock);
       
       if (ret == 0)
           call_rcu(&entry->rcu, cache_entry_free);
       
       return ret;
   }

RCU Variants
============

Classic RCU (CONFIG_TREE_RCU)
-----------------------------

Standard RCU for SMP systems.

.. code-block:: c

   rcu_read_lock();
   /* Read-side critical section */
   rcu_read_unlock();
   
   synchronize_rcu();

RCU-sched
---------

.. code-block:: c

   rcu_read_lock_sched();
   /* Read-side critical section */
   rcu_read_unlock_sched();
   
   synchronize_sched();

RCU-bh (Bottom Half)
--------------------

.. code-block:: c

   rcu_read_lock_bh();
   /* Read-side critical section */
   rcu_read_unlock_bh();
   
   synchronize_rcu_bh();

SRCU (Sleepable RCU)
--------------------

Allows sleeping in read-side critical section.

.. code-block:: c

   #include <linux/srcu.h>
   
   DEFINE_SRCU(my_srcu);
   
   /* Reader */
   int idx;
   idx = srcu_read_lock(&my_srcu);
   /* Can sleep here! */
   msleep(100);
   srcu_read_unlock(&my_srcu, idx);
   
   /* Writer */
   synchronize_srcu(&my_srcu);

Call RCU - Deferred Callbacks
==============================

Basic Usage
-----------

.. code-block:: c

   struct my_data {
       int value;
       struct rcu_head rcu;
   };
   
   static void my_data_free(struct rcu_head *rcu) {
       struct my_data *data = container_of(rcu, struct my_data, rcu);
       pr_info("Freeing data with value %d\n", data->value);
       kfree(data);
   }
   
   static void delete_data(struct my_data *data) {
       /* Schedule callback after grace period */
       call_rcu(&data->rcu, my_data_free);
       /* Returns immediately - callback runs later */
   }

Batching Deletes
----------------

.. code-block:: c

   static void delete_all_devices(void) {
       struct device_node *node, *tmp;
       
       spin_lock(&device_list_lock);
       
       list_for_each_entry_safe(node, tmp, &device_list, list) {
           list_del_rcu(&node->list);
           call_rcu(&node->rcu, device_free_rcu);
       }
       
       spin_unlock(&device_list_lock);
       
       /* All callbacks scheduled, no need to wait */
   }

Complex RCU Patterns
====================

RCU with Reference Counting
----------------------------

.. code-block:: c

   struct shared_data {
       atomic_t refcount;
       struct rcu_head rcu;
       void *data;
   };
   
   static void shared_data_free(struct rcu_head *rcu) {
       struct shared_data *sd = container_of(rcu, struct shared_data, rcu);
       kfree(sd->data);
       kfree(sd);
   }
   
   static struct shared_data *shared_data_get(struct shared_data *sd) {
       if (sd)
           atomic_inc(&sd->refcount);
       return sd;
   }
   
   static void shared_data_put(struct shared_data *sd) {
       if (sd && atomic_dec_and_test(&sd->refcount))
           call_rcu(&sd->rcu, shared_data_free);
   }
   
   /* Usage */
   static struct shared_data __rcu *global_data;
   
   static struct shared_data *get_global_data(void) {
       struct shared_data *sd;
       
       rcu_read_lock();
       sd = rcu_dereference(global_data);
       sd = shared_data_get(sd);  // Increment refcount
       rcu_read_unlock();
       
       return sd;  // Safe to use outside RCU read-side
   }
   
   static void use_data(void) {
       struct shared_data *sd;
       
       sd = get_global_data();
       if (sd) {
           /* Can use sd safely */
           process_data(sd->data);
           shared_data_put(sd);
       }
   }

RCU with Dynamic Structures
----------------------------

.. code-block:: c

   struct tree_node {
       int key;
       void *data;
       struct tree_node __rcu *left;
       struct tree_node __rcu *right;
       struct rcu_head rcu;
   };
   
   static struct tree_node __rcu *tree_root;
   
   static void *tree_lookup(int key) {
       struct tree_node *node;
       void *data = NULL;
       
       rcu_read_lock();
       
       node = rcu_dereference(tree_root);
       while (node) {
           if (key == node->key) {
               data = node->data;
               break;
           } else if (key < node->key) {
               node = rcu_dereference(node->left);
           } else {
               node = rcu_dereference(node->right);
           }
       }
       
       rcu_read_unlock();
       return data;
   }

Performance Considerations
==========================

Read Performance
----------------

- **No locks:** Zero overhead for readers
- **No atomic operations:** Just memory reads
- **Cache-friendly:** Readers don't modify cache lines
- **Scalable:** Readers don't contend with each other

Write Performance
-----------------

- **Allocation overhead:** Must allocate new versions
- **Grace period wait:** Can be significant (milliseconds)
- **Memory overhead:** Old versions kept during grace period

Optimization Techniques
-----------------------

.. code-block:: c

   /* Use call_rcu instead of synchronize_rcu for better performance */
   
   /* Bad: Synchronous wait */
   for (i = 0; i < 1000; i++) {
       update_pointer();
       synchronize_rcu();  // Wait 1000 times!
       kfree(old);
   }
   
   /* Good: Asynchronous callbacks */
   for (i = 0; i < 1000; i++) {
       update_pointer();
       call_rcu(&old->rcu, free_callback);  // Schedule 1000 callbacks
   }
   /* All freed after single grace period */

Common Pitfalls
===============

1. **Dereferencing outside RCU read-side**

.. code-block:: c

   /* WRONG */
   ptr = rcu_dereference(global_ptr);
   rcu_read_unlock();
   use(ptr);  // May be freed!

2. **Forgetting rcu_assign_pointer**

.. code-block:: c

   /* WRONG */
   global_ptr = new_ptr;  // Missing barrier!
   
   /* CORRECT */
   rcu_assign_pointer(global_ptr, new_ptr);

3. **Using wrong dereference function**

.. code-block:: c

   /* Reader side */
   ptr = rcu_dereference(global_ptr);  // Correct
   
   /* Writer side (under lock) */
   ptr = rcu_dereference_protected(global_ptr,
                                   lockdep_is_held(&lock));  // Correct

Debugging
=========

.. code-block:: text

   CONFIG_PROVE_RCU=y
   CONFIG_RCU_TRACE=y

Best Practices
==============

1. Use **RCU for read-mostly** workloads
2. **Keep read-side critical sections short**
3. **Don't sleep** in RCU read-side (unless SRCU)
4. Use **call_rcu** instead of synchronize_rcu for performance
5. **Validate** with lockdep and RCU debugging
6. **Document** RCU usage and requirements
7. Use **appropriate dereference** functions

See Also
========

- Linux_Kernel_Synchronization.rst
- Linux_Spinlocks.rst
- Linux_Mutexes_Semaphores.rst
- Linux_Atomic_Operations.rst

References
==========

- Documentation/RCU/
- Documentation/RCU/whatisRCU.rst
- Documentation/RCU/checklist.rst
- include/linux/rcupdate.h
- kernel/rcu/
