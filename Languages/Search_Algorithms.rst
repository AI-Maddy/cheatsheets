🔍 Search Algorithms for Embedded Systems
==========================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

🎯 TL;DR - Quick Reference
===========================

**Search Algorithm Selection Guide:**

+---------------------+-------------+---------------+---------------+----------------------------------+
| Algorithm           | Time (Avg)  | Time (Worst)  | Space         | Best Use Case                    |
+=====================+=============+===============+===============+==================================+
| Sequential Search   | O(n)        | O(n)          | O(1)          | Unsorted data, small arrays      |
+---------------------+-------------+---------------+---------------+----------------------------------+
| Binary Search       | O(log n)    | O(log n)      | O(1) iter     | Sorted arrays, lookups           |
+---------------------+-------------+---------------+---------------+----------------------------------+
| Hash Table          | O(1)        | O(n)          | O(n)          | Fast lookups, sufficient RAM     |
+---------------------+-------------+---------------+---------------+----------------------------------+
| Binary Search Tree  | O(log n)    | O(n)          | O(n)          | Dynamic sorted data              |
+---------------------+-------------+---------------+---------------+----------------------------------+
| Interpolation       | O(log log n)| O(n)          | O(1)          | Uniformly distributed sorted data|
+---------------------+-------------+---------------+---------------+----------------------------------+

**Embedded Systems Quick Picks:**

* **Flash lookup tables:** Binary search (ROM-friendly, no RAM)
* **Config parameters:** Hash table with fixed size
* **Sensor calibration:** Interpolation search
* **Protocol parsing:** Hash table for commands
* **Device registry:** Binary search tree

📚 1. Sequential Search (Linear Search)
========================================

Overview
--------
Simplest search - check each element until found or end reached.

**When to Use:**
* Unsorted data
* Very small arrays (n < 10-20)
* RAM-constrained (O(1) space)
* One-time searches

Implementation
--------------

.. code-block:: c

    // Basic sequential search
    int sequential_search(const int arr[], int n, int target) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == target) {
                return i;  // Found at index i
            }
        }
        return -1;  // Not found
    }

    // Sequential search with early termination (sorted arrays)
    int sequential_search_sorted(const int arr[], int n, int target) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == target) return i;
            if (arr[i] > target) return -1;  // Stop early
        }
        return -1;
    }

    // Sentinel search (optimized - one less comparison per iteration)
    int sentinel_search(int arr[], int n, int target) {
        int last = arr[n - 1];
        arr[n - 1] = target;  // Place sentinel
        
        int i = 0;
        while (arr[i] != target) {
            i++;
        }
        
        arr[n - 1] = last;  // Restore original
        
        if (i < n - 1 || arr[n - 1] == target) {
            return i;
        }
        return -1;
    }

Embedded Use Case
-----------------

.. code-block:: c

    // Search command in protocol message
    typedef struct {
        uint8_t cmd_id;
        void (*handler)(uint8_t* data);
    } Command;
    
    Command commands[] = {
        {0x01, handle_read},
        {0x02, handle_write},
        {0x03, handle_reset}
    };
    
    void process_command(uint8_t cmd_id, uint8_t* data) {
        for (int i = 0; i < 3; i++) {
            if (commands[i].cmd_id == cmd_id) {
                commands[i].handler(data);
                return;
            }
        }
        // Unknown command
        send_error(CMD_UNKNOWN);
    }

📊 2. Binary Search
===================

Overview
--------
Efficient search for **sorted** arrays - divide and conquer approach.

**Requirements:**
* Data must be sorted
* Random access (arrays, not linked lists)

**When to Use:**
* Lookup tables in flash/ROM
* Calibration tables
* Large sorted datasets
* Configuration parameters

Iterative Implementation
------------------------

.. code-block:: c

    // Standard iterative binary search
    int binary_search(const int arr[], int n, int target) {
        int left = 0;
        int right = n - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;  // Avoid overflow
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;  // Not found
    }

    // Binary search - find insertion point
    int binary_search_insert_point(const int arr[], int n, int target) {
        int left = 0;
        int right = n;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return left;  // Insertion index
    }

Recursive Implementation
------------------------

.. code-block:: c

    // Recursive binary search (uses stack - careful in embedded!)
    int binary_search_recursive(const int arr[], int left, int right, int target) {
        if (left > right) {
            return -1;
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return binary_search_recursive(arr, mid + 1, right, target);
        } else {
            return binary_search_recursive(arr, left, mid - 1, target);
        }
    }

Embedded Applications
---------------------

.. code-block:: c

    // Temperature calibration lookup (stored in flash)
    const int16_t ADC_VALUES[] __attribute__((section(".rodata"))) = {
        0, 100, 205, 315, 430, 550, 675, 805, 940, 1080, 1225, 1375, 
        1530, 1690, 1855, 2025, 2200, 2380, 2565, 2755, 2950, 3150, 
        3355, 3565, 3780, 4000
    };
    
    const int8_t TEMP_VALUES[] = {
        -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15,
        20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85
    };
    
    #define CALIB_SIZE (sizeof(ADC_VALUES) / sizeof(ADC_VALUES[0]))
    
    int8_t adc_to_temperature(int16_t adc_value) {
        int idx = binary_search(ADC_VALUES, CALIB_SIZE, adc_value);
        
        if (idx >= 0) {
            return TEMP_VALUES[idx];  // Exact match
        }
        
        // Linear interpolation between points
        int insert_idx = binary_search_insert_point(ADC_VALUES, CALIB_SIZE, adc_value);
        
        if (insert_idx == 0) return TEMP_VALUES[0];
        if (insert_idx >= CALIB_SIZE) return TEMP_VALUES[CALIB_SIZE - 1];
        
        // Interpolate
        int16_t adc_low = ADC_VALUES[insert_idx - 1];
        int16_t adc_high = ADC_VALUES[insert_idx];
        int8_t temp_low = TEMP_VALUES[insert_idx - 1];
        int8_t temp_high = TEMP_VALUES[insert_idx];
        
        int32_t temp = temp_low + ((int32_t)(adc_value - adc_low) * (temp_high - temp_low)) / (adc_high - adc_low);
        
        return (int8_t)temp;
    }

📈 3. Interpolation Search
===========================

Overview
--------
Improved binary search for **uniformly distributed** sorted data.
Uses value-based positioning instead of middle point.

**Time Complexity:**
* Best/Average: O(log log n)
* Worst: O(n) (non-uniform data)

Implementation
--------------

.. code-block:: c

    int interpolation_search(const int arr[], int n, int target) {
        int left = 0;
        int right = n - 1;
        
        while (left <= right && target >= arr[left] && target <= arr[right]) {
            if (left == right) {
                if (arr[left] == target) return left;
                return -1;
            }
            
            // Interpolation formula
            int pos = left + ((int64_t)(right - left) * (target - arr[left])) / 
                             (arr[right] - arr[left]);
            
            if (arr[pos] == target) {
                return pos;
            } else if (arr[pos] < target) {
                left = pos + 1;
            } else {
                right = pos - 1;
            }
        }
        
        return -1;
    }

Use Case
--------

.. code-block:: c

    // Frequency-to-channel lookup for radio tuner
    // Frequencies are uniformly distributed
    const uint32_t FREQ_TABLE[] = {
        88000000, 88500000, 89000000, 89500000, 90000000,
        90500000, 91000000, 91500000, 92000000, 92500000,
        // ... up to 108000000 (500 kHz steps)
    };
    
    int find_channel(uint32_t frequency) {
        return interpolation_search(FREQ_TABLE, FREQ_COUNT, frequency);
    }

🗂️ 4. Hash-Based Search
==========================

Overview
--------
O(1) average-case lookups using hash function to index directly into table.

**When to Use:**
* Fast lookups required
* Sufficient RAM available
* Key uniqueness guaranteed (or collision handling available)

Hash Functions
--------------

.. code-block:: c

    // Simple modulo hash (for integers)
    uint32_t hash_modulo(uint32_t key, uint32_t table_size) {
        return key % table_size;
    }
    
    // Multiplicative hash
    uint32_t hash_multiplicative(uint32_t key, uint32_t table_size) {
        const uint32_t A = 2654435769u;  // (sqrt(5) - 1) * 2^32
        return (key * A) >> (32 - __builtin_ctz(table_size));
    }
    
    // DJB2 hash (for strings)
    uint32_t hash_djb2(const char* str) {
        uint32_t hash = 5381;
        int c;
        
        while ((c = *str++)) {
            hash = ((hash << 5) + hash) + c;  // hash * 33 + c
        }
        
        return hash;
    }
    
    // FNV-1a hash (fast, good distribution)
    uint32_t hash_fnv1a(const void* data, size_t len) {
        const uint8_t* bytes = (const uint8_t*)data;
        uint32_t hash = 2166136261u;
        
        for (size_t i = 0; i < len; i++) {
            hash ^= bytes[i];
            hash *= 16777619u;
        }
        
        return hash;
    }

Fixed-Size Hash Table (Embedded)
---------------------------------

.. code-block:: c

    #define HASH_TABLE_SIZE 64
    
    typedef struct {
        uint32_t key;
        void* value;
        bool occupied;
    } HashEntry;
    
    typedef struct {
        HashEntry entries[HASH_TABLE_SIZE];
    } HashTable;
    
    void hash_table_init(HashTable* table) {
        memset(table, 0, sizeof(HashTable));
    }
    
    // Linear probing collision resolution
    bool hash_table_insert(HashTable* table, uint32_t key, void* value) {
        uint32_t index = hash_modulo(key, HASH_TABLE_SIZE);
        uint32_t start_index = index;
        
        do {
            if (!table->entries[index].occupied) {
                table->entries[index].key = key;
                table->entries[index].value = value;
                table->entries[index].occupied = true;
                return true;
            }
            
            if (table->entries[index].key == key) {
                // Update existing
                table->entries[index].value = value;
                return true;
            }
            
            // Linear probe
            index = (index + 1) % HASH_TABLE_SIZE;
            
        } while (index != start_index);
        
        return false;  // Table full
    }
    
    void* hash_table_search(const HashTable* table, uint32_t key) {
        uint32_t index = hash_modulo(key, HASH_TABLE_SIZE);
        uint32_t start_index = index;
        
        do {
            if (!table->entries[index].occupied) {
                return NULL;  // Not found
            }
            
            if (table->entries[index].key == key) {
                return table->entries[index].value;
            }
            
            index = (index + 1) % HASH_TABLE_SIZE;
            
        } while (index != start_index);
        
        return NULL;
    }

Practical Embedded Example
---------------------------

.. code-block:: c

    // Configuration parameter storage
    typedef struct {
        const char* name;
        uint32_t value;
    } ConfigParam;
    
    #define CONFIG_HASH_SIZE 32
    
    typedef struct {
        const char* key;
        uint32_t value;
        bool valid;
    } ConfigEntry;
    
    ConfigEntry config_table[CONFIG_HASH_SIZE];
    
    void config_set(const char* key, uint32_t value) {
        uint32_t hash = hash_djb2(key) % CONFIG_HASH_SIZE;
        uint32_t index = hash;
        
        for (int i = 0; i < CONFIG_HASH_SIZE; i++) {
            if (!config_table[index].valid || 
                strcmp(config_table[index].key, key) == 0) {
                config_table[index].key = key;
                config_table[index].value = value;
                config_table[index].valid = true;
                return;
            }
            index = (index + 1) % CONFIG_HASH_SIZE;
        }
    }
    
    uint32_t config_get(const char* key, uint32_t default_val) {
        uint32_t hash = hash_djb2(key) % CONFIG_HASH_SIZE;
        uint32_t index = hash;
        
        for (int i = 0; i < CONFIG_HASH_SIZE; i++) {
            if (!config_table[index].valid) {
                return default_val;
            }
            if (strcmp(config_table[index].key, key) == 0) {
                return config_table[index].value;
            }
            index = (index + 1) % CONFIG_HASH_SIZE;
        }
        
        return default_val;
    }

🌳 5. Binary Search Tree (BST)
===============================

Overview
--------
Dynamic sorted data structure with O(log n) operations (average case).

**When to Use:**
* Dynamic insertions/deletions
* Need sorted iteration
* Range queries

Implementation
--------------

.. code-block:: c

    typedef struct TreeNode {
        int key;
        void* data;
        struct TreeNode* left;
        struct TreeNode* right;
    } TreeNode;
    
    TreeNode* bst_search(TreeNode* root, int key) {
        if (root == NULL || root->key == key) {
            return root;
        }
        
        if (key < root->key) {
            return bst_search(root->left, key);
        } else {
            return bst_search(root->right, key);
        }
    }
    
    TreeNode* bst_insert(TreeNode* root, int key, void* data) {
        if (root == NULL) {
            TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
            node->key = key;
            node->data = data;
            node->left = node->right = NULL;
            return node;
        }
        
        if (key < root->key) {
            root->left = bst_insert(root->left, key, data);
        } else if (key > root->key) {
            root->right = bst_insert(root->right, key, data);
        } else {
            // Update existing
            root->data = data;
        }
        
        return root;
    }
    
    // In-order traversal (sorted)
    void bst_inorder(TreeNode* root, void (*visit)(TreeNode*)) {
        if (root == NULL) return;
        
        bst_inorder(root->left, visit);
        visit(root);
        bst_inorder(root->right, visit);
    }

Memory Pool BST (No malloc)
----------------------------

.. code-block:: c

    #define BST_POOL_SIZE 100
    
    typedef struct {
        TreeNode nodes[BST_POOL_SIZE];
        bool used[BST_POOL_SIZE];
        int next_free;
    } BSTPool;
    
    static BSTPool pool;
    
    void bst_pool_init(void) {
        memset(&pool, 0, sizeof(pool));
        pool.next_free = 0;
    }
    
    TreeNode* bst_alloc_node(int key, void* data) {
        for (int i = 0; i < BST_POOL_SIZE; i++) {
            int idx = (pool.next_free + i) % BST_POOL_SIZE;
            if (!pool.used[idx]) {
                pool.used[idx] = true;
                pool.next_free = (idx + 1) % BST_POOL_SIZE;
                
                TreeNode* node = &pool.nodes[idx];
                node->key = key;
                node->data = data;
                node->left = node->right = NULL;
                return node;
            }
        }
        return NULL;  // Pool exhausted
    }
    
    void bst_free_node(TreeNode* node) {
        if (node >= pool.nodes && node < pool.nodes + BST_POOL_SIZE) {
            int idx = node - pool.nodes;
            pool.used[idx] = false;
        }
    }

📋 6. Comparison & Selection Guide
===================================

Algorithm Selection Matrix
---------------------------

+------------------+--------------+--------------+----------------+---------------------+
| Criteria         | Sequential   | Binary       | Hash Table     | BST                 |
+==================+==============+==============+================+=====================+
| Data Sorted?     | No required  | **Required** | No required    | Auto-sorted         |
+------------------+--------------+--------------+----------------+---------------------+
| RAM Usage        | Minimal      | Minimal      | High           | Medium              |
+------------------+--------------+--------------+----------------+---------------------+
| ROM-friendly?    | Yes          | **Yes**      | No             | No                  |
+------------------+--------------+--------------+----------------+---------------------+
| Dynamic inserts? | Easy         | Hard         | **Easy**       | **Easy**            |
+------------------+--------------+--------------+----------------+---------------------+
| Worst-case time  | O(n)         | **O(log n)** | O(n)           | O(n)                |
+------------------+--------------+--------------+----------------+---------------------+
| Best for         | Small arrays | Lookups      | Fast access    | Dynamic sorted data |
+------------------+--------------+--------------+----------------+---------------------+

Embedded Systems Recommendations
---------------------------------

**Microcontroller with 32KB RAM:**
* Use binary search for flash lookups
* Use hash tables (fixed size) for configuration
* Avoid BST unless dynamic sorted data needed

**Microcontroller with 256KB+ RAM:**
* Hash tables for command parsing
* BST for event queues with priorities
* Binary search for calibration tables

**Safety-Critical Systems:**
* Prefer binary search (deterministic, no dynamic allocation)
* Use static hash tables with overflow handling
* Avoid recursive algorithms (stack risk)

🛠️ Performance Optimization Tips
===================================

1. Cache Optimization
---------------------

.. code-block:: c

    // BAD: Poor cache locality
    typedef struct {
        int key;
        char padding[60];  // Cache line pollution
    } BadEntry;
    
    // GOOD: Pack data tightly
    typedef struct {
        int key;
        int value;
    } GoodEntry;

2. Branch Prediction
--------------------

.. code-block:: c

    // Help branch predictor with likely/unlikely
    #define likely(x)   __builtin_expect(!!(x), 1)
    #define unlikely(x) __builtin_expect(!!(x), 0)
    
    int search_optimized(const int arr[], int n, int target) {
        for (int i = 0; i < n; i++) {
            if (unlikely(arr[i] == target)) {
                return i;
            }
        }
        return -1;
    }

3. SIMD for Parallel Search
----------------------------

.. code-block:: c

    // ARM NEON example - search for byte in array
    #include <arm_neon.h>
    
    int find_byte_simd(const uint8_t* data, size_t len, uint8_t target) {
        uint8x16_t target_vec = vdupq_n_u8(target);
        size_t i;
        
        for (i = 0; i + 16 <= len; i += 16) {
            uint8x16_t data_vec = vld1q_u8(&data[i]);
            uint8x16_t cmp = vceqq_u8(data_vec, target_vec);
            
            if (vmaxvq_u8(cmp) != 0) {
                // Found match in this chunk
                for (int j = 0; j < 16; j++) {
                    if (data[i + j] == target) {
                        return i + j;
                    }
                }
            }
        }
        
        // Check remaining bytes
        for (; i < len; i++) {
            if (data[i] == target) return i;
        }
        
        return -1;
    }

📚 References
=============

* Algorithms in a Nutshell (O'Reilly) - Chapters 4-5
* Introduction to Algorithms (CLRS) - Hash tables and search trees
* Embedded C coding practices for search optimization

🎓 Key Takeaways
================

1. **Binary search** is king for sorted flash/ROM lookups
2. **Hash tables** excel when RAM available and speed critical
3. **Sequential search** perfectly fine for small arrays (n < 20)
4. **Always profile** - theoretical complexity != real performance
5. **Static allocation** preferred in embedded (avoid malloc)
6. **Cache locality** matters more than algorithm choice for small n
7. **Interpolation search** only helps with uniform distributions
8. **BST** useful for dynamic sorted data, but beware fragmentation

==========================================
✅ Completion Checklist
==========================================

- [x] Sequential search implementations
- [x] Binary search (iterative and recursive)
- [x] Interpolation search
- [x] Hash table with collision handling
- [x] Binary search tree
- [x] Memory pool alternatives to malloc
- [x] Embedded real-world examples
- [x] Performance optimization tips
- [x] Algorithm selection guide

==========================================
