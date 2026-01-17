============================================================
ARINC 653 — Avionics Application Software Standard Interface
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC 653** defines the **APEX (APplication EXecutive)** interface for partitioned real-time operating systems in safety-critical avionics. It enables multiple applications of different criticality levels to run on shared hardware with **time and space partitioning** guarantees.

**Key Concepts:**
- **Time Partitioning:** Fixed scheduling windows prevent timing interference
- **Space Partitioning:** Memory isolation prevents data corruption between partitions
- **IPC:** Sampling ports (latest-value), Queuing ports (FIFO), Blackboards (shared memory)
- **Health Monitoring:** Partition and process-level fault detection and recovery
- **Certification:** Enables DO-178C DAL A/B software on Integrated Modular Avionics (IMA)

**Common RTOS:** VxWorks 653, PikeOS, INTEGRITY-178B, Deos, Lynx MOSA.ic

**Applications:** Flight controls, FADEC, FMS, TCAS, displays (Boeing 787, Airbus A350/A380)

================================================================================
1. Overview & Architecture
================================================================================

**Purpose:**
ARINC 653 standardizes the interface between safety-critical avionics applications and the underlying partitioned operating system. This enables:
- Portable applications across different RTOS vendors
- Mixed-criticality systems (DAL A, B, C, D on same hardware)
- Reduced certification costs (partition independence)
- Integrated Modular Avionics (IMA) architectures

**Standardization:**
- **SAE AS6653:** Current SAE designation
- **ARINC 653:** Original ARINC specification
- **EUROCAE ED-237:** European equivalent
- **Parts:**
  - Part 0: Overview and concepts
  - Part 1: Core APEX services (required)
  - Part 2: Extended services (optional)
  - Part 3: Conformity test specification
  - Part 4: Multicore supplement
  - Part 5: Security extensions (2026)

**Integrated Modular Avionics (IMA):**
Traditional federated avionics uses dedicated LRUs per function. IMA consolidates multiple functions onto shared computing modules (e.g., Airbus CPIOM, Boeing CCS):

.. code-block:: text

   Federated Architecture:        IMA Architecture (ARINC 653):
   ┌─────────────┐               ┌──────────────────────────────┐
   │ FMS (LRU 1) │               │      CPIOM / IMA Module      │
   └─────────────┘               │ ┌──────────┬──────────┬────┐ │
   ┌─────────────┐               │ │FMS Part. │TCAS Part.│... │ │
   │ TCAS (LRU2) │      →        │ │ (DAL B)  │ (DAL A)  │    │ │
   └─────────────┘               │ └──────────┴──────────┴────┘ │
   ┌─────────────┐               │   ARINC 653 APEX Interface   │
   │ Display     │               │   Partitioned RTOS Kernel    │
   └─────────────┘               └──────────────────────────────┘

Benefits: -70% hardware, -50% power, -60% weight vs federated

================================================================================
2. Partitioning Concepts
================================================================================

**2.1 Time Partitioning**
----------------------------

Fixed, deterministic scheduling ensures each partition gets guaranteed CPU time:

**Major Frame (MAF):**
- Repeating cycle of partition time windows
- Typically 50-500 ms duration
- Divided into partition windows

**Partition Window:**
- Fixed duration CPU allocation for one partition
- Multiple windows per partition allowed (for periodic tasks)
- No preemption between partitions

**Example Schedule:**

.. code-block:: text

   Major Frame = 100 ms
   ┌──────────────────────────────────────────────────────────┐
   │ P1  │  P2   │ P3 │  P1  │  P4   │ P2  │  P5   │  Idle  │
   │10ms │ 20ms  │5ms │ 15ms │ 25ms  │10ms │ 10ms  │  5ms   │
   └──────────────────────────────────────────────────────────┘
   
   P1 gets 25ms total (10+15), P2 gets 30ms (20+10), etc.

**ARINC 653 API:**

.. code-block:: c

   // Get partition mode/status
   RETURN_CODE_TYPE GET_PARTITION_STATUS(
       PARTITION_STATUS_TYPE *PARTITION_STATUS,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Partition modes: COLD_START, WARM_START, NORMAL, IDLE

**2.2 Space Partitioning**
----------------------------

Memory isolation prevents partitions from corrupting each other's data:

**MMU/MPU Configuration:**
- Each partition has isolated memory regions
- No shared writable memory between partitions (except via IPC)
- Read-only code/data regions allowed
- Stack/heap protected per partition

**Memory Layout Example:**

.. code-block:: text

   ┌─────────────────────────────────────┐ 0xFFFFFFFF
   │        RTOS Kernel (Supervisor)      │
   ├─────────────────────────────────────┤
   │  Partition 1 (Code: RO, Data: RW)   │
   ├─────────────────────────────────────┤
   │  Partition 2 (Code: RO, Data: RW)   │
   ├─────────────────────────────────────┤
   │  Partition 3 (Code: RO, Data: RW)   │
   ├─────────────────────────────────────┤
   │         Shared Resources             │
   │  (IPC buffers, OS data structures)  │
   └─────────────────────────────────────┘ 0x00000000

**C Example - Partition Initialization:**

.. code-block:: c

   // Partition configuration (in Module Configuration Table)
   typedef struct {
       PARTITION_NAME_TYPE name;
       SYSTEM_ADDRESS_TYPE entry_point;
       MEMORY_RANGE_TYPE memory_regions[MAX_REGIONS];
       SYSTEM_TIME_TYPE duration;
       PARTITION_MODE_TYPE mode;
   } PARTITION_CONFIG;

   // Application entry point
   void partition_main(void) {
       // Initialize partition resources
       CREATE_PROCESS(...);
       CREATE_SAMPLING_PORT(...);
       
       // Start partition scheduling
       SET_PARTITION_MODE(NORMAL, &rc);
   }

================================================================================
3. APEX API — Core Services
================================================================================

**3.1 Partition Management**
------------------------------

.. code-block:: c

   // Set partition operating mode
   void SET_PARTITION_MODE(
       OPERATING_MODE_TYPE OPERATING_MODE,  // IDLE, COLD_START, WARM_START, NORMAL
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Get current partition status
   void GET_PARTITION_STATUS(
       PARTITION_STATUS_TYPE *PARTITION_STATUS,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   typedef struct {
       SYSTEM_TIME_TYPE PERIOD;
       SYSTEM_TIME_TYPE DURATION;
       PARTITION_ID_TYPE IDENTIFIER;
       LOCK_LEVEL_TYPE LOCK_LEVEL;
       OPERATING_MODE_TYPE OPERATING_MODE;
       START_CONDITION_TYPE START_CONDITION;
   } PARTITION_STATUS_TYPE;

**3.2 Process Management**
----------------------------

Processes run within partitions (multiple processes per partition allowed):

.. code-block:: c

   // Create a process
   void CREATE_PROCESS(
       PROCESS_ATTRIBUTE_TYPE *ATTRIBUTES,
       PROCESS_ID_TYPE *PROCESS_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   typedef struct {
       PROCESS_NAME_TYPE NAME;
       SYSTEM_ADDRESS_TYPE ENTRY_POINT;
       STACK_SIZE_TYPE STACK_SIZE;
       PRIORITY_TYPE BASE_PRIORITY;
       SYSTEM_TIME_TYPE PERIOD;
       SYSTEM_TIME_TYPE TIME_CAPACITY;
       DEADLINE_TYPE DEADLINE;
   } PROCESS_ATTRIBUTE_TYPE;
   
   // Start a process
   void START(
       PROCESS_ID_TYPE PROCESS_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Suspend self
   void PERIODIC_WAIT(RETURN_CODE_TYPE *RETURN_CODE);
   
   // Example: Periodic process
   void sensor_task(void) {
       while (1) {
           read_sensor_data();
           process_data();
           PERIODIC_WAIT(&rc);  // Wait for next period
       }
   }

**3.3 Time Management**
------------------------

.. code-block:: c

   // Get system time (nanoseconds since partition start)
   void GET_TIME(
       SYSTEM_TIME_TYPE *SYSTEM_TIME,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Delay process for specified duration
   void TIMED_WAIT(
       SYSTEM_TIME_TYPE DELAY_TIME,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Periodic wait (for periodic processes)
   void PERIODIC_WAIT(RETURN_CODE_TYPE *RETURN_CODE);
   
   // Example: 50ms periodic task
   PROCESS_ATTRIBUTE_TYPE attr = {
       .NAME = "ControlTask",
       .ENTRY_POINT = control_loop,
       .PERIOD = 50 * 1000000,  // 50 ms in nanoseconds
       .TIME_CAPACITY = 10 * 1000000,  // 10 ms budget
       .BASE_PRIORITY = 10,
       .DEADLINE = SOFT
   };

================================================================================
4. Inter-Partition Communication (IPC)
================================================================================

**4.1 Sampling Ports**
-----------------------

Latest-value communication (overwrites old data):

**Characteristics:**
- Unidirectional (source → destination)
- Non-blocking writes
- Reads get latest value (or stale if no new data)
- Low latency, deterministic
- Used for: Sensor data, control outputs, status

.. code-block:: c

   // Source partition - Create sampling port (write)
   void CREATE_SAMPLING_PORT(
       SAMPLING_PORT_NAME_TYPE SAMPLING_PORT_NAME,
       MESSAGE_SIZE_TYPE MAX_MESSAGE_SIZE,
       PORT_DIRECTION_TYPE PORT_DIRECTION,  // SOURCE or DESTINATION
       SYSTEM_TIME_TYPE REFRESH_PERIOD,
       SAMPLING_PORT_ID_TYPE *SAMPLING_PORT_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Write to sampling port
   void WRITE_SAMPLING_MESSAGE(
       SAMPLING_PORT_ID_TYPE SAMPLING_PORT_ID,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       MESSAGE_SIZE_TYPE LENGTH,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Destination partition - Read from sampling port
   void READ_SAMPLING_MESSAGE(
       SAMPLING_PORT_ID_TYPE SAMPLING_PORT_ID,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       MESSAGE_SIZE_TYPE *LENGTH,
       VALIDITY_TYPE *VALIDITY,  // VALID or INVALID
       RETURN_CODE_TYPE *RETURN_CODE
   );

**Example: Altitude Data Communication**

.. code-block:: c

   // Sensor partition (source)
   typedef struct {
       float altitude_ft;
       float rate_fpm;
       uint32_t timestamp;
   } AltitudeData;
   
   SAMPLING_PORT_ID_TYPE alt_port;
   
   void init_sensor_partition(void) {
       CREATE_SAMPLING_PORT(
           "ALTITUDE_OUT",
           sizeof(AltitudeData),
           SOURCE,
           50000000,  // 50ms refresh
           &alt_port,
           &rc
       );
   }
   
   void sensor_process(void) {
       AltitudeData data;
       while (1) {
           data.altitude_ft = read_pressure_altitude();
           data.rate_fpm = compute_rate();
           data.timestamp = get_timestamp();
           
           WRITE_SAMPLING_MESSAGE(alt_port, &data, sizeof(data), &rc);
           PERIODIC_WAIT(&rc);
       }
   }
   
   // Display partition (destination)
   SAMPLING_PORT_ID_TYPE alt_in_port;
   
   void init_display_partition(void) {
       CREATE_SAMPLING_PORT(
           "ALTITUDE_IN",
           sizeof(AltitudeData),
           DESTINATION,
           0,
           &alt_in_port,
           &rc
       );
   }
   
   void display_process(void) {
       AltitudeData data;
       MESSAGE_SIZE_TYPE len;
       VALIDITY_TYPE valid;
       
       while (1) {
           READ_SAMPLING_MESSAGE(alt_in_port, &data, &len, &valid, &rc);
           if (valid == VALID) {
               update_altitude_display(data.altitude_ft);
           }
           PERIODIC_WAIT(&rc);
       }
   }

**4.2 Queuing Ports**
----------------------

FIFO message queues with guaranteed delivery:

**Characteristics:**
- Unidirectional (source → destination)
- Blocking writes when queue full
- Blocking reads when queue empty
- No data loss if queue not full
- Used for: Events, commands, alarms

.. code-block:: c

   // Create queuing port
   void CREATE_QUEUING_PORT(
       QUEUING_PORT_NAME_TYPE QUEUING_PORT_NAME,
       MESSAGE_SIZE_TYPE MAX_MESSAGE_SIZE,
       MESSAGE_RANGE_TYPE MAX_NB_MESSAGE,
       PORT_DIRECTION_TYPE PORT_DIRECTION,
       QUEUING_DISCIPLINE_TYPE QUEUING_DISCIPLINE,  // FIFO or PRIORITY
       QUEUING_PORT_ID_TYPE *QUEUING_PORT_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Send message (blocks if queue full)
   void SEND_QUEUING_MESSAGE(
       QUEUING_PORT_ID_TYPE QUEUING_PORT_ID,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       MESSAGE_SIZE_TYPE LENGTH,
       SYSTEM_TIME_TYPE TIME_OUT,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Receive message (blocks if queue empty)
   void RECEIVE_QUEUING_MESSAGE(
       QUEUING_PORT_ID_TYPE QUEUING_PORT_ID,
       SYSTEM_TIME_TYPE TIME_OUT,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       MESSAGE_SIZE_TYPE *LENGTH,
       RETURN_CODE_TYPE *RETURN_CODE
   );

**Example: Alarm System**

.. code-block:: c

   typedef enum {
       ALARM_ENGINE_FIRE,
       ALARM_LOW_FUEL,
       ALARM_CABIN_PRESSURE,
       ALARM_HYDRAULIC_FAILURE
   } AlarmType;
   
   typedef struct {
       AlarmType type;
       uint8_t severity;  // 1=WARNING, 2=CAUTION, 3=CRITICAL
       uint32_t timestamp;
       char message[64];
   } AlarmMessage;
   
   // Monitoring partition (source)
   QUEUING_PORT_ID_TYPE alarm_out;
   
   void init_monitor(void) {
       CREATE_QUEUING_PORT(
           "ALARM_QUEUE_OUT",
           sizeof(AlarmMessage),
           10,  // Max 10 alarms queued
           SOURCE,
           PRIORITY,
           &alarm_out,
           &rc
       );
   }
   
   void raise_alarm(AlarmType type, uint8_t severity, const char* msg) {
       AlarmMessage alarm;
       alarm.type = type;
       alarm.severity = severity;
       alarm.timestamp = get_time();
       strncpy(alarm.message, msg, 63);
       alarm.message[63] = '\0';
       
       SEND_QUEUING_MESSAGE(alarm_out, &alarm, sizeof(alarm), INFINITE_TIME_VALUE, &rc);
   }
   
   // Display partition (destination)
   QUEUING_PORT_ID_TYPE alarm_in;
   
   void alarm_handler_process(void) {
       AlarmMessage alarm;
       MESSAGE_SIZE_TYPE len;
       
       while (1) {
           RECEIVE_QUEUING_MESSAGE(alarm_in, INFINITE_TIME_VALUE, &alarm, &len, &rc);
           
           // Display alarm based on severity
           switch (alarm.severity) {
               case 3:  // CRITICAL
                   display_master_caution();
                   sound_aural_warning();
                   break;
               case 2:  // CAUTION
                   display_caution_message(alarm.message);
                   break;
               case 1:  // WARNING
                   log_warning(alarm.message);
                   break;
           }
       }
   }

**4.3 Blackboards**
--------------------

Shared memory within a partition (intra-partition IPC):

.. code-block:: c

   // Create blackboard
   void CREATE_BLACKBOARD(
       BLACKBOARD_NAME_TYPE BLACKBOARD_NAME,
       MESSAGE_SIZE_TYPE MAX_MESSAGE_SIZE,
       BLACKBOARD_ID_TYPE *BLACKBOARD_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Display (atomic read, blocks if no data)
   void DISPLAY_BLACKBOARD(
       BLACKBOARD_ID_TYPE BLACKBOARD_ID,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       MESSAGE_SIZE_TYPE *LENGTH,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Read (non-blocking, may return empty)
   void READ_BLACKBOARD(
       BLACKBOARD_ID_TYPE BLACKBOARD_ID,
       SYSTEM_TIME_TYPE TIME_OUT,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       MESSAGE_SIZE_TYPE *LENGTH,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Clear blackboard
   void CLEAR_BLACKBOARD(
       BLACKBOARD_ID_TYPE BLACKBOARD_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );

================================================================================
5. Synchronization Services
================================================================================

**5.1 Semaphores**
-------------------

.. code-block:: c

   // Create semaphore
   void CREATE_SEMAPHORE(
       SEMAPHORE_NAME_TYPE SEMAPHORE_NAME,
       SEMAPHORE_VALUE_TYPE CURRENT_VALUE,
       SEMAPHORE_VALUE_TYPE MAXIMUM_VALUE,
       QUEUING_DISCIPLINE_TYPE QUEUING_DISCIPLINE,
       SEMAPHORE_ID_TYPE *SEMAPHORE_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Wait (P operation, decrement)
   void WAIT_SEMAPHORE(
       SEMAPHORE_ID_TYPE SEMAPHORE_ID,
       SYSTEM_TIME_TYPE TIME_OUT,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Signal (V operation, increment)
   void SIGNAL_SEMAPHORE(
       SEMAPHORE_ID_TYPE SEMAPHORE_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Example: Mutual exclusion
   SEMAPHORE_ID_TYPE mutex;
   
   void init_partition(void) {
       CREATE_SEMAPHORE("SHARED_RESOURCE_MUTEX", 1, 1, FIFO, &mutex, &rc);
   }
   
   void critical_section_user(void) {
       WAIT_SEMAPHORE(mutex, INFINITE_TIME_VALUE, &rc);
       // ... critical section ...
       access_shared_resource();
       SIGNAL_SEMAPHORE(mutex, &rc);
   }

**5.2 Events**
---------------

.. code-block:: c

   // Create event
   void CREATE_EVENT(
       EVENT_NAME_TYPE EVENT_NAME,
       EVENT_ID_TYPE *EVENT_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Set event (signal waiting processes)
   void SET_EVENT(
       EVENT_ID_TYPE EVENT_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Wait for event
   void WAIT_EVENT(
       EVENT_ID_TYPE EVENT_ID,
       SYSTEM_TIME_TYPE TIME_OUT,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Reset event
   void RESET_EVENT(
       EVENT_ID_TYPE EVENT_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );

================================================================================
6. Health Monitoring
================================================================================

**6.1 Partition-Level Health Monitoring**
-------------------------------------------

The RTOS monitors partition behavior and takes action on faults:

**Partition States:**
- NORMAL: Operating correctly
- ERROR_HANDLER: Error detected, custom handler executing
- FAILED: Unrecoverable error, partition stopped

**Error Handling:**

.. code-block:: c

   // Raise application error
   void RAISE_APPLICATION_ERROR(
       ERROR_CODE_TYPE ERROR_CODE,
       MESSAGE_ADDR_TYPE MESSAGE_ADDR,
       ERROR_MESSAGE_SIZE_TYPE LENGTH,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   // Partition error handler (called by RTOS on fault)
   void PARTITION_ERROR_HANDLER(
       ERROR_STATUS_TYPE *ERROR_STATUS
   ) {
       // Log error
       log_partition_error(ERROR_STATUS);
       
       // Attempt recovery based on error
       switch (ERROR_STATUS->ERROR_CODE) {
           case DEADLINE_MISSED:
               // Reset processes, restart partition
               SET_PARTITION_MODE(WARM_START, &rc);
               break;
           case APPLICATION_ERROR:
               // Application-specific recovery
               recover_from_app_error();
               break;
           case NUMERIC_ERROR:
               // Division by zero, overflow, etc.
               SET_PARTITION_MODE(COLD_START, &rc);
               break;
           default:
               // Unrecoverable, halt partition
               SET_PARTITION_MODE(IDLE, &rc);
               break;
       }
   }

**6.2 Process-Level Health Monitoring**
-----------------------------------------

.. code-block:: c

   // Get process status
   void GET_PROCESS_STATUS(
       PROCESS_ID_TYPE PROCESS_ID,
       PROCESS_STATUS_TYPE *PROCESS_STATUS,
       RETURN_CODE_TYPE *RETURN_CODE
   );
   
   typedef struct {
       SYSTEM_TIME_TYPE DEADLINE_TIME;
       PRIORITY_TYPE CURRENT_PRIORITY;
       PROCESS_STATE_TYPE PROCESS_STATE;  // DORMANT, READY, RUNNING, WAITING
       PROCESSOR_CORE_ID_TYPE ATTRIBUTES;
   } PROCESS_STATUS_TYPE;
   
   // Stop a misbehaving process
   void STOP(
       PROCESS_ID_TYPE PROCESS_ID,
       RETURN_CODE_TYPE *RETURN_CODE
   );

**6.3 Watchdog / Deadline Monitoring**

Processes can have hard deadlines. RTOS raises error if deadline missed:

.. code-block:: c

   PROCESS_ATTRIBUTE_TYPE attr = {
       .NAME = "FlightControl",
       .PERIOD = 20000000,  // 20ms
       .TIME_CAPACITY = 5000000,  // 5ms budget
       .DEADLINE = HARD  // Miss = partition error
   };

================================================================================
7. Module Configuration
================================================================================

**Module Configuration Table (XML):**

System integrators define partitions, scheduling, and IPC in XML configuration:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <ARINC_653_Module>
     <Module_Schedule>
       <Partition_Schedule>
         <Window PartitionName="FlightControl" Duration="10ms" Offset="0ms"/>
         <Window PartitionName="Navigation" Duration="20ms" Offset="10ms"/>
         <Window PartitionName="Display" Duration="15ms" Offset="30ms"/>
         <Window PartitionName="FlightControl" Duration="10ms" Offset="45ms"/>
       </Partition_Schedule>
       <MajorFrameDuration>100ms</MajorFrameDuration>
     </Module_Schedule>
     
     <Partition Name="FlightControl" Identifier="1">
       <Memory>
         <Region Type="CODE" BaseAddress="0x40000000" Size="2MB" Access="RO"/>
         <Region Type="DATA" BaseAddress="0x50000000" Size="1MB" Access="RW"/>
       </Memory>
       <Sampling_Port Name="ALTITUDE_IN" Direction="DESTINATION" MaxSize="128"/>
       <Sampling_Port Name="CONTROL_OUT" Direction="SOURCE" MaxSize="256"/>
     </Partition>
     
     <Partition Name="Navigation" Identifier="2">
       <Memory>
         <Region Type="CODE" BaseAddress="0x60000000" Size="4MB" Access="RO"/>
         <Region Type="DATA" BaseAddress="0x70000000" Size="2MB" Access="RW"/>
       </Memory>
     </Partition>
     
     <Channel Name="ALTITUDE_CHANNEL">
       <Source PartitionName="Sensors" PortName="ALTITUDE_OUT"/>
       <Destination PartitionName="FlightControl" PortName="ALTITUDE_IN"/>
       <Destination PartitionName="Display" PortName="ALT_DISPLAY"/>
     </Channel>
   </ARINC_653_Module>

================================================================================
8. Real-World Applications
================================================================================

**8.1 Boeing 787 Dreamliner**
-------------------------------

**Common Core System (CCS):**
- ARINC 653 IMA modules
- 16 common computing modules per aircraft
- VxWorks 653 RTOS
- ARINC 664 AFDX networking between modules
- Functions: Flight controls, displays, systems management
- Certification: DO-178C DAL A (flight critical partitions)

**8.2 Airbus A350 XWB**
------------------------

**Core Processing Input/Output Modules (CPIOMs):**
- ~21 CPIOM variants per aircraft
- ARINC 653 partitioning (VxWorks 653 or PikeOS)
- ARINC 600 3-MCU form factor
- 20+ partitions per CPIOM
- Functions: IMA consolidation of 50+ traditional LRUs
- 70% weight reduction vs A330 federated architecture

**Example Partitions:**
- Flight Management (DAL B)
- TCAS (DAL A)
- Weather Radar (DAL C)
- Cabin Pressure Control (DAL B)
- Display Management (DAL B)

**8.3 Military: F-35 Lightning II**
------------------------------------

**Vehicle Management Computer (VMC):**
- ARINC 653 partitioning
- INTEGRITY-178B RTOS
- Mission-critical and safety-critical partitions
- Sensor fusion, flight controls, weapons management

================================================================================
9. DO-178C Integration
================================================================================

**Certification Strategy:**

ARINC 653 enables **partition independence** for DO-178C certification:

**Key Benefits:**
1. **Partition-level certification:** Each partition certified independently
2. **Mixed DAL:** DAL A partition coexists with DAL C/D without interference
3. **Incremental updates:** Modify one partition without re-certifying others
4. **Reduced testing:** No need to test all combinations of partition states

**Requirements:**
- RTOS must be DO-178C certified (DAL A for hosting DAL A partitions)
- Configuration data must be verified (DO-178C DAL A)
- Partitioning demonstrated via testing (memory, timing isolation)
- Interference analysis required (CAST-32A guidance)

**DO-178C Objectives:**
- A-4.1: Partition design verification
- A-4.2: Partition implementation verification
- A-4.3: Partition requirements-based testing
- A-4.4: Partition boundary testing (isolation verification)

**Example Verification:**
- **Memory isolation test:** Attempt to write to another partition's memory → should fault
- **Timing isolation test:** One partition loops infinitely → others unaffected
- **IPC security test:** Send message larger than port buffer → should reject

================================================================================
10. Python Simulation Example
================================================================================

Simplified ARINC 653 simulator for understanding concepts:

.. code-block:: python

   import threading
   import time
   from collections import deque
   from dataclasses import dataclass
   from typing import Any, Optional
   
   @dataclass
   class SamplingPort:
       name: str
       max_size: int
       direction: str  # 'SOURCE' or 'DESTINATION'
       data: Optional[bytes] = None
       valid: bool = False
       lock: threading.Lock = None
       
       def __post_init__(self):
           self.lock = threading.Lock()
   
   @dataclass
   class QueuingPort:
       name: str
       max_size: int
       max_messages: int
       direction: str
       queue: deque = None
       lock: threading.Lock = None
       
       def __post_init__(self):
           self.queue = deque(maxlen=self.max_messages)
           self.lock = threading.Lock()
   
   class Partition:
       def __init__(self, name: str, duration_ms: int):
           self.name = name
           self.duration_ms = duration_ms
           self.sampling_ports = {}
           self.queuing_ports = {}
           self.processes = []
           
       def create_sampling_port(self, name: str, max_size: int, direction: str):
           port = SamplingPort(name, max_size, direction)
           self.sampling_ports[name] = port
           return port
       
       def create_queuing_port(self, name: str, max_size: int, max_msgs: int, direction: str):
           port = QueuingPort(name, max_size, max_msgs, direction)
           self.queuing_ports[name] = port
           return port
       
       def write_sampling(self, port_name: str, data: bytes):
           port = self.sampling_ports[port_name]
           with port.lock:
               port.data = data[:port.max_size]
               port.valid = True
       
       def read_sampling(self, port_name: str) -> tuple[Optional[bytes], bool]:
           port = self.sampling_ports[port_name]
           with port.lock:
               return port.data, port.valid
       
       def send_queuing(self, port_name: str, data: bytes):
           port = self.queuing_ports[port_name]
           with port.lock:
               if len(port.queue) < port.max_messages:
                   port.queue.append(data[:port.max_size])
                   return True
               return False  # Queue full
       
       def receive_queuing(self, port_name: str) -> Optional[bytes]:
           port = self.queuing_ports[port_name]
           with port.lock:
               if port.queue:
                   return port.queue.popleft()
               return None  # Queue empty
   
   class ARINC653Scheduler:
       def __init__(self, major_frame_ms: int):
           self.major_frame_ms = major_frame_ms
           self.schedule = []  # List of (partition, offset_ms, duration_ms)
           self.channels = {}  # IPC channel connections
           
       def add_partition_window(self, partition: Partition, offset_ms: int):
           self.schedule.append((partition, offset_ms, partition.duration_ms))
       
       def connect_sampling_channel(self, source_part: str, source_port: str,
                                     dest_part: str, dest_port: str):
           channel_name = f"{source_part}:{source_port}->{dest_part}:{dest_port}"
           self.channels[channel_name] = (source_part, source_port, dest_part, dest_port)
       
       def run_schedule(self):
           """Execute major frame schedule"""
           # Sort by offset
           schedule = sorted(self.schedule, key=lambda x: x[1])
           
           start_time = time.time()
           for partition, offset_ms, duration_ms in schedule:
               # Wait until offset time
               current_time = (time.time() - start_time) * 1000
               sleep_time = max(0, offset_ms - current_time)
               time.sleep(sleep_time / 1000.0)
               
               print(f"[{current_time:.1f}ms] Running {partition.name} for {duration_ms}ms")
               
               # Execute partition (simplified - just sleep for duration)
               time.sleep(duration_ms / 1000.0)
               
           # Transfer data via sampling port channels
           for channel, (src_part, src_port, dst_part, dst_port) in self.channels.items():
               # Find partitions
               src_partition = next(p for p, _, _ in schedule if p.name == src_part)
               dst_partition = next(p for p, _, _ in schedule if p.name == dst_part)
               
               # Transfer data
               data, valid = src_partition.read_sampling(src_port)
               if valid:
                   dst_partition.sampling_ports[dst_port].data = data
                   dst_partition.sampling_ports[dst_port].valid = True
   
   # Example usage
   if __name__ == "__main__":
       # Create partitions
       flight_control = Partition("FlightControl", duration_ms=10)
       navigation = Partition("Navigation", duration_ms=20)
       display = Partition("Display", duration_ms=15)
       
       # Create IPC ports
       nav_alt_out = navigation.create_sampling_port("ALT_OUT", 128, "SOURCE")
       fc_alt_in = flight_control.create_sampling_port("ALT_IN", 128, "DESTINATION")
       disp_alt_in = display.create_sampling_port("ALT_DISP", 128, "DESTINATION")
       
       # Create scheduler (100ms major frame)
       scheduler = ARINC653Scheduler(major_frame_ms=100)
       scheduler.add_partition_window(flight_control, offset_ms=0)
       scheduler.add_partition_window(navigation, offset_ms=10)
       scheduler.add_partition_window(display, offset_ms=30)
       scheduler.add_partition_window(flight_control, offset_ms=50)  # Second window
       
       # Connect channels
       scheduler.connect_sampling_channel("Navigation", "ALT_OUT", "FlightControl", "ALT_IN")
       scheduler.connect_sampling_channel("Navigation", "ALT_OUT", "Display", "ALT_DISP")
       
       # Run major frame
       scheduler.run_schedule()

================================================================================
11. Exam Preparation — 5 Comprehensive Questions
================================================================================

**Question 1: Partition Scheduling (15 points)**

Given the following ARINC 653 partition configuration:

- Partition A: Duration 20ms, Windows at 0ms and 60ms
- Partition B: Duration 30ms, Window at 20ms  
- Partition C: Duration 10ms, Window at 50ms
- Major Frame: 100ms

a) Draw the timeline showing all partition windows (5 pts)
b) Calculate the CPU utilization (5 pts)
c) If Partition A has a periodic process with 40ms period and 8ms execution time, will it meet its deadline in each major frame? Explain. (5 pts)

**Answer:**

a) Timeline:

.. code-block:: text

   0    20   50   60   80        100 ms
   |--A--|--B--|--C--|--A--|...Idle...|
   20ms  30ms  10ms  20ms      20ms

b) CPU Utilization:
   - Partition A: 20ms + 20ms = 40ms
   - Partition B: 30ms
   - Partition C: 10ms
   - Total: 80ms out of 100ms = **80% CPU utilization**

c) Partition A process analysis:
   - Period: 40ms, Execution time: 8ms
   - In first window (0-20ms): Process can execute for 8ms → Meets deadline
   - Process next release: 40ms (during idle time, not in A's window)
   - Process misses second execution in this major frame
   - **Conclusion:** Process will miss deadlines. Need to adjust schedule or process period.

---

**Question 2: Sampling vs Queuing Ports (10 points)**

a) Explain the difference between ARINC 653 sampling ports and queuing ports (4 pts)
b) For each scenario, choose sampling or queuing port and justify:
   - Scenario 1: Sending current airspeed (updated 50 times/second) to flight control (3 pts)
   - Scenario 2: Sending fault codes from engine monitor to maintenance system (3 pts)

**Answer:**

a) Differences:
   - **Sampling Port:** Latest-value semantics. Writes overwrite old data, reads get most recent. Non-blocking. Used for periodic sensor data where only latest value matters.
   - **Queuing Port:** FIFO message queue. All messages preserved (if queue not full). Blocking on full queue. Used for events/commands where no messages should be lost.

b) Port selection:
   - **Scenario 1:** **Sampling Port**
     - Airspeed updated 50 times/sec (every 20ms)
     - Flight control only needs latest value
     - Old airspeed readings irrelevant
     - Low latency critical
   
   - **Scenario 2:** **Queuing Port**
     - Fault codes are events, not continuous data
     - Cannot lose any fault notifications
     - Maintenance system may process slower than faults generated
     - FIFO ensures all faults logged in order

---

**Question 3: Health Monitoring & Error Recovery (12 points)**

A partition hosts two processes:
- Process 1: Periodic, 50ms period, 10ms execution budget, HARD deadline
- Process 2: Aperiodic, triggered by queuing port messages

Describe what happens in these fault scenarios:
a) Process 1 executes for 12ms (exceeds budget) (4 pts)
b) Process 1 calls undefined function (causes exception) (4 pts)
c) Process 2 writes to NULL pointer (4 pts)

**Answer:**

a) **Budget overrun (12ms > 10ms):**
   - RTOS detects execution time exceeded TIME_CAPACITY
   - Raises DEADLINE_MISSED error
   - Partition transitions to ERROR state
   - PARTITION_ERROR_HANDLER() called
   - Error handler can:
     - Log error for diagnostics
     - Restart process (WARM_START)
     - Reconfigure if systematic problem
   - If HARD deadline, may trigger module-level health monitoring

b) **Undefined function / illegal instruction:**
   - Memory exception or invalid opcode
   - Raises ILLEGAL_REQUEST or MEMORY_VIOLATION error
   - Partition ERROR_HANDLER invoked
   - Typical recovery:
     - COLD_START (full partition reset)
     - If repeated, IDLE mode (partition disabled)
   - Space partitioning prevents affecting other partitions

c) **NULL pointer write:**
   - MMU/MPU detects invalid memory access
   - MEMORY_VIOLATION error raised
   - Process stopped immediately (cannot corrupt other memory)
   - Partition ERROR_HANDLER decides:
     - Restart misbehaving process only
     - Or full partition COLD_START
   - Other partitions unaffected (space isolation)

---

**Question 4: DO-178C Certification (8 points)**

An IMA module hosts:
- Partition 1: Flight control (DAL A)
- Partition 2: Weather display (DAL C)

a) What Design Assurance Level must the ARINC 653 RTOS kernel be certified to? Why? (4 pts)
b) If Partition 2 is modified, must Partition 1 be re-certified? Explain the conditions. (4 pts)

**Answer:**

a) **RTOS DAL:** **DAL A**
   - RTOS kernel is shared by all partitions
   - Highest DAL partition dictates kernel DAL
   - Partition 1 (DAL A) requires DAL A kernel
   - RTOS must meet DO-178C DAL A objectives (MC/DC coverage, etc.)
   - Configuration data also DAL A

b) **Re-certification of Partition 1:**
   - **Normally NO**, due to partition independence
   - **Conditions for no re-cert:**
     - No changes to Partition 1 code/requirements
     - No changes to module configuration (schedule, memory map)
     - Partition isolation verified (CAST-32A testing)
     - No shared resources modified
   - **Must re-cert if:**
     - Module configuration changes affecting Partition 1 schedule
     - RTOS updated
     - New IPC channels added between partitions
     - Interference analysis shows new coupling

---

**Question 5: IMA Architecture Design (10 points)**

Design an ARINC 653 configuration for these avionics functions:
- Flight Management System (FMS): 40ms processing, DAL B
- TCAS: 50ms processing, DAL A
- Weather Radar: 30ms processing, DAL C
- System Monitoring: 20ms processing, DAL D

Requirements:
- Major frame ≤ 200ms
- Minimum 10ms between windows of same partition
- CPU utilization < 85%

Provide:
a) Partition windows schedule (6 pts)
b) CPU utilization calculation (2 pts)
c) IPC design for TCAS needing altitude from FMS (2 pts)

**Answer:**

a) **Schedule (200ms major frame):**

.. code-block:: text

   Time:  0    40   90   130  170  200 ms
   Part:  |FMS |TCAS|FMS |Radar|Mon |Idle|
   Dur:   40ms 50ms 40ms 30ms  20ms 20ms
   
   - FMS (DAL B): Windows at 0ms and 90ms (40ms each, 90ms apart ✓)
   - TCAS (DAL A): Window at 40ms (50ms)
   - Weather (DAL C): Window at 130ms (30ms)
   - Monitor (DAL D): Window at 170ms (20ms)

b) **CPU Utilization:**
   - Total partition time: 40+50+40+30+20 = 180ms
   - Utilization: 180/200 = **90%**
   - ❌ Exceeds 85% requirement
   - **Fix:** Extend major frame to 240ms → 180/240 = 75% ✓

c) **IPC Design (TCAS ← FMS altitude):**
   - **Sampling Port Channel:**
     - FMS creates SOURCE port "ALTITUDE_OUT" (write current altitude)
     - TCAS creates DESTINATION port "ALTITUDE_IN" (read altitude)
     - Refresh period: 40ms (FMS update rate)
     - Message: struct { float altitude_ft; uint32_t timestamp; }
   - **Justification:** Sampling port appropriate because TCAS needs latest altitude value, not historical data

================================================================================
12. Completion Checklist
================================================================================

Master ARINC 653 by completing these objectives:

**Foundation (Concepts):**
□ Understand time vs space partitioning
□ Know partition lifecycle (COLD_START, WARM_START, NORMAL, IDLE)
□ Understand major frame and partition windows
□ Know process vs partition distinction

**APEX API:**
□ Create/start processes (CREATE_PROCESS, START)
□ Implement periodic processes (PERIODIC_WAIT)
□ Use time services (GET_TIME, TIMED_WAIT)
□ Create sampling ports (CREATE_SAMPLING_PORT)
□ Implement queuing ports (CREATE_QUEUING_PORT)
□ Use semaphores for mutual exclusion
□ Understand blackboards vs sampling ports

**IPC Design:**
□ Choose sampling vs queuing port for scenarios
□ Design multi-partition communication
□ Handle data staleness (sampling port validity)
□ Avoid queue overflow (queuing port sizing)

**Health Monitoring:**
□ Implement partition error handler
□ Handle process faults gracefully
□ Understand deadline monitoring (HARD vs SOFT)
□ Design fault recovery strategies

**Configuration:**
□ Read/write module configuration XML
□ Design partition schedule (minimize fragmentation)
□ Calculate CPU utilization
□ Allocate memory regions per partition

**Certification:**
□ Understand DO-178C integration
□ Know partition independence criteria
□ Perform isolation testing (memory, timing)
□ Apply CAST-32A guidance

**Hands-On:**
□ Implement sampling port example in C
□ Create partition scheduling simulator
□ Design IMA system with 3+ partitions
□ Debug partition errors (using RTOS tools)

================================================================================
13. Key Takeaways
================================================================================

1. **ARINC 653 = Standardized IMA:** Enables multiple applications to share hardware safely via partitioning

2. **Time Partitioning:** Fixed schedule ensures no partition steals CPU time from others (determinism)

3. **Space Partitioning:** MMU/MPU isolation prevents memory corruption across partitions (safety)

4. **APEX API:** Portable application interface works across VxWorks 653, PikeOS, INTEGRITY-178B, etc.

5. **Sampling vs Queuing:** Sampling = latest-value (sensors), Queuing = FIFO events (alarms, commands)

6. **Health Monitoring:** Two-level (partition and process) with configurable error recovery

7. **DO-178C Synergy:** Partition independence reduces certification costs for mixed-DAL systems

8. **IMA Benefits:** 70% weight reduction, 50% cost savings vs federated avionics

9. **Real-World Use:** Boeing 787 CCS, Airbus A350 CPIOM, F-35 VMC all use ARINC 653

10. **2026 Trends:** Multicore (Part 4), security extensions (Part 5), TSN integration for networking

================================================================================
References & Further Reading
================================================================================

**Standards:**
- SAE AS6653 (ARINC 653 Parts 0-5)
- EUROCAE ED-237 (European equivalent)
- DO-178C (Software certification)
- CAST-32A (Multicore interference mitigation)

**Books:**
- "Real-Time Systems Design and Analysis" by Phillip A. Laplante
- "Avionics Development and Implementation" by Cary R. Spitzer
- "Integrated Modular Avionics" by Dr. Michael S. Hammons

**RTOS Vendors:**
- Wind River VxWorks 653
- SYSGO PikeOS
- Green Hills INTEGRITY-178B
- DDC-I Deos
- Lynx MOSA.ic

**Aircraft:**
- Boeing 787 Common Core System (CCS) documentation
- Airbus A350/A380 CPIOM architecture
- F-35 Vehicle Management Computer (VMC)

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Standards:** SAE AS6653, EUROCAE ED-237, DO-178C

================================================================================
