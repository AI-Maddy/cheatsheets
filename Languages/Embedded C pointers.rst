
================================================================================
Embedded C Pointers Cheat Sheet
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



⭐ Essential guide to using pointers effectively and safely in resource-constrained embedded systems (microcontrollers like AVR, ARM Cortex-M, STM32, PIC, etc.).

📖 **1. Pointer Basics**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

int x = 42;
int *p = &x;            // p points to x
int y = *p;             // y = 42 (dereference)

void *generic_ptr;      // Can point to anything (use sparingly)

| Syntax              | Meaning                          |
|---------------------|----------------------------------|
| ``type *var;``        | Declare pointer to type          |
| ``&var``              | Address of var                   |
| ``*ptr``              | Value pointed to (dereference)   |
| ``ptr++``             | Move to next element (size-aware)|
| ``ptr + n``           | Pointer arithmetic: n × sizeof(type) bytes |

📌 **2. Common Pointer Types in Embedded**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

uint8_t  *data_ptr;          // Byte access (common for buffers)
uint16_t *reg16;             // 16-bit hardware register
uint32_t *reg32;             // 32-bit register

volatile uint8_t  *port;     // MUST be volatile for hardware regs
const    uint8_t  *flash_data; // Data in flash (e.g., lookup tables)

⭐ **Key rule**: Always use ``volatile`` for pointers to hardware registers or shared ISR variables.

⭐ 🛡️ **3. Pointers to Hardware Registers (Critical!)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

// 🟢 🟢 Best: Use vendor-provided headers (CMSIS, stm32xx.h, etc.)
#define GPIOA_BASE  0x40020000U
#define GPIOA       ((GPIO_TypeDef *) GPIOA_BASE)

GPIOA->MODER = 0x00000001;   // Proper typed access

// Manual definition (common on AVR)
#define PORTB   (*(volatile uint8_t *)0x25)
#define DDRB    (*(volatile uint8_t *)0x24)
#define PINB    (*(volatile uint8_t *)0x23)

PORTB = 0xFF;                // Write to port
uint8_t inputs = PINB;       // Read inputs

📌 **4. Pointer Arithmetic**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

uint8_t buffer[10];
uint8_t *ptr = buffer;

ptr[0] = 1;          // Same as buffer[0]
*(ptr + 3) = 5;      // buffer[3]
ptr += 2;            // Now points to buffer[2]

// Array/pointer equivalence
for (uint8_t i = 0; i < 10; i++) {
    *ptr++ = i;      // Fill buffer sequentially
}

**🟡 🟡 Caution**: Pointer arithmetic is in units of the pointed type size.

⚙️ **5. Const and Volatile Combinations**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Declaration                          | Meaning                                      |
|--------------------------------------|----------------------------------------------|
| ``volatile uint8_t *port``             | Can read/write hardware, value may change externally |
| ``uint8_t volatile *port``             | Same as above                                |
| ``const volatile uint8_t *status_reg`` | Read-only hardware register (e.g., status flags) |
| ``uint8_t * const fixed_ptr``          | Pointer itself is constant (can't change address) |
| ``const uint8_t *rom_data``            | Points to read-only data (flash/const section) |

📚 **6. Function Pointers (Very Useful in Embedded)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

// Declare
void (*callback)(uint8_t);
typedef void (*handler_t)(void);

// Array of functions (state machine, command table)
void cmd_help(void);
void cmd_status(void);
void cmd_reset(void);

handler_t commands[] = { cmd_help, cmd_status, cmd_reset };

// Call
commands[1]();  // Calls cmd_status()

// ISR vector table style
void default_handler(void) __attribute__((weak));
void TIM2_IRQHandler(void) __attribute__((alias("default_handler")));

📌 **7. Pointers in Structures (Packed!)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

typedef struct {
    uint8_t  len;
    uint8_t  cmd;
    uint16_t data;
⭐ } __attribute__((packed)) packet_t;  // Critical: no padding!

packet_t *pkt = (packet_t *)rx_buffer;
if (pkt->cmd == 0x01) { ... }

Use ``__attribute__((packed))`` when mapping structures over hardware registers or communication packets.

💡 **8. Common Pitfalls & 🟢 🟢 Best Practices**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Issue                        | Fix / Rule                                                                 |
|------------------------------|----------------------------------------------------------------------------|
| Dangling pointer             | Never use pointer after memory is freed or goes out of scope                |
| Null pointer dereference     | Always initialize: ``uint8_t *p = NULL;`` Check before use: ``if (p) *p = ...`` |
| Wild pointers                | Always initialize pointers!                                                |
| Overrunning arrays           | Use ``sizeof`` carefully; prefer index checks                                |
| Casting without volatile     | 🔴 🔴 Don't cast away volatile: 🔴 🔴 bad → ``*(uint8_t *)0x40000000``                   |
| Pointer size mismatch        | On 32-bit MCU, pointers are 32-bit — 🔴 🔴 avoid ``uint16_t`` for addresses        |

.. code-block:: c

// Safe null check
if (ptr != NULL) {
    *ptr = value;
}

// Or macro
#define IS_VALID_PTR(p) ((p) != NULL)

💾 **9. Memory Section Pointers**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

// Pointer to data in flash (AVR)
const uint8_t table[] __flash = {1,2,3,4};
const uint8_t *p = table;

// Cortex-M: const goes to flash automatically
const uint16_t sine_table[256] = {...};
const uint16_t *sine_ptr = sine_table;

📚 **10. Quick Reference Macros**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

#define REG8(addr)   (*(volatile uint8_t *)(addr))
#define REG16(addr)  (*(volatile uint16_t *)(addr))
#define REG32(addr)  (*(volatile uint32_t *)(addr))

#define PTR_OFFSET(base, offset) ((void *)((uint8_t *)(base) + (offset)))

**Golden Rules for Embedded Pointers**:
- Always use ``volatile`` for hardware and ISR-shared data
- Initialize all pointers (prefer ``NULL``)
- Use exact-width types (``uint8_t*``, ``uint32_t*``)
- Prefer array indexing over raw pointer arithmetic when possible
- Use ``const`` and ``packed`` appropriately
- 🔴 🔴 Avoid ``void*`` unless necessary (loses type safety)

Master these, and your embedded C code will be safer, faster, and more maintainable!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
