
═══════════════════════════════════════════════════════════════════════
RTOS (REAL-TIME OPERATING SYSTEMS) INTERVIEW PREPARATION
═══════════════════════════════════════════════════════════════════════

**Target Roles:** RTOS Engineer, Real-Time Embedded Developer, Firmware Engineer
**Difficulty:** Intermediate to Advanced
**Preparation Time:** 4-5 hours
**Last Updated:** January 2026

═══════════════════════════════════════════════════════════════════════

⚡ **QUICK REVISION (10-MINUTE READ)**
─────────────────────────────────────────────────────────────────────────

**What is RTOS?**
Real-Time Operating System guarantees task execution within defined time constraints (deadlines).

**Hard vs Soft Real-Time:**

.. code-block:: text

    Hard Real-Time:
    - Missing deadline = system failure
    - Examples: Airbag, ABS, aircraft control
    - Deterministic timing (guaranteed)
    
    Soft Real-Time:
    - Missing deadline = degraded performance
    - Examples: Video streaming, audio playback
    - Best-effort timing

**Popular RTOS:**

| RTOS | Type | License | Certification | Use Case |
|------|------|---------|---------------|----------|
| **FreeRTOS** | Open | MIT | No (DIY) | IoT, general embedded |
| **QNX** | Commercial | Proprietary | ISO 26262, DO-178C | Automotive, avionics |
| **VxWorks** | Commercial | Proprietary | DO-178B/C | Aerospace, defense |
| **Zephyr** | Open | Apache 2.0 | Partial | IoT, Bluetooth |
| **ThreadX** | Open | MIT | IEC 61508 | Industrial, medical |

**RTOS Core Concepts:**

.. code-block:: text

    ┌────────────────────────────────────┐
    │         RTOS Kernel                │
    ├────────────────────────────────────┤
    │ 1. Task Scheduler                  │
    │    - Preemptive priority-based     │
    │    - Round-robin for same priority │
    ├────────────────────────────────────┤
    │ 2. Task Management                 │
    │    - Create, delete, suspend       │
    │    - Task control blocks (TCB)     │
    ├────────────────────────────────────┤
    │ 3. Inter-Task Communication        │
    │    - Queues, semaphores, mutexes   │
    │    - Event flags, mailboxes        │
    ├────────────────────────────────────┤
    │ 4. Memory Management               │
    │    - Static allocation (most RTOS) │
    │    - Dynamic pools                 │
    ├────────────────────────────────────┤
    │ 5. Interrupt Handling              │
    │    - ISR → Task notification       │
    │    - Minimal ISR duration          │
    ├────────────────────────────────────┤
    │ 6. Timer Services                  │
    │    - Software timers               │
    │    - Periodic/one-shot             │
    └────────────────────────────────────┘

**Task States:**

.. code-block:: text

    ┌─────────┐  Create    ┌───────┐
    │  NULL   │───────────→│ Ready │
    └─────────┘            └───────┘
                             ↑   ↓  Scheduler
                             │   ↓  dispatches
                          Block  ┌─────────┐
                             │   │ Running │
                             ↓   └─────────┘
                           ┌─────────┐  Delete
                           │ Blocked │─────────→ NULL
                           └─────────┘

**Priority Inversion Problem:**

.. code-block:: text

    High Priority Task → Blocked (waits for resource)
    Medium Priority Task → Running (preempts low)
    Low Priority Task → Holds resource needed by high
    
    Solution: Priority Inheritance Protocol

═══════════════════════════════════════════════════════════════════════

🎯 **TOP 25 INTERVIEW QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**BEGINNER LEVEL (8 Questions)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q1: What is the difference between RTOS and GPOS (General Purpose OS)?**

**Answer:**

| Aspect | RTOS | GPOS (Linux/Windows) |
|--------|------|----------------------|
| **Scheduling** | Priority-based, deterministic | Time-sharing, fairness |
| **Latency** | < 10 μs (predictable) | 10-100 ms (variable) |
| **Priority** | Task priority fixed | Dynamic priority |
| **Context Switch** | Fast (< 1 μs) | Slower (10-100 μs) |
| **Memory** | Static allocation | Dynamic (heap, malloc) |
| **Footprint** | Small (10-100 KB) | Large (GB) |
| **Determinism** | Guaranteed deadlines | Best-effort |
| **Use Case** | Embedded, safety-critical | Desktop, server |

**Key Difference:** RTOS guarantees **deadline**, GPOS maximizes **throughput**.

*Talking Point:* "In our automotive ECU, we used FreeRTOS for CAN message handling (< 1ms deadline) and ran Linux on a separate core for infotainment (no hard deadline)."

───────────────────────────────────────────────────────────────────────

**Q2: Explain preemptive vs cooperative scheduling**

**Answer:**

**Preemptive Scheduling:**
- Scheduler can interrupt running task
- Higher priority task preempts lower priority
- Most RTOS use this (guaranteed response time)

.. code-block:: c

    // FreeRTOS preemptive example
    void vTaskLowPriority(void *pvParameters) {
        for (;;) {
            // Long-running work
            process_data();  // Can be preempted
            vTaskDelay(10);
        }
    }
    
    void vTaskHighPriority(void *pvParameters) {
        for (;;) {
            // Urgent work (preempts low priority task)
            handle_interrupt_data();
            vTaskDelay(1);
        }
    }

**Cooperative Scheduling:**
- Task runs until it voluntarily yields
- No preemption
- Simpler, but one task can block others

.. code-block:: c

    // Cooperative example (rare in RTOS)
    void task1(void) {
        while (1) {
            do_work();
            task_yield();  // Must explicitly yield
        }
    }
    
    void task2(void) {
        while (1) {
            do_other_work();
            task_yield();  // Otherwise task1 never runs
        }
    }

**Comparison:**

| Aspect | Preemptive | Cooperative |
|--------|------------|-------------|
| **Response Time** | Guaranteed (high priority) | Unpredictable |
| **Complexity** | Higher (race conditions) | Lower (no preemption) |
| **Fairness** | Priority-based | Depends on yield discipline |
| **Use Case** | Real-time systems | Simple embedded |

───────────────────────────────────────────────────────────────────────

**Q3: What is a task and how do you create one in FreeRTOS?**

**Answer:**

**Task** = Independent thread of execution with its own stack and priority.

**FreeRTOS Task Creation:**

.. code-block:: c

    #include "FreeRTOS.h"
    #include "task.h"
    
    // Task function
    void vTaskFunction(void *pvParameters) {
        // Task initialization
        int *param = (int *)pvParameters;
        
        // Task loop (never return)
        for (;;) {
            // Do work
            printf("Task running with param: %d\n", *param);
            
            // Delay (unblock other tasks)
            vTaskDelay(pdMS_TO_TICKS(1000));  // 1 second
        }
    }
    
    int main(void) {
        int task_param = 42;
        TaskHandle_t xHandle = NULL;
        
        // Create task
        BaseType_t result = xTaskCreate(
            vTaskFunction,          // Task function
            "MyTask",               // Task name (debug)
            1000,                   // Stack size (words)
            (void *)&task_param,    // Parameters
            2,                      // Priority (0=lowest)
            &xHandle                // Task handle
        );
        
        if (result != pdPASS) {
            printf("Task creation failed\n");
            return -1;
        }
        
        // Start scheduler (never returns)
        vTaskStartScheduler();
        
        // Should never reach here
        return 0;
    }

**Task Control:**

.. code-block:: c

    // Suspend task
    vTaskSuspend(xHandle);
    
    // Resume task
    vTaskResume(xHandle);
    
    // Delete task
    vTaskDelete(xHandle);
    
    // Get task priority
    UBaseType_t priority = uxTaskPriorityGet(xHandle);
    
    // Change task priority
    vTaskPrioritySet(xHandle, 5);

**Task Stack:**
- Each task has its own stack (specified in xTaskCreate)
- Stack overflow = common bug (use `configCHECK_FOR_STACK_OVERFLOW`)

.. code-block:: c

    // Enable stack overflow detection
    #define configCHECK_FOR_STACK_OVERFLOW 2
    
    // Overflow callback
    void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
        printf("Stack overflow in task: %s\n", pcTaskName);
        // Handle error (log, reset, etc.)
    }

───────────────────────────────────────────────────────────────────────

**Q4: Explain semaphores, mutexes, and their differences**

**Answer:**

**Semaphore** = Signaling mechanism (count-based)

**Types:**

1. **Binary Semaphore** (count 0 or 1)
   - Used for signaling (ISR → Task)
   - No ownership

2. **Counting Semaphore** (count 0 to N)
   - Resource counting (e.g., buffer slots)

3. **Mutex** (Mutual Exclusion)
   - Special binary semaphore
   - Has ownership (only owner can unlock)
   - Supports priority inheritance

**Comparison:**

| Feature | Binary Semaphore | Mutex |
|---------|------------------|-------|
| **Purpose** | Signaling | Mutual exclusion |
| **Ownership** | No | Yes (owner task) |
| **Priority Inheritance** | No | Yes |
| **Recursive** | No | Yes (recursive mutex) |
| **ISR-safe** | Yes (give only) | No |

**Binary Semaphore Example (ISR → Task):**

.. code-block:: c

    #include "semphr.h"
    
    SemaphoreHandle_t xSemaphore;
    
    // ISR (hardware interrupt)
    void UART_IRQHandler(void) {
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        
        // Signal task that data is ready
        xSemaphoreGiveFromISR(xSemaphore, &xHigherPriorityTaskWoken);
        
        // Request context switch if needed
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
    
    // Task waits for data
    void vUARTTask(void *pvParameters) {
        for (;;) {
            // Block until ISR signals
            if (xSemaphoreTake(xSemaphore, portMAX_DELAY) == pdTRUE) {
                // Data ready, process it
                process_uart_data();
            }
        }
    }
    
    int main(void) {
        // Create binary semaphore
        xSemaphore = xSemaphoreCreateBinary();
        
        xTaskCreate(vUARTTask, "UART", 1000, NULL, 3, NULL);
        vTaskStartScheduler();
        return 0;
    }

**Mutex Example (Protecting Shared Resource):**

.. code-block:: c

    SemaphoreHandle_t xMutex;
    
    void vTask1(void *pvParameters) {
        for (;;) {
            // Lock mutex
            if (xSemaphoreTake(xMutex, portMAX_DELAY) == pdTRUE) {
                // Critical section (exclusive access)
                shared_variable++;
                printf("Task1: %d\n", shared_variable);
                
                // Unlock mutex
                xSemaphoreGive(xMutex);
            }
            vTaskDelay(10);
        }
    }
    
    void vTask2(void *pvParameters) {
        for (;;) {
            if (xSemaphoreTake(xMutex, portMAX_DELAY) == pdTRUE) {
                shared_variable += 10;
                printf("Task2: %d\n", shared_variable);
                xSemaphoreGive(xMutex);
            }
            vTaskDelay(20);
        }
    }
    
    int main(void) {
        // Create mutex
        xMutex = xSemaphoreCreateMutex();
        
        xTaskCreate(vTask1, "Task1", 1000, NULL, 2, NULL);
        xTaskCreate(vTask2, "Task2", 1000, NULL, 2, NULL);
        vTaskStartScheduler();
        return 0;
    }

**Counting Semaphore Example (Buffer Management):**

.. code-block:: c

    #define BUFFER_SIZE 10
    SemaphoreHandle_t xBufferSemaphore;
    
    int main(void) {
        // Create counting semaphore (initial count = 10)
        xBufferSemaphore = xSemaphoreCreateCounting(BUFFER_SIZE, BUFFER_SIZE);
        
        // Producer task
        xTaskCreate(vProducerTask, "Producer", 1000, NULL, 2, NULL);
        
        // Consumer task
        xTaskCreate(vConsumerTask, "Consumer", 1000, NULL, 2, NULL);
        
        vTaskStartScheduler();
        return 0;
    }
    
    void vProducerTask(void *pvParameters) {
        for (;;) {
            // Wait for free buffer slot
            if (xSemaphoreTake(xBufferSemaphore, portMAX_DELAY) == pdTRUE) {
                // Produce data
                add_to_buffer(data);
            }
        }
    }
    
    void vConsumerTask(void *pvParameters) {
        for (;;) {
            // Consume data
            process_buffer(data);
            
            // Release buffer slot
            xSemaphoreGive(xBufferSemaphore);
            vTaskDelay(50);
        }
    }

───────────────────────────────────────────────────────────────────────

**Q5: What is priority inversion and how do you prevent it?**

**Answer:**

**Priority Inversion** occurs when a high-priority task is blocked by a low-priority task holding a shared resource, and a medium-priority task preempts the low-priority task.

**Example Scenario:**

.. code-block:: text

    Time →
    
    1. Low priority task (L) locks Mutex
    2. High priority task (H) tries to lock Mutex → BLOCKED
    3. Medium priority task (M) preempts L
    4. M runs (not waiting for Mutex)
    5. L cannot run (preempted by M)
    6. H waits indefinitely!
    
    Result: High priority task blocked by medium priority task!

**Classic Example: Mars Pathfinder (1997)**
- Information bus watchdog reset due to priority inversion
- High-priority task blocked for extended period
- Fixed by enabling priority inheritance

**Solutions:**

**1. Priority Inheritance Protocol (PIP):**

.. code-block:: c

    // FreeRTOS mutex automatically uses priority inheritance
    SemaphoreHandle_t xMutex = xSemaphoreCreateMutex();
    
    // How it works:
    // 1. Low priority task (L) locks mutex
    // 2. High priority task (H) tries to lock → blocked
    // 3. L's priority temporarily boosted to H's priority
    // 4. L finishes quickly (no preemption by medium)
    // 5. L unlocks mutex, priority restored
    // 6. H runs

**2. Priority Ceiling Protocol (PCP):**

.. code-block:: c

    // When task locks mutex, priority raised to highest priority
    // of any task that might use that mutex
    
    // Example:
    // Mutex used by tasks with priority 3, 5, 7
    // Any task locking mutex → priority = 7
    // No lower priority task can preempt

**3. Disabling Preemption (Not Recommended):**

.. code-block:: c

    // Disable task switching (crude solution)
    vTaskSuspendAll();
    
    // Critical section
    shared_resource++;
    
    // Re-enable task switching
    xTaskResumeAll();

**Real-World Code:**

.. code-block:: c

    // Task priorities
    #define PRIORITY_HIGH   5
    #define PRIORITY_MEDIUM 3
    #define PRIORITY_LOW    1
    
    SemaphoreHandle_t xMutex;
    int shared_data = 0;
    
    void vLowPriorityTask(void *pvParameters) {
        for (;;) {
            xSemaphoreTake(xMutex, portMAX_DELAY);
            // Long critical section
            for (int i = 0; i < 1000000; i++) {
                shared_data++;
            }
            xSemaphoreGive(xMutex);
            vTaskDelay(100);
        }
    }
    
    void vMediumPriorityTask(void *pvParameters) {
        for (;;) {
            // CPU-intensive work (doesn't use mutex)
            compute_heavy_task();
            vTaskDelay(10);
        }
    }
    
    void vHighPriorityTask(void *pvParameters) {
        for (;;) {
            // Needs shared_data urgently
            xSemaphoreTake(xMutex, portMAX_DELAY);
            printf("High priority: %d\n", shared_data);
            xSemaphoreGive(xMutex);
            vTaskDelay(50);
        }
    }
    
    int main(void) {
        // Mutex with priority inheritance (solves inversion)
        xMutex = xSemaphoreCreateMutex();
        
        xTaskCreate(vLowPriorityTask, "Low", 1000, NULL, PRIORITY_LOW, NULL);
        xTaskCreate(vMediumPriorityTask, "Med", 1000, NULL, PRIORITY_MEDIUM, NULL);
        xTaskCreate(vHighPriorityTask, "High", 1000, NULL, PRIORITY_HIGH, NULL);
        
        vTaskStartScheduler();
        return 0;
    }

*Talking Point:* "In our motor control system, we had priority inversion between the high-priority PWM task and low-priority logging task. Using FreeRTOS mutex with priority inheritance solved the issue, reducing PWM jitter from 500 μs to < 10 μs."

───────────────────────────────────────────────────────────────────────

**Q6: Explain queues in RTOS and their usage**

**Answer:**

**Queue** = FIFO data structure for inter-task communication.

**FreeRTOS Queue:**

.. code-block:: c

    #include "queue.h"
    
    // Queue handle
    QueueHandle_t xQueue;
    
    // Data structure
    typedef struct {
        int sensor_id;
        float value;
        uint32_t timestamp;
    } sensor_data_t;
    
    // Create queue
    #define QUEUE_LENGTH 10
    xQueue = xQueueCreate(QUEUE_LENGTH, sizeof(sensor_data_t));
    
    // Producer task (sends data)
    void vSensorTask(void *pvParameters) {
        sensor_data_t data;
        
        for (;;) {
            // Read sensor
            data.sensor_id = 1;
            data.value = read_adc();
            data.timestamp = xTaskGetTickCount();
            
            // Send to queue (block if full)
            if (xQueueSend(xQueue, &data, pdMS_TO_TICKS(100)) != pdTRUE) {
                printf("Queue full!\n");
            }
            
            vTaskDelay(pdMS_TO_TICKS(50));  // 50ms sampling
        }
    }
    
    // Consumer task (receives data)
    void vProcessTask(void *pvParameters) {
        sensor_data_t data;
        
        for (;;) {
            // Receive from queue (block if empty)
            if (xQueueReceive(xQueue, &data, portMAX_DELAY) == pdTRUE) {
                // Process data
                printf("Sensor %d: %.2f at %u\n", 
                       data.sensor_id, data.value, data.timestamp);
                process_sensor_data(&data);
            }
        }
    }

**Queue Operations:**

.. code-block:: c

    // Send to back of queue
    xQueueSend(xQueue, &data, timeout);
    
    // Send to front (urgent)
    xQueueSendToFront(xQueue, &data, timeout);
    
    // Receive from queue
    xQueueReceive(xQueue, &buffer, timeout);
    
    // Peek (don't remove)
    xQueuePeek(xQueue, &buffer, timeout);
    
    // Check queue status
    UBaseType_t count = uxQueueMessagesWaiting(xQueue);
    UBaseType_t free = uxQueueSpacesAvailable(xQueue);
    
    // Reset queue
    xQueueReset(xQueue);

**ISR-safe Queue Operations:**

.. code-block:: c

    // ISR sends to queue
    void UART_IRQHandler(void) {
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        uint8_t data = UART_ReadByte();
        
        // Send from ISR
        xQueueSendFromISR(xQueue, &data, &xHigherPriorityTaskWoken);
        
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }

**Producer-Consumer Pattern:**

.. code-block:: text

    ┌──────────────┐        ┌───────┐        ┌──────────────┐
    │   Producer   │──data──→│ Queue │──data──→│   Consumer   │
    │   (Sensor)   │        │ (FIFO)│        │  (Process)   │
    └──────────────┘        └───────┘        └──────────────┘
         50ms                10 items             20ms

**Queue vs Direct Function Call:**

| Aspect | Queue | Direct Call |
|--------|-------|-------------|
| **Coupling** | Loose (async) | Tight (sync) |
| **Blocking** | Producer doesn't wait | Producer waits |
| **Priority** | Consumer runs at its priority | Runs at producer priority |
| **Buffering** | Yes (N items) | No |

───────────────────────────────────────────────────────────────────────

**Q7: How do you handle interrupts in RTOS?**

**Answer:**

**Best Practice:** Keep ISR short, defer work to task.

**ISR → Task Communication:**

.. code-block:: c

    // Method 1: Binary Semaphore (simple signaling)
    SemaphoreHandle_t xSemaphore;
    
    void GPIO_IRQHandler(void) {
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        
        // Clear interrupt flag
        clear_gpio_interrupt();
        
        // Signal task
        xSemaphoreGiveFromISR(xSemaphore, &xHigherPriorityTaskWoken);
        
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
    
    void vButtonTask(void *pvParameters) {
        for (;;) {
            // Wait for button press
            xSemaphoreTake(xSemaphore, portMAX_DELAY);
            
            // Process button (heavy work)
            handle_button_press();
        }
    }

**Method 2: Task Notifications (Efficient):**

.. code-block:: c

    TaskHandle_t xHandlerTask;
    
    void UART_IRQHandler(void) {
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        
        // Read data
        uint32_t data = UART_ReadRegister();
        
        // Notify task (faster than semaphore)
        vTaskNotifyGiveIndexedFromISR(xHandlerTask, 0, &xHigherPriorityTaskWoken);
        
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
    
    void vUARTHandlerTask(void *pvParameters) {
        for (;;) {
            // Wait for notification
            ulTaskNotifyTakeIndexed(0, pdTRUE, portMAX_DELAY);
            
            // Process UART data
            process_uart_data();
        }
    }

**Method 3: Queue (Pass Data):**

.. code-block:: c

    QueueHandle_t xQueue;
    
    void ADC_IRQHandler(void) {
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        
        // Read ADC value
        uint16_t adc_value = ADC_ReadValue();
        
        // Send to queue
        xQueueSendFromISR(xQueue, &adc_value, &xHigherPriorityTaskWoken);
        
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
    
    void vADCTask(void *pvParameters) {
        uint16_t value;
        
        for (;;) {
            if (xQueueReceive(xQueue, &value, portMAX_DELAY) == pdTRUE) {
                // Process ADC value
                float voltage = (value / 4095.0) * 3.3;
                printf("Voltage: %.2fV\n", voltage);
            }
        }
    }

**Interrupt Priority:**

.. code-block:: c

    // FreeRTOS config
    #define configMAX_SYSCALL_INTERRUPT_PRIORITY 5
    
    // Interrupt priorities (lower number = higher priority)
    // Priority 0-4: Cannot call FreeRTOS API (too high)
    // Priority 5-15: Can call FreeRTOS FromISR functions
    
    // Set interrupt priority (ARM Cortex-M)
    NVIC_SetPriority(UART_IRQn, 6);  // Can use FreeRTOS API
    NVIC_SetPriority(TIMER_IRQn, 3); // Cannot use FreeRTOS API (time-critical)

**Critical Sections:**

.. code-block:: c

    // Disable interrupts (short duration only!)
    taskENTER_CRITICAL();
    
    shared_variable++;  // Atomic operation
    
    taskEXIT_CRITICAL();
    
    // ISR version
    UBaseType_t uxSavedInterruptStatus;
    uxSavedInterruptStatus = taskENTER_CRITICAL_FROM_ISR();
    
    // Critical code
    
    taskEXIT_CRITICAL_FROM_ISR(uxSavedInterruptStatus);

───────────────────────────────────────────────────────────────────────

**Q8: Explain timer services in RTOS**

**Answer:**

**Software Timers** run in the context of the timer daemon task.

**FreeRTOS Timers:**

.. code-block:: c

    #include "timers.h"
    
    // Timer handle
    TimerHandle_t xTimer;
    
    // Timer callback function
    void vTimerCallback(TimerHandle_t xTimer) {
        // Timer expired
        printf("Timer triggered\n");
        
        // Do work (keep short, runs in timer task context)
        toggle_led();
    }
    
    int main(void) {
        // Create one-shot timer (1000ms)
        xTimer = xTimerCreate(
            "OneShot",              // Name
            pdMS_TO_TICKS(1000),    // Period (1 second)
            pdFALSE,                // Auto-reload (pdFALSE = one-shot)
            (void *)0,              // Timer ID
            vTimerCallback          // Callback function
        );
        
        // Start timer
        xTimerStart(xTimer, 0);
        
        // Create periodic timer (500ms)
        TimerHandle_t xPeriodicTimer = xTimerCreate(
            "Periodic",
            pdMS_TO_TICKS(500),
            pdTRUE,                 // Auto-reload (pdTRUE = periodic)
            (void *)1,
            vTimerCallback
        );
        
        xTimerStart(xPeriodicTimer, 0);
        
        vTaskStartScheduler();
        return 0;
    }

**Timer Control:**

.. code-block:: c

    // Start timer
    xTimerStart(xTimer, 0);
    
    // Stop timer
    xTimerStop(xTimer, 0);
    
    // Reset timer (restart from 0)
    xTimerReset(xTimer, 0);
    
    // Change period
    xTimerChangePeriod(xTimer, pdMS_TO_TICKS(2000), 0);
    
    // Check if timer is active
    BaseType_t active = xTimerIsTimerActive(xTimer);

**Real-World Example: Watchdog**

.. code-block:: c

    #define WATCHDOG_TIMEOUT_MS 5000
    TimerHandle_t xWatchdogTimer;
    
    void vWatchdogCallback(TimerHandle_t xTimer) {
        // Watchdog expired → system hang detected
        printf("ERROR: Watchdog timeout! Resetting system...\n");
        system_reset();
    }
    
    void vCriticalTask(void *pvParameters) {
        for (;;) {
            // Do critical work
            process_data();
            
            // Pet the watchdog (reset timer)
            xTimerReset(xWatchdogTimer, 0);
            
            vTaskDelay(pdMS_TO_TICKS(1000));
        }
    }
    
    int main(void) {
        // Create watchdog timer
        xWatchdogTimer = xTimerCreate(
            "Watchdog",
            pdMS_TO_TICKS(WATCHDOG_TIMEOUT_MS),
            pdFALSE,  // One-shot (reset manually)
            NULL,
            vWatchdogCallback
        );
        
        xTimerStart(xWatchdogTimer, 0);
        xTaskCreate(vCriticalTask, "Critical", 1000, NULL, 3, NULL);
        vTaskStartScheduler();
        return 0;
    }

═══════════════════════════════════════════════════════════════════════

**INTERMEDIATE LEVEL (10 Questions)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q9: How do you measure task execution time and CPU utilization?**

**Answer:**

**Method 1: FreeRTOS Runtime Stats:**

.. code-block:: c

    // Enable in FreeRTOSConfig.h
    #define configGENERATE_RUN_TIME_STATS 1
    #define configUSE_TRACE_FACILITY 1
    #define configUSE_STATS_FORMATTING_FUNCTIONS 1
    
    // Provide high-resolution timer
    #define portCONFIGURE_TIMER_FOR_RUN_TIME_STATS() configure_timer()
    #define portGET_RUN_TIME_COUNTER_VALUE() read_timer()
    
    // Get task stats
    void print_task_stats(void) {
        char buffer[1024];
        vTaskGetRunTimeStats(buffer);
        printf("Task Statistics:\n%s\n", buffer);
    }
    
    // Output example:
    // Task          Abs Time      % Time
    // ────────────────────────────────────
    // IDLE          12500         25%
    // SensorTask    30000         60%
    // ControlTask   7500          15%

**Method 2: Task-Level Profiling:**

.. code-block:: c

    // Measure task execution time
    void vSensorTask(void *pvParameters) {
        TickType_t xStartTime, xEndTime, xExecutionTime;
        
        for (;;) {
            xStartTime = xTaskGetTickCount();
            
            // Do work
            process_sensor_data();
            
            xEndTime = xTaskGetTickCount();
            xExecutionTime = xEndTime - xStartTime;
            
            printf("Task execution time: %u ms\n", xExecutionTime);
            
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

**Method 3: CPU Utilization:**

.. code-block:: c

    // Measure CPU idle time
    uint32_t idle_count = 0;
    
    void vIdleHook(void) {
        idle_count++;
    }
    
    void vMonitorTask(void *pvParameters) {
        uint32_t last_idle = 0;
        
        for (;;) {
            vTaskDelay(pdMS_TO_TICKS(1000));  // 1 second
            
            uint32_t idle_diff = idle_count - last_idle;
            last_idle = idle_count;
            
            // Calculate CPU utilization
            float cpu_util = 100.0 - (idle_diff / 10000.0 * 100.0);
            printf("CPU Utilization: %.2f%%\n", cpu_util);
        }
    }

**Method 4: GPIO Toggle (Oscilloscope):**

.. code-block:: c

    void vCriticalTask(void *pvParameters) {
        for (;;) {
            GPIO_SET(DEBUG_PIN);   // Set pin high
            
            // Critical work
            control_motor();
            
            GPIO_CLEAR(DEBUG_PIN); // Set pin low
            
            vTaskDelay(10);
        }
    }
    
    // Measure pulse width on oscilloscope
    // Pulse width = task execution time

═══════════════════════════════════════════════════════════════════════

📝 **RESUME TALKING POINTS**
─────────────────────────────────────────────────────────────────────────

**When asked: "Tell me about your RTOS experience"**

**1. Task Design**
- "Designed multi-task architecture with 8 tasks (priorities 1-7) for motor control system"
- "Used FreeRTOS preemptive scheduler with < 1 μs context switch time"
- "Implemented priority inheritance mutexes to prevent priority inversion"

**2. IPC Mechanisms**
- "Used queues for sensor data buffering (10-item FIFO, 50ms producer, 20ms consumer)"
- "Implemented binary semaphores for ISR-to-task signaling (< 10 μs latency)"
- "Designed mutex-protected SPI bus access for multi-sensor communication"

**3. Real-Time Performance**
- "Achieved < 1ms deterministic response time for CAN message handling"
- "Optimized task execution: reduced motor control loop from 500 μs to 100 μs"
- "Maintained < 60% CPU utilization under peak load"

**4. Safety & Reliability**
- "Implemented software watchdog (5-second timeout) to detect task hangs"
- "Used stack overflow detection (caught 3 bugs during development)"
- "Designed fail-safe mechanism for sensor failures (graceful degradation)"

**Quantifiable Results:**
- < 1 ms response time
- < 60% CPU utilization
- < 10 μs ISR-to-task latency
- Zero missed deadlines in 1M+ test cycles

═══════════════════════════════════════════════════════════════════════

**Last Updated:** January 2026
**Good Luck with Your Interview! 🚀**

═══════════════════════════════════════════════════════════════════════
