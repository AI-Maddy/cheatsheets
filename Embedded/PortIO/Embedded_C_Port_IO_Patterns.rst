================================================================================
Port I/O Patterns for Embedded C
================================================================================

**TL;DR**: Memory-mapped I/O, register access, and port manipulation patterns 
for embedded systems. Covers bit manipulation, hardware abstraction, and 
safe register operations based on embedded C best practices.

**Related Cheatsheets**: 
:doc:`Embedded C </Languages/Embedded C>`, 
:doc:`Embedded System Architecture </Embedded/Embedded_System_Architecture_Patterns>`,
:doc:`Linux Device Tree </Linux/Linux device tree>`,
:doc:`Embedded Design Patterns </Embedded/Embedded_Design_Patterns_Structural>`

================================================================================
1. Memory-Mapped I/O Fundamentals
================================================================================

1.1 Register Access Basics
--------------------------------------------------------------------------------

**Register Pointer Definition**:

.. code-block:: c

    #include <stdint.h>
    
    /* Basic register access using volatile pointer */
    #define REG8(addr)   (*(volatile uint8_t  *)(addr))
    #define REG16(addr)  (*(volatile uint16_t *)(addr))
    #define REG32(addr)  (*(volatile uint32_t *)(addr))
    
    /* Example: GPIO port at base address 0x40020000 */
    #define GPIOA_BASE   0x40020000
    #define GPIOA_MODER  REG32(GPIOA_BASE + 0x00)  /* Mode register */
    #define GPIOA_ODR    REG32(GPIOA_BASE + 0x14)  /* Output data register */
    #define GPIOA_IDR    REG32(GPIOA_BASE + 0x10)  /* Input data register */
    
    /* Usage */
    void set_pin_output(void) {
        GPIOA_MODER |= (1 << 10);  /* Set PA5 as output */
    }

**Why Volatile is Critical**:

.. code-block:: c

    /* WRONG - compiler may optimize away repeated reads */
    uint32_t *gpio_idr = (uint32_t *)0x40020010;
    
    while (*gpio_idr & (1 << 5)) {
        /* Compiler might read once and loop forever! */
    }
    
    /* CORRECT - volatile prevents optimization */
    volatile uint32_t *gpio_idr = (volatile uint32_t *)0x40020010;
    
    while (*gpio_idr & (1 << 5)) {
        /* Each access actually reads from hardware */
    }

1.2 Register Structures
--------------------------------------------------------------------------------

**Struct-Based Register Mapping**:

.. code-block:: c

    /**
     * GPIO register structure (STM32-style)
     */
    typedef struct {
        volatile uint32_t MODER;    /* Mode register            offset 0x00 */
        volatile uint32_t OTYPER;   /* Output type register     offset 0x04 */
        volatile uint32_t OSPEEDR;  /* Output speed register    offset 0x08 */
        volatile uint32_t PUPDR;    /* Pull-up/pull-down reg    offset 0x0C */
        volatile uint32_t IDR;      /* Input data register      offset 0x10 */
        volatile uint32_t ODR;      /* Output data register     offset 0x14 */
        volatile uint32_t BSRR;     /* Bit set/reset register   offset 0x18 */
        volatile uint32_t LCKR;     /* Lock register            offset 0x1C */
        volatile uint32_t AFR[2];   /* Alternate function regs  offset 0x20 */
    } GPIO_TypeDef;
    
    /* Define base pointers */
    #define GPIOA  ((GPIO_TypeDef *)0x40020000)
    #define GPIOB  ((GPIO_TypeDef *)0x40020400)
    #define GPIOC  ((GPIO_TypeDef *)0x40020800)
    
    /* Usage - more readable */
    void configure_pin(void) {
        GPIOA->MODER |= (1 << 10);   /* Set PA5 as output */
        GPIOA->ODR   |= (1 << 5);    /* Set PA5 high */
    }

**Union for Bit-Level Access**:

.. code-block:: c

    /**
     * Register with both word and bit access
     */
    typedef union {
        volatile uint32_t word;
        struct {
            volatile uint32_t bit0  : 1;
            volatile uint32_t bit1  : 1;
            volatile uint32_t bit2  : 1;
            volatile uint32_t bit3  : 1;
            volatile uint32_t bit4  : 1;
            volatile uint32_t bit5  : 1;
            volatile uint32_t bit6  : 1;
            volatile uint32_t bit7  : 1;
            volatile uint32_t reserved : 24;
        } bits;
    } GPIO_ODR_TypeDef;
    
    /* Usage */
    GPIO_ODR_TypeDef *odr = (GPIO_ODR_TypeDef *)&GPIOA->ODR;
    odr->bits.bit5 = 1;  /* Set bit 5 */

================================================================================
2. Bit Manipulation Patterns
================================================================================

2.1 Standard Bit Operations
--------------------------------------------------------------------------------

**Essential Macros**:

.. code-block:: c

    /* Set a bit */
    #define BIT_SET(reg, bit)      ((reg) |= (1U << (bit)))
    
    /* Clear a bit */
    #define BIT_CLEAR(reg, bit)    ((reg) &= ~(1U << (bit)))
    
    /* Toggle a bit */
    #define BIT_TOGGLE(reg, bit)   ((reg) ^= (1U << (bit)))
    
    /* Test if bit is set */
    #define BIT_CHECK(reg, bit)    (((reg) >> (bit)) & 1U)
    
    /* Read bit value (returns 0 or 1) */
    #define BIT_READ(reg, bit)     (((reg) >> (bit)) & 1U)
    
    /* Write bit value (val must be 0 or 1) */
    #define BIT_WRITE(reg, bit, val) \
        ((val) ? BIT_SET(reg, bit) : BIT_CLEAR(reg, bit))
    
    /* Example usage */
    void gpio_operations(void) {
        BIT_SET(GPIOA->ODR, 5);      /* Set PA5 high */
        BIT_CLEAR(GPIOA->ODR, 6);    /* Set PA6 low */
        BIT_TOGGLE(GPIOA->ODR, 7);   /* Toggle PA7 */
        
        if (BIT_CHECK(GPIOA->IDR, 8)) {
            /* PA8 is high */
        }
    }

**Multi-Bit Operations**:

.. code-block:: c

    /* Set multiple bits using mask */
    #define BITS_SET(reg, mask)     ((reg) |= (mask))
    
    /* Clear multiple bits using mask */
    #define BITS_CLEAR(reg, mask)   ((reg) &= ~(mask))
    
    /* Modify field (clear then set) */
    #define FIELD_MODIFY(reg, mask, value) \
        ((reg) = ((reg) & ~(mask)) | ((value) & (mask)))
    
    /* Read field */
    #define FIELD_READ(reg, mask, shift) \
        (((reg) & (mask)) >> (shift))
    
    /* Example: Configure GPIO pin mode (2 bits per pin) */
    #define GPIO_MODE_INPUT   0x00
    #define GPIO_MODE_OUTPUT  0x01
    #define GPIO_MODE_AF      0x02
    #define GPIO_MODE_ANALOG  0x03
    
    void set_pin_mode(GPIO_TypeDef *gpio, uint8_t pin, uint8_t mode) {
        uint32_t mask = 0x3 << (pin * 2);     /* 2 bits per pin */
        uint32_t value = mode << (pin * 2);
        
        FIELD_MODIFY(gpio->MODER, mask, value);
    }

2.2 Atomic Bit Operations
--------------------------------------------------------------------------------

**Read-Modify-Write Protection**:

.. code-block:: c

    #include <stdbool.h>
    
    /**
     * Atomic bit set (disable interrupts during operation)
     */
    void atomic_bit_set(volatile uint32_t *reg, uint8_t bit) {
        uint32_t primask = __get_PRIMASK();  /* Save interrupt state */
        __disable_irq();                      /* Disable interrupts */
        
        *reg |= (1U << bit);
        
        __set_PRIMASK(primask);               /* Restore interrupts */
    }
    
    /**
     * Hardware atomic operations (if available)
     * STM32: Use BSRR (Bit Set/Reset Register) for atomic GPIO
     */
    void gpio_set_atomic(GPIO_TypeDef *gpio, uint8_t pin) {
        gpio->BSRR = (1U << pin);        /* Set bit atomically */
    }
    
    void gpio_clear_atomic(GPIO_TypeDef *gpio, uint8_t pin) {
        gpio->BSRR = (1U << (pin + 16)); /* Clear bit atomically */
    }

**Compare-and-Swap Pattern**:

.. code-block:: c

    /**
     * Atomic compare and swap for flag
     */
    bool atomic_flag_test_and_set(volatile bool *flag) {
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        
        bool old_value = *flag;
        *flag = true;
        
        __set_PRIMASK(primask);
        return old_value;
    }

================================================================================
3. Port Initialization Patterns
================================================================================

3.1 GPIO Configuration
--------------------------------------------------------------------------------

**Complete Pin Setup**:

.. code-block:: c

    /**
     * GPIO pin configuration structure
     */
    typedef struct {
        GPIO_TypeDef *port;    /* GPIO port (GPIOA, GPIOB, etc.) */
        uint8_t pin;           /* Pin number (0-15) */
        uint8_t mode;          /* Input, Output, AF, Analog */
        uint8_t otype;         /* Push-pull or Open-drain */
        uint8_t speed;         /* Low, Medium, High, Very High */
        uint8_t pull;          /* No pull, Pull-up, Pull-down */
        uint8_t af;            /* Alternate function number */
    } gpio_pin_config_t;
    
    /**
     * Initialize a GPIO pin
     */
    void gpio_init(const gpio_pin_config_t *config) {
        /* Enable GPIO clock (implementation-specific) */
        gpio_enable_clock(config->port);
        
        /* Configure mode (input, output, AF, analog) */
        uint32_t mode_mask = 0x3 << (config->pin * 2);
        uint32_t mode_val = config->mode << (config->pin * 2);
        FIELD_MODIFY(config->port->MODER, mode_mask, mode_val);
        
        /* Configure output type (push-pull / open-drain) */
        if (config->mode == GPIO_MODE_OUTPUT || config->mode == GPIO_MODE_AF) {
            if (config->otype) {
                BIT_SET(config->port->OTYPER, config->pin);
            } else {
                BIT_CLEAR(config->port->OTYPER, config->pin);
            }
        }
        
        /* Configure speed */
        uint32_t speed_mask = 0x3 << (config->pin * 2);
        uint32_t speed_val = config->speed << (config->pin * 2);
        FIELD_MODIFY(config->port->OSPEEDR, speed_mask, speed_val);
        
        /* Configure pull-up/pull-down */
        uint32_t pull_mask = 0x3 << (config->pin * 2);
        uint32_t pull_val = config->pull << (config->pin * 2);
        FIELD_MODIFY(config->port->PUPDR, pull_mask, pull_val);
        
        /* Configure alternate function */
        if (config->mode == GPIO_MODE_AF) {
            uint8_t af_index = config->pin / 8;  /* AFR[0] or AFR[1] */
            uint8_t af_shift = (config->pin % 8) * 4;
            uint32_t af_mask = 0xF << af_shift;
            uint32_t af_val = config->af << af_shift;
            FIELD_MODIFY(config->port->AFR[af_index], af_mask, af_val);
        }
    }

**Example Usage**:

.. code-block:: c

    void setup_leds_and_buttons(void) {
        /* LED on PA5 (output, push-pull) */
        gpio_pin_config_t led = {
            .port = GPIOA,
            .pin = 5,
            .mode = GPIO_MODE_OUTPUT,
            .otype = 0,  /* Push-pull */
            .speed = 0,  /* Low speed */
            .pull = 0,   /* No pull */
        };
        gpio_init(&led);
        
        /* Button on PC13 (input with pull-up) */
        gpio_pin_config_t button = {
            .port = GPIOC,
            .pin = 13,
            .mode = GPIO_MODE_INPUT,
            .pull = 1,  /* Pull-up */
        };
        gpio_init(&button);
        
        /* UART TX on PA9 (alternate function) */
        gpio_pin_config_t uart_tx = {
            .port = GPIOA,
            .pin = 9,
            .mode = GPIO_MODE_AF,
            .otype = 0,  /* Push-pull */
            .speed = 3,  /* Very high speed */
            .pull = 1,   /* Pull-up */
            .af = 7,     /* AF7 = USART1 */
        };
        gpio_init(&uart_tx);
    }

3.2 Peripheral Clock Enable
--------------------------------------------------------------------------------

**Clock Control Pattern**:

.. code-block:: c

    /**
     * RCC (Reset and Clock Control) register structure
     */
    typedef struct {
        volatile uint32_t CR;
        volatile uint32_t PLLCFGR;
        volatile uint32_t CFGR;
        volatile uint32_t CIR;
        volatile uint32_t AHB1RSTR;
        volatile uint32_t AHB2RSTR;
        uint32_t RESERVED[2];
        volatile uint32_t APB1RSTR;
        volatile uint32_t APB2RSTR;
        uint32_t RESERVED2[2];
        volatile uint32_t AHB1ENR;    /* AHB1 enable register */
        volatile uint32_t AHB2ENR;
        uint32_t RESERVED3[2];
        volatile uint32_t APB1ENR;    /* APB1 enable register */
        volatile uint32_t APB2ENR;    /* APB2 enable register */
    } RCC_TypeDef;
    
    #define RCC  ((RCC_TypeDef *)0x40023800)
    
    /**
     * Enable GPIO port clock
     */
    void gpio_enable_clock(GPIO_TypeDef *gpio) {
        if (gpio == GPIOA) {
            RCC->AHB1ENR |= (1 << 0);
        } else if (gpio == GPIOB) {
            RCC->AHB1ENR |= (1 << 1);
        } else if (gpio == GPIOC) {
            RCC->AHB1ENR |= (1 << 2);
        }
        /* Add small delay after clock enable */
        volatile uint32_t dummy = RCC->AHB1ENR;
        (void)dummy;  /* Prevent compiler warning */
    }

================================================================================
4. Hardware Abstraction Layer (HAL)
================================================================================

4.1 Basic GPIO HAL
--------------------------------------------------------------------------------

**Simple HAL Interface**:

.. code-block:: c

    /**
     * Hardware-independent GPIO HAL interface
     */
    typedef void* gpio_port_t;
    typedef uint8_t gpio_pin_t;
    
    typedef enum {
        GPIO_DIR_INPUT = 0,
        GPIO_DIR_OUTPUT = 1
    } gpio_direction_t;
    
    typedef enum {
        GPIO_LOW = 0,
        GPIO_HIGH = 1
    } gpio_state_t;
    
    /**
     * HAL API
     */
    void hal_gpio_set_direction(gpio_port_t port, gpio_pin_t pin, 
                                gpio_direction_t dir);
    void hal_gpio_write(gpio_port_t port, gpio_pin_t pin, gpio_state_t state);
    gpio_state_t hal_gpio_read(gpio_port_t port, gpio_pin_t pin);
    void hal_gpio_toggle(gpio_port_t port, gpio_pin_t pin);
    
    /**
     * Implementation for STM32
     */
    void hal_gpio_set_direction(gpio_port_t port, gpio_pin_t pin, 
                                gpio_direction_t dir) {
        GPIO_TypeDef *gpio = (GPIO_TypeDef *)port;
        uint32_t mode = (dir == GPIO_DIR_OUTPUT) ? GPIO_MODE_OUTPUT : GPIO_MODE_INPUT;
        
        uint32_t mask = 0x3 << (pin * 2);
        uint32_t value = mode << (pin * 2);
        FIELD_MODIFY(gpio->MODER, mask, value);
    }
    
    void hal_gpio_write(gpio_port_t port, gpio_pin_t pin, gpio_state_t state) {
        GPIO_TypeDef *gpio = (GPIO_TypeDef *)port;
        
        if (state == GPIO_HIGH) {
            gpio->BSRR = (1U << pin);
        } else {
            gpio->BSRR = (1U << (pin + 16));
        }
    }
    
    gpio_state_t hal_gpio_read(gpio_port_t port, gpio_pin_t pin) {
        GPIO_TypeDef *gpio = (GPIO_TypeDef *)port;
        return (gpio->IDR & (1U << pin)) ? GPIO_HIGH : GPIO_LOW;
    }
    
    void hal_gpio_toggle(gpio_port_t port, gpio_pin_t pin) {
        GPIO_TypeDef *gpio = (GPIO_TypeDef *)port;
        gpio->ODR ^= (1U << pin);
    }

**Application Using HAL**:

.. code-block:: c

    void application_code(void) {
        /* Hardware-independent code */
        gpio_port_t led_port = GPIOA;
        gpio_pin_t led_pin = 5;
        
        hal_gpio_set_direction(led_port, led_pin, GPIO_DIR_OUTPUT);
        hal_gpio_write(led_port, led_pin, GPIO_HIGH);
        
        /* This code works on any platform with HAL implementation */
    }

4.2 Advanced HAL with Error Handling
--------------------------------------------------------------------------------

**Robust HAL Pattern**:

.. code-block:: c

    typedef enum {
        HAL_OK = 0,
        HAL_ERROR,
        HAL_BUSY,
        HAL_TIMEOUT
    } hal_status_t;
    
    /**
     * GPIO handle with error tracking
     */
    typedef struct {
        GPIO_TypeDef *instance;
        gpio_pin_config_t config;
        hal_status_t error_code;
    } gpio_handle_t;
    
    /**
     * Initialize GPIO with error checking
     */
    hal_status_t hal_gpio_init(gpio_handle_t *handle) {
        if (handle == NULL || handle->instance == NULL) {
            return HAL_ERROR;
        }
        
        /* Validate pin number */
        if (handle->config.pin > 15) {
            handle->error_code = HAL_ERROR;
            return HAL_ERROR;
        }
        
        /* Enable clock */
        gpio_enable_clock(handle->instance);
        
        /* Configure pin */
        gpio_init(&handle->config);
        
        handle->error_code = HAL_OK;
        return HAL_OK;
    }
    
    /**
     * Usage with error checking
     */
    void safe_gpio_usage(void) {
        gpio_handle_t led_handle = {
            .instance = GPIOA,
            .config = {
                .port = GPIOA,
                .pin = 5,
                .mode = GPIO_MODE_OUTPUT,
            }
        };
        
        if (hal_gpio_init(&led_handle) != HAL_OK) {
            /* Handle error */
            error_handler();
        }
    }

================================================================================
5. Port Expander and Virtual Ports
================================================================================

5.1 I2C Port Expander Pattern
--------------------------------------------------------------------------------

**Virtual Port Abstraction**:

.. code-block:: c

    /**
     * Generic port interface (can be hardware or I2C expander)
     */
    typedef enum {
        PORT_TYPE_HARDWARE,
        PORT_TYPE_I2C_EXPANDER
    } port_type_t;
    
    typedef struct {
        port_type_t type;
        union {
            GPIO_TypeDef *hw_port;
            struct {
                uint8_t i2c_addr;
                uint8_t port_num;
            } expander;
        } hw;
        uint8_t shadow_reg;  /* Shadow register for expander */
    } virtual_port_t;
    
    /**
     * Write to virtual port
     */
    void vport_write(virtual_port_t *vport, uint8_t pin, bool state) {
        if (vport->type == PORT_TYPE_HARDWARE) {
            /* Direct hardware access */
            hal_gpio_write(vport->hw.hw_port, pin, state);
        } else {
            /* I2C expander - update shadow register */
            if (state) {
                vport->shadow_reg |= (1 << pin);
            } else {
                vport->shadow_reg &= ~(1 << pin);
            }
            
            /* Write to I2C device */
            i2c_write_byte(vport->hw.expander.i2c_addr, 
                          vport->hw.expander.port_num,
                          vport->shadow_reg);
        }
    }
    
    /**
     * Read from virtual port
     */
    bool vport_read(virtual_port_t *vport, uint8_t pin) {
        if (vport->type == PORT_TYPE_HARDWARE) {
            return hal_gpio_read(vport->hw.hw_port, pin);
        } else {
            uint8_t data = i2c_read_byte(vport->hw.expander.i2c_addr,
                                         vport->hw.expander.port_num);
            return (data & (1 << pin)) != 0;
        }
    }

================================================================================
6. Special Register Operations
================================================================================

6.1 Set/Clear Registers
--------------------------------------------------------------------------------

**Bit Set/Reset Register Pattern**:

.. code-block:: c

    /**
     * Many peripherals have separate set/clear registers
     * for atomic operations without read-modify-write
     */
    
    /* Example: GPIO with BSRR (Bit Set/Reset Register) */
    void gpio_set_pin(GPIO_TypeDef *gpio, uint8_t pin) {
        /* Lower 16 bits: set bits
           Upper 16 bits: clear bits */
        gpio->BSRR = (1U << pin);        /* Set pin */
    }
    
    void gpio_clear_pin(GPIO_TypeDef *gpio, uint8_t pin) {
        gpio->BSRR = (1U << (pin + 16)); /* Clear pin */
    }
    
    /**
     * Generic set/clear register abstraction
     */
    typedef struct {
        volatile uint32_t *set_reg;
        volatile uint32_t *clear_reg;
    } setclr_regs_t;
    
    void setclr_set_bits(const setclr_regs_t *regs, uint32_t mask) {
        *regs->set_reg = mask;
    }
    
    void setclr_clear_bits(const setclr_regs_t *regs, uint32_t mask) {
        *regs->clear_reg = mask;
    }

6.2 Read-Only and Write-Only Registers
--------------------------------------------------------------------------------

**Access Control Pattern**:

.. code-block:: c

    /**
     * Explicitly mark read-only and write-only registers
     */
    #define __RO  volatile const  /* Read-only */
    #define __WO  volatile        /* Write-only */
    #define __RW  volatile        /* Read-write */
    
    typedef struct {
        __RW uint32_t CTRL;     /* Control register (R/W) */
        __RO uint32_t STATUS;   /* Status register (RO) */
        __WO uint32_t CMD;      /* Command register (WO) */
        __RW uint32_t DATA;     /* Data register (R/W) */
    } peripheral_regs_t;
    
    /**
     * Usage
     */
    void use_peripheral(peripheral_regs_t *periph) {
        uint32_t status = periph->STATUS;  /* OK: read from RO */
        periph->CMD = 0x01;                /* OK: write to WO */
        
        /* Compiler error: cannot write to const */
        // periph->STATUS = 0;  /* ERROR! */
    }

================================================================================
7. Safe Register Access Patterns
================================================================================

7.1 Read-Modify-Write Wrapper
--------------------------------------------------------------------------------

**Safe Modify Function**:

.. code-block:: c

    /**
     * Safe register modify with critical section
     */
    void reg_modify_safe(volatile uint32_t *reg, uint32_t clear_mask, 
                         uint32_t set_mask) {
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        
        uint32_t val = *reg;
        val &= ~clear_mask;  /* Clear bits */
        val |= set_mask;     /* Set bits */
        *reg = val;
        
        __set_PRIMASK(primask);
    }
    
    /**
     * Usage
     */
    void configure_peripheral(void) {
        /* Clear bits 8-10, set bit 5 */
        reg_modify_safe(&PERIPHERAL->CTRL, 0x700, 0x20);
    }

7.2 Register Transaction Pattern
--------------------------------------------------------------------------------

**Transactional Register Updates**:

.. code-block:: c

    /**
     * Begin register transaction (save state)
     */
    typedef struct {
        volatile uint32_t *reg;
        uint32_t saved_value;
        bool active;
    } reg_transaction_t;
    
    void reg_transaction_begin(reg_transaction_t *txn, volatile uint32_t *reg) {
        txn->reg = reg;
        txn->saved_value = *reg;
        txn->active = true;
    }
    
    /**
     * Commit or rollback
     */
    void reg_transaction_commit(reg_transaction_t *txn) {
        txn->active = false;
    }
    
    void reg_transaction_rollback(reg_transaction_t *txn) {
        if (txn->active) {
            *txn->reg = txn->saved_value;
            txn->active = false;
        }
    }
    
    /**
     * Usage
     */
    bool configure_with_validation(void) {
        reg_transaction_t txn;
        
        reg_transaction_begin(&txn, &PERIPHERAL->CTRL);
        
        /* Make changes */
        *txn.reg |= (1 << 5);
        *txn.reg &= ~(1 << 8);
        
        /* Validate */
        if (peripheral_self_test()) {
            reg_transaction_commit(&txn);
            return true;
        } else {
            reg_transaction_rollback(&txn);
            return false;
        }
    }

================================================================================
8. Port I/O Best Practices
================================================================================

8.1 Guidelines
--------------------------------------------------------------------------------

**DO**:

- Always use `volatile` for hardware registers
- Use structs for register mapping (better readability)
- Define clear macros for bit manipulation
- Document register addresses and bit fields
- Use atomic operations when available (BSRR, etc.)
- Protect read-modify-write with critical sections if needed
- Validate parameters in HAL functions
- Use const for read-only registers
- Add delays after clock enables
- Initialize all GPIO pins explicitly

**DON'T**:

- Never access registers without `volatile`
- Avoid magic numbers (use meaningful macros)
- Don't assume register reset values
- Never modify reserved bits
- Avoid busy-waiting on hardware without timeout
- Don't forget to enable peripheral clocks
- Never nest critical sections excessively
- Avoid platform-specific code in application layer

8.2 Common Pitfalls
--------------------------------------------------------------------------------

**Missing Volatile**:

.. code-block:: c

    /* WRONG */
    uint32_t *reg = (uint32_t *)0x40000000;
    while (!(*reg & 0x01));  /* May optimize to infinite loop */
    
    /* CORRECT */
    volatile uint32_t *reg = (volatile uint32_t *)0x40000000;
    while (!(*reg & 0x01));  /* Always reads from hardware */

**Race Condition in RMW**:

.. code-block:: c

    /* WRONG - race condition if interrupt modifies same register */
    void set_bit_unsafe(void) {
        GPIO->ODR |= (1 << 5);  /* Read-Modify-Write not atomic */
    }
    
    /* CORRECT - use hardware atomic operation */
    void set_bit_safe(void) {
        GPIO->BSRR = (1 << 5);  /* Atomic set */
    }
    
    /* CORRECT - use critical section if no atomic operation */
    void set_bit_critical(void) {
        __disable_irq();
        GPIO->ODR |= (1 << 5);
        __enable_irq();
    }

**Clock Not Enabled**:

.. code-block:: c

    /* WRONG - accessing GPIO without enabling clock */
    void broken_init(void) {
        GPIOA->MODER |= (1 << 10);  /* May fault or have no effect */
    }
    
    /* CORRECT */
    void correct_init(void) {
        RCC->AHB1ENR |= (1 << 0);     /* Enable GPIOA clock */
        __DSB();                       /* Ensure write completes */
        GPIOA->MODER |= (1 << 10);    /* Now safe to access */
    }

================================================================================
9. Platform-Specific Examples
================================================================================

9.1 STM32 GPIO
--------------------------------------------------------------------------------

**Complete Example**:

.. code-block:: c

    void stm32_led_init(void) {
        /* Enable GPIOA clock */
        RCC->AHB1ENR |= (1 << 0);
        
        /* Configure PA5 as output */
        GPIOA->MODER &= ~(3 << 10);   /* Clear mode bits */
        GPIOA->MODER |= (1 << 10);    /* Set as output */
        
        /* Push-pull output */
        GPIOA->OTYPER &= ~(1 << 5);
        
        /* Medium speed */
        GPIOA->OSPEEDR &= ~(3 << 10);
        GPIOA->OSPEEDR |= (1 << 10);
        
        /* No pull-up/pull-down */
        GPIOA->PUPDR &= ~(3 << 10);
    }
    
    void stm32_led_toggle(void) {
        GPIOA->ODR ^= (1 << 5);
    }

9.2 AVR GPIO
--------------------------------------------------------------------------------

**ATmega328P Example**:

.. code-block:: c

    #include <avr/io.h>
    
    void avr_led_init(void) {
        /* Set PB5 (Arduino pin 13) as output */
        DDRB |= (1 << DDB5);
    }
    
    void avr_led_on(void) {
        PORTB |= (1 << PORTB5);
    }
    
    void avr_led_off(void) {
        PORTB &= ~(1 << PORTB5);
    }
    
    void avr_led_toggle(void) {
        PORTB ^= (1 << PORTB5);
    }

9.3 ESP32 GPIO
--------------------------------------------------------------------------------

**ESP32 Example**:

.. code-block:: c

    #include "driver/gpio.h"
    
    #define LED_PIN GPIO_NUM_2
    
    void esp32_led_init(void) {
        gpio_config_t io_conf = {
            .pin_bit_mask = (1ULL << LED_PIN),
            .mode = GPIO_MODE_OUTPUT,
            .pull_up_en = GPIO_PULLUP_DISABLE,
            .pull_down_en = GPIO_PULLDOWN_DISABLE,
            .intr_type = GPIO_INTR_DISABLE,
        };
        gpio_config(&io_conf);
    }
    
    void esp32_led_set(bool state) {
        gpio_set_level(LED_PIN, state);
    }

================================================================================
See Also
================================================================================

- :doc:`Embedded C </Languages/Embedded C>`
- :doc:`Embedded System Architecture </Embedded/Embedded_System_Architecture_Patterns>`
- :doc:`Embedded Design Patterns </Embedded/Embedded_Design_Patterns_Structural>`
- :doc:`Linux Device Tree </Linux/Linux device tree>`
- :doc:`Linux DMA </Linux/Linux DMA>`
