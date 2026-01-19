====================================
Linux Atomic Operations Guide
====================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Atomic Integer Operations
--------------------------

.. code-block:: c

   #include <linux/atomic.h>
   #include <asm/atomic.h>
   
   /* Declaration and initialization */
   atomic_t counter = ATOMIC_INIT(0);
   atomic_set(&counter, 5);
   
   /* Read */
   int val = atomic_read(&counter);
   
   /* Arithmetic */
   atomic_inc(&counter);                // counter++
   atomic_dec(&counter);                // counter--
   atomic_add(5, &counter);             // counter += 5
   atomic_sub(3, &counter);             // counter -= 3
   
   /* Test and return */
   int old = atomic_inc_return(&counter);       // Returns new value
   int old = atomic_dec_return(&counter);
   int old = atomic_add_return(5, &counter);
   
   /* Test operations */
   if (atomic_dec_and_test(&counter))   // Returns true if result is 0
   if (atomic_inc_and_test(&counter))
   if (atomic_sub_and_test(5, &counter))
   
   /* Compare and exchange */
   int old_val = atomic_cmpxchg(&counter, old, new);
   int old_val = atomic_xchg(&counter, new);

64-bit Atomic Operations
------------------------

.. code-block:: c

   atomic64_t big_counter = ATOMIC64_INIT(0);
   
   atomic64_inc(&big_counter);
   atomic64_add(1000000, &big_counter);
   s64 val = atomic64_read(&big_counter);

Atomic Bitops
-------------

.. code-block:: c

   unsigned long flags = 0;
   
   /* Set, clear, flip bits */
   set_bit(5, &flags);              // Set bit 5
   clear_bit(5, &flags);            // Clear bit 5
   change_bit(5, &flags);           // Toggle bit 5
   
   /* Test and modify */
   int was_set = test_and_set_bit(5, &flags);
   int was_set = test_and_clear_bit(5, &flags);
   int was_set = test_and_change_bit(5, &flags);
   
   /* Test only */
   if (test_bit(5, &flags))

Memory Barriers
---------------

.. code-block:: c

   /* Compiler barriers */
   barrier();                       // Prevent compiler reordering
   
   /* CPU memory barriers */
   smp_mb();                        // Full memory barrier
   smp_rmb();                       // Read memory barrier
   smp_wmb();                       // Write memory barrier
   
   /* Acquire/release semantics */
   smp_load_acquire(&ptr);         // Load with acquire semantics
   smp_store_release(&ptr, val);   // Store with release semantics
   
   /* Read/write once */
   val = READ_ONCE(variable);
   WRITE_ONCE(variable, val);

Atomic Operations Fundamentals
===============================

Introduction
------------

Atomic operations are indivisible operations that complete without interruption. They provide lock-free synchronization for simple operations.

**Key Characteristics:**

- No locks required
- Cannot be interrupted mid-operation
- Architecture-specific implementation
- Compiler and CPU barriers included
- Very efficient for simple operations

**When to Use:**

- Simple counters and flags
- Reference counting
- Simple state machines
- Lock-free algorithms

**When NOT to Use:**

- Complex multi-variable updates
- Operations that can fail
- When ordering of multiple operations matters

Atomic Integer Types
=====================

atomic_t Type
-------------

.. code-block:: c

   typedef struct {
       int counter;
   } atomic_t;

Declaration and Initialization
-------------------------------

.. code-block:: c

   /* Static initialization */
   static atomic_t my_counter = ATOMIC_INIT(0);
   static atomic_t ref_count = ATOMIC_INIT(1);
   
   /* Dynamic initialization */
   struct device {
       atomic_t use_count;
   };
   
   void device_init(struct device *dev) {
       atomic_set(&dev->use_count, 0);
   }

Basic Operations
----------------

Read and Write
~~~~~~~~~~~~~~

.. code-block:: c

   atomic_t counter = ATOMIC_INIT(10);
   
   /* Read - returns int */
   int value = atomic_read(&counter);
   
   /* Write - sets new value */
   atomic_set(&counter, 42);

Increment and Decrement
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Simple increment/decrement */
   atomic_inc(&counter);      // counter++
   atomic_dec(&counter);      // counter--
   
   /* With return value */
   int new_val = atomic_inc_return(&counter);
   int new_val = atomic_dec_return(&counter);
   
   /* Test operations - return true if result is zero */
   if (atomic_dec_and_test(&counter)) {
       pr_info("Counter reached zero\n");
   }
   
   if (atomic_inc_and_test(&counter)) {
       pr_info("Counter is zero after increment\n");
   }

Add and Subtract
~~~~~~~~~~~~~~~~

.. code-block:: c

   /* Simple add/subtract */
   atomic_add(5, &counter);       // counter += 5
   atomic_sub(3, &counter);       // counter -= 3
   
   /* With return value */
   int new_val = atomic_add_return(10, &counter);
   int new_val = atomic_sub_return(5, &counter);
   
   /* Test if result is zero */
   if (atomic_sub_and_test(5, &counter)) {
       pr_info("Result is zero\n");
   }
   
   /* Test and add - returns true if result is negative */
   if (atomic_add_negative(-10, &counter)) {
       pr_info("Result is negative\n");
   }

Compare and Swap Operations
----------------------------

.. code-block:: c

   atomic_t value = ATOMIC_INIT(10);
   
   /* Compare and exchange (cmpxchg) */
   int old_val = atomic_cmpxchg(&value, 10, 20);
   if (old_val == 10) {
       pr_info("Successfully changed from 10 to 20\n");
   } else {
       pr_info("Value was %d, not 10\n", old_val);
   }
   
   /* Unconditional exchange */
   old_val = atomic_xchg(&value, 30);
   pr_info("Old value was %d, now it's 30\n", old_val);

Lock-Free Reference Counting
-----------------------------

.. code-block:: c

   struct shared_resource {
       atomic_t refcount;
       void *data;
   };
   
   static struct shared_resource *resource_get(struct shared_resource *res) {
       atomic_inc(&res->refcount);
       return res;
   }
   
   static void resource_put(struct shared_resource *res) {
       if (atomic_dec_and_test(&res->refcount)) {
           /* Last reference released */
           kfree(res->data);
           kfree(res);
       }
   }
   
   /* Usage */
   void use_resource(struct shared_resource *res) {
       struct shared_resource *my_ref;
       
       my_ref = resource_get(res);  // Increment refcount
       
       /* Use resource */
       process_data(my_ref->data);
       
       resource_put(my_ref);  // Decrement refcount
   }

64-bit Atomic Operations
========================

atomic64_t Type
---------------

.. code-block:: c

   typedef struct {
       s64 counter;
   } atomic64_t;

Operations
----------

.. code-block:: c

   /* Initialization */
   atomic64_t big_counter = ATOMIC64_INIT(0);
   
   /* Read and write */
   s64 value = atomic64_read(&big_counter);
   atomic64_set(&big_counter, 1000000000LL);
   
   /* Increment/decrement */
   atomic64_inc(&big_counter);
   atomic64_dec(&big_counter);
   s64 new_val = atomic64_inc_return(&big_counter);
   
   /* Add/subtract */
   atomic64_add(500000, &big_counter);
   atomic64_sub(100000, &big_counter);
   s64 new_val = atomic64_add_return(1000000, &big_counter);
   
   /* Compare and exchange */
   s64 old = atomic64_cmpxchg(&big_counter, 1000000, 2000000);
   
   /* Test operations */
   if (atomic64_dec_and_test(&big_counter)) {
       pr_info("Counter is zero\n");
   }

Statistics Counter Example
---------------------------

.. code-block:: c

   struct network_stats {
       atomic64_t rx_packets;
       atomic64_t rx_bytes;
       atomic64_t tx_packets;
       atomic64_t tx_bytes;
       atomic64_t errors;
   };
   
   static void update_rx_stats(struct network_stats *stats,
                                size_t packet_len) {
       atomic64_inc(&stats->rx_packets);
       atomic64_add(packet_len, &stats->rx_bytes);
   }
   
   static void show_stats(struct network_stats *stats) {
       pr_info("RX: %lld packets, %lld bytes\n",
               atomic64_read(&stats->rx_packets),
               atomic64_read(&stats->rx_bytes));
       pr_info("TX: %lld packets, %lld bytes\n",
               atomic64_read(&stats->tx_packets),
               atomic64_read(&stats->tx_bytes));
       pr_info("Errors: %lld\n", atomic64_read(&stats->errors));
   }

Atomic Bit Operations
======================

Introduction
------------

Atomic bit operations work on individual bits in unsigned long variables or arrays.

**Key Functions:**

- Set, clear, toggle bits atomically
- Test bit state
- Test and modify atomically
- Find first set/clear bit

Basic Bit Operations
--------------------

.. code-block:: c

   unsigned long flags = 0;
   
   /* Set bit (make it 1) */
   set_bit(0, &flags);          // Set bit 0
   set_bit(5, &flags);          // Set bit 5
   
   /* Clear bit (make it 0) */
   clear_bit(0, &flags);        // Clear bit 0
   
   /* Toggle bit */
   change_bit(5, &flags);       // Flip bit 5
   
   /* Test bit (non-atomic read) */
   if (test_bit(5, &flags)) {
       pr_info("Bit 5 is set\n");
   }

Test and Modify Operations
---------------------------

.. code-block:: c

   unsigned long flags = 0;
   int old_value;
   
   /* Test and set - returns old value */
   old_value = test_and_set_bit(3, &flags);
   if (old_value == 0) {
       pr_info("Bit was clear, now set\n");
   } else {
       pr_info("Bit was already set\n");
   }
   
   /* Test and clear */
   old_value = test_and_clear_bit(3, &flags);
   if (old_value == 1) {
       pr_info("Bit was set, now cleared\n");
   }
   
   /* Test and toggle */
   old_value = test_and_change_bit(5, &flags);
   pr_info("Bit 5 was %d, now %d\n", old_value, !old_value);

Bit Array Operations
--------------------

.. code-block:: c

   #define NUM_FLAGS 256
   unsigned long flag_array[BITS_TO_LONGS(NUM_FLAGS)];
   
   /* Initialize all bits to 0 */
   bitmap_zero(flag_array, NUM_FLAGS);
   
   /* Set bit 100 */
   set_bit(100, flag_array);
   
   /* Test bit 100 */
   if (test_bit(100, flag_array)) {
       pr_info("Bit 100 is set\n");
   }
   
   /* Find first set bit */
   int first = find_first_bit(flag_array, NUM_FLAGS);
   if (first < NUM_FLAGS) {
       pr_info("First set bit is %d\n", first);
   }
   
   /* Find first zero bit */
   first = find_first_zero_bit(flag_array, NUM_FLAGS);
   
   /* Find next set bit after position */
   int next = find_next_bit(flag_array, NUM_FLAGS, first + 1);

Lock-Free Flag Example
-----------------------

.. code-block:: c

   #define FLAG_READY      0
   #define FLAG_BUSY       1
   #define FLAG_ERROR      2
   
   struct device {
       unsigned long flags;
       void *data;
   };
   
   static int device_acquire(struct device *dev) {
       /* Try to mark device as busy */
       if (test_and_set_bit(FLAG_BUSY, &dev->flags))
           return -EBUSY;  // Already busy
       
       /* Wait for ready */
       if (!test_bit(FLAG_READY, &dev->flags)) {
           clear_bit(FLAG_BUSY, &dev->flags);
           return -ENODEV;
       }
       
       return 0;
   }
   
   static void device_release(struct device *dev) {
       clear_bit(FLAG_BUSY, &dev->flags);
   }
   
   static void device_set_ready(struct device *dev) {
       set_bit(FLAG_READY, &dev->flags);
   }
   
   static void device_set_error(struct device *dev) {
       set_bit(FLAG_ERROR, &dev->flags);
   }

Resource Bitmap Example
------------------------

.. code-block:: c

   #define MAX_RESOURCES 64
   
   struct resource_pool {
       unsigned long bitmap;
       void *resources[MAX_RESOURCES];
       atomic_t allocated;
   };
   
   static int alloc_resource(struct resource_pool *pool) {
       int bit;
       
       /* Find first free resource */
       do {
           bit = find_first_zero_bit(&pool->bitmap, MAX_RESOURCES);
           if (bit >= MAX_RESOURCES)
               return -ENOSPC;  // No free resources
       } while (test_and_set_bit(bit, &pool->bitmap));
       
       atomic_inc(&pool->allocated);
       return bit;
   }
   
   static void free_resource(struct resource_pool *pool, int id) {
       if (id < 0 || id >= MAX_RESOURCES)
           return;
       
       if (test_and_clear_bit(id, &pool->bitmap))
           atomic_dec(&pool->allocated);
   }

Memory Barriers
===============

Introduction
------------

Memory barriers prevent CPU and compiler from reordering memory accesses.

**Types:**

- **Compiler barriers:** Prevent compiler reordering
- **CPU barriers:** Prevent CPU reordering
- **SMP barriers:** Only on SMP systems

Compiler Barrier
----------------

.. code-block:: c

   /* Prevent compiler from reordering across this point */
   barrier();
   
   /* Example */
   int ready = 0;
   int data = 0;
   
   void producer(void) {
       data = 42;
       barrier();  // Ensure data written before ready
       ready = 1;
   }

CPU Memory Barriers
-------------------

.. code-block:: c

   /* Full memory barrier */
   smp_mb();        // Prevents all memory reordering
   
   /* Read barrier */
   smp_rmb();       // Prevents read-read reordering
   
   /* Write barrier */
   smp_wmb();       // Prevents write-write reordering
   
   /* Example: Producer-Consumer */
   struct message {
       int data;
       int ready;
   };
   
   /* Producer */
   void send_message(struct message *msg, int value) {
       msg->data = value;
       smp_wmb();  // Ensure data written before ready
       msg->ready = 1;
   }
   
   /* Consumer */
   int receive_message(struct message *msg) {
       while (!msg->ready)
           cpu_relax();
       smp_rmb();  // Ensure ready read before data
       return msg->data;
   }

Acquire and Release Semantics
------------------------------

.. code-block:: c

   /* Load with acquire semantics */
   ptr = smp_load_acquire(&shared_ptr);
   /* Subsequent reads cannot be reordered before this */
   
   /* Store with release semantics */
   smp_store_release(&shared_ptr, new_ptr);
   /* Previous writes cannot be reordered after this */
   
   /* Example: Lock-free queue */
   struct queue_entry {
       void *data;
       struct queue_entry *next;
   };
   
   struct lockfree_queue {
       struct queue_entry *head;
       struct queue_entry *tail;
   };
   
   void enqueue(struct lockfree_queue *q, void *data) {
       struct queue_entry *entry = kmalloc(sizeof(*entry), GFP_ATOMIC);
       entry->data = data;
       entry->next = NULL;
       
       struct queue_entry *tail = smp_load_acquire(&q->tail);
       smp_store_release(&tail->next, entry);
       smp_store_release(&q->tail, entry);
   }

READ_ONCE and WRITE_ONCE
-------------------------

Prevent compiler optimizations that could cause issues.

.. code-block:: c

   /* Ensure single read from memory */
   value = READ_ONCE(shared_variable);
   
   /* Ensure single write to memory */
   WRITE_ONCE(shared_variable, new_value);
   
   /* Example: Busy-wait loop */
   void wait_for_ready(volatile int *ready) {
       /* Wrong - compiler might optimize away loop */
       while (*ready == 0)
           ;
       
       /* Correct */
       while (READ_ONCE(*ready) == 0)
           cpu_relax();
   }
   
   /* Example: Shared flag */
   static int shutdown_flag = 0;
   
   void request_shutdown(void) {
       WRITE_ONCE(shutdown_flag, 1);
       smp_mb();  // Ensure visible to all CPUs
   }
   
   int check_shutdown(void) {
       return READ_ONCE(shutdown_flag);
   }

Complete Examples
=================

Lock-Free Stack
---------------

.. code-block:: c

   struct stack_node {
       void *data;
       struct stack_node *next;
   };
   
   struct lockfree_stack {
       struct stack_node *head;
   };
   
   static void stack_init(struct lockfree_stack *stack) {
       stack->head = NULL;
   }
   
   static void stack_push(struct lockfree_stack *stack, void *data) {
       struct stack_node *node, *old_head;
       
       node = kmalloc(sizeof(*node), GFP_ATOMIC);
       node->data = data;
       
       do {
           old_head = READ_ONCE(stack->head);
           node->next = old_head;
       } while (cmpxchg(&stack->head, old_head, node) != old_head);
   }
   
   static void *stack_pop(struct lockfree_stack *stack) {
       struct stack_node *old_head, *new_head;
       void *data;
       
       do {
           old_head = READ_ONCE(stack->head);
           if (!old_head)
               return NULL;
           new_head = READ_ONCE(old_head->next);
       } while (cmpxchg(&stack->head, old_head, new_head) != old_head);
       
       data = old_head->data;
       kfree(old_head);
       return data;
   }

Reference Counted Object
------------------------

.. code-block:: c

   struct ref_object {
       atomic_t refcount;
       void (*release)(struct ref_object *);
       void *private_data;
   };
   
   static void ref_object_init(struct ref_object *obj,
                                void (*release)(struct ref_object *)) {
       atomic_set(&obj->refcount, 1);
       obj->release = release;
   }
   
   static struct ref_object *ref_object_get(struct ref_object *obj) {
       atomic_inc(&obj->refcount);
       return obj;
   }
   
   static void ref_object_put(struct ref_object *obj) {
       if (atomic_dec_and_test(&obj->refcount)) {
           if (obj->release)
               obj->release(obj);
       }
   }
   
   /* Usage example */
   struct my_data {
       struct ref_object ref;
       char name[32];
   };
   
   static void my_data_release(struct ref_object *ref) {
       struct my_data *data = container_of(ref, struct my_data, ref);
       pr_info("Releasing %s\n", data->name);
       kfree(data);
   }
   
   static struct my_data *create_data(const char *name) {
       struct my_data *data;
       
       data = kzalloc(sizeof(*data), GFP_KERNEL);
       if (!data)
           return NULL;
       
       ref_object_init(&data->ref, my_data_release);
       strncpy(data->name, name, sizeof(data->name) - 1);
       
       return data;
   }

Performance Considerations
==========================

When to Use Atomic Operations
------------------------------

**Good Use Cases:**

- Simple counters
- Reference counts
- Flags and state bits
- Statistics gathering

**Bad Use Cases:**

- Complex multi-step operations
- When locks already held
- Large data structure updates

Performance Comparison
----------------------

.. code-block:: c

   /* Fastest - atomic operation */
   atomic_inc(&counter);
   
   /* Slower - spinlock */
   spin_lock(&lock);
   counter++;
   spin_unlock(&lock);
   
   /* Slowest - mutex */
   mutex_lock(&mutex);
   counter++;
   mutex_unlock(&mutex);

Debugging
=========

.. code-block:: text

   # Kernel config options
   CONFIG_DEBUG_ATOMIC_SLEEP=y
   CONFIG_DEBUG_SPINLOCK=y

Common Pitfalls
===============

1. **Assuming atomicity of multiple operations**

.. code-block:: c

   /* WRONG - race condition */
   if (atomic_read(&counter) == 0)
       atomic_set(&counter, 1);
   
   /* CORRECT */
   if (atomic_cmpxchg(&counter, 0, 1) == 0)
       pr_info("Changed from 0 to 1\n");

2. **Missing memory barriers**

.. code-block:: c

   /* May not work on all architectures */
   data_ready = 1;
   flag = 1;
   
   /* Correct */
   data_ready = 1;
   smp_wmb();
   flag = 1;

Best Practices
==============

1. Use **atomic operations** for simple counters
2. Use **READ_ONCE/WRITE_ONCE** for shared variables
3. Add **memory barriers** when ordering matters
4. Prefer **existing patterns** (refcount, bitops)
5. **Test on SMP** systems
6. Use **lockdep** and other debugging tools
7. **Document** memory ordering requirements

See Also
========

- Linux_Kernel_Synchronization.rst
- Linux_Spinlocks.rst
- Linux_RCU.rst
- Linux_Mutexes_Semaphores.rst

References
==========

- Documentation/atomic_t.txt
- Documentation/memory-barriers.txt
- include/linux/atomic.h
- include/asm-generic/bitops/atomic.h
