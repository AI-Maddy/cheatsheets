🔒 **ARINC 653 PARTITIONING — Time & Space Isolation for IMA**
═══════════════════════════════════════════════════════════════════

**Context:** Integrated Modular Avionics (IMA) partitioning standard
**Focus:** Time/space partitioning, APEX API, health monitoring
**Standards:** ARINC 653, DO-178C, RTCA DO-297

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — ARINC 653 IN 60 SECONDS**
───────────────────────────────────────

**Core Concepts:**

::

    Partition = Isolated runtime environment
    
    Time Partitioning:  CPU time slices (fixed schedule)
    Space Partitioning: Memory isolation (MMU protection)
    
    APEX API: Standard interface for partition management

**Partition Schedule Example:**

::

    Major Frame: 100ms (repeating)
    
    |─ P1 (20ms) ─|─ P2 (30ms) ─|─ P3 (10ms) ─|─ P4 (40ms) ─|
    0ms          20ms          50ms          60ms         100ms
                                                           ↓
                                                    Repeat from 0ms

**Benefits:**

- ✅ Fault isolation (crash in P1 doesn't affect P2)
- ✅ Mixed criticality (DAL A + DAL D on same hardware)
- ✅ Independent certification
- ✅ Cost/weight reduction (fewer boxes)

════════════════════════════════════════════════════════════════════

📖 **1. TIME PARTITIONING**
═══════════════════════════

**1.1 Major Frame**
------------------

**Definition:** Fixed repeating schedule for all partitions

**Example Schedule:**

.. code-block:: xml

    <Module_Schedule MajorFrameDuration="100ms">
      <Partition_Schedule PartitionId="1" 
                          Start="0ms" 
                          Duration="20ms" 
                          PeriodDuration="100ms"/>
      <Partition_Schedule PartitionId="2" 
                          Start="20ms" 
                          Duration="30ms" 
                          PeriodDuration="100ms"/>
      <Partition_Schedule PartitionId="3" 
                          Start="50ms" 
                          Duration="10ms" 
                          PeriodDuration="100ms"/>
      <Partition_Schedule PartitionId="4" 
                          Start="60ms" 
                          Duration="40ms" 
                          PeriodDuration="100ms"/>
    </Module_Schedule>

**Timeline Visualization:**

::

    Major Frame (100ms)
    ┌─────────────────────────────────────────────────────┐
    │                                                       │
    │  FMS    │    IFE     │Nav│    Comm                  │
    │ (20ms)  │   (30ms)   │10 │   (40ms)                │
    │  DAL A  │   DAL D    │ms │   DAL C                  │
    │         │            │   │                           │
    └─────────┴────────────┴───┴───────────────────────────┘
    0        20           50  60                         100
                                                          ↓
                                                    [Repeat]

**1.2 Partition Windows**
-------------------------

**Rules:**

- Partition executes ONLY during its time window
- Preempted at window boundary (hard limit)
- Scheduler enforces timing in hardware timer

**Consequences:**

- **Determinism:** FMS always gets exactly 20ms every 100ms
- **No interference:** IFE overrun cannot steal FMS time
- **Predictable:** WCET analysis simplified

**1.3 Aperiodic Partitions**
----------------------------

**Definition:** Partition that runs less frequently

.. code-block:: xml

    <Partition_Schedule PartitionId="5" 
                        Start="0ms" 
                        Duration="10ms" 
                        PeriodDuration="500ms"/>
    <!-- Runs only in frames 0, 500, 1000, 1500... -->

════════════════════════════════════════════════════════════════════

📖 **2. SPACE PARTITIONING**
════════════════════════════

**2.1 Memory Protection**
-------------------------

**Mechanism:** Hardware MMU (Memory Management Unit)

**Partition Memory Layout:**

::

    ┌─────────────────────────────────────────────┐
    │  Partition 1 (FMS)                          │
    │  Code:    0x10000000 - 0x10100000 (1 MB)   │
    │  Data:    0x20000000 - 0x20200000 (2 MB)   │
    │  Stack:   0x30000000 - 0x30010000 (64 KB)  │
    └─────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────┐
    │  Partition 2 (IFE)                          │
    │  Code:    0x10200000 - 0x10600000 (4 MB)   │
    │  Data:    0x20400000 - 0x20C00000 (8 MB)   │
    │  Stack:   0x30020000 - 0x30040000 (128 KB) │
    └─────────────────────────────────────────────┘
    
    [No overlap! MMU enforces boundaries]

**2.2 MMU Configuration**
-------------------------

**Example (ARM Cortex-A53):**

.. code-block:: c

    // Set up MMU for Partition 1
    void configure_mmu_partition1(void) {
        // Code region: Read-only, Execute
        mmu_map_region(0x10000000, 0x10100000, 
                      MMU_READ | MMU_EXEC);
        
        // Data region: Read-write, No-execute
        mmu_map_region(0x20000000, 0x20200000, 
                      MMU_READ | MMU_WRITE);
        
        // Stack region: Read-write, No-execute
        mmu_map_region(0x30000000, 0x30010000, 
                      MMU_READ | MMU_WRITE);
        
        // Enable MMU
        enable_mmu();
    }

**2.3 Fault Handling**
----------------------

**Memory Access Violation:**

::

    Partition 1 attempts: write to 0x20400000 (Partition 2 memory)
           ↓
    MMU detects violation
           ↓
    Hardware exception
           ↓
    Health Monitor invoked
           ↓
    Partition 1 terminated (depends on HM table)

════════════════════════════════════════════════════════════════════

📖 **3. PARTITION MANAGEMENT**
══════════════════════════════

**3.1 Partition States**
------------------------

**State Machine:**

::

    [COLD_START] ←──────┐
         ↓              │
    [WARM_START] ←──┐   │
         ↓          │   │
    [NORMAL] ───────┤   │
         ↓          │   │
    [IDLE]          │   │
         ↓          │   │
    [FAULT] ────────┴───┘

**State Descriptions:**

+---------------+------------------------------------------------+
| **State**     | **Description**                                |
+===============+================================================+
| COLD_START    | Initial boot, all variables initialized       |
+---------------+------------------------------------------------+
| WARM_START    | Restart after fault, some state preserved     |
+---------------+------------------------------------------------+
| NORMAL        | Active execution                               |
+---------------+------------------------------------------------+
| IDLE          | Finished work, waiting for next window        |
+---------------+------------------------------------------------+
| FAULT         | Error detected, awaiting recovery action      |
+---------------+------------------------------------------------+

**3.2 Health Monitoring**
-------------------------

**Health Monitor (HM) Table:**

.. code-block:: xml

    <HM_Table PartitionId="1">
      <Error Code="DEADLINE_MISSED" 
             Level="PARTITION" 
             Action="WARM_RESTART"/>
      <Error Code="MEMORY_VIOLATION" 
             Level="MODULE" 
             Action="COLD_RESTART"/>
      <Error Code="STACK_OVERFLOW" 
             Level="PARTITION" 
             Action="WARM_RESTART"/>
      <Error Code="DIVIDE_BY_ZERO" 
             Level="PROCESS" 
             Action="IGNORE"/>
    </HM_Table>

**Recovery Actions:**

- **IGNORE:** Log error, continue
- **WARM_RESTART:** Restart partition (preserve config)
- **COLD_RESTART:** Restart partition (reinitialize)
- **MODULE_RESTART:** Restart entire IMA module

════════════════════════════════════════════════════════════════════

📖 **4. INTER-PARTITION COMMUNICATION**
═══════════════════════════════════════

**4.1 Communication Restrictions**
----------------------------------

**Rule:** Partitions CANNOT directly access each other's memory

**Allowed Mechanisms:**

1. **Sampling Ports** (periodic, latest value)
2. **Queuing Ports** (FIFO message queue)
3. **Blackboard** (shared memory with mutex)

**4.2 Sampling Ports**
---------------------

**Concept:** Unacknowledged, periodic data (e.g., sensor readings)

**Characteristics:**

- **Write:** Always succeeds (overwrites old value)
- **Read:** Returns latest value (may be stale)
- **No blocking**

**APEX API:**

.. code-block:: c

    // Sender (Partition 1)
    SAMPLING_PORT_ID_TYPE port_id;
    RETURN_CODE_TYPE rc;
    
    CREATE_SAMPLING_PORT("ALTITUDE_DATA", 
                         sizeof(double), 
                         DESTINATION, 
                         100, // Refresh period (ms)
                         &port_id, 
                         &rc);
    
    double altitude = 35000.0;
    WRITE_SAMPLING_MESSAGE(port_id, 
                          (MESSAGE_ADDR_TYPE)&altitude, 
                          sizeof(double), 
                          &rc);
    
    // Receiver (Partition 2)
    SAMPLING_PORT_ID_TYPE port_id;
    double altitude;
    MESSAGE_SIZE_TYPE length;
    VALIDITY_TYPE validity;
    
    CREATE_SAMPLING_PORT("ALTITUDE_DATA", 
                         sizeof(double), 
                         SOURCE, 
                         100, 
                         &port_id, 
                         &rc);
    
    READ_SAMPLING_MESSAGE(port_id, 
                         (MESSAGE_ADDR_TYPE)&altitude, 
                         &length, 
                         &validity, 
                         &rc);
    
    if (validity == VALID) {
        printf("Altitude: %.0f ft\n", altitude);
    }

**4.3 Queuing Ports**
--------------------

**Concept:** Acknowledged, queued messages (e.g., commands)

**Characteristics:**

- **Write:** Blocks if queue full
- **Read:** Blocks if queue empty
- **FIFO ordering**

**APEX API:**

.. code-block:: c

    // Sender
    QUEUING_PORT_ID_TYPE port_id;
    
    CREATE_QUEUING_PORT("COMMAND_QUEUE", 
                        256, // Max message size
                        10,  // Queue depth
                        DESTINATION, 
                        FIFO, 
                        &port_id, 
                        &rc);
    
    char command[] = "SET_HEADING 270";
    SEND_QUEUING_MESSAGE(port_id, 
                        (MESSAGE_ADDR_TYPE)command, 
                        strlen(command), 
                        0, // Timeout (infinite)
                        &rc);
    
    // Receiver
    char buffer[256];
    MESSAGE_SIZE_TYPE length;
    
    RECEIVE_QUEUING_MESSAGE(port_id, 
                           0, // Timeout (infinite)
                           (MESSAGE_ADDR_TYPE)buffer, 
                           &length, 
                           &rc);
    
    printf("Command: %s\n", buffer);

**4.4 Blackboard**
-----------------

**Concept:** Shared memory with mutex protection

.. code-block:: c

    BLACKBOARD_ID_TYPE bb_id;
    
    CREATE_BLACKBOARD("SHARED_CONFIG", 
                     1024, // Size
                     &bb_id, 
                     &rc);
    
    // Write
    char config[] = "mode=AUTO,speed=250";
    DISPLAY_BLACKBOARD(bb_id, 
                      (MESSAGE_ADDR_TYPE)config, 
                      strlen(config), 
                      &rc);
    
    // Read
    char buffer[1024];
    MESSAGE_SIZE_TYPE length;
    READ_BLACKBOARD(bb_id, 
                   0, // Timeout
                   (MESSAGE_ADDR_TYPE)buffer, 
                   &length, 
                   &rc);

════════════════════════════════════════════════════════════════════

📖 **5. APEX API OVERVIEW**
═══════════════════════════

**5.1 Service Categories**
--------------------------

+------------------------+----------------------------------+
| **Category**           | **Services**                     |
+========================+==================================+
| Partition Management   | GET_PARTITION_STATUS             |
+------------------------+----------------------------------+
| Process Management     | CREATE_PROCESS, START, STOP      |
+------------------------+----------------------------------+
| Time Management        | PERIODIC_WAIT, GET_TIME          |
+------------------------+----------------------------------+
| Communication          | Sampling/Queuing ports           |
+------------------------+----------------------------------+
| Synchronization        | Semaphores, Events               |
+------------------------+----------------------------------+
| Health Monitoring      | RAISE_APPLICATION_ERROR          |
+------------------------+----------------------------------+

**5.2 Process Management**
--------------------------

.. code-block:: c

    #include <apex.h>
    
    void sensor_task(void) {
        while (1) {
            double temp = read_temperature();
            printf("Temperature: %.2f°C\n", temp);
            
            PERIODIC_WAIT();  // Wait for next period
        }
    }
    
    int main(void) {
        PROCESS_ID_TYPE proc_id;
        RETURN_CODE_TYPE rc;
        
        // Create periodic process
        CREATE_PROCESS(
            "SENSOR_TASK",
            sensor_task,
            32768,              // Stack size
            50,                 // Base priority
            100 * 1000000,      // Period (100ms in ns)
            0,                  // Time capacity
            PERIODIC,
            &proc_id,
            &rc
        );
        
        // Start process
        START(proc_id, &rc);
        
        // Start partition
        SET_PARTITION_MODE(NORMAL, &rc);
        
        return 0;
    }

**5.3 Time Services**
--------------------

.. code-block:: c

    // Get system time
    SYSTEM_TIME_TYPE time;
    GET_TIME(&time, &rc);
    printf("System time: %lld ns\n", time);
    
    // Periodic wait
    void periodic_task(void) {
        while (1) {
            do_work();
            PERIODIC_WAIT();  // Sleep until next period
        }
    }
    
    // Timed wait
    TIMED_WAIT(50 * 1000000, &rc);  // Wait 50ms

════════════════════════════════════════════════════════════════════

📖 **6. SAFETY CERTIFICATION**
══════════════════════════════

**6.1 DO-178C Implications**
----------------------------

**Benefit:** Change isolation

**Without ARINC 653:**

::

    Change IFE app → Recertify ENTIRE system (FMS + IFE + Nav + Comm)
    Cost: $10M+, 18+ months

**With ARINC 653:**

::

    Change IFE app → Recertify ONLY IFE partition
    Cost: $500K, 3 months

**6.2 Interference Analysis**
-----------------------------

**Required Demonstration:**

1. **Time partitioning enforced** - CPU time cannot be stolen
2. **Space partitioning enforced** - Memory cannot be corrupted
3. **Resource isolation** - I/O devices properly partitioned
4. **Error containment** - Faults don't propagate

**Test Case Example:**

.. code-block:: c

    // Test: IFE partition cannot access FMS memory
    void test_memory_isolation(void) {
        volatile uint32_t *fms_memory = (uint32_t *)0x20000000;
        
        // Attempt illegal write
        *fms_memory = 0xDEADBEEF;  // Should trigger MMU fault
        
        // If we reach here, FAIL
        printf("FAIL: Memory isolation violated!\n");
    }

**Expected Result:** MMU fault, partition terminated by HM

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
═════════════════════════

**Q1:** Explain time partitioning and why it's critical for mixed-criticality systems.

**A1:**

**Time Partitioning:** CPU divided into fixed time windows assigned to partitions

**Example:**

::

    Major Frame: 100ms
    FMS (DAL A):  20ms window
    IFE (DAL D):  30ms window

**Why Critical:**

1. **Determinism:** FMS always gets exactly 20ms (predictable WCET)
2. **Fault isolation:** IFE infinite loop cannot steal FMS time
3. **Independent certification:** Change IFE without recertifying FMS
4. **Mixed criticality:** DAL A and DAL D coexist safely

**Without time partitioning:** IFE bug → FMS starvation → loss of aircraft

────────────────────────────────────────────────────────────────────

**Q2:** Compare sampling ports vs queuing ports.

**A2:**

**Sampling Ports:**

- **Use case:** Periodic sensor data (altitude, airspeed)
- **Semantics:** Latest value only (old data discarded)
- **Blocking:** Never blocks
- **Reliability:** May miss updates

**Queuing Ports:**

- **Use case:** Commands, events (mode changes)
- **Semantics:** FIFO queue (all messages preserved)
- **Blocking:** Blocks if queue full/empty
- **Reliability:** Guaranteed delivery (within queue depth)

**Example Decision:**

- Temperature reading → Sampling (only latest matters)
- Autopilot command → Queuing (cannot lose commands)

────────────────────────────────────────────────────────────────────

**Q3:** What happens when a partition exceeds its time window?

**A3:**

**Scenario:** FMS partition has 20ms window, runs for 25ms

**ARINC 653 Behavior:**

1. **At 20ms:** Hardware timer interrupt fires
2. **Scheduler:** Forcibly preempts FMS partition
3. **State:** Save FMS context (registers, PC)
4. **Next partition:** IFE partition starts executing
5. **Health Monitor:** Logs DEADLINE_MISSED error

**HM Action (configurable):**

- **IGNORE:** Log warning, continue next frame
- **WARM_RESTART:** Restart FMS partition
- **COLD_RESTART:** Full reinitialization

**Key Point:** IFE partition is NEVER affected by FMS overrun

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand time partitioning concept
- [ ] Design partition schedule (major frame)
- [ ] Configure MMU for space partitioning
- [ ] Define health monitoring table
- [ ] Choose communication mechanism (sampling vs queuing)
- [ ] Implement APEX API calls
- [ ] Test partition isolation
- [ ] Verify time budget not exceeded
- [ ] Document partition interfaces
- [ ] Perform interference analysis
- [ ] Create DO-178C traceability matrix
- [ ] Validate fault containment
- [ ] Test health monitor recovery actions

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Time partitioning = CPU time slices** → Fixed schedule, deterministic, 
no interference

2️⃣ **Space partitioning = MMU enforcement** → Hardware-enforced memory isolation

3️⃣ **APEX API standardizes services** → Portable across ARINC 653 platforms

4️⃣ **Sampling ports for periodic data** → Latest value, non-blocking, suitable 
for sensors

5️⃣ **Queuing ports for commands** → FIFO queue, blocking, reliable delivery

6️⃣ **Health Monitor handles faults** → Configurable recovery actions per error type

7️⃣ **Independent certification is key** → Change one partition without 
recertifying others ($10M+ savings)

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **ARINC 653 PARTITIONING COMPLETE**
**Created:** January 14, 2026
**Coverage:** Time/Space Partitioning, APEX API, Health Monitoring, Certification

════════════════════════════════════════════════════════════════════
