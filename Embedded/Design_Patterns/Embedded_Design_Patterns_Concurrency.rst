=============================================
Embedded Design Patterns - Concurrency
=============================================

:Author: Embedded Systems Design Patterns Documentation
:Date: January 2026
:Version: 1.0
:Focus: Concurrency patterns for embedded systems and RTOS

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Concurrency Patterns Overview
------------------------------

.. code-block:: text

   Concurrency Patterns:
   
   1. Guarded Call
      - Protect shared resources
      - Mutex/semaphore guards
   
   2. Queuing
      - Producer-consumer
      - Thread-safe queues
   
   3. Rendezvous
      - Synchronization point
      - Multiple tasks meet
   
   4. Simultaneous Locking
      - Lock ordering
      - Deadlock prevention
   
   5. Message Queue
      - Inter-task communication
      - Asynchronous messaging

Guarded Call Pattern
====================

Intent
------

Protect shared resources from concurrent access using mutual exclusion.

Mutex-Based Guard
-----------------

.. code-block:: c

   // Shared resource
   typedef struct {
       uint32_t value;
       osMutexId_t mutex;
   } GuardedCounter;
   
   void GuardedCounter_Init(GuardedCounter *self) {
       self->value = 0;
       
       const osMutexAttr_t mutex_attr = {
           .name = "CounterMutex",
           .attr_bits = osMutexRecursive | osMutexPrioInherit
       };
       
       self->mutex = osMutexNew(&mutex_attr);
   }
   
   void GuardedCounter_Increment(GuardedCounter *self) {
       osMutexAcquire(self->mutex, osWaitForever);
       self->value++;
       osMutexRelease(self->mutex);
   }
   
   uint32_t GuardedCounter_Get(GuardedCounter *self) {
       osMutexAcquire(self->mutex, osWaitForever);
       uint32_t val = self->value;
       osMutexRelease(self->mutex);
       return val;
   }

RAII-Style Guard (C with macros)
---------------------------------

.. code-block:: c

   // Automatic mutex guard using macros
   #define MUTEX_GUARD_START(mutex) \
       do { \
           osMutexAcquire(mutex, osWaitForever);
   
   #define MUTEX_GUARD_END(mutex) \
           osMutexRelease(mutex); \
       } while(0)
   
   void GuardedCounter_IncrementBy(GuardedCounter *self, uint32_t amount) {
       MUTEX_GUARD_START(self->mutex) {
           self->value += amount;
       } MUTEX_GUARD_END(self->mutex);
   }

Critical Section Guard
----------------------

.. code-block:: c

   // Bare-metal critical section
   typedef struct {
       uint32_t irq_state;
   } CriticalSection;
   
   void CriticalSection_Enter(CriticalSection *self) {
       self->irq_state = __get_PRIMASK();
       __disable_irq();
   }
   
   void CriticalSection_Exit(CriticalSection *self) {
       __set_PRIMASK(self->irq_state);
   }
   
   // Usage with automatic cleanup (requires compiler support)
   #define CRITICAL_SECTION() \
       for (CriticalSection __cs = {0}, *__p = &__cs; \
            __p && (CriticalSection_Enter(__p), 1); \
            CriticalSection_Exit(__p), __p = NULL)
   
   void atomic_operation(void) {
       CRITICAL_SECTION() {
           // Atomic code here
           shared_variable++;
       }
   }

Producer-Consumer Pattern
==========================

Intent
------

Decouple producers from consumers using a thread-safe queue.

Queue Implementation
--------------------

.. code-block:: c

   // Thread-safe ring buffer
   typedef struct {
       uint8_t *buffer;
       size_t size;
       size_t head;
       size_t tail;
       size_t count;
       osMutexId_t mutex;
       osSemaphoreId_t items;      // Counts filled slots
       osSemaphoreId_t spaces;     // Counts empty slots
   } ThreadSafeQueue;
   
   void ThreadSafeQueue_Init(ThreadSafeQueue *self, uint8_t *buffer, size_t size) {
       self->buffer = buffer;
       self->size = size;
       self->head = 0;
       self->tail = 0;
       self->count = 0;
       
       self->mutex = osMutexNew(NULL);
       self->items = osSemaphoreNew(size, 0, NULL);   // Initially 0
       self->spaces = osSemaphoreNew(size, size, NULL); // Initially full
   }
   
   bool ThreadSafeQueue_Put(ThreadSafeQueue *self, uint8_t data, uint32_t timeout) {
       // Wait for space
       if (osSemaphoreAcquire(self->spaces, timeout) != osOK) {
           return false;
       }
       
       osMutexAcquire(self->mutex, osWaitForever);
       
       self->buffer[self->tail] = data;
       self->tail = (self->tail + 1) % self->size;
       self->count++;
       
       osMutexRelease(self->mutex);
       
       // Signal item available
       osSemaphoreRelease(self->items);
       
       return true;
   }
   
   bool ThreadSafeQueue_Get(ThreadSafeQueue *self, uint8_t *data, uint32_t timeout) {
       // Wait for item
       if (osSemaphoreAcquire(self->items, timeout) != osOK) {
           return false;
       }
       
       osMutexAcquire(self->mutex, osWaitForever);
       
       *data = self->buffer[self->head];
       self->head = (self->head + 1) % self->size;
       self->count--;
       
       osMutexRelease(self->mutex);
       
       // Signal space available
       osSemaphoreRelease(self->spaces);
       
       return true;
   }

Producer Task
-------------

.. code-block:: c

   void producer_task(void *argument) {
       ThreadSafeQueue *queue = (ThreadSafeQueue *)argument;
       uint8_t data = 0;
       
       while (1) {
           // Generate data
           data = generate_sensor_reading();
           
           // Put in queue (block if full)
           if (!ThreadSafeQueue_Put(queue, data, osWaitForever)) {
               // Handle error
           }
           
           osDelay(100);  // 100ms interval
       }
   }

Consumer Task
-------------

.. code-block:: c

   void consumer_task(void *argument) {
       ThreadSafeQueue *queue = (ThreadSafeQueue *)argument;
       uint8_t data;
       
       while (1) {
           // Get from queue (block if empty)
           if (ThreadSafeQueue_Get(queue, &data, osWaitForever)) {
               // Process data
               process_sensor_reading(data);
           }
       }
   }

Multiple Producers/Consumers
-----------------------------

.. code-block:: c

   // Setup
   uint8_t buffer[128];
   ThreadSafeQueue queue;
   
   void setup_producer_consumer(void) {
       ThreadSafeQueue_Init(&queue, buffer, sizeof(buffer));
       
       // Create multiple producers
       osThreadNew(producer_task, &queue, NULL);
       osThreadNew(producer_task, &queue, NULL);
       
       // Create multiple consumers
       osThreadNew(consumer_task, &queue, NULL);
       osThreadNew(consumer_task, &queue, NULL);
       osThreadNew(consumer_task, &queue, NULL);
   }

Rendezvous Pattern
==================

Intent
------

Synchronize multiple tasks at a specific point before continuing.

Barrier Implementation
----------------------

.. code-block:: c

   // Barrier synchronization
   typedef struct {
       uint32_t count;          // Number of tasks to wait for
       uint32_t current;        // Current count
       osMutexId_t mutex;
       osSemaphoreId_t barrier;
   } Barrier;
   
   void Barrier_Init(Barrier *self, uint32_t count) {
       self->count = count;
       self->current = 0;
       self->mutex = osMutexNew(NULL);
       self->barrier = osSemaphoreNew(count, 0, NULL);
   }
   
   void Barrier_Wait(Barrier *self) {
       osMutexAcquire(self->mutex, osWaitForever);
       
       self->current++;
       
       if (self->current == self->count) {
           // Last task arrived, release all
           for (uint32_t i = 0; i < self->count; i++) {
               osSemaphoreRelease(self->barrier);
           }
           self->current = 0;  // Reset for next use
       }
       
       osMutexRelease(self->mutex);
       
       // Wait for all tasks
       osSemaphoreAcquire(self->barrier, osWaitForever);
   }

Usage Example
--------------

.. code-block:: c

   Barrier phase_barrier;
   
   void worker_task(void *argument) {
       while (1) {
           // Phase 1: Data collection
           collect_data();
           
           // Wait for all workers to finish phase 1
           Barrier_Wait(&phase_barrier);
           
           // Phase 2: Data processing (all workers have data)
           process_data();
           
           // Wait for all workers to finish phase 2
           Barrier_Wait(&phase_barrier);
           
           // Phase 3: Result transmission
           transmit_results();
           
           Barrier_Wait(&phase_barrier);
       }
   }
   
   void setup_workers(void) {
       const uint32_t num_workers = 4;
       Barrier_Init(&phase_barrier, num_workers);
       
       for (uint32_t i = 0; i < num_workers; i++) {
           osThreadNew(worker_task, NULL, NULL);
       }
   }

Simultaneous Locking Pattern
=============================

Intent
------

Acquire multiple locks safely without deadlock.

Lock Ordering
-------------

.. code-block:: c

   // Always acquire locks in consistent order (by address)
   void transfer_money(Account *from, Account *to, uint32_t amount) {
       // Determine lock order
       Account *first = (from < to) ? from : to;
       Account *second = (from < to) ? to : from;
       
       // Acquire in order
       osMutexAcquire(first->mutex, osWaitForever);
       osMutexAcquire(second->mutex, osWaitForever);
       
       // Critical section
       if (from->balance >= amount) {
           from->balance -= amount;
           to->balance += amount;
       }
       
       // Release in reverse order
       osMutexRelease(second->mutex);
       osMutexRelease(first->mutex);
   }

Try-Lock Pattern
----------------

.. code-block:: c

   // Try-lock with backoff to avoid deadlock
   bool acquire_multiple_locks(osMutexId_t *locks, size_t count, uint32_t timeout) {
       uint32_t start = osKernelGetTickCount();
       
       while (1) {
           size_t acquired = 0;
           
           // Try to acquire all locks
           for (size_t i = 0; i < count; i++) {
               if (osMutexAcquire(locks[i], 0) == osOK) {
                   acquired++;
               } else {
                   // Failed, release all acquired
                   for (size_t j = 0; j < acquired; j++) {
                       osMutexRelease(locks[j]);
                   }
                   break;
               }
           }
           
           if (acquired == count) {
               return true;  // All acquired
           }
           
           // Check timeout
           if ((osKernelGetTickCount() - start) >= timeout) {
               return false;
           }
           
           // Backoff
           osDelay(1);
       }
   }

Message Queue Pattern
======================

Intent
------

Enable asynchronous inter-task communication through message passing.

Message Structure
-----------------

.. code-block:: c

   // Message types
   typedef enum {
       MSG_SENSOR_DATA,
       MSG_COMMAND,
       MSG_STATUS,
       MSG_ERROR
   } MessageType;
   
   typedef struct {
       MessageType type;
       uint32_t timestamp;
       uint8_t data[32];
       size_t length;
   } Message;
   
   // Message queue wrapper
   typedef struct {
       osMessageQueueId_t queue;
   } MessageQueue;
   
   void MessageQueue_Init(MessageQueue *self, uint32_t capacity) {
       const osMessageQueueAttr_t attr = {
           .name = "MessageQueue"
       };
       
       self->queue = osMessageQueueNew(capacity, sizeof(Message), &attr);
   }
   
   bool MessageQueue_Send(MessageQueue *self, const Message *msg, uint32_t timeout) {
       return osMessageQueuePut(self->queue, msg, 0, timeout) == osOK;
   }
   
   bool MessageQueue_Receive(MessageQueue *self, Message *msg, uint32_t timeout) {
       return osMessageQueueGet(self->queue, msg, NULL, timeout) == osOK;
   }

Message-Based Communication
----------------------------

.. code-block:: c

   MessageQueue sensor_queue;
   MessageQueue control_queue;
   
   void sensor_task(void *argument) {
       Message msg;
       
       while (1) {
           // Read sensor
           float temp = read_temperature();
           
           // Create message
           msg.type = MSG_SENSOR_DATA;
           msg.timestamp = osKernelGetTickCount();
           memcpy(msg.data, &temp, sizeof(float));
           msg.length = sizeof(float);
           
           // Send to control task
           MessageQueue_Send(&sensor_queue, &msg, osWaitForever);
           
           osDelay(1000);
       }
   }
   
   void control_task(void *argument) {
       Message msg;
       
       while (1) {
           // Wait for sensor data
           if (MessageQueue_Receive(&sensor_queue, &msg, osWaitForever)) {
               if (msg.type == MSG_SENSOR_DATA) {
                   float temp;
                   memcpy(&temp, msg.data, sizeof(float));
                   
                   // Control logic
                   if (temp > 50.0f) {
                       activate_cooling();
                   }
               }
           }
       }
   }

Priority Message Queue
----------------------

.. code-block:: c

   // Message with priority
   typedef struct {
       Message msg;
       uint8_t priority;  // 0 = highest
   } PriorityMessage;
   
   typedef struct {
       PriorityMessage messages[QUEUE_SIZE];
       size_t count;
       osMutexId_t mutex;
       osSemaphoreId_t items;
   } PriorityMessageQueue;
   
   void PriorityMessageQueue_Init(PriorityMessageQueue *self) {
       self->count = 0;
       self->mutex = osMutexNew(NULL);
       self->items = osSemaphoreNew(QUEUE_SIZE, 0, NULL);
   }
   
   bool PriorityMessageQueue_Send(PriorityMessageQueue *self,
                                   const Message *msg, uint8_t priority) {
       osMutexAcquire(self->mutex, osWaitForever);
       
       if (self->count >= QUEUE_SIZE) {
           osMutexRelease(self->mutex);
           return false;
       }
       
       // Find insertion point
       size_t i;
       for (i = self->count; i > 0; i--) {
           if (self->messages[i - 1].priority <= priority) {
               break;
           }
           self->messages[i] = self->messages[i - 1];
       }
       
       // Insert message
       self->messages[i].msg = *msg;
       self->messages[i].priority = priority;
       self->count++;
       
       osMutexRelease(self->mutex);
       osSemaphoreRelease(self->items);
       
       return true;
   }

Read-Write Lock Pattern
========================

Intent
------

Allow multiple readers or single writer to access shared data.

Implementation
--------------

.. code-block:: c

   typedef struct {
       osMutexId_t mutex;
       osSemaphoreId_t write_sem;
       uint32_t readers;
   } RWLock;
   
   void RWLock_Init(RWLock *self) {
       self->mutex = osMutexNew(NULL);
       self->write_sem = osSemaphoreNew(1, 1, NULL);
       self->readers = 0;
   }
   
   void RWLock_ReadLock(RWLock *self) {
       osMutexAcquire(self->mutex, osWaitForever);
       
       self->readers++;
       if (self->readers == 1) {
           // First reader blocks writers
           osSemaphoreAcquire(self->write_sem, osWaitForever);
       }
       
       osMutexRelease(self->mutex);
   }
   
   void RWLock_ReadUnlock(RWLock *self) {
       osMutexAcquire(self->mutex, osWaitForever);
       
       self->readers--;
       if (self->readers == 0) {
           // Last reader allows writers
           osSemaphoreRelease(self->write_sem);
       }
       
       osMutexRelease(self->mutex);
   }
   
   void RWLock_WriteLock(RWLock *self) {
       osSemaphoreAcquire(self->write_sem, osWaitForever);
   }
   
   void RWLock_WriteUnlock(RWLock *self) {
       osSemaphoreRelease(self->write_sem);
   }

Usage
-----

.. code-block:: c

   RWLock config_lock;
   Config global_config;
   
   // Multiple readers
   void reader_task(void *argument) {
       while (1) {
           RWLock_ReadLock(&config_lock);
           
           // Read configuration (multiple readers allowed)
           uint32_t value = global_config.value;
           
           RWLock_ReadUnlock(&config_lock);
           
           use_config_value(value);
           osDelay(100);
       }
   }
   
   // Single writer
   void writer_task(void *argument) {
       while (1) {
           RWLock_WriteLock(&config_lock);
           
           // Write configuration (exclusive access)
           global_config.value = new_value;
           
           RWLock_WriteUnlock(&config_lock);
           
           osDelay(1000);
       }
   }

Lock-Free Patterns
==================

Single Producer, Single Consumer Queue
---------------------------------------

.. code-block:: c

   // Lock-free SPSC queue (single producer, single consumer)
   typedef struct {
       uint8_t *buffer;
       size_t size;
       volatile size_t head;  // Only producer writes
       volatile size_t tail;  // Only consumer writes
   } SPSCQueue;
   
   void SPSCQueue_Init(SPSCQueue *self, uint8_t *buffer, size_t size) {
       self->buffer = buffer;
       self->size = size;
       self->head = 0;
       self->tail = 0;
   }
   
   bool SPSCQueue_Put(SPSCQueue *self, uint8_t data) {
       size_t next_head = (self->head + 1) % self->size;
       
       if (next_head == self->tail) {
           return false;  // Full
       }
       
       self->buffer[self->head] = data;
       __DMB();  // Memory barrier
       self->head = next_head;
       
       return true;
   }
   
   bool SPSCQueue_Get(SPSCQueue *self, uint8_t *data) {
       if (self->head == self->tail) {
           return false;  // Empty
       }
       
       *data = self->buffer[self->tail];
       __DMB();  // Memory barrier
       self->tail = (self->tail + 1) % self->size;
       
       return true;
   }

Best Practices
==============

1. **Always use RTOS primitives** when available (mutex, semaphore)
2. **Minimize critical section time** - keep guards short
3. **Use lock ordering** to prevent deadlock
4. **Prefer message passing** over shared memory
5. **Use appropriate queue size** based on producer/consumer rates
6. **Consider priority inversion** - use priority inheritance
7. **Test concurrency** thoroughly (stress tests, race conditions)
8. **Document locking strategy** clearly
9. **Profile overhead** of synchronization
10. **Use lock-free structures** when performance critical

Common Pitfalls
===============

1. **Deadlock** - circular wait on locks
2. **Priority inversion** - low priority task blocks high priority
3. **Starvation** - task never gets resource
4. **Race conditions** - unprotected shared access
5. **Forgetting to release** locks/semaphores
6. **Queue overflow** - not handling full queues
7. **Busy waiting** - wasting CPU cycles
8. **Memory barriers** - forgetting on lock-free code

Quick Reference
===============

.. code-block:: c

   // Guarded call
   osMutexAcquire(mutex, osWaitForever);
   critical_operation();
   osMutexRelease(mutex);
   
   // Producer-consumer
   ThreadSafeQueue_Put(&queue, data, osWaitForever);
   ThreadSafeQueue_Get(&queue, &data, osWaitForever);
   
   // Barrier
   Barrier_Wait(&barrier);
   
   // Message queue
   MessageQueue_Send(&queue, &msg, osWaitForever);
   MessageQueue_Receive(&queue, &msg, osWaitForever);
   
   // Read-write lock
   RWLock_ReadLock(&rwlock);
   RWLock_WriteLock(&rwlock);

See Also
========

- Embedded_Design_Patterns_Structural.rst
- Embedded_Design_Patterns_Behavioral.rst
- Embedded_State_Machines.rst
- Linux/Linux_Kernel_Sync.rst

References
==========

- Design Patterns for Embedded Systems in C (Bruce Powel Douglass)
- The Little Book of Semaphores (Allen B. Downey)
- CMSIS-RTOS2 Documentation
- FreeRTOS Documentation
