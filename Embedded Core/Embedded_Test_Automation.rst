======================================================
Embedded Test Automation Complete Guide
======================================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

Comprehensive guide to test automation for embedded systems, covering unit tests, integration tests, Hardware-in-the-Loop (HIL), End-to-End (E2E) testing, and test framework implementation.

Test Pyramid for Embedded
--------------------------

.. code-block:: text

   
          ┌───────────────┐
         ╱  E2E / System  ╲        10% - Slow, expensive
        ╱   Tests (few)    ╲       Full system validation
       ╱───────────────────╲      Device farm, real hardware
      ╱                     ╲
     ╱   Integration Tests  ╲     20% - Medium speed/cost
    ╱    (more)              ╲    Component interaction
   ╱─────────────────────────╲   HIL, QEMU, emulators
  ╱                           ╲
 ╱      Unit Tests (many)      ╲  70% - Fast, cheap
╱────────────────────────────────╲ Function-level testing
                                   Host machine, mocks

Test Framework Comparison
--------------------------

+------------------+---------------+------------------+------------------+
| **Framework**    | **Language**  | **Best For**     | **Key Feature**  |
+==================+===============+==================+==================+
| **PyTest**       | Python        | All levels       | Fixtures, marks  |
+------------------+---------------+------------------+------------------+
| **Robot**        | Python/KW     | Acceptance       | Keyword-driven   |
+------------------+---------------+------------------+------------------+
| **Unity**        | C             | Unit (embedded)  | Minimal overhead |
+------------------+---------------+------------------+------------------+
| **GoogleTest**   | C++           | Unit/Integration | Rich assertions  |
+------------------+---------------+------------------+------------------+
| **Ceedling**     | C             | TDD embedded     | Unity + mocks    |
+------------------+---------------+------------------+------------------+
| **Appium**       | Multiple      | Mobile/Android   | Cross-platform   |
+------------------+---------------+------------------+------------------+

🐍 PyTest for Embedded
========================

Basic Test Structure
--------------------

.. code-block:: python

   # tests/test_device.py
   import pytest
   import serial
   
   class TestDevice:
       """Test suite for embedded device"""
       
       @pytest.fixture(scope='class')
       def device(self):
           """Connect to device serial port"""
           ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
           yield ser
           ser.close()
       
       def test_device_responds(self, device):
           """Test device responds to ping"""
           device.write(b'ping\n')
           response = device.readline().decode().strip()
           assert response == 'pong'
       
       def test_version_command(self, device):
           """Test version reporting"""
           device.write(b'version\n')
           response = device.readline().decode().strip()
           assert response.startswith('v')
       
       @pytest.mark.slow
       def test_long_running_operation(self, device):
           """Test operation that takes time"""
           device.write(b'long_op\n')
           # Wait for completion
           response = device.readline().decode().strip()
           assert 'done' in response

Fixtures for Hardware
---------------------

.. code-block:: python

   # conftest.py
   import pytest
   import serial
   import subprocess
   
   @pytest.fixture(scope='session')
   def power_controller():
       """Control power to test fixtures"""
       class PowerController:
           def __init__(self):
               self.relay_board = '/dev/ttyACM0'
           
           def power_on(self, channel):
               subprocess.run(['usbrelay', f'{channel}_1'])
           
           def power_off(self, channel):
               subprocess.run(['usbrelay', f'{channel}_0'])
           
           def cycle(self, channel, delay=2):
               self.power_off(channel)
               time.sleep(delay)
               self.power_on(channel)
       
       return PowerController()
   
   @pytest.fixture(scope='function')
   def device(power_controller):
       """Device with power cycling"""
       # Power cycle before each test
       power_controller.cycle('DUT1')
       time.sleep(5)  # Wait for boot
       
       ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
       yield ser
       ser.close()
   
   @pytest.fixture(scope='session')
   def flash_firmware():
       """Flash firmware before test session"""
       subprocess.run([
           'openocd',
           '-f', 'interface/jlink.cfg',
           '-f', 'target/stm32f4x.cfg',
           '-c', 'program firmware.elf verify reset exit'
       ], check=True)

Parametrized Tests
------------------

.. code-block:: python

   import pytest
   
   @pytest.mark.parametrize('input,expected', [
       (b'led on\n', 'LED: ON'),
       (b'led off\n', 'LED: OFF'),
       (b'led toggle\n', 'LED: TOGGLED'),
   ])
   def test_led_commands(device, input, expected):
       """Test LED control commands"""
       device.write(input)
       response = device.readline().decode().strip()
       assert response == expected
   
   @pytest.mark.parametrize('baudrate', [9600, 19200, 38400, 115200])
   def test_multiple_baudrates(baudrate):
       """Test communication at different speeds"""
       ser = serial.Serial('/dev/ttyUSB0', baudrate, timeout=1)
       ser.write(b'ping\n')
       response = ser.readline().decode().strip()
       assert response == 'pong'
       ser.close()

Markers for Test Organization
------------------------------

.. code-block:: python

   # pytest.ini or pyproject.toml
   [pytest]
   markers =
       slow: marks tests as slow (deselect with '-m "not slow"')
       hw: requires actual hardware
       hil: hardware-in-the-loop tests
       integration: integration tests
       smoke: smoke tests
       regression: regression test suite
   
   # Usage in tests
   @pytest.mark.hw
   @pytest.mark.slow
   def test_flash_memory_write(device):
       """Test writing large data to flash"""
       pass
   
   @pytest.mark.hil
   def test_can_communication(can_interface):
       """Test CAN bus communication"""
       pass
   
   # Run specific markers
   # pytest -m "hw and not slow"
   # pytest -m "smoke or regression"

🤖 Hardware-in-the-Loop (HIL) Testing
=======================================

HIL Test Framework
------------------

.. code-block:: python

   # hil_framework.py
   import serial
   import time
   import subprocess
   from typing import List, Dict
   
   class HILDevice:
       """Base class for HIL device control"""
       
       def __init__(self, serial_port: str, baudrate: int = 115200):
           self.serial = serial.Serial(serial_port, baudrate, timeout=1)
           self.power_relay = None
       
       def send_command(self, cmd: str) -> str:
           """Send command and get response"""
           self.serial.write(f'{cmd}\n'.encode())
           return self.serial.readline().decode().strip()
       
       def flash_firmware(self, firmware_path: str):
           """Flash new firmware via JTAG"""
           subprocess.run([
               'openocd',
               '-f', 'interface/jlink.cfg',
               '-f', 'target/stm32f4x.cfg',
               '-c', f'program {firmware_path} verify reset exit'
           ], check=True)
       
       def power_cycle(self, delay: float = 2.0):
           """Power cycle the device"""
           if self.power_relay:
               self.power_relay.off()
               time.sleep(delay)
               self.power_relay.on()
               time.sleep(delay)  # Wait for boot
       
       def wait_for_boot(self, timeout: int = 30):
           """Wait for device to boot and be ready"""
           start = time.time()
           while time.time() - start < timeout:
               try:
                   response = self.send_command('status')
                   if 'ready' in response.lower():
                       return True
               except:
                   pass
               time.sleep(0.5)
           return False
       
       def close(self):
           """Cleanup"""
           self.serial.close()
   
   class CANInterface:
       """CAN bus testing interface"""
       
       def __init__(self, interface: str = 'can0'):
           self.interface = interface
           self._setup_interface()
       
       def _setup_interface(self):
           """Setup CAN interface"""
           subprocess.run([
               'sudo', 'ip', 'link', 'set', self.interface, 'type', 'can', 'bitrate', '500000'
           ])
           subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'up'])
       
       def send_frame(self, can_id: int, data: bytes):
           """Send CAN frame"""
           subprocess.run([
               'cansend', self.interface,
               f'{can_id:03X}#{data.hex()}'
           ])
       
       def receive_frame(self, timeout: float = 1.0) -> Dict:
           """Receive CAN frame"""
           result = subprocess.run(
               ['timeout', str(timeout), 'candump', self.interface, '-n', '1'],
               capture_output=True,
               text=True
           )
           # Parse candump output
           # Format: "can0  123   [8]  01 02 03 04 05 06 07 08"
           if result.stdout:
               parts = result.stdout.split()
               return {
                   'id': int(parts[1], 16),
                   'data': bytes.fromhex(''.join(parts[3:]))
               }
           return None

CAN Bus HIL Tests
-----------------

.. code-block:: python

   # tests/test_can_hil.py
   import pytest
   from hil_framework import HILDevice, CANInterface
   
   @pytest.fixture(scope='module')
   def dut():
       """Device Under Test"""
       device = HILDevice('/dev/ttyUSB0')
       device.wait_for_boot()
       yield device
       device.close()
   
   @pytest.fixture(scope='module')
   def can():
       """CAN interface"""
       return CANInterface('can0')
   
   def test_can_transmit(dut, can):
       """Test device can transmit CAN messages"""
       # Tell device to send CAN frame
       dut.send_command('can_send 0x123 01020304')
       
       # Verify frame received
       frame = can.receive_frame(timeout=2.0)
       assert frame is not None
       assert frame['id'] == 0x123
       assert frame['data'] == b'\x01\x02\x03\x04'
   
   def test_can_receive(dut, can):
       """Test device can receive CAN messages"""
       # Send frame to device
       can.send_frame(0x456, b'\x05\x06\x07\x08')
       
       # Check device received it
       response = dut.send_command('can_received?')
       assert '0x456' in response
   
   @pytest.mark.parametrize('can_id,data', [
       (0x100, b'\x11\x22\x33\x44'),
       (0x200, b'\xAA\xBB\xCC\xDD'),
       (0x7FF, b'\xFF\xFF\xFF\xFF'),
   ])
   def test_can_loopback(dut, can, can_id, data):
       """Test CAN loopback functionality"""
       dut.send_command(f'can_loopback 0x{can_id:X} {data.hex()}')
       
       frame = can.receive_frame(timeout=2.0)
       assert frame['id'] == can_id
       assert frame['data'] == data

I2C/SPI HIL Tests
-----------------

.. code-block:: python

   # tests/test_i2c_hil.py
   import pytest
   import smbus2
   
   @pytest.fixture
   def i2c_bus():
       """I2C bus interface"""
       bus = smbus2.SMBus(1)  # /dev/i2c-1
       yield bus
       bus.close()
   
   def test_i2c_sensor_read(dut, i2c_bus):
       """Test reading I2C sensor"""
       SENSOR_ADDR = 0x48
       TEMP_REG = 0x00
       
       # Read temperature register
       temp_data = i2c_bus.read_word_data(SENSOR_ADDR, TEMP_REG)
       
       # Verify device can also read it
       response = dut.send_command('i2c_read 0x48 0x00')
       device_temp = int(response.split()[-1], 16)
       
       assert abs(temp_data - device_temp) < 10  # Allow small variance

GPIO HIL Tests
--------------

.. code-block:: python

   # tests/test_gpio_hil.py
   import pytest
   import RPi.GPIO as GPIO
   
   @pytest.fixture(scope='module')
   def gpio_setup():
       """Setup GPIO pins"""
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(17, GPIO.IN)   # Device output connected here
       GPIO.setup(27, GPIO.OUT)  # Control device input
       yield
       GPIO.cleanup()
   
   def test_gpio_output(dut, gpio_setup):
       """Test device GPIO output"""
       dut.send_command('gpio set 5 high')
       time.sleep(0.1)
       assert GPIO.input(17) == GPIO.HIGH
       
       dut.send_command('gpio set 5 low')
       time.sleep(0.1)
       assert GPIO.input(17) == GPIO.LOW
   
   def test_gpio_input(dut, gpio_setup):
       """Test device GPIO input"""
       GPIO.output(27, GPIO.HIGH)
       response = dut.send_command('gpio get 3')
       assert 'high' in response.lower()
       
       GPIO.output(27, GPIO.LOW)
       response = dut.send_command('gpio get 3')
       assert 'low' in response.lower()

🔬 Fault Injection Testing
============================

Power Loss Testing
------------------

.. code-block:: python

   # tests/test_fault_injection.py
   import pytest
   import time
   import random
   
   def test_power_loss_during_write(dut, power_controller):
       """Test resilience to power loss during flash write"""
       
       for iteration in range(100):
           # Start write operation
           dut.send_command('flash_write_start')
           
           # Random delay before power cut
           delay = random.uniform(0.01, 0.5)
           time.sleep(delay)
           
           # Cut power
           power_controller.power_off('DUT1')
           time.sleep(1)
           power_controller.power_on('DUT1')
           
           # Wait for recovery
           assert dut.wait_for_boot(timeout=30)
           
           # Verify filesystem integrity
           response = dut.send_command('fs_check')
           assert 'corrupt' not in response.lower()
   
   def test_brownout_detection(dut, power_controller):
       """Test brownout detection and handling"""
       # Simulate brownout (voltage sag)
       power_controller.set_voltage('DUT1', 3.0)  # Below 3.3V nominal
       
       response = dut.send_command('status')
       assert 'brownout' in response.lower()
       
       # Restore voltage
       power_controller.set_voltage('DUT1', 3.3)

Boundary Value Testing
-----------------------

.. code-block:: python

   @pytest.mark.parametrize('value,expected', [
       (0, 'OK'),           # Minimum
       (100, 'OK'),         # Maximum
       (-1, 'ERROR'),       # Below min
       (101, 'ERROR'),      # Above max
       (50, 'OK'),          # Mid-range
   ])
   def test_input_boundaries(dut, value, expected):
       """Test input validation boundaries"""
       response = dut.send_command(f'set_value {value}')
       assert expected in response

Error Injection
---------------

.. code-block:: python

   def test_bad_crc(dut):
       """Test handling of corrupted data"""
       # Send packet with bad CRC
       packet = bytearray(b'\x01\x02\x03\x04\xFF\xFF')  # Bad CRC
       dut.serial.write(packet)
       
       response = dut.serial.readline().decode()
       assert 'CRC_ERROR' in response
   
   def test_buffer_overflow(dut):
       """Test buffer overflow protection"""
       # Send oversized packet
       large_data = b'A' * 2048
       dut.serial.write(large_data)
       
       # Device should reject or truncate
       response = dut.serial.readline().decode()
       assert 'OVERFLOW' in response or 'TRUNCATED' in response

⏱️ Long-Run / Soak Testing
===========================

Soak Test Framework
-------------------

.. code-block:: python

   # tests/test_soak.py
   import pytest
   import time
   from datetime import datetime, timedelta
   
   @pytest.mark.soak
   @pytest.mark.timeout(86400)  # 24 hours
   def test_24hour_soak(dut):
       """Run device for 24 hours"""
       
       start_time = datetime.now()
       end_time = start_time + timedelta(hours=24)
       iteration = 0
       errors = []
       
       while datetime.now() < end_time:
           iteration += 1
           
           try:
               # Perform operation
               response = dut.send_command('status')
               
               if 'error' in response.lower():
                   errors.append({
                       'iteration': iteration,
                       'time': datetime.now(),
                       'error': response
                   })
               
               # Check memory
               response = dut.send_command('mem_stats')
               if 'leak' in response.lower():
                   errors.append({
                       'iteration': iteration,
                       'time': datetime.now(),
                       'error': 'Memory leak detected'
                   })
               
               time.sleep(60)  # Check every minute
               
           except Exception as e:
               errors.append({
                   'iteration': iteration,
                   'time': datetime.now(),
                   'error': str(e)
               })
       
       # Report results
       print(f'\nSoak Test Completed:')
       print(f'Duration: 24 hours')
       print(f'Iterations: {iteration}')
       print(f'Errors: {len(errors)}')
       
       for error in errors:
           print(f"  {error['time']}: {error['error']}")
       
       assert len(errors) == 0, f'Soak test failed with {len(errors)} errors'

Stress Testing
--------------

.. code-block:: python

   @pytest.mark.stress
   def test_rapid_commands(dut):
       """Send commands as fast as possible"""
       
       commands = ['status', 'version', 'uptime'] * 1000
       errors = 0
       
       for cmd in commands:
           try:
               response = dut.send_command(cmd)
               if not response:
                   errors += 1
           except:
               errors += 1
       
       error_rate = errors / len(commands)
       assert error_rate < 0.01, f'Error rate {error_rate:.2%} exceeds 1%'

📱 Appium for Android Devices
===============================

Appium Setup
------------

.. code-block:: python

   # conftest.py
   import pytest
   from appium import webdriver
   
   @pytest.fixture(scope='module')
   def android_driver():
       """Appium driver for Android"""
       
       desired_caps = {
           'platformName': 'Android',
           'platformVersion': '11',
           'deviceName': 'Device Serial',
           'automationName': 'UiAutomator2',
           'app': '/path/to/app.apk',
           'noReset': False,
       }
       
       driver = webdriver.Remote(
           'http://localhost:4723/wd/hub',
           desired_caps
       )
       
       yield driver
       driver.quit()

Android Device Tests
--------------------

.. code-block:: python

   # tests/test_android_device.py
   from appium.webdriver.common.mobileby import MobileBy
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   def test_app_launch(android_driver):
       """Test app launches successfully"""
       # Wait for main activity
       WebDriverWait(android_driver, 10).until(
           EC.presence_of_element_located((MobileBy.ID, 'com.example:id/main'))
       )
       
       assert android_driver.current_activity == '.MainActivity'
   
   def test_bluetooth_connection(android_driver):
       """Test Bluetooth device connection"""
       # Enable Bluetooth
       android_driver.execute_script('mobile: shell', {
           'command': 'svc bluetooth enable'
       })
       
       # Wait for BT to initialize
       time.sleep(2)
       
       # Navigate to pairing screen
       pair_button = android_driver.find_element(MobileBy.ID, 'com.example:id/pair_device')
       pair_button.click()
       
       # Wait for connection
       WebDriverWait(android_driver, 30).until(
           EC.presence_of_element_located((MobileBy.ID, 'com.example:id/connected_label'))
       )
   
   def test_data_transfer(android_driver):
       """Test data transfer to embedded device"""
       # Send data
       send_button = android_driver.find_element(MobileBy.ID, 'com.example:id/send_data')
       send_button.click()
       
       # Verify acknowledgment
       status = WebDriverWait(android_driver, 10).until(
           EC.presence_of_element_located((MobileBy.ID, 'com.example:id/status'))
       )
       
       assert 'success' in status.text.lower()

ADB Commands in Tests
---------------------

.. code-block:: python

   import subprocess
   
   def adb_shell(command):
       """Execute ADB shell command"""
       result = subprocess.run(
           ['adb', 'shell', command],
           capture_output=True,
           text=True
       )
       return result.stdout.strip()
   
   def test_logcat_monitoring():
       """Monitor logcat for errors"""
       # Clear logcat
       subprocess.run(['adb', 'logcat', '-c'])
       
       # Trigger operation
       adb_shell('am start -n com.example/.MainActivity')
       
       # Capture logs
       result = subprocess.run(
           ['adb', 'logcat', '-d'],
           capture_output=True,
           text=True
       )
       
       # Check for errors
       assert 'FATAL' not in result.stdout
       assert 'ERROR' not in result.stdout

🤖 Robot Framework
===================

Robot Test Suite
----------------

.. code-block:: robotframework

   *** Settings ***
   Library           Serial
   Library           OperatingSystem
   
   Suite Setup       Connect To Device
   Suite Teardown    Disconnect From Device
   
   *** Variables ***
   ${PORT}           /dev/ttyUSB0
   ${BAUDRATE}       115200
   
   *** Test Cases ***
   Device Responds To Ping
       [Documentation]    Test basic device communication
       Send Command    ping
       ${response}=    Read Response
       Should Be Equal    ${response}    pong
   
   LED Control Test
       [Documentation]    Test LED control functionality
       Send Command    led on
       ${response}=    Read Response
       Should Contain    ${response}    LED: ON
       
       Send Command    led off
       ${response}=    Read Response
       Should Contain    ${response}    LED: OFF
   
   Version Information
       [Tags]    smoke
       Send Command    version
       ${response}=    Read Response
       Should Start With    ${response}    v
   
   *** Keywords ***
   Connect To Device
       Open Serial Port    ${PORT}    ${BAUDRATE}
   
   Disconnect From Device
       Close Serial Port
   
   Send Command
       [Arguments]    ${command}
       Write To Serial    ${command}\n
   
   Read Response
       ${response}=    Read From Serial
       [Return]    ${response}

📊 Test Reporting
==================

JUnit XML Generation
--------------------

.. code-block:: python

   # Run tests with JUnit output
   pytest tests/ --junitxml=results.xml

Custom HTML Report
------------------

.. code-block:: python

   pytest tests/ --html=report.html --self-contained-html

Test Metrics Script
-------------------

.. code-block:: python

   #!/usr/bin/env python3
   import xml.etree.ElementTree as ET
   import json
   
   def analyze_junit_xml(xml_file):
       """Analyze JUnit XML results"""
       
       tree = ET.parse(xml_file)
       root = tree.getroot()
       
       metrics = {
           'total': int(root.attrib['tests']),
           'passed': 0,
           'failed': int(root.attrib['failures']),
           'errors': int(root.attrib['errors']),
           'skipped': int(root.attrib['skipped']),
           'duration': float(root.attrib['time']),
           'pass_rate': 0.0,
       }
       
       metrics['passed'] = metrics['total'] - metrics['failed'] - metrics['errors'] - metrics['skipped']
       metrics['pass_rate'] = (metrics['passed'] / metrics['total']) * 100
       
       return metrics
   
   if __name__ == '__main__':
       metrics = analyze_junit_xml('results.xml')
       print(json.dumps(metrics, indent=2))

📖 Best Practices
==================

1. **Start with unit tests** - Fastest feedback loop
2. **Mock hardware dependencies** - Test logic without HW
3. **Use fixtures effectively** - DRY principle for test setup
4. **Parametrize tests** - Cover more cases with less code
5. **Mark tests appropriately** - Enable selective execution
6. **Implement retry logic** - Handle flaky hardware
7. **Log verbosely** - Essential for debugging failures
8. **Measure coverage** - Identify untested code paths
9. **Automate flash/provision** - Consistent test environment
10. **Monitor test duration** - Optimize slow tests

📚 References
==============

* **PyTest**: https://docs.pytest.org/
* **Robot Framework**: https://robotframework.org/
* **Unity**: http://www.throwtheswitch.org/unity
* **GoogleTest**: https://github.com/google/googletest
* **Appium**: https://appium.io/docs/
* **Python Serial**: https://pyserial.readthedocs.io/

================================
Last Updated: January 2026
Version: 3.0
================================
