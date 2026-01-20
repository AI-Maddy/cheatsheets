=============================================
Embedded Testing Strategies
=============================================

:Author: Embedded Systems Design Documentation
:Date: January 2026
:Version: 1.0
:Focus: Testing strategies and methodologies for embedded systems
:Source: Making Embedded Systems (Elecia White) + industry practices

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Testing Pyramid
----------------

.. code-block:: text

   Testing Levels (Bottom to Top):
   
   1. Unit Tests (70%)
      - Test individual functions
      - Mock dependencies
      - Fast, automated
   
   2. Integration Tests (20%)
      - Test component interactions
      - Hardware abstraction
      - Moderate speed
   
   3. System Tests (10%)
      - End-to-end testing
      - Real hardware
      - Slow, manual/automated
   
   Testing Types:
   - White-box (code coverage)
   - Black-box (requirements)
   - Hardware-in-the-Loop (HIL)
   - Regression testing

Unit Testing
============

Test Framework Setup
--------------------

.. code-block:: c

   // Unity test framework example
   #include "unity.h"
   
   void setUp(void) {
       // Run before each test
   }
   
   void tearDown(void) {
       // Run after each test
   }
   
   // Test case
   void test_buffer_initialization(void) {
       Buffer buf;
       buffer_init(&buf, 256);
       
       TEST_ASSERT_EQUAL(0, buf.count);
       TEST_ASSERT_EQUAL(256, buf.size);
       TEST_ASSERT_NOT_NULL(buf.data);
   }
   
   void test_buffer_write_read(void) {
       Buffer buf;
       buffer_init(&buf, 256);
       
       uint8_t data[] = {0x12, 0x34, 0x56};
       buffer_write(&buf, data, sizeof(data));
       
       TEST_ASSERT_EQUAL(3, buf.count);
       
       uint8_t read_data[3];
       buffer_read(&buf, read_data, sizeof(read_data));
       
       TEST_ASSERT_EQUAL_UINT8_ARRAY(data, read_data, 3);
   }
   
   void test_buffer_overflow(void) {
       Buffer buf;
       buffer_init(&buf, 4);
       
       uint8_t data[8] = {0};
       int result = buffer_write(&buf, data, sizeof(data));
       
       TEST_ASSERT_EQUAL(-1, result);  // Should fail
   }
   
   int main(void) {
       UNITY_BEGIN();
       RUN_TEST(test_buffer_initialization);
       RUN_TEST(test_buffer_write_read);
       RUN_TEST(test_buffer_overflow);
       return UNITY_END();
   }

Mocking Hardware
----------------

.. code-block:: c

   // HAL mock for testing
   typedef struct {
       GPIO_PinState expected_state;
       GPIO_Pin expected_pin;
       int call_count;
   } GPIO_Mock;
   
   static GPIO_Mock gpio_mock;
   
   void GPIO_Mock_Init(void) {
       memset(&gpio_mock, 0, sizeof(gpio_mock));
   }
   
   void GPIO_Mock_ExpectWrite(GPIO_Pin pin, GPIO_PinState state) {
       gpio_mock.expected_pin = pin;
       gpio_mock.expected_state = state;
   }
   
   // Mock implementation
   void HAL_GPIO_WritePin(GPIO_TypeDef *port, uint16_t pin, GPIO_PinState state) {
       gpio_mock.call_count++;
       TEST_ASSERT_EQUAL(gpio_mock.expected_pin, pin);
       TEST_ASSERT_EQUAL(gpio_mock.expected_state, state);
   }
   
   // Test using mock
   void test_led_on(void) {
       GPIO_Mock_Init();
       GPIO_Mock_ExpectWrite(LED_PIN, GPIO_PIN_SET);
       
       led_on();
       
       TEST_ASSERT_EQUAL(1, gpio_mock.call_count);
   }

Dependency Injection
--------------------

.. code-block:: c

   // Interface for hardware abstraction
   typedef struct {
       int (*init)(void);
       int (*read)(uint8_t *data, size_t len);
       int (*write)(const uint8_t *data, size_t len);
   } UART_Interface;
   
   // Production implementation
   static int uart_hw_init(void) {
       HAL_UART_Init(&huart1);
       return 0;
   }
   
   static const UART_Interface uart_hardware = {
       .init = uart_hw_init,
       .read = uart_hw_read,
       .write = uart_hw_write
   };
   
   // Test mock implementation
   static uint8_t mock_buffer[256];
   static size_t mock_len = 0;
   
   static int uart_mock_write(const uint8_t *data, size_t len) {
       memcpy(mock_buffer, data, len);
       mock_len = len;
       return len;
   }
   
   static const UART_Interface uart_mock = {
       .init = NULL,
       .read = NULL,
       .write = uart_mock_write
   };
   
   // Code under test uses interface
   void send_message(const UART_Interface *uart, const char *msg) {
       uart->write((const uint8_t *)msg, strlen(msg));
   }
   
   // Test
   void test_send_message(void) {
       send_message(&uart_mock, "Hello");
       
       TEST_ASSERT_EQUAL(5, mock_len);
       TEST_ASSERT_EQUAL_STRING("Hello", mock_buffer);
   }

Code Coverage
=============

GCC Coverage Setup
------------------

.. code-block:: makefile

   # Makefile for coverage
   CFLAGS += -fprofile-arcs -ftest-coverage
   LDFLAGS += -lgcov --coverage
   
   # Run tests
   test: test.elf
   \t./test.elf
   \tlcov --capture --directory . --output-file coverage.info
   \tgenhtml coverage.info --output-directory coverage_html
   
   clean:
   \trm -f *.gcda *.gcno *.gcov coverage.info
   \trm -rf coverage_html

Coverage Analysis
-----------------

.. code-block:: c

   // Function with branches to test
   int process_command(uint8_t cmd, uint8_t *data) {
       switch (cmd) {
       case CMD_READ:
           return handle_read(data);
           
       case CMD_WRITE:
           return handle_write(data);
           
       case CMD_STATUS:
           return handle_status(data);
           
       default:
           return -1;  // Error
       }
   }
   
   // Tests should cover all branches
   void test_process_command_read(void) {
       uint8_t data[8];
       int result = process_command(CMD_READ, data);
       TEST_ASSERT_EQUAL(0, result);
   }
   
   void test_process_command_write(void) {
       uint8_t data[8] = {0x12, 0x34};
       int result = process_command(CMD_WRITE, data);
       TEST_ASSERT_EQUAL(0, result);
   }
   
   void test_process_command_status(void) {
       uint8_t data[8];
       int result = process_command(CMD_STATUS, data);
       TEST_ASSERT_EQUAL(0, result);
   }
   
   void test_process_command_invalid(void) {
       uint8_t data[8];
       int result = process_command(0xFF, data);
       TEST_ASSERT_EQUAL(-1, result);
   }

Integration Testing
===================

Component Integration
---------------------

.. code-block:: c

   // Integration test: Sensor + Display
   void test_sensor_display_integration(void) {
       Sensor sensor;
       Display display;
       
       sensor_init(&sensor, I2C_ADDR);
       display_init(&display);
       
       // Read sensor
       float temperature = sensor_read_temperature(&sensor);
       
       // Display should update
       display_show_temperature(&display, temperature);
       
       // Verify display content
       char expected[32];
       snprintf(expected, sizeof(expected), "Temp: %.1fC", temperature);
       TEST_ASSERT_EQUAL_STRING(expected, display_get_text(&display, 0));
   }

Protocol Testing
----------------

.. code-block:: c

   // Test UART protocol state machine
   typedef enum {
       PROTO_IDLE,
       PROTO_HEADER,
       PROTO_DATA,
       PROTO_CHECKSUM
   } ProtoState;
   
   void test_protocol_valid_packet(void) {
       ProtoState state = PROTO_IDLE;
       
       // Simulate receiving: START_BYTE, LEN, DATA..., CHECKSUM
       uint8_t packet[] = {0xAA, 0x03, 0x11, 0x22, 0x33, 0x66};
       
       for (size_t i = 0; i < sizeof(packet); i++) {
           state = protocol_process_byte(state, packet[i]);
       }
       
       TEST_ASSERT_EQUAL(PROTO_IDLE, state);  // Returned to idle
       TEST_ASSERT_TRUE(protocol_packet_valid());
   }
   
   void test_protocol_checksum_error(void) {
       ProtoState state = PROTO_IDLE;
       
       // Bad checksum
       uint8_t packet[] = {0xAA, 0x03, 0x11, 0x22, 0x33, 0xFF};
       
       for (size_t i = 0; i < sizeof(packet); i++) {
           state = protocol_process_byte(state, packet[i]);
       }
       
       TEST_ASSERT_FALSE(protocol_packet_valid());
       TEST_ASSERT_EQUAL(1, protocol_get_error_count());
   }

Hardware-in-the-Loop (HIL) Testing
===================================

Automated HIL Setup
-------------------

.. code-block:: python

   # Python test script for HIL
   import serial
   import time
   
   class EmbeddedDeviceTest:
       def __init__(self, port):
           self.ser = serial.Serial(port, 115200, timeout=1)
           time.sleep(0.1)  # Wait for reset
       
       def send_command(self, cmd):
           self.ser.write(cmd.encode() + b'\n')
           return self.ser.readline().decode().strip()
       
       def test_echo(self):
           response = self.send_command('ECHO Hello')
           assert response == 'Hello', f"Expected 'Hello', got '{response}'"
       
       def test_led_control(self):
           response = self.send_command('LED ON')
           assert response == 'OK', f"LED ON failed: {response}"
           
           response = self.send_command('LED STATUS')
           assert 'ON' in response, "LED should be ON"
           
           response = self.send_command('LED OFF')
           assert response == 'OK', f"LED OFF failed: {response}"
       
       def test_sensor_reading(self):
           response = self.send_command('READ TEMP')
           temp = float(response.split(':')[1])
           assert 15.0 <= temp <= 35.0, f"Temperature out of range: {temp}"
   
   if __name__ == '__main__':
       test = EmbeddedDeviceTest('/dev/ttyUSB0')
       test.test_echo()
       test.test_led_control()
       test.test_sensor_reading()
       print("All tests passed!")

Continuous Integration
----------------------

.. code-block:: yaml

   # .gitlab-ci.yml for embedded CI/CD
   stages:
     - build
     - test
     - deploy
   
   build:
     stage: build
     script:
       - arm-none-eabi-gcc --version
       - make clean
       - make all
     artifacts:
       paths:
         - build/firmware.elf
         - build/firmware.bin
   
   unit_test:
     stage: test
     script:
       - make test
       - lcov --capture --directory . --output-file coverage.info
       - genhtml coverage.info --output-directory coverage
     coverage: '/lines......: \d+\.\d+%/'
     artifacts:
       paths:
         - coverage/
   
   hil_test:
     stage: test
     tags:
       - hardware
     script:
       - python3 flash_device.py build/firmware.bin
       - python3 hil_tests.py
     only:
       - main

Regression Testing
==================

Automated Test Suite
--------------------

.. code-block:: c

   // Regression test suite
   static TestCase regression_tests[] = {
       {"Buffer Init", test_buffer_init},
       {"Buffer Write/Read", test_buffer_write_read},
       {"Buffer Overflow", test_buffer_overflow},
       {"UART Protocol", test_uart_protocol},
       {"Sensor Reading", test_sensor_reading},
       {"LED Control", test_led_control},
       {"Timer Accuracy", test_timer_accuracy},
       {"I2C Communication", test_i2c_comm},
       {"SPI Transfer", test_spi_transfer},
       {"ADC Conversion", test_adc_conversion},
   };
   
   void run_regression_suite(void) {
       int passed = 0;
       int failed = 0;
       
       printf("Running %d tests...\n", ARRAY_SIZE(regression_tests));
       
       for (size_t i = 0; i < ARRAY_SIZE(regression_tests); i++) {
           printf("[%zu/%zu] %s... ", i+1, ARRAY_SIZE(regression_tests),
                  regression_tests[i].name);
           
           if (regression_tests[i].func() == 0) {
               printf("PASS\n");
               passed++;
           } else {
               printf("FAIL\n");
               failed++;
           }
       }
       
       printf("\nResults: %d passed, %d failed\n", passed, failed);
   }

Stress Testing
==============

Load Testing
------------

.. code-block:: c

   // Stress test: Queue under heavy load
   void stress_test_queue(void) {
       Queue q;
       queue_init(&q, 128);
       
       const int ITERATIONS = 10000;
       int errors = 0;
       
       // Rapid enqueue/dequeue
       for (int i = 0; i < ITERATIONS; i++) {
           if (!queue_enqueue(&q, i & 0xFF)) {
               errors++;
           }
           
           if (i % 2 == 0) {
               uint8_t data;
               if (!queue_dequeue(&q, &data)) {
                   errors++;
               }
           }
       }
       
       printf("Queue stress test: %d errors in %d iterations\n",
              errors, ITERATIONS);
       TEST_ASSERT_EQUAL(0, errors);
   }

Endurance Testing
-----------------

.. code-block:: c

   // Long-running test
   void endurance_test_24h(void) {
       uint32_t start_time = get_tick_count();
       uint32_t test_duration = 24 * 60 * 60 * 1000;  // 24 hours
       uint32_t iterations = 0;
       int errors = 0;
       
       while ((get_tick_count() - start_time) < test_duration) {
           // Perform typical operations
           sensor_read();
           process_data();
           update_display();
           
           if (check_error()) {
               errors++;
           }
           
           iterations++;
           delay_ms(1000);  // 1 Hz
       }
       
       printf("Endurance test completed:\n");
       printf("  Duration: 24 hours\n");
       printf("  Iterations: %lu\n", iterations);
       printf("  Errors: %d\n", errors);
       printf("  Success rate: %.2f%%\n",
              100.0 * (iterations - errors) / iterations);
   }

Best Practices
==============

1. **Test early, test often** - continuous testing
2. **Automate tests** - run on every commit
3. **Mock hardware** - unit tests without hardware
4. **Test edge cases** - boundary conditions
5. **Measure coverage** - aim for >80%
6. **Integration tests** - test component interactions
7. **HIL for validation** - real hardware testing
8. **Regression suite** - prevent breaking changes
9. **Stress test** - find limits
10. **Document test cases** - requirements traceability

Common Testing Pitfalls
========================

1. **No mocking** - tests depend on hardware
2. **Poor coverage** - untested code paths
3. **No automation** - manual testing only
4. **Ignoring edge cases** - only happy path tested
5. **No regression tests** - bugs reappear
6. **Inadequate HIL** - hardware issues not caught

Quick Reference
===============

.. code-block:: c

   // Unity test
   TEST_ASSERT_EQUAL(expected, actual);
   TEST_ASSERT_TRUE(condition);
   TEST_ASSERT_NOT_NULL(pointer);
   
   // Run tests
   UNITY_BEGIN();
   RUN_TEST(test_function);
   return UNITY_END();
   
   // Coverage
   make test && lcov --capture --directory .
   
   // Mock
   void mock_init(Mock *m);
   void mock_expect_call(Mock *m, ...);

See Also
========

- Embedded_Debugging_Techniques.rst
- Embedded_System_Architecture_Patterns.rst
- Linux/Linux_Debug.rst

References
==========

- Making Embedded Systems (Elecia White)
- Test Driven Development for Embedded C (James Grenning)
- Unity Test Framework Documentation
- Embedded Testing Best Practices
