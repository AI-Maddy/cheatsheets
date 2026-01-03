# Embedded C Cheat Sheet

Essential quick reference for writing efficient, reliable C code on microcontrollers (e.g., AVR, ARM Cortex-M, PIC, ESP32, STM32).

## 1. Data Types & Sizes (Typical for 8/16/32-bit MCUs)

| Type              | Size (bytes) | Range                              | Use in Embedded |
|-------------------|--------------|------------------------------------|-----------------|
| `bool` (_Bool)    | 1            | 0 or 1                             | Logic flags     |
| `char`            | 1            | -128 to 127 (signed)               | Characters, small data |
| `unsigned char`   | 1            | 0 to 255                           | Bytes, bitfields |
| `int8_t` / `uint8_t`  | 1        | -128..127 / 0..255                 | Preferred exact width |
| `int16_t` / `uint16_t`| 2        | -32768..32767 / 0..65535            | Common for registers |
| `int32_t` / `uint32_t`| 4        | ±2^31 / 0..2^32-1                  | Timers, calculations |
| `int64_t` / `uint64_t`| 8        | Rare on 8/16-bit MCUs              | Only if needed |
| `float`           | 4            | IEEE 754 (avoid if possible)       | Use fixed-point instead |
| `double`          | 4 or 8       | Often same as float on MCUs        | Avoid |

**Include**: `<stdint.h>` for exact-width types (`int8_t`, `uint32_t`, etc.)  
**Include**: `<stdbool.h>` for `bool`, `true`, `false`

## 2. Volatile Keyword (Critical!)

```c
volatile uint8_t flag;          // Prevent optimizer from removing reads/writes
volatile const uint16_t *reg;   // Hardware register
```

Use `volatile` for:
- Variables modified by ISR
- Hardware registers (peripheral SFRs)
- Global variables shared between threads/tasks

## 3. Bit Manipulation

```c
// Set, clear, toggle, test bit
#define SET_BIT(reg, bit)   (reg |= (1U << bit))
#define CLR_BIT(reg, bit)   (reg &= ~(1U << bit))
#define TOG_BIT(reg, bit)   (reg ^= (1U << bit))
#define TST_BIT(reg, bit)   ((reg & (1U << bit)) != 0)

// Example: Port B, pin 5
SET_BIT(PORTB, 5);   // Output high
CLR_BIT(PORTB, 5);   // Output low
if (TST_BIT(PINB, 5)) { /* input high */ }
```

**Atomic operations**: Use bit-band (Cortex-M3/M4) or disable interrupts for multi-bit fields.

## 4. Hardware Registers Access

```c
// Preferred: Use CMSIS or vendor headers
#include "stm32f4xx.h"          // STM32 example

GPIOA->MODER |= (1 << 10);      // Set PA5 as output
GPIOB->IDR;                     // Read input register

// Or define your own
#define PORTB   (*(volatile uint8_t *)0x25)
#define DDRB    (*(volatile uint8_t *)0x24)
```

## 5. Interrupts (ISR)

```c
// AVR/GCC
#include <avr/interrupt.h>
ISR(TIMER1_OVF_vect) {
    // Must be fast!
    flag = 1;
}

// ARM Cortex-M (CMSIS)
void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        TIM2->SR &= ~TIM_SR_UIF;   // Clear flag
        flag = 1;
    }
}

// Disable/enable interrupts (critical sections)
__disable_irq();   // Cortex-M
// critical code
__enable_irq();

// Or local:
uint32_t primask = __get_PRIMASK();
__disable_irq();
// ...
__set_PRIMASK(primask);
```

## 6. Memory Sections & Attributes

```c
// Place variable in specific section
__attribute__((section(".noinit"))) uint32_t boot_flag;  // Survives reset

// Const in flash
const uint8_t lookup_table[256] __attribute__((section(".flash"))) = {...};

// Inline functions
static inline void delay_us(uint16_t us) { ... }

// Force function to stay (prevent optimization removal)
void isr_handler(void) __attribute__((used));
```

## 7. Common Macros & Tricks

```c
#define ARRAY_SIZE(arr)     (sizeof(arr) / sizeof((arr)[0]))
#define MIN(a,b)            (((a)<(b))?(a):(b))
#define MAX(a,b)            (((a)>(b))?(a):(b))
#define CONSTRAIN(val,lo,hi) MIN(MAX(val,lo),hi)
#define BIT(x)              (1U << (x))
#define PACKED              __attribute__((packed))
#define ALIGN(n)            __attribute__((aligned(n)))

// String in flash (AVR)
#define FSTR(str)           ((const __flash char *)(str))  // AVR specific
```

## 8. Fixed-Point Math (Avoid float!)

```c
// Q15.16 format (16-bit integer, 16-bit fraction)
typedef int32_t q31_t;
#define Q16_MULT(a,b)       ((int32_t)(((int64_t)a * b) >> 16))
#define FLOAT_TO_Q16(f)     ((int32_t)((f) * 65536.0f))
```

## 9. Delay & Timing

```c
// Simple busy-wait (calibrate for your clock!)
void delay_ms(uint16_t ms) {
    while (ms--) {
        __delay_cycles(F_CPU / 1000);  // Some toolchains
        // or hand-coded loop
    }
}
```

## 10. Best Practices Summary

- Use `uint8_t`/`uint16_t` etc. from `<stdint.h>`
- Always `volatile` for peripherals and ISR-shared vars
- Avoid `malloc`/`free` — use static or pool allocators
- Prefer `static inline` for small functions
- No recursion unless stack usage proven safe
- Enable compiler warnings: `-Wall -Wextra -Werror`
- Use MISRA C guidelines for safety-critical code
- Check stack/heap usage (Cortex-M: check `_estack`, `__stack`)

**Recommended Headers**:
```c
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
```

This cheat sheet focuses on portable and safe practices across most embedded platforms. Always refer to your MCU vendor's documentation and CMSIS/device header files for specifics.
