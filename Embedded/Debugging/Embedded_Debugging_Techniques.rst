=============================================
Embedded Debugging Techniques
=============================================

:Author: Embedded Systems Design Documentation
:Date: January 2026
:Version: 1.0
:Focus: Practical debugging techniques for embedded systems
:Source: Making Embedded Systems (Elecia White) + industry practices

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Debugging Toolbox
-----------------

.. code-block:: text

   Essential Debugging Tools:
   
   1. Printf/UART Debugging
      - Serial output
      - Log levels
      - Minimal overhead
   
   2. JTAG/SWD Debuggers
      - Breakpoints
      - Step execution
      - Variable inspection
   
   3. Logic Analyzer
      - Signal timing
      - Protocol analysis
      - Multi-channel capture
   
   4. Oscilloscope
      - Analog signals
      - Timing measurements
      - Signal integrity
   
   5. Memory Debugging
      - Stack overflow detection
      - Heap corruption
      - Memory leaks
   
   6. Assert Macros
      - Runtime checks
      - Contract programming

Printf Debugging
================

Intent
------

Use serial output for runtime debugging when debugger unavailable or impractical.

Basic Printf Setup
------------------

.. code-block:: c

   // UART printf implementation
   #include <stdarg.h>
   #include <stdio.h>
   
   // Redirect printf to UART
   int _write(int file, char *ptr, int len) {
       for (int i = 0; i < len; i++) {
           while (!(USART1->SR & USART_SR_TXE));
           USART1->DR = ptr[i];
       }
       return len;
   }
   
   // Basic usage
   void debug_example(void) {
       printf("System initialized\n");
       printf("Sensor value: %d\n", sensor_read());
       printf("Error code: 0x%08X\n", error_code);
   }

Log Levels
----------

.. code-block:: c

   // Log level system
   typedef enum {
       LOG_LEVEL_ERROR,
       LOG_LEVEL_WARN,
       LOG_LEVEL_INFO,
       LOG_LEVEL_DEBUG,
       LOG_LEVEL_TRACE
   } LogLevel;
   
   static LogLevel current_log_level = LOG_LEVEL_INFO;
   
   void log_set_level(LogLevel level) {
       current_log_level = level;
   }
   
   // Log macros with file/line info
   #define LOG_ERROR(fmt, ...) \
       do { \
           if (current_log_level >= LOG_LEVEL_ERROR) { \
               printf("[ERROR] %s:%d: " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__); \
           } \
       } while(0)
   
   #define LOG_WARN(fmt, ...) \
       do { \
           if (current_log_level >= LOG_LEVEL_WARN) { \
               printf("[WARN]  %s:%d: " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__); \
           } \
       } while(0)
   
   #define LOG_INFO(fmt, ...) \
       do { \
           if (current_log_level >= LOG_LEVEL_INFO) { \
               printf("[INFO]  " fmt "\n", ##__VA_ARGS__); \
           } \
       } while(0)
   
   #define LOG_DEBUG(fmt, ...) \
       do { \
           if (current_log_level >= LOG_LEVEL_DEBUG) { \
               printf("[DEBUG] %s:%d: " fmt "\n", __func__, __LINE__, ##__VA_ARGS__); \
           } \
       } while(0)
   
   #define LOG_TRACE(fmt, ...) \
       do { \
           if (current_log_level >= LOG_LEVEL_TRACE) { \
               printf("[TRACE] %s(): " fmt "\n", __func__, ##__VA_ARGS__); \
           } \
       } while(0)
   
   // Usage
   void process_data(uint8_t *data, size_t len) {
       LOG_TRACE("Processing %zu bytes", len);
       
       if (data == NULL) {
           LOG_ERROR("Null pointer received!");
           return;
       }
       
       if (len == 0) {
           LOG_WARN("Empty data buffer");
           return;
       }
       
       LOG_DEBUG("First byte: 0x%02X", data[0]);
       LOG_INFO("Data processed successfully");
   }

Circular Log Buffer
-------------------

.. code-block:: c

   // Circular buffer for log history
   #define LOG_BUFFER_SIZE 1024
   
   typedef struct {
       char buffer[LOG_BUFFER_SIZE];
       uint16_t head;
       uint16_t tail;
       bool overflow;
   } CircularLogBuffer;
   
   static CircularLogBuffer log_buffer;
   
   void log_buffer_init(void) {
       log_buffer.head = 0;
       log_buffer.tail = 0;
       log_buffer.overflow = false;
   }
   
   void log_buffer_write(const char *str) {
       while (*str) {
           log_buffer.buffer[log_buffer.tail] = *str++;
           log_buffer.tail = (log_buffer.tail + 1) % LOG_BUFFER_SIZE;
           
           if (log_buffer.tail == log_buffer.head) {
               // Buffer full, advance head
               log_buffer.head = (log_buffer.head + 1) % LOG_BUFFER_SIZE;
               log_buffer.overflow = true;
           }
       }
   }
   
   void log_buffer_dump(void) {
       uint16_t pos = log_buffer.head;
       
       if (log_buffer.overflow) {
           printf("*** LOG BUFFER OVERFLOWED ***\n");
       }
       
       while (pos != log_buffer.tail) {
           putchar(log_buffer.buffer[pos]);
           pos = (pos + 1) % LOG_BUFFER_SIZE;
       }
   }

JTAG/SWD Debugging
==================

Breakpoint Strategies
---------------------

.. code-block:: c

   // Conditional breakpoints (conceptual - set in debugger)
   void process_packet(Packet *pkt) {
       // Break when pkt->id == 0x1234
       if (pkt->id == 0x1234) {
           __asm__("nop");  // Set breakpoint here
       }
       
       // Break on error condition
       if (pkt->checksum != calculate_checksum(pkt)) {
           __asm__("nop");  // Breakpoint for debugging
           handle_error();
       }
   }
   
   // Data watchpoints (set in debugger)
   // Watch for writes to critical variable
   volatile uint32_t critical_register;
   
   // Hardware breakpoint on PC value
   // Set breakpoint at specific function address

GDB Commands for Embedded
--------------------------

.. code-block:: bash

   # Common GDB commands for ARM Cortex-M
   
   # Connect to target
   target extended-remote localhost:3333
   
   # Load program
   load firmware.elf
   monitor reset halt
   
   # Breakpoints
   break main
   break file.c:123
   break function_name
   
   # Watchpoints (data breakpoints)
   watch variable_name
   watch *(uint32_t*)0x20000100  # Watch memory address
   
   # Examine memory
   x/16x 0x20000000    # 16 words hex at address
   x/16b 0x20000000    # 16 bytes
   x/16i $pc           # 16 instructions at PC
   
   # Examine variables
   print variable_name
   print/x variable    # Hex format
   print *ptr          # Dereference pointer
   print array[0]@10   # Print 10 elements
   
   # Registers
   info registers
   print $sp           # Stack pointer
   print $pc           # Program counter
   
   # Backtrace
   backtrace
   backtrace full      # With local variables
   
   # Step execution
   step                # Step into
   next                # Step over
   finish              # Step out
   continue            # Resume
   
   # Memory dump
   dump binary memory dump.bin 0x20000000 0x20010000

OpenOCD Integration
-------------------

.. code-block:: bash

   # OpenOCD configuration for STM32
   openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
   
   # OpenOCD commands
   reset halt
   flash write_image erase firmware.elf
   reset run
   
   # GDB connection
   gdb-multiarch firmware.elf
   (gdb) target extended-remote localhost:3333

Assert Macros
=============

Runtime Assertion Checking
---------------------------

.. code-block:: c

   // Custom assert with more information
   #ifdef DEBUG
   #define ASSERT(condition, msg) \
       do { \
           if (!(condition)) { \
               printf("ASSERT FAILED: %s\n", msg); \
               printf("  File: %s\n", __FILE__); \
               printf("  Line: %d\n", __LINE__); \
               printf("  Function: %s\n", __func__); \
               while(1) {  /* Halt */ \
                   __asm__("bkpt 0"); \
               } \
           } \
       } while(0)
   #else
   #define ASSERT(condition, msg) ((void)0)
   #endif
   
   // Usage
   void buffer_write(uint8_t *buf, size_t offset, uint8_t value) {
       ASSERT(buf != NULL, "Buffer is NULL");
       ASSERT(offset < BUFFER_SIZE, "Offset out of bounds");
       
       buf[offset] = value;
   }

Contract Programming
--------------------

.. code-block:: c

   // Precondition/postcondition checks
   #define REQUIRE(condition) ASSERT(condition, "Precondition failed: " #condition)
   #define ENSURE(condition) ASSERT(condition, "Postcondition failed: " #condition)
   #define INVARIANT(condition) ASSERT(condition, "Invariant failed: " #condition)
   
   void queue_enqueue(Queue *q, uint8_t data) {
       // Preconditions
       REQUIRE(q != NULL);
       REQUIRE(!queue_is_full(q));
       
       size_t old_count = q->count;
       
       // Implementation
       q->buffer[q->tail] = data;
       q->tail = (q->tail + 1) % q->size;
       q->count++;
       
       // Postconditions
       ENSURE(q->count == old_count + 1);
       ENSURE(!queue_is_empty(q));
   }

Logic Analyzer Debugging
=========================

Signal Capture Techniques
--------------------------

.. code-block:: c

   // Debug pins for logic analyzer
   #define DEBUG_PIN_1  GPIO_PIN_0
   #define DEBUG_PIN_2  GPIO_PIN_1
   #define DEBUG_PIN_3  GPIO_PIN_2
   #define DEBUG_PIN_4  GPIO_PIN_3
   
   void debug_pins_init(void) {
       GPIO_InitTypeDef gpio = {0};
       gpio.Mode = GPIO_MODE_OUTPUT_PP;
       gpio.Pull = GPIO_NOPULL;
       gpio.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
       gpio.Pin = DEBUG_PIN_1 | DEBUG_PIN_2 | DEBUG_PIN_3 | DEBUG_PIN_4;
       HAL_GPIO_Init(DEBUG_PORT, &gpio);
   }
   
   // Instrument critical sections
   void spi_transaction(uint8_t *data, size_t len) {
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_1, GPIO_PIN_SET);
       
       // SPI transfer
       HAL_SPI_Transmit(&hspi1, data, len, TIMEOUT);
       
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_1, GPIO_PIN_RESET);
   }
   
   // State machine visualization
   void state_machine_transition(State new_state) {
       // Encode state on debug pins (3 bits = 8 states)
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_1, (new_state & 0x01) ? GPIO_PIN_SET : GPIO_PIN_RESET);
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_2, (new_state & 0x02) ? GPIO_PIN_SET : GPIO_PIN_RESET);
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_3, (new_state & 0x04) ? GPIO_PIN_SET : GPIO_PIN_RESET);
       
       current_state = new_state;
   }
   
   // Timing measurements
   void measure_function_time(void) {
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_4, GPIO_PIN_SET);
       
       critical_function();  // Measure this
       
       HAL_GPIO_WritePin(DEBUG_PORT, DEBUG_PIN_4, GPIO_PIN_RESET);
   }

Memory Debugging
================

Stack Overflow Detection
------------------------

.. code-block:: c

   // Stack canary pattern
   #define STACK_CANARY 0xDEADBEEF
   
   extern uint32_t _sstack;  // Linker symbol
   extern uint32_t _estack;
   
   void stack_init_canary(void) {
       volatile uint32_t *canary = &_sstack;
       *canary = STACK_CANARY;
   }
   
   bool stack_check_overflow(void) {
       volatile uint32_t *canary = &_sstack;
       return (*canary != STACK_CANARY);
   }
   
   // Periodic check
   void system_tick_handler(void) {
       if (stack_check_overflow()) {
           LOG_ERROR("STACK OVERFLOW DETECTED!");
           // Handle error
       }
   }
   
   // Stack usage measurement
   #define STACK_FILL_PATTERN 0xA5A5A5A5
   
   void stack_fill(void) {
       extern uint32_t _sstack;
       extern uint32_t _estack;
       
       for (uint32_t *p = &_sstack; p < &_estack; p++) {
           *p = STACK_FILL_PATTERN;
       }
   }
   
   uint32_t stack_get_usage(void) {
       extern uint32_t _sstack;
       extern uint32_t _estack;
       
       uint32_t *p = &_sstack;
       while (*p == STACK_FILL_PATTERN && p < &_estack) {
           p++;
       }
       
       return (uint32_t)&_estack - (uint32_t)p;
   }

Heap Debugging
--------------

.. code-block:: c

   // Heap allocation wrapper with guards
   #define HEAP_GUARD_PATTERN 0xDEADC0DE
   
   typedef struct {
       uint32_t guard_front;
       size_t size;
       void *caller;
       uint8_t data[];  // Flexible array member
       // guard_back follows data
   } HeapBlock;
   
   void *debug_malloc(size_t size, void *caller) {
       size_t total = sizeof(HeapBlock) + size + sizeof(uint32_t);
       HeapBlock *block = malloc(total);
       
       if (block) {
           block->guard_front = HEAP_GUARD_PATTERN;
           block->size = size;
           block->caller = caller;
           
           uint32_t *guard_back = (uint32_t *)(block->data + size);
           *guard_back = HEAP_GUARD_PATTERN;
           
           LOG_DEBUG("malloc(%zu) = %p by %p", size, block->data, caller);
           return block->data;
       }
       
       LOG_ERROR("malloc(%zu) FAILED", size);
       return NULL;
   }
   
   void debug_free(void *ptr) {
       if (!ptr) return;
       
       HeapBlock *block = (HeapBlock *)((uint8_t *)ptr - offsetof(HeapBlock, data));
       
       // Check guards
       if (block->guard_front != HEAP_GUARD_PATTERN) {
           LOG_ERROR("Heap corruption: front guard damaged at %p", ptr);
       }
       
       uint32_t *guard_back = (uint32_t *)(block->data + block->size);
       if (*guard_back != HEAP_GUARD_PATTERN) {
           LOG_ERROR("Heap corruption: back guard damaged at %p", ptr);
           LOG_ERROR("Possible buffer overflow of %zu bytes", block->size);
       }
       
       LOG_DEBUG("free(%p), size %zu", ptr, block->size);
       
       // Fill with pattern to detect use-after-free
       memset(block->data, 0xDD, block->size);
       
       free(block);
   }
   
   #define malloc(size) debug_malloc(size, __builtin_return_address(0))
   #define free(ptr) debug_free(ptr)

Fault Handlers
==============

HardFault Handler
-----------------

.. code-block:: c

   // Enhanced HardFault handler with diagnostics
   void HardFault_Handler(void) {
       __asm volatile (
           "tst lr, #4                     \n"
           "ite eq                         \n"
           "mrseq r0, msp                  \n"
           "mrsne r0, psp                  \n"
           "b HardFault_Handler_C          \n"
       );
   }
   
   void HardFault_Handler_C(uint32_t *hardfault_args) {
       volatile uint32_t stacked_r0;
       volatile uint32_t stacked_r1;
       volatile uint32_t stacked_r2;
       volatile uint32_t stacked_r3;
       volatile uint32_t stacked_r12;
       volatile uint32_t stacked_lr;
       volatile uint32_t stacked_pc;
       volatile uint32_t stacked_psr;
       
       stacked_r0 = ((uint32_t)hardfault_args[0]);
       stacked_r1 = ((uint32_t)hardfault_args[1]);
       stacked_r2 = ((uint32_t)hardfault_args[2]);
       stacked_r3 = ((uint32_t)hardfault_args[3]);
       stacked_r12 = ((uint32_t)hardfault_args[4]);
       stacked_lr = ((uint32_t)hardfault_args[5]);
       stacked_pc = ((uint32_t)hardfault_args[6]);
       stacked_psr = ((uint32_t)hardfault_args[7]);
       
       printf("\n\n[Hard Fault]\n");
       printf("R0  = 0x%08X\n", stacked_r0);
       printf("R1  = 0x%08X\n", stacked_r1);
       printf("R2  = 0x%08X\n", stacked_r2);
       printf("R3  = 0x%08X\n", stacked_r3);
       printf("R12 = 0x%08X\n", stacked_r12);
       printf("LR  = 0x%08X\n", stacked_lr);
       printf("PC  = 0x%08X\n", stacked_pc);
       printf("PSR = 0x%08X\n", stacked_psr);
       
       // CFSR - Configurable Fault Status Register
       printf("CFSR = 0x%08X\n", SCB->CFSR);
       printf("HFSR = 0x%08X\n", SCB->HFSR);
       printf("DFSR = 0x%08X\n", SCB->DFSR);
       printf("AFSR = 0x%08X\n", SCB->AFSR);
       printf("BFAR = 0x%08X\n", SCB->BFAR);
       printf("MMAR = 0x%08X\n", SCB->MMFAR);
       
       while(1);
   }

Performance Profiling
=====================

Execution Time Measurement
--------------------------

.. code-block:: c

   // Cycle counter for Cortex-M
   #define DWT_CYCCNT *(volatile uint32_t *)0xE0001004
   #define DWT_CONTROL *(volatile uint32_t *)0xE0001000
   #define SCB_DEMCR *(volatile uint32_t *)0xE000EDFC
   
   void profiling_init(void) {
       SCB_DEMCR |= 0x01000000;    // Enable trace
       DWT_CYCCNT = 0;              // Reset counter
       DWT_CONTROL |= 1;            // Enable counter
   }
   
   uint32_t profiling_start(void) {
       return DWT_CYCCNT;
   }
   
   uint32_t profiling_end(uint32_t start) {
       return DWT_CYCCNT - start;
   }
   
   // Usage
   void measure_function(void) {
       uint32_t start = profiling_start();
       
       function_to_measure();
       
       uint32_t cycles = profiling_end(start);
       printf("Execution: %lu cycles (%.2f us)\n", 
              cycles, (float)cycles / SystemCoreClock * 1000000);
   }

Best Practices
==============

1. **Use log levels** - control verbosity
2. **Keep debug code** - conditionally compiled
3. **Assert liberally** - catch bugs early
4. **Instrument with debug pins** - logic analyzer visibility
5. **Check stack usage** - prevent overflows
6. **Guard heap allocations** - detect corruption
7. **Implement fault handlers** - capture crash info
8. **Profile performance** - measure, don't guess
9. **Version debug output** - track firmware versions
10. **Save crash dumps** - analyze post-mortem

Common Debugging Scenarios
===========================

.. code-block:: c

   // Scenario 1: Intermittent crash
   // Solution: Add logging and assertions
   
   // Scenario 2: Timing issues
   // Solution: Logic analyzer + debug pins
   
   // Scenario 3: Memory corruption
   // Solution: Heap guards + stack canary
   
   // Scenario 4: Performance problems
   // Solution: Cycle counting + profiling
   
   // Scenario 5: Hardware not responding
   // Solution: Oscilloscope + register dumps

Quick Reference
===============

.. code-block:: c

   // Logging
   LOG_ERROR("Error: %d", code);
   LOG_DEBUG("Value: 0x%08X", value);
   
   // Assertions
   ASSERT(ptr != NULL, "Null pointer");
   REQUIRE(len > 0);
   
   // Debug pins
   HAL_GPIO_WritePin(DEBUG_PORT, PIN, SET);
   
   // Stack check
   stack_check_overflow();
   
   // Profiling
   uint32_t cycles = profiling_end(profiling_start());

See Also
========

- Embedded_Optimization_Techniques.rst
- Embedded_Testing_Strategies.rst
- Linux/Linux_Debug.rst
- Linux/Linux_KGDB.rst

References
==========

- Making Embedded Systems (Elecia White)
- The Definitive Guide to ARM Cortex-M3/M4 (Joseph Yiu)
- Embedded Software Development with C (Kai Qian)
- GDB Documentation
