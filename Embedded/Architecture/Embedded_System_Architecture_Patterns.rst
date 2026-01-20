=============================================
Embedded System Architecture Patterns
=============================================

:Author: Embedded Systems Design Documentation
:Date: January 2026
:Version: 1.0
:Focus: Architectural patterns for embedded system design
:Source: Making Embedded Systems (Elecia White) + industry practices

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Architecture Patterns Overview
-------------------------------

.. code-block:: text

   Embedded Architecture Patterns:
   
   1. Layered Architecture
      - Hardware Abstraction Layer (HAL)
      - Driver Layer
      - Middleware
      - Application Layer
   
   2. Event-Driven Architecture
      - Event loops
      - Callbacks
      - Message queues
   
   3. Component-Based Design
      - Modular components
      - Well-defined interfaces
      - Loose coupling
   
   4. Pipe-and-Filter
      - Data processing pipelines
      - Filters transform data
   
   5. Model-View-Controller (MVC)
      - Separation of concerns
      - UI patterns

Layered Architecture
====================

Intent
------

Organize code into distinct layers with clear responsibilities and dependencies.

Classic Embedded Layers
-----------------------

.. code-block:: c

   /*
    * Layer 4: Application Layer
    * - Business logic
    * - User interface
    * - Application-specific features
    */
   
   void application_main(void) {
       // Uses middleware APIs
       sensor_start_reading();
       display_update();
       process_user_input();
   }
   
   /*
    * Layer 3: Middleware Layer
    * - Protocol stacks
    * - File systems
    * - Graphics libraries
    * - RTOS
    */
   
   void sensor_start_reading(void) {
       // Uses driver APIs
       i2c_master_transmit(SENSOR_ADDR, cmd, len);
   }
   
   /*
    * Layer 2: Driver Layer
    * - Device drivers
    * - Peripheral control
    * - Hardware-specific code
    */
   
   int i2c_master_transmit(uint8_t addr, const uint8_t *data, size_t len) {
       // Uses HAL APIs
       HAL_I2C_Master_Transmit(&hi2c1, addr, data, len, TIMEOUT);
   }
   
   /*
    * Layer 1: Hardware Abstraction Layer (HAL)
    * - Register access
    * - Low-level peripheral control
    * - Platform-specific code
    */
   
   void HAL_I2C_Master_Transmit(I2C_TypeDef *i2c, uint8_t addr,
                                const uint8_t *data, size_t len, uint32_t timeout) {
       // Direct hardware access
       i2c->CR1 |= I2C_CR1_START;
       while (!(i2c->SR1 & I2C_SR1_SB));
       i2c->DR = addr;
       // ...
   }

Hardware Abstraction Layer (HAL)
---------------------------------

.. code-block:: c

   // HAL interface for GPIO
   typedef struct {
       void (*init)(GPIO_Port port, GPIO_Pin pin, GPIO_Mode mode);
       void (*write)(GPIO_Port port, GPIO_Pin pin, bool value);
       bool (*read)(GPIO_Port port, GPIO_Pin pin);
       void (*toggle)(GPIO_Port port, GPIO_Pin pin);
   } GPIO_HAL;
   
   // STM32 implementation
   static void stm32_gpio_init(GPIO_Port port, GPIO_Pin pin, GPIO_Mode mode) {
       GPIO_TypeDef *gpio = (GPIO_TypeDef *)port;
       // STM32-specific initialization
       gpio->MODER &= ~(3 << (pin * 2));
       gpio->MODER |= (mode << (pin * 2));
   }
   
   static void stm32_gpio_write(GPIO_Port port, GPIO_Pin pin, bool value) {
       GPIO_TypeDef *gpio = (GPIO_TypeDef *)port;
       if (value) {
           gpio->BSRR = (1 << pin);
       } else {
           gpio->BSRR = (1 << (pin + 16));
       }
   }
   
   static const GPIO_HAL stm32_gpio_hal = {
       .init = stm32_gpio_init,
       .write = stm32_gpio_write,
       .read = stm32_gpio_read,
       .toggle = stm32_gpio_toggle
   };
   
   // ATmega implementation
   static const GPIO_HAL atmega_gpio_hal = {
       .init = atmega_gpio_init,
       .write = atmega_gpio_write,
       .read = atmega_gpio_read,
       .toggle = atmega_gpio_toggle
   };
   
   // Platform-independent code uses HAL
   extern const GPIO_HAL *gpio_hal;
   
   void led_init(void) {
       gpio_hal->init(LED_PORT, LED_PIN, GPIO_MODE_OUTPUT);
   }
   
   void led_on(void) {
       gpio_hal->write(LED_PORT, LED_PIN, true);
   }

Event-Driven Architecture
==========================

Super Loop with Events
----------------------

.. code-block:: c

   // Event structure
   typedef enum {
       EVENT_NONE,
       EVENT_BUTTON_PRESS,
       EVENT_BUTTON_RELEASE,
       EVENT_TIMER_TICK,
       EVENT_DATA_READY,
       EVENT_ERROR
   } EventType;
   
   typedef struct {
       EventType type;
       uint32_t timestamp;
       void *data;
   } Event;
   
   // Event queue
   #define EVENT_QUEUE_SIZE 32
   static Event event_queue[EVENT_QUEUE_SIZE];
   static volatile uint8_t queue_head = 0;
   static volatile uint8_t queue_tail = 0;
   
   void event_post(EventType type, void *data) {
       uint8_t next = (queue_tail + 1) % EVENT_QUEUE_SIZE;
       if (next != queue_head) {
           event_queue[queue_tail].type = type;
           event_queue[queue_tail].timestamp = get_tick_count();
           event_queue[queue_tail].data = data;
           queue_tail = next;
       }
   }
   
   bool event_get(Event *event) {
       if (queue_head == queue_tail) {
           return false;  // No events
       }
       
       *event = event_queue[queue_head];
       queue_head = (queue_head + 1) % EVENT_QUEUE_SIZE;
       return true;
   }
   
   // Event handlers
   void handle_button_press(void *data) {
       // Process button press
       toggle_led();
   }
   
   void handle_timer_tick(void *data) {
       // Update state
       update_sensor_readings();
   }
   
   void handle_data_ready(void *data) {
       // Process incoming data
       process_uart_data(data);
   }
   
   // Main event loop
   int main(void) {
       system_init();
       
       while (1) {
           Event event;
           
           if (event_get(&event)) {
               switch (event.type) {
               case EVENT_BUTTON_PRESS:
                   handle_button_press(event.data);
                   break;
               case EVENT_TIMER_TICK:
                   handle_timer_tick(event.data);
                   break;
               case EVENT_DATA_READY:
                   handle_data_ready(event.data);
                   break;
               case EVENT_ERROR:
                   handle_error(event.data);
                   break;
               default:
                   break;
               }
           } else {
               // No events, can enter low-power mode
               enter_sleep_mode();
           }
       }
   }

Callback-Based Event Handling
------------------------------

.. code-block:: c

   // Callback registry
   typedef void (*EventCallback)(void *context);
   
   typedef struct {
       EventType type;
       EventCallback callback;
       void *context;
   } EventSubscription;
   
   #define MAX_SUBSCRIPTIONS 16
   static EventSubscription subscriptions[MAX_SUBSCRIPTIONS];
   static size_t subscription_count = 0;
   
   void event_subscribe(EventType type, EventCallback callback, void *context) {
       if (subscription_count < MAX_SUBSCRIPTIONS) {
           subscriptions[subscription_count].type = type;
           subscriptions[subscription_count].callback = callback;
           subscriptions[subscription_count].context = context;
           subscription_count++;
       }
   }
   
   void event_dispatch(EventType type, void *data) {
       for (size_t i = 0; i < subscription_count; i++) {
           if (subscriptions[i].type == type) {
               subscriptions[i].callback(data);
           }
       }
   }
   
   // Usage
   void on_button_press(void *context) {
       // Handle button press
   }
   
   void setup(void) {
       event_subscribe(EVENT_BUTTON_PRESS, on_button_press, NULL);
   }

Component-Based Architecture
=============================

Component Interface
-------------------

.. code-block:: c

   // Generic component interface
   typedef struct Component Component;
   
   typedef struct {
       int (*init)(Component *self);
       int (*start)(Component *self);
       int (*stop)(Component *self);
       int (*process)(Component *self);
       void (*destroy)(Component *self);
   } ComponentVTable;
   
   struct Component {
       const ComponentVTable *vtable;
       void *private_data;
       const char *name;
   };
   
   // Helper macros
   #define COMPONENT_INIT(comp)    (comp)->vtable->init(comp)
   #define COMPONENT_START(comp)   (comp)->vtable->start(comp)
   #define COMPONENT_STOP(comp)    (comp)->vtable->stop(comp)
   #define COMPONENT_PROCESS(comp) (comp)->vtable->process(comp)
   #define COMPONENT_DESTROY(comp) (comp)->vtable->destroy(comp)

Example: Sensor Component
--------------------------

.. code-block:: c

   // Sensor component
   typedef struct {
       Component base;
       uint8_t i2c_address;
       float last_reading;
       bool initialized;
   } SensorComponent;
   
   static int sensor_init(Component *self) {
       SensorComponent *sensor = (SensorComponent *)self;
       
       // Initialize I2C
       i2c_init();
       
       // Configure sensor
       uint8_t config[] = {REG_CONFIG, CONFIG_VALUE};
       i2c_write(sensor->i2c_address, config, sizeof(config));
       
       sensor->initialized = true;
       return 0;
   }
   
   static int sensor_start(Component *self) {
       SensorComponent *sensor = (SensorComponent *)self;
       
       // Start continuous measurement
       uint8_t cmd[] = {REG_CTRL, CTRL_START};
       i2c_write(sensor->i2c_address, cmd, sizeof(cmd));
       
       return 0;
   }
   
   static int sensor_process(Component *self) {
       SensorComponent *sensor = (SensorComponent *)self;
       
       // Read sensor value
       uint8_t reg = REG_DATA;
       uint8_t data[2];
       i2c_write_read(sensor->i2c_address, &reg, 1, data, 2);
       
       sensor->last_reading = (data[0] << 8 | data[1]) * SCALE_FACTOR;
       
       // Post event with reading
       event_post(EVENT_DATA_READY, &sensor->last_reading);
       
       return 0;
   }
   
   static const ComponentVTable sensor_vtable = {
       .init = sensor_init,
       .start = sensor_start,
       .stop = sensor_stop,
       .process = sensor_process,
       .destroy = sensor_destroy
   };
   
   Component *sensor_create(uint8_t i2c_addr) {
       SensorComponent *sensor = malloc(sizeof(SensorComponent));
       sensor->base.vtable = &sensor_vtable;
       sensor->base.name = "Temperature Sensor";
       sensor->i2c_address = i2c_addr;
       sensor->initialized = false;
       return &sensor->base;
   }

Component Manager
-----------------

.. code-block:: c

   // Component manager
   typedef struct {
       Component *components[MAX_COMPONENTS];
       size_t count;
   } ComponentManager;
   
   void manager_add_component(ComponentManager *mgr, Component *comp) {
       if (mgr->count < MAX_COMPONENTS) {
           mgr->components[mgr->count++] = comp;
       }
   }
   
   void manager_init_all(ComponentManager *mgr) {
       for (size_t i = 0; i < mgr->count; i++) {
           COMPONENT_INIT(mgr->components[i]);
       }
   }
   
   void manager_start_all(ComponentManager *mgr) {
       for (size_t i = 0; i < mgr->count; i++) {
           COMPONENT_START(mgr->components[i]);
       }
   }
   
   void manager_process_all(ComponentManager *mgr) {
       for (size_t i = 0; i < mgr->count; i++) {
           COMPONENT_PROCESS(mgr->components[i]);
       }
   }
   
   // Usage
   int main(void) {
       ComponentManager manager = {0};
       
       manager_add_component(&manager, sensor_create(0x48));
       manager_add_component(&manager, display_create());
       manager_add_component(&manager, communication_create());
       
       manager_init_all(&manager);
       manager_start_all(&manager);
       
       while (1) {
           manager_process_all(&manager);
           delay_ms(10);
       }
   }

Pipe-and-Filter Architecture
=============================

Data Processing Pipeline
------------------------

.. code-block:: c

   // Filter interface
   typedef struct Filter Filter;
   typedef int (*FilterProcess_fn)(Filter *self, void *input, void *output);
   
   struct Filter {
       FilterProcess_fn process;
       Filter *next;
       void *context;
   };
   
   // Pipeline
   typedef struct {
       Filter *first;
       Filter *last;
   } Pipeline;
   
   void pipeline_add_filter(Pipeline *pipe, Filter *filter) {
       if (pipe->first == NULL) {
           pipe->first = filter;
           pipe->last = filter;
       } else {
           pipe->last->next = filter;
           pipe->last = filter;
       }
       filter->next = NULL;
   }
   
   int pipeline_process(Pipeline *pipe, void *input, void *output) {
       Filter *filter = pipe->first;
       void *data = input;
       void *temp_output;
       
       while (filter) {
           if (filter->next) {
               temp_output = malloc(BUFFER_SIZE);  // Or use stack/pool
           } else {
               temp_output = output;
           }
           
           int result = filter->process(filter, data, temp_output);
           
           if (result != 0) {
               return result;  // Error
           }
           
           if (data != input) {
               free(data);  // Clean up intermediate buffer
           }
           
           data = temp_output;
           filter = filter->next;
       }
       
       return 0;
   }

Example: ADC Signal Processing
-------------------------------

.. code-block:: c

   // Filter 1: DC offset removal
   int dc_offset_filter(Filter *self, void *input, void *output) {
       int16_t *in = (int16_t *)input;
       int16_t *out = (int16_t *)output;
       
       int32_t sum = 0;
       for (int i = 0; i < SAMPLE_COUNT; i++) {
           sum += in[i];
       }
       int16_t offset = sum / SAMPLE_COUNT;
       
       for (int i = 0; i < SAMPLE_COUNT; i++) {
           out[i] = in[i] - offset;
       }
       
       return 0;
   }
   
   // Filter 2: Low-pass filter
   int lowpass_filter(Filter *self, void *input, void *output) {
       int16_t *in = (int16_t *)input;
       int16_t *out = (int16_t *)output;
       
       // Simple moving average
       for (int i = 0; i < SAMPLE_COUNT; i++) {
           int32_t sum = 0;
           for (int j = -WINDOW/2; j <= WINDOW/2; j++) {
               int idx = i + j;
               if (idx >= 0 && idx < SAMPLE_COUNT) {
                   sum += in[idx];
               }
           }
           out[i] = sum / WINDOW;
       }
       
       return 0;
   }
   
   // Filter 3: Peak detection
   int peak_detection_filter(Filter *self, void *input, void *output) {
       int16_t *in = (int16_t *)input;
       Peak *peaks = (Peak *)output;
       int peak_count = 0;
       
       for (int i = 1; i < SAMPLE_COUNT - 1; i++) {
           if (in[i] > in[i-1] && in[i] > in[i+1] && in[i] > THRESHOLD) {
               peaks[peak_count].index = i;
               peaks[peak_count].value = in[i];
               peak_count++;
           }
       }
       
       return peak_count;
   }
   
   // Build pipeline
   Pipeline signal_pipeline;
   Filter dc_filter = {.process = dc_offset_filter};
   Filter lp_filter = {.process = lowpass_filter};
   Filter peak_filter = {.process = peak_detection_filter};
   
   pipeline_add_filter(&signal_pipeline, &dc_filter);
   pipeline_add_filter(&signal_pipeline, &lp_filter);
   pipeline_add_filter(&signal_pipeline, &peak_filter);
   
   // Use pipeline
   int16_t samples[SAMPLE_COUNT];
   Peak peaks[MAX_PEAKS];
   
   adc_read_samples(samples, SAMPLE_COUNT);
   int num_peaks = pipeline_process(&signal_pipeline, samples, peaks);

Model-View-Controller (MVC)
============================

Embedded MVC Pattern
--------------------

.. code-block:: c

   // Model: Data and business logic
   typedef struct {
       float temperature;
       float humidity;
       uint32_t timestamp;
       bool alarm_active;
   } SensorModel;
   
   void model_update_temperature(SensorModel *model, float temp) {
       model->temperature = temp;
       model->timestamp = get_timestamp();
       
       if (temp > ALARM_THRESHOLD) {
           model->alarm_active = true;
       }
       
       // Notify views
       view_notify_update();
   }
   
   // View: Display representation
   typedef struct {
       SensorModel *model;
       LCD_Handle *lcd;
   } LCDView;
   
   void view_update(LCDView *view) {
       char buffer[32];
       
       lcd_clear(view->lcd);
       
       snprintf(buffer, sizeof(buffer), "Temp: %.1fC", view->model->temperature);
       lcd_write_string(view->lcd, 0, 0, buffer);
       
       snprintf(buffer, sizeof(buffer), "Hum: %.1f%%", view->model->humidity);
       lcd_write_string(view->lcd, 0, 1, buffer);
       
       if (view->model->alarm_active) {
           lcd_write_string(view->lcd, 0, 2, "ALARM!");
       }
   }
   
   // Controller: User input handling
   typedef struct {
       SensorModel *model;
       LCDView *view;
   } Controller;
   
   void controller_button_pressed(Controller *ctrl, uint8_t button) {
       switch (button) {
       case BUTTON_RESET:
           ctrl->model->alarm_active = false;
           view_update(ctrl->view);
           break;
           
       case BUTTON_REFRESH:
           // Trigger sensor reading
           sensor_read_values();
           break;
       }
   }

Best Practices
==============

1. **Use layers** - separate concerns clearly
2. **Define interfaces** - use HAL for hardware abstraction
3. **Keep layers independent** - minimize dependencies
4. **Event-driven when possible** - responsive and efficient
5. **Component-based design** - modular and testable
6. **Clear component interfaces** - well-defined APIs
7. **Pipeline for data processing** - clean data flow
8. **Separate model from view** - easier testing
9. **Document architecture** - diagrams and descriptions
10. **Test each layer** - unit and integration tests

Common Pitfalls
===============

1. **Layer violations** - bypassing layers for "efficiency"
2. **God objects** - components doing too much
3. **Tight coupling** - hard to test and reuse
4. **No abstraction** - hardware-specific code everywhere
5. **Event queue overflow** - not handling events fast enough
6. **Circular dependencies** - components depending on each other
7. **Monolithic design** - everything in main()

Quick Reference
===============

.. code-block:: c

   // Layered architecture
   Application → Middleware → Drivers → HAL → Hardware
   
   // Event-driven
   event_post(EVENT_BUTTON_PRESS, NULL);
   event_get(&event);
   
   // Component-based
   Component *comp = sensor_create(0x48);
   COMPONENT_INIT(comp);
   COMPONENT_PROCESS(comp);
   
   // Pipeline
   pipeline_add_filter(&pipe, &filter);
   pipeline_process(&pipe, input, output);

See Also
========

- Embedded_Design_Patterns_Structural.rst
- Embedded_Design_Patterns_Behavioral.rst
- Embedded_State_Machines.rst
- Embedded_Testing_Strategies.rst

References
==========

- Making Embedded Systems (Elecia White, O'Reilly)
- Design Patterns for Embedded Systems in C (Bruce Powel Douglass)
- Clean Architecture (Robert C. Martin)
- Embedded Software Development with C (Kai Qian)
