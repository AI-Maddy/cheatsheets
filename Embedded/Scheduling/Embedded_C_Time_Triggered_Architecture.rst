================================================================================
Time-Triggered Architecture for Embedded C
================================================================================

**TL;DR**: Time-triggered cooperative scheduler architecture for embedded systems 
using tick-based scheduling with predictable timing and deterministic behavior. 
Based on Michael Pont's PTTC (Pattern Time-Triggered Cooperative) scheduler.

**Related Cheatsheets**: 
:doc:`Embedded C </Languages/Embedded C>`, 
:doc:`RTOS Concepts </RTOS/RTOS_Concepts>`, 
:doc:`Embedded System Architecture </Embedded/Embedded_System_Architecture_Patterns>`,
:doc:`Embedded Design Patterns </Embedded/Embedded_Design_Patterns_Behavioral>`

================================================================================
1. Time-Triggered Architecture Fundamentals
================================================================================

1.1 Core Principles
--------------------------------------------------------------------------------

**Key Concepts**:

- **Predictability**: All tasks execute at predetermined intervals
- **Deterministic**: System behavior is repeatable and analyzable
- **Cooperative**: Tasks voluntarily yield control (no preemption)
- **Tick-based**: Hardware timer generates periodic interrupts (ticks)

**Advantages**:

- Low overhead compared to preemptive RTOS
- Predictable timing behavior
- Easier to test and verify
- Suitable for low-power applications
- Good for hard real-time constraints

**Limitations**:

- Tasks must be well-behaved (short execution time)
- No task can block or delay
- Less flexible than preemptive scheduling
- Requires careful timing analysis

1.2 System Architecture
--------------------------------------------------------------------------------

**Typical Structure**:

.. code-block:: text

    ┌─────────────────────────────────────┐
    │       Hardware Timer (SysTick)      │
    │  Generates periodic tick interrupts │
    └──────────────┬──────────────────────┘
                   │ Tick ISR
                   ▼
    ┌─────────────────────────────────────┐
    │       Scheduler Update ISR          │
    │   Updates task ready flags/counters │
    └──────────────┬──────────────────────┘
                   │ Return from ISR
                   ▼
    ┌─────────────────────────────────────┐
    │         Main Scheduler Loop         │
    │  Dispatches ready tasks in order    │
    └──────────────┬──────────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
    ┌─────────┐         ┌─────────┐
    │ Task 1  │   ...   │ Task N  │
    │ (run)   │         │ (run)   │
    └─────────┘         └─────────┘

================================================================================
2. Basic Time-Triggered Scheduler Implementation
================================================================================

2.1 Scheduler Data Structures
--------------------------------------------------------------------------------

**Task Control Block**:

.. code-block:: c

    #include <stdint.h>
    #include <stdbool.h>
    
    #define MAX_TASKS 10
    
    /* Task function pointer type */
    typedef void (*task_fn_t)(void);
    
    /* Task control block */
    typedef struct {
        task_fn_t task;           /* Pointer to task function */
        uint32_t period;          /* Task period in ticks */
        uint32_t delay;           /* Initial delay before first run */
        uint32_t counter;         /* Countdown counter */
        bool run_me;              /* Flag: task ready to run */
        bool enabled;             /* Task enabled/disabled */
    } task_t;
    
    /* Scheduler state */
    typedef struct {
        task_t tasks[MAX_TASKS];  /* Task array */
        uint8_t num_tasks;        /* Number of registered tasks */
        uint32_t tick_count;      /* Total ticks since start */
        uint32_t tick_ms;         /* Tick period in milliseconds */
    } scheduler_t;
    
    /* Global scheduler instance */
    static scheduler_t g_scheduler = {0};

2.2 Scheduler Initialization
--------------------------------------------------------------------------------

**Setup Function**:

.. code-block:: c

    #include <string.h>
    
    /**
     * Initialize the scheduler
     * @param tick_period_ms Tick period in milliseconds (e.g., 1ms)
     */
    void scheduler_init(uint32_t tick_period_ms) {
        memset(&g_scheduler, 0, sizeof(scheduler_t));
        g_scheduler.tick_ms = tick_period_ms;
        g_scheduler.num_tasks = 0;
    }
    
    /**
     * Add a task to the scheduler
     * @param task Task function pointer
     * @param period Task period in ticks
     * @param delay Initial delay before first run (0 for immediate)
     * @return Task index, or -1 on error
     */
    int scheduler_add_task(task_fn_t task, uint32_t period, uint32_t delay) {
        if (g_scheduler.num_tasks >= MAX_TASKS) {
            return -1;  /* Scheduler full */
        }
        
        if (task == NULL || period == 0) {
            return -1;  /* Invalid parameters */
        }
        
        uint8_t index = g_scheduler.num_tasks;
        g_scheduler.tasks[index].task = task;
        g_scheduler.tasks[index].period = period;
        g_scheduler.tasks[index].delay = delay;
        g_scheduler.tasks[index].counter = delay;
        g_scheduler.tasks[index].run_me = false;
        g_scheduler.tasks[index].enabled = true;
        
        g_scheduler.num_tasks++;
        return index;
    }

2.3 Tick ISR (Timer Interrupt Handler)
--------------------------------------------------------------------------------

**Update Task Counters**:

.. code-block:: c

    /**
     * Scheduler tick ISR - called from timer interrupt
     * This function MUST be called at regular intervals
     */
    void scheduler_tick_isr(void) {
        g_scheduler.tick_count++;
        
        /* Update all task counters */
        for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
            task_t *t = &g_scheduler.tasks[i];
            
            if (!t->enabled) {
                continue;  /* Skip disabled tasks */
            }
            
            if (t->counter > 0) {
                t->counter--;
            }
            
            if (t->counter == 0) {
                /* Task is ready to run */
                t->run_me = true;
                t->counter = t->period;  /* Reload for next period */
            }
        }
    }

**Hardware Timer Setup (ARM Cortex-M SysTick)**:

.. code-block:: c

    #include "stm32f4xx.h"  /* Or appropriate device header */
    
    /**
     * Configure SysTick timer for 1ms ticks
     * Assumes 168 MHz system clock (adjust for your MCU)
     */
    void systick_init(void) {
        uint32_t ticks = SystemCoreClock / 1000;  /* 1ms period */
        
        SysTick->LOAD = ticks - 1;
        SysTick->VAL = 0;
        SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk |  /* Use CPU clock */
                        SysTick_CTRL_TICKINT_Msk |    /* Enable interrupt */
                        SysTick_CTRL_ENABLE_Msk;      /* Enable SysTick */
    }
    
    /**
     * SysTick interrupt handler
     */
    void SysTick_Handler(void) {
        scheduler_tick_isr();
    }

2.4 Main Dispatcher Loop
--------------------------------------------------------------------------------

**Cooperative Task Dispatch**:

.. code-block:: c

    /**
     * Main scheduler dispatch loop
     * Call this continuously in main()
     */
    void scheduler_dispatch(void) {
        /* Dispatch all ready tasks */
        for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
            task_t *t = &g_scheduler.tasks[i];
            
            if (t->run_me && t->enabled) {
                t->run_me = false;  /* Clear flag BEFORE running task */
                t->task();          /* Execute task */
                
                /* Task must return quickly! */
            }
        }
    }
    
    /**
     * Start the scheduler (never returns)
     */
    void scheduler_start(void) {
        systick_init();
        
        /* Main loop */
        while (1) {
            scheduler_dispatch();
            
            /* Optional: Enter low-power mode until next interrupt */
            // __WFI();  /* Wait For Interrupt */
        }
    }

================================================================================
3. Example Application
================================================================================

3.1 Simple Multi-Task System
--------------------------------------------------------------------------------

**Task Definitions**:

.. code-block:: c

    #include <stdio.h>
    
    /* Task 1: Blink LED at 1 Hz (500ms on, 500ms off) */
    void task_led_blink(void) {
        static bool led_state = false;
        
        led_state = !led_state;
        GPIO_WritePin(LED_GPIO, LED_PIN, led_state);
        
        printf("LED: %s\n", led_state ? "ON" : "OFF");
    }
    
    /* Task 2: Read button every 50ms */
    void task_button_read(void) {
        static uint8_t button_count = 0;
        
        bool button = GPIO_ReadPin(BUTTON_GPIO, BUTTON_PIN);
        
        if (button) {
            button_count++;
            if (button_count > 3) {  /* Debounce: 3 consecutive reads */
                printf("Button pressed!\n");
                button_count = 0;
            }
        } else {
            button_count = 0;
        }
    }
    
    /* Task 3: Send telemetry every 1 second */
    void task_telemetry(void) {
        static uint32_t counter = 0;
        
        printf("Telemetry #%lu: Uptime=%lu ms\n", 
               counter++, 
               g_scheduler.tick_count * g_scheduler.tick_ms);
    }
    
    /* Task 4: ADC sampling at 100 Hz */
    void task_adc_sample(void) {
        static uint16_t samples[10];
        static uint8_t index = 0;
        
        samples[index] = ADC_Read();
        index = (index + 1) % 10;
        
        /* Could compute average, detect threshold, etc. */
    }

**Main Function**:

.. code-block:: c

    int main(void) {
        /* Hardware initialization */
        system_init();
        GPIO_Init();
        ADC_Init();
        
        /* Initialize scheduler with 1ms ticks */
        scheduler_init(1);
        
        /* Add tasks with different periods */
        scheduler_add_task(task_led_blink,   500,  0);    /* 500ms period, no delay */
        scheduler_add_task(task_button_read,  50,  0);    /* 50ms period */
        scheduler_add_task(task_telemetry,  1000, 100);   /* 1s period, 100ms delay */
        scheduler_add_task(task_adc_sample,   10,  0);    /* 10ms period (100 Hz) */
        
        /* Start scheduler (never returns) */
        scheduler_start();
        
        return 0;  /* Never reached */
    }

================================================================================
4. Advanced Scheduler Features
================================================================================

4.1 Task Management Functions
--------------------------------------------------------------------------------

**Enable/Disable Tasks**:

.. code-block:: c

    /**
     * Enable a task
     */
    void scheduler_enable_task(uint8_t task_id) {
        if (task_id < g_scheduler.num_tasks) {
            g_scheduler.tasks[task_id].enabled = true;
        }
    }
    
    /**
     * Disable a task
     */
    void scheduler_disable_task(uint8_t task_id) {
        if (task_id < g_scheduler.num_tasks) {
            g_scheduler.tasks[task_id].enabled = false;
            g_scheduler.tasks[task_id].run_me = false;
        }
    }
    
    /**
     * Remove a task from the scheduler
     */
    void scheduler_remove_task(uint8_t task_id) {
        if (task_id >= g_scheduler.num_tasks) {
            return;
        }
        
        /* Shift remaining tasks down */
        for (uint8_t i = task_id; i < g_scheduler.num_tasks - 1; i++) {
            g_scheduler.tasks[i] = g_scheduler.tasks[i + 1];
        }
        
        g_scheduler.num_tasks--;
    }

4.2 One-Shot Tasks
--------------------------------------------------------------------------------

**Single Execution Tasks**:

.. code-block:: c

    /**
     * Add a one-shot task (runs once after delay, then removed)
     */
    int scheduler_add_one_shot_task(task_fn_t task, uint32_t delay) {
        int task_id = scheduler_add_task(task, 0xFFFFFFFF, delay);
        
        if (task_id >= 0) {
            g_scheduler.tasks[task_id].period = 0;  /* Mark as one-shot */
        }
        
        return task_id;
    }
    
    /**
     * Modified dispatcher to handle one-shot tasks
     */
    void scheduler_dispatch_advanced(void) {
        for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
            task_t *t = &g_scheduler.tasks[i];
            
            if (t->run_me && t->enabled) {
                t->run_me = false;
                t->task();
                
                /* Remove one-shot tasks after execution */
                if (t->period == 0) {
                    scheduler_remove_task(i);
                    i--;  /* Adjust index after removal */
                }
            }
        }
    }

4.3 Watchdog Integration
--------------------------------------------------------------------------------

**Heartbeat Pattern**:

.. code-block:: c

    #define WATCHDOG_TIMEOUT_MS 5000
    
    static volatile uint32_t last_heartbeat = 0;
    
    /**
     * Watchdog kick task - must run periodically
     */
    void task_watchdog(void) {
        IWDG_Reload();  /* Kick the hardware watchdog */
        last_heartbeat = g_scheduler.tick_count;
    }
    
    /**
     * Check if watchdog task is running
     * Call from supervisor or monitoring task
     */
    bool watchdog_check(void) {
        uint32_t elapsed = g_scheduler.tick_count - last_heartbeat;
        return (elapsed * g_scheduler.tick_ms) < WATCHDOG_TIMEOUT_MS;
    }
    
    /**
     * Main setup with watchdog
     */
    void main_with_watchdog(void) {
        scheduler_init(1);
        
        /* Add watchdog task at 1s period (timeout is 5s) */
        scheduler_add_task(task_watchdog, 1000, 0);
        
        /* Add other tasks */
        scheduler_add_task(task_led_blink, 500, 0);
        
        scheduler_start();
    }

================================================================================
5. Timing Analysis
================================================================================

5.1 Worst-Case Execution Time (WCET)
--------------------------------------------------------------------------------

**Analysis Methodology**:

.. code-block:: c

    /**
     * Measure task execution time using DWT cycle counter
     */
    #define DWT_CYCCNT  (*(volatile uint32_t *)0xE0001004)
    #define DWT_CONTROL (*(volatile uint32_t *)0xE0001000)
    #define DWT_ENABLE  0x00000001
    
    void dwt_init(void) {
        DWT_CONTROL |= DWT_ENABLE;
        DWT_CYCCNT = 0;
    }
    
    uint32_t task_measure_cycles(task_fn_t task) {
        uint32_t start = DWT_CYCCNT;
        task();
        uint32_t end = DWT_CYCCNT;
        return end - start;
    }
    
    /**
     * Timing analysis during development
     */
    void analyze_task_timing(void) {
        dwt_init();
        
        uint32_t cycles = task_measure_cycles(task_led_blink);
        uint32_t us = cycles / (SystemCoreClock / 1000000);
        
        printf("Task execution time: %lu cycles (%lu us)\n", cycles, us);
    }

**Timing Constraints**:

.. code-block:: c

    /**
     * Rule: Sum of all WCET in one tick period must be < tick period
     * 
     * Example with 1ms tick:
     *   Task A: 100us (runs every tick)
     *   Task B: 200us (runs every 10 ticks)
     *   Task C: 50us  (runs every tick)
     * 
     * Worst case in one tick:
     *   Task A: 100us
     *   Task B: 200us (every 10 ticks)
     *   Task C: 50us
     *   Total: 350us < 1000us ✓ OK
     */
    
    typedef struct {
        const char *name;
        uint32_t wcet_us;       /* Worst-case execution time */
        uint32_t period_ticks;  /* Period in ticks */
    } task_timing_t;
    
    bool validate_timing(task_timing_t *tasks, uint8_t num_tasks, uint32_t tick_us) {
        uint32_t total_wcet = 0;
        
        for (uint8_t i = 0; i < num_tasks; i++) {
            /* Calculate utilization per tick */
            total_wcet += tasks[i].wcet_us / tasks[i].period_ticks;
        }
        
        return total_wcet < tick_us;
    }

5.2 Jitter Analysis
--------------------------------------------------------------------------------

**Measuring Timing Jitter**:

.. code-block:: c

    /**
     * Track task execution jitter
     */
    typedef struct {
        uint32_t min_interval;
        uint32_t max_interval;
        uint32_t last_exec_time;
    } task_stats_t;
    
    static task_stats_t task_stats[MAX_TASKS] = {0};
    
    void task_with_jitter_tracking(uint8_t task_id, task_fn_t task) {
        uint32_t now = g_scheduler.tick_count;
        
        if (task_stats[task_id].last_exec_time > 0) {
            uint32_t interval = now - task_stats[task_id].last_exec_time;
            
            if (interval < task_stats[task_id].min_interval || 
                task_stats[task_id].min_interval == 0) {
                task_stats[task_id].min_interval = interval;
            }
            
            if (interval > task_stats[task_id].max_interval) {
                task_stats[task_id].max_interval = interval;
            }
        }
        
        task_stats[task_id].last_exec_time = now;
        task();
    }
    
    void print_task_jitter(uint8_t task_id, uint32_t expected_period) {
        uint32_t jitter = task_stats[task_id].max_interval - 
                          task_stats[task_id].min_interval;
        
        printf("Task %u: Expected=%lu, Min=%lu, Max=%lu, Jitter=%lu\n",
               task_id, expected_period,
               task_stats[task_id].min_interval,
               task_stats[task_id].max_interval,
               jitter);
    }

================================================================================
6. Low-Power Operation
================================================================================

6.1 Sleep Mode Integration
--------------------------------------------------------------------------------

**Idle Task with Sleep**:

.. code-block:: c

    /**
     * Low-power scheduler dispatch
     */
    void scheduler_dispatch_low_power(void) {
        bool any_task_ready = false;
        
        /* Check if any task is ready */
        for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
            if (g_scheduler.tasks[i].run_me && g_scheduler.tasks[i].enabled) {
                any_task_ready = true;
                break;
            }
        }
        
        if (any_task_ready) {
            /* Dispatch ready tasks */
            for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
                task_t *t = &g_scheduler.tasks[i];
                if (t->run_me && t->enabled) {
                    t->run_me = false;
                    t->task();
                }
            }
        } else {
            /* No tasks ready - enter sleep mode */
            __WFI();  /* Wait for interrupt (SysTick will wake us) */
        }
    }

**Dynamic Tick Adjustment**:

.. code-block:: c

    /**
     * Calculate time until next task execution
     * Used for tickless idle mode
     */
    uint32_t scheduler_get_next_task_time(void) {
        uint32_t min_time = 0xFFFFFFFF;
        
        for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
            task_t *t = &g_scheduler.tasks[i];
            if (t->enabled && t->counter < min_time) {
                min_time = t->counter;
            }
        }
        
        return min_time;
    }

================================================================================
7. Error Handling and Diagnostics
================================================================================

7.1 Scheduler Error Reporting
--------------------------------------------------------------------------------

**Error Codes**:

.. code-block:: c

    typedef enum {
        SCHED_OK = 0,
        SCHED_ERR_FULL,           /* Scheduler task array full */
        SCHED_ERR_INVALID_TASK,   /* Invalid task function */
        SCHED_ERR_INVALID_PERIOD, /* Invalid period (0) */
        SCHED_ERR_TIMING_OVERRUN, /* Task exceeded time budget */
        SCHED_ERR_TICK_MISSED,    /* Missed tick deadline */
    } sched_error_t;
    
    static volatile sched_error_t last_error = SCHED_OK;
    static void (*error_callback)(sched_error_t) = NULL;
    
    void scheduler_set_error_handler(void (*handler)(sched_error_t)) {
        error_callback = handler;
    }
    
    void scheduler_report_error(sched_error_t error) {
        last_error = error;
        if (error_callback) {
            error_callback(error);
        }
    }

7.2 Runtime Monitoring
--------------------------------------------------------------------------------

**Task Overrun Detection**:

.. code-block:: c

    #define TASK_TIMEOUT_TICKS 5  /* Max ticks a task can run */
    
    static volatile uint8_t current_task = 0xFF;
    static volatile uint32_t task_start_tick = 0;
    
    void scheduler_dispatch_monitored(void) {
        for (uint8_t i = 0; i < g_scheduler.num_tasks; i++) {
            task_t *t = &g_scheduler.tasks[i];
            
            if (t->run_me && t->enabled) {
                t->run_me = false;
                
                /* Mark task as running */
                current_task = i;
                task_start_tick = g_scheduler.tick_count;
                
                t->task();
                
                /* Check for overrun */
                uint32_t elapsed = g_scheduler.tick_count - task_start_tick;
                if (elapsed > TASK_TIMEOUT_TICKS) {
                    scheduler_report_error(SCHED_ERR_TIMING_OVERRUN);
                }
                
                current_task = 0xFF;
            }
        }
    }

================================================================================
8. Best Practices
================================================================================

8.1 Task Design Guidelines
--------------------------------------------------------------------------------

**DO**:

- Keep tasks short (< 1ms typical, < tick period always)
- Design tasks to be idempotent (can run multiple times safely)
- Use static variables for task state (not globals)
- Return quickly from tasks
- Disable interrupts only briefly if needed
- Use const for read-only data
- Document worst-case execution time

**DON'T**:

- Never block or delay in tasks
- Don't use infinite loops in tasks
- Avoid dynamic memory allocation in tasks
- Don't disable interrupts for long periods
- Never call scheduler functions from ISRs (except tick ISR)
- Don't share data without protection

8.2 Common Patterns
--------------------------------------------------------------------------------

**State Machine Task**:

.. code-block:: c

    typedef enum {
        STATE_IDLE,
        STATE_ACTIVE,
        STATE_ERROR
    } state_t;
    
    void task_state_machine(void) {
        static state_t state = STATE_IDLE;
        
        switch (state) {
            case STATE_IDLE:
                if (check_trigger()) {
                    state = STATE_ACTIVE;
                }
                break;
                
            case STATE_ACTIVE:
                if (process_data()) {
                    state = STATE_IDLE;
                } else {
                    state = STATE_ERROR;
                }
                break;
                
            case STATE_ERROR:
                handle_error();
                state = STATE_IDLE;
                break;
        }
    }

**Periodic Sampling with Averaging**:

.. code-block:: c

    #define SAMPLE_SIZE 8
    
    void task_sensor_average(void) {
        static uint16_t samples[SAMPLE_SIZE] = {0};
        static uint8_t index = 0;
        static bool buffer_full = false;
        
        /* Read new sample */
        samples[index] = read_sensor();
        index++;
        
        if (index >= SAMPLE_SIZE) {
            index = 0;
            buffer_full = true;
        }
        
        /* Compute average when buffer is full */
        if (buffer_full) {
            uint32_t sum = 0;
            for (uint8_t i = 0; i < SAMPLE_SIZE; i++) {
                sum += samples[i];
            }
            uint16_t average = sum / SAMPLE_SIZE;
            
            process_average(average);
        }
    }

================================================================================
9. Comparison with RTOS
================================================================================

**Time-Triggered vs Preemptive RTOS**:

+------------------------+-------------------------+-------------------------+
| Feature                | Time-Triggered          | Preemptive RTOS         |
+========================+=========================+=========================+
| Scheduling             | Cooperative, tick-based | Preemptive, priority    |
| Overhead               | Very low (~100 bytes)   | High (KB of RAM)        |
| Predictability         | Excellent               | Good (priority issues)  |
| Timing Analysis        | Simple, deterministic   | Complex (priority inv.) |
| Task Blocking          | Not allowed             | Supported               |
| Inter-task Comm        | Shared variables        | Queues, semaphores      |
| Learning Curve         | Low                     | Moderate-High           |
| Resource Usage         | Minimal                 | Significant             |
| Best For               | Simple, predictable     | Complex, dynamic        |
+------------------------+-------------------------+-------------------------+

**When to Use Time-Triggered**:

- Resource-constrained systems (small RAM/Flash)
- Hard real-time requirements with simple tasks
- Predictable, cyclic behavior
- Safety-critical applications (easier verification)
- Low-power applications
- Simple task interactions

**When to Use RTOS**:

- Complex task interactions
- Dynamic task creation/deletion
- Tasks with variable execution times
- Need for blocking operations
- Many concurrent tasks with different priorities
- TCP/IP stacks, file systems, complex protocols

================================================================================
See Also
================================================================================

- :doc:`Embedded C </Languages/Embedded C>`
- :doc:`RTOS Concepts </RTOS/RTOS_Concepts>`
- :doc:`Embedded System Architecture </Embedded/Embedded_System_Architecture_Patterns>`
- :doc:`Embedded Testing </Embedded/Embedded_Testing_Strategies>`
- :doc:`Embedded Optimization </Embedded/Embedded_Optimization_Techniques>`
- :doc:`Linux Real-Time </Linux/Linux Real-Time>`
