=============================================
Embedded Design Patterns - Structural
=============================================

:Author: Embedded Systems Design Patterns Documentation
:Date: January 2026
:Version: 1.0
:Focus: Structural design patterns for embedded systems

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Structural Patterns Overview
-----------------------------

.. code-block:: text

   Structural Patterns:
   
   1. Hardware Proxy
      - Abstracts hardware access
      - Provides safe interface
   
   2. Debouncing Decorator
      - Filters transient signals
      - Stabilizes input
   
   3. Interrupt Service Routine (ISR) Adapter
      - Adapts hardware interrupts to software handlers
      - Minimizes ISR code
   
   4. Device Driver
      - Encapsulates hardware control
      - Provides consistent API
   
   5. Bridge
      - Separates abstraction from implementation
      - Allows independent variation

Hardware Proxy Pattern
======================

Intent
------

Provide a safe, controlled interface to hardware registers while hiding direct memory access details.

Structure
---------

.. code-block:: c

   // Hardware Proxy for GPIO port
   typedef struct {
       volatile uint32_t *data_reg;
       volatile uint32_t *dir_reg;
       volatile uint32_t *mode_reg;
       uint8_t pin_mask;
   } GPIO_Proxy;
   
   // Initialize proxy
   void GPIO_Proxy_Init(GPIO_Proxy *self, uint32_t base_addr, uint8_t pin) {
       self->data_reg = (volatile uint32_t *)(base_addr + 0x00);
       self->dir_reg  = (volatile uint32_t *)(base_addr + 0x04);
       self->mode_reg = (volatile uint32_t *)(base_addr + 0x08);
       self->pin_mask = (1 << pin);
   }
   
   // High-level operations
   void GPIO_SetOutput(GPIO_Proxy *self) {
       *self->dir_reg |= self->pin_mask;
   }
   
   void GPIO_SetInput(GPIO_Proxy *self) {
       *self->dir_reg &= ~self->pin_mask;
   }
   
   void GPIO_SetHigh(GPIO_Proxy *self) {
       *self->data_reg |= self->pin_mask;
   }
   
   void GPIO_SetLow(GPIO_Proxy *self) {
       *self->data_reg &= ~self->pin_mask;
   }
   
   bool GPIO_Read(GPIO_Proxy *self) {
       return (*self->data_reg & self->pin_mask) != 0;
   }
   
   void GPIO_Toggle(GPIO_Proxy *self) {
       *self->data_reg ^= self->pin_mask;
   }

Usage
-----

.. code-block:: c

   int main(void) {
       GPIO_Proxy led;
       
       // Initialize LED on GPIOA, pin 5
       GPIO_Proxy_Init(&led, GPIOA_BASE, 5);
       GPIO_SetOutput(&led);
       
       while (1) {
           GPIO_Toggle(&led);
           delay_ms(500);
       }
   }

Benefits
--------

- **Safety**: Prevents invalid register access
- **Abstraction**: Hides hardware details
- **Portability**: Easy to adapt to different hardware
- **Testability**: Can mock for unit tests

Debouncing Decorator
=====================

Intent
------

Add debouncing functionality to existing button/switch objects to filter mechanical bounce.

Structure
---------

.. code-block:: c

   // Button interface
   typedef bool (*ButtonRead_fn)(void *context);
   
   typedef struct {
       ButtonRead_fn read;
       void *context;
   } Button;
   
   // Debouncing decorator
   typedef struct {
       Button *button;              // Decorated button
       uint16_t debounce_time_ms;   // Debounce period
       uint32_t last_change_time;   // Last state change
       bool last_stable_state;      // Last stable state
       bool current_state;          // Current raw state
   } DebouncedButton;
   
   void DebouncedButton_Init(DebouncedButton *self, Button *button,
                             uint16_t debounce_ms) {
       self->button = button;
       self->debounce_time_ms = debounce_ms;
       self->last_change_time = 0;
       self->last_stable_state = false;
       self->current_state = false;
   }
   
   bool DebouncedButton_Read(DebouncedButton *self) {
       bool raw_state = self->button->read(self->button->context);
       uint32_t current_time = get_tick_count();
       
       // Detect state change
       if (raw_state != self->current_state) {
           self->current_state = raw_state;
           self->last_change_time = current_time;
       }
       
       // Check if debounce period elapsed
       if ((current_time - self->last_change_time) >= self->debounce_time_ms) {
           self->last_stable_state = self->current_state;
       }
       
       return self->last_stable_state;
   }

Advanced Debouncing
-------------------

.. code-block:: c

   // Multi-state debouncing with hysteresis
   typedef enum {
       DEBOUNCE_STATE_LOW,
       DEBOUNCE_STATE_TRANSITION_HIGH,
       DEBOUNCE_STATE_HIGH,
       DEBOUNCE_STATE_TRANSITION_LOW
   } DebounceState;
   
   typedef struct {
       Button *button;
       DebounceState state;
       uint32_t transition_start;
       uint16_t debounce_ms;
   } HysteresisDebouncer;
   
   bool HysteresisDebouncer_Update(HysteresisDebouncer *self) {
       bool raw = self->button->read(self->button->context);
       uint32_t now = get_tick_count();
       uint32_t elapsed = now - self->transition_start;
       
       switch (self->state) {
       case DEBOUNCE_STATE_LOW:
           if (raw) {
               self->state = DEBOUNCE_STATE_TRANSITION_HIGH;
               self->transition_start = now;
           }
           return false;
           
       case DEBOUNCE_STATE_TRANSITION_HIGH:
           if (!raw) {
               self->state = DEBOUNCE_STATE_LOW;
           } else if (elapsed >= self->debounce_ms) {
               self->state = DEBOUNCE_STATE_HIGH;
           }
           return false;
           
       case DEBOUNCE_STATE_HIGH:
           if (!raw) {
               self->state = DEBOUNCE_STATE_TRANSITION_LOW;
               self->transition_start = now;
           }
           return true;
           
       case DEBOUNCE_STATE_TRANSITION_LOW:
           if (raw) {
               self->state = DEBOUNCE_STATE_HIGH;
           } else if (elapsed >= self->debounce_ms) {
               self->state = DEBOUNCE_STATE_LOW;
           }
           return true;
       }
       
       return false;
   }

ISR Adapter Pattern
===================

Intent
------

Adapt hardware interrupts to application-level handlers while keeping ISR minimal.

Structure
---------

.. code-block:: c

   // ISR Adapter
   typedef void (*ISR_Callback)(void *context);
   
   typedef struct {
       ISR_Callback callback;
       void *context;
       volatile bool pending;
   } ISR_Adapter;
   
   static ISR_Adapter timer_adapter;
   static ISR_Adapter uart_adapter;
   
   // Hardware ISR - minimal, just set flag
   void TIMER_IRQHandler(void) {
       // Clear interrupt flag
       TIMER->SR = 0;
       
       // Signal adapter
       timer_adapter.pending = true;
   }
   
   void UART_IRQHandler(void) {
       // Read data register (clears interrupt)
       volatile uint8_t data = UART->DR;
       
       // Store data and signal
       uart_adapter.context = (void *)(uintptr_t)data;
       uart_adapter.pending = true;
   }
   
   // Initialize adapter
   void ISR_Adapter_Init(ISR_Adapter *self, ISR_Callback cb, void *ctx) {
       self->callback = cb;
       self->context = ctx;
       self->pending = false;
   }
   
   // Process pending interrupts (called from main loop or task)
   void ISR_Adapter_Process(ISR_Adapter *self) {
       if (self->pending) {
           self->pending = false;
           if (self->callback) {
               self->callback(self->context);
           }
       }
   }

Usage
-----

.. code-block:: c

   void timer_handler(void *context) {
       // Long processing, safe to do here
       update_display();
       process_sensor_data();
   }
   
   void uart_handler(void *context) {
       uint8_t data = (uint8_t)(uintptr_t)context;
       process_received_byte(data);
   }
   
   int main(void) {
       ISR_Adapter_Init(&timer_adapter, timer_handler, NULL);
       ISR_Adapter_Init(&uart_adapter, uart_handler, NULL);
       
       // Enable interrupts
       NVIC_EnableIRQ(TIMER_IRQn);
       NVIC_EnableIRQ(UART_IRQn);
       
       while (1) {
           // Process in main loop
           ISR_Adapter_Process(&timer_adapter);
           ISR_Adapter_Process(&uart_adapter);
           
           // Or in RTOS task
       }
   }

Device Driver Pattern
=====================

Intent
------

Encapsulate hardware device access into a reusable, testable component.

Structure
---------

.. code-block:: c

   // Device Driver Interface
   typedef struct Device_Driver Device_Driver;
   
   typedef int (*Driver_Init_fn)(Device_Driver *self);
   typedef int (*Driver_Read_fn)(Device_Driver *self, void *buffer, size_t len);
   typedef int (*Driver_Write_fn)(Device_Driver *self, const void *buffer, size_t len);
   typedef int (*Driver_Ioctl_fn)(Device_Driver *self, uint32_t cmd, void *arg);
   typedef int (*Driver_Close_fn)(Device_Driver *self);
   
   struct Device_Driver {
       Driver_Init_fn init;
       Driver_Read_fn read;
       Driver_Write_fn write;
       Driver_Ioctl_fn ioctl;
       Driver_Close_fn close;
       void *private_data;
   };
   
   // UART Driver Implementation
   typedef struct {
       Device_Driver base;
       UART_TypeDef *uart;
       uint32_t baudrate;
       RingBuffer rx_buffer;
       RingBuffer tx_buffer;
   } UART_Driver;
   
   int UART_Init(Device_Driver *self) {
       UART_Driver *uart = (UART_Driver *)self;
       
       // Configure UART hardware
       uart->uart->BRR = SystemCoreClock / uart->baudrate;
       uart->uart->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
       
       // Initialize buffers
       RingBuffer_Init(&uart->rx_buffer, 256);
       RingBuffer_Init(&uart->tx_buffer, 256);
       
       // Enable interrupts
       uart->uart->CR1 |= USART_CR1_RXNEIE;
       
       return 0;
   }
   
   int UART_Read(Device_Driver *self, void *buffer, size_t len) {
       UART_Driver *uart = (UART_Driver *)self;
       size_t read_count = 0;
       uint8_t *buf = (uint8_t *)buffer;
       
       while (len > 0 && !RingBuffer_IsEmpty(&uart->rx_buffer)) {
           *buf++ = RingBuffer_Get(&uart->rx_buffer);
           read_count++;
           len--;
       }
       
       return read_count;
   }
   
   int UART_Write(Device_Driver *self, const void *buffer, size_t len) {
       UART_Driver *uart = (UART_Driver *)self;
       const uint8_t *buf = (const uint8_t *)buffer;
       size_t written = 0;
       
       while (len > 0 && !RingBuffer_IsFull(&uart->tx_buffer)) {
           RingBuffer_Put(&uart->tx_buffer, *buf++);
           written++;
           len--;
       }
       
       // Enable TX interrupt
       uart->uart->CR1 |= USART_CR1_TXEIE;
       
       return written;
   }
   
   // Device driver factory
   Device_Driver *UART_Create(UART_TypeDef *uart_hw, uint32_t baudrate) {
       UART_Driver *uart = malloc(sizeof(UART_Driver));
       
       uart->base.init = UART_Init;
       uart->base.read = UART_Read;
       uart->base.write = UART_Write;
       uart->base.ioctl = UART_Ioctl;
       uart->base.close = UART_Close;
       uart->uart = uart_hw;
       uart->baudrate = baudrate;
       
       return &uart->base;
   }

Usage
-----

.. code-block:: c

   // Create and initialize driver
   Device_Driver *uart1 = UART_Create(USART1, 115200);
   uart1->init(uart1);
   
   // Use driver
   char message[] = "Hello, World!\n";
   uart1->write(uart1, message, strlen(message));
   
   char buffer[64];
   int received = uart1->read(uart1, buffer, sizeof(buffer));

Bridge Pattern
==============

Intent
------

Separate abstraction from implementation, allowing them to vary independently.

Structure
---------

.. code-block:: c

   // Implementation interface
   typedef struct Display_Impl Display_Impl;
   
   typedef void (*Display_WritePixel_fn)(Display_Impl *self, int x, int y, uint32_t color);
   typedef void (*Display_Fill_fn)(Display_Impl *self, uint32_t color);
   typedef void (*Display_Flush_fn)(Display_Impl *self);
   
   struct Display_Impl {
       Display_WritePixel_fn write_pixel;
       Display_Fill_fn fill;
       Display_Flush_fn flush;
       uint16_t width;
       uint16_t height;
       void *private_data;
   };
   
   // Abstraction
   typedef struct {
       Display_Impl *impl;
   } Display;
   
   void Display_Init(Display *self, Display_Impl *impl) {
       self->impl = impl;
   }
   
   void Display_DrawLine(Display *self, int x0, int y0, int x1, int y1, uint32_t color) {
       // Bresenham's line algorithm
       int dx = abs(x1 - x0);
       int dy = abs(y1 - y0);
       int sx = (x0 < x1) ? 1 : -1;
       int sy = (y0 < y1) ? 1 : -1;
       int err = dx - dy;
       
       while (1) {
           self->impl->write_pixel(self->impl, x0, y0, color);
           
           if (x0 == x1 && y0 == y1) break;
           
           int e2 = 2 * err;
           if (e2 > -dy) {
               err -= dy;
               x0 += sx;
           }
           if (e2 < dx) {
               err += dx;
               y0 += sy;
           }
       }
   }
   
   void Display_DrawRectangle(Display *self, int x, int y, int w, int h, uint32_t color) {
       Display_DrawLine(self, x, y, x + w, y, color);
       Display_DrawLine(self, x + w, y, x + w, y + h, color);
       Display_DrawLine(self, x + w, y + h, x, y + h, color);
       Display_DrawLine(self, x, y + h, x, y, color);
   }

Implementations
---------------

.. code-block:: c

   // SPI LCD Implementation
   typedef struct {
       Display_Impl base;
       SPI_TypeDef *spi;
       GPIO_Pin cs_pin;
       GPIO_Pin dc_pin;
       uint16_t *framebuffer;
   } SPI_LCD_Impl;
   
   void SPI_LCD_WritePixel(Display_Impl *self, int x, int y, uint32_t color) {
       SPI_LCD_Impl *lcd = (SPI_LCD_Impl *)self;
       if (x >= 0 && x < self->width && y >= 0 && y < self->height) {
           lcd->framebuffer[y * self->width + x] = color;
       }
   }
   
   void SPI_LCD_Flush(Display_Impl *self) {
       SPI_LCD_Impl *lcd = (SPI_LCD_Impl *)self;
       // Transfer framebuffer to LCD via SPI
       SPI_Transfer(lcd->spi, (uint8_t *)lcd->framebuffer,
                   self->width * self->height * 2);
   }
   
   // Parallel LCD Implementation
   typedef struct {
       Display_Impl base;
       volatile uint16_t *data_port;
       volatile uint8_t *control_port;
   } Parallel_LCD_Impl;
   
   void Parallel_LCD_WritePixel(Display_Impl *self, int x, int y, uint32_t color) {
       Parallel_LCD_Impl *lcd = (Parallel_LCD_Impl *)self;
       // Direct write to LCD
       LCD_SetWindow(lcd, x, y, x, y);
       *lcd->data_port = color;
   }
   
   // Create implementations
   Display_Impl *SPI_LCD_Create(SPI_TypeDef *spi, uint16_t width, uint16_t height) {
       SPI_LCD_Impl *impl = malloc(sizeof(SPI_LCD_Impl));
       impl->base.write_pixel = SPI_LCD_WritePixel;
       impl->base.fill = SPI_LCD_Fill;
       impl->base.flush = SPI_LCD_Flush;
       impl->base.width = width;
       impl->base.height = height;
       impl->spi = spi;
       impl->framebuffer = malloc(width * height * 2);
       return &impl->base;
   }

Usage
-----

.. code-block:: c

   // Use either implementation with same abstraction
   Display_Impl *impl = SPI_LCD_Create(SPI1, 240, 320);
   // or
   // Display_Impl *impl = Parallel_LCD_Create(LCD_PORT, 480, 800);
   
   Display display;
   Display_Init(&display, impl);
   
   // Same high-level code works with both implementations
   Display_DrawRectangle(&display, 10, 10, 100, 50, COLOR_RED);
   Display_DrawLine(&display, 0, 0, 239, 319, COLOR_BLUE);

Facade Pattern
==============

Intent
------

Provide a simplified interface to a complex subsystem.

Structure
---------

.. code-block:: c

   // Complex subsystem
   typedef struct {
       // ...
   } ADC_Module;
   
   typedef struct {
       // ...
   } DMA_Module;
   
   typedef struct {
       // ...
   } Timer_Module;
   
   // Facade
   typedef struct {
       ADC_Module adc;
       DMA_Module dma;
       Timer_Module timer;
       uint16_t *sample_buffer;
       size_t buffer_size;
   } ADC_Acquisition_Facade;
   
   void ADC_Facade_Init(ADC_Acquisition_Facade *self, size_t buffer_size) {
       self->buffer_size = buffer_size;
       self->sample_buffer = malloc(buffer_size * sizeof(uint16_t));
       
       // Configure subsystems
       ADC_Init(&self->adc, ADC_12BIT, ADC_CHANNEL_0);
       DMA_Init(&self->dma, DMA_CHANNEL_1);
       Timer_Init(&self->timer, TIMER_2);
       
       // Link subsystems
       DMA_SetSource(&self->dma, &self->adc);
       DMA_SetDestination(&self->dma, self->sample_buffer, buffer_size);
       Timer_SetCallback(&self->timer, ADC_Trigger, &self->adc);
   }
   
   void ADC_Facade_StartContinuous(ADC_Acquisition_Facade *self, uint32_t sample_rate) {
       Timer_SetFrequency(&self->timer, sample_rate);
       DMA_EnableCircular(&self->dma);
       ADC_EnableDMA(&self->adc);
       Timer_Start(&self->timer);
   }
   
   uint16_t ADC_Facade_GetLatestSample(ADC_Acquisition_Facade *self) {
       size_t index = DMA_GetCurrentIndex(&self->dma);
       return self->sample_buffer[index];
   }

Best Practices
==============

1. **Use proxies** for hardware access safety
2. **Debounce all mechanical inputs** (buttons, switches)
3. **Keep ISRs minimal** using adapter pattern
4. **Encapsulate devices** in driver structures
5. **Separate abstraction from implementation** (bridge)
6. **Provide facades** for complex subsystems
7. **Make patterns testable** (dependency injection)
8. **Document pattern intent** clearly
9. **Consider memory constraints** when choosing patterns
10. **Profile pattern overhead** in critical paths

Common Pitfalls
===============

1. **Over-engineering** - don't use patterns unnecessarily
2. **Memory overhead** - patterns add indirection
3. **Performance cost** - function pointers have overhead
4. **Complexity** - patterns can obscure simple code
5. **Tight coupling** - not properly abstracting interfaces

Quick Reference
===============

.. code-block:: c

   // Hardware Proxy
   GPIO_Proxy led;
   GPIO_Proxy_Init(&led, GPIOA_BASE, 5);
   GPIO_SetHigh(&led);
   
   // Debouncing
   DebouncedButton btn;
   DebouncedButton_Init(&btn, &raw_button, 50);
   if (DebouncedButton_Read(&btn)) { /* pressed */ }
   
   // ISR Adapter
   ISR_Adapter_Process(&adapter);
   
   // Device Driver
   driver->write(driver, data, len);
   
   // Bridge
   Display_Init(&display, impl);
   Display_DrawLine(&display, x0, y0, x1, y1, color);

See Also
========

- Embedded_Design_Patterns_Behavioral.rst
- Embedded_Design_Patterns_Concurrency.rst
- Embedded_State_Machines.rst

References
==========

- Design Patterns for Embedded Systems in C (Bruce Powel Douglass)
- Embedded C Coding Standard
- MISRA C Guidelines
