================================================================================
Data Structures for Embedded Systems
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Data Structures and Algorithms Made Easy, Algorithms in a Nutshell
:Focus: Static allocation, memory-efficient implementations for embedded

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. Overview
================================================================================

Data structures for embedded systems must consider:

**Resource Constraints:**

- Limited RAM (32KB - 512KB typical for microcontrollers)
- No dynamic memory allocation (avoid malloc/free)
- Predictable memory usage
- Cache-friendly access patterns
- Minimal fragmentation

**Design Principles:**

- Static allocation with compile-time sizing
- Memory pools for dynamic-like behavior
- Fixed-size containers
- In-place algorithms
- Cache-aware data layout

================================================================================
2. Arrays and Buffers
================================================================================

2.1 Static Arrays
--------------------------------------------------------------------------------

**Basic Array Declaration:**

.. code-block:: c

   #define MAX_SENSORS 16
   
   // Static array - compile-time size
   int sensor_readings[MAX_SENSORS];
   
   // Initialize to zero
   int calibration_data[MAX_SENSORS] = {0};
   
   // Explicit initialization
   const uint8_t lookup_table[256] = {
       0x00, 0x01, 0x02, /* ... */
   };

**Array Operations:**

.. code-block:: c

   // Array traversal
   void process_all_sensors(void) {
       for (int i = 0; i < MAX_SENSORS; i++) {
           sensor_readings[i] = read_sensor(i);
       }
   }
   
   // Array search (linear)
   int find_sensor_index(int sensor_id) {
       for (int i = 0; i < MAX_SENSORS; i++) {
           if (sensor_ids[i] == sensor_id) {
               return i;
           }
       }
       return -1;  // Not found
   }
   
   // Array insertion (shift elements)
   bool insert_at(int array[], int *size, int max_size, 
                  int index, int value) {
       if (*size >= max_size || index > *size) {
           return false;
       }
       
       // Shift elements right
       for (int i = *size; i > index; i--) {
           array[i] = array[i - 1];
       }
       
       array[index] = value;
       (*size)++;
       return true;
   }
   
   // Array deletion (shift elements)
   bool delete_at(int array[], int *size, int index) {
       if (index >= *size) {
           return false;
       }
       
       // Shift elements left
       for (int i = index; i < *size - 1; i++) {
           array[i] = array[i + 1];
       }
       
       (*size)--;
       return true;
   }

2.2 Circular Buffers (Ring Buffers)
--------------------------------------------------------------------------------

**Essential for Embedded I/O:**

.. code-block:: c

   #define BUFFER_SIZE 64  // Power of 2 for efficient modulo
   
   typedef struct {
       uint8_t data[BUFFER_SIZE];
       volatile uint32_t head;  // Write index
       volatile uint32_t tail;  // Read index
       volatile uint32_t count; // Number of elements
   } circular_buffer_t;
   
   // Initialize buffer
   void circ_buf_init(circular_buffer_t *cb) {
       cb->head = 0;
       cb->tail = 0;
       cb->count = 0;
   }
   
   // Check if buffer is full
   bool circ_buf_is_full(circular_buffer_t *cb) {
       return cb->count == BUFFER_SIZE;
   }
   
   // Check if buffer is empty
   bool circ_buf_is_empty(circular_buffer_t *cb) {
       return cb->count == 0;
   }
   
   // Write to buffer (producer - interrupt context)
   bool circ_buf_write(circular_buffer_t *cb, uint8_t data) {
       if (circ_buf_is_full(cb)) {
           return false;  // Buffer overflow
       }
       
       cb->data[cb->head] = data;
       cb->head = (cb->head + 1) & (BUFFER_SIZE - 1);  // Efficient modulo
       cb->count++;
       return true;
   }
   
   // Read from buffer (consumer - main loop)
   bool circ_buf_read(circular_buffer_t *cb, uint8_t *data) {
       if (circ_buf_is_empty(cb)) {
           return false;  // Buffer underflow
       }
       
       *data = cb->data[cb->tail];
       cb->tail = (cb->tail + 1) & (BUFFER_SIZE - 1);
       cb->count--;
       return true;
   }
   
   // Peek without removing
   bool circ_buf_peek(circular_buffer_t *cb, uint8_t *data) {
       if (circ_buf_is_empty(cb)) {
           return false;
       }
       
       *data = cb->data[cb->tail];
       return true;
   }

**UART Reception Using Circular Buffer:**

.. code-block:: c

   static circular_buffer_t uart_rx_buffer;
   
   // Interrupt handler
   void UART_IRQHandler(void) {
       uint8_t byte = UART->DATA;
       circ_buf_write(&uart_rx_buffer, byte);
   }
   
   // Main loop processing
   void process_uart_data(void) {
       uint8_t byte;
       while (circ_buf_read(&uart_rx_buffer, &byte)) {
           handle_received_byte(byte);
       }
   }

================================================================================
3. Linked Lists
================================================================================

3.1 Memory Pool for Nodes
--------------------------------------------------------------------------------

**Static Memory Pool (No malloc):**

.. code-block:: c

   #define MAX_LIST_NODES 32
   
   typedef struct node {
       int data;
       struct node *next;
   } node_t;
   
   // Memory pool
   typedef struct {
       node_t pool[MAX_LIST_NODES];
       bool used[MAX_LIST_NODES];
       int free_count;
   } node_pool_t;
   
   static node_pool_t g_node_pool;
   
   // Initialize memory pool
   void node_pool_init(node_pool_t *pool) {
       for (int i = 0; i < MAX_LIST_NODES; i++) {
           pool->used[i] = false;
       }
       pool->free_count = MAX_LIST_NODES;
   }
   
   // Allocate node from pool
   node_t* node_alloc(node_pool_t *pool) {
       for (int i = 0; i < MAX_LIST_NODES; i++) {
           if (!pool->used[i]) {
               pool->used[i] = true;
               pool->free_count--;
               return &pool->pool[i];
           }
       }
       return NULL;  // Pool exhausted
   }
   
   // Free node back to pool
   void node_free(node_pool_t *pool, node_t *node) {
       int index = node - pool->pool;
       if (index >= 0 && index < MAX_LIST_NODES) {
           pool->used[index] = false;
           pool->free_count++;
       }
   }

3.2 Singly Linked List
--------------------------------------------------------------------------------

.. code-block:: c

   typedef struct {
       node_t *head;
       int size;
   } linked_list_t;
   
   // Initialize list
   void list_init(linked_list_t *list) {
       list->head = NULL;
       list->size = 0;
   }
   
   // Insert at front (O(1))
   bool list_insert_front(linked_list_t *list, int data) {
       node_t *new_node = node_alloc(&g_node_pool);
       if (!new_node) {
           return false;
       }
       
       new_node->data = data;
       new_node->next = list->head;
       list->head = new_node;
       list->size++;
       return true;
   }
   
   // Delete from front (O(1))
   bool list_delete_front(linked_list_t *list, int *data) {
       if (!list->head) {
           return false;
       }
       
       node_t *temp = list->head;
       *data = temp->data;
       list->head = temp->next;
       node_free(&g_node_pool, temp);
       list->size--;
       return true;
   }
   
   // Search for value (O(n))
   node_t* list_find(linked_list_t *list, int data) {
       node_t *current = list->head;
       while (current) {
           if (current->data == data) {
               return current;
           }
           current = current->next;
       }
       return NULL;
   }
   
   // Delete specific value
   bool list_delete_value(linked_list_t *list, int data) {
       if (!list->head) {
           return false;
       }
       
       // Check head
       if (list->head->data == data) {
           node_t *temp = list->head;
           list->head = temp->next;
           node_free(&g_node_pool, temp);
           list->size--;
           return true;
       }
       
       // Check rest of list
       node_t *current = list->head;
       while (current->next) {
           if (current->next->data == data) {
               node_t *temp = current->next;
               current->next = temp->next;
               node_free(&g_node_pool, temp);
               list->size--;
               return true;
           }
           current = current->next;
       }
       
       return false;
   }
   
   // Traverse and print
   void list_print(linked_list_t *list) {
       node_t *current = list->head;
       printf("List: ");
       while (current) {
           printf("%d -> ", current->data);
           current = current->next;
       }
       printf("NULL\n");
   }

3.3 Doubly Linked List
--------------------------------------------------------------------------------

.. code-block:: c

   typedef struct dnode {
       int data;
       struct dnode *next;
       struct dnode *prev;
   } dnode_t;
   
   typedef struct {
       dnode_t *head;
       dnode_t *tail;
       int size;
   } dlinked_list_t;
   
   // Insert at end (O(1) with tail pointer)
   bool dlist_insert_end(dlinked_list_t *list, int data) {
       dnode_t *new_node = dnode_alloc(&g_dnode_pool);
       if (!new_node) {
           return false;
       }
       
       new_node->data = data;
       new_node->next = NULL;
       
       if (!list->tail) {
           // Empty list
           new_node->prev = NULL;
           list->head = new_node;
           list->tail = new_node;
       } else {
           new_node->prev = list->tail;
           list->tail->next = new_node;
           list->tail = new_node;
       }
       
       list->size++;
       return true;
   }
   
   // Delete node (O(1) if node pointer known)
   void dlist_delete_node(dlinked_list_t *list, dnode_t *node) {
       if (node->prev) {
           node->prev->next = node->next;
       } else {
           list->head = node->next;
       }
       
       if (node->next) {
           node->next->prev = node->prev;
       } else {
           list->tail = node->prev;
       }
       
       dnode_free(&g_dnode_pool, node);
       list->size--;
   }

================================================================================
4. Stacks
================================================================================

4.1 Array-Based Stack
--------------------------------------------------------------------------------

.. code-block:: c

   #define STACK_SIZE 64
   
   typedef struct {
       int data[STACK_SIZE];
       int top;  // Index of top element (-1 if empty)
   } stack_t;
   
   // Initialize stack
   void stack_init(stack_t *stack) {
       stack->top = -1;
   }
   
   // Check if empty
   bool stack_is_empty(stack_t *stack) {
       return stack->top == -1;
   }
   
   // Check if full
   bool stack_is_full(stack_t *stack) {
       return stack->top == STACK_SIZE - 1;
   }
   
   // Push (O(1))
   bool stack_push(stack_t *stack, int value) {
       if (stack_is_full(stack)) {
           return false;  // Stack overflow
       }
       
       stack->data[++stack->top] = value;
       return true;
   }
   
   // Pop (O(1))
   bool stack_pop(stack_t *stack, int *value) {
       if (stack_is_empty(stack)) {
           return false;  // Stack underflow
       }
       
       *value = stack->data[stack->top--];
       return true;
   }
   
   // Peek (O(1))
   bool stack_peek(stack_t *stack, int *value) {
       if (stack_is_empty(stack)) {
           return false;
       }
       
       *value = stack->data[stack->top];
       return true;
   }
   
   // Get size
   int stack_size(stack_t *stack) {
       return stack->top + 1;
   }

**Expression Evaluation Example:**

.. code-block:: c

   // Evaluate postfix expression: 3 4 + 5 *
   int evaluate_postfix(const char *expr) {
       stack_t stack;
       stack_init(&stack);
       
       for (int i = 0; expr[i]; i++) {
           if (isdigit(expr[i])) {
               stack_push(&stack, expr[i] - '0');
           } else if (expr[i] == '+' || expr[i] == '*') {
               int b, a;
               stack_pop(&stack, &b);
               stack_pop(&stack, &a);
               
               int result = (expr[i] == '+') ? (a + b) : (a * b);
               stack_push(&stack, result);
           }
       }
       
       int result;
       stack_pop(&stack, &result);
       return result;
   }

4.2 Function Call Stack Example
--------------------------------------------------------------------------------

.. code-block:: c

   // Task context for task scheduler
   typedef struct {
       uint32_t stack_pointer;
       uint32_t registers[16];
       uint8_t priority;
   } task_context_t;
   
   #define MAX_TASKS 8
   task_context_t task_stack[MAX_TASKS];
   int current_task = -1;
   
   // Context switch simulation
   void push_task_context(task_context_t *ctx) {
       if (current_task < MAX_TASKS - 1) {
           task_stack[++current_task] = *ctx;
       }
   }

================================================================================
5. Queues
================================================================================

5.1 Array-Based Queue
--------------------------------------------------------------------------------

.. code-block:: c

   #define QUEUE_SIZE 32
   
   typedef struct {
       int data[QUEUE_SIZE];
       int front;  // Index of front element
       int rear;   // Index of next insertion point
       int count;  // Number of elements
   } queue_t;
   
   // Initialize queue
   void queue_init(queue_t *queue) {
       queue->front = 0;
       queue->rear = 0;
       queue->count = 0;
   }
   
   // Check if empty
   bool queue_is_empty(queue_t *queue) {
       return queue->count == 0;
   }
   
   // Check if full
   bool queue_is_full(queue_t *queue) {
       return queue->count == QUEUE_SIZE;
   }
   
   // Enqueue (O(1))
   bool queue_enqueue(queue_t *queue, int value) {
       if (queue_is_full(queue)) {
           return false;
       }
       
       queue->data[queue->rear] = value;
       queue->rear = (queue->rear + 1) % QUEUE_SIZE;  // Circular
       queue->count++;
       return true;
   }
   
   // Dequeue (O(1))
   bool queue_dequeue(queue_t *queue, int *value) {
       if (queue_is_empty(queue)) {
           return false;
       }
       
       *value = queue->data[queue->front];
       queue->front = (queue->front + 1) % QUEUE_SIZE;  // Circular
       queue->count--;
       return true;
   }
   
   // Peek front
   bool queue_peek(queue_t *queue, int *value) {
       if (queue_is_empty(queue)) {
           return false;
       }
       
       *value = queue->data[queue->front];
       return true;
   }

5.2 Priority Queue (Heap-Based)
--------------------------------------------------------------------------------

.. code-block:: c

   #define PQ_SIZE 32
   
   typedef struct {
       int priority;
       int data;
   } pq_element_t;
   
   typedef struct {
       pq_element_t heap[PQ_SIZE];
       int size;
   } priority_queue_t;
   
   // Initialize
   void pq_init(priority_queue_t *pq) {
       pq->size = 0;
   }
   
   // Swap elements
   static void pq_swap(pq_element_t *a, pq_element_t *b) {
       pq_element_t temp = *a;
       *a = *b;
       *b = temp;
   }
   
   // Heapify up (for insertion)
   static void pq_heapify_up(priority_queue_t *pq, int index) {
       while (index > 0) {
           int parent = (index - 1) / 2;
           
           // Min heap: parent should be smaller
           if (pq->heap[parent].priority <= pq->heap[index].priority) {
               break;
           }
           
           pq_swap(&pq->heap[parent], &pq->heap[index]);
           index = parent;
       }
   }
   
   // Heapify down (for extraction)
   static void pq_heapify_down(priority_queue_t *pq, int index) {
       while (true) {
           int left = 2 * index + 1;
           int right = 2 * index + 2;
           int smallest = index;
           
           if (left < pq->size && 
               pq->heap[left].priority < pq->heap[smallest].priority) {
               smallest = left;
           }
           
           if (right < pq->size && 
               pq->heap[right].priority < pq->heap[smallest].priority) {
               smallest = right;
           }
           
           if (smallest == index) {
               break;
           }
           
           pq_swap(&pq->heap[index], &pq->heap[smallest]);
           index = smallest;
       }
   }
   
   // Insert (O(log n))
   bool pq_insert(priority_queue_t *pq, int priority, int data) {
       if (pq->size >= PQ_SIZE) {
           return false;
       }
       
       pq->heap[pq->size].priority = priority;
       pq->heap[pq->size].data = data;
       pq_heapify_up(pq, pq->size);
       pq->size++;
       return true;
   }
   
   // Extract minimum (O(log n))
   bool pq_extract_min(priority_queue_t *pq, pq_element_t *element) {
       if (pq->size == 0) {
           return false;
       }
       
       *element = pq->heap[0];
       pq->heap[0] = pq->heap[pq->size - 1];
       pq->size--;
       pq_heapify_down(pq, 0);
       return true;
   }

**Task Scheduler with Priority Queue:**

.. code-block:: c

   priority_queue_t task_queue;
   
   // Add task with priority (lower = higher priority)
   void schedule_task(int priority, int task_id) {
       pq_insert(&task_queue, priority, task_id);
   }
   
   // Run highest priority task
   void run_next_task(void) {
       pq_element_t task;
       if (pq_extract_min(&task_queue, &task)) {
           execute_task(task.data);
       }
   }

================================================================================
6. Trees
================================================================================

6.1 Binary Tree with Memory Pool
--------------------------------------------------------------------------------

.. code-block:: c

   #define MAX_TREE_NODES 64
   
   typedef struct tree_node {
       int data;
       struct tree_node *left;
       struct tree_node *right;
   } tree_node_t;
   
   typedef struct {
       tree_node_t pool[MAX_TREE_NODES];
       bool used[MAX_TREE_NODES];
   } tree_pool_t;
   
   static tree_pool_t g_tree_pool;
   
   // Allocate tree node
   tree_node_t* tree_node_alloc(tree_pool_t *pool, int data) {
       for (int i = 0; i < MAX_TREE_NODES; i++) {
           if (!pool->used[i]) {
               pool->used[i] = true;
               pool->pool[i].data = data;
               pool->pool[i].left = NULL;
               pool->pool[i].right = NULL;
               return &pool->pool[i];
           }
       }
       return NULL;
   }
   
   // Free tree node
   void tree_node_free(tree_pool_t *pool, tree_node_t *node) {
       int index = node - pool->pool;
       if (index >= 0 && index < MAX_TREE_NODES) {
           pool->used[index] = false;
       }
   }

6.2 Binary Search Tree (BST)
--------------------------------------------------------------------------------

.. code-block:: c

   typedef struct {
       tree_node_t *root;
       int size;
   } bst_t;
   
   // Initialize BST
   void bst_init(bst_t *bst) {
       bst->root = NULL;
       bst->size = 0;
   }
   
   // Insert (recursive)
   tree_node_t* bst_insert_helper(tree_node_t *node, int data) {
       if (!node) {
           return tree_node_alloc(&g_tree_pool, data);
       }
       
       if (data < node->data) {
           node->left = bst_insert_helper(node->left, data);
       } else if (data > node->data) {
           node->right = bst_insert_helper(node->right, data);
       }
       
       return node;
   }
   
   bool bst_insert(bst_t *bst, int data) {
       int old_size = bst->size;
       bst->root = bst_insert_helper(bst->root, data);
       bst->size++;
       return bst->size > old_size;
   }
   
   // Search (recursive)
   tree_node_t* bst_search(tree_node_t *node, int data) {
       if (!node || node->data == data) {
           return node;
       }
       
       if (data < node->data) {
           return bst_search(node->left, data);
       } else {
           return bst_search(node->right, data);
       }
   }
   
   // Find minimum
   tree_node_t* bst_find_min(tree_node_t *node) {
       while (node && node->left) {
           node = node->left;
       }
       return node;
   }
   
   // In-order traversal (sorted output)
   void bst_inorder(tree_node_t *node) {
       if (node) {
           bst_inorder(node->left);
           printf("%d ", node->data);
           bst_inorder(node->right);
       }
   }
   
   // Pre-order traversal
   void bst_preorder(tree_node_t *node) {
       if (node) {
           printf("%d ", node->data);
           bst_preorder(node->left);
           bst_preorder(node->right);
       }
   }
   
   // Post-order traversal
   void bst_postorder(tree_node_t *node) {
       if (node) {
           bst_postorder(node->left);
           bst_postorder(node->right);
           printf("%d ", node->data);
       }
   }

6.3 Iterative Tree Traversals (Stack-Based)
--------------------------------------------------------------------------------

.. code-block:: c

   // Iterative in-order traversal
   void bst_inorder_iterative(tree_node_t *root) {
       stack_t stack;
       stack_init(&stack);
       tree_node_t *current = root;
       
       while (current || !stack_is_empty(&stack)) {
           // Reach leftmost node
           while (current) {
               stack_push(&stack, (int)current);
               current = current->left;
           }
           
           // Visit node
           stack_pop(&stack, (int*)&current);
           printf("%d ", current->data);
           
           // Move to right subtree
           current = current->right;
       }
   }

================================================================================
7. Hash Tables (Fixed-Size)
================================================================================

7.1 Chaining with Static Lists
--------------------------------------------------------------------------------

.. code-block:: c

   #define HASH_TABLE_SIZE 128
   #define MAX_CHAIN_LENGTH 8
   
   typedef struct hash_entry {
       int key;
       int value;
       bool occupied;
   } hash_entry_t;
   
   typedef struct {
       hash_entry_t chains[HASH_TABLE_SIZE][MAX_CHAIN_LENGTH];
   } hash_table_t;
   
   // Hash function
   static unsigned int hash(int key) {
       return (unsigned int)key % HASH_TABLE_SIZE;
   }
   
   // Initialize
   void ht_init(hash_table_t *ht) {
       for (int i = 0; i < HASH_TABLE_SIZE; i++) {
           for (int j = 0; j < MAX_CHAIN_LENGTH; j++) {
               ht->chains[i][j].occupied = false;
           }
       }
   }
   
   // Insert
   bool ht_insert(hash_table_t *ht, int key, int value) {
       unsigned int index = hash(key);
       
       // Find empty slot in chain
       for (int i = 0; i < MAX_CHAIN_LENGTH; i++) {
           if (!ht->chains[index][i].occupied) {
               ht->chains[index][i].key = key;
               ht->chains[index][i].value = value;
               ht->chains[index][i].occupied = true;
               return true;
           }
       }
       
       return false;  // Chain full
   }
   
   // Search
   bool ht_search(hash_table_t *ht, int key, int *value) {
       unsigned int index = hash(key);
       
       for (int i = 0; i < MAX_CHAIN_LENGTH; i++) {
           if (ht->chains[index][i].occupied && 
               ht->chains[index][i].key == key) {
               *value = ht->chains[index][i].value;
               return true;
           }
       }
       
       return false;
   }
   
   // Delete
   bool ht_delete(hash_table_t *ht, int key) {
       unsigned int index = hash(key);
       
       for (int i = 0; i < MAX_CHAIN_LENGTH; i++) {
           if (ht->chains[index][i].occupied && 
               ht->chains[index][i].key == key) {
               ht->chains[index][i].occupied = false;
               return true;
           }
       }
       
       return false;
   }

================================================================================
8. Performance Comparison
================================================================================

Time Complexities
--------------------------------------------------------------------------------

+-------------------+--------+--------+--------+--------+
| Data Structure    | Access | Search | Insert | Delete |
+===================+========+========+========+========+
| Array             | O(1)   | O(n)   | O(n)   | O(n)   |
+-------------------+--------+--------+--------+--------+
| Linked List       | O(n)   | O(n)   | O(1)*  | O(1)*  |
+-------------------+--------+--------+--------+--------+
| Stack             | O(n)   | O(n)   | O(1)   | O(1)   |
+-------------------+--------+--------+--------+--------+
| Queue             | O(n)   | O(n)   | O(1)   | O(1)   |
+-------------------+--------+--------+--------+--------+
| Binary Search Tree| O(n)** | O(n)** | O(n)** | O(n)** |
+-------------------+--------+--------+--------+--------+
| Hash Table        | N/A    | O(1)   | O(1)   | O(1)   |
+-------------------+--------+--------+--------+--------+
| Priority Queue    | O(1)   | O(n)   | O(log) | O(log) |
+-------------------+--------+--------+--------+--------+

\* If position is known
\** Average case O(log n) for balanced tree, O(n) worst case

Space Complexities
--------------------------------------------------------------------------------

All structures: O(n) where n is number of elements

================================================================================
9. Embedded Applications
================================================================================

9.1 Event Queue for Embedded Systems
--------------------------------------------------------------------------------

.. code-block:: c

   typedef struct {
       uint16_t event_id;
       uint32_t timestamp;
       uint8_t data[8];
   } event_t;
   
   #define EVENT_QUEUE_SIZE 16
   
   typedef struct {
       event_t events[EVENT_QUEUE_SIZE];
       int front, rear, count;
   } event_queue_t;
   
   event_queue_t g_event_queue;
   
   // Post event (from interrupt or task)
   bool post_event(uint16_t event_id, uint8_t *data) {
       if (g_event_queue.count >= EVENT_QUEUE_SIZE) {
           return false;
       }
       
       event_t *evt = &g_event_queue.events[g_event_queue.rear];
       evt->event_id = event_id;
       evt->timestamp = get_system_tick();
       memcpy(evt->data, data, 8);
       
       g_event_queue.rear = (g_event_queue.rear + 1) % EVENT_QUEUE_SIZE;
       g_event_queue.count++;
       return true;
   }
   
   // Process events (main loop)
   void process_events(void) {
       while (g_event_queue.count > 0) {
           event_t *evt = &g_event_queue.events[g_event_queue.front];
           handle_event(evt);
           
           g_event_queue.front = (g_event_queue.front + 1) % EVENT_QUEUE_SIZE;
           g_event_queue.count--;
       }
   }

9.2 LRU Cache for Flash Access
--------------------------------------------------------------------------------

.. code-block:: c

   #define CACHE_SIZE 8
   
   typedef struct cache_entry {
       uint32_t address;
       uint8_t data[64];
       bool valid;
       uint32_t last_used;
   } cache_entry_t;
   
   typedef struct {
       cache_entry_t entries[CACHE_SIZE];
       uint32_t access_counter;
   } lru_cache_t;
   
   static lru_cache_t flash_cache;
   
   // Read with LRU cache
   bool flash_read_cached(uint32_t address, uint8_t *data) {
       // Check cache
       for (int i = 0; i < CACHE_SIZE; i++) {
           if (flash_cache.entries[i].valid && 
               flash_cache.entries[i].address == address) {
               // Cache hit
               memcpy(data, flash_cache.entries[i].data, 64);
               flash_cache.entries[i].last_used = flash_cache.access_counter++;
               return true;
           }
       }
       
       // Cache miss - read from flash
       read_flash(address, data);
       
       // Find LRU entry to replace
       int lru_index = 0;
       uint32_t min_used = flash_cache.entries[0].last_used;
       
       for (int i = 1; i < CACHE_SIZE; i++) {
           if (flash_cache.entries[i].last_used < min_used) {
               min_used = flash_cache.entries[i].last_used;
               lru_index = i;
           }
       }
       
       // Update cache
       flash_cache.entries[lru_index].address = address;
       memcpy(flash_cache.entries[lru_index].data, data, 64);
       flash_cache.entries[lru_index].valid = true;
       flash_cache.entries[lru_index].last_used = flash_cache.access_counter++;
       
       return true;
   }

================================================================================
10. Best Practices
================================================================================

**Memory Management:**

1. Use static allocation with compile-time sizing
2. Implement memory pools for dynamic-like behavior
3. Track pool usage for debugging
4. Set maximum sizes based on worst-case analysis

**Performance:**

1. Choose appropriate data structure for access pattern
2. Use circular buffers for FIFO operations
3. Implement caching for expensive operations
4. Profile memory and CPU usage

**Safety:**

1. Always check return values for full/empty conditions
2. Use volatile for interrupt-shared data
3. Protect shared data with critical sections
4. Initialize all structures before use

**Debugging:**

1. Track high water marks for dynamic structures
2. Implement overflow/underflow detection
3. Add assertions for invariants
4. Log allocation failures

================================================================================
End of Data Structures Cheatsheet
================================================================================
