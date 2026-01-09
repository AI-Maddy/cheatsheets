
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**Embedded C Cheat Sheet for Abstract Data Types (ADT)**  
focusing on the most common ones in resource-constrained embedded systems: **List**, **Queue**, **Ring Buffer** (circular queue), **Stack**, **Pool** (fixed-size object allocator), and **State Machine**.

All examples use **static allocation only** (no ``malloc``/``free``), deterministic behavior, and minimal RAM/Flash usage.

📌 1. Ring Buffer / Circular Queue (most used in embedded)

.. code-block:: c

#define RINGBUF_SIZE 64

typedef struct {
    uint8_t  buf[RINGBUF_SIZE];
    uint16_t head;          // write index
    uint16_t tail;          // read index
    uint16_t count;         // current items
} RingBuf_t;

// Initialize
void RingBuf_Init(RingBuf_t *rb) {
    rb->head = rb->tail = rb->count = 0;
}

// Enqueue (return false if full)
bool RingBuf_Put(RingBuf_t *rb, uint8_t byte) {
    if (rb->count >= RINGBUF_SIZE) return false;
    rb->buf[rb->head] = byte;
    rb->head = (rb->head + 1) % RINGBUF_SIZE;
    rb->count++;
    return true;
}

// Dequeue (return false if empty)
bool RingBuf_Get(RingBuf_t *rb, uint8_t *byte) {
    if (rb->count == 0) return false;
    *byte = rb->buf[rb->tail];
    rb->tail = (rb->tail + 1) % RINGBUF_SIZE;
    rb->count--;
    return true;
}

// Status helpers
bool RingBuf_IsFull(const RingBuf_t *rb)  { return rb->count == RINGBUF_SIZE; }
bool RingBuf_IsEmpty(const RingBuf_t *rb) { return rb->count == 0; }
uint16_t RingBuf_Count(const RingBuf_t *rb) { return rb->count; }

**Variants**  
- Use ``volatile`` on ``buf``, ``head``, ``tail``, ``count`` if accessed from ISR + main  
- For multi-byte items → change ``uint8_t`` to desired type and adjust indexing

📌 2. Single-linked List (used sparingly – prefer arrays)

.. code-block:: c

typedef struct ListNode {
    struct ListNode *next;
    uint32_t         value;     // or any payload
    void            *data;      // optional generic pointer
} ListNode_t;

// Static pool example (🔴 🔴 avoid dynamic allocation)
#define MAX_NODES 32
static ListNode_t node_pool[MAX_NODES];
static ListNode_t *free_list = NULL;

void List_InitPool(void) {
    free_list = NULL;
    for (int i = 0; i < MAX_NODES; i++) {
        node_pool[i].next = free_list;
        free_list = &node_pool[i];
    }
}

ListNode_t *List_Alloc(void) {
    if (!free_list) return NULL;
    ListNode_t *node = free_list;
    free_list = free_list->next;
    node->next = NULL;
    return node;
}

void List_Free(ListNode_t *node) {
    node->next = free_list;
    free_list = node;
}

// Insert at head
void List_InsertHead(ListNode_t **head, ListNode_t *node) {
    node->next = *head;
    *head = node;
}

// Remove specific node (O(n))
bool List_Remove(ListNode_t **head, ListNode_t *node) {
    ListNode_t **curr = head;
    while (*curr) {
        if (*curr == node) {
            *curr = node->next;
            List_Free(node);
            return true;
        }
        curr = &(*curr)->next;
    }
    return false;
}

📌 3. Static Stack (LIFO)

.. code-block:: c

#define STACK_SIZE 32

typedef struct {
    uint32_t items[STACK_SIZE];
    int16_t  top;               // -1 = empty
} Stack_t;

void Stack_Init(Stack_t *s) {
    s->top = -1;
}

bool Stack_Push(Stack_t *s, uint32_t value) {
    if (s->top >= STACK_SIZE - 1) return false;
    s->items[++s->top] = value;
    return true;
}

bool Stack_Pop(Stack_t *s, uint32_t *value) {
    if (s->top < 0) return false;
    *value = s->items[s->top--];
    return true;
}

bool Stack_IsEmpty(const Stack_t *s) { return s->top < 0; }
bool Stack_IsFull(const Stack_t *s)  { return s->top >= STACK_SIZE - 1; }

💾 4. Fixed-size Object Pool (memory pool / slab-like)

.. code-block:: c

#define POOL_SIZE 16
#define ITEM_SIZE 32   // e.g. 32-byte CAN message

typedef struct {
    uint8_t  mem[POOL_SIZE][ITEM_SIZE];
    uint8_t  used[POOL_SIZE];   // 0=free, 1=used
} Pool_t;

void Pool_Init(Pool_t *p) {
    for (int i = 0; i < POOL_SIZE; i++) p->used[i] = 0;
}

void *Pool_Alloc(Pool_t *p) {
    for (int i = 0; i < POOL_SIZE; i++) {
        if (!p->used[i]) {
            p->used[i] = 1;
            return p->mem[i];
        }
    }
    return NULL;
}

void Pool_Free(Pool_t *p, void *ptr) {
    ptrdiff_t idx = (uint8_t *)ptr - (uint8_t *)p->mem;
    if (idx >= 0 && idx < POOL_SIZE * ITEM_SIZE && (idx % ITEM_SIZE == 0)) {
        p->used[idx / ITEM_SIZE] = 0;
    }
}

🏗️ 5. Simple State Machine (very common pattern)

.. code-block:: c

typedef enum : uint8_t {
    STATE_POWER_ON,
    STATE_IDLE,
    STATE_CONFIG,
    STATE_RUNNING,
    STATE_ERROR
} State_t;

typedef struct {
    State_t current;
    uint32_t timeout_ms;
    uint16_t error_code;
    void (*on_enter)(State_t old, State_t new);
    void (*on_exit)(State_t old, State_t new);
} StateMachine_t;

void SM_Transition(StateMachine_t *sm, State_t next) {
    if (sm->on_exit) sm->on_exit(sm->current, next);
    State_t old = sm->current;
    sm->current = next;
    if (sm->on_enter) sm->on_enter(old, next);
}

📌 6. Embedded C ADT Quick Rules of Thumb (2025–2026)

Rule                                      | Recommendation / Reason
------------------------------------------|---------------------------
Dynamic allocation (``malloc``/``free``)      | 🔴 🔴 Avoid in safety-critical & hard real-time code
Preferred ADT                                 | Ring buffer > static pool > linked list
Maximum stack usage per function          | Keep < 256–512 bytes (use static/global)
Use ``const``, ``static``, ``inline``           | Maximize flash placement & optimization
MISRA C Rule 8.7, 20.7, etc.              | No function-like macros for ADT ops, prefer inline
ISR safety                                | Use ``volatile``, disable/enable interrupts or atomic ops
Zero-cost abstraction                     | Prefer macros/inline functions over function pointers

🟢 🟢 Good luck implementing clean, deterministic ADTs in your embedded project!  
**Ring buffers** and **state machines** cover ~80 % of real-world needs in bare-metal / RTOS embedded C code in 2026. Keep everything static and sized at compile time whenever possible.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
