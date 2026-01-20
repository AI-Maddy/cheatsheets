═══════════════════════════════════════════════════════════════════════
REAL-TIME OPERATING SYSTEMS (RTOS) - COMPREHENSIVE GUIDE
═══════════════════════════════════════════════════════════════════════

**MQX, ThreadX, Integrity, OSEK/VDX - Complete Reference**  
**Domain:** Embedded Systems ⚙️ | Real-Time Systems ⏱️ | Safety-Critical 🔒  
**Purpose:** Task scheduling, IPC, resource management, interrupt handling, RTOS comparison

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**RTOS** (Real-Time Operating System) provides deterministic task scheduling and resource management for time-critical embedded systems.

**Key Characteristics:**
- **Deterministic:** Guaranteed response time (hard real-time)
- **Preemptive:** Higher priority tasks interrupt lower priority
- **Minimal latency:** Interrupt response <10 µs
- **Small footprint:** 10-50 KB typical (vs Linux: 10+ MB)
- **Predictable:** Fixed execution time, no virtual memory

**Your RTOS Experience:**
- **MQX:** Kinetis K50, industrial gateways, motor control (primary)
- **ThreadX:** Multiple embedded systems projects
- **Integrity:** Avionics fuel controller (safety-critical, DO-178B)
- **MICORSAR:** Automotive ECU projects (AUTOSAR-compliant)

**Common Use Cases:**
- Avionics (flight control, engine management)
- Automotive (ECU, motor control, ADAS)
- Industrial automation (PLCs, motion control)
- Medical devices (pacemakers, ventilators)
- Robotics (servo control, sensor fusion)

═══════════════════════════════════════════════════════════════════════

🏗️ **1. RTOS FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**1.1 What is Real-Time?**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Real-Time ≠ Fast**

Real-time means **predictable**, not necessarily fast.

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │  Task Timing Requirements                               │
   ├─────────────────────────────────────────────────────────┤
   │                                                          │
   │  Event ──→ Process ──→ Response                         │
   │   (t0)      (Δt)        (t1)                            │
   │                                                          │
   │  Deadline: t1 - t0 ≤ T_max                              │
   │                                                          │
   │  Hard Real-Time:                                        │
   │    Missing deadline = SYSTEM FAILURE                    │
   │    Examples: Airbag, anti-lock brakes, flight control   │
   │                                                          │
   │  Soft Real-Time:                                        │
   │    Missing deadline = DEGRADED PERFORMANCE              │
   │    Examples: Video streaming, audio playback, UI        │
   │                                                          │
   │  Firm Real-Time:                                        │
   │    Missing deadline = DATA LOST (but system OK)         │
   │    Examples: Sensor sampling, network packets           │
   └─────────────────────────────────────────────────────────┘

**Examples:**

.. code-block:: text

   Hard Real-Time (MUST meet deadline):
   ─────────────────────────────────────
   • Airbag deployment: 15 ms (crash to inflate)
   • Anti-lock brakes: 10 ms (wheel lock detection to release)
   • Flight control: 5 ms (sensor to actuator)
   • Engine control: 1 ms (crankshaft position to fuel injection)
   
   Soft Real-Time (should meet deadline):
   ──────────────────────────────────────
   • Video frame: 16.7 ms (60 fps) - dropped frame OK
   • Audio sample: 10 ms - occasional glitch acceptable
   • UI response: 100 ms - user notices lag but functional
   
   Non-Real-Time (no timing guarantee):
   ────────────────────────────────────
   • File download: seconds to minutes
   • Database query: variable response time
   • Batch processing: hours to days

**1.2 RTOS vs GPOS (General Purpose OS)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌──────────────────────┬─────────────────────┬─────────────────────┐
   │  Feature             │  RTOS               │  Linux/Windows      │
   ├──────────────────────┼─────────────────────┼─────────────────────┤
   │  Scheduling          │  Preemptive priority│  Fair scheduling    │
   │                      │  Fixed priorities   │  Dynamic priorities │
   │                      │                     │                     │
   │  Latency             │  <10 µs deterministic│ 100 µs - 10 ms     │
   │                      │                     │  (non-deterministic)│
   │                      │                     │                     │
   │  Footprint           │  10-50 KB           │  10-500 MB          │
   │                      │                     │                     │
   │  Memory Management   │  Static allocation  │  Virtual memory     │
   │                      │  No paging          │  Demand paging      │
   │                      │                     │                     │
   │  Context Switch      │  1-5 µs             │  10-100 µs          │
   │                      │                     │                     │
   │  Interrupt Response  │  <1 µs              │  10-100 µs          │
   │                      │                     │                     │
   │  Certification       │  DO-178, ISO 26262  │  Not certifiable    │
   │                      │                     │                     │
   │  Development Cost    │  License: $10K-50K  │  Free (Linux)       │
   │                      │                     │                     │
   │  Ecosystem           │  Vendor-specific    │  Massive ecosystem  │
   └──────────────────────┴─────────────────────┴─────────────────────┘

**When to Use RTOS:**

✅ **Use RTOS when:**
- Hard real-time requirements (flight control, brakes)
- Deterministic response critical (motor control)
- Small memory footprint needed (<1 MB RAM)
- Safety certification required (DO-178B/C, ISO 26262)
- Power constraints (low-power microcontrollers)
- Bare-metal CPU (no MMU)

❌ **Don't use RTOS when:**
- Soft real-time acceptable (multimedia)
- Need large ecosystem (web server, databases)
- Frequent updates required (security patches)
- Multi-user environment
- File system intensive
- Network-heavy application

**1.3 RTOS Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~

**Layered Architecture:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │  Application Layer                                      │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
   │  │  Task 1  │  │  Task 2  │  │  Task 3  │             │
   │  │ (High P) │  │ (Med P)  │  │ (Low P)  │             │
   │  └──────────┘  └──────────┘  └──────────┘             │
   └──────────────────────────┬──────────────────────────────┘
                              │ API Calls
   ┌──────────────────────────▼──────────────────────────────┐
   │  RTOS Services Layer                                    │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
   │  │  Task    │  │   IPC    │  │  Memory  │             │
   │  │  Mgmt    │  │ (queues, │  │  Mgmt    │             │
   │  │          │  │semaphores)│  │          │             │
   │  └──────────┘  └──────────┘  └──────────┘             │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
   │  │  Timer   │  │ Interrupt│  │  Device  │             │
   │  │  Mgmt    │  │  Mgmt    │  │  Drivers │             │
   │  └──────────┘  └──────────┘  └──────────┘             │
   └──────────────────────────┬──────────────────────────────┘
                              │ Kernel Calls
   ┌──────────────────────────▼──────────────────────────────┐
   │  Kernel (Scheduler + Dispatcher)                        │
   │  • Priority-based preemptive scheduling                 │
   │  • Context switching                                    │
   │  • Interrupt handling (ISR → Task)                      │
   │  • Tick timer (system clock)                            │
   └──────────────────────────┬──────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │  Hardware Abstraction Layer (HAL)                       │
   │  • CPU-specific code (ARM Cortex-M, A, R)               │
   │  • Interrupt vector table                               │
   │  • Low-level I/O                                        │
   └──────────────────────────┬──────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │  Hardware (MCU/SoC)                                     │
   │  • ARM Cortex-M4 (Kinetis K50)                          │
   │  • ARM Cortex-R5 (Automotive)                           │
   │  • ARM Cortex-A (Application processor)                 │
   └─────────────────────────────────────────────────────────┘

**1.4 Task States**
~~~~~~~~~~~~~~~~~~~

**RTOS Task State Machine:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │                    Task States                          │
   └─────────────────────────────────────────────────────────┘
   
              Task Created
                   │
                   │ _task_create()
                   ▼
            ┌──────────────┐
            │    READY     │◄───────────────────┐
            │              │                    │
            │ (Runnable,   │                    │
            │  waiting for │                    │ Event occurs
            │  CPU)        │                    │ (signal, msg)
            └───────┬──────┘                    │
                    │                           │
                    │ Scheduler picks           │
                    │ (highest priority)        │
                    ▼                           │
            ┌──────────────┐              ┌─────────────┐
            │   RUNNING    │              │   BLOCKED   │
            │              │              │             │
            │ (Executing   │─────────────►│ (Waiting    │
            │  on CPU)     │  Wait for    │  for event) │
            │              │  event       │             │
            └───────┬──────┘  (msg_recv,  └─────────────┘
                    │         sem_wait)
                    │ Preempted by
                    │ higher priority
                    │ task
                    ▼
            ┌──────────────┐
            │   SUSPENDED  │
            │              │
            │ (Suspended   │
            │  by _task_   │
            │  suspend())  │
            └──────────────┘

**State Transitions:**

.. code-block:: c

   // MQX Example
   
   // Create task → READY
   _task_id task_id = _task_create(0, SENSOR_TASK, 0);
   
   // READY → RUNNING (scheduler picks)
   // (automatic when task has highest priority)
   
   // RUNNING → BLOCKED (wait for event)
   _msgq_receive(queue_id, &msg, 0);  // Block until message
   
   // BLOCKED → READY (event occurs)
   _msgq_send(queue_id, msg);  // Sender posts message
   
   // RUNNING → READY (preempted)
   // (automatic when higher priority task becomes ready)
   
   // RUNNING → SUSPENDED (explicit suspend)
   _task_suspend(task_id);
   
   // SUSPENDED → READY (resume)
   _task_resume(task_id);

**1.5 Scheduling Algorithms**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Priority-Based Preemptive Scheduling (Most Common):**

.. code-block:: text

   Time ──────────────────────────────────────────────►
   
   Priority 1 (High):   ████░░░░░░░░████░░░░░░░░░░
   Task A (10 ms)           ^           ^
                            │           │
   Priority 2 (Med):    ░░██████░░░░░░░░░░██████░░░
   Task B (20 ms)         ^                 ^
   
   Priority 3 (Low):    ░░░░░░░░██████████████░░░░░
   Task C (50 ms)               ^
   
   Legend:
   ████ = Task running
   ░░░░ = Task not running (preempted or waiting)
   ^    = Task activation (timer, interrupt, event)
   
   Rules:
   1. Highest priority ready task runs
   2. Equal priority → FIFO (first come, first served)
   3. Preemption: High priority task immediately preempts low
   4. No time slicing (unless explicitly configured)

**Round-Robin (Time Slicing):**

.. code-block:: text

   Priority 2 (Equal priority tasks A, B, C):
   Time slice = 10 ms
   
   Time: 0    10   20   30   40   50   60   70
         │────│────│────│────│────│────│────│
   Task A: ████░░░░░░░░░░░░████░░░░░░░░░░░░
   Task B: ░░░░████░░░░░░░░░░░░████░░░░░░░░
   Task C: ░░░░░░░░████░░░░░░░░░░░░████░░░░
   
   Each task runs for time slice, then yields to next
   (Only for tasks at SAME priority level)

**Rate Monotonic Scheduling (RMS):**

.. code-block:: text

   Theory: Shorter period → Higher priority
   
   Task A: Period = 10 ms  →  Priority 1 (highest)
   Task B: Period = 20 ms  →  Priority 2
   Task C: Period = 50 ms  →  Priority 3 (lowest)
   
   Schedulability Test:
   U = Σ (C_i / T_i) ≤ n(2^(1/n) - 1)
   
   Where:
   C_i = Execution time of task i
   T_i = Period of task i
   n   = Number of tasks
   
   Example:
   Task A: C=2ms, T=10ms → U_A = 2/10 = 0.20
   Task B: C=3ms, T=20ms → U_B = 3/20 = 0.15
   Task C: C=5ms, T=50ms → U_C = 5/50 = 0.10
   Total U = 0.45
   
   Threshold: 3(2^(1/3) - 1) = 0.78
   0.45 ≤ 0.78 ✅ Schedulable!

**1.6 Context Switching**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is Context Switch:**

When CPU switches from Task A to Task B, it must:
1. Save Task A's context (registers, PC, SP)
2. Restore Task B's context
3. Jump to Task B's program counter

**Context (Saved State):**

.. code-block:: text

   Task Context (ARM Cortex-M4):
   ────────────────────────────
   • R0-R12     (13 general-purpose registers)
   • SP         (Stack pointer)
   • LR         (Link register)
   • PC         (Program counter)
   • PSR        (Program status register)
   • FPU regs   (S0-S31 if floating-point used)
   
   Total: 16-32 registers (64-128 bytes)

**Context Switch Time:**

.. code-block:: text

   Typical Timing (ARM Cortex-M4 @ 120 MHz):
   ─────────────────────────────────────────
   Hardware stacking (automatic):     500 ns
   Kernel save context:               1 µs
   Scheduler (select next task):      500 ns
   Kernel restore context:            1 µs
   Hardware unstacking:               500 ns
   ─────────────────────────────────────────
   Total context switch time:         3.5 µs
   
   Overhead at 1 kHz (1 ms period):
   3.5 µs / 1000 µs = 0.35%

**Context Switch Code (ARM Cortex-M):**

.. code-block:: c

   // Simplified context switch (ARM Cortex-M)
   // Called from PendSV interrupt handler
   
   void PendSV_Handler(void) {
       __asm volatile (
           // Save context of current task
           "mrs r0, psp                  \n"  // Get process stack pointer
           "stmdb r0!, {r4-r11}          \n"  // Save R4-R11 (R0-R3,R12,LR,PC,PSR auto-saved)
           "str r0, [%[current_sp]]      \n"  // Save SP to TCB
           
           // Load context of next task
           "ldr r0, [%[next_sp]]         \n"  // Load SP from next TCB
           "ldmia r0!, {r4-r11}          \n"  // Restore R4-R11
           "msr psp, r0                  \n"  // Set process stack pointer
           
           "bx lr                        \n"  // Return (auto-restores R0-R3,R12,LR,PC,PSR)
           :
           : [current_sp] "r" (&current_task->sp),
             [next_sp] "r" (&next_task->sp)
           : "r0", "memory"
       );
   }

═══════════════════════════════════════════════════════════════════════

🔧 **2. TASK MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**2.1 Task Creation**
~~~~~~~~~~~~~~~~~~~~~~

**Task Components:**

.. code-block:: text

   Task = Code + Stack + TCB (Task Control Block)
   
   ┌─────────────────────────────────────────┐
   │  Task Control Block (TCB)               │
   │  ┌───────────────────────────────────┐  │
   │  │ Task ID          : 0x1001         │  │
   │  │ Priority         : 5              │  │
   │  │ State            : READY          │  │
   │  │ Stack Pointer    : 0x20001000     │  │
   │  │ Stack Size       : 2048 bytes     │  │
   │  │ Entry Point      : task_function  │  │
   │  │ Creation Time    : 12345 ticks    │  │
   │  │ CPU Time Used    : 1234 ticks     │  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────┐
   │  Task Stack                             │
   │  ┌───────────────────────────────────┐  │
   │  │ High Address  ──► 0x20001800      │  │
   │  │                                   │  │
   │  │ ┌─────────────────────────────┐   │  │
   │  │ │  Local Variables            │   │  │
   │  │ ├─────────────────────────────┤   │  │
   │  │ │  Function Call Stack        │   │  │
   │  │ ├─────────────────────────────┤   │  │
   │  │ │  Saved Context (R0-R12, PC) │   │  │
   │  │ └─────────────────────────────┘   │  │
   │  │                                   │  │
   │  │ Low Address   ──► 0x20001000      │  │
   │  │                   (SP points here)│  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────┐
   │  Task Code (in Flash)                   │
   │  void task_function(uint32_t param) {   │
   │      while(1) {                         │
   │          // Task work                   │
   │      }                                  │
   │  }                                      │
   └─────────────────────────────────────────┘

**Task Creation Examples:**

**MQX (Your Primary RTOS):**

.. code-block:: c

   // MQX Task Template (in task list)
   const TASK_TEMPLATE_STRUCT MQX_template_list[] = {
       // Task Index, Entry Function, Stack Size, Priority, Name, Attributes
       {SENSOR_TASK,   sensor_task,   2000, 8, "sensor",   MQX_AUTO_START_TASK},
       {CONTROL_TASK,  control_task,  2000, 7, "control",  MQX_AUTO_START_TASK},
       {COMM_TASK,     comm_task,     3000, 6, "comm",     0},
       {0}  // Terminator
   };
   
   // Task function
   void sensor_task(uint32_t initial_data) {
       printf("Sensor task started\n");
       
       while(1) {
           // Read sensor
           uint16_t adc_value = read_adc();
           
           // Process data
           float temperature = convert_to_celsius(adc_value);
           
           // Send to control task
           send_message(CONTROL_TASK, temperature);
           
           // Wait 100 ms
           _time_delay(100);
       }
   }
   
   // Dynamic task creation
   void create_dynamic_task(void) {
       _task_id task_id = _task_create(0, COMM_TASK, 0);
       if (task_id == MQX_NULL_TASK_ID) {
           printf("ERROR: Task creation failed\n");
       } else {
           printf("Task created with ID: 0x%X\n", task_id);
       }
   }

**ThreadX:**

.. code-block:: c

   // ThreadX Task Creation
   
   TX_THREAD sensor_thread;
   UCHAR sensor_stack[2048];
   
   void tx_application_define(void *first_unused_memory) {
       UINT status;
       
       // Create sensor task
       status = tx_thread_create(
           &sensor_thread,              // Thread control block
           "Sensor Task",               // Name
           sensor_task_entry,           // Entry function
           0x1234,                      // Entry input (parameter)
           sensor_stack,                // Stack start
           2048,                        // Stack size
           5,                           // Priority (0=highest, 31=lowest)
           5,                           // Preemption threshold
           TX_NO_TIME_SLICE,            // No time slicing
           TX_AUTO_START                // Auto-start
       );
       
       if (status != TX_SUCCESS) {
           // Handle error
       }
   }
   
   void sensor_task_entry(ULONG thread_input) {
       printf("Sensor task started with param: 0x%lX\n", thread_input);
       
       while(1) {
           // Task work
           tx_thread_sleep(10);  // Sleep 10 ticks
       }
   }

**Integrity RTOS (Safety-Critical):**

.. code-block:: c

   // Integrity - Static configuration in .int file
   // (No dynamic task creation in safety-critical mode)
   
   // integrity_config.int
   AddressSpace SensorSpace {
       Language C
       Heap 64K
       
       Task SensorTask {
           StackSize 8K
           Priority 100
           StartIt true
       }
   }
   
   // C code
   void SensorTask(void) {
       // Integrity tasks don't take parameters
       // Use shared memory for communication
       
       while(1) {
           // Read sensor
           // Process data
           // Send via message
           
           Sleep(MilliSeconds(100));
       }
   }

**2.2 Priority Assignment**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Priority Levels:**

.. code-block:: text

   MQX:      1-255 (1=highest, 255=lowest, 0=invalid)
   ThreadX:  0-31  (0=highest, 31=lowest)
   Integrity: 1-255 (255=highest, 1=lowest) ⚠️  Reversed!
   FreeRTOS: 0-configMAX_PRIORITIES (higher number=higher priority)

**Priority Inversion Problem:**

.. code-block:: text

   Priority Inversion Scenario:
   ────────────────────────────
   
   Task A (Priority 1 - High):   Needs resource R
   Task B (Priority 2 - Medium): CPU-intensive
   Task C (Priority 3 - Low):    Holds resource R
   
   Timeline:
   
   t=0:  Task C (P3) locks resource R
   t=1:  Task A (P1) preempts C, tries to lock R → BLOCKED
   t=2:  Task B (P2) preempts C (C still holds R!)
   t=3-10: Task B runs (while A waits for C to release R)
   t=11: Task B completes
   t=12: Task C resumes, releases R
   t=13: Task A gets R and runs
   
   Problem: High-priority Task A waited for medium-priority Task B!
   (Effective priority inversion)

**Priority Inheritance Solution:**

.. code-block:: text

   With Priority Inheritance:
   ─────────────────────────
   
   t=0:  Task C (P3) locks resource R
   t=1:  Task A (P1) tries to lock R → Task C inherits P1
   t=2:  Task B (P2) tries to preempt, but C now has P1 → Cannot preempt
   t=3:  Task C (running at P1) releases R
   t=4:  Task C priority restored to P3
   t=5:  Task A gets R and runs
   
   Result: No inversion! Task B couldn't interfere.

**Priority Inheritance in MQX:**

.. code-block:: c

   // MQX Mutex with priority inheritance
   
   MUTEX_STRUCT resource_mutex;
   MUTEX_ATTR_STRUCT mutex_attr;
   
   // Initialize mutex
   _mutatr_init(&mutex_attr);
   _mutatr_set_wait_protocol(&mutex_attr, MUTEX_PRIO_INHERIT);  // Enable priority inheritance
   _mutex_init(&resource_mutex, &mutex_attr);
   
   // Task C (low priority)
   void task_c(uint32_t param) {
       _mutex_lock(&resource_mutex);
       // Critical section (now runs at inherited priority if task_a waits)
       process_resource();
       _mutex_unlock(&resource_mutex);
   }
   
   // Task A (high priority)
   void task_a(uint32_t param) {
       _mutex_lock(&resource_mutex);  // If C holds lock, C inherits A's priority
       // Critical section
       _mutex_unlock(&resource_mutex);
   }

**2.3 Task Communication Overhead**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Performance Comparison (ARM Cortex-M4 @ 120 MHz):**

.. code-block:: text

   ┌────────────────────────┬──────────────┬──────────────┐
   │  Mechanism             │  Latency     │  Use Case    │
   ├────────────────────────┼──────────────┼──────────────┤
   │  Shared Memory         │  <100 ns     │  Fastest     │
   │  (with mutex)          │              │              │
   │                        │              │              │
   │  Semaphore             │  2-5 µs      │  Sync only   │
   │                        │              │              │
   │  Message Queue         │  5-10 µs     │  Data + sync │
   │                        │              │              │
   │  Event Flags           │  1-3 µs      │  Multiple    │
   │                        │              │  events      │
   │                        │              │              │
   │  Mailbox               │  3-7 µs      │  Fixed-size  │
   │                        │              │  messages    │
   └────────────────────────┴──────────────┴──────────────┘

═══════════════════════════════════════════════════════════════════════

📬 **3. INTER-PROCESS COMMUNICATION (IPC)**
─────────────────────────────────────────────────────────────────────────

**3.1 Message Queues**
~~~~~~~~~~~~~~~~~~~~~~~

**MQX Message Queues (Most Common in Your Projects):**

.. code-block:: c

   // MQX Message Queue Example
   
   // Message structure (must start with MESSAGE_HEADER_STRUCT)
   typedef struct {
       MESSAGE_HEADER_STRUCT header;
       uint32_t sensor_id;
       float value;
       uint32_t timestamp;
   } SENSOR_MSG, *SENSOR_MSG_PTR;
   
   // Queue IDs
   #define SENSOR_QUEUE  1
   #define CONTROL_QUEUE 2
   
   // Sender task (sensor task)
   void sensor_task(uint32_t param) {
       _queue_id sensor_qid, control_qid;
       SENSOR_MSG_PTR msg_ptr;
       
       // Open message queues
       sensor_qid = _msgq_open(SENSOR_QUEUE, 0);
       control_qid = _msgq_open_system(CONTROL_QUEUE, 0, NULL, NULL);
       
       while(1) {
           // Allocate message
           msg_ptr = (SENSOR_MSG_PTR)_msg_alloc(sizeof(SENSOR_MSG));
           if (msg_ptr == NULL) {
               printf("ERROR: Message allocation failed\n");
               _time_delay(100);
               continue;
           }
           
           // Fill message
           msg_ptr->header.TARGET_QID = control_qid;
           msg_ptr->header.SIZE = sizeof(SENSOR_MSG);
           msg_ptr->sensor_id = 1;
           msg_ptr->value = read_temperature();
           msg_ptr->timestamp = _time_get_ticks();
           
           // Send message (non-blocking)
           if (!_msgq_send(msg_ptr)) {
               printf("ERROR: Message send failed\n");
               _msg_free(msg_ptr);
           }
           
           _time_delay(100);  // 100 ms sampling
       }
   }
   
   // Receiver task (control task)
   void control_task(uint32_t param) {
       _queue_id control_qid;
       SENSOR_MSG_PTR msg_ptr;
       
       // Open queue
       control_qid = _msgq_open(CONTROL_QUEUE, 0);
       
       while(1) {
           // Receive message (blocking, wait forever)
           msg_ptr = (SENSOR_MSG_PTR)_msgq_receive(control_qid, 0);
           
           if (msg_ptr == NULL) {
               printf("ERROR: Message receive failed\n");
               continue;
           }
           
           // Process message
           printf("Received: Sensor %u = %.2f°C at %u\n",
                  msg_ptr->sensor_id,
                  msg_ptr->value,
                  msg_ptr->timestamp);
           
           // Control logic
           if (msg_ptr->value > 80.0f) {
               activate_cooling();
           }
           
           // Free message
           _msg_free(msg_ptr);
       }
   }

**ThreadX Message Queues:**

.. code-block:: c

   // ThreadX Message Queue
   
   TX_QUEUE sensor_queue;
   ULONG sensor_queue_area[100];  // Storage for 100 messages (each 1 ULONG)
   
   // Create queue
   void tx_application_define(void *first_unused_memory) {
       tx_queue_create(
           &sensor_queue,          // Queue control block
           "Sensor Queue",         // Name
           TX_1_ULONG,             // Message size (1 ULONG = 4 bytes)
           sensor_queue_area,      // Queue start address
           sizeof(sensor_queue_area)  // Queue size in bytes
       );
   }
   
   // Send message
   void sender_task(ULONG param) {
       ULONG sensor_value;
       
       while(1) {
           sensor_value = read_sensor();
           
           // Send (block if queue full)
           tx_queue_send(&sensor_queue, &sensor_value, TX_WAIT_FOREVER);
           
           tx_thread_sleep(10);
       }
   }
   
   // Receive message
   void receiver_task(ULONG param) {
       ULONG received_value;
       UINT status;
       
       while(1) {
           // Receive (block if queue empty)
           status = tx_queue_receive(&sensor_queue, &received_value, TX_WAIT_FOREVER);
           
           if (status == TX_SUCCESS) {
               printf("Received: %lu\n", received_value);
           }
       }
   }

**3.2 Semaphores**
~~~~~~~~~~~~~~~~~~

**Binary Semaphore (Mutex Alternative):**

.. code-block:: c

   // MQX Lightweight Semaphore (binary)
   
   LWSEM_STRUCT resource_sem;
   
   // Initialize (value=1 for mutex-like behavior)
   _lwsem_create(&resource_sem, 1);
   
   // Task A
   void task_a(uint32_t param) {
       while(1) {
           // Wait (decrement, block if 0)
           _lwsem_wait(&resource_sem);
           
           // Critical section
           access_shared_resource();
           
           // Signal (increment)
           _lwsem_post(&resource_sem);
           
           _time_delay(50);
       }
   }

**Counting Semaphore (Resource Pool):**

.. code-block:: c

   // ThreadX Counting Semaphore
   
   TX_SEMAPHORE buffer_pool_sem;
   
   // Create semaphore (initial count = 10 buffers available)
   tx_semaphore_create(&buffer_pool_sem, "Buffer Pool", 10);
   
   // Allocate buffer
   void allocate_buffer(void) {
       // Wait for available buffer (decrement count)
       tx_semaphore_get(&buffer_pool_sem, TX_WAIT_FOREVER);
       
       // Allocate buffer
       buffer_t *buf = get_free_buffer();
       
       // Use buffer
       fill_buffer(buf);
   }
   
   // Free buffer
   void free_buffer(buffer_t *buf) {
       // Return buffer to pool
       release_buffer(buf);
       
       // Increment semaphore count
       tx_semaphore_put(&buffer_pool_sem);
   }

**3.3 Mutexes**
~~~~~~~~~~~~~~~

**MQX Mutex (Priority Inheritance):**

.. code-block:: c

   // MQX Mutex Example
   
   MUTEX_STRUCT spi_mutex;
   MUTEX_ATTR_STRUCT mutex_attr;
   
   // Initialize
   void init_mutex(void) {
       _mutatr_init(&mutex_attr);
       _mutatr_set_wait_protocol(&mutex_attr, MUTEX_PRIO_INHERIT);
       _mutatr_set_sched_protocol(&mutex_attr, MUTEX_PRIO_PROTECT);
       _mutex_init(&spi_mutex, &mutex_attr);
   }
   
   // Use mutex
   void access_spi_bus(uint8_t *data, uint16_t len) {
       // Lock mutex
       if (_mutex_lock(&spi_mutex) != MQX_OK) {
           printf("ERROR: Mutex lock failed\n");
           return;
       }
       
       // Critical section (exclusive SPI access)
       spi_transfer(data, len);
       
       // Unlock mutex
       _mutex_unlock(&spi_mutex);
   }

**Deadlock Example (and Prevention):**

.. code-block:: c

   // DEADLOCK SCENARIO (BAD CODE!)
   
   MUTEX_STRUCT mutex_a, mutex_b;
   
   // Task 1
   void task_1(uint32_t param) {
       _mutex_lock(&mutex_a);  // Lock A
       _time_delay(10);        // Simulate work
       _mutex_lock(&mutex_b);  // Lock B (DEADLOCK if task_2 holds B!)
       
       // Work
       
       _mutex_unlock(&mutex_b);
       _mutex_unlock(&mutex_a);
   }
   
   // Task 2
   void task_2(uint32_t param) {
       _mutex_lock(&mutex_b);  // Lock B
       _time_delay(10);        // Simulate work
       _mutex_lock(&mutex_a);  // Lock A (DEADLOCK if task_1 holds A!)
       
       // Work
       
       _mutex_unlock(&mutex_a);
       _mutex_unlock(&mutex_b);
   }
   
   // DEADLOCK PREVENTION: Always lock in same order
   
   // Task 1 (FIXED)
   void task_1_fixed(uint32_t param) {
       _mutex_lock(&mutex_a);  // Lock A first
       _mutex_lock(&mutex_b);  // Lock B second
       
       // Work
       
       _mutex_unlock(&mutex_b);  // Unlock in reverse order
       _mutex_unlock(&mutex_a);
   }
   
   // Task 2 (FIXED)
   void task_2_fixed(uint32_t param) {
       _mutex_lock(&mutex_a);  // Lock A first (same order as task_1)
       _mutex_lock(&mutex_b);  // Lock B second
       
       // Work
       
       _mutex_unlock(&mutex_b);
       _mutex_unlock(&mutex_a);
   }

**3.4 Event Flags**
~~~~~~~~~~~~~~~~~~~

**MQX Event Groups (Lightweight Events):**

.. code-block:: c

   // MQX Lightweight Event
   
   LWEVENT_STRUCT system_events;
   
   // Event bits
   #define EVENT_SENSOR_READY    (1 << 0)
   #define EVENT_DATA_PROCESSED  (1 << 1)
   #define EVENT_TRANSMIT_DONE   (1 << 2)
   #define EVENT_ERROR           (1 << 3)
   
   // Initialize
   _lwevent_create(&system_events, 0);  // All events cleared
   
   // Set event (signal)
   void sensor_isr(void) {
       _lwevent_set(&system_events, EVENT_SENSOR_READY);
   }
   
   // Wait for event
   void processing_task(uint32_t param) {
       while(1) {
           // Wait for sensor ready (block until event set)
           _lwevent_wait_for(&system_events, EVENT_SENSOR_READY, TRUE, NULL);
           
           // Process data
           process_sensor_data();
           
           // Signal completion
           _lwevent_set(&system_events, EVENT_DATA_PROCESSED);
       }
   }
   
   // Wait for multiple events (AND logic)
   void transmit_task(uint32_t param) {
       while(1) {
           // Wait for BOTH data processed AND transmit done
           _lwevent_wait_for(
               &system_events,
               EVENT_DATA_PROCESSED | EVENT_TRANSMIT_DONE,
               TRUE,   // Wait for ALL events (AND)
               NULL
           );
           
           // Transmit data
           transmit_to_network();
       }
   }
   
   // Wait for any event (OR logic)
   void monitor_task(uint32_t param) {
       while(1) {
           // Wait for ANY event
           _lwevent_wait_for(
               &system_events,
               EVENT_SENSOR_READY | EVENT_DATA_PROCESSED | EVENT_ERROR,
               FALSE,  // Wait for ANY event (OR)
               NULL
           );
           
           // Check which event occurred
           uint32_t events = _lwevent_get_signalled();
           
           if (events & EVENT_ERROR) {
               handle_error();
           }
       }
   }

═══════════════════════════════════════════════════════════════════════

🚀 **4. MQX RTOS - DEEP DIVE**
─────────────────────────────────────────────────────────────────────────

**Your Primary RTOS (Kinetis K50, Industrial Gateways, Motor Control)**

**4.1 MQX Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~

**MQX Components:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │  MQX RTOS Architecture                                  │
   └─────────────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────────────┐
   │  Application Tasks                                      │
   │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐              │
   │  │Task 1│  │Task 2│  │Task 3│  │Task N│              │
   │  └──────┘  └──────┘  └──────┘  └──────┘              │
   └──────────────────────┬──────────────────────────────────┘
                          │ MQX API
   ┌──────────────────────▼──────────────────────────────────┐
   │  MQX Kernel Services                                    │
   │  ┌─────────────────────────────────────────────────┐   │
   │  │ Core (PSP - Platform Support Package)          │   │
   │  │  • Scheduler                                    │   │
   │  │  • Task management                              │   │
   │  │  • Interrupt handling                           │   │
   │  │  • Context switching                            │   │
   │  └─────────────────────────────────────────────────┘   │
   │  ┌─────────────────────────────────────────────────┐   │
   │  │ IPC Components                                  │   │
   │  │  • Message queues  • Semaphores                 │   │
   │  │  • Mutexes         • Events                     │   │
   │  │  • Partitions      • Logs                       │   │
   │  └─────────────────────────────────────────────────┘   │
   │  ┌─────────────────────────────────────────────────┐   │
   │  │ Memory Management                               │   │
   │  │  • System memory   • Partition pools            │   │
   │  │  • Message pools   • Light memory               │   │
   │  └─────────────────────────────────────────────────┘   │
   │  ┌─────────────────────────────────────────────────┐   │
   │  │ Time Services                                   │   │
   │  │  • Time delay      • Watchdogs                  │   │
   │  │  • Timers          • Tick timer                 │   │
   │  └─────────────────────────────────────────────────┘   │
   └──────────────────────┬──────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────┐
   │  BSP (Board Support Package)                            │
   │  • Clock configuration  • Pin muxing                    │
   │  • Peripheral init      • Low-level drivers             │
   └──────────────────────┬──────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────┐
   │  Hardware (Kinetis K50/K60)                             │
   │  • ARM Cortex-M4 @ 100-120 MHz                          │
   │  • 128-512 KB Flash, 16-128 KB RAM                      │
   │  • FPU, MPU, DSP extensions                             │
   └─────────────────────────────────────────────────────────┘

**MQX Directory Structure:**

.. code-block:: text

   mqx/
   ├── mqx/                    # MQX kernel source
   │   ├── source/
   │   │   ├── kernel/         # Core kernel (scheduler, tasks)
   │   │   ├── message/        # Message queues
   │   │   ├── sem/            # Semaphores
   │   │   ├── mutex/          # Mutexes
   │   │   ├── event/          # Events
   │   │   ├── mem/            # Memory management
   │   │   ├── timer/          # Timers
   │   │   └── log/            # Kernel logging
   │   └── build/              # Pre-built libraries
   ├── mqx_stdlib/             # Standard library (printf, etc.)
   ├── psp/                    # Platform Support Package
   │   └── cortex_m/
   │       ├── core/           # ARM Cortex-M core code
   │       │   ├── M4/         # Cortex-M4 specific
   │       │   └── M0/         # Cortex-M0 specific
   │       └── compiler/       # IAR, Keil, GCC support
   ├── bsp/                    # Board Support Packages
   │   ├── twrk60n512/         # Tower K60
   │   ├── twrk50/             # Tower K50
   │   └── custom_board/       # Your custom board
   └── lib/                    # MQX libraries
       ├── twrk60n512.iar/     # Pre-compiled for IAR
       └── twrk60n512.gcc/     # Pre-compiled for GCC

**4.2 MQX Initialization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**MQX Startup Sequence:**

.. code-block:: c

   // main.c - Typical MQX startup
   
   #include <mqx.h>
   #include <bsp.h>
   
   // Task template list (defines all tasks)
   const TASK_TEMPLATE_STRUCT MQX_template_list[] = {
       // Task Index, Function, Stack, Priority, Name, Attributes, Creation Param, Time Slice
       {MAIN_TASK,    main_task,    2000, 8, "main",    MQX_AUTO_START_TASK, 0, 0},
       {SENSOR_TASK,  sensor_task,  1500, 9, "sensor",  MQX_AUTO_START_TASK, 0, 0},
       {CONTROL_TASK, control_task, 2000, 7, "control", 0, 0, 0},
       {COMM_TASK,    comm_task,    2500, 6, "comm",    0, 0, 0},
       {0}  // Terminator
   };
   
   // Application entry point
   void main_task(uint32_t initial_data) {
       _task_id task_id;
       
       printf("\n\n*** MQX Application Started ***\n");
       printf("Processor: %s\n", _PSP_CPU_NAME);
       printf("Frequency: %d MHz\n", _BSP_CPU_MHZ);
       printf("MQX Version: %s\n", _mqx_version);
       
       // Create message queues
       init_message_queues();
       
       // Create additional tasks (not auto-started)
       task_id = _task_create(0, CONTROL_TASK, 0);
       if (task_id == MQX_NULL_TASK_ID) {
           printf("ERROR: Failed to create control task\n");
           _task_block();
       }
       
       task_id = _task_create(0, COMM_TASK, 0);
       if (task_id == MQX_NULL_TASK_ID) {
           printf("ERROR: Failed to create comm task\n");
           _task_block();
       }
       
       // Main task work
       while(1) {
           printf("Heartbeat: %d ticks\n", _time_get_ticks());
           _time_delay(1000);  // 1 second
       }
   }

**BSP Configuration (bsp_config.h):**

.. code-block:: c

   // bsp_config.h - Board Support Package configuration
   
   #ifndef __bsp_config_h__
   #define __bsp_config_h__
   
   // Clock configuration
   #define BSP_SYSTEM_CLOCK               120000000UL  // 120 MHz
   #define BSP_BUS_CLOCK                  60000000UL   // 60 MHz
   #define BSP_CORE_CLOCK                 120000000UL  // 120 MHz
   
   // MQX tick timer (1 ms tick)
   #define BSP_ALARM_FREQUENCY            1000         // 1 kHz (1 ms tick)
   #define BSP_ALARM_RESOLUTION           1            // 1 ms
   
   // Default interrupt priority
   #define BSP_DEFAULT_MQX_HARDWARE_INTERRUPT_LEVEL_MAX  (1)
   
   // Memory configuration
   #define BSP_DEFAULT_START_OF_KERNEL_MEMORY  ((void *)__KERNEL_DATA_START)
   #define BSP_DEFAULT_END_OF_KERNEL_MEMORY    ((void *)__KERNEL_DATA_END)
   
   // Serial console
   #define BSP_DEFAULT_IO_CHANNEL          "ttya:"     // UART0
   #define BSP_DEFAULT_IO_CHANNEL_DEFINED
   
   #endif

**4.3 MQX Memory Management**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Memory Pools:**

.. code-block:: text

   MQX Memory Types:
   ─────────────────
   
   1. System Memory (_mem_alloc, _mem_free)
      • General-purpose heap allocation
      • Dynamic allocation (like malloc)
      • Fragmentation possible
   
   2. Partition Pools (_partition_create)
      • Fixed-size blocks
      • No fragmentation
      • Fast allocation/deallocation
      • Ideal for buffers, messages
   
   3. Light Memory (_mem_alloc_from, _mem_free_from)
      • Custom memory pools
      • Application-managed
   
   4. Message Pools (_msgpool_create)
      • Specialized for message queues
      • Pre-allocated message buffers

**System Memory Example:**

.. code-block:: c

   // System memory allocation (heap)
   
   void system_memory_example(void) {
       uint8_t *buffer;
       
       // Allocate 1024 bytes
       buffer = (uint8_t *)_mem_alloc(1024);
       if (buffer == NULL) {
           printf("ERROR: Memory allocation failed\n");
           return;
       }
       
       // Use buffer
       memset(buffer, 0, 1024);
       
       // Free memory
       _mem_free(buffer);
   }
   
   // Check memory statistics
   void check_memory_usage(void) {
       _mem_size used, free_mem;
       
       _mem_get_free(&free_mem);
       printf("Free memory: %u bytes\n", free_mem);
       
       // MQX 4.x and later
       KERNEL_DATA_STRUCT_PTR kernel_data = _mqx_get_kernel_data();
       MEM_POOL_STRUCT_PTR mem_pool = kernel_data->KER_POOL_PTR;
       
       printf("Total blocks: %u\n", mem_pool->POOL_BLOCK_COUNT);
       printf("Free blocks: %u\n", mem_pool->POOL_FREE_LIST.SIZE);
   }

**Partition Pools (Recommended for Real-Time):**

.. code-block:: c

   // Partition pool example (fixed-size blocks)
   
   _partition_id buffer_pool_id;
   
   #define BUFFER_SIZE     256
   #define NUM_BUFFERS     10
   
   // Create partition pool
   void create_buffer_pool(void) {
       // Allocate memory for pool (10 buffers × 256 bytes)
       void *pool_memory = _mem_alloc(NUM_BUFFERS * BUFFER_SIZE);
       if (pool_memory == NULL) {
           printf("ERROR: Pool allocation failed\n");
           return;
       }
       
       // Create partition pool
       buffer_pool_id = _partition_create(
           pool_memory,      // Pool start address
           NUM_BUFFERS,      // Number of blocks
           BUFFER_SIZE,      // Block size
           0                 // Flags (0=default)
       );
       
       if (buffer_pool_id == 0) {
           printf("ERROR: Partition pool creation failed\n");
           _mem_free(pool_memory);
       }
   }
   
   // Allocate from partition pool (FAST, deterministic)
   void use_buffer_pool(void) {
       uint8_t *buffer;
       
       // Allocate block (O(1) time, no search)
       buffer = (uint8_t *)_partition_alloc(buffer_pool_id);
       if (buffer == NULL) {
           printf("ERROR: All buffers in use\n");
           return;
       }
       
       // Use buffer
       fill_buffer_with_sensor_data(buffer);
       
       // Free block (O(1) time)
       _partition_free(buffer);
   }

**Message Pools:**

.. code-block:: c

   // Message pool for efficient IPC
   
   _pool_id message_pool_id;
   
   typedef struct {
       MESSAGE_HEADER_STRUCT header;
       uint32_t sensor_id;
       float value;
       uint32_t timestamp;
   } SENSOR_MSG, *SENSOR_MSG_PTR;
   
   // Create message pool
   void create_message_pool(void) {
       message_pool_id = _msgpool_create(
           sizeof(SENSOR_MSG),  // Message size
           20,                  // Initial messages
           10,                  // Grow by (if pool exhausted)
           100                  // Maximum messages
       );
       
       if (message_pool_id == MSGPOOL_NULL_POOL_ID) {
           printf("ERROR: Message pool creation failed\n");
       }
   }
   
   // Allocate message from pool
   void send_sensor_message(float temperature) {
       SENSOR_MSG_PTR msg;
       
       // Allocate from pool (faster than _msg_alloc)
       msg = (SENSOR_MSG_PTR)_msg_alloc(message_pool_id);
       if (msg == NULL) {
           printf("ERROR: Message allocation failed\n");
           return;
       }
       
       // Fill message
       msg->header.TARGET_QID = _msgq_get_id(0, CONTROL_QUEUE);
       msg->header.SIZE = sizeof(SENSOR_MSG);
       msg->sensor_id = 1;
       msg->value = temperature;
       msg->timestamp = _time_get_ticks();
       
       // Send
       _msgq_send(msg);
   }

**4.4 MQX Interrupt Handling**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Interrupt Service Routine (ISR) Structure:**

.. code-block:: text

   MQX Interrupt Handling:
   ───────────────────────
   
   Hardware Interrupt
         │
         ▼
   ┌──────────────────────────────────────┐
   │  MQX Kernel ISR Wrapper              │
   │  • Save context                      │
   │  • Increment ISR nesting counter     │
   │  • Call user ISR                     │
   └──────────────┬───────────────────────┘
                  │
                  ▼
   ┌──────────────────────────────────────┐
   │  User ISR (_int_install_isr)         │
   │  • Minimal processing                │
   │  • Read hardware register            │
   │  • Set flag / post semaphore         │
   │  • Defer work to task                │
   └──────────────┬───────────────────────┘
                  │
                  ▼
   ┌──────────────────────────────────────┐
   │  MQX Kernel ISR Wrapper (return)     │
   │  • Decrement ISR nesting counter     │
   │  • Check if reschedule needed        │
   │  • Restore context                   │
   │  • Return from interrupt             │
   └──────────────────────────────────────┘

**Installing ISR:**

.. code-block:: c

   // MQX ISR installation example
   
   #include <mqx.h>
   #include <bsp.h>
   
   // Global semaphore for ISR-to-task communication
   LWSEM_STRUCT adc_semaphore;
   
   // ADC interrupt service routine
   void adc_isr(void *param) {
       // Read ADC status (clear interrupt flag)
       uint32_t status = ADC0_SC1A;
       
       // Read ADC result
       volatile uint16_t adc_result = ADC0_RA;
       
       // Store result (shared memory - use mutex if accessed by multiple tasks)
       extern uint16_t g_adc_value;
       g_adc_value = adc_result;
       
       // Signal task (post semaphore)
       _lwsem_post(&adc_semaphore);
       
       // Note: Keep ISR short! No printf, no delays, no heavy processing
   }
   
   // Initialize ADC and install ISR
   void init_adc_interrupt(void) {
       // Create semaphore
       _lwsem_create(&adc_semaphore, 0);  // Initial value = 0
       
       // Install ISR
       _int_install_isr(
           INT_ADC0,           // Interrupt vector number (from BSP)
           adc_isr,            // ISR function
           NULL                // Parameter (passed to ISR)
       );
       
       // Set interrupt priority (lower number = higher priority in MQX)
       // Priorities 1-7: Kernel cannot be preempted
       // Priorities 8-15: Kernel can be preempted (recommended for most ISRs)
       _bsp_int_init(INT_ADC0, 10, 0, TRUE);  // Priority 10, subpriority 0, enable
       
       // Configure ADC hardware
       // Enable ADC conversion complete interrupt
       ADC0_SC1A = ADC_SC1_AIEN_MASK | 0;  // Enable interrupt, channel 0
   }
   
   // Task that processes ADC data
   void adc_task(uint32_t param) {
       extern uint16_t g_adc_value;
       
       while(1) {
           // Wait for ISR to post semaphore (blocking)
           _lwsem_wait(&adc_semaphore);
           
           // Process ADC value
           float voltage = (g_adc_value * 3.3f) / 4096.0f;
           printf("ADC: %u (%.3f V)\n", g_adc_value, voltage);
           
           // Trigger next conversion
           ADC0_SC1A = ADC_SC1_AIEN_MASK | 0;
       }
   }

**Interrupt Priorities (ARM Cortex-M):**

.. code-block:: text

   MQX Interrupt Priority Levels (ARM Cortex-M):
   ──────────────────────────────────────────────
   
   Priority 0-7:   KERNEL CANNOT BE PREEMPTED
                   • Use for critical, time-sensitive interrupts
                   • Cannot call most MQX functions (except _int_* APIs)
                   • Example: Motor control PWM, encoder capture
   
   Priority 8-15:  KERNEL CAN BE PREEMPTED (default)
                   • Safe to call MQX APIs (_lwsem_post, _lwevent_set, etc.)
                   • Recommended for most interrupts
                   • Example: UART, I2C, SPI, ADC, timers
   
   Configuration:
   #define BSP_DEFAULT_MQX_HARDWARE_INTERRUPT_LEVEL_MAX  (1)
   
   Interrupts at priority ≤ 1 cannot preempt kernel
   Interrupts at priority > 1 can preempt kernel

**DMA with MQX:**

.. code-block:: c

   // DMA transfer with interrupt
   
   LWSEM_STRUCT dma_complete_sem;
   uint8_t dma_buffer[1024];
   
   // DMA interrupt handler
   void dma_isr(void *param) {
       // Clear DMA interrupt flag
       DMA_INT |= DMA_INT_INT0_MASK;
       
       // Signal completion
       _lwsem_post(&dma_complete_sem);
   }
   
   // Setup DMA transfer
   void setup_dma_transfer(void) {
       // Create semaphore
       _lwsem_create(&dma_complete_sem, 0);
       
       // Install DMA ISR
       _int_install_isr(INT_DMA0, dma_isr, NULL);
       _bsp_int_init(INT_DMA0, 10, 0, TRUE);
       
       // Configure DMA channel 0
       DMA_SAR0 = (uint32_t)&UART0_D;           // Source: UART data register
       DMA_DAR0 = (uint32_t)dma_buffer;         // Destination: Buffer
       DMA_DSR_BCR0 = DMA_DSR_BCR_BCR(1024);    // Byte count: 1024
       
       // Enable DMA completion interrupt
       DMA_DCR0 = DMA_DCR_EINT_MASK |           // Enable interrupt on completion
                  DMA_DCR_DINC_MASK |           // Increment destination
                  DMA_DCR_SSIZE(0) |            // Source size: 8-bit
                  DMA_DCR_DSIZE(0);             // Dest size: 8-bit
       
       // Start DMA
       DMA_DCR0 |= DMA_DCR_START_MASK;
   }
   
   // Wait for DMA completion
   void wait_dma_complete(void) {
       // Block until DMA ISR posts semaphore
       _lwsem_wait(&dma_complete_sem);
       
       printf("DMA transfer complete: %u bytes\n", 1024);
       
       // Process received data
       process_uart_data(dma_buffer, 1024);
   }

**4.5 MQX Timers**
~~~~~~~~~~~~~~~~~~

**Software Timers:**

.. code-block:: c

   // MQX Timer example
   
   #include <timer.h>
   
   TIMER_STRUCT periodic_timer;
   
   // Timer callback (runs in timer ISR context!)
   void timer_callback(_timer_id timer_id, void *data_ptr, uint32_t seconds, uint32_t milliseconds) {
       // Keep this SHORT and FAST!
       // Do NOT call blocking MQX functions
       
       // Example: Toggle LED
       GPIO_TOGGLE_PIN(LED_PIN);
       
       // Or post event
       LWEVENT_STRUCT *event = (LWEVENT_STRUCT *)data_ptr;
       _lwevent_set(event, EVENT_TIMER_EXPIRED);
   }
   
   // Create periodic timer (100 ms period)
   void create_periodic_timer(LWEVENT_STRUCT *event) {
       _timer_id timer_id;
       TIME_STRUCT time;
       
       // Set period: 100 ms
       time.SECONDS = 0;
       time.MILLISECONDS = 100;
       
       // Create timer
       timer_id = _timer_start_periodic_every(
           timer_callback,     // Callback function
           event,              // User data (passed to callback)
           TIMER_ELAPSED_TIME_MODE,
           &time               // Period
       );
       
       if (timer_id == TIMER_NULL_ID) {
           printf("ERROR: Timer creation failed\n");
       }
   }
   
   // One-shot timer
   void create_oneshot_timer(void) {
       _timer_id timer_id;
       TIME_STRUCT time;
       
       // Delay: 5 seconds
       time.SECONDS = 5;
       time.MILLISECONDS = 0;
       
       // Create one-shot timer
       timer_id = _timer_start_oneshot_after(
           timer_callback,
           NULL,               // No user data
           TIMER_ELAPSED_TIME_MODE,
           &time
       );
   }

**Watchdog Timer:**

.. code-block:: c

   // MQX Watchdog example
   
   #include <watchdog.h>
   
   void init_watchdog(void) {
       _watchdog_id watchdog_id;
       
       // Create watchdog (2 second timeout)
       watchdog_id = _watchdog_create_component(
           BSP_TIMER_INTERRUPT_VECTOR,  // Timer vector
           watchdog_expiry_handler      // Expiry handler (or NULL for reset)
       );
       
       if (watchdog_id == 0) {
           printf("ERROR: Watchdog creation failed\n");
           return;
       }
       
       // Start watchdog for main task (2000 ms timeout)
       _watchdog_start_ticks(2000);
   }
   
   // Main task with watchdog
   void main_task_with_watchdog(uint32_t param) {
       init_watchdog();
       
       while(1) {
           // Do work
           process_data();
           
           // Pet the watchdog (reset timer)
           _watchdog_stop();
           _watchdog_start_ticks(2000);
           
           _time_delay(500);  // Sleep 500 ms
       }
   }
   
   // Watchdog expiry handler (called if task doesn't pet watchdog)
   void watchdog_expiry_handler(void) {
       printf("WATCHDOG EXPIRED! System hung?\n");
       
       // Log error
       log_error("Watchdog timeout");
       
       // Reset system
       _mqx_exit(0);
   }

**4.6 MQX Task Synchronization Patterns**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Producer-Consumer Pattern:**

.. code-block:: c

   // Producer-Consumer using message queue
   
   #define PRODUCER_QUEUE  10
   #define CONSUMER_QUEUE  11
   
   _queue_id producer_qid, consumer_qid;
   
   // Message structure
   typedef struct {
       MESSAGE_HEADER_STRUCT header;
       uint32_t data[64];  // 256 bytes of data
   } DATA_MSG, *DATA_MSG_PTR;
   
   // Producer task
   void producer_task(uint32_t param) {
       DATA_MSG_PTR msg;
       uint32_t count = 0;
       
       // Open queues
       producer_qid = _msgq_open(PRODUCER_QUEUE, 0);
       consumer_qid = _msgq_open_system(CONSUMER_QUEUE, 0, NULL, NULL);
       
       while(1) {
           // Allocate message
           msg = (DATA_MSG_PTR)_msg_alloc(sizeof(DATA_MSG));
           if (msg) {
               // Fill data
               for (int i = 0; i < 64; i++) {
                   msg->data[i] = count++;
               }
               
               msg->header.TARGET_QID = consumer_qid;
               msg->header.SIZE = sizeof(DATA_MSG);
               
               // Send to consumer
               _msgq_send(msg);
               
               printf("Produced: %u items\n", count);
           }
           
           _time_delay(100);  // Produce every 100 ms
       }
   }
   
   // Consumer task
   void consumer_task(uint32_t param) {
       DATA_MSG_PTR msg;
       
       // Open queue
       consumer_qid = _msgq_open(CONSUMER_QUEUE, 0);
       
       while(1) {
           // Receive message (blocking)
           msg = (DATA_MSG_PTR)_msgq_receive(consumer_qid, 0);
           
           if (msg) {
               // Process data
               process_received_data(msg->data, 64);
               
               // Free message
               _msg_free(msg);
               
               printf("Consumed message\n");
           }
       }
   }

**Rendezvous Pattern (Barrier):**

.. code-block:: c

   // Barrier synchronization (N tasks meet at sync point)
   
   #define NUM_WORKERS  4
   
   LWSEM_STRUCT barrier_sem;
   volatile uint32_t barrier_count = 0;
   MUTEX_STRUCT barrier_mutex;
   
   void init_barrier(void) {
       _lwsem_create(&barrier_sem, 0);  // Initially blocked
       _mutex_init(&barrier_mutex, NULL);
   }
   
   void barrier_wait(void) {
       // Atomically increment counter
       _mutex_lock(&barrier_mutex);
       barrier_count++;
       
       if (barrier_count == NUM_WORKERS) {
           // Last task to arrive - release all
           barrier_count = 0;  // Reset for next round
           _mutex_unlock(&barrier_mutex);
           
           // Post semaphore N-1 times (for other tasks)
           for (int i = 0; i < NUM_WORKERS - 1; i++) {
               _lwsem_post(&barrier_sem);
           }
           
           // This task continues immediately
       } else {
           _mutex_unlock(&barrier_mutex);
           
           // Wait for last task
           _lwsem_wait(&barrier_sem);
       }
   }
   
   // Worker tasks
   void worker_task(uint32_t worker_id) {
       while(1) {
           // Phase 1: Independent work
           printf("Worker %u: Phase 1\n", worker_id);
           do_phase1_work();
           
           // Synchronization point
           barrier_wait();
           
           // Phase 2: All workers proceed together
           printf("Worker %u: Phase 2\n", worker_id);
           do_phase2_work();
           
           // Repeat
       }
   }

**Reader-Writer Lock (Many readers, one writer):**

.. code-block:: c

   // Reader-writer lock using MQX semaphores
   
   typedef struct {
       LWSEM_STRUCT resource_sem;      // Protects resource
       LWSEM_STRUCT reader_count_sem;  // Protects reader_count
       uint32_t reader_count;
   } RW_LOCK, *RW_LOCK_PTR;
   
   void rwlock_init(RW_LOCK_PTR lock) {
       _lwsem_create(&lock->resource_sem, 1);       // Initially available
       _lwsem_create(&lock->reader_count_sem, 1);   // Initially available
       lock->reader_count = 0;
   }
   
   void rwlock_read_lock(RW_LOCK_PTR lock) {
       // Increment reader count
       _lwsem_wait(&lock->reader_count_sem);
       lock->reader_count++;
       
       if (lock->reader_count == 1) {
           // First reader locks resource (blocks writers)
           _lwsem_wait(&lock->resource_sem);
       }
       
       _lwsem_post(&lock->reader_count_sem);
   }
   
   void rwlock_read_unlock(RW_LOCK_PTR lock) {
       // Decrement reader count
       _lwsem_wait(&lock->reader_count_sem);
       lock->reader_count--;
       
       if (lock->reader_count == 0) {
           // Last reader unlocks resource (allows writers)
           _lwsem_post(&lock->resource_sem);
       }
       
       _lwsem_post(&lock->reader_count_sem);
   }
   
   void rwlock_write_lock(RW_LOCK_PTR lock) {
       // Writer gets exclusive access
       _lwsem_wait(&lock->resource_sem);
   }
   
   void rwlock_write_unlock(RW_LOCK_PTR lock) {
       _lwsem_post(&lock->resource_sem);
   }
   
   // Usage example
   RW_LOCK shared_data_lock;
   uint32_t shared_data[1000];
   
   void reader_task(uint32_t param) {
       while(1) {
           rwlock_read_lock(&shared_data_lock);
           
           // Multiple readers can read simultaneously
           uint32_t value = shared_data[42];
           printf("Read: %u\n", value);
           
           rwlock_read_unlock(&shared_data_lock);
           
           _time_delay(100);
       }
   }
   
   void writer_task(uint32_t param) {
       while(1) {
           rwlock_write_lock(&shared_data_lock);
           
           // Exclusive access (no readers or other writers)
           for (int i = 0; i < 1000; i++) {
               shared_data[i]++;
           }
           printf("Updated shared data\n");
           
           rwlock_write_unlock(&shared_data_lock);
           
           _time_delay(500);
       }
   }

**4.7 MQX Logging and Debugging**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Kernel Log:**

.. code-block:: c

   // MQX Kernel Logging
   
   #include <log.h>
   
   _mqx_uint log_number;
   
   void init_logging(void) {
       // Create log (1024 entries)
       log_number = _log_create_component();
       
       // Create log (custom size)
       log_number = _klog_create(1024, 0);
       
       if (log_number == 0) {
           printf("ERROR: Log creation failed\n");
       }
       
       // Enable logging
       _klog_control(KLOG_ENABLED | KLOG_CONTEXT_ENABLED | KLOG_FUNCTIONS_ENABLED, TRUE);
       
       // Log function entry/exit
       _klog_control(KLOG_TASK_FUNCTIONS, TRUE);
       _klog_control(KLOG_INTERRUPT_FUNCTIONS, TRUE);
   }
   
   // Write to log
   void log_event(const char *message) {
       _klog_log(KLOG_TASK_FUNCTIONS, _task_get_id(), (uint32_t)message, 0, 0);
   }
   
   // Read log
   void print_log(void) {
       KLOG_ENTRY_STRUCT entry;
       
       while (_klog_get_next_entry(&entry)) {
           printf("Task: 0x%X, Function: %u, Data: 0x%X\n",
                  entry.TASK_ID,
                  entry.FUNCTION,
                  entry.DATA[0]);
       }
   }

**Task Stack Usage:**

.. code-block:: c

   // Check task stack usage
   
   void check_stack_usage(void) {
       _task_id task_id = _task_get_id();
       TD_STRUCT_PTR td_ptr = _task_get_td(task_id);
       
       void *stack_base = td_ptr->STACK_BASE;
       void *stack_ptr = td_ptr->STACK_PTR;
       uint32_t stack_size = (uint32_t)stack_base - (uint32_t)td_ptr->STACK_LIMIT;
       uint32_t stack_used = (uint32_t)stack_base - (uint32_t)stack_ptr;
       
       printf("Task 0x%X Stack:\n", task_id);
       printf("  Size: %u bytes\n", stack_size);
       printf("  Used: %u bytes (%.1f%%)\n", 
              stack_used, 
              (float)stack_used / stack_size * 100.0f);
       
       // Check for stack overflow
       if (stack_used > stack_size * 0.9f) {
           printf("  ⚠️  WARNING: Stack usage >90%%!\n");
       }
   }

**Performance Profiling:**

.. code-block:: c

   // Measure task execution time
   
   void profile_task_performance(void) {
       TIME_STRUCT start_time, end_time;
       uint32_t overflow;
       
       // Get start time
       _time_get_elapsed(&start_time);
       
       // Execute task work
       process_sensor_data();
       
       // Get end time
       _time_get_elapsed(&end_time);
       
       // Calculate elapsed time
       TIME_STRUCT elapsed;
       _time_diff(&start_time, &end_time, &elapsed, &overflow);
       
       printf("Task execution time: %u.%03u sec\n",
              elapsed.SECONDS,
              elapsed.MILLISECONDS);
   }

═══════════════════════════════════════════════════════════════════════

🎯 **5. THREADX RTOS**
─────────────────────────────────────────────────────────────────────────

**Microsoft ThreadX (formerly Express Logic ThreadX)**

**5.1 ThreadX Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~

**ThreadX Characteristics:**

.. code-block:: text

   ThreadX Features:
   ─────────────────
   • Preemptive priority-based scheduling
   • 32 priority levels (0=highest, 31=lowest)
   • Preemption-threshold scheduling (unique feature)
   • Time-slicing (optional, per priority level)
   • Fast context switch: ~1-3 µs
   • Small footprint: 2-5 KB code, 1-2 KB RAM
   • Picokernel architecture
   • Safety certifications: DO-178B/C, IEC 61508, IEC 62304
   • Now open-source (Microsoft Azure RTOS, MIT license)

**ThreadX Architecture:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │  Application Threads                                    │
   │  ┌────────┐  ┌────────┐  ┌────────┐                   │
   │  │Thread 1│  │Thread 2│  │Thread 3│                   │
   │  └────────┘  └────────┘  └────────┘                   │
   └──────────────────────┬──────────────────────────────────┘
                          │ ThreadX API (tx_*.c)
   ┌──────────────────────▼──────────────────────────────────┐
   │  ThreadX Services                                       │
   │  ┌──────────────────────────────────────────────────┐  │
   │  │ Core Services                                    │  │
   │  │  • Thread management  • Scheduler                │  │
   │  │  • Time management    • Interrupts               │  │
   │  └──────────────────────────────────────────────────┘  │
   │  ┌──────────────────────────────────────────────────┐  │
   │  │ Synchronization                                  │  │
   │  │  • Semaphores  • Mutexes  • Event flags          │  │
   │  │  • Queues      • Block pools                     │  │
   │  └──────────────────────────────────────────────────┘  │
   └──────────────────────┬──────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────┐
   │  ThreadX Port (tx_port.c, tx_port.s)                    │
   │  • ARM Cortex-M/A/R  • x86  • RISC-V                    │
   └─────────────────────────────────────────────────────────┘

**5.2 ThreadX Thread Management**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Thread Creation:**

.. code-block:: c

   // ThreadX Thread Example
   
   #include "tx_api.h"
   
   // Thread control blocks
   TX_THREAD sensor_thread;
   TX_THREAD control_thread;
   
   // Thread stacks
   UCHAR sensor_stack[1024];
   UCHAR control_stack[2048];
   
   // Application entry point
   void tx_application_define(void *first_unused_memory) {
       UINT status;
       
       // Create sensor thread
       status = tx_thread_create(
           &sensor_thread,              // Thread control block
           "Sensor Thread",             // Thread name
           sensor_thread_entry,         // Entry function
           0x1234,                      // Entry input (uint32_t param)
           sensor_stack,                // Stack pointer
           1024,                        // Stack size
           5,                           // Priority (0-31, 0=highest)
           5,                           // Preemption threshold
           TX_NO_TIME_SLICE,            // Time slice (0=disabled)
           TX_AUTO_START                // Auto-start flag
       );
       
       if (status != TX_SUCCESS) {
           // Handle error
       }
       
       // Create control thread
       status = tx_thread_create(
           &control_thread,
           "Control Thread",
           control_thread_entry,
           0,
           control_stack,
           2048,
           10,                          // Lower priority
           10,
           20,                          // Time slice = 20 ticks (if equal priority)
           TX_AUTO_START
       );
   }
   
   // Sensor thread entry point
   void sensor_thread_entry(ULONG thread_input) {
       printf("Sensor thread started (param: 0x%lX)\n", thread_input);
       
       while(1) {
           // Read sensor
           uint16_t adc_value = read_adc();
           
           // Process
           float temperature = convert_to_celsius(adc_value);
           
           // Send to control thread
           send_to_control(temperature);
           
           // Sleep 100 ms (100 ticks if 1 ms tick)
           tx_thread_sleep(100);
       }
   }

**Preemption-Threshold Scheduling (Unique to ThreadX):**

.. code-block:: text

   Preemption-Threshold Concept:
   ─────────────────────────────
   
   Thread Priority:            5 (actual execution priority)
   Preemption Threshold:      10 (can only be preempted by priority ≤10)
   
   Effect:
   • Thread runs at priority 5
   • But can only be preempted by threads with priority 0-10
   • Threads with priority 11-31 CANNOT preempt it
   
   Benefit:
   • Reduces context switches
   • Allows mutex-free critical sections
   • Better real-time performance
   
   Example:
   ─────────
   Thread A: Priority 5, Threshold 5  → Can be preempted by 0-5
   Thread B: Priority 10, Threshold 5 → Runs at 10, but protected from 6-31
   Thread C: Priority 15, Threshold 15 → Can be preempted by 0-15

**Example with Preemption-Threshold:**

.. code-block:: c

   // Thread with preemption-threshold
   
   void create_thread_with_threshold(void) {
       TX_THREAD my_thread;
       UCHAR my_stack[2048];
       
       tx_thread_create(
           &my_thread,
           "Protected Thread",
           thread_entry,
           0,
           my_stack,
           2048,
           15,     // Priority: 15 (runs at this priority)
           10,     // Threshold: 10 (only 0-10 can preempt)
           TX_NO_TIME_SLICE,
           TX_AUTO_START
       );
       
       // This thread runs at priority 15
       // But threads with priority 11-31 cannot preempt it
       // Only threads with priority 0-10 can preempt it
   }
   
   // Change threshold dynamically
   void change_threshold_example(void) {
       UINT old_threshold;
       
       // Lower threshold temporarily (more protection)
       tx_thread_preemption_change(&sensor_thread, 5, &old_threshold);
       
       // Critical section (now protected from priority 6-31)
       access_shared_resource();
       
       // Restore threshold
       tx_thread_preemption_change(&sensor_thread, old_threshold, &old_threshold);
   }

**5.3 ThreadX Synchronization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Semaphores:**

.. code-block:: c

   // ThreadX Semaphore (counting semaphore)
   
   TX_SEMAPHORE resource_semaphore;
   
   // Create semaphore (initial count = 1 for binary semaphore)
   void create_semaphore(void) {
       UINT status;
       
       status = tx_semaphore_create(
           &resource_semaphore,     // Semaphore control block
           "Resource Sem",          // Name
           1                        // Initial count (1=available)
       );
       
       if (status != TX_SUCCESS) {
           printf("ERROR: Semaphore creation failed\n");
       }
   }
   
   // Use semaphore
   void use_resource(void) {
       // Wait for semaphore (decrement, block if 0)
       tx_semaphore_get(&resource_semaphore, TX_WAIT_FOREVER);
       
       // Critical section
       access_shared_resource();
       
       // Release semaphore (increment)
       tx_semaphore_put(&resource_semaphore);
   }
   
   // Counting semaphore (buffer pool)
   TX_SEMAPHORE buffer_pool_sem;
   
   void create_buffer_pool_semaphore(void) {
       // Create with count = 10 (10 buffers available)
       tx_semaphore_create(&buffer_pool_sem, "Buffer Pool", 10);
   }
   
   void allocate_buffer(void) {
       // Wait for available buffer
       tx_semaphore_get(&buffer_pool_sem, TX_WAIT_FOREVER);
       
       // Get buffer from pool
       buffer_t *buf = pool_get_buffer();
       
       // Use buffer
       fill_buffer(buf);
   }
   
   void free_buffer(buffer_t *buf) {
       // Return buffer
       pool_return_buffer(buf);
       
       // Increment semaphore
       tx_semaphore_put(&buffer_pool_sem);
   }

**Mutexes (with Priority Inheritance):**

.. code-block:: c

   // ThreadX Mutex
   
   TX_MUTEX spi_mutex;
   
   // Create mutex (priority inheritance enabled by default)
   void create_mutex(void) {
       UINT status;
       
       status = tx_mutex_create(
           &spi_mutex,              // Mutex control block
           "SPI Mutex",             // Name
           TX_INHERIT               // Priority inheritance (or TX_NO_INHERIT)
       );
   }
   
   // Use mutex
   void access_spi_bus(void) {
       // Lock mutex
       tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
       
       // Critical section (exclusive SPI access)
       spi_transfer(data, len);
       
       // Unlock mutex
       tx_mutex_put(&spi_mutex);
   }

**Event Flags:**

.. code-block:: c

   // ThreadX Event Flags (32-bit event group)
   
   TX_EVENT_FLAGS_GROUP system_events;
   
   // Event flags
   #define EVENT_SENSOR_READY     (1 << 0)
   #define EVENT_DATA_PROCESSED   (1 << 1)
   #define EVENT_TX_COMPLETE      (1 << 2)
   #define EVENT_ERROR            (1 << 3)
   
   // Create event group
   void create_events(void) {
       tx_event_flags_create(&system_events, "System Events");
   }
   
   // Set event (signal)
   void sensor_isr(void) {
       tx_event_flags_set(&system_events, EVENT_SENSOR_READY, TX_OR);
   }
   
   // Wait for event (AND logic)
   void wait_for_both_events(void) {
       ULONG actual_flags;
       
       // Wait for BOTH sensor ready AND data processed
       tx_event_flags_get(
           &system_events,
           EVENT_SENSOR_READY | EVENT_DATA_PROCESSED,
           TX_AND_CLEAR,        // Wait for ALL, clear on success
           &actual_flags,
           TX_WAIT_FOREVER
       );
       
       printf("Both events occurred!\n");
   }
   
   // Wait for any event (OR logic)
   void wait_for_any_event(void) {
       ULONG actual_flags;
       
       // Wait for ANY of the events
       tx_event_flags_get(
           &system_events,
           EVENT_SENSOR_READY | EVENT_DATA_PROCESSED | EVENT_ERROR,
           TX_OR_CLEAR,         // Wait for ANY, clear on success
           &actual_flags,
           TX_WAIT_FOREVER
       );
       
       // Check which event occurred
       if (actual_flags & EVENT_ERROR) {
           handle_error();
       } else if (actual_flags & EVENT_SENSOR_READY) {
           process_sensor();
       }
   }

**Message Queues:**

.. code-block:: c

   // ThreadX Message Queue
   
   TX_QUEUE sensor_queue;
   ULONG queue_storage[100];  // Storage for 100 ULONGs
   
   // Create queue (4-ULONG messages, 25 max messages)
   void create_queue(void) {
       UINT status;
       
       status = tx_queue_create(
           &sensor_queue,           // Queue control block
           "Sensor Queue",          // Name
           TX_4_ULONG,              // Message size (4 × 4 bytes = 16 bytes)
           queue_storage,           // Queue memory
           sizeof(queue_storage)    // Queue size in bytes
       );
       
       // Calculates capacity: sizeof(queue_storage) / (4 × 4) = 25 messages
   }
   
   // Send message (structure as 4 ULONGs)
   typedef struct {
       ULONG sensor_id;
       ULONG value;
       ULONG timestamp_hi;
       ULONG timestamp_lo;
   } SENSOR_MSG;
   
   void send_sensor_data(void) {
       SENSOR_MSG msg;
       
       msg.sensor_id = 1;
       msg.value = read_sensor();
       msg.timestamp_hi = 0;
       msg.timestamp_lo = tx_time_get();
       
       // Send (non-blocking)
       UINT status = tx_queue_send(&sensor_queue, &msg, TX_NO_WAIT);
       
       if (status == TX_QUEUE_FULL) {
           printf("Queue full!\n");
       }
   }
   
   // Receive message
   void receive_sensor_data(void) {
       SENSOR_MSG msg;
       
       // Receive (blocking)
       tx_queue_receive(&sensor_queue, &msg, TX_WAIT_FOREVER);
       
       printf("Received: Sensor %lu = %lu\n", msg.sensor_id, msg.value);
   }

**5.4 ThreadX Memory Management**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Block Pools (Fixed-Size Allocation):**

.. code-block:: c

   // ThreadX Block Pool
   
   TX_BLOCK_POOL packet_pool;
   UCHAR pool_memory[10 * 256];  // 10 blocks × 256 bytes
   
   // Create block pool
   void create_block_pool(void) {
       UINT status;
       
       status = tx_block_pool_create(
           &packet_pool,            // Pool control block
           "Packet Pool",           // Name
           256,                     // Block size
           pool_memory,             // Pool memory
           sizeof(pool_memory)      // Pool size (10 blocks)
       );
   }
   
   // Allocate block
   void allocate_packet(void) {
       UCHAR *packet;
       
       // Allocate block (blocking)
       tx_block_allocate(&packet_pool, (VOID **)&packet, TX_WAIT_FOREVER);
       
       // Use packet
       fill_packet(packet);
       
       // Release block
       tx_block_release(packet);
   }

**Byte Pools (Variable-Size Allocation):**

.. code-block:: c

   // ThreadX Byte Pool (like malloc)
   
   TX_BYTE_POOL system_pool;
   UCHAR pool_memory[8192];  // 8 KB heap
   
   // Create byte pool
   void create_byte_pool(void) {
       tx_byte_pool_create(
           &system_pool,
           "System Pool",
           pool_memory,
           sizeof(pool_memory)
       );
   }
   
   // Allocate memory
   void allocate_variable_memory(void) {
       UCHAR *buffer;
       
       // Allocate 512 bytes
       tx_byte_allocate(&system_pool, (VOID **)&buffer, 512, TX_WAIT_FOREVER);
       
       // Use buffer
       memset(buffer, 0, 512);
       
       // Release memory
       tx_byte_release(buffer);
   }

**5.5 ThreadX Timers**
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // ThreadX Application Timer
   
   TX_TIMER periodic_timer;
   
   // Timer expiration callback
   void timer_callback(ULONG param) {
       printf("Timer expired! Param: 0x%lX\n", param);
       
       // Toggle LED
       toggle_led();
       
       // Post event
       tx_event_flags_set(&system_events, EVENT_TIMER_EXPIRED, TX_OR);
   }
   
   // Create periodic timer (100 ticks period)
   void create_timer(void) {
       UINT status;
       
       status = tx_timer_create(
           &periodic_timer,         // Timer control block
           "Periodic Timer",        // Name
           timer_callback,          // Expiration function
           0x5678,                  // Expiration input (param)
           100,                     // Initial ticks (100 ms if 1 ms tick)
           100,                     // Reschedule ticks (periodic)
           TX_AUTO_ACTIVATE         // Auto-start
       );
   }
   
   // One-shot timer (reschedule ticks = 0)
   void create_oneshot_timer(void) {
       tx_timer_create(
           &periodic_timer,
           "One-Shot Timer",
           timer_callback,
           0,
           500,                     // 500 ticks delay
           0,                       // 0 = one-shot (don't reschedule)
           TX_AUTO_ACTIVATE
       );
   }
   
   // Start/stop timer dynamically
   void control_timer(void) {
       // Stop timer
       tx_timer_deactivate(&periodic_timer);
       
       // Change period
       tx_timer_change(&periodic_timer, 200, 200);  // 200 ticks
       
       // Restart timer
       tx_timer_activate(&periodic_timer);
   }

═══════════════════════════════════════════════════════════════════════

🔒 **6. INTEGRITY RTOS (SAFETY-CRITICAL)**
─────────────────────────────────────────────────────────────────────────

**Your Experience: Avionics Fuel Controller (DO-178B Level A)**

**6.1 Integrity Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Integrity Characteristics:**

.. code-block:: text

   Green Hills Integrity RTOS:
   ───────────────────────────
   • Partitioned architecture (time & space partitioning)
   • ARINC 653 compliant
   • Microkernel design (similar to QNX)
   • Safety certifications:
     * DO-178B/C Level A (DAL A)
     * IEC 61508 SIL 3/4
     * ISO 26262 ASIL D
     * EN 50128 SIL 4
   • Formally proven separation kernel
   • Common Criteria EAL 6+ certified
   • Used in: Avionics, automotive, medical, nuclear

**Integrity Architecture:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │  Address Spaces (Isolated Partitions)                   │
   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
   │  │AddressSpace1│  │AddressSpace2│  │AddressSpace3│    │
   │  │             │  │             │  │             │    │
   │  │ Task A      │  │ Task C      │  │ Task E      │    │
   │  │ Task B      │  │ Task D      │  │ Task F      │    │
   │  │             │  │             │  │             │    │
   │  │ (Safety)    │  │ (Control)   │  │ (Comm)      │    │
   │  └─────────────┘  └─────────────┘  └─────────────┘    │
   └──────────────────────┬──────────────────────────────────┘
                          │ Controlled communication
   ┌──────────────────────▼──────────────────────────────────┐
   │  Integrity Separation Kernel                            │
   │  • Memory protection (MMU/MPU)                          │
   │  • Time partitioning (ARINC 653 scheduling)             │
   │  • Resource isolation                                   │
   │  • Inter-partition communication (IPC)                  │
   └──────────────────────┬──────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────┐
   │  Hardware (ARM Cortex-R5, PowerPC)                      │
   └─────────────────────────────────────────────────────────┘

**6.2 Integrity Partitioning**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Address Space (Partition) Definition:**

.. code-block:: c

   // Integrity .int file (system configuration)
   
   // Address Space for safety-critical fuel control
   AddressSpace FuelControlSpace {
       Language C
       Heap 64K
       
       // Tasks within this partition
       Task FuelMonitorTask {
           StackSize 8K
           Priority 100
           StartIt true
       }
       
       Task FuelCalculationTask {
           StackSize 8K
           Priority 90
           StartIt true
       }
       
       // Memory region (protected from other address spaces)
       MemoryRegion {
           Start 0x80000000
           Size 256K
           Attributes ReadWrite
       }
   }
   
   // Address Space for communication (lower criticality)
   AddressSpace CommSpace {
       Language C
       Heap 128K
       
       Task CANCommTask {
           StackSize 16K
           Priority 80
           StartIt true
       }
       
       MemoryRegion {
           Start 0x80100000
           Size 512K
           Attributes ReadWrite
       }
   }
   
   // Shared memory region (for inter-partition communication)
   SharedMemory FuelDataShared {
       Size 4K
       AddressSpaces FuelControlSpace, CommSpace
   }

**6.3 Integrity Task Management**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Task Creation (Static Configuration):**

.. code-block:: c

   // Integrity tasks are defined in .int file
   // No dynamic task creation in safety mode
   
   // C code for task
   void FuelMonitorTask(void) {
       // Integrity tasks don't take parameters
       // Use shared memory or message passing for data
       
       while(1) {
           // Read fuel sensors
           uint32_t fuel_level = read_fuel_level_sensor();
           uint32_t fuel_flow = read_fuel_flow_sensor();
           
           // Store in shared memory
           write_fuel_data(fuel_level, fuel_flow);
           
           // Sleep 100 ms
           Sleep(MilliSeconds(100));
       }
   }
   
   void FuelCalculationTask(void) {
       while(1) {
           // Read from shared memory
           uint32_t fuel_level = read_fuel_level();
           uint32_t fuel_flow = read_fuel_flow();
           
           // Calculate remaining flight time
           uint32_t flight_time = calculate_endurance(fuel_level, fuel_flow);
           
           // Send to display via message
           send_fuel_message(flight_time);
           
           Sleep(MilliSeconds(500));
       }
   }

**6.4 Integrity IPC (Inter-Partition Communication)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Shared Memory (Fastest, but requires synchronization):**

.. code-block:: c

   // Integrity Shared Memory
   
   // Define in .int file
   SharedMemory SensorDataRegion {
       Size 1024
       AddressSpaces SafetySpace, ControlSpace
   }
   
   // Access from C code
   typedef struct {
       uint32_t sensor_id;
       float value;
       uint32_t timestamp;
       uint8_t valid;
   } SensorData;
   
   // Writer (in SafetySpace)
   void write_sensor_data(uint32_t id, float value) {
       // Map shared memory
       SensorData *shared = (SensorData *)MapSharedMemory("SensorDataRegion");
       
       // Write data (atomic on 32-bit aligned writes)
       shared->sensor_id = id;
       shared->value = value;
       shared->timestamp = GetTicks();
       __sync_synchronize();  // Memory barrier
       shared->valid = 1;     // Mark as valid (last)
       
       UnmapSharedMemory(shared);
   }
   
   // Reader (in ControlSpace)
   float read_sensor_data(uint32_t id) {
       SensorData *shared = (SensorData *)MapSharedMemory("SensorDataRegion");
       
       // Read data
       while (!shared->valid) {
           // Wait for valid data
           Sleep(MilliSeconds(1));
       }
       
       float value = shared->value;
       shared->valid = 0;  // Mark as consumed
       
       UnmapSharedMemory(shared);
       return value;
   }

**Message Passing (Safer, Kernel-Mediated):**

.. code-block:: c

   // Integrity Message Passing (Connection objects)
   
   // Define in .int file
   Connection FuelDataConnection {
       Source FuelControlSpace.FuelMonitorTask
       Destination CommSpace.CANCommTask
       MessageSize 64
       QueueSize 10
   }
   
   // Sender (FuelMonitorTask)
   void send_fuel_data(void) {
       typedef struct {
           uint32_t fuel_level;
           uint32_t fuel_flow;
           uint32_t timestamp;
       } FuelMsg;
       
       FuelMsg msg;
       msg.fuel_level = 1500;  // Liters
       msg.fuel_flow = 25;     // L/min
       msg.timestamp = GetTicks();
       
       // Send message
       Connection conn = GetConnectionByName("FuelDataConnection");
       SendMessage(conn, &msg, sizeof(msg));
   }
   
   // Receiver (CANCommTask)
   void receive_fuel_data(void) {
       FuelMsg msg;
       
       Connection conn = GetConnectionByName("FuelDataConnection");
       
       // Receive (blocking)
       ReceiveMessage(conn, &msg, sizeof(msg));
       
       printf("Fuel: %u L, Flow: %u L/min\n", msg.fuel_level, msg.fuel_flow);
       
       // Transmit on CAN bus
       transmit_can_message(CAN_FUEL_ID, &msg);
   }

**6.5 Integrity Time Partitioning (ARINC 653)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Time Partition Schedule:**

.. code-block:: c

   // Integrity time partitioning (.int file)
   
   // Define schedule (100 ms major frame)
   Schedule MainSchedule {
       MajorFrame 100ms
       
       // Safety partition: 40 ms (40% CPU)
       Partition FuelControlSpace {
           Duration 40ms
           Offset 0ms
       }
       
       // Control partition: 30 ms (30% CPU)
       Partition ControlSpace {
           Duration 30ms
           Offset 40ms
       }
       
       // Communication partition: 20 ms (20% CPU)
       Partition CommSpace {
           Duration 20ms
           Offset 70ms
       }
       
       // Idle: 10 ms (10% CPU)
       // Offset 90ms-100ms
   }
   
   // Timeline visualization:
   // ┌────────────────────────────────────────────────────────┐
   // │ Major Frame: 100 ms                                    │
   // ├────────────────┬──────────────┬──────────┬─────────────┤
   // │ FuelControl    │ Control      │ Comm     │ Idle        │
   // │ 40 ms          │ 30 ms        │ 20 ms    │ 10 ms       │
   // └────────────────┴──────────────┴──────────┴─────────────┘
   //   0ms            40ms           70ms        90ms    100ms

**6.6 Integrity Safety Features**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Memory Protection:**

.. code-block:: text

   Integrity Memory Protection:
   ────────────────────────────
   
   • Each AddressSpace has isolated memory regions
   • Hardware MMU/MPU enforcement
   • No shared memory unless explicitly defined
   • Stack overflow detection (guard pages)
   • Read-only code sections
   • NX (No-Execute) data sections
   
   Example Memory Map:
   ───────────────────
   0x00000000 - 0x000FFFFF: Kernel (protected)
   0x80000000 - 0x8003FFFF: FuelControl (256 KB, isolated)
   0x80100000 - 0x8017FFFF: Control (512 KB, isolated)
   0x80200000 - 0x80200FFF: Shared memory (4 KB, explicit)

**Health Monitoring:**

.. code-block:: c

   // Integrity Health Monitoring
   
   // Define in .int file
   HealthMonitor FuelMonitor {
       Task FuelMonitorTask
       Timeout 200ms           // Task must check in every 200 ms
       Action RestartTask      // Restart task on timeout
   }
   
   // C code
   void FuelMonitorTask(void) {
       while(1) {
           // Do work
           monitor_fuel_sensors();
           
           // Check in with health monitor (heartbeat)
           ReportHealth();
           
           Sleep(MilliSeconds(100));  // Check in every 100 ms (< 200 ms timeout)
       }
   }

**Error Handling:**

.. code-block:: c

   // Integrity error handling
   
   void FuelCalculationTask(void) {
       Error err;
       
       while(1) {
           // Read fuel data
           err = read_fuel_level(&fuel_level);
           
           if (err != Success) {
               // Log error
               LogError(ERROR_FUEL_SENSOR_FAILURE, err);
               
               // Use default safe value
               fuel_level = FUEL_LEVEL_UNKNOWN;
               
               // Raise partition error
               RaisePartitionError(ERROR_SENSOR);
           }
           
           // Continue with safe degraded operation
       }
   }

═══════════════════════════════════════════════════════════════════════

📊 **7. RTOS COMPARISON**
─────────────────────────────────────────────────────────────────────────

**7.1 Feature Comparison**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌─────────────────────┬────────────┬────────────┬────────────┐
   │ Feature             │ MQX        │ ThreadX    │ Integrity  │
   ├─────────────────────┼────────────┼────────────┼────────────┤
   │ Scheduling          │ Preemptive │ Preemptive │ Partition  │
   │                     │ priority   │ priority + │ + priority │
   │                     │            │ threshold  │            │
   │                     │            │            │            │
   │ Priority Levels     │ 1-255      │ 0-31       │ 1-255      │
   │                     │            │            │            │
   │ Context Switch      │ 3-5 µs     │ 1-3 µs     │ 5-10 µs    │
   │                     │            │            │ (partition)│
   │                     │            │            │            │
   │ Footprint (code)    │ 10-20 KB   │ 2-5 KB     │ 50-100 KB  │
   │                     │            │            │ (kernel)   │
   │                     │            │            │            │
   │ RAM Usage           │ 2-5 KB     │ 1-2 KB     │ 10-20 KB   │
   │                     │            │            │            │
   │ Safety Cert         │ None       │ DO-178B    │ DO-178B/C  │
   │                     │            │ IEC 61508  │ Level A    │
   │                     │            │            │ EAL 6+     │
   │                     │            │            │            │
   │ Partitioning        │ No         │ No         │ Yes (ARINC │
   │                     │            │            │ 653)       │
   │                     │            │            │            │
   │ License Cost        │ Free (NXP) │ Free (MIT) │ $$$        │
   │                     │            │ (Azure)    │ (per seat) │
   │                     │            │            │            │
   │ Best For            │ NXP MCUs   │ General    │ Safety-    │
   │                     │ Industrial │ embedded   │ critical   │
   │                     │            │            │ avionics   │
   └─────────────────────┴────────────┴────────────┴────────────┘

**7.2 API Comparison**
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌──────────────────┬──────────────────┬──────────────────┬────────────────┐
   │ Operation        │ MQX              │ ThreadX          │ Integrity      │
   ├──────────────────┼──────────────────┼──────────────────┼────────────────┤
   │ Create Task      │ _task_create()   │ tx_thread_create()│ Static (.int) │
   │                  │                  │                  │                │
   │ Delay            │ _time_delay(ms)  │ tx_thread_sleep()│ Sleep(ms)      │
   │                  │                  │                  │                │
   │ Semaphore Get    │ _lwsem_wait()    │ tx_semaphore_get()│ WaitSemaphore()│
   │                  │                  │                  │                │
   │ Semaphore Post   │ _lwsem_post()    │ tx_semaphore_put()│ PostSemaphore()│
   │                  │                  │                  │                │
   │ Mutex Lock       │ _mutex_lock()    │ tx_mutex_get()   │ LockMutex()    │
   │                  │                  │                  │                │
   │ Mutex Unlock     │ _mutex_unlock()  │ tx_mutex_put()   │ UnlockMutex()  │
   │                  │                  │                  │                │
   │ Message Send     │ _msgq_send()     │ tx_queue_send()  │ SendMessage()  │
   │                  │                  │                  │                │
   │ Message Receive  │ _msgq_receive()  │ tx_queue_receive()│ ReceiveMessage()│
   │                  │                  │                  │                │
   │ Event Set        │ _lwevent_set()   │ tx_event_flags_  │ SetEvent()     │
   │                  │                  │ set()            │                │
   │                  │                  │                  │                │
   │ Event Wait       │ _lwevent_wait_   │ tx_event_flags_  │ WaitForEvent() │
   │                  │ for()            │ get()            │                │
   └──────────────────┴──────────────────┴──────────────────┴────────────────┘

**7.3 Use Case Recommendations**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   When to Use Each RTOS:
   ──────────────────────
   
   MQX:
   ✅ NXP Kinetis/i.MX RT microcontrollers
   ✅ Industrial automation (PLCs, gateways)
   ✅ Motor control applications
   ✅ No safety certification required
   ✅ Existing NXP ecosystem (good BSP support)
   
   ThreadX (Azure RTOS):
   ✅ General embedded applications
   ✅ IoT devices (integrates with Azure cloud)
   ✅ Medical devices (IEC 62304 certified)
   ✅ Small footprint requirements (<5 KB)
   ✅ Open-source preference (MIT license)
   ✅ Preemption-threshold needed (unique feature)
   
   Integrity:
   ✅ Safety-critical avionics (DO-178C Level A)
   ✅ Automotive (ISO 26262 ASIL D)
   ✅ Railway (EN 50128 SIL 4)
   ✅ Mixed-criticality systems (partitioning required)
   ✅ Highest security needs (Common Criteria EAL 6+)
   ✅ Budget available (expensive licensing)

═══════════════════════════════════════════════════════════════════════

🎓 **8. OSEK/VDX RTOS (AUTOMOTIVE)**
─────────────────────────────────────────────────────────────────────────

**OSEK/VDX** = **O**pen **S**ystems and their Interfaces for the **E**lectronics in Motor Vehicles / **V**ehicle **D**istributed E**X**ecutive

**8.1 OSEK Overview**
~~~~~~~~~~~~~~~~~~~~~~

**OSEK Characteristics:**

.. code-block:: text

   OSEK/VDX Features (AUTOSAR predecessor):
   ────────────────────────────────────────
   • Static configuration (all objects defined at compile-time)
   • Conformance classes: BCC1, BCC2, ECC1, ECC2
   • Priority-based scheduling
   • No dynamic memory allocation
   • Minimal RAM footprint (500 bytes - 2 KB)
   • Used in: Automotive ECUs, AUTOSAR Classic
   
   Your Experience: MICORSAR (Automotive ECU projects)

**OSEK Conformance Classes:**

.. code-block:: text

   ┌─────────┬───────────────────────────────────────────┐
   │ Class   │ Features                                  │
   ├─────────┼───────────────────────────────────────────┤
   │ BCC1    │ Basic tasks, 1 task per priority          │
   │ (Basic) │ No extended tasks (no waiting)            │
   │         │ FIFO activation queue                     │
   │         │                                           │
   │ BCC2    │ Basic tasks, multiple per priority        │
   │         │ Priority-based activation queue           │
   │         │                                           │
   │ ECC1    │ Extended tasks (can wait), 1 per priority │
   │ (Ext)   │ Events supported                          │
   │         │                                           │
   │ ECC2    │ Extended tasks, multiple per priority     │
   │         │ Full OSEK feature set                     │
   └─────────┴───────────────────────────────────────────┘

**8.2 OSEK Task Types**
~~~~~~~~~~~~~~~~~~~~~~~~

**Basic Tasks vs Extended Tasks:**

.. code-block:: text

   Basic Task:
   ───────────
   • Runs to completion (cannot block)
   • No WaitEvent() allowed
   • Terminated by TerminateTask()
   • Lower overhead (no wait queues)
   
   State Machine:
      SUSPENDED → READY → RUNNING → SUSPENDED
   
   Extended Task:
   ──────────────
   • Can wait for events (WaitEvent())
   • Remains in memory when waiting
   • Higher RAM usage (stack preserved)
   
   State Machine:
      SUSPENDED → READY → RUNNING → WAITING → READY → SUSPENDED

**OSEK Task Configuration:**

.. code-block:: c

   // OSEK Configuration (OIL - OSEK Implementation Language)
   
   TASK EngineControlTask {
       PRIORITY = 10;           // Higher number = higher priority
       SCHEDULE = FULL;         // Preemptive (or NON for non-preemptive)
       ACTIVATION = 1;          // Max simultaneous activations
       AUTOSTART = TRUE;        // Start at system init
       STACKSIZE = 512;         // Stack size in bytes
   };
   
   TASK SensorTask {
       PRIORITY = 5;
       SCHEDULE = FULL;
       ACTIVATION = 3;          // Can be activated 3 times concurrently
       AUTOSTART = FALSE;
       STACKSIZE = 256;
   };
   
   TASK IdleTask {
       PRIORITY = 1;            // Lowest priority
       SCHEDULE = FULL;
       ACTIVATION = 1;
       AUTOSTART = TRUE;
       STACKSIZE = 128;
   };
   
   // Events for extended tasks
   EVENT IgnitionEvent {
       MASK = 0x01;
   };
   
   EVENT FuelInjectionEvent {
       MASK = 0x02;
   };

**OSEK Task Implementation:**

.. code-block:: c

   // OSEK C Code
   
   #include "os.h"
   
   // Basic task (runs to completion)
   TASK(SensorTask) {
       // Read sensors
       uint16_t rpm = read_engine_rpm();
       uint16_t throttle = read_throttle_position();
       
       // Store in shared memory
       g_engine_rpm = rpm;
       g_throttle_pos = throttle;
       
       // Signal event to extended task
       SetEvent(EngineControlTask, IgnitionEvent);
       
       // Terminate (return to SUSPENDED state)
       TerminateTask();
   }
   
   // Extended task (can wait for events)
   TASK(EngineControlTask) {
       while(1) {
           // Wait for event (task enters WAITING state)
           WaitEvent(IgnitionEvent | FuelInjectionEvent);
           
           // Get which events occurred
           EventMaskType events;
           GetEvent(EngineControlTask, &events);
           
           // Clear events
           ClearEvent(IgnitionEvent | FuelInjectionEvent);
           
           // Process based on event
           if (events & IgnitionEvent) {
               calculate_ignition_timing();
           }
           
           if (events & FuelInjectionEvent) {
               calculate_fuel_injection();
           }
       }
       
       // Extended tasks typically never terminate
   }

**8.3 OSEK Alarms**
~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // OSEK Alarm Configuration (OIL)
   
   COUNTER SystemCounter {
       MINCYCLE = 1;            // Minimum cycle time
       MAXALLOWEDVALUE = 65535; // 16-bit counter
       TICKSPERBASE = 1;        // 1 tick = 1 ms
   };
   
   ALARM CyclicSensorAlarm {
       COUNTER = SystemCounter;
       ACTION = ACTIVATETASK {
           TASK = SensorTask;   // Activate SensorTask periodically
       };
       AUTOSTART = TRUE {
           ALARMTIME = 10;      // First activation at 10 ms
           CYCLETIME = 100;     // Repeat every 100 ms
       };
   };
   
   ALARM IgnitionAlarm {
       COUNTER = SystemCounter;
       ACTION = SETEVENT {
           TASK = EngineControlTask;
           EVENT = IgnitionEvent;
       };
       AUTOSTART = FALSE;       // Started dynamically
   };

**OSEK Alarm API:**

.. code-block:: c

   // OSEK Alarm Usage
   
   void setup_periodic_alarm(void) {
       // Set relative alarm (trigger after 500 ms, repeat every 100 ms)
       SetRelAlarm(CyclicSensorAlarm, 500, 100);
   }
   
   void setup_oneshot_alarm(void) {
       // Set one-shot alarm (trigger after 1000 ms, no repeat)
       SetRelAlarm(IgnitionAlarm, 1000, 0);
   }
   
   void cancel_alarm(void) {
       CancelAlarm(CyclicSensorAlarm);
   }

**8.4 OSEK Resources (Mutex):**

.. code-block:: c

   // OSEK Resource Configuration (OIL)
   
   RESOURCE SharedSPIResource {
       RESOURCEPROPERTY = STANDARD;
   };
   
   // C Code - Using resource (like mutex)
   TASK(Task1) {
       // Lock resource
       GetResource(SharedSPIResource);
       
       // Critical section (protected from preemption by priority ceiling)
       spi_transfer(data, len);
       
       // Unlock resource
       ReleaseResource(SharedSPIResource);
       
       TerminateTask();
   }
   
   // Priority Ceiling Protocol:
   // - When Task1 acquires SharedSPIResource, its priority is raised
   //   to the highest priority of any task that uses this resource
   // - Prevents priority inversion automatically

═══════════════════════════════════════════════════════════════════════

⚡ **9. REAL-TIME SCHEDULING THEORY**
─────────────────────────────────────────────────────────────────────────

**9.1 Schedulability Analysis**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Rate Monotonic Scheduling (RMS):**

.. code-block:: text

   RMS Theory:
   ───────────
   • Optimal static priority assignment for periodic tasks
   • Rule: Shorter period → Higher priority
   • Schedulability test: U ≤ n(2^(1/n) - 1)
   
   Where:
   U = Σ (C_i / T_i)    # Total CPU utilization
   C_i = Worst-case execution time of task i
   T_i = Period of task i
   n = Number of tasks
   
   Schedulability Bound:
   n=1:  U ≤ 1.000  (100%)
   n=2:  U ≤ 0.828  (82.8%)
   n=3:  U ≤ 0.780  (78.0%)
   n=4:  U ≤ 0.757  (75.7%)
   n→∞:  U ≤ 0.693  (69.3%)

**RMS Example:**

.. code-block:: c

   // Three periodic tasks
   
   // Task A: Period = 10 ms, Execution = 2 ms
   void task_a(void) {
       uint32_t start = get_time_ms();
       
       process_sensor_data();  // 2 ms worst-case
       
       wait_until_next_period(start + 10);
   }
   
   // Task B: Period = 20 ms, Execution = 3 ms
   void task_b(void) {
       uint32_t start = get_time_ms();
       
       calculate_control_output();  // 3 ms worst-case
       
       wait_until_next_period(start + 20);
   }
   
   // Task C: Period = 50 ms, Execution = 5 ms
   void task_c(void) {
       uint32_t start = get_time_ms();
       
       transmit_to_network();  // 5 ms worst-case
       
       wait_until_next_period(start + 50);
   }
   
   // Priority Assignment (RMS):
   // Task A: Priority 1 (highest) - shortest period (10 ms)
   // Task B: Priority 2           - medium period (20 ms)
   // Task C: Priority 3 (lowest)  - longest period (50 ms)
   
   // Schedulability Check:
   // U = (2/10) + (3/20) + (5/50)
   //   = 0.20 + 0.15 + 0.10
   //   = 0.45
   // 
   // Threshold: 3(2^(1/3) - 1) = 0.78
   // 0.45 ≤ 0.78 ✅ Schedulable!

**Deadline Monotonic Scheduling (DMS):**

.. code-block:: text

   DMS (Generalization of RMS):
   ────────────────────────────
   • For tasks where deadline ≠ period
   • Rule: Shorter deadline → Higher priority
   • Example: Task with period=100ms, deadline=50ms
   
   Task properties:
   ────────────────
   T_i = Period (time between activations)
   D_i = Relative deadline (must complete within this time)
   C_i = Execution time
   
   Constraint: D_i ≤ T_i (deadline cannot exceed period)

**9.2 Worst-Case Execution Time (WCET)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Measuring WCET:**

.. code-block:: c

   // WCET measurement using hardware timer
   
   volatile uint32_t wcet_max = 0;
   
   void measure_wcet(void) {
       uint32_t start, end, elapsed;
       
       // Disable interrupts for accurate measurement
       __disable_irq();
       
       // Start timer
       start = DWT->CYCCNT;  // ARM Cortex-M cycle counter
       
       // Execute function
       process_sensor_data();
       
       // End timer
       end = DWT->CYCCNT;
       
       __enable_irq();
       
       // Calculate elapsed cycles
       elapsed = end - start;
       
       // Track maximum
       if (elapsed > wcet_max) {
           wcet_max = elapsed;
           printf("New WCET: %u cycles (%.2f µs)\n", 
                  elapsed, 
                  (float)elapsed / CPU_FREQ_MHZ);
       }
   }
   
   // Convert to time
   // At 120 MHz: 1 cycle = 1/120,000,000 sec = 8.33 ns
   // 10,000 cycles = 83.3 µs

**Static WCET Analysis Tools:**

.. code-block:: text

   WCET Analysis Tools:
   ────────────────────
   • aiT WCET Analyzer (AbsInt)
   • RapiTime (Rapita Systems)
   • Bound-T (Tidorum)
   • OTAWA (Open-source)
   
   Techniques:
   ───────────
   1. Static analysis (control flow + CPU model)
   2. Measurement-based (run with worst-case inputs)
   3. Hybrid (combine both methods)
   
   Challenges:
   ───────────
   • Cache effects (instruction/data cache)
   • Pipeline stalls
   • Branch prediction
   • Memory access latency
   • Interrupts (add overhead)

**9.3 Priority Inversion Solutions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem Recap:**

.. code-block:: text

   Priority Inversion Scenario:
   ────────────────────────────
   High-priority task (H) blocked by low-priority task (L)
   Medium-priority task (M) preempts L while L holds resource
   → H waits for L, but L is blocked by M
   → Unbounded priority inversion!

**Solution 1: Priority Inheritance Protocol (PIP):**

.. code-block:: c

   // MQX Mutex with Priority Inheritance
   
   MUTEX_STRUCT resource_mutex;
   MUTEX_ATTR_STRUCT attr;
   
   void init_pip_mutex(void) {
       _mutatr_init(&attr);
       _mutatr_set_wait_protocol(&attr, MUTEX_PRIO_INHERIT);
       _mutex_init(&resource_mutex, &attr);
   }
   
   // Low-priority task
   void low_priority_task(void) {
       _mutex_lock(&resource_mutex);  // Acquires mutex
       
       // If high-priority task tries to lock mutex:
       // → Low task inherits high priority
       // → Medium task cannot preempt low task
       // → Low task completes critical section faster
       
       critical_section();
       
       _mutex_unlock(&resource_mutex);  // Priority restored
   }

**Solution 2: Priority Ceiling Protocol (PCP):**

.. code-block:: c

   // OSEK Resource (uses Priority Ceiling)
   
   // Configuration: Resource ceiling = highest priority of any task using it
   RESOURCE SharedResource {
       RESOURCEPROPERTY = STANDARD;
   };
   
   // Tasks using the resource:
   // - Task H (priority 10)
   // - Task L (priority 5)
   // → Resource ceiling = 10
   
   TASK(LowPriorityTask) {
       // When GetResource() is called:
       // → Task L's priority raised to 10 (ceiling)
       // → No task can preempt L while it holds resource
       GetResource(SharedResource);
       
       critical_section();
       
       ReleaseResource(SharedResource);  // Priority restored to 5
       
       TerminateTask();
   }

**Comparison:**

.. code-block:: text

   Priority Inheritance vs Priority Ceiling:
   ──────────────────────────────────────────
   
   Priority Inheritance (PIP):
   ✅ Lower overhead (priority raised only when needed)
   ❌ Still allows some blocking
   ❌ Possible deadlock with nested locks
   
   Priority Ceiling (PCP):
   ✅ Prevents deadlock (if ceiling assigned correctly)
   ✅ Bounded blocking time
   ❌ Higher overhead (always raises to ceiling)
   ❌ Requires knowing all tasks using resource at compile-time

═══════════════════════════════════════════════════════════════════════

🚀 **10. RTOS OPTIMIZATION**
─────────────────────────────────────────────────────────────────────────

**10.1 Reducing Context Switch Overhead**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Lazy FPU Context Switching:**

.. code-block:: c

   // ARM Cortex-M4 with FPU
   
   // Default: FPU registers (S0-S31) saved on every context switch
   // → 32 registers × 4 bytes = 128 bytes extra
   // → Adds ~500 ns to context switch
   
   // Optimization: Lazy FPU stacking
   // → FPU registers saved only when next task uses FPU
   // → Enabled via FPCCR register
   
   void enable_lazy_fpu_stacking(void) {
       // FPU->FPCCR |= FPU_FPCCR_LSPEN_Msk | FPU_FPCCR_ASPEN_Msk;
       
       // LSPEN: Lazy stacking enable
       // ASPEN: Automatic state preservation enable
       
       // Result: Tasks not using FPU don't pay FPU context switch cost
   }

**Minimize Task Switching Frequency:**

.. code-block:: c

   // BAD: Excessive task switches
   void sensor_task_bad(void) {
       while(1) {
           read_sensor();
           _time_delay(1);  // Sleep 1 ms → 1000 switches/second!
       }
   }
   
   // GOOD: Longer sleep period
   void sensor_task_good(void) {
       while(1) {
           read_sensor();
           _time_delay(10);  // Sleep 10 ms → 100 switches/second
       }
   }
   
   // Even better: Event-driven (no periodic wakeup)
   void sensor_task_best(void) {
       while(1) {
           // Wait for interrupt (no polling)
           _lwsem_wait(&adc_complete_sem);  // ISR posts semaphore
           
           process_adc_data();
       }
   }

**10.2 Stack Optimization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Stack Size Tuning:**

.. code-block:: c

   // MQX Stack Usage Check
   
   void check_stack_usage(void) {
       _task_id task_id = _task_get_id();
       TD_STRUCT_PTR td = _task_get_td(task_id);
       
       uint32_t stack_size = (uint32_t)td->STACK_BASE - (uint32_t)td->STACK_LIMIT;
       uint32_t stack_used = (uint32_t)td->STACK_BASE - (uint32_t)td->STACK_PTR;
       
       float usage_pct = (float)stack_used / stack_size * 100.0f;
       
       printf("Stack: %u / %u bytes (%.1f%%)\n", 
              stack_used, stack_size, usage_pct);
       
       // Rule of thumb: Aim for 50-70% peak usage
       // Too low: Wasting RAM
       // Too high: Risk of overflow
   }

**Stack Overflow Detection:**

.. code-block:: c

   // ARM Cortex-M MPU for stack overflow detection
   
   void setup_stack_guard(void *stack_base, uint32_t stack_size) {
       // Configure MPU region as read-only guard page
       // Below stack (catches stack overflow)
       
       MPU->RNR = 0;  // Region 0
       MPU->RBAR = (uint32_t)stack_base - 32;  // 32-byte guard below stack
       MPU->RASR = (1 << MPU_RASR_ENABLE_Pos) |
                   (0 << MPU_RASR_AP_Pos) |      // No access (trap on overflow)
                   (4 << MPU_RASR_SIZE_Pos);     // 32 bytes
       
       MPU->CTRL = MPU_CTRL_ENABLE_Msk | MPU_CTRL_PRIVDEFENA_Msk;
       
       // Now stack overflow triggers MemManage fault
   }

**10.3 Interrupt Latency Optimization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Minimize ISR Duration:**

.. code-block:: c

   // BAD: Heavy processing in ISR
   void uart_isr_bad(void) {
       uint8_t data = UART0_D;  // Read data
       
       // ❌ BAD: Complex processing in ISR
       process_protocol(data);
       update_crc(data);
       check_frame_complete();
       
       // ❌ Blocks all lower-priority interrupts for too long!
   }
   
   // GOOD: Minimal ISR, defer to task
   void uart_isr_good(void) {
       uint8_t data = UART0_D;  // Read hardware register
       
       // Store in circular buffer (fast)
       rx_buffer[rx_head++] = data;
       rx_head %= BUFFER_SIZE;
       
       // Signal task (post semaphore)
       _lwsem_post(&uart_rx_sem);
       
       // ✅ ISR completes in <1 µs
   }
   
   // Processing task (runs at task level, can be preempted)
   void uart_rx_task(void) {
       while(1) {
           _lwsem_wait(&uart_rx_sem);
           
           // Heavy processing here (interruptible)
           while (rx_head != rx_tail) {
               uint8_t data = rx_buffer[rx_tail++];
               rx_tail %= BUFFER_SIZE;
               
               process_protocol(data);
           }
       }
   }

**Interrupt Nesting Configuration:**

.. code-block:: c

   // ARM Cortex-M Interrupt Priorities
   
   // Configure critical interrupts at higher priority
   NVIC_SetPriority(DMA_IRQn, 0);      // Highest (0 = most urgent)
   NVIC_SetPriority(UART_IRQn, 5);     // Medium
   NVIC_SetPriority(TIMER_IRQn, 10);   // Low
   
   // BASEPRI register: Mask interrupts below priority threshold
   void enter_critical_section(void) {
       __set_BASEPRI(5 << (8 - __NVIC_PRIO_BITS));  // Block priority ≥5
       // DMA (priority 0) can still interrupt
       // UART (priority 5) and TIMER (priority 10) blocked
   }
   
   void exit_critical_section(void) {
       __set_BASEPRI(0);  // Allow all interrupts
   }

**10.4 Cache Optimization (ARM Cortex-A/R)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Cache-aware data structure placement
   
   // Align frequently-accessed structures to cache line (64 bytes on Cortex-A)
   typedef struct {
       uint32_t counter;
       uint32_t timestamp;
       // ... (total 64 bytes)
   } __attribute__((aligned(64))) CacheLineAligned;
   
   // Prevent false sharing (two CPUs writing to same cache line)
   typedef struct {
       uint32_t cpu0_counter;
       uint8_t padding0[60];  // Pad to 64 bytes
       
       uint32_t cpu1_counter;
       uint8_t padding1[60];  // Separate cache line
   } MultiCoreData;
   
   // Cache maintenance for DMA buffers
   void dma_cache_coherency(void *buffer, uint32_t size) {
       // Before DMA write (CPU → peripheral):
       SCB_CleanDCache_by_Addr(buffer, size);  // Write back dirty cache lines
       
       // Before DMA read (peripheral → CPU):
       SCB_InvalidateDCache_by_Addr(buffer, size);  // Discard stale cache
   }

═══════════════════════════════════════════════════════════════════════

🐛 **11. RTOS DEBUGGING**
─────────────────────────────────────────────────────────────────────────

**11.1 Common RTOS Bugs**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Stack Overflow:**

.. code-block:: c

   // Symptoms:
   // - Random crashes
   // - Task corruption
   // - Variables mysteriously changing
   
   // Detection:
   void detect_stack_overflow(void) {
       TD_STRUCT_PTR td = _task_get_td(_task_get_id());
       
       // Check stack limit (MQX fills unused stack with 0xA5A5A5A5)
       uint32_t *stack_check = (uint32_t *)td->STACK_LIMIT;
       
       if (*stack_check != 0xA5A5A5A5) {
           printf("❌ STACK OVERFLOW DETECTED!\n");
           _task_block();  // Stop task
       }
   }
   
   // Solution:
   // 1. Increase stack size in task template
   // 2. Reduce local variable usage (use static or heap)
   // 3. Reduce call depth (avoid deep recursion)

**Deadlock:**

.. code-block:: c

   // Classic deadlock example
   
   MUTEX_STRUCT mutex_a, mutex_b;
   
   // Task 1
   void task1(void) {
       _mutex_lock(&mutex_a);
       _time_delay(10);  // Simulate work
       _mutex_lock(&mutex_b);  // ❌ Deadlock if task2 holds mutex_b!
       
       critical_section();
       
       _mutex_unlock(&mutex_b);
       _mutex_unlock(&mutex_a);
   }
   
   // Task 2
   void task2(void) {
       _mutex_lock(&mutex_b);  // ← Different lock order!
       _time_delay(10);
       _mutex_lock(&mutex_a);  // ❌ Deadlock if task1 holds mutex_a!
       
       critical_section();
       
       _mutex_unlock(&mutex_a);
       _mutex_unlock(&mutex_b);
   }
   
   // Detection: Tasks stop responding, CPU idle
   // Solution: Always acquire locks in same order

**Priority Inversion (Unbounded):**

.. code-block:: c

   // Detection: High-priority task misses deadlines
   
   void detect_priority_inversion(void) {
       // Monitor task execution times
       // If high-priority task takes unusually long → Check for inversion
       
       // Solution: Use priority inheritance mutexes
       _mutatr_set_wait_protocol(&attr, MUTEX_PRIO_INHERIT);
   }

**11.2 RTOS Debugging Tools**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Task Trace (Execution History):**

.. code-block:: c

   // MQX Kernel Log
   
   void enable_kernel_trace(void) {
       _klog_create(10000, 0);  // 10,000 entries
       
       // Enable tracing
       _klog_control(KLOG_ENABLED | 
                     KLOG_CONTEXT_ENABLED |
                     KLOG_TASK_FUNCTIONS |
                     KLOG_INTERRUPT_FUNCTIONS, TRUE);
   }
   
   // Analyze log
   void print_kernel_log(void) {
       KLOG_ENTRY_STRUCT entry;
       
       while (_klog_get_next_entry(&entry)) {
           printf("[%10u] Task 0x%X: Func %u\n",
                  entry.TIMESTAMP,
                  entry.TASK_ID,
                  entry.FUNCTION);
       }
   }

**RTOS-Aware Debuggers:**

.. code-block:: text

   Debugger RTOS Plugins:
   ──────────────────────
   • Segger Ozone (ThreadX, FreeRTOS, embOS)
   • IAR Embedded Workbench (MQX, ThreadX, µC/OS)
   • Keil MDK (RTX, FreeRTOS, ThreadX)
   • Eclipse + OpenOCD (FreeRTOS, Zephyr)
   
   Features:
   ─────────
   • Task list view (name, priority, state, stack usage)
   • Queue/semaphore inspection
   • Stack backtrace per task
   • CPU usage per task
   • Timeline view (Gantt chart)

**Real-Time Trace (Hardware Trace):**

.. code-block:: c

   // ARM Cortex-M ETM (Embedded Trace Macrocell)
   
   // Hardware trace captures:
   // - Every instruction executed
   // - Every branch taken
   // - Timestamp of each event
   
   // Analyzed with:
   // - Segger SystemView
   // - Percepio Tracealyzer
   // - Lauterbach TRACE32
   
   // Example: Trace task switches
   void trace_task_switch(void) {
       // Insert trace markers in scheduler
       ITM_SendChar('T');  // Instrumentation Trace Macrocell
       ITM_SendChar(task_id);
   }

**11.3 Performance Profiling**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CPU Usage Measurement:**

.. code-block:: c

   // MQX CPU usage tracking
   
   #include <lwtimer.h>
   
   typedef struct {
       _task_id task_id;
       uint32_t total_time_us;
   } TaskStats;
   
   TaskStats task_stats[10];
   
   void measure_cpu_usage(void) {
       uint32_t total_time = 0;
       
       // Get task execution time
       for (int i = 0; i < num_tasks; i++) {
           TD_STRUCT_PTR td = _task_get_td(task_stats[i].task_id);
           
           // MQX tracks per-task CPU time
           TIME_STRUCT elapsed;
           _time_get_elapsed(&elapsed);
           
           task_stats[i].total_time_us = elapsed.SECONDS * 1000000 + 
                                         elapsed.MILLISECONDS * 1000;
           
           total_time += task_stats[i].total_time_us;
       }
       
       // Calculate percentages
       printf("CPU Usage:\n");
       for (int i = 0; i < num_tasks; i++) {
           float pct = (float)task_stats[i].total_time_us / total_time * 100.0f;
           printf("  Task 0x%X: %.1f%%\n", task_stats[i].task_id, pct);
       }
   }

**Instrumentation for Profiling:**

.. code-block:: c

   // Custom profiling hooks
   
   #define PROFILE_START(id) \
       uint32_t _prof_start_##id = DWT->CYCCNT
   
   #define PROFILE_END(id) \
       do { \
           uint32_t _prof_end_##id = DWT->CYCCNT; \
           uint32_t _prof_cycles_##id = _prof_end_##id - _prof_start_##id; \
           printf(#id ": %u cycles\n", _prof_cycles_##id); \
       } while(0)
   
   // Usage:
   void process_data(void) {
       PROFILE_START(fft);
       compute_fft(samples, 1024);
       PROFILE_END(fft);
       
       PROFILE_START(filter);
       apply_filter(samples, 1024);
       PROFILE_END(filter);
   }

═══════════════════════════════════════════════════════════════════════

✅ **KEY TAKEAWAYS**
─────────────────────────────────────────────────────────────────────────

**RTOS Selection:**
1. ✅ **MQX:** NXP Kinetis/i.MX RT, industrial automation, motor control
2. ✅ **ThreadX:** General embedded, IoT, small footprint, open-source
3. ✅ **Integrity:** Safety-critical (DO-178C, ISO 26262), partitioning
4. ✅ **OSEK/VDX:** Automotive ECUs, AUTOSAR Classic, static config

**Core Concepts:**
1. ✅ **Real-time ≠ Fast:** Predictable, deterministic response
2. ✅ **Priority scheduling:** Higher priority preempts lower
3. ✅ **Priority inversion:** Use priority inheritance/ceiling
4. ✅ **Schedulability:** RMS/DMS analysis, WCET measurement

**IPC Mechanisms:**
1. ✅ **Message queues:** Data + synchronization, safe inter-task communication
2. ✅ **Semaphores:** Signaling, counting resources
3. ✅ **Mutexes:** Mutual exclusion with priority inheritance
4. ✅ **Event flags:** Multiple event notification (AND/OR logic)

**Optimization:**
1. ✅ **Minimize context switches:** Event-driven vs polling
2. ✅ **Tune stack sizes:** 50-70% peak usage
3. ✅ **Short ISRs:** Defer processing to tasks
4. ✅ **Cache awareness:** Align data, prevent false sharing

**Debugging:**
1. ✅ **Stack overflow:** Check stack usage, MPU guards
2. ✅ **Deadlock:** Lock ordering, timeout on acquisition
3. ✅ **RTOS-aware debuggers:** Task view, queue inspection
4. ✅ **Profiling:** CPU usage per task, execution time

**Your Experience (Interview Talking Points):**
- ✅ **MQX:** Kinetis K50 industrial gateway, motor control, CAN/Modbus communication
- ✅ **ThreadX:** Multiple embedded systems projects, demonstrated portability
- ✅ **Integrity:** Avionics fuel controller (DO-178B Level A), partitioned safety architecture
- ✅ **MICORSAR:** Automotive ECU development, OSEK/VDX compliance
- ✅ **Real-world debugging:** Stack overflow detection, priority inversion resolution, performance optimization

═══════════════════════════════════════════════════════════════════════

**RTOS COMPREHENSIVE GUIDE - COMPLETE**

**Total:** 2,700 lines covering MQX, ThreadX, Integrity, OSEK/VDX

**Part 1:** RTOS Fundamentals (700 lines) ✅
**Part 2:** MQX Deep Dive (800 lines) ✅
**Part 3:** ThreadX & Integrity (600 lines) ✅
**Part 4:** Advanced Topics (600 lines) ✅

**References:**

- MQX RTOS User Guide (NXP)
- ThreadX User Guide (Microsoft)
- Green Hills Integrity RTOS Documentation
- OSEK/VDX Operating System Specification 2.2.3
- "Real-Time Systems" by Jane W. S. Liu
- "Real-Time Concepts for Embedded Systems" by Qing Li, Caroline Yao

**Last Updated:** January 2026

═══════════════════════════════════════════════════════════════════════
