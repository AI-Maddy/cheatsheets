=============================================
Embedded Design Patterns - Behavioral
=============================================

:Author: Embedded Systems Design Patterns Documentation
:Date: January 2026
:Version: 1.0
:Focus: Behavioral design patterns for embedded systems

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Behavioral Patterns Overview
-----------------------------

.. code-block:: text

   Behavioral Patterns:
   
   1. Observer (Publish-Subscribe)
      - Event notification
      - Loose coupling
   
   2. Strategy
      - Algorithm selection at runtime
      - Replaces switch/if-else
   
   3. Command
      - Encapsulate requests
      - Queue, log, undo operations
   
   4. Chain of Responsibility
      - Pass request through handlers
      - Dynamic handler selection
   
   5. Template Method
      - Define algorithm skeleton
      - Subclasses override steps

Observer Pattern
================

Intent
------

Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.

Structure
---------

.. code-block:: c

   // Observer interface
   typedef struct Observer Observer;
   typedef void (*Observer_Update_fn)(Observer *self, void *data);
   
   struct Observer {
       Observer_Update_fn update;
       void *context;
   };
   
   // Subject
   typedef struct {
       Observer *observers[MAX_OBSERVERS];
       uint8_t observer_count;
   } Subject;
   
   void Subject_Init(Subject *self) {
       self->observer_count = 0;
   }
   
   void Subject_Attach(Subject *self, Observer *observer) {
       if (self->observer_count < MAX_OBSERVERS) {
           self->observers[self->observer_count++] = observer;
       }
   }
   
   void Subject_Detach(Subject *self, Observer *observer) {
       for (uint8_t i = 0; i < self->observer_count; i++) {
           if (self->observers[i] == observer) {
               // Shift remaining observers
               for (uint8_t j = i; j < self->observer_count - 1; j++) {
                   self->observers[j] = self->observers[j + 1];
               }
               self->observer_count--;
               break;
           }
       }
   }
   
   void Subject_Notify(Subject *self, void *data) {
       for (uint8_t i = 0; i < self->observer_count; i++) {
           self->observers[i]->update(self->observers[i], data);
       }
   }

Example: Temperature Sensor
----------------------------

.. code-block:: c

   // Temperature sensor (Subject)
   typedef struct {
       Subject subject;
       float temperature;
   } TemperatureSensor;
   
   void TemperatureSensor_Init(TemperatureSensor *self) {
       Subject_Init(&self->subject);
       self->temperature = 0.0f;
   }
   
   void TemperatureSensor_SetTemperature(TemperatureSensor *self, float temp) {
       self->temperature = temp;
       Subject_Notify(&self->subject, &self->temperature);
   }
   
   // Display observer
   typedef struct {
       Observer observer;
   } DisplayObserver;
   
   void Display_Update(Observer *self, void *data) {
       float temp = *(float *)data;
       LCD_Printf("Temperature: %.1f C\n", temp);
   }
   
   void DisplayObserver_Init(DisplayObserver *self) {
       self->observer.update = Display_Update;
       self->observer.context = self;
   }
   
   // Logger observer
   typedef struct {
       Observer observer;
       FILE *log_file;
   } LoggerObserver;
   
   void Logger_Update(Observer *self, void *data) {
       LoggerObserver *logger = (LoggerObserver *)self->context;
       float temp = *(float *)data;
       fprintf(logger->log_file, "%lu,%.2f\n", get_timestamp(), temp);
   }
   
   // Alarm observer
   typedef struct {
       Observer observer;
       float threshold;
   } AlarmObserver;
   
   void Alarm_Update(Observer *self, void *data) {
       AlarmObserver *alarm = (AlarmObserver *)self->context;
       float temp = *(float *)data;
       
       if (temp > alarm->threshold) {
           activate_alarm();
       }
   }

Usage
-----

.. code-block:: c

   int main(void) {
       TemperatureSensor sensor;
       DisplayObserver display;
       LoggerObserver logger;
       AlarmObserver alarm;
       
       TemperatureSensor_Init(&sensor);
       DisplayObserver_Init(&display);
       alarm.threshold = 50.0f;
       
       // Attach observers
       Subject_Attach(&sensor.subject, &display.observer);
       Subject_Attach(&sensor.subject, &logger.observer);
       Subject_Attach(&sensor.subject, &alarm.observer);
       
       // Update temperature - all observers notified
       TemperatureSensor_SetTemperature(&sensor, 45.2f);
   }

Event-Driven Observer
---------------------

.. code-block:: c

   // Event types
   typedef enum {
       EVENT_BUTTON_PRESSED,
       EVENT_BUTTON_RELEASED,
       EVENT_TIMER_EXPIRED,
       EVENT_DATA_RECEIVED
   } EventType;
   
   typedef struct {
       EventType type;
       void *data;
       size_t data_size;
   } Event;
   
   typedef void (*EventHandler_fn)(const Event *event, void *context);
   
   typedef struct {
       EventType event_type;
       EventHandler_fn handler;
       void *context;
   } EventSubscription;
   
   typedef struct {
       EventSubscription subscriptions[MAX_SUBSCRIPTIONS];
       uint8_t count;
   } EventDispatcher;
   
   void EventDispatcher_Subscribe(EventDispatcher *self, EventType type,
                                   EventHandler_fn handler, void *context) {
       if (self->count < MAX_SUBSCRIPTIONS) {
           self->subscriptions[self->count].event_type = type;
           self->subscriptions[self->count].handler = handler;
           self->subscriptions[self->count].context = context;
           self->count++;
       }
   }
   
   void EventDispatcher_Publish(EventDispatcher *self, const Event *event) {
       for (uint8_t i = 0; i < self->count; i++) {
           if (self->subscriptions[i].event_type == event->type) {
               self->subscriptions[i].handler(event,
                                             self->subscriptions[i].context);
           }
       }
   }

Strategy Pattern
================

Intent
------

Define a family of algorithms, encapsulate each one, and make them interchangeable.

Structure
---------

.. code-block:: c

   // Strategy interface
   typedef struct {
       int (*compress)(const uint8_t *input, size_t input_len,
                      uint8_t *output, size_t *output_len);
       int (*decompress)(const uint8_t *input, size_t input_len,
                        uint8_t *output, size_t *output_len);
   } CompressionStrategy;
   
   // RLE compression strategy
   int RLE_Compress(const uint8_t *input, size_t input_len,
                    uint8_t *output, size_t *output_len) {
       size_t out_idx = 0;
       size_t i = 0;
       
       while (i < input_len) {
           uint8_t byte = input[i];
           uint8_t count = 1;
           
           while (i + count < input_len && input[i + count] == byte && count < 255) {
               count++;
           }
           
           output[out_idx++] = count;
           output[out_idx++] = byte;
           i += count;
       }
       
       *output_len = out_idx;
       return 0;
   }
   
   CompressionStrategy RLE_Strategy = {
       .compress = RLE_Compress,
       .decompress = RLE_Decompress
   };
   
   // LZ77 compression strategy
   CompressionStrategy LZ77_Strategy = {
       .compress = LZ77_Compress,
       .decompress = LZ77_Decompress
   };
   
   // Huffman compression strategy
   CompressionStrategy Huffman_Strategy = {
       .compress = Huffman_Compress,
       .decompress = Huffman_Decompress
   };
   
   // Context using strategy
   typedef struct {
       CompressionStrategy *strategy;
   } DataCompressor;
   
   void DataCompressor_SetStrategy(DataCompressor *self, CompressionStrategy *strategy) {
       self->strategy = strategy;
   }
   
   int DataCompressor_Compress(DataCompressor *self, const uint8_t *input, size_t input_len,
                                uint8_t *output, size_t *output_len) {
       return self->strategy->compress(input, input_len, output, output_len);
   }

Example: Motor Control
----------------------

.. code-block:: c

   // Motor control strategy
   typedef struct {
       void (*set_speed)(int speed);
       void (*set_direction)(bool forward);
       int (*get_current)(void);
   } MotorControlStrategy;
   
   // PWM strategy
   void PWM_SetSpeed(int speed) {
       TIM1->CCR1 = speed;  // 0-100%
   }
   
   void PWM_SetDirection(bool forward) {
       if (forward) {
           GPIO_SetHigh(DIR_PIN);
       } else {
           GPIO_SetLow(DIR_PIN);
       }
   }
   
   MotorControlStrategy PWM_Strategy = {
       .set_speed = PWM_SetSpeed,
       .set_direction = PWM_SetDirection,
       .get_current = ADC_ReadMotorCurrent
   };
   
   // H-Bridge strategy
   void HBridge_SetSpeed(int speed) {
       if (speed >= 0) {
           GPIO_SetHigh(IN1_PIN);
           GPIO_SetLow(IN2_PIN);
           TIM1->CCR1 = speed;
       } else {
           GPIO_SetLow(IN1_PIN);
           GPIO_SetHigh(IN2_PIN);
           TIM1->CCR1 = -speed;
       }
   }
   
   // Motor controller
   typedef struct {
       MotorControlStrategy *strategy;
   } MotorController;
   
   void MotorController_Init(MotorController *self, MotorControlStrategy *strategy) {
       self->strategy = strategy;
   }
   
   void MotorController_Run(MotorController *self, int speed, bool forward) {
       self->strategy->set_direction(forward);
       self->strategy->set_speed(speed);
   }

Command Pattern
===============

Intent
------

Encapsulate a request as an object, allowing parameterization and queuing of requests.

Structure
---------

.. code-block:: c

   // Command interface
   typedef struct Command Command;
   typedef void (*Command_Execute_fn)(Command *self);
   typedef void (*Command_Undo_fn)(Command *self);
   
   struct Command {
       Command_Execute_fn execute;
       Command_Undo_fn undo;
       void *context;
   };
   
   // LED command
   typedef struct {
       Command base;
       GPIO_Pin *led;
       bool previous_state;
   } LED_Command;
   
   void LED_Command_Execute(Command *self) {
       LED_Command *cmd = (LED_Command *)self;
       cmd->previous_state = GPIO_Read(cmd->led);
       GPIO_Toggle(cmd->led);
   }
   
   void LED_Command_Undo(Command *self) {
       LED_Command *cmd = (LED_Command *)self;
       GPIO_Write(cmd->led, cmd->previous_state);
   }
   
   Command *LED_Command_Create(GPIO_Pin *led) {
       LED_Command *cmd = malloc(sizeof(LED_Command));
       cmd->base.execute = LED_Command_Execute;
       cmd->base.undo = LED_Command_Undo;
       cmd->led = led;
       return &cmd->base;
   }

Command Queue
-------------

.. code-block:: c

   // Command queue
   typedef struct {
       Command *commands[QUEUE_SIZE];
       uint8_t head;
       uint8_t tail;
       uint8_t count;
   } CommandQueue;
   
   void CommandQueue_Init(CommandQueue *self) {
       self->head = 0;
       self->tail = 0;
       self->count = 0;
   }
   
   bool CommandQueue_Enqueue(CommandQueue *self, Command *cmd) {
       if (self->count >= QUEUE_SIZE) {
           return false;
       }
       
       self->commands[self->tail] = cmd;
       self->tail = (self->tail + 1) % QUEUE_SIZE;
       self->count++;
       return true;
   }
   
   Command *CommandQueue_Dequeue(CommandQueue *self) {
       if (self->count == 0) {
           return NULL;
       }
       
       Command *cmd = self->commands[self->head];
       self->head = (self->head + 1) % QUEUE_SIZE;
       self->count--;
       return cmd;
   }
   
   // Command processor
   void CommandQueue_Process(CommandQueue *self) {
       Command *cmd = CommandQueue_Dequeue(self);
       if (cmd) {
           cmd->execute(cmd);
       }
   }

Example: Protocol Commands
---------------------------

.. code-block:: c

   // Write register command
   typedef struct {
       Command base;
       uint8_t device_addr;
       uint8_t reg_addr;
       uint8_t value;
   } WriteRegisterCommand;
   
   void WriteRegister_Execute(Command *self) {
       WriteRegisterCommand *cmd = (WriteRegisterCommand *)self;
       I2C_WriteRegister(cmd->device_addr, cmd->reg_addr, cmd->value);
   }
   
   // Read register command
   typedef struct {
       Command base;
       uint8_t device_addr;
       uint8_t reg_addr;
       uint8_t *result;
   } ReadRegisterCommand;
   
   void ReadRegister_Execute(Command *self) {
       ReadRegisterCommand *cmd = (ReadRegisterCommand *)self;
       *cmd->result = I2C_ReadRegister(cmd->device_addr, cmd->reg_addr);
   }
   
   // Delay command
   typedef struct {
       Command base;
       uint32_t delay_ms;
   } DelayCommand;
   
   void Delay_Execute(Command *self) {
       DelayCommand *cmd = (DelayCommand *)self;
       delay_ms(cmd->delay_ms);
   }

Usage
-----

.. code-block:: c

   // Create command sequence for device initialization
   CommandQueue init_sequence;
   CommandQueue_Init(&init_sequence);
   
   // Queue commands
   CommandQueue_Enqueue(&init_sequence, CreateWriteRegCmd(0x50, 0x00, 0x80));
   CommandQueue_Enqueue(&init_sequence, CreateDelayCmd(100));
   CommandQueue_Enqueue(&init_sequence, CreateWriteRegCmd(0x50, 0x01, 0xFF));
   
   // Execute sequence
   while (init_sequence.count > 0) {
       CommandQueue_Process(&init_sequence);
   }

Chain of Responsibility
========================

Intent
------

Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.

Structure
---------

.. code-block:: c

   // Handler interface
   typedef struct Handler Handler;
   typedef bool (*Handler_Handle_fn)(Handler *self, void *request);
   
   struct Handler {
       Handler_Handle_fn handle;
       Handler *next;
       void *context;
   };
   
   void Handler_SetNext(Handler *self, Handler *next) {
       self->next = next;
   }
   
   bool Handler_Process(Handler *self, void *request) {
       if (self->handle(self, request)) {
           return true;  // Handled
       }
       
       if (self->next) {
           return Handler_Process(self->next, request);
       }
       
       return false;  // Not handled
   }

Example: Message Processing
----------------------------

.. code-block:: c

   // Message types
   typedef enum {
       MSG_TYPE_CONTROL,
       MSG_TYPE_DATA,
       MSG_TYPE_STATUS
   } MessageType;
   
   typedef struct {
       MessageType type;
       uint8_t *payload;
       size_t length;
   } Message;
   
   // Control message handler
   typedef struct {
       Handler base;
   } ControlHandler;
   
   bool ControlHandler_Handle(Handler *self, void *request) {
       Message *msg = (Message *)request;
       
       if (msg->type == MSG_TYPE_CONTROL) {
           // Process control message
           process_control_message(msg->payload, msg->length);
           return true;
       }
       
       return false;  // Not handled, pass to next
   }
   
   void ControlHandler_Init(ControlHandler *self) {
       self->base.handle = ControlHandler_Handle;
       self->base.next = NULL;
   }
   
   // Data message handler
   typedef struct {
       Handler base;
   } DataHandler;
   
   bool DataHandler_Handle(Handler *self, void *request) {
       Message *msg = (Message *)request;
       
       if (msg->type == MSG_TYPE_DATA) {
           process_data_message(msg->payload, msg->length);
           return true;
       }
       
       return false;
   }
   
   // Status message handler
   typedef struct {
       Handler base;
   } StatusHandler;
   
   bool StatusHandler_Handle(Handler *self, void *request) {
       Message *msg = (Message *)request;
       
       if (msg->type == MSG_TYPE_STATUS) {
           process_status_message(msg->payload, msg->length);
           return true;
       }
       
       return false;
   }
   
   // Unknown message handler (catch-all)
   typedef struct {
       Handler base;
   } UnknownHandler;
   
   bool UnknownHandler_Handle(Handler *self, void *request) {
       Message *msg = (Message *)request;
       log_error("Unknown message type: %d", msg->type);
       return true;  // Always handles (end of chain)
   }

Usage
-----

.. code-block:: c

   int main(void) {
       ControlHandler control;
       DataHandler data;
       StatusHandler status;
       UnknownHandler unknown;
       
       ControlHandler_Init(&control);
       DataHandler_Init(&data);
       StatusHandler_Init(&status);
       UnknownHandler_Init(&unknown);
       
       // Build chain
       Handler_SetNext(&control.base, &data.base);
       Handler_SetNext(&data.base, &status.base);
       Handler_SetNext(&status.base, &unknown.base);
       
       // Process message - will traverse chain until handled
       Message msg = {MSG_TYPE_DATA, payload, length};
       Handler_Process(&control.base, &msg);
   }

Template Method Pattern
========================

Intent
------

Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.

Structure
---------

.. code-block:: c

   // Base sensor class
   typedef struct Sensor Sensor;
   
   typedef void (*Sensor_PowerOn_fn)(Sensor *self);
   typedef void (*Sensor_Configure_fn)(Sensor *self);
   typedef uint32_t (*Sensor_ReadRaw_fn)(Sensor *self);
   typedef float (*Sensor_Convert_fn)(Sensor *self, uint32_t raw);
   typedef void (*Sensor_PowerOff_fn)(Sensor *self);
   
   struct Sensor {
       Sensor_PowerOn_fn power_on;
       Sensor_Configure_fn configure;
       Sensor_ReadRaw_fn read_raw;
       Sensor_Convert_fn convert;
       Sensor_PowerOff_fn power_off;
       void *context;
   };
   
   // Template method
   float Sensor_Read(Sensor *self) {
       self->power_on(self);
       self->configure(self);
       
       uint32_t raw = self->read_raw(self);
       float value = self->convert(self, raw);
       
       self->power_off(self);
       
       return value;
   }
   
   // ADC temperature sensor
   typedef struct {
       Sensor base;
       ADC_TypeDef *adc;
       uint8_t channel;
   } ADC_TempSensor;
   
   void ADC_TempSensor_PowerOn(Sensor *self) {
       ADC_TempSensor *sensor = (ADC_TempSensor *)self;
       ADC_Enable(sensor->adc);
   }
   
   void ADC_TempSensor_Configure(Sensor *self) {
       ADC_TempSensor *sensor = (ADC_TempSensor *)self;
       ADC_SelectChannel(sensor->adc, sensor->channel);
       ADC_SetSampleTime(sensor->adc, ADC_SAMPLE_480_CYCLES);
   }
   
   uint32_t ADC_TempSensor_ReadRaw(Sensor *self) {
       ADC_TempSensor *sensor = (ADC_TempSensor *)self;
       ADC_StartConversion(sensor->adc);
       while (!ADC_ConversionComplete(sensor->adc));
       return ADC_ReadValue(sensor->adc);
   }
   
   float ADC_TempSensor_Convert(Sensor *self, uint32_t raw) {
       // Convert ADC value to temperature
       float voltage = (raw * 3.3f) / 4095.0f;
       float temp = (voltage - 0.76f) / 0.0025f + 25.0f;
       return temp;
   }
   
   void ADC_TempSensor_PowerOff(Sensor *self) {
       ADC_TempSensor *sensor = (ADC_TempSensor *)self;
       ADC_Disable(sensor->adc);
   }
   
   // I2C temperature sensor
   typedef struct {
       Sensor base;
       uint8_t i2c_addr;
   } I2C_TempSensor;
   
   void I2C_TempSensor_PowerOn(Sensor *self) {
       I2C_TempSensor *sensor = (I2C_TempSensor *)self;
       I2C_WriteRegister(sensor->i2c_addr, PWR_REG, PWR_ON);
   }
   
   void I2C_TempSensor_Configure(Sensor *self) {
       I2C_TempSensor *sensor = (I2C_TempSensor *)self;
       I2C_WriteRegister(sensor->i2c_addr, CFG_REG, CFG_12BIT);
   }
   
   uint32_t I2C_TempSensor_ReadRaw(Sensor *self) {
       I2C_TempSensor *sensor = (I2C_TempSensor *)self;
       return I2C_ReadRegister16(sensor->i2c_addr, TEMP_REG);
   }
   
   float I2C_TempSensor_Convert(Sensor *self, uint32_t raw) {
       // Sensor-specific conversion
       return raw * 0.0625f;
   }

Best Practices
==============

1. **Use observer** for event notification and decoupling
2. **Use strategy** to replace complex switch/if-else
3. **Use command** for queuing, logging, undo
4. **Use chain of responsibility** for flexible message routing
5. **Use template method** for common algorithm structure
6. **Keep patterns simple** - don't over-engineer
7. **Consider memory** - patterns use heap/function pointers
8. **Document intent** clearly
9. **Test patterns** thoroughly
10. **Profile performance** if used in critical paths

Common Pitfalls
===============

1. **Memory leaks** - forgetting to free command objects
2. **Stack overflow** - deep chains of responsibility
3. **Observer overhead** - too many observers
4. **Null pointers** - not checking function pointers
5. **Circular dependencies** - observers observing each other

Quick Reference
===============

.. code-block:: c

   // Observer
   Subject_Attach(&subject, &observer);
   Subject_Notify(&subject, data);
   
   // Strategy
   compressor.strategy = &RLE_Strategy;
   compressor.strategy->compress(input, len, output, &out_len);
   
   // Command
   CommandQueue_Enqueue(&queue, cmd);
   CommandQueue_Process(&queue);
   
   // Chain of Responsibility
   Handler_Process(&first_handler, &request);
   
   // Template Method
   float value = Sensor_Read(&sensor);

See Also
========

- Embedded_Design_Patterns_Structural.rst
- Embedded_State_Machines.rst
- Embedded_Design_Patterns_Concurrency.rst

References
==========

- Design Patterns for Embedded Systems in C (Bruce Powel Douglass)
- Gang of Four Design Patterns
- Embedded C Coding Standard
