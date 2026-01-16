🦀 **Rust for Safety-Critical Systems — Memory Safety Without Garbage Collection**
═══════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for Rust in Automotive, Avionics, Medical, and Industrial Systems**  
**Key Features:** Ownership ✅ | Borrow Checker ✅ | No Data Races ✅ | No Null Pointers ✅  
**Certification:** DO-178C 🛫 | ISO 26262 🚗 | IEC 61508 ⚙️ | IEC 62304 🏥  
**Status 2026:** Emerging (prototypes, non-critical subsystems, toolchain qualification in progress)

═══════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**Why Rust for Safety-Critical?**

.. code-block:: text

   Traditional C/C++ Safety Challenges:
   ❌ Buffer overflows (70% of security vulnerabilities)
   ❌ Use-after-free (dangling pointers)
   ❌ Data races (concurrent access without synchronization)
   ❌ Null pointer dereferences
   
   Rust Solution:
   ✅ Ownership prevents use-after-free (compile-time check)
   ✅ Borrow checker prevents data races (no shared mutable state)
   ✅ No null pointers (Option<T> type forces handling)
   ✅ Bounds checking (array access validated)
   ✅ Type safety (no void pointers, strong typing)

**Memory Safety Guarantee:**

.. code-block:: rust

   // ❌ This won't compile (use-after-free prevented)
   let vec = vec![1, 2, 3];
   let first = &vec[0];
   drop(vec);  // Error: cannot move out of `vec` because it is borrowed
   println!("{}", first);
   
   // ✅ Correct: Either borrow OR move, not both
   let vec = vec![1, 2, 3];
   let first = vec[0];  // Copy the value (i32 is Copy)
   drop(vec);  // OK, vec moved after copying value
   println!("{}", first);  // Output: 1

**Certification Status (2026):**

+----------------+--------------------+----------------------------------------+
| Domain         | Standard           | Rust Status                            |
+================+====================+========================================+
| Automotive     | ISO 26262          | ⚠️ Prototype (Volvo, Ferrocene effort) |
+----------------+--------------------+----------------------------------------+
| Avionics       | DO-178C            | ⚠️ Research (AdaCore, Ferrous Systems) |
+----------------+--------------------+----------------------------------------+
| Railway        | EN 50128           | ⚠️ Early adoption (SIL 0-2 only)       |
+----------------+--------------------+----------------------------------------+
| Industrial     | IEC 61508          | ⚠️ SIL 1-2 (qualified compiler needed) |
+----------------+--------------------+----------------------------------------+
| Medical        | IEC 62304          | ⚠️ Class A/B (Class C requires qual)   |
+----------------+--------------------+----------------------------------------+

**Key Insight:** Rust prevents entire **classes of undefined behavior** at compile time, eliminating ~70% of memory safety bugs that plague C/C++ safety-critical code.

═══════════════════════════════════════════════════════════════════════════════

📖 **1. RUST SAFETY FUNDAMENTALS**
═══════════════════════════════════════════════════════════════════════════════

1.1 Ownership System
--------------------

**Three Rules:**

.. code-block:: text

   1. Each value has ONE owner
   2. When owner goes out of scope, value is dropped (freed)
   3. Ownership can be transferred (moved) or borrowed

**Example: Preventing Use-After-Free**

.. code-block:: rust

   fn main() {
       let sensor_data = String::from("Temperature: 85°C");
       process_data(sensor_data);  // Ownership moved to function
       
       // ❌ Error: value used after move
       // println!("{}", sensor_data);
   }
   
   fn process_data(data: String) {
       println!("Processing: {}", data);
   }  // data dropped here (freed)

**Comparison with C:**

.. code-block:: c

   // C: Manual memory management (error-prone)
   char* sensor_data = malloc(100);
   strcpy(sensor_data, "Temperature: 85C");
   process_data(sensor_data);
   
   // ❌ DANGER: sensor_data might be freed inside process_data()
   // Undefined behavior if accessed here!
   printf("%s\n", sensor_data);  // Use-after-free bug
   
   free(sensor_data);  // Potential double-free

**Rust eliminates this entire class of bugs at compile time.**

────────────────────────────────────────────────────────────────────────────

**1.2 Borrowing and References**
--------------------------------

**Immutable Borrows (Shared References):**

.. code-block:: rust

   fn main() {
       let sensor_value = 42;
       
       // Multiple immutable borrows allowed
       let ref1 = &sensor_value;
       let ref2 = &sensor_value;
       
       println!("ref1: {}, ref2: {}", ref1, ref2);  // OK
   }

**Mutable Borrow (Exclusive Reference):**

.. code-block:: rust

   fn main() {
       let mut sensor_value = 42;
       
       let ref_mut = &mut sensor_value;
       *ref_mut = 85;  // Modify through mutable reference
       
       // ❌ Error: Cannot have multiple mutable borrows
       // let ref_mut2 = &mut sensor_value;
       
       println!("Updated: {}", sensor_value);  // Output: 85
   }

**Preventing Data Races:**

.. code-block:: text

   Rust Rule: At any given time, either:
   - ONE mutable reference (&mut T), OR
   - MULTIPLE immutable references (&T)
   
   But NOT BOTH simultaneously.
   
   This prevents data races at compile time (no synchronization overhead needed).

**Example: Data Race Prevention**

.. code-block:: rust

   use std::thread;
   
   fn main() {
       let mut counter = 0;
       
       // ❌ This won't compile (data race)
       // thread::spawn(|| {
       //     counter += 1;  // Error: cannot borrow `counter` as mutable
       // });
       
       // ✅ Correct: Use atomic or mutex
       use std::sync::Arc;
       use std::sync::Mutex;
       
       let counter = Arc::new(Mutex::new(0));
       let counter_clone = Arc::clone(&counter);
       
       let handle = thread::spawn(move || {
           let mut num = counter_clone.lock().unwrap();
           *num += 1;
       });
       
       handle.join().unwrap();
       println!("Result: {}", *counter.lock().unwrap());  // Output: 1
   }

────────────────────────────────────────────────────────────────────────────

**1.3 No Null Pointers (Option<T>)**
------------------------------------

**C Problem:**

.. code-block:: c

   // C: Null pointer crashes are common
   Sensor* sensor = get_sensor();
   if (sensor == NULL) {  // Easy to forget this check
       return ERROR_NULL_POINTER;
   }
   sensor->read_value();  // Potential crash if NULL

**Rust Solution:**

.. code-block:: rust

   fn get_sensor() -> Option<Sensor> {
       // Returns Some(sensor) or None
       if sensor_available() {
           Some(Sensor::new())
       } else {
           None
       }
   }
   
   fn main() {
       match get_sensor() {
           Some(sensor) => {
               sensor.read_value();  // Safe: sensor definitely exists
           }
           None => {
               println!("Sensor unavailable");
           }
       }
   }

**Forced Error Handling:** Compiler requires matching on `Option<T>`, preventing null pointer dereferences.

────────────────────────────────────────────────────────────────────────────

**1.4 Array Bounds Checking**
-----------------------------

**C Problem:**

.. code-block:: c

   // C: Buffer overflow (undefined behavior)
   int arr[10];
   int value = arr[15];  // ❌ Out of bounds, undefined behavior

**Rust Solution:**

.. code-block:: rust

   fn main() {
       let arr = [0; 10];
       
       // ❌ Panic at runtime (but no undefined behavior)
       // let value = arr[15];  // thread 'main' panicked at 'index out of bounds'
       
       // ✅ Safe access with bounds check
       if let Some(value) = arr.get(15) {
           println!("Value: {}", value);
       } else {
           println!("Index out of bounds");  // Handled gracefully
       }
   }

**Tradeoff:** Runtime bounds checking has minimal overhead (~1 CPU cycle) but prevents catastrophic memory corruption.

═══════════════════════════════════════════════════════════════════════════════

📖 **2. RUST vs C vs ADA vs MISRA C++ COMPARISON**
═══════════════════════════════════════════════════════════════════════════════

2.1 Memory Safety Comparison
-----------------------------

+------------------------+--------+--------+--------+--------------+
| Safety Feature         | C      | Ada    | MISRA  | Rust         |
|                        |        |        | C++    |              |
+========================+========+========+========+==============+
| Prevent buffer overflow| ❌ No  | ⚠️ Some| ⚠️ Some| ✅ Yes       |
+------------------------+--------+--------+--------+--------------+
| Prevent use-after-free | ❌ No  | ❌ No  | ❌ No  | ✅ Yes       |
+------------------------+--------+--------+--------+--------------+
| Prevent data races     | ❌ No  | ⚠️ Some| ❌ No  | ✅ Yes       |
+------------------------+--------+--------+--------+--------------+
| Null pointer safety    | ❌ No  | ✅ Yes | ⚠️ Some| ✅ Yes       |
+------------------------+--------+--------+--------+--------------+
| Type safety            | ⚠️ Weak| ✅ Yes | ✅ Yes | ✅ Yes       |
+------------------------+--------+--------+--------+--------------+
| Runtime overhead       | None   | Low    | Low    | Minimal      |
+------------------------+--------+--------+--------+--------------+
| Certification status   | ✅ Wide| ✅ Wide| ✅ Wide| ⚠️ Emerging  |
+------------------------+--------+--------+--------+--------------+

────────────────────────────────────────────────────────────────────────────

**2.2 Code Comparison: Sensor Reading**
---------------------------------------

**C Implementation:**

.. code-block:: c

   // C: Manual error handling, potential memory leaks
   typedef struct {
       int id;
       float temperature;
   } SensorReading;
   
   SensorReading* read_sensor(int sensor_id) {
       SensorReading* reading = malloc(sizeof(SensorReading));
       if (reading == NULL) {
           return NULL;  // Allocation failed
       }
       
       reading->id = sensor_id;
       reading->temperature = read_hw_register(0x1000);
       
       return reading;  // Caller must remember to free()
   }
   
   // Usage (potential memory leak if free() forgotten)
   SensorReading* r = read_sensor(5);
   if (r != NULL) {
       printf("Temp: %.2f\n", r->temperature);
       free(r);  // ❌ Easy to forget
   }

**Rust Implementation:**

.. code-block:: rust

   // Rust: Automatic memory management, enforced error handling
   struct SensorReading {
       id: u32,
       temperature: f32,
   }
   
   fn read_sensor(sensor_id: u32) -> Option<SensorReading> {
       // Simulated hardware read
       Some(SensorReading {
           id: sensor_id,
           temperature: 25.5,
       })
   }  // Memory automatically freed when SensorReading goes out of scope
   
   // Usage (compiler forces Option handling)
   fn main() {
       if let Some(reading) = read_sensor(5) {
           println!("Temp: {:.2}", reading.temperature);
       }  // reading automatically dropped here (no manual free needed)
   }

**Key Advantages:**
- ✅ No manual memory management (ownership handles it)
- ✅ No null checks (Option<T> forces handling)
- ✅ No memory leaks (automatic Drop trait)

═══════════════════════════════════════════════════════════════════════════════

📖 **3. CERTIFICATION CHALLENGES**
═══════════════════════════════════════════════════════════════════════════════

3.1 Compiler Qualification Requirements
----------------------------------------

**DO-178C Requirements:**

.. code-block:: text

   Tool Qualification Level (TQL):
   - TQL-1: Can introduce errors, cannot be detected (highest scrutiny)
   - TQL-5: Cannot introduce errors (lowest scrutiny)
   
   Rust Compiler Classification:
   - TQL-1 (compiler = verification tool, generates object code)
   - Requires: Tool Operational Requirements (TOR), Tool Qualification Plan

**Challenges:**

.. code-block:: text

   1. Compiler Complexity:
      - LLVM backend (millions of lines of code)
      - Optimizer transformations (difficult to verify)
      - Incremental compilation caching
   
   2. Language Evolution:
      - New features added every 6 weeks (stable releases)
      - Backward compatibility not guaranteed for all features
      - Certification requires frozen toolchain
   
   3. Standard Library:
      - Which subset is certifiable? (core, alloc, std?)
      - Panic behavior (unwinding vs abort)
      - Unsafe code in std library

────────────────────────────────────────────────────────────────────────────

**3.2 Ferrocene — Qualified Rust Toolchain**
--------------------------------------------

**Status (2026):** ISO 26262 qualification in progress, DO-178C planned

.. code-block:: text

   Ferrocene Goals:
   ✅ Qualified compiler (frozen version of rustc + LLVM)
   ✅ Qualified standard library subset
   ✅ Documentation package (TOR, verification results)
   ✅ Long-term support (10+ years)
   ✅ Deterministic builds
   
   Target Certifications:
   - ISO 26262 ASIL D (automotive) — 2026 target
   - DO-178C DAL A (avionics) — 2027 target
   - IEC 61508 SIL 3 (industrial) — 2026 target
   - EN 50128 SIL 4 (railway) — 2027 target

**Qualification Process:**

.. code-block:: text

   1. Define qualified subset (language features allowed)
   2. Freeze compiler version (no updates during project)
   3. Test suite (MISRA-like compliance checks)
   4. Traceability (source code → object code verification)
   5. Tool validation report (submit to certification authority)

────────────────────────────────────────────────────────────────────────────

**3.3 Unsafe Code Restrictions**
--------------------------------

**Problem:** `unsafe` keyword bypasses Rust's safety guarantees

.. code-block:: rust

   // Unsafe allows:
   // - Dereferencing raw pointers
   // - Calling unsafe functions
   // - Accessing mutable static variables
   // - Implementing unsafe traits
   
   unsafe {
       let ptr = 0x1000 as *const u32;  // Hardware register
       let value = *ptr;  // Dereference (no safety checks)
   }

**Certification Requirement:**

.. code-block:: text

   ✅ Minimize unsafe code (< 5% of codebase)
   ✅ Isolate in audited modules (hardware abstraction layer)
   ✅ Document safety invariants (pre/post conditions)
   ✅ Review by safety experts (manual analysis)
   
   Example Policy (ISO 26262 ASIL D):
   - All unsafe blocks require justification + review
   - Unsafe code limited to HAL (Hardware Abstraction Layer)
   - Formal verification of unsafe abstractions (Prusti, KANI)

────────────────────────────────────────────────────────────────────────────

**3.4 Panic Behavior Configuration**
------------------------------------

**Problem:** Panics (runtime errors) must be controlled in safety-critical systems

.. code-block:: rust

   // Panic triggers (must be eliminated or handled):
   // - Array out-of-bounds
   // - Integer overflow (in debug mode)
   // - unwrap() on None
   // - Division by zero

**Certification Configuration:**

.. code-block:: toml

   # Cargo.toml
   [profile.release]
   panic = "abort"  # Don't unwind, immediately abort (simpler, deterministic)
   overflow-checks = true  # Check integer overflow even in release mode
   lto = true  # Link-time optimization (better dead code elimination)

**Safe Alternatives:**

.. code-block:: rust

   // ❌ Don't use unwrap() (can panic)
   let value = option.unwrap();
   
   // ✅ Use match or if-let (explicit handling)
   let value = match option {
       Some(v) => v,
       None => return Err(Error::SensorFailure),
   };
   
   // ✅ Use expect() with clear message (for debugging)
   let value = option.expect("Sensor should always be available during init");

═══════════════════════════════════════════════════════════════════════════════

📖 **4. REAL-WORLD SAFETY-CRITICAL RUST (2026 STATUS)**
═══════════════════════════════════════════════════════════════════════════════

4.1 Automotive: Volvo Cars
---------------------------

**Project:** Low-level software components in Electric Vehicle (EV) platform

.. code-block:: text

   Status: Prototype/evaluation (2024-2026)
   Certification: ISO 26262 ASIL B (non-critical subsystems)
   Components:
   - Battery management system (BMS) monitoring
   - Sensor data aggregation (non-safety-critical path)
   - Diagnostics logging
   
   Tools: Ferrocene (ISO 26262 qualification in progress)
   
   Benefits Reported:
   ✅ 70% reduction in memory safety bugs (compared to C baseline)
   ✅ Faster development (less debugging time)
   ⚠️ Learning curve (6-month ramp-up for C++ developers)

────────────────────────────────────────────────────────────────────────────

**4.2 Avionics: Airbus (Research)**
-----------------------------------

**Project:** Flight control software prototypes (not in production aircraft)

.. code-block:: text

   Status: Research phase (2025-2026)
   Certification: DO-178C DAL C/D (exploring feasibility)
   Focus Areas:
   - Ground support equipment
   - Non-flight-critical subsystems
   - Tooling (test harnesses, data analysis)
   
   Challenges:
   ❌ No qualified Rust compiler for DO-178C DAL A/B yet
   ❌ Aerospace conservative culture (slow adoption)
   ⚠️ Formal methods integration needed (SCADE, model-based design)

────────────────────────────────────────────────────────────────────────────

**4.3 Industrial: Programmable Logic Controllers (PLCs)**
---------------------------------------------------------

**Project:** Siemens, Beckhoff exploring Rust for control software

.. code-block:: text

   Status: Early adoption (SIL 1-2, 2025-2026)
   Certification: IEC 61508 SIL 1-2 (lower safety integrity levels)
   Use Cases:
   - Edge computing modules
   - Data preprocessing pipelines
   - Communication stacks (EtherCAT, PROFINET)
   
   Benefits:
   ✅ Memory safety (prevents buffer overflows in network stacks)
   ✅ Concurrency (async/await for real-time event handling)
   ⚠️ Real-time guarantees still challenging (garbage collector-free helps)

────────────────────────────────────────────────────────────────────────────

**4.4 Medical Devices: Class A/B**
----------------------------------

**Project:** Patient monitoring device firmware

.. code-block:: text

   Status: Prototype (IEC 62304 Class A/B, 2025-2026)
   Certification: FDA 510(k) (lower-risk devices)
   Components:
   - Bluetooth communication stack
   - Data logging and storage
   - User interface (non-alarm logic)
   
   Benefits:
   ✅ No buffer overflows in BLE stack (security + safety)
   ✅ Type safety prevents wrong unit conversions (mg vs g)
   
   Limitations:
   ❌ Class C (life-sustaining devices) still requires C/C++ (toolchain maturity)

═══════════════════════════════════════════════════════════════════════════════

📖 **5. FORMAL VERIFICATION TOOLS**
═══════════════════════════════════════════════════════════════════════════════

5.1 Prusti — Deductive Verification
------------------------------------

**Tool:** Prusti (ETH Zurich, based on Viper verification infrastructure)

**Capability:** Prove functional correctness using preconditions/postconditions

.. code-block:: rust

   use prusti_contracts::*;
   
   #[requires(divisor != 0)]  // Precondition: prevent division by zero
   #[ensures(result == dividend / divisor)]  // Postcondition: correct result
   fn safe_divide(dividend: i32, divisor: i32) -> i32 {
       dividend / divisor
   }
   
   fn main() {
       let result = safe_divide(10, 2);  // ✅ Verifies (divisor != 0)
       
       // ❌ This would fail verification:
       // safe_divide(10, 0);  // Prusti error: precondition violated
   }

**Use Case:** Prove absence of panics, validate safety properties

────────────────────────────────────────────────────────────────────────────

**5.2 KANI — Model Checking**
-----------------------------

**Tool:** KANI (Amazon Web Services, based on CBMC)

**Capability:** Exhaustively check all possible executions (bounded)

.. code-block:: rust

   #[kani::proof]
   fn verify_sensor_range() {
       let sensor_value: u8 = kani::any();  // All possible u8 values (0-255)
       
       // Assert: sensor value must be in valid range
       if sensor_value >= 10 && sensor_value <= 100 {
           // Process valid sensor data
           let calibrated = sensor_value * 2;
           assert!(calibrated >= 20 && calibrated <= 200);  // Verification passes
       }
   }

**Result:** KANI checks all 256 possible u8 values, proves assertion always holds

────────────────────────────────────────────────────────────────────────────

**5.3 MIRAI — Abstract Interpretation**
---------------------------------------

**Tool:** MIRAI (Facebook/Meta)

**Capability:** Static analysis for common bugs (panics, overflows, precondition violations)

.. code-block:: rust

   fn process_array(arr: &[i32], index: usize) -> i32 {
       arr[index]  // MIRAI warns: potential out-of-bounds access
   }
   
   // MIRAI recommendation: Add bounds check
   fn safe_process_array(arr: &[i32], index: usize) -> Option<i32> {
       arr.get(index).copied()  // ✅ No warning (safe access)
   }

═══════════════════════════════════════════════════════════════════════════════

📖 **6. EMBEDDED RUST (NO_STD ENVIRONMENT)**
═══════════════════════════════════════════════════════════════════════════════

6.1 No Standard Library (no_std)
---------------------------------

**Requirement:** Safety-critical embedded systems often have no OS (bare-metal)

.. code-block:: rust

   #![no_std]  // Don't link standard library (no heap, no OS dependencies)
   #![no_main]  // No default main function
   
   use panic_halt as _;  // Panic handler (halt on panic)
   
   #[no_mangle]
   pub extern "C" fn _start() -> ! {
       // Entry point for embedded system
       loop {
           // Main control loop
       }
   }

────────────────────────────────────────────────────────────────────────────

**6.2 Hardware Abstraction Layer (HAL)**
----------------------------------------

**Example: ARM Cortex-M Microcontroller**

.. code-block:: rust

   use cortex_m_rt::entry;  // Runtime for ARM Cortex-M
   use stm32f4xx_hal::{pac, prelude::*};  // STM32F4 HAL
   
   #[entry]
   fn main() -> ! {
       let peripherals = pac::Peripherals::take().unwrap();
       let gpioa = peripherals.GPIOA.split();
       
       // Configure LED pin as output
       let mut led = gpioa.pa5.into_push_pull_output();
       
       loop {
           led.set_high();  // LED on
           cortex_m::asm::delay(1_000_000);
           led.set_low();   // LED off
           cortex_m::asm::delay(1_000_000);
       }
   }

**Safety Benefits:**
- ✅ Type-safe register access (no magic numbers)
- ✅ Compile-time peripheral ownership (can't access same GPIO from multiple threads)
- ✅ No null pointers (Option<T> for peripheral availability)

────────────────────────────────────────────────────────────────────────────

**6.3 Real-Time Operating System (RTOS)**
-----------------------------------------

**Example: RTIC (Real-Time Interrupt-driven Concurrency)**

.. code-block:: rust

   #![no_std]
   #![no_main]
   
   use rtic::app;
   
   #[app(device = stm32f4xx_hal::pac, dispatchers = [EXTI0])]
   mod app {
       use stm32f4xx_hal::{gpio, prelude::*};
       
       #[shared]
       struct Shared {
           sensor_value: u32,
       }
       
       #[local]
       struct Local {
           led: gpio::PA5<gpio::Output<gpio::PushPull>>,
       }
       
       #[init]
       fn init(ctx: init::Context) -> (Shared, Local, init::Monotonics) {
           let peripherals = ctx.device;
           let gpioa = peripherals.GPIOA.split();
           let led = gpioa.pa5.into_push_pull_output();
           
           (Shared { sensor_value: 0 }, Local { led }, init::Monotonics())
       }
       
       // Task triggered by timer interrupt
       #[task(shared = [sensor_value], local = [led])]
       fn blink(ctx: blink::Context) {
           ctx.local.led.toggle();
           
           // Access shared resource (automatically uses critical section)
           ctx.shared.sensor_value.lock(|val| {
               *val += 1;
           });
       }
   }

**RTIC Benefits:**
- ✅ Data race freedom (enforced by borrow checker + static analysis)
- ✅ Deadlock freedom (static priority-based scheduling)
- ✅ Zero-cost abstractions (no runtime overhead vs hand-written C)

═══════════════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
═══════════════════════════════════════════════════════════════════════════════

**Q1:** How does Rust's ownership system prevent use-after-free bugs at compile time?

**A1:**

**Ownership Rules:**

.. code-block:: text

   1. Each value has exactly ONE owner
   2. When owner goes out of scope, value is automatically dropped (freed)
   3. Ownership can be moved or borrowed, but not both simultaneously

**Example:**

.. code-block:: rust

   let data = String::from("sensor reading");
   process(data);  // Ownership moved to process()
   
   // ❌ Compiler error: value used after move
   // println!("{}", data);

**Result:** Compile-time error prevents use-after-free (no runtime check needed).

**C Comparison:** In C, pointer remains valid after free(), causing undefined behavior. Rust makes this impossible by invalidating the original variable.

────────────────────────────────────────────────────────────────────────────

**Q2:** What are the main challenges for Rust certification in DO-178C DAL A avionics?

**A2:**

**Challenges:**

.. code-block:: text

   1. Compiler Qualification:
      - Rust compiler (rustc + LLVM) is Tool Qualification Level TQL-1
      - Millions of lines of code to verify
      - Optimizer transformations difficult to prove correct
   
   2. Language Evolution:
      - Rust updates every 6 weeks (new features, bug fixes)
      - Certification requires frozen toolchain (no updates for 10+ years)
      - Need qualified subset (Ferrocene effort)
   
   3. Unsafe Code:
      - Hardware access requires `unsafe` blocks
      - Must audit all unsafe code manually (negates some benefits)
      - Formal verification needed (Prusti, KANI)
   
   4. Panic Behavior:
      - Runtime errors (array bounds, unwrap) can panic
      - Must configure panic=abort and eliminate all panics
      - Requires extensive testing to prove no panics
   
   5. Cultural Adoption:
      - Aerospace industry conservative (slow to change from C/Ada)
      - Limited experienced Rust developers in aerospace
      - Training costs and learning curve

**Status 2026:** Research phase only, not yet approved for DAL A/B flight-critical software.

────────────────────────────────────────────────────────────────────────────

**Q3:** Compare memory safety mechanisms: C, Ada, MISRA C++, and Rust.

**A3:**

+------------------------+------------+------------+------------+------------+
| Memory Safety Feature  | C          | Ada        | MISRA C++  | Rust       |
+========================+============+============+============+============+
| Buffer overflow        | ❌ None    | ⚠️ Runtime | ⚠️ Guideline| ✅ Compile|
| prevention             |            | check      | only       | + runtime  |
+------------------------+------------+------------+------------+------------+
| Use-after-free         | ❌ None    | ❌ None    | ❌ None    | ✅ Compile |
+------------------------+------------+------------+------------+------------+
| Data race prevention   | ❌ None    | ⚠️ Protected| ❌ None    | ✅ Compile |
|                        |            | objects    |            |            |
+------------------------+------------+------------+------------+------------+
| Null pointer safety    | ❌ None    | ✅ Compile | ⚠️ Guideline| ✅ Compile |
|                        |            |            | (unique_ptr)|            |
+------------------------+------------+------------+------------+------------+
| Type safety            | ⚠️ Weak    | ✅ Strong  | ✅ Strong  | ✅ Strong  |
+------------------------+------------+------------+------------+------------+
| Certification status   | ✅ Mature  | ✅ Mature  | ✅ Mature  | ⚠️ Emerging|
+------------------------+------------+------------+------------+------------+

**Key Insight:** Rust is the only language preventing use-after-free and data races at compile time (zero runtime overhead for these checks).

────────────────────────────────────────────────────────────────────────────

**Q4:** What is the role of formal verification tools (Prusti, KANI, MIRAI) in Rust safety-critical development?

**A4:**

**Prusti (Deductive Verification):**

.. code-block:: text

   Purpose: Prove functional correctness
   Method: Preconditions, postconditions, loop invariants
   Example: Prove division-by-zero never occurs
   
   #[requires(divisor != 0)]
   fn divide(dividend: i32, divisor: i32) -> i32

**KANI (Model Checking):**

.. code-block:: text

   Purpose: Exhaustively test all possible inputs (bounded)
   Method: Symbolic execution, SAT solving
   Example: Verify sensor range check for all possible u8 values (0-255)
   
   let value: u8 = kani::any();
   assert!(validate_range(value));  // Checks all 256 values

**MIRAI (Abstract Interpretation):**

.. code-block:: text

   Purpose: Find common bugs (panics, overflows, null dereferences)
   Method: Static analysis, control flow analysis
   Example: Detect potential array out-of-bounds access
   
   Warning: arr[index] may panic if index >= arr.len()

**Integration with Certification:**

.. code-block:: text

   ✅ Supplement testing (reduce test cases needed)
   ✅ Prove safety properties (ASIL D, SIL 3/4 requirements)
   ✅ Document assumptions (preconditions as safety requirements)
   ⚠️ Tools themselves may need qualification (verification tool qualification)

────────────────────────────────────────────────────────────────────────────

**Q5:** Explain Rust's `no_std` embedded development and how it differs from standard Rust.

**A5:**

**Standard Rust (std):**

.. code-block:: text

   ✅ Standard library (Vec, String, HashMap, File I/O, threading)
   ✅ Dynamic memory allocation (heap)
   ✅ Operating system dependencies (Linux, Windows, macOS)
   ✅ Default panic unwinding
   
   Use case: Server applications, desktop software

**No-Standard Rust (no_std):**

.. code-block:: text

   ❌ No standard library (only core and alloc)
   ❌ No heap allocation by default (stack only)
   ❌ No OS dependencies (bare-metal)
   ✅ Panic = abort (no unwinding)
   
   Use case: Embedded systems, microcontrollers, safety-critical firmware

**Code Example:**

.. code-block:: rust

   #![no_std]  // Don't link std library
   #![no_main]  // No default main()
   
   use core::panic::PanicInfo;
   
   #[panic_handler]
   fn panic(_info: &PanicInfo) -> ! {
       loop {}  // Halt on panic (safety-critical requirement)
   }
   
   #[no_mangle]
   pub extern "C" fn _start() -> ! {
       // Bare-metal entry point
       loop {
           // Main control loop (never returns)
       }
   }

**Available Libraries:**
- **core:** Platform-agnostic primitives (Option, Result, iterators)
- **alloc:** Heap allocation (if allocator provided)
- **embedded-hal:** Hardware abstraction traits (GPIO, SPI, I2C)

**Benefits for Safety-Critical:**
- ✅ Smaller binary size (easier to verify)
- ✅ No hidden allocations (predictable memory usage)
- ✅ No OS dependencies (deterministic behavior)

═══════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Understanding:**
- [ ] Rust ownership prevents use-after-free at compile time
- [ ] Borrow checker prevents data races (no shared mutable state)
- [ ] Option<T> eliminates null pointer dereferences
- [ ] Memory safety without garbage collection (zero-cost abstractions)

**Certification:**
- [ ] Compiler qualification is main challenge (TQL-1 for DO-178C, ISO 26262)
- [ ] Ferrocene provides qualified toolchain (ISO 26262 ASIL D target 2026)
- [ ] Minimize unsafe code (< 5%, isolate in audited HAL modules)
- [ ] Configure panic=abort and eliminate runtime panics

**Comparison:**
- [ ] Rust prevents more bug classes than C, Ada, MISRA C++ (at compile time)
- [ ] Tradeoff: Learning curve vs long-term safety benefits
- [ ] 2026 status: Emerging (prototypes only, not production-critical yet)

**Tools:**
- [ ] Prusti: Prove functional correctness (preconditions/postconditions)
- [ ] KANI: Exhaustive model checking (bounded verification)
- [ ] MIRAI: Static analysis (detect panics, overflows)

**Embedded:**
- [ ] no_std for bare-metal (no OS, no heap by default)
- [ ] embedded-hal for hardware abstraction (type-safe registers)
- [ ] RTIC for real-time concurrency (data race + deadlock freedom)

═══════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
═══════════════════════════════════════════════════════════════════════════════

1️⃣ **Memory safety without garbage collection** — Rust eliminates 70% of C/C++ vulnerabilities (buffer overflows, use-after-free, data races) at compile time, with zero runtime overhead

2️⃣ **Ownership + borrow checker = compiler-enforced safety** — Prevents entire classes of undefined behavior that static analysis tools (Coverity, Polyspace) can only warn about in C

3️⃣ **Certification is the bottleneck** — Rust language is ready, but qualified toolchains (Ferrocene) and industry acceptance lag behind (2-5 years for DO-178C DAL A, ISO 26262 ASIL D)

4️⃣ **2026 status: Emerging, not mature** — Prototypes in automotive (Volvo), research in avionics (Airbus), early adoption in industrial SIL 1-2, but NOT yet approved for flight-critical or life-sustaining devices

5️⃣ **Formal verification amplifies safety** — Prusti, KANI, MIRAI prove properties beyond testing, complement certification requirements (especially for SIL 3/4, ASIL D)

6️⃣ **Embedded Rust (no_std) is production-ready** — Bare-metal support mature, RTIC provides data-race-free real-time concurrency, extensive HAL ecosystem for ARM Cortex-M/R

7️⃣ **Unsafe code is the escape hatch** — Hardware access requires `unsafe`, must be minimized and audited, negates some compile-time safety guarantees (but still better than C's all-unsafe default)

═══════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **RUST FOR SAFETY-CRITICAL SYSTEMS CHEATSHEET COMPLETE**

**Created:** January 15, 2026  
**Coverage:** Ownership and borrow checker, memory safety comparison (C/Ada/MISRA C++/Rust), certification challenges (DO-178C, ISO 26262, IEC 61508), real-world adoption status (automotive/avionics/industrial/medical), formal verification tools (Prusti/KANI/MIRAI), embedded Rust (no_std, HAL, RTIC), qualified toolchains (Ferrocene)

═══════════════════════════════════════════════════════════════════════════════
