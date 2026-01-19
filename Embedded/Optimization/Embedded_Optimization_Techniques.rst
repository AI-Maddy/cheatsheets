=============================================
Embedded Optimization Techniques
=============================================

:Author: Embedded Systems Design Documentation
:Date: January 2026
:Version: 1.0
:Focus: Optimization techniques for embedded systems
:Source: Making Embedded Systems (Elecia White) + industry practices

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Optimization Targets
--------------------

.. code-block:: text

   Optimization Priorities:
   
   1. Code Size
      - Compiler flags (-Os)
      - Function inlining
      - Data structure packing
      - Dead code elimination
   
   2. Execution Speed
      - Algorithm selection
      - Loop optimization
      - Compiler flags (-O2, -O3)
      - Cache optimization
   
   3. Memory Usage
      - Static vs dynamic allocation
      - Memory pools
      - Data structure optimization
   
   4. Power Consumption
      - Sleep modes
      - Clock gating
      - Peripheral management
      - DMA usage
   
   Measure First, Optimize Later!

Code Size Optimization
======================

Compiler Flags
--------------

.. code-block:: makefile

   # GCC optimization flags for size
   CFLAGS += -Os                    # Optimize for size
   CFLAGS += -ffunction-sections   # Each function in separate section
   CFLAGS += -fdata-sections        # Each data item in separate section
   
   LDFLAGS += -Wl,--gc-sections     # Garbage collect unused sections
   LDFLAGS += -Wl,-Map=output.map   # Generate map file
   
   # Link-time optimization
   CFLAGS += -flto
   LDFLAGS += -flto
   
   # Additional size optimizations
   CFLAGS += -fno-unwind-tables     # Remove exception tables
   CFLAGS += -fno-asynchronous-unwind-tables
   CFLAGS += -fno-stack-protector   # Remove stack protection (if safe)

Function Inlining Control
--------------------------

.. code-block:: c

   // Force inline for small, frequently called functions
   static inline __attribute__((always_inline))
   uint16_t swap_bytes(uint16_t value) {
       return (value << 8) | (value >> 8);
   }
   
   // Prevent inlining for large functions
   __attribute__((noinline))
   void large_complex_function(void) {
       // Large function body
   }
   
   // Compiler will decide
   static inline uint8_t checksum(const uint8_t *data, size_t len) {
       uint8_t sum = 0;
       for (size_t i = 0; i < len; i++) {
           sum += data[i];
       }
       return sum;
   }

Data Structure Packing
----------------------

.. code-block:: c

   // Unpacked structure - wastes space
   struct unpacked {
       uint8_t a;    // 1 byte + 3 padding
       uint32_t b;   // 4 bytes
       uint8_t c;    // 1 byte + 3 padding
       uint16_t d;   // 2 bytes + 2 padding
   };  // Total: 16 bytes
   
   // Packed structure - optimal ordering
   struct packed {
       uint32_t b;   // 4 bytes (aligned)
       uint16_t d;   // 2 bytes
       uint8_t a;    // 1 byte
       uint8_t c;    // 1 byte
   };  // Total: 8 bytes
   
   // Explicit packing attribute
   struct __attribute__((packed)) force_packed {
       uint8_t a;
       uint32_t b;
       uint8_t c;
   };  // Total: 6 bytes (no padding)
   
   // Bit fields for flags
   struct flags {
       uint8_t enabled : 1;
       uint8_t ready : 1;
       uint8_t error : 1;
       uint8_t mode : 2;
       uint8_t reserved : 3;
   };  // Total: 1 byte

Common Function Optimization
-----------------------------

.. code-block:: c

   // Use common functions instead of duplicating code
   
   // Before: Duplicated code
   void process_uart1(uint8_t data) {
       if (data == START_BYTE) {
           state1 = RECEIVING;
           index1 = 0;
       } else if (state1 == RECEIVING) {
           buffer1[index1++] = data;
           if (index1 >= MAX_SIZE) {
               process_buffer1();
           }
       }
   }
   
   void process_uart2(uint8_t data) {
       if (data == START_BYTE) {
           state2 = RECEIVING;
           index2 = 0;
       } else if (state2 == RECEIVING) {
           buffer2[index2++] = data;
           if (index2 >= MAX_SIZE) {
               process_buffer2();
           }
       }
   }
   
   // After: Common function
   typedef struct {
       uint8_t *buffer;
       size_t index;
       size_t max_size;
       enum { IDLE, RECEIVING } state;
   } UartContext;
   
   void process_uart_data(UartContext *ctx, uint8_t data) {
       if (data == START_BYTE) {
           ctx->state = RECEIVING;
           ctx->index = 0;
       } else if (ctx->state == RECEIVING) {
           ctx->buffer[ctx->index++] = data;
           if (ctx->index >= ctx->max_size) {
               ctx->state = IDLE;
               // Process complete
           }
       }
   }

Execution Speed Optimization
=============================

Algorithm Selection
-------------------

.. code-block:: c

   // Example: Finding maximum value
   
   // O(n) linear search - acceptable for small arrays
   uint16_t find_max_linear(const uint16_t *array, size_t len) {
       uint16_t max = array[0];
       for (size_t i = 1; i < len; i++) {
           if (array[i] > max) {
               max = array[i];
           }
       }
       return max;
   }
   
   // Maintain sorted array - O(log n) binary search
   size_t binary_search(const uint16_t *sorted_array, size_t len, uint16_t value) {
       size_t left = 0;
       size_t right = len;
       
       while (left < right) {
           size_t mid = left + (right - left) / 2;
           
           if (sorted_array[mid] < value) {
               left = mid + 1;
           } else {
               right = mid;
           }
       }
       
       return left;
   }
   
   // Hash table for O(1) lookup
   #define HASH_SIZE 256
   typedef struct {
       uint16_t key;
       void *value;
       bool valid;
   } HashEntry;
   
   static HashEntry hash_table[HASH_SIZE];
   
   size_t hash_function(uint16_t key) {
       return key % HASH_SIZE;
   }
   
   void *hash_lookup(uint16_t key) {
       size_t idx = hash_function(key);
       size_t start = idx;
       
       do {
           if (hash_table[idx].valid && hash_table[idx].key == key) {
               return hash_table[idx].value;
           }
           idx = (idx + 1) % HASH_SIZE;
       } while (idx != start);
       
       return NULL;
   }

Loop Optimization
-----------------

.. code-block:: c

   // Loop unrolling
   // Before
   void copy_buffer(uint8_t *dest, const uint8_t *src, size_t len) {
       for (size_t i = 0; i < len; i++) {
           dest[i] = src[i];
       }
   }
   
   // After (manual unrolling)
   void copy_buffer_unrolled(uint8_t *dest, const uint8_t *src, size_t len) {
       size_t i = 0;
       
       // Process 4 bytes at a time
       for (; i + 4 <= len; i += 4) {
           dest[i] = src[i];
           dest[i + 1] = src[i + 1];
           dest[i + 2] = src[i + 2];
           dest[i + 3] = src[i + 3];
       }
       
       // Handle remaining bytes
       for (; i < len; i++) {
           dest[i] = src[i];
       }
   }
   
   // Loop hoisting - move invariant code out
   // Before
   void process_array(uint8_t *array, size_t len, Config *cfg) {
       for (size_t i = 0; i < len; i++) {
           uint8_t threshold = cfg->threshold * 2;  // Invariant!
           if (array[i] > threshold) {
               array[i] = threshold;
           }
       }
   }
   
   // After
   void process_array_optimized(uint8_t *array, size_t len, Config *cfg) {
       uint8_t threshold = cfg->threshold * 2;  // Moved outside
       
       for (size_t i = 0; i < len; i++) {
           if (array[i] > threshold) {
               array[i] = threshold;
           }
       }
   }
   
   // Strength reduction - replace expensive operations
   // Before
   for (size_t i = 0; i < 100; i++) {
       array[i] = i * 10;  // Multiplication
   }
   
   // After
   size_t value = 0;
   for (size_t i = 0; i < 100; i++) {
       array[i] = value;
       value += 10;  // Addition instead
   }

Lookup Tables
-------------

.. code-block:: c

   // Sin/Cos lookup tables
   #define TABLE_SIZE 360
   static const int16_t sin_table[TABLE_SIZE] = {
       0, 17, 35, 52, 70, 87, 105, 122, 139, 156, // ...
   };
   
   int16_t fast_sin(uint16_t degrees) {
       return sin_table[degrees % TABLE_SIZE];
   }
   
   int16_t fast_cos(uint16_t degrees) {
       return sin_table[(degrees + 90) % TABLE_SIZE];
   }
   
   // CRC lookup table
   static const uint8_t crc8_table[256] = {
       // Pre-computed CRC values
   };
   
   uint8_t crc8_fast(const uint8_t *data, size_t len) {
       uint8_t crc = 0;
       for (size_t i = 0; i < len; i++) {
           crc = crc8_table[crc ^ data[i]];
       }
       return crc;
   }

Cache Optimization
------------------

.. code-block:: c

   // Cache-friendly data layout
   // Bad: Array of structures (AoS) - poor cache locality
   typedef struct {
       float x, y, z;
       float vx, vy, vz;
       uint32_t id;
   } Particle;
   
   Particle particles[1000];
   
   void update_positions_aos(void) {
       for (int i = 0; i < 1000; i++) {
           particles[i].x += particles[i].vx;
           particles[i].y += particles[i].vy;
           particles[i].z += particles[i].vz;
       }
   }
   
   // Good: Structure of arrays (SoA) - better cache locality
   typedef struct {
       float x[1000];
       float y[1000];
       float z[1000];
       float vx[1000];
       float vy[1000];
       float vz[1000];
       uint32_t id[1000];
   } ParticleSystem;
   
   ParticleSystem particles_soa;
   
   void update_positions_soa(void) {
       for (int i = 0; i < 1000; i++) {
           particles_soa.x[i] += particles_soa.vx[i];
           particles_soa.y[i] += particles_soa.vy[i];
           particles_soa.z[i] += particles_soa.vz[i];
       }
   }

Memory Usage Optimization
==========================

Static vs Dynamic Allocation
-----------------------------

.. code-block:: c

   // Static allocation - preferred in embedded
   #define MAX_MESSAGES 16
   static Message message_pool[MAX_MESSAGES];
   static uint16_t free_bitmap = 0xFFFF;
   
   Message *message_alloc_static(void) {
       for (int i = 0; i < MAX_MESSAGES; i++) {
           if (free_bitmap & (1 << i)) {
               free_bitmap &= ~(1 << i);
               return &message_pool[i];
           }
       }
       return NULL;
   }
   
   void message_free_static(Message *msg) {
       int idx = msg - message_pool;
       if (idx >= 0 && idx < MAX_MESSAGES) {
           free_bitmap |= (1 << idx);
       }
   }
   
   // Dynamic allocation - use sparingly
   Message *message_alloc_dynamic(void) {
       return (Message *)malloc(sizeof(Message));
   }

Memory Pools
------------

.. code-block:: c

   // Fixed-size memory pool
   typedef struct {
       uint8_t pool[BLOCK_SIZE * NUM_BLOCKS];
       uint8_t *free_list;
   } MemoryPool;
   
   void pool_init(MemoryPool *p) {
       p->free_list = p->pool;
       
       for (size_t i = 0; i < NUM_BLOCKS - 1; i++) {
           uint8_t **next = (uint8_t **)(p->pool + i * BLOCK_SIZE);
           *next = p->pool + (i + 1) * BLOCK_SIZE;
       }
       
       uint8_t **last = (uint8_t **)(p->pool + (NUM_BLOCKS - 1) * BLOCK_SIZE);
       *last = NULL;
   }
   
   void *pool_alloc(MemoryPool *p) {
       if (p->free_list == NULL) return NULL;
       
       void *block = p->free_list;
       p->free_list = *(uint8_t **)block;
       return block;
   }
   
   void pool_free(MemoryPool *p, void *block) {
       *(uint8_t **)block = p->free_list;
       p->free_list = block;
   }

Data Compression
----------------

.. code-block:: c

   // Run-length encoding for repetitive data
   size_t rle_compress(const uint8_t *input, size_t in_len,
                       uint8_t *output, size_t out_max) {
       size_t in_pos = 0;
       size_t out_pos = 0;
       
       while (in_pos < in_len && out_pos + 2 <= out_max) {
           uint8_t value = input[in_pos];
           uint8_t count = 1;
           
           while (in_pos + count < in_len &&
                  input[in_pos + count] == value &&
                  count < 255) {
               count++;
           }
           
           output[out_pos++] = count;
           output[out_pos++] = value;
           in_pos += count;
       }
       
       return out_pos;
   }

Power Optimization
==================

Sleep Modes
-----------

.. code-block:: c

   // STM32 sleep modes
   void enter_sleep_mode(void) {
       // Sleep mode - CPU stopped, peripherals running
       __WFI();  // Wait for interrupt
   }
   
   void enter_stop_mode(void) {
       // Stop mode - clocks stopped, RAM retained
       HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
   }
   
   void enter_standby_mode(void) {
       // Standby mode - minimal power, RAM lost
       HAL_PWR_EnterSTANDBYMode();
   }
   
   // Event-driven sleep
   void main_loop_with_sleep(void) {
       while (1) {
           if (event_queue_empty()) {
               // No work to do, sleep until interrupt
               __WFI();
           } else {
               process_events();
           }
       }
   }

Clock Management
----------------

.. code-block:: c

   // Dynamic clock scaling
   void set_clock_speed(ClockSpeed speed) {
       switch (speed) {
       case CLOCK_SPEED_FULL:
           // 168 MHz
           SystemClock_Config_168MHz();
           break;
           
       case CLOCK_SPEED_HALF:
           // 84 MHz - half power
           SystemClock_Config_84MHz();
           break;
           
       case CLOCK_SPEED_LOW:
           // 16 MHz - minimal power
           SystemClock_Config_16MHz();
           break;
       }
       
       // Update SystemCoreClock variable
       SystemCoreClockUpdate();
   }
   
   // Adaptive clocking
   void adaptive_clock_control(void) {
       if (system_busy()) {
           set_clock_speed(CLOCK_SPEED_FULL);
       } else if (periodic_tasks_pending()) {
           set_clock_speed(CLOCK_SPEED_HALF);
       } else {
           set_clock_speed(CLOCK_SPEED_LOW);
       }
   }

Peripheral Power Management
----------------------------

.. code-block:: c

   // Enable peripherals only when needed
   void i2c_transaction(uint8_t addr, const uint8_t *data, size_t len) {
       // Enable I2C clock
       __HAL_RCC_I2C1_CLK_ENABLE();
       
       // Perform transaction
       HAL_I2C_Master_Transmit(&hi2c1, addr, data, len, TIMEOUT);
       
       // Disable I2C clock to save power
       __HAL_RCC_I2C1_CLK_DISABLE();
   }
   
   // DMA for power-efficient data transfer
   void adc_dma_setup(void) {
       // ADC + DMA = CPU can sleep during conversion
       HAL_ADC_Start_DMA(&hadc1, (uint32_t *)adc_buffer, ADC_BUFFER_SIZE);
       
       // Enter sleep, DMA will wake CPU when done
       __WFI();
   }

Profiling and Measurement
==========================

Cycle Counting
--------------

.. code-block:: c

   // ARM Cortex-M cycle counter
   static inline void cycle_counter_enable(void) {
       CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
       DWT->CYCCNT = 0;
       DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
   }
   
   static inline uint32_t get_cycles(void) {
       return DWT->CYCCNT;
   }
   
   void profile_function(void) {
       uint32_t start = get_cycles();
       
       function_to_measure();
       
       uint32_t cycles = get_cycles() - start;
       float us = (float)cycles / (SystemCoreClock / 1000000);
       
       printf("Execution: %lu cycles (%.2f us)\n", cycles, us);
   }

Code Size Analysis
------------------

.. code-block:: bash

   # Generate map file
   arm-none-eabi-gcc -Wl,-Map=output.map ...
   
   # Analyze code size
   arm-none-eabi-size firmware.elf
   
   # Detailed section sizes
   arm-none-eabi-objdump -h firmware.elf
   
   # Find largest functions
   arm-none-eabi-nm --size-sort firmware.elf | tail -20
   
   # Bloat analysis
   bloaty firmware.elf

Best Practices
==============

1. **Measure first** - profile before optimizing
2. **Optimize hot paths** - focus on frequently executed code
3. **Use appropriate flags** - -Os for size, -O2/-O3 for speed
4. **Pack structures** - order fields by size
5. **Lookup tables** - trade memory for speed
6. **Memory pools** - avoid fragmentation
7. **Sleep when idle** - save power
8. **DMA for bulk transfers** - free CPU
9. **Cache-friendly data** - structure of arrays
10. **Profile iteratively** - measure improvements

Common Pitfalls
===============

1. **Premature optimization** - optimize after profiling
2. **Over-optimization** - diminishing returns
3. **Breaking functionality** - test after optimizing
4. **Ignoring power** - battery life matters
5. **Cache assumptions** - verify cache behavior
6. **Compiler defeats** - volatile for hardware registers

Quick Reference
===============

.. code-block:: c

   // Compiler optimization
   -Os -flto -ffunction-sections -fdata-sections
   
   // Inlining
   __attribute__((always_inline))
   __attribute__((noinline))
   
   // Packing
   __attribute__((packed))
   
   // Power
   __WFI();  // Sleep until interrupt
   
   // Profiling
   uint32_t cycles = get_cycles();

See Also
========

- Embedded_Debugging_Techniques.rst
- Embedded_Memory_Management_Patterns.rst
- Embedded_C.rst

References
==========

- Making Embedded Systems (Elecia White)
- ARM Cortex-M Programming Guide
- GCC Optimization Options
- Embedded C Coding Standard
