======================================================
Device Provisioning & Flashing Complete Guide
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

Comprehensive guide to device provisioning, firmware flashing, commissioning workflows, and CLI tooling for embedded device manufacturing and testing.

Device Lifecycle
-----------------

.. code-block:: text

   Manufacturing → Provisioning → Testing → Deployment → Updates
        │              │            │           │            │
        ▼              ▼            ▼           ▼            ▼
   Flash Boot    Serial#/Keys   QA Tests   Commission   OTA Updates
   Program MCU   Calibration    HIL Test   Activate     Patches
   Burn Fuses    Certificates   Burn-in    Register     Features

Provisioning Components
-----------------------

+-------------------------+------------------------------------------------+
| **Component**           | **Purpose**                                    |
+=========================+================================================+
| **Firmware Flashing**   | Load bootloader, application, FPGA images      |
+-------------------------+------------------------------------------------+
| **Configuration**       | Device settings, network, operational params   |
+-------------------------+------------------------------------------------+
| **Credentials**         | Keys, certificates, passwords                  |
+-------------------------+------------------------------------------------+
| **Calibration**         | Sensor offsets, ADC calibration, trim values   |
+-------------------------+------------------------------------------------+
| **Identification**      | Serial number, MAC address, device ID          |
+-------------------------+------------------------------------------------+
| **Activation**          | License keys, feature flags, cloud registration|
+-------------------------+------------------------------------------------+

🔌 Flashing Methods
====================

JTAG/SWD Flashing
-----------------

**OpenOCD (ARM Cortex-M/A/R):**

.. code-block:: bash

   # Flash via OpenOCD
   openocd \
       -f interface/jlink.cfg \
       -f target/stm32f4x.cfg \
       -c "program firmware.elf verify reset exit"
   
   # Flash specific regions
   openocd \
       -f interface/stlink.cfg \
       -f target/stm32f4x.cfg \
       -c "init" \
       -c "reset halt" \
       -c "flash write_image erase bootloader.bin 0x08000000" \
       -c "flash write_image erase application.bin 0x08010000" \
       -c "verify_image application.bin 0x08010000" \
       -c "reset run" \
       -c "shutdown"
   
   # Dump flash for backup
   openocd \
       -f interface/jlink.cfg \
       -f target/stm32f4x.cfg \
       -c "init" \
       -c "dump_image flash_backup.bin 0x08000000 0x100000" \
       -c "shutdown"

**J-Link Commander:**

.. code-block:: bash

   # Interactive flashing
   JLinkExe -device STM32F407VG -if SWD -speed 4000
   
   # In J-Link shell:
   # > connect
   # > erase
   # > loadbin firmware.bin 0x08000000
   # > verifybin firmware.bin 0x08000000
   # > r
   # > go
   # > exit
   
   # Scripted flashing
   cat > flash_script.jlink << 'EOF'
   si SWD
   speed 4000
   device STM32F407VG
   connect
   erase
   loadbin firmware.bin 0x08000000
   verifybin firmware.bin 0x08000000
   r
   go
   exit
   EOF
   
   JLinkExe -CommandFile flash_script.jlink

**GDB with OpenOCD:**

.. code-block:: bash

   # Terminal 1: Start OpenOCD
   openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
   
   # Terminal 2: Connect with GDB
   arm-none-eabi-gdb firmware.elf
   
   # In GDB:
   (gdb) target extended-remote :3333
   (gdb) monitor reset halt
   (gdb) load
   (gdb) monitor reset init
   (gdb) continue

DFU (Device Firmware Upgrade)
------------------------------

**USB DFU Protocol:**

.. code-block:: bash

   # List DFU devices
   dfu-util -l
   
   # Flash firmware
   dfu-util -a 0 -D firmware.bin
   
   # Flash to specific address
   dfu-util -a 0 -s 0x08000000:leave -D firmware.bin
   
   # Flash multiple regions
   dfu-util -a 0 -s 0x08000000 -D bootloader.bin
   dfu-util -a 0 -s 0x08010000 -D application.bin
   
   # Mass erase before flash
   dfu-util -a 0 -s 0x08000000:mass-erase:force -D firmware.bin
   
   # Upload (read) firmware
   dfu-util -a 0 -U firmware_backup.bin

**STM32 DFU via dfu-util:**

.. code-block:: bash

   # Enter DFU mode (BOOT0=1, reset)
   # Then flash
   dfu-util \
       -d 0483:df11 \
       -a 0 \
       -s 0x08000000:leave \
       -D firmware.bin
   
   # STM32CubeProgrammer CLI
   STM32_Programmer_CLI \
       -c port=usb1 \
       -w firmware.bin 0x08000000 \
       -v \
       -rst

Serial Bootloader
-----------------

**STM32 UART Bootloader:**

.. code-block:: bash

   # Using stm32flash
   stm32flash -w firmware.bin -v -g 0x0 /dev/ttyUSB0
   
   # Erase flash first
   stm32flash -o /dev/ttyUSB0
   
   # Flash with specific options
   stm32flash \
       -b 115200 \
       -w firmware.bin \
       -v \
       -g 0x08000000 \
       /dev/ttyUSB0
   
   # Read flash
   stm32flash -r flash_dump.bin /dev/ttyUSB0

**Custom Serial Bootloader Protocol:**

.. code-block:: python

   #!/usr/bin/env python3
   import serial
   import struct
   import time
   
   class SerialBootloader:
       def __init__(self, port, baudrate=115200):
           self.ser = serial.Serial(port, baudrate, timeout=1)
           time.sleep(0.5)
       
       def enter_bootloader(self):
           """Enter bootloader mode"""
           self.ser.write(b'BOOT\r\n')
           response = self.ser.readline()
           return b'READY' in response
       
       def erase_flash(self):
           """Erase application flash"""
           self.ser.write(b'ERASE\r\n')
           response = self.ser.readline(timeout=30)
           return b'OK' in response
       
       def flash_firmware(self, firmware_path, address=0x08010000):
           """Flash firmware in chunks"""
           with open(firmware_path, 'rb') as f:
               firmware = f.read()
           
           chunk_size = 256
           total_chunks = (len(firmware) + chunk_size - 1) // chunk_size
           
           for i in range(total_chunks):
               chunk = firmware[i*chunk_size:(i+1)*chunk_size]
               chunk_address = address + i * chunk_size
               
               # Send write command
               cmd = struct.pack('<BIH', 0x01, chunk_address, len(chunk))
               self.ser.write(cmd + chunk)
               
               # Wait for acknowledgment
               ack = self.ser.read(1)
               if ack != b'\x06':
                   raise Exception(f'Flash failed at chunk {i}')
               
               # Progress
               percent = (i + 1) / total_chunks * 100
               print(f'\rFlashing: {percent:.1f}%', end='')
           
           print('\nFlashing complete')
       
       def verify_firmware(self, firmware_path, address=0x08010000):
           """Verify flashed firmware"""
           with open(firmware_path, 'rb') as f:
               firmware = f.read()
           
           # Send read command
           cmd = struct.pack('<BII', 0x02, address, len(firmware))
           self.ser.write(cmd)
           
           # Read back
           readback = self.ser.read(len(firmware))
           
           return firmware == readback
       
       def boot_application(self):
           """Jump to application"""
           self.ser.write(b'BOOT_APP\r\n')
           response = self.ser.readline()
           return b'BOOTING' in response
   
   # Usage
   if __name__ == '__main__':
       bl = SerialBootloader('/dev/ttyUSB0')
       
       if bl.enter_bootloader():
           print('Entered bootloader')
           bl.erase_flash()
           bl.flash_firmware('firmware.bin')
           
           if bl.verify_firmware('firmware.bin'):
               print('Verification successful')
               bl.boot_application()
           else:
               print('Verification failed!')

Fastboot Protocol
-----------------

**Android Fastboot:**

.. code-block:: bash

   # Enter fastboot mode
   adb reboot bootloader
   
   # List devices
   fastboot devices
   
   # Flash partitions
   fastboot flash boot boot.img
   fastboot flash system system.img
   fastboot flash userdata userdata.img
   fastboot flash recovery recovery.img
   
   # Flash sparse images
   fastboot flash system system.img.sparse
   
   # Erase partition
   fastboot erase userdata
   
   # Format partition
   fastboot format userdata
   
   # Reboot
   fastboot reboot
   
   # Unlock bootloader (OEM specific)
   fastboot oem unlock
   
   # Get variables
   fastboot getvar all
   fastboot getvar version-bootloader
   fastboot getvar serialno
   
   # Flash all (flash-all.sh script)
   fastboot flashall

**Custom Fastboot for Embedded:**

.. code-block:: python

   #!/usr/bin/env python3
   import usb.core
   import usb.util
   
   class FastbootDevice:
       VENDOR_ID = 0x18d1
       PRODUCT_ID = 0x4ee0
       
       def __init__(self):
           self.dev = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)
           if self.dev is None:
               raise ValueError('Device not found')
           
           self.dev.set_configuration()
       
       def send_command(self, cmd):
           """Send fastboot command"""
           self.dev.write(0x01, cmd.encode() + b'\x00')
           response = self.dev.read(0x81, 64).tobytes()
           return response.decode().strip('\x00')
       
       def download_data(self, data):
           """Download data to device"""
           size = len(data)
           cmd = f'download:{size:08x}'
           response = self.send_command(cmd)
           
           if not response.startswith('DATA'):
               raise Exception(f'Download failed: {response}')
           
           # Send data in chunks
           chunk_size = 4096
           for i in range(0, size, chunk_size):
               chunk = data[i:i+chunk_size]
               self.dev.write(0x01, chunk)
           
           # Wait for acknowledgment
           response = self.dev.read(0x81, 64).tobytes().decode().strip('\x00')
           return response.startswith('OKAY')
       
       def flash_partition(self, partition, image_data):
           """Flash partition with image data"""
           # Download image
           if not self.download_data(image_data):
               raise Exception('Data download failed')
           
           # Flash command
           response = self.send_command(f'flash:{partition}')
           return response.startswith('OKAY')
       
       def reboot(self):
           """Reboot device"""
           self.send_command('reboot')

📱 Android Device Flashing
============================

ADB (Android Debug Bridge)
---------------------------

.. code-block:: bash

   # Install/update ADB
   sudo apt install android-tools-adb android-tools-fastboot
   
   # Start ADB server
   adb start-server
   
   # List devices
   adb devices
   
   # Reboot modes
   adb reboot                 # Normal reboot
   adb reboot bootloader      # Fastboot mode
   adb reboot recovery        # Recovery mode
   adb reboot download        # Download mode (Samsung)
   
   # Push files
   adb push local_file /sdcard/
   
   # Pull files
   adb pull /sdcard/file local_file
   
   # Install APK
   adb install app.apk
   adb install -r app.apk     # Reinstall
   adb install -g app.apk     # Grant permissions
   
   # Uninstall
   adb uninstall com.example.app
   
   # Shell access
   adb shell
   adb shell "ls -la /system"
   
   # Root access
   adb root
   adb remount
   
   # Logcat
   adb logcat
   adb logcat -c              # Clear
   adb logcat -d > log.txt    # Dump to file
   
   # Screenshots
   adb shell screencap /sdcard/screen.png
   adb pull /sdcard/screen.png
   
   # Screen recording
   adb shell screenrecord /sdcard/demo.mp4
   
   # Backup/Restore
   adb backup -all -f backup.ab
   adb restore backup.ab

System Image Flashing
----------------------

.. code-block:: bash

   # Full system flash (Pixel devices)
   unzip image-xxx.zip
   cd image-xxx
   ./flash-all.sh
   
   # Manual flashing
   adb reboot bootloader
   
   fastboot flash bootloader bootloader.img
   fastboot reboot-bootloader
   
   fastboot flash radio radio.img
   fastboot reboot-bootloader
   
   fastboot flash boot boot.img
   fastboot flash system system.img
   fastboot flash vendor vendor.img
   fastboot flash userdata userdata.img
   
   fastboot reboot

Custom Recovery (TWRP)
----------------------

.. code-block:: bash

   # Flash TWRP
   adb reboot bootloader
   fastboot flash recovery twrp.img
   fastboot reboot recovery
   
   # In TWRP, use UI or ADB sideload
   adb sideload rom.zip

🏭 Manufacturing Provisioning
===============================

Production Flashing Workflow
-----------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Production provisioning script"""
   
   import subprocess
   import time
   import json
   import serial
   from datetime import datetime
   
   class ProductionProvisioner:
       def __init__(self, config_file):
           with open(config_file) as f:
               self.config = json.load(f)
           
           self.log = []
       
       def flash_bootloader(self):
           """Flash bootloader via JTAG"""
           cmd = [
               'openocd',
               '-f', self.config['jtag_interface'],
               '-f', self.config['jtag_target'],
               '-c', f'program {self.config["bootloader"]} verify reset exit'
           ]
           
           result = subprocess.run(cmd, capture_output=True, text=True)
           success = result.returncode == 0
           
           self.log.append({
               'step': 'flash_bootloader',
               'success': success,
               'output': result.stdout
           })
           
           return success
       
       def flash_application(self):
           """Flash application via bootloader"""
           ser = serial.Serial(self.config['serial_port'], 115200, timeout=1)
           
           # Enter bootloader
           ser.write(b'BOOT\r\n')
           time.sleep(0.5)
           
           # Flash
           bl = SerialBootloader(self.config['serial_port'])
           bl.erase_flash()
           bl.flash_firmware(self.config['application'])
           
           success = bl.verify_firmware(self.config['application'])
           
           self.log.append({
               'step': 'flash_application',
               'success': success
           })
           
           return success
       
       def program_serial_number(self):
           """Program unique serial number"""
           serial_num = self.generate_serial_number()
           
           ser = serial.Serial(self.config['serial_port'], 115200, timeout=1)
           ser.write(f'SET_SERIAL {serial_num}\r\n'.encode())
           response = ser.readline().decode()
           
           success = 'OK' in response
           
           self.log.append({
               'step': 'program_serial_number',
               'success': success,
               'serial_number': serial_num
           })
           
           return success, serial_num
       
       def burn_keys(self):
           """Program cryptographic keys (one-time)"""
           # Generate device-specific key
           from cryptography.hazmat.primitives.asymmetric import rsa
           from cryptography.hazmat.backends import default_backend
           
           private_key = rsa.generate_private_key(
               public_exponent=65537,
               key_size=2048,
               backend=default_backend()
           )
           
           # Write to device OTP/fuses (irreversible!)
           # Implementation depends on MCU
           
           success = True  # Placeholder
           
           self.log.append({
               'step': 'burn_keys',
               'success': success
           })
           
           return success
       
       def calibrate_sensors(self):
           """Perform sensor calibration"""
           ser = serial.Serial(self.config['serial_port'], 115200, timeout=1)
           
           # Temperature calibration
           ser.write(b'CAL_TEMP 25.0\r\n')
           response = ser.readline().decode()
           
           # ADC calibration
           ser.write(b'CAL_ADC\r\n')
           response = ser.readline().decode()
           
           success = 'OK' in response
           
           self.log.append({
               'step': 'calibrate_sensors',
               'success': success
           })
           
           return success
       
       def functional_test(self):
           """Run basic functional tests"""
           ser = serial.Serial(self.config['serial_port'], 115200, timeout=1)
           
           tests = [
               ('ping', 'pong'),
               ('led on', 'LED: ON'),
               ('read temp', lambda x: 20 < float(x.split()[0]) < 30),
           ]
           
           all_passed = True
           
           for cmd, expected in tests:
               ser.write(f'{cmd}\r\n'.encode())
               response = ser.readline().decode().strip()
               
               if callable(expected):
                   passed = expected(response)
               else:
                   passed = expected in response
               
               all_passed &= passed
           
           self.log.append({
               'step': 'functional_test',
               'success': all_passed
           })
           
           return all_passed
       
       def save_report(self, serial_number):
           """Save provisioning report"""
           report = {
               'serial_number': serial_number,
               'timestamp': datetime.now().isoformat(),
               'firmware_version': self.config['firmware_version'],
               'steps': self.log,
               'passed': all(step['success'] for step in self.log)
           }
           
           filename = f'provision_{serial_number}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
           with open(filename, 'w') as f:
               json.dump(report, f, indent=2)
           
           return report['passed']
       
       def provision(self):
           """Complete provisioning sequence"""
           print('Starting provisioning...')
           
           if not self.flash_bootloader():
               print('ERROR: Bootloader flash failed')
               return False
           
           if not self.flash_application():
               print('ERROR: Application flash failed')
               return False
           
           success, serial_num = self.program_serial_number()
           if not success:
               print('ERROR: Serial number programming failed')
               return False
           
           if not self.calibrate_sensors():
               print('ERROR: Calibration failed')
               return False
           
           if not self.functional_test():
               print('ERROR: Functional test failed')
               return False
           
           if self.save_report(serial_num):
               print(f'✓ Provisioning complete: {serial_num}')
               return True
           else:
               print('✗ Provisioning failed')
               return False
       
       def generate_serial_number(self):
           """Generate unique serial number"""
           from datetime import datetime
           import random
           
           timestamp = datetime.now().strftime('%Y%m%d')
           random_part = ''.join([str(random.randint(0, 9)) for _ in range(6)])
           
           return f'SN{timestamp}{random_part}'
   
   # Usage
   if __name__ == '__main__':
       provisioner = ProductionProvisioner('provision_config.json')
       provisioner.provision()

Commissioning Workflow
-----------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Device commissioning for deployment"""
   
   import requests
   import json
   
   class DeviceCommissioner:
       def __init__(self, api_url, api_key):
           self.api_url = api_url
           self.api_key = api_key
           self.headers = {'Authorization': f'Bearer {api_key}'}
       
       def register_device(self, serial_number, device_type):
           """Register device with cloud backend"""
           data = {
               'serial_number': serial_number,
               'device_type': device_type,
               'firmware_version': self.get_firmware_version(),
               'registered_at': datetime.now().isoformat()
           }
           
           response = requests.post(
               f'{self.api_url}/devices',
               json=data,
               headers=self.headers
           )
           
           if response.status_code == 201:
               device_id = response.json()['device_id']
               return device_id
           else:
               raise Exception(f'Registration failed: {response.text}')
       
       def provision_credentials(self, device_id):
           """Get device credentials from server"""
           response = requests.get(
               f'{self.api_url}/devices/{device_id}/credentials',
               headers=self.headers
           )
           
           if response.status_code == 200:
               creds = response.json()
               return creds['client_id'], creds['client_secret']
           else:
               raise Exception('Credential provisioning failed')
       
       def configure_device(self, serial_port, config):
           """Send configuration to device"""
           ser = serial.Serial(serial_port, 115200, timeout=1)
           
           for key, value in config.items():
               cmd = f'CONFIG_SET {key} {value}\r\n'
               ser.write(cmd.encode())
               response = ser.readline().decode()
               
               if 'OK' not in response:
                   raise Exception(f'Config failed: {key}')
       
       def activate_device(self, device_id):
           """Activate device for production use"""
           response = requests.post(
               f'{self.api_url}/devices/{device_id}/activate',
               headers=self.headers
           )
           
           return response.status_code == 200
       
       def commission(self, serial_number, device_type, serial_port):
           """Complete commissioning workflow"""
           print(f'Commissioning device: {serial_number}')
           
           # Register
           device_id = self.register_device(serial_number, device_type)
           print(f'Registered: {device_id}')
           
           # Get credentials
           client_id, client_secret = self.provision_credentials(device_id)
           
           # Configure device
           config = {
               'DEVICE_ID': device_id,
               'CLIENT_ID': client_id,
               'CLIENT_SECRET': client_secret,
               'API_URL': self.api_url
           }
           self.configure_device(serial_port, config)
           print('Configured')
           
           # Activate
           if self.activate_device(device_id):
               print('✓ Commissioning complete')
               return device_id
           else:
               raise Exception('Activation failed')

🔧 CLI Tool Development
=========================

Python CLI with Click
---------------------

.. code-block:: python

   #!/usr/bin/env python3
   """Device flashing CLI tool"""
   
   import click
   import serial
   import subprocess
   from pathlib import Path
   
   @click.group()
   @click.option('--port', default='/dev/ttyUSB0', help='Serial port')
   @click.option('--baudrate', default=115200, help='Baud rate')
   @click.pass_context
   def cli(ctx, port, baudrate):
       """Device provisioning and flashing tool"""
       ctx.ensure_object(dict)
       ctx.obj['PORT'] = port
       ctx.obj['BAUDRATE'] = baudrate
   
   @cli.command()
   @click.argument('firmware', type=click.Path(exists=True))
   @click.option('--verify/--no-verify', default=True)
   @click.pass_context
   def flash(ctx, firmware, verify):
       """Flash firmware via serial bootloader"""
       click.echo(f'Flashing {firmware} to {ctx.obj["PORT"]}')
       
       bl = SerialBootloader(ctx.obj['PORT'], ctx.obj['BAUDRATE'])
       
       with click.progressbar(length=100, label='Flashing') as bar:
           # Implement progress callback in flash_firmware
           bl.flash_firmware(firmware)
           bar.update(100)
       
       if verify:
           click.echo('Verifying...', nl=False)
           if bl.verify_firmware(firmware):
               click.secho(' ✓', fg='green')
           else:
               click.secho(' ✗', fg='red')
               raise click.Abort()
   
   @cli.command()
   @click.argument('serial_number')
   @click.pass_context
   def set_serial(ctx, serial_number):
       """Program device serial number"""
       ser = serial.Serial(ctx.obj['PORT'], ctx.obj['BAUDRATE'])
       ser.write(f'SET_SERIAL {serial_number}\r\n'.encode())
       response = ser.readline().decode()
       
       if 'OK' in response:
           click.secho(f'✓ Serial number set: {serial_number}', fg='green')
       else:
           click.secho(f'✗ Failed: {response}', fg='red')
   
   @cli.command()
   @click.pass_context
   def test(ctx):
       """Run functional tests"""
       ser = serial.Serial(ctx.obj['PORT'], ctx.obj['BAUDRATE'])
       
       tests = [
           ('ping', 'pong'),
           ('version', 'v'),
           ('status', 'OK'),
       ]
       
       all_passed = True
       
       for cmd, expected in tests:
           ser.write(f'{cmd}\r\n'.encode())
           response = ser.readline().decode().strip()
           
           passed = expected in response
           all_passed &= passed
           
           status = click.style('✓', fg='green') if passed else click.style('✗', fg='red')
           click.echo(f'{status} {cmd}: {response}')
       
       if not all_passed:
           raise click.Abort()
   
   @cli.command()
   @click.argument('firmware', type=click.Path(exists=True))
   @click.option('--interface', default='interface/jlink.cfg')
   @click.option('--target', default='target/stm32f4x.cfg')
   def jtag_flash(firmware, interface, target):
       """Flash via JTAG/SWD"""
       cmd = [
           'openocd',
           '-f', interface,
           '-f', target,
           '-c', f'program {firmware} verify reset exit'
       ]
       
       result = subprocess.run(cmd, capture_output=True, text=True)
       
       if result.returncode == 0:
           click.secho('✓ Flashing complete', fg='green')
       else:
           click.secho('✗ Flashing failed', fg='red')
           click.echo(result.stderr)
           raise click.Abort()
   
   if __name__ == '__main__':
       cli(obj={})

Bash CLI Tool
-------------

.. code-block:: bash

   #!/bin/bash
   # Device provisioning script
   
   set -euo pipefail
   
   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   PORT="${PORT:-/dev/ttyUSB0}"
   BAUDRATE="${BAUDRATE:-115200}"
   
   # Colors
   RED='\033[0;31m'
   GREEN='\033[0;32m'
   YELLOW='\033[1;33m'
   NC='\033[0m' # No Color
   
   log_info() {
       echo -e "${GREEN}[INFO]${NC} $1"
   }
   
   log_error() {
       echo -e "${RED}[ERROR]${NC} $1" >&2
   }
   
   log_warn() {
       echo -e "${YELLOW}[WARN]${NC} $1"
   }
   
   flash_firmware() {
       local firmware="$1"
       
       log_info "Flashing $firmware to $PORT"
       
       if command -v stm32flash &> /dev/null; then
           stm32flash -w "$firmware" -v -g 0x0 "$PORT"
       elif command -v dfu-util &> /dev/null; then
           dfu-util -a 0 -D "$firmware"
       else
           log_error "No flashing tool found"
           return 1
       fi
   }
   
   set_serial_number() {
       local serial_num="$1"
       
       log_info "Setting serial number: $serial_num"
       
       echo "SET_SERIAL $serial_num" > "$PORT"
       sleep 0.5
       
       # Read response
       response=$(timeout 2 cat "$PORT" || echo "TIMEOUT")
       
       if [[ "$response" == *"OK"* ]]; then
           log_info "Serial number set successfully"
       else
           log_error "Failed to set serial number"
           return 1
       fi
   }
   
   run_tests() {
       log_info "Running functional tests"
       
       local tests=("ping:pong" "version:v" "status:OK")
       local all_passed=true
       
       for test in "${tests[@]}"; then
           IFS=':' read -r cmd expected <<< "$test"
           
           echo "$cmd" > "$PORT"
           sleep 0.5
           response=$(timeout 2 cat "$PORT" || echo "TIMEOUT")
           
           if [[ "$response" == *"$expected"* ]]; then
               echo -e "${GREEN}✓${NC} $cmd: $response"
           else
               echo -e "${RED}✗${NC} $cmd: $response"
               all_passed=false
           fi
       done
       
       if [[ "$all_passed" == "false" ]]; then
           return 1
       fi
   }
   
   main() {
       case "${1:-}" in
           flash)
               flash_firmware "${2:-firmware.bin}"
               ;;
           set-serial)
               set_serial_number "${2:-}"
               ;;
           test)
               run_tests
               ;;
           provision)
               log_info "Starting full provisioning"
               flash_firmware "${2:-firmware.bin}"
               set_serial_number "$(date +%Y%m%d)$(shuf -i 100000-999999 -n 1)"
               run_tests
               log_info "Provisioning complete"
               ;;
           *)
               echo "Usage: $0 {flash|set-serial|test|provision} [args]"
               exit 1
               ;;
       esac
   }
   
   main "$@"

📖 Best Practices
==================

1. **Automate everything** - Manual steps lead to errors
2. **Verify after flash** - Always verify written data
3. **Log all operations** - Traceability for manufacturing
4. **Handle errors gracefully** - Retry logic, clear messages
5. **Use unique identifiers** - Serial numbers, MAC addresses
6. **Secure credentials** - Never hardcode, use secure storage
7. **Test thoroughly** - Functional tests after provisioning
8. **Version control configs** - Track provisioning changes
9. **Monitor flash wear** - Limit unnecessary writes
10. **Document procedures** - Clear instructions for operators

📚 References
==============

* **OpenOCD**: https://openocd.org/doc/
* **dfu-util**: http://dfu-util.sourceforge.net/
* **Android ADB**: https://developer.android.com/studio/command-line/adb
* **Fastboot Protocol**: https://android.googlesource.com/platform/system/core/+/master/fastboot/
* **J-Link**: https://www.segger.com/products/debug-probes/j-link/
* **Click (Python CLI)**: https://click.palletsprojects.com/

================================
Last Updated: January 2026
Version: 3.0
================================
