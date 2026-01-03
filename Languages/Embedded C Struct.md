**Cheat Sheet for `struct`, `enum`, and **ADT** (Abstract Data Types) in Embedded C**  
(oriented toward resource-constrained embedded systems – bare-metal, RTOS, no STL – 2025–2026 best practices)

### 1. `struct` – Basic Usage & Embedded Patterns

```c
// Classic named struct (most common in embedded)
typedef struct {
    uint8_t  state;         // 1 byte
    uint16_t sensor_value;  // 2 bytes
    uint32_t timestamp_ms;  // 4 bytes
    int16_t  temperature;   // 2 bytes
} SensorData_t;

// Anonymous struct inside typedef (cleaner in headers)
typedef struct {
    volatile uint32_t CR;       // Control Register
    volatile uint32_t SR;       // Status Register
    volatile uint32_t DR;       // Data Register
    uint32_t _reserved[10];
} UART_TypeDef;

// Packed struct – force no padding (very common in comms & registers)
#pragma pack(push, 1)           // or __attribute__((packed))
typedef struct {
    uint8_t  header;            // offset 0
    uint16_t length;            // offset 1
    uint8_t  command;           // offset 3
    uint32_t data;              // offset 4
} __attribute__((packed)) CANMessage_t;
#pragma pack(pop)

// Bitfield struct – perfect for hardware registers
typedef struct {
    uint32_t enable      : 1;
    uint32_t mode        : 2;
    uint32_t irq_en      : 1;
    uint32_t _reserved   : 12;
    uint32_t status      : 8;
    uint32_t overrun     : 1;
} __attribute__((packed)) StatusReg_t;

// Union + struct for register overlay (very common in drivers)
typedef union {
    uint32_t raw;
    struct {
        uint32_t start     : 1;
        uint32_t stop      : 1;
        uint32_t reset     : 1;
        uint32_t _rsvd     : 13;
        uint32_t error     : 8;
        uint32_t done      : 1;
    } bits;
} ControlReg_t;
```

**Embedded `struct` Best Practices**

Rule                                      | Why / Consequence
------------------------------------------|---------------------------
Use `typedef` + `_t` suffix               | Cleaner usage, self-documenting
Prefer `__attribute__((packed))` or `#pragma pack(1)` | Avoids padding → saves RAM, matches wire/register layout
Avoid large automatic structs on stack    | Stack overflow risk (use static/global or heap)
Use `volatile` on register structs        | Prevents compiler optimization on hardware access
Order fields descending size (largest first) | Better alignment & packing efficiency
Use unions for type-punning registers     | Clean & type-safe way to access bitfields/raw

### 2. `enum` – Modern Embedded Usage

```c
// Classic enum (C89 style – underlying type is int)
enum MotorState {
    MOTOR_OFF = 0,
    MOTOR_FWD,
    MOTOR_REV,
    MOTOR_BRAKE
};

// C11 / modern style – explicit underlying type (very useful in embedded)
typedef enum : uint8_t {
    STATE_IDLE    = 0x00,
    STATE_INIT    = 0x01,
    STATE_RUNNING = 0x10,
    STATE_ERROR   = 0xFF
} DeviceState_t;

// Bit flags – very common in status/control registers
typedef enum : uint32_t {
    FLAG_READY       = (1U << 0),
    FLAG_BUSY        = (1U << 1),
    FLAG_ERROR       = (1U << 2),
    FLAG_OVERRUN     = (1U << 3),
    FLAG_ALL_ERRORS  = FLAG_ERROR | FLAG_OVERRUN
} StatusFlags_t;

// Anonymous enum for compile-time constants (no type name needed)
enum {
    MAX_PACKET_SIZE = 512,
    UART_BAUD_115200 = 115200,
    WATCHDOG_TIMEOUT_MS = 5000
};
```

**Embedded `enum` Best Practices**

Rule                                      | Why / Consequence
------------------------------------------|---------------------------
Use `typedef enum : uint8_t / uint16_t`   | Controls size → saves RAM, matches register/protocol
Use bit flags with shifts `(1U << n)`     | Type-safe, readable, easy to combine with `| & ~`
Avoid gaps unless intentional             | Prevents accidental invalid states
Use anonymous enums for constants         | Cleaner than `#define`, scoped, no storage
Prefix enum values with module name       | Avoids name clashes (`MOTOR_STATE_OFF` vs `LED_STATE_OFF`)

### 3. Abstract Data Types (ADT) in Pure C (no C++)

Most common embedded ADT patterns (zero dynamic allocation preferred)

```c
// 1. Static fixed-size ring buffer (very common)
#define RINGBUF_SIZE 64
typedef struct {
    uint8_t  buffer[RINGBUF_SIZE];
    uint16_t head;
    uint16_t tail;
    uint16_t count;
} RingBuffer_t;

// 2. Linked list node (used sparingly – prefer arrays)
typedef struct ListNode {
    struct ListNode *next;
    uint32_t         value;
    void            *payload;
} ListNode_t;

// 3. Simple state machine (most used ADT pattern in embedded)
typedef enum : uint8_t {
    SM_IDLE, SM_CONFIG, SM_RUNNING, SM_ERROR
} SM_State_t;

typedef struct {
    SM_State_t   state;
    uint32_t     timeout_ms;
    uint16_t     error_code;
    void       (*on_enter)(void);
    void       (*on_exit)(void);
} StateMachine_t;

// 4. Opaque handle / ADT style (hides implementation)
typedef struct QueueImpl Queue_t;          // forward declaration

Queue_t* Queue_Create(uint16_t capacity);
void     Queue_Destroy(Queue_t *q);
bool     Queue_Enqueue(Queue_t *q, void *item);
bool     Queue_Dequeue(Queue_t *q, void **item);
```

**Embedded ADT Best Practices**

Pattern                                | When to Use                              | Memory / Determinism
---------------------------------------|------------------------------------------|-----------------------
Static array / fixed ring buffer      | Most queues, logs, command buffers       | Deterministic, no heap
Static pool + handle                  | Limited number of objects (tasks, timers)| Deterministic, fast
Opaque pointer (handle)               | Driver context, module instance          | Encapsulation, binary compatibility
Linked list / dynamic                 | Only if size truly unknown & RAM allows  | Non-deterministic, fragmentation risk
State machine struct                  | Almost every non-trivial stateful module | Very clean & maintainable

### Quick Reference – Embedded C `struct`/`enum`/ADT Rules of Thumb

Rule                                      | Recommendation
------------------------------------------|---------------------------
Max stack usage per function              | < 256–512 bytes (usually)
Prefer static/global over dynamic         | Avoid `malloc` in safety-critical code
Use `const` & `static` aggressively       | Compiler can optimize & place in flash
Zero-cost abstraction                     | Use inline functions, macros, opaque handles
MISRA C / BARR-C compliance               | Restrict pointer arithmetic, unions carefully

Good luck writing clean, safe, and resource-efficient embedded C!  
The most common pattern in 2025–2026 embedded projects is still **packed structs + fixed-size ring buffers + enum-based state machines** — keep it simple, deterministic, and statically allocated whenever possible.