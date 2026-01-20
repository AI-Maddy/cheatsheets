=============================================
Embedded Memory Management Patterns
=============================================

:Author: Embedded Systems Design Patterns Documentation
:Date: January 2026
:Version: 1.0
:Focus: Memory management patterns for embedded systems

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Memory Management Strategies
-----------------------------

.. code-block:: text

   Embedded Memory Patterns:
   
   1. Static Allocation
      - Compile-time allocation
      - Predictable, safe
   
   2. Memory Pool
      - Fixed-size blocks
      - O(1) allocation/free
   
   3. Object Pool
      - Pre-allocated objects
      - Object reuse
   
   4. Stack-Based Allocation
      - LIFO allocation
      - Automatic cleanup
   
   5. Small Object Allocator
      - Optimized for small sizes
      - Reduced fragmentation
   
   6. Placement New (C-style)
      - Allocate at specific address
      - Manual construction

Static Allocation Pattern
==========================

Intent
------

Avoid dynamic allocation by using compile-time memory allocation.

Fixed-Size Buffers
------------------

.. code-block:: c

   // Static buffer allocation
   #define UART_BUFFER_SIZE 256
   #define NUM_BUFFERS 4
   
   typedef struct {
       uint8_t data[UART_BUFFER_SIZE];
       size_t length;
       bool in_use;
   } StaticBuffer;
   
   static StaticBuffer uart_buffers[NUM_BUFFERS];
   
   StaticBuffer *StaticBuffer_Acquire(void) {
       for (size_t i = 0; i < NUM_BUFFERS; i++) {
           if (!uart_buffers[i].in_use) {
               uart_buffers[i].in_use = true;
               uart_buffers[i].length = 0;
               return &uart_buffers[i];
           }
       }
       return NULL;  // All buffers in use
   }
   
   void StaticBuffer_Release(StaticBuffer *buffer) {
       if (buffer >= uart_buffers && buffer < uart_buffers + NUM_BUFFERS) {
           buffer->in_use = false;
           buffer->length = 0;
       }
   }

Pre-allocated Objects
---------------------

.. code-block:: c

   // Message structure
   typedef struct {
       uint8_t type;
       uint8_t data[32];
       size_t length;
   } Message;
   
   #define MAX_MESSAGES 16
   static Message message_pool[MAX_MESSAGES];
   static uint32_t message_bitmap = 0;  // Tracks allocation
   
   Message *Message_Alloc(void) {
       for (size_t i = 0; i < MAX_MESSAGES; i++) {
           if (!(message_bitmap & (1 << i))) {
               message_bitmap |= (1 << i);
               return &message_pool[i];
           }
       }
       return NULL;
   }
   
   void Message_Free(Message *msg) {
       size_t index = msg - message_pool;
       if (index < MAX_MESSAGES) {
           message_bitmap &= ~(1 << index);
       }
   }

Memory Pool Pattern
===================

Intent
------

Allocate fixed-size memory blocks from a pre-allocated pool for O(1) allocation/deallocation.

Fixed Block Pool
----------------

.. code-block:: c

   // Memory pool for fixed-size blocks
   typedef struct {
       uint8_t *pool;              // Pool memory
       uint8_t *free_list;         // Free list head
       size_t block_size;          // Size of each block
       size_t num_blocks;          // Number of blocks
       size_t allocated_count;     // Current allocations
   } MemoryPool;
   
   void MemoryPool_Init(MemoryPool *self, void *memory, 
                        size_t block_size, size_t num_blocks) {
       self->pool = (uint8_t *)memory;
       self->block_size = block_size;
       self->num_blocks = num_blocks;
       self->allocated_count = 0;
       
       // Build free list (linked list through blocks)
       self->free_list = self->pool;
       uint8_t *block = self->pool;
       
       for (size_t i = 0; i < num_blocks - 1; i++) {
           uint8_t **next = (uint8_t **)block;
           *next = block + block_size;
           block += block_size;
       }
       
       // Last block points to NULL
       uint8_t **last = (uint8_t **)block;
       *last = NULL;
   }
   
   void *MemoryPool_Alloc(MemoryPool *self) {
       if (self->free_list == NULL) {
           return NULL;  // Pool exhausted
       }
       
       // Take block from free list
       void *block = self->free_list;
       uint8_t **next = (uint8_t **)block;
       self->free_list = *next;
       
       self->allocated_count++;
       
       return block;
   }
   
   void MemoryPool_Free(MemoryPool *self, void *block) {
       if (block == NULL) return;
       
       // Add block to free list
       uint8_t **next = (uint8_t **)block;
       *next = self->free_list;
       self->free_list = block;
       
       self->allocated_count--;
   }
   
   bool MemoryPool_IsEmpty(MemoryPool *self) {
       return self->free_list == NULL;
   }
   
   size_t MemoryPool_GetAllocatedCount(MemoryPool *self) {
       return self->allocated_count;
   }

Usage Example
--------------

.. code-block:: c

   // Define pool
   #define BLOCK_SIZE 64
   #define NUM_BLOCKS 32
   
   static uint8_t pool_memory[BLOCK_SIZE * NUM_BLOCKS];
   static MemoryPool packet_pool;
   
   void init_pools(void) {
       MemoryPool_Init(&packet_pool, pool_memory, BLOCK_SIZE, NUM_BLOCKS);
   }
   
   void process_packet(void) {
       void *packet = MemoryPool_Alloc(&packet_pool);
       
       if (packet) {
           // Use packet
           memset(packet, 0, BLOCK_SIZE);
           process_data(packet);
           
           // Free when done
           MemoryPool_Free(&packet_pool, packet);
       } else {
           // Handle pool exhaustion
           log_error("Packet pool exhausted");
       }
   }

Multiple Pool Sizes
-------------------

.. code-block:: c

   // Memory pools for different sizes
   typedef struct {
       MemoryPool small;   // 32 bytes
       MemoryPool medium;  // 128 bytes
       MemoryPool large;   // 512 bytes
   } TieredMemoryPools;
   
   static uint8_t small_memory[32 * 64];
   static uint8_t medium_memory[128 * 32];
   static uint8_t large_memory[512 * 8];
   
   static TieredMemoryPools pools;
   
   void TieredPools_Init(void) {
       MemoryPool_Init(&pools.small, small_memory, 32, 64);
       MemoryPool_Init(&pools.medium, medium_memory, 128, 32);
       MemoryPool_Init(&pools.large, large_memory, 512, 8);
   }
   
   void *TieredPools_Alloc(size_t size) {
       if (size <= 32) {
           return MemoryPool_Alloc(&pools.small);
       } else if (size <= 128) {
           return MemoryPool_Alloc(&pools.medium);
       } else if (size <= 512) {
           return MemoryPool_Alloc(&pools.large);
       }
       return NULL;  // Too large
   }

Object Pool Pattern
===================

Intent
------

Pre-allocate and reuse objects to avoid construction/destruction overhead.

Typed Object Pool
-----------------

.. code-block:: c

   // Object pool for specific type
   typedef struct {
       uint32_t id;
       float value;
       bool active;
   } SensorReading;
   
   typedef struct {
       SensorReading objects[MAX_READINGS];
       uint32_t free_bitmap;
       size_t capacity;
   } SensorReadingPool;
   
   void SensorReadingPool_Init(SensorReadingPool *self, size_t capacity) {
       self->capacity = (capacity > MAX_READINGS) ? MAX_READINGS : capacity;
       self->free_bitmap = (1ULL << self->capacity) - 1;  // All free
       
       // Initialize objects
       for (size_t i = 0; i < self->capacity; i++) {
           self->objects[i].active = false;
       }
   }
   
   SensorReading *SensorReadingPool_Acquire(SensorReadingPool *self) {
       if (self->free_bitmap == 0) {
           return NULL;  // All in use
       }
       
       // Find first free
       size_t index = __builtin_ctz(self->free_bitmap);  // Count trailing zeros
       self->free_bitmap &= ~(1ULL << index);
       
       SensorReading *obj = &self->objects[index];
       obj->active = true;
       obj->id = index;
       obj->value = 0.0f;
       
       return obj;
   }
   
   void SensorReadingPool_Release(SensorReadingPool *self, SensorReading *obj) {
       size_t index = obj - self->objects;
       
       if (index < self->capacity) {
           obj->active = false;
           self->free_bitmap |= (1ULL << index);
       }
   }

Generic Object Pool
-------------------

.. code-block:: c

   // Generic object pool with callbacks
   typedef void (*ObjectInit_fn)(void *obj);
   typedef void (*ObjectReset_fn)(void *obj);
   
   typedef struct {
       void *pool;
       size_t object_size;
       size_t capacity;
       uint8_t *free_list;
       ObjectInit_fn init_fn;
       ObjectReset_fn reset_fn;
   } GenericObjectPool;
   
   void GenericObjectPool_Init(GenericObjectPool *self, void *memory,
                                size_t object_size, size_t capacity,
                                ObjectInit_fn init_fn, ObjectReset_fn reset_fn) {
       self->pool = memory;
       self->object_size = object_size;
       self->capacity = capacity;
       self->init_fn = init_fn;
       self->reset_fn = reset_fn;
       
       // Build free list
       self->free_list = (uint8_t *)memory;
       uint8_t *obj = self->free_list;
       
       for (size_t i = 0; i < capacity; i++) {
           if (init_fn) {
               init_fn(obj);
           }
           
           if (i < capacity - 1) {
               uint8_t **next = (uint8_t **)obj;
               *next = obj + object_size;
               obj += object_size;
           } else {
               uint8_t **next = (uint8_t **)obj;
               *next = NULL;
           }
       }
   }
   
   void *GenericObjectPool_Acquire(GenericObjectPool *self) {
       if (self->free_list == NULL) {
           return NULL;
       }
       
       void *obj = self->free_list;
       uint8_t **next = (uint8_t **)obj;
       self->free_list = *next;
       
       if (self->reset_fn) {
           self->reset_fn(obj);
       }
       
       return obj;
   }
   
   void GenericObjectPool_Release(GenericObjectPool *self, void *obj) {
       uint8_t **next = (uint8_t **)obj;
       *next = self->free_list;
       self->free_list = obj;
   }

Stack-Based Allocator
======================

Intent
------

Allocate memory in LIFO order for automatic deallocation.

Linear Allocator
----------------

.. code-block:: c

   // Stack/linear allocator
   typedef struct {
       uint8_t *buffer;
       size_t size;
       size_t offset;
   } StackAllocator;
   
   void StackAllocator_Init(StackAllocator *self, void *buffer, size_t size) {
       self->buffer = buffer;
       self->size = size;
       self->offset = 0;
   }
   
   void *StackAllocator_Alloc(StackAllocator *self, size_t size) {
       // Align to 4-byte boundary
       size_t aligned_size = (size + 3) & ~3;
       
       if (self->offset + aligned_size > self->size) {
           return NULL;  // Out of memory
       }
       
       void *ptr = self->buffer + self->offset;
       self->offset += aligned_size;
       
       return ptr;
   }
   
   void StackAllocator_Reset(StackAllocator *self) {
       self->offset = 0;
   }
   
   // Scoped allocation
   typedef struct {
       StackAllocator *allocator;
       size_t saved_offset;
   } AllocatorScope;
   
   void AllocatorScope_Begin(AllocatorScope *self, StackAllocator *allocator) {
       self->allocator = allocator;
       self->saved_offset = allocator->offset;
   }
   
   void AllocatorScope_End(AllocatorScope *self) {
       self->allocator->offset = self->saved_offset;
   }

Usage
-----

.. code-block:: c

   static uint8_t temp_memory[4096];
   static StackAllocator temp_allocator;
   
   void process_frame(void) {
       StackAllocator_Init(&temp_allocator, temp_memory, sizeof(temp_memory));
       
       // Allocate temporary buffers
       uint8_t *buffer1 = StackAllocator_Alloc(&temp_allocator, 1024);
       uint8_t *buffer2 = StackAllocator_Alloc(&temp_allocator, 512);
       
       // Use buffers
       process_data(buffer1, 1024);
       process_data(buffer2, 512);
       
       // Reset for next frame (automatic cleanup)
       StackAllocator_Reset(&temp_allocator);
   }
   
   // Scoped usage
   void scoped_allocation(void) {
       AllocatorScope scope;
       AllocatorScope_Begin(&scope, &temp_allocator);
       
       // Allocations
       void *data = StackAllocator_Alloc(&temp_allocator, 256);
       process(data);
       
       // Automatic cleanup when scope ends
       AllocatorScope_End(&scope);
   }

Small Object Allocator
======================

Intent
------

Optimize allocation for many small objects to reduce fragmentation.

Segregated Free Lists
---------------------

.. code-block:: c

   #define NUM_SIZE_CLASSES 8
   #define MIN_ALLOC_SIZE 8
   
   typedef struct {
       MemoryPool pools[NUM_SIZE_CLASSES];
       uint8_t *memory[NUM_SIZE_CLASSES];
   } SmallObjectAllocator;
   
   // Size classes: 8, 16, 32, 64, 128, 256, 512, 1024
   static const size_t size_classes[] = {8, 16, 32, 64, 128, 256, 512, 1024};
   static const size_t blocks_per_class[] = {128, 64, 32, 16, 8, 4, 2, 1};
   
   void SmallObjectAllocator_Init(SmallObjectAllocator *self) {
       for (size_t i = 0; i < NUM_SIZE_CLASSES; i++) {
           size_t total_size = size_classes[i] * blocks_per_class[i];
           self->memory[i] = malloc(total_size);
           
           MemoryPool_Init(&self->pools[i], self->memory[i],
                          size_classes[i], blocks_per_class[i]);
       }
   }
   
   void *SmallObjectAllocator_Alloc(SmallObjectAllocator *self, size_t size) {
       // Find appropriate size class
       for (size_t i = 0; i < NUM_SIZE_CLASSES; i++) {
           if (size <= size_classes[i]) {
               return MemoryPool_Alloc(&self->pools[i]);
           }
       }
       
       return NULL;  // Too large
   }
   
   void SmallObjectAllocator_Free(SmallObjectAllocator *self, void *ptr, size_t size) {
       // Find size class
       for (size_t i = 0; i < NUM_SIZE_CLASSES; i++) {
           if (size <= size_classes[i]) {
               MemoryPool_Free(&self->pools[i], ptr);
               return;
           }
       }
   }

Placement New Pattern
=====================

Intent
------

Construct objects at specific memory locations.

C-Style Placement
-----------------

.. code-block:: c

   // Manual object construction at specific address
   typedef struct {
       uint32_t id;
       float value;
       bool initialized;
   } Sensor;
   
   void Sensor_Construct(Sensor *self, uint32_t id) {
       self->id = id;
       self->value = 0.0f;
       self->initialized = true;
   }
   
   void Sensor_Destruct(Sensor *self) {
       self->initialized = false;
   }
   
   // Placement in static memory
   static uint8_t sensor_memory[sizeof(Sensor)] __attribute__((aligned(4)));
   
   Sensor *create_sensor_at(void *memory, uint32_t id) {
       Sensor *sensor = (Sensor *)memory;
       Sensor_Construct(sensor, id);
       return sensor;
   }
   
   void destroy_sensor_at(Sensor *sensor) {
       Sensor_Destruct(sensor);
   }
   
   // Usage
   void example(void) {
       Sensor *sensor = create_sensor_at(sensor_memory, 123);
       
       // Use sensor
       sensor->value = read_sensor();
       
       // Destroy (memory remains)
       destroy_sensor_at(sensor);
   }

Memory Management Utilities
============================

Alignment Helpers
-----------------

.. code-block:: c

   // Alignment macros
   #define ALIGN_UP(value, alignment) \
       (((value) + (alignment) - 1) & ~((alignment) - 1))
   
   #define ALIGN_DOWN(value, alignment) \
       ((value) & ~((alignment) - 1))
   
   #define IS_ALIGNED(value, alignment) \
       (((value) & ((alignment) - 1)) == 0)
   
   #define ALIGN_PTR(ptr, alignment) \
       ((void *)ALIGN_UP((uintptr_t)(ptr), (alignment)))
   
   // Usage
   size_t aligned_size = ALIGN_UP(size, 4);
   void *aligned_ptr = ALIGN_PTR(ptr, 8);

Memory Statistics
-----------------

.. code-block:: c

   typedef struct {
       size_t total_size;
       size_t allocated;
       size_t peak_allocated;
       size_t num_allocations;
       size_t num_frees;
       size_t failed_allocations;
   } MemoryStats;
   
   void MemoryStats_Init(MemoryStats *self, size_t total_size) {
       self->total_size = total_size;
       self->allocated = 0;
       self->peak_allocated = 0;
       self->num_allocations = 0;
       self->num_frees = 0;
       self->failed_allocations = 0;
   }
   
   void MemoryStats_OnAlloc(MemoryStats *self, size_t size, bool success) {
       if (success) {
           self->allocated += size;
           self->num_allocations++;
           
           if (self->allocated > self->peak_allocated) {
               self->peak_allocated = self->allocated;
           }
       } else {
           self->failed_allocations++;
       }
   }
   
   void MemoryStats_OnFree(MemoryStats *self, size_t size) {
       self->allocated -= size;
       self->num_frees++;
   }
   
   float MemoryStats_GetUtilization(MemoryStats *self) {
       return (float)self->allocated / self->total_size;
   }

Best Practices
==============

1. **Prefer static allocation** when size is known
2. **Use memory pools** for fixed-size objects
3. **Avoid malloc/free** in embedded systems
4. **Track memory usage** with statistics
5. **Align allocations** properly
6. **Check for NULL** after allocation
7. **Reset pools** between frames/cycles
8. **Profile memory usage** during development
9. **Set memory budgets** per subsystem
10. **Use scoped allocators** for temporary data

Common Pitfalls
===============

1. **Fragmentation** - use pools to avoid
2. **Leaks** - always free/release
3. **Alignment issues** - use alignment helpers
4. **Pool exhaustion** - size pools appropriately
5. **Dangling pointers** - NULL after free
6. **Buffer overruns** - check bounds

Quick Reference
===============

.. code-block:: c

   // Memory pool
   MemoryPool pool;
   MemoryPool_Init(&pool, memory, block_size, num_blocks);
   void *block = MemoryPool_Alloc(&pool);
   MemoryPool_Free(&pool, block);
   
   // Object pool
   SensorReadingPool pool;
   SensorReading *obj = SensorReadingPool_Acquire(&pool);
   SensorReadingPool_Release(&pool, obj);
   
   // Stack allocator
   StackAllocator alloc;
   void *mem = StackAllocator_Alloc(&alloc, size);
   StackAllocator_Reset(&alloc);

See Also
========

- Linux/Linux_Memory_Management.rst
- Linux/Linux_Memory_Management_Internals.rst
- Embedded_Core/ARM_SOC.rst (Memory architecture)
- Languages/Embedded_C.rst

References
==========

- Design Patterns for Embedded Systems in C (Bruce Powel Douglass)
- Game Programming Patterns (Robert Nystrom) - Memory patterns
- Embedded C Coding Standard
