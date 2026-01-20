================================================================================
Dynamic Programming for Embedded Systems
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Introduction to Algorithms (CLRS), Algorithms in a Nutshell
:Focus: Memory-efficient DP for resource-constrained systems

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. Dynamic Programming Overview
================================================================================

1.1 What is Dynamic Programming?
--------------------------------------------------------------------------------

**Dynamic Programming (DP)** is an optimization technique that solves complex
problems by breaking them into simpler subproblems and storing results to
avoid redundant computation.

**Key Characteristics:**

1. **Optimal Substructure:** Optimal solution contains optimal solutions to
   subproblems
2. **Overlapping Subproblems:** Same subproblems are solved multiple times
3. **Memoization or Tabulation:** Store results to avoid recomputation

**DP vs Divide & Conquer:**

- **Divide & Conquer:** Subproblems are independent (e.g., merge sort)
- **Dynamic Programming:** Subproblems overlap (e.g., Fibonacci)

1.2 Two Approaches
--------------------------------------------------------------------------------

**Top-Down (Memoization):**

- Start with original problem
- Recursively solve subproblems
- Cache results in memo table
- Pros: Only solve needed subproblems
- Cons: Recursion overhead, stack usage

**Bottom-Up (Tabulation):**

- Start with smallest subproblems
- Iteratively build up to solution
- Fill table in order
- Pros: No recursion, predictable memory
- Cons: May solve unnecessary subproblems

**Embedded Systems Preference:** Bottom-up (no recursion, predictable resources)

================================================================================
2. Classic DP Problems - Embedded Implementations
================================================================================

2.1 Fibonacci Numbers
--------------------------------------------------------------------------------

**Problem:** Compute F(n) = F(n-1) + F(n-2), F(0)=0, F(1)=1

**Naive Recursive (Exponential Time):**

.. code-block:: c

   // ❌ Bad: O(2^n) time, deep recursion
   int fib_recursive(int n) {
       if (n <= 1) return n;
       return fib_recursive(n - 1) + fib_recursive(n - 2);
   }

**Memoization (Top-Down):**

.. code-block:: c

   #define MAX_N 50
   static int memo[MAX_N];
   static bool computed[MAX_N];
   
   int fib_memo(int n) {
       if (n <= 1) return n;
       
       if (computed[n]) {
           return memo[n];
       }
       
       memo[n] = fib_memo(n - 1) + fib_memo(n - 2);
       computed[n] = true;
       return memo[n];
   }
   
   // Initialize
   void fib_memo_init(void) {
       for (int i = 0; i < MAX_N; i++) {
           computed[i] = false;
       }
   }

**Tabulation (Bottom-Up):**

.. code-block:: c

   // ✅ Best for embedded: O(n) time, O(n) space, no recursion
   int fib_tabulation(int n) {
       if (n <= 1) return n;
       
       int dp[n + 1];
       dp[0] = 0;
       dp[1] = 1;
       
       for (int i = 2; i <= n; i++) {
           dp[i] = dp[i - 1] + dp[i - 2];
       }
       
       return dp[n];
   }

**Space-Optimized (O(1) space):**

.. code-block:: c

   // ✅ Best: O(n) time, O(1) space
   int fib_optimized(int n) {
       if (n <= 1) return n;
       
       int prev2 = 0;  // F(i-2)
       int prev1 = 1;  // F(i-1)
       int current;
       
       for (int i = 2; i <= n; i++) {
           current = prev1 + prev2;
           prev2 = prev1;
           prev1 = current;
       }
       
       return prev1;
   }

2.2 Coin Change Problem
--------------------------------------------------------------------------------

**Problem:** Given coins of denominations and amount, find minimum coins needed.

**Example:** coins = {1, 5, 10, 25}, amount = 37
**Answer:** 4 coins (25 + 10 + 1 + 1)

**Tabulation Approach:**

.. code-block:: c

   #define MAX_AMOUNT 1000
   #define INF 9999
   
   int coin_change(int coins[], int n_coins, int amount) {
       int dp[amount + 1];
       
       // Initialize: 0 coins for amount 0, INF for others
       dp[0] = 0;
       for (int i = 1; i <= amount; i++) {
           dp[i] = INF;
       }
       
       // Fill table
       for (int i = 1; i <= amount; i++) {
           for (int j = 0; j < n_coins; j++) {
               if (coins[j] <= i) {
                   int sub_result = dp[i - coins[j]];
                   if (sub_result != INF && sub_result + 1 < dp[i]) {
                       dp[i] = sub_result + 1;
                   }
               }
           }
       }
       
       return dp[amount] == INF ? -1 : dp[amount];
   }

**Embedded Example - Power State Transitions:**

.. code-block:: c

   // Minimum transitions to reach target power level
   #define MAX_POWER_LEVEL 100
   
   typedef enum {
       POWER_UP_1 = 1,
       POWER_UP_5 = 5,
       POWER_UP_10 = 10,
       POWER_UP_25 = 25
   } power_step_t;
   
   int min_power_transitions(int target_level) {
       int steps[] = {1, 5, 10, 25};
       return coin_change(steps, 4, target_level);
   }

2.3 Longest Common Subsequence (LCS)
--------------------------------------------------------------------------------

**Problem:** Find length of longest subsequence common to two sequences.

**Example:** X = "ABCDGH", Y = "AEDFHR"
**LCS:** "ADH" (length 3)

**Tabulation:**

.. code-block:: c

   #define MAX_SEQ_LEN 128
   
   int lcs_length(const char *X, const char *Y, int m, int n) {
       int dp[m + 1][n + 1];
       
       // Initialize first row and column to 0
       for (int i = 0; i <= m; i++) dp[i][0] = 0;
       for (int j = 0; j <= n; j++) dp[0][j] = 0;
       
       // Fill table
       for (int i = 1; i <= m; i++) {
           for (int j = 1; j <= n; j++) {
               if (X[i - 1] == Y[j - 1]) {
                   dp[i][j] = dp[i - 1][j - 1] + 1;
               } else {
                   dp[i][j] = (dp[i - 1][j] > dp[i][j - 1]) ?
                              dp[i - 1][j] : dp[i][j - 1];
               }
           }
       }
       
       return dp[m][n];
   }

**Space-Optimized (O(n) space):**

.. code-block:: c

   // Only need previous row
   int lcs_length_optimized(const char *X, const char *Y, int m, int n) {
       int prev[n + 1];
       int curr[n + 1];
       
       // Initialize
       for (int j = 0; j <= n; j++) {
           prev[j] = 0;
       }
       
       for (int i = 1; i <= m; i++) {
           curr[0] = 0;
           for (int j = 1; j <= n; j++) {
               if (X[i - 1] == Y[j - 1]) {
                   curr[j] = prev[j - 1] + 1;
               } else {
                   curr[j] = (prev[j] > curr[j - 1]) ? prev[j] : curr[j - 1];
               }
           }
           
           // Swap rows
           for (int j = 0; j <= n; j++) {
               prev[j] = curr[j];
           }
       }
       
       return prev[n];
   }

**Embedded Example - Sensor Data Sequence Matching:**

.. code-block:: c

   #define MAX_SAMPLES 64
   
   typedef struct {
       uint16_t samples[MAX_SAMPLES];
       int count;
   } sensor_sequence_t;
   
   // Find common pattern length between two sensor sequences
   int find_common_pattern(sensor_sequence_t *seq1, sensor_sequence_t *seq2) {
       int dp[seq1->count + 1][seq2->count + 1];
       
       for (int i = 0; i <= seq1->count; i++) dp[i][0] = 0;
       for (int j = 0; j <= seq2->count; j++) dp[0][j] = 0;
       
       for (int i = 1; i <= seq1->count; i++) {
           for (int j = 1; j <= seq2->count; j++) {
               if (seq1->samples[i - 1] == seq2->samples[j - 1]) {
                   dp[i][j] = dp[i - 1][j - 1] + 1;
               } else {
                   dp[i][j] = (dp[i - 1][j] > dp[i][j - 1]) ?
                              dp[i - 1][j] : dp[i][j - 1];
               }
           }
       }
       
       return dp[seq1->count][seq2->count];
   }

2.4 0/1 Knapsack Problem
--------------------------------------------------------------------------------

**Problem:** Given items with weights and values, maximize value without
exceeding capacity.

**Tabulation:**

.. code-block:: c

   typedef struct {
       int weight;
       int value;
   } item_t;
   
   int knapsack(item_t items[], int n, int capacity) {
       int dp[n + 1][capacity + 1];
       
       // Initialize: 0 value with 0 items or 0 capacity
       for (int i = 0; i <= n; i++) dp[i][0] = 0;
       for (int w = 0; w <= capacity; w++) dp[0][w] = 0;
       
       // Fill table
       for (int i = 1; i <= n; i++) {
           for (int w = 1; w <= capacity; w++) {
               if (items[i - 1].weight <= w) {
                   // Can include item i
                   int include = items[i - 1].value + 
                                dp[i - 1][w - items[i - 1].weight];
                   int exclude = dp[i - 1][w];
                   dp[i][w] = (include > exclude) ? include : exclude;
               } else {
                   // Can't include item i
                   dp[i][w] = dp[i - 1][w];
               }
           }
       }
       
       return dp[n][capacity];
   }

**Space-Optimized (1D array):**

.. code-block:: c

   int knapsack_optimized(item_t items[], int n, int capacity) {
       int dp[capacity + 1];
       
       // Initialize
       for (int w = 0; w <= capacity; w++) {
           dp[w] = 0;
       }
       
       // Process each item
       for (int i = 0; i < n; i++) {
           // Traverse backwards to avoid using updated values
           for (int w = capacity; w >= items[i].weight; w--) {
               int include = items[i].value + dp[w - items[i].weight];
               if (include > dp[w]) {
                   dp[w] = include;
               }
           }
       }
       
       return dp[capacity];
   }

**Embedded Example - Task Scheduling with Resource Constraints:**

.. code-block:: c

   #define MAX_TASKS 16
   #define MAX_RAM 256  // KB
   
   typedef struct {
       uint8_t ram_required;  // KB
       uint8_t priority;      // Value
       char name[16];
   } task_info_t;
   
   task_info_t tasks[MAX_TASKS];
   
   // Select tasks to maximize priority within RAM budget
   int schedule_tasks_optimal(task_info_t tasks[], int n_tasks, int ram_budget) {
       item_t items[MAX_TASKS];
       
       // Convert to knapsack items
       for (int i = 0; i < n_tasks; i++) {
           items[i].weight = tasks[i].ram_required;
           items[i].value = tasks[i].priority;
       }
       
       return knapsack_optimized(items, n_tasks, ram_budget);
   }

2.5 Edit Distance (Levenshtein Distance)
--------------------------------------------------------------------------------

**Problem:** Minimum operations (insert, delete, replace) to transform one
string to another.

**Tabulation:**

.. code-block:: c

   #define MAX_STRING_LEN 64
   
   int min3(int a, int b, int c) {
       int min = a;
       if (b < min) min = b;
       if (c < min) min = c;
       return min;
   }
   
   int edit_distance(const char *str1, const char *str2, int m, int n) {
       int dp[m + 1][n + 1];
       
       // Initialize: i inserts or j deletes
       for (int i = 0; i <= m; i++) dp[i][0] = i;
       for (int j = 0; j <= n; j++) dp[0][j] = j;
       
       // Fill table
       for (int i = 1; i <= m; i++) {
           for (int j = 1; j <= n; j++) {
               if (str1[i - 1] == str2[j - 1]) {
                   dp[i][j] = dp[i - 1][j - 1];  // No operation needed
               } else {
                   dp[i][j] = 1 + min3(
                       dp[i - 1][j],      // Delete
                       dp[i][j - 1],      // Insert
                       dp[i - 1][j - 1]   // Replace
                   );
               }
           }
       }
       
       return dp[m][n];
   }

**Embedded Example - Command String Correction:**

.. code-block:: c

   #define MAX_COMMANDS 32
   
   const char *valid_commands[] = {
       "START", "STOP", "RESET", "CONFIG", "STATUS"
   };
   
   // Find closest valid command to user input
   const char* find_closest_command(const char *input) {
       int min_distance = MAX_STRING_LEN;
       const char *closest = NULL;
       
       for (int i = 0; i < 5; i++) {
           int dist = edit_distance(input, valid_commands[i],
                                   strlen(input), strlen(valid_commands[i]));
           if (dist < min_distance) {
               min_distance = dist;
               closest = valid_commands[i];
           }
       }
       
       return closest;
   }

================================================================================
3. Matrix Chain Multiplication
================================================================================

**Problem:** Find optimal parenthesization to minimize scalar multiplications.

**Tabulation:**

.. code-block:: c

   #define MAX_MATRICES 10
   #define INF 999999
   
   int matrix_chain_order(int dims[], int n) {
       int dp[n][n];
       
       // Cost is 0 for single matrix
       for (int i = 1; i < n; i++) {
           dp[i][i] = 0;
       }
       
       // len is chain length
       for (int len = 2; len < n; len++) {
           for (int i = 1; i < n - len + 1; i++) {
               int j = i + len - 1;
               dp[i][j] = INF;
               
               for (int k = i; k < j; k++) {
                   int cost = dp[i][k] + dp[k + 1][j] +
                             dims[i - 1] * dims[k] * dims[j];
                   if (cost < dp[i][j]) {
                       dp[i][j] = cost;
                   }
               }
           }
       }
       
       return dp[1][n - 1];
   }

================================================================================
4. Longest Increasing Subsequence (LIS)
================================================================================

**Problem:** Find length of longest strictly increasing subsequence.

**O(n²) DP Solution:**

.. code-block:: c

   int lis_length(int arr[], int n) {
       int dp[n];
       
       // Each element is LIS of length 1
       for (int i = 0; i < n; i++) {
           dp[i] = 1;
       }
       
       // Compute LIS ending at each position
       for (int i = 1; i < n; i++) {
           for (int j = 0; j < i; j++) {
               if (arr[j] < arr[i] && dp[j] + 1 > dp[i]) {
                   dp[i] = dp[j] + 1;
               }
           }
       }
       
       // Find maximum
       int max_len = 1;
       for (int i = 0; i < n; i++) {
           if (dp[i] > max_len) {
               max_len = dp[i];
           }
       }
       
       return max_len;
   }

**Embedded Example - Temperature Trend Analysis:**

.. code-block:: c

   #define MAX_TEMP_SAMPLES 128
   
   int16_t temperature_log[MAX_TEMP_SAMPLES];
   
   // Find longest warming trend
   int longest_warming_period(int16_t temps[], int n) {
       return lis_length((int*)temps, n);
   }

================================================================================
5. Subset Sum Problem
================================================================================

**Problem:** Determine if subset of array sums to target.

**Tabulation:**

.. code-block:: c

   bool subset_sum(int set[], int n, int target) {
       bool dp[n + 1][target + 1];
       
       // Sum 0 is always possible (empty subset)
       for (int i = 0; i <= n; i++) {
           dp[i][0] = true;
       }
       
       // No elements, non-zero sum impossible
       for (int j = 1; j <= target; j++) {
           dp[0][j] = false;
       }
       
       // Fill table
       for (int i = 1; i <= n; i++) {
           for (int j = 1; j <= target; j++) {
               if (set[i - 1] <= j) {
                   dp[i][j] = dp[i - 1][j] || dp[i - 1][j - set[i - 1]];
               } else {
                   dp[i][j] = dp[i - 1][j];
               }
           }
       }
       
       return dp[n][target];
   }

**Space-Optimized:**

.. code-block:: c

   bool subset_sum_optimized(int set[], int n, int target) {
       bool dp[target + 1];
       
       dp[0] = true;
       for (int i = 1; i <= target; i++) {
           dp[i] = false;
       }
       
       for (int i = 0; i < n; i++) {
           for (int j = target; j >= set[i]; j--) {
               dp[j] = dp[j] || dp[j - set[i]];
           }
       }
       
       return dp[target];
   }

================================================================================
6. Memory Optimization Techniques
================================================================================

6.1 Space Optimization Patterns
--------------------------------------------------------------------------------

**Pattern 1: Use Only Previous Row/Column**

.. code-block:: c

   // Instead of dp[n][m], use dp[2][m] or dp[m]
   // Example: LCS, Edit Distance
   
   int prev[MAX_COL];
   int curr[MAX_COL];
   
   for (int i = 0; i < n; i++) {
       for (int j = 0; j < m; j++) {
           curr[j] = compute(prev[j], curr[j-1], prev[j-1]);
       }
       swap(prev, curr);
   }

**Pattern 2: Reverse Traversal for 1D**

.. code-block:: c

   // Knapsack pattern - traverse backwards
   for (int i = 0; i < n; i++) {
       for (int w = capacity; w >= weight[i]; w--) {
           dp[w] = max(dp[w], dp[w - weight[i]] + value[i]);
       }
   }

**Pattern 3: Rolling Array**

.. code-block:: c

   #define BUF_SIZE 3
   int dp[BUF_SIZE][MAX_COL];
   
   for (int i = 0; i < n; i++) {
       int curr_row = i % BUF_SIZE;
       int prev_row = (i - 1 + BUF_SIZE) % BUF_SIZE;
       // Use curr_row and prev_row indices
   }

6.2 Static vs Stack Allocation
--------------------------------------------------------------------------------

.. code-block:: c

   // ❌ Bad for embedded: VLA on stack
   void bad_dp(int n, int m) {
       int dp[n][m];  // Variable-length array
       // ...
   }
   
   // ✅ Good: Static with maximum size
   #define MAX_N 100
   #define MAX_M 100
   
   void good_dp(int n, int m) {
       static int dp[MAX_N][MAX_M];  // Static or global
       // ...
   }
   
   // ✅ Alternative: 1D array
   void better_dp(int n, int m) {
       static int dp[MAX_M];  // Much smaller
       // ...
   }

================================================================================
7. DP Patterns Summary
================================================================================

Common DP Problem Patterns
--------------------------------------------------------------------------------

+-------------------------+-------------------+-------------------------+
| Pattern                 | Example           | Recurrence              |
+=========================+===================+=========================+
| Linear DP               | Fibonacci, LIS    | dp[i] = f(dp[i-1])      |
+-------------------------+-------------------+-------------------------+
| 2D Grid DP              | LCS, Edit Dist    | dp[i][j] = f(dp[i-1][j])|
+-------------------------+-------------------+-------------------------+
| Knapsack Variant        | 0/1, Subset Sum   | dp[w] = max(with/out)   |
+-------------------------+-------------------+-------------------------+
| Interval DP             | Matrix Chain      | dp[i][j] = min over k   |
+-------------------------+-------------------+-------------------------+
| State Machine DP        | Stock Trading     | dp[i][state] = ...      |
+-------------------------+-------------------+-------------------------+

================================================================================
8. Embedded Applications
================================================================================

8.1 Battery Life Optimization
--------------------------------------------------------------------------------

.. code-block:: c

   #define MAX_TIME_SLOTS 24  // Hours
   #define MAX_TASKS 10
   
   typedef struct {
       uint8_t duration;  // Hours
       uint8_t power_cost;  // mAh
       uint8_t priority;
   } battery_task_t;
   
   // Maximize priority within battery budget
   int optimize_battery_schedule(battery_task_t tasks[], int n, 
                                 int battery_capacity) {
       item_t items[MAX_TASKS];
       
       for (int i = 0; i < n; i++) {
           items[i].weight = tasks[i].power_cost;
           items[i].value = tasks[i].priority;
       }
       
       return knapsack_optimized(items, n, battery_capacity);
   }

8.2 Network Packet Scheduling
--------------------------------------------------------------------------------

.. code-block:: c

   #define MAX_PACKETS 64
   
   typedef struct {
       uint16_t size;      // Bytes
       uint8_t priority;
       uint32_t deadline;
   } packet_t;
   
   // Schedule packets to maximize priority within bandwidth
   int schedule_packets(packet_t packets[], int n, int bandwidth) {
       item_t items[MAX_PACKETS];
       
       for (int i = 0; i < n; i++) {
           items[i].weight = packets[i].size;
           items[i].value = packets[i].priority;
       }
       
       return knapsack_optimized(items, n, bandwidth);
   }

================================================================================
9. Performance Tips
================================================================================

**Algorithm Selection:**

1. For small inputs (n < 20): Recursion OK if stack permits
2. For medium inputs (20 < n < 1000): Tabulation preferred
3. For large inputs (n > 1000): Space-optimized tabulation required

**Memory Management:**

1. Use static arrays with MAX_SIZE constants
2. Optimize to 1D when possible
3. Consider rolling arrays for large 2D tables
4. Profile actual memory usage

**Code Size:**

1. Implement only needed DP algorithms
2. Use iterative (bottom-up) to save stack
3. Share memo tables across similar problems

**Real-Time Considerations:**

1. Precompute DP tables at initialization
2. Use lookup tables for frequently accessed values
3. Bound maximum problem size
4. Consider approximation algorithms for hard DP problems

================================================================================
10. Complexity Cheat Sheet
================================================================================

+-------------------------+-------------+-------------+-------------------+
| Problem                 | Time        | Space       | Space Optimized   |
+=========================+=============+=============+===================+
| Fibonacci               | O(n)        | O(n)        | O(1)              |
+-------------------------+-------------+-------------+-------------------+
| Coin Change             | O(n × m)    | O(n)        | O(n)              |
+-------------------------+-------------+-------------+-------------------+
| LCS                     | O(n × m)    | O(n × m)    | O(min(n, m))      |
+-------------------------+-------------+-------------+-------------------+
| 0/1 Knapsack            | O(n × W)    | O(n × W)    | O(W)              |
+-------------------------+-------------+-------------+-------------------+
| Edit Distance           | O(n × m)    | O(n × m)    | O(min(n, m))      |
+-------------------------+-------------+-------------+-------------------+
| Matrix Chain            | O(n³)       | O(n²)       | O(n²)             |
+-------------------------+-------------+-------------+-------------------+
| LIS                     | O(n²)       | O(n)        | O(n)              |
+-------------------------+-------------+-------------+-------------------+
| Subset Sum              | O(n × sum)  | O(n × sum)  | O(sum)            |
+-------------------------+-------------+-------------+-------------------+

Where n, m = input sizes, W = capacity, sum = target sum

================================================================================
End of Dynamic Programming Cheatsheet
================================================================================
