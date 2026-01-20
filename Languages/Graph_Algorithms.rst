📊 Graph Algorithms for Embedded Systems
==========================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

🎯 TL;DR - Quick Reference
===========================

**Graph Algorithm Selection Guide:**

+----------------------+-------------+---------------+---------------+------------------------------+
| Algorithm            | Time        | Space         | Use Case      | Embedded Application         |
+======================+=============+===============+===============+==============================+
| BFS                  | O(V + E)    | O(V)          | Shortest path | Task scheduling, routing     |
+----------------------+-------------+---------------+---------------+------------------------------+
| DFS                  | O(V + E)    | O(V)          | Traversal     | Dependency resolution        |
+----------------------+-------------+---------------+---------------+------------------------------+
| Dijkstra             | O(V²)       | O(V)          | Weighted path | Network routing, navigation  |
+----------------------+-------------+---------------+---------------+------------------------------+
| Topological Sort     | O(V + E)    | O(V)          | Ordering      | Build systems, task ordering |
+----------------------+-------------+---------------+---------------+------------------------------+
| Kruskal's MST        | O(E log E)  | O(V)          | Min spanning  | Sensor network optimization  |
+----------------------+-------------+---------------+---------------+------------------------------+
| Floyd-Warshall       | O(V³)       | O(V²)         | All pairs     | Reachability matrix          |
+----------------------+-------------+---------------+---------------+------------------------------+

**Common Embedded Uses:**

* **Task scheduling:** Topological sort for dependency graphs
* **Network routing:** Dijkstra for shortest path
* **State machines:** DFS for state reachability
* **Sensor networks:** MST for optimal connectivity
* **Resource allocation:** Graph coloring

📚 1. Graph Representations
============================

Adjacency Matrix
----------------
**Best for:** Dense graphs, fast edge lookup, fixed size

.. code-block:: c

    #define MAX_NODES 16
    
    typedef struct {
        int num_nodes;
        bool adj_matrix[MAX_NODES][MAX_NODES];
    } GraphMatrix;
    
    void graph_matrix_init(GraphMatrix* g, int num_nodes) {
        g->num_nodes = num_nodes;
        memset(g->adj_matrix, 0, sizeof(g->adj_matrix));
    }
    
    void graph_add_edge(GraphMatrix* g, int u, int v) {
        g->adj_matrix[u][v] = true;
        // For undirected: g->adj_matrix[v][u] = true;
    }
    
    bool graph_has_edge(const GraphMatrix* g, int u, int v) {
        return g->adj_matrix[u][v];
    }

Adjacency List
--------------
**Best for:** Sparse graphs, memory efficiency, dynamic graphs

.. code-block:: c

    #define MAX_NODES 32
    #define MAX_NEIGHBORS 8
    
    typedef struct {
        int neighbors[MAX_NEIGHBORS];
        int weights[MAX_NEIGHBORS];  // For weighted graphs
        int count;
    } AdjList;
    
    typedef struct {
        int num_nodes;
        AdjList lists[MAX_NODES];
    } GraphList;
    
    void graph_list_init(GraphList* g, int num_nodes) {
        g->num_nodes = num_nodes;
        for (int i = 0; i < num_nodes; i++) {
            g->lists[i].count = 0;
        }
    }
    
    bool graph_list_add_edge(GraphList* g, int u, int v, int weight) {
        if (g->lists[u].count >= MAX_NEIGHBORS) {
            return false;  // Full
        }
        
        AdjList* list = &g->lists[u];
        list->neighbors[list->count] = v;
        list->weights[list->count] = weight;
        list->count++;
        return true;
    }

🔍 2. Breadth-First Search (BFS)
==================================

Overview
--------
Level-by-level graph traversal, shortest path in unweighted graphs.

**Applications:**
* Shortest path finding
* Level-order traversal
* Connected component detection
* Network broadcasting

Implementation
--------------

.. code-block:: c

    #include <stdbool.h>
    #include <string.h>
    
    #define QUEUE_SIZE 64
    
    typedef struct {
        int data[QUEUE_SIZE];
        int front, rear;
    } Queue;
    
    void queue_init(Queue* q) {
        q->front = q->rear = 0;
    }
    
    bool queue_enqueue(Queue* q, int value) {
        int next = (q->rear + 1) % QUEUE_SIZE;
        if (next == q->front) return false;  // Full
        q->data[q->rear] = value;
        q->rear = next;
        return true;
    }
    
    bool queue_dequeue(Queue* q, int* value) {
        if (q->front == q->rear) return false;  // Empty
        *value = q->data[q->front];
        q->front = (q->front + 1) % QUEUE_SIZE;
        return true;
    }
    
    bool queue_is_empty(const Queue* q) {
        return q->front == q->rear;
    }
    
    // BFS traversal
    void bfs(const GraphList* g, int start, void (*visit)(int node)) {
        bool visited[MAX_NODES] = {false};
        Queue q;
        queue_init(&q);
        
        visited[start] = true;
        queue_enqueue(&q, start);
        
        while (!queue_is_empty(&q)) {
            int current;
            queue_dequeue(&q, &current);
            visit(current);
            
            const AdjList* list = &g->lists[current];
            for (int i = 0; i < list->count; i++) {
                int neighbor = list->neighbors[i];
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue_enqueue(&q, neighbor);
                }
            }
        }
    }
    
    // BFS shortest path
    int bfs_shortest_path(const GraphList* g, int start, int target, int* path) {
        bool visited[MAX_NODES] = {false};
        int parent[MAX_NODES];
        Queue q;
        queue_init(&q);
        
        for (int i = 0; i < MAX_NODES; i++) {
            parent[i] = -1;
        }
        
        visited[start] = true;
        queue_enqueue(&q, start);
        
        while (!queue_is_empty(&q)) {
            int current;
            queue_dequeue(&q, &current);
            
            if (current == target) {
                // Reconstruct path
                int length = 0;
                int node = target;
                while (node != -1) {
                    path[length++] = node;
                    node = parent[node];
                }
                
                // Reverse path
                for (int i = 0; i < length / 2; i++) {
                    int temp = path[i];
                    path[i] = path[length - 1 - i];
                    path[length - 1 - i] = temp;
                }
                
                return length;
            }
            
            const AdjList* list = &g->lists[current];
            for (int i = 0; i < list->count; i++) {
                int neighbor = list->neighbors[i];
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    parent[neighbor] = current;
                    queue_enqueue(&q, neighbor);
                }
            }
        }
        
        return 0;  // No path found
    }

Embedded Use Case - Task Dependency
------------------------------------

.. code-block:: c

    // Task dependency graph for startup sequence
    typedef enum {
        TASK_INIT_CLOCK,
        TASK_INIT_GPIO,
        TASK_INIT_UART,
        TASK_INIT_I2C,
        TASK_INIT_SPI,
        TASK_INIT_SENSORS,
        TASK_START_MAIN,
        NUM_TASKS
    } TaskID;
    
    void build_dependency_graph(GraphList* g) {
        graph_list_init(g, NUM_TASKS);
        
        // Clock must be first
        graph_list_add_edge(g, TASK_INIT_CLOCK, TASK_INIT_GPIO, 0);
        graph_list_add_edge(g, TASK_INIT_CLOCK, TASK_INIT_UART, 0);
        
        // Peripherals depend on GPIO
        graph_list_add_edge(g, TASK_INIT_GPIO, TASK_INIT_I2C, 0);
        graph_list_add_edge(g, TASK_INIT_GPIO, TASK_INIT_SPI, 0);
        
        // Sensors depend on I2C/SPI
        graph_list_add_edge(g, TASK_INIT_I2C, TASK_INIT_SENSORS, 0);
        graph_list_add_edge(g, TASK_INIT_SPI, TASK_INIT_SENSORS, 0);
        
        // Main depends on sensors
        graph_list_add_edge(g, TASK_INIT_SENSORS, TASK_START_MAIN, 0);
    }

🌊 3. Depth-First Search (DFS)
================================

Overview
--------
Explores as far as possible along each branch before backtracking.

**Applications:**
* Cycle detection
* Topological sorting
* Pathfinding (mazes)
* Connected components

Iterative Implementation
------------------------

.. code-block:: c

    #define STACK_SIZE 64
    
    typedef struct {
        int data[STACK_SIZE];
        int top;
    } Stack;
    
    void stack_init(Stack* s) {
        s->top = -1;
    }
    
    bool stack_push(Stack* s, int value) {
        if (s->top >= STACK_SIZE - 1) return false;
        s->data[++s->top] = value;
        return true;
    }
    
    bool stack_pop(Stack* s, int* value) {
        if (s->top < 0) return false;
        *value = s->data[s->top--];
        return true;
    }
    
    bool stack_is_empty(const Stack* s) {
        return s->top < 0;
    }
    
    // DFS iterative
    void dfs_iterative(const GraphList* g, int start, void (*visit)(int node)) {
        bool visited[MAX_NODES] = {false};
        Stack s;
        stack_init(&s);
        
        stack_push(&s, start);
        
        while (!stack_is_empty(&s)) {
            int current;
            stack_pop(&s, &current);
            
            if (visited[current]) continue;
            
            visited[current] = true;
            visit(current);
            
            const AdjList* list = &g->lists[current];
            // Push neighbors in reverse order for correct DFS order
            for (int i = list->count - 1; i >= 0; i--) {
                int neighbor = list->neighbors[i];
                if (!visited[neighbor]) {
                    stack_push(&s, neighbor);
                }
            }
        }
    }

Recursive Implementation
------------------------

.. code-block:: c

    static bool visited[MAX_NODES];
    
    void dfs_recursive_helper(const GraphList* g, int node, void (*visit)(int node)) {
        visited[node] = true;
        visit(node);
        
        const AdjList* list = &g->lists[node];
        for (int i = 0; i < list->count; i++) {
            int neighbor = list->neighbors[i];
            if (!visited[neighbor]) {
                dfs_recursive_helper(g, neighbor, visit);
            }
        }
    }
    
    void dfs_recursive(const GraphList* g, int start, void (*visit)(int node)) {
        memset(visited, 0, sizeof(visited));
        dfs_recursive_helper(g, start, visit);
    }

Cycle Detection
---------------

.. code-block:: c

    typedef enum {
        WHITE,  // Not visited
        GRAY,   // Being processed
        BLACK   // Processed
    } NodeColor;
    
    static NodeColor colors[MAX_NODES];
    
    bool dfs_has_cycle_helper(const GraphList* g, int node) {
        colors[node] = GRAY;
        
        const AdjList* list = &g->lists[node];
        for (int i = 0; i < list->count; i++) {
            int neighbor = list->neighbors[i];
            
            if (colors[neighbor] == GRAY) {
                return true;  // Back edge found - cycle!
            }
            
            if (colors[neighbor] == WHITE) {
                if (dfs_has_cycle_helper(g, neighbor)) {
                    return true;
                }
            }
        }
        
        colors[node] = BLACK;
        return false;
    }
    
    bool graph_has_cycle(const GraphList* g) {
        memset(colors, WHITE, sizeof(colors));
        
        for (int i = 0; i < g->num_nodes; i++) {
            if (colors[i] == WHITE) {
                if (dfs_has_cycle_helper(g, i)) {
                    return true;
                }
            }
        }
        
        return false;
    }

📋 4. Topological Sort
=======================

Overview
--------
Linear ordering of vertices in directed acyclic graph (DAG).
Vertex u appears before v if edge u→v exists.

**Applications:**
* Build systems (dependency resolution)
* Task scheduling
* Software installation order
* Course prerequisites

Implementation (DFS-based)
--------------------------

.. code-block:: c

    static int finish_time[MAX_NODES];
    static int time_counter;
    
    void topological_sort_helper(const GraphList* g, int node, bool* visited) {
        visited[node] = true;
        
        const AdjList* list = &g->lists[node];
        for (int i = 0; i < list->count; i++) {
            int neighbor = list->neighbors[i];
            if (!visited[neighbor]) {
                topological_sort_helper(g, neighbor, visited);
            }
        }
        
        finish_time[node] = time_counter++;
    }
    
    int topological_sort(const GraphList* g, int* sorted_order) {
        bool visited[MAX_NODES] = {false};
        time_counter = 0;
        
        // DFS from all unvisited nodes
        for (int i = 0; i < g->num_nodes; i++) {
            if (!visited[i]) {
                topological_sort_helper(g, i, &visited[0]);
            }
        }
        
        // Sort by finish time (descending)
        typedef struct {
            int node;
            int time;
        } NodeTime;
        
        NodeTime nodes[MAX_NODES];
        for (int i = 0; i < g->num_nodes; i++) {
            nodes[i].node = i;
            nodes[i].time = finish_time[i];
        }
        
        // Simple bubble sort for small arrays
        for (int i = 0; i < g->num_nodes - 1; i++) {
            for (int j = 0; j < g->num_nodes - i - 1; j++) {
                if (nodes[j].time < nodes[j + 1].time) {
                    NodeTime temp = nodes[j];
                    nodes[j] = nodes[j + 1];
                    nodes[j + 1] = temp;
                }
            }
        }
        
        for (int i = 0; i < g->num_nodes; i++) {
            sorted_order[i] = nodes[i].node;
        }
        
        return g->num_nodes;
    }

Kahn's Algorithm (BFS-based)
-----------------------------

.. code-block:: c

    int topological_sort_kahn(const GraphList* g, int* sorted_order) {
        int in_degree[MAX_NODES] = {0};
        
        // Calculate in-degrees
        for (int u = 0; u < g->num_nodes; u++) {
            const AdjList* list = &g->lists[u];
            for (int i = 0; i < list->count; i++) {
                int v = list->neighbors[i];
                in_degree[v]++;
            }
        }
        
        // Queue nodes with in-degree 0
        Queue q;
        queue_init(&q);
        for (int i = 0; i < g->num_nodes; i++) {
            if (in_degree[i] == 0) {
                queue_enqueue(&q, i);
            }
        }
        
        int count = 0;
        while (!queue_is_empty(&q)) {
            int u;
            queue_dequeue(&q, &u);
            sorted_order[count++] = u;
            
            const AdjList* list = &g->lists[u];
            for (int i = 0; i < list->count; i++) {
                int v = list->neighbors[i];
                in_degree[v]--;
                if (in_degree[v] == 0) {
                    queue_enqueue(&q, v);
                }
            }
        }
        
        // If count != num_nodes, graph has cycle
        return (count == g->num_nodes) ? count : -1;
    }

Use Case - Build System
------------------------

.. code-block:: c

    typedef enum {
        FILE_MAIN_C,
        FILE_UART_C,
        FILE_GPIO_C,
        FILE_MAIN_O,
        FILE_UART_O,
        FILE_GPIO_O,
        FILE_FIRMWARE_ELF,
        NUM_FILES
    } FileID;
    
    void build_dependency_graph(GraphList* g) {
        graph_list_init(g, NUM_FILES);
        
        // .c → .o dependencies
        graph_list_add_edge(g, FILE_MAIN_C, FILE_MAIN_O, 0);
        graph_list_add_edge(g, FILE_UART_C, FILE_UART_O, 0);
        graph_list_add_edge(g, FILE_GPIO_C, FILE_GPIO_O, 0);
        
        // .o → .elf dependencies
        graph_list_add_edge(g, FILE_MAIN_O, FILE_FIRMWARE_ELF, 0);
        graph_list_add_edge(g, FILE_UART_O, FILE_FIRMWARE_ELF, 0);
        graph_list_add_edge(g, FILE_GPIO_O, FILE_FIRMWARE_ELF, 0);
    }
    
    void execute_build(void) {
        GraphList g;
        build_dependency_graph(&g);
        
        int build_order[NUM_FILES];
        int count = topological_sort_kahn(&g, build_order);
        
        if (count < 0) {
            printf("Error: Circular dependency detected!\n");
            return;
        }
        
        for (int i = 0; i < count; i++) {
            build_file(build_order[i]);
        }
    }

🛤️ 5. Dijkstra's Shortest Path
=================================

Overview
--------
Finds shortest path in weighted graphs with non-negative weights.

**Applications:**
* Network routing
* GPS navigation
* Resource allocation
* Packet routing

Implementation
--------------

.. code-block:: c

    #define INFINITY 0x7FFFFFFF
    
    typedef struct {
        int node;
        int distance;
    } DistNode;
    
    int dijkstra(const GraphList* g, int start, int target, int* path) {
        int dist[MAX_NODES];
        int prev[MAX_NODES];
        bool visited[MAX_NODES] = {false};
        
        // Initialize
        for (int i = 0; i < g->num_nodes; i++) {
            dist[i] = INFINITY;
            prev[i] = -1;
        }
        dist[start] = 0;
        
        // Main loop
        for (int count = 0; count < g->num_nodes; count++) {
            // Find min distance unvisited node
            int u = -1;
            int min_dist = INFINITY;
            for (int i = 0; i < g->num_nodes; i++) {
                if (!visited[i] && dist[i] < min_dist) {
                    min_dist = dist[i];
                    u = i;
                }
            }
            
            if (u == -1) break;  // All reachable nodes visited
            
            visited[u] = true;
            
            if (u == target) break;  // Found target
            
            // Update neighbors
            const AdjList* list = &g->lists[u];
            for (int i = 0; i < list->count; i++) {
                int v = list->neighbors[i];
                int weight = list->weights[i];
                
                if (!visited[v]) {
                    int new_dist = dist[u] + weight;
                    if (new_dist < dist[v]) {
                        dist[v] = new_dist;
                        prev[v] = u;
                    }
                }
            }
        }
        
        // Reconstruct path
        if (dist[target] == INFINITY) {
            return -1;  // No path
        }
        
        int path_len = 0;
        int node = target;
        while (node != -1) {
            path[path_len++] = node;
            node = prev[node];
        }
        
        // Reverse path
        for (int i = 0; i < path_len / 2; i++) {
            int temp = path[i];
            path[i] = path[path_len - 1 - i];
            path[path_len - 1 - i] = temp;
        }
        
        return dist[target];
    }

Use Case - Sensor Network Routing
----------------------------------

.. code-block:: c

    typedef enum {
        NODE_SENSOR1,
        NODE_SENSOR2,
        NODE_SENSOR3,
        NODE_GATEWAY1,
        NODE_GATEWAY2,
        NODE_SERVER,
        NUM_NETWORK_NODES
    } NetworkNode;
    
    void build_network_graph(GraphList* g) {
        graph_list_init(g, NUM_NETWORK_NODES);
        
        // Add edges with signal strength (inverse = cost)
        graph_list_add_edge(g, NODE_SENSOR1, NODE_GATEWAY1, 10);
        graph_list_add_edge(g, NODE_SENSOR1, NODE_GATEWAY2, 15);
        graph_list_add_edge(g, NODE_SENSOR2, NODE_GATEWAY1, 8);
        graph_list_add_edge(g, NODE_SENSOR3, NODE_GATEWAY2, 12);
        graph_list_add_edge(g, NODE_GATEWAY1, NODE_SERVER, 5);
        graph_list_add_edge(g, NODE_GATEWAY2, NODE_SERVER, 5);
    }
    
    int find_best_route(NetworkNode sensor) {
        GraphList g;
        build_network_graph(&g);
        
        int path[NUM_NETWORK_NODES];
        int cost = dijkstra(&g, sensor, NODE_SERVER, path);
        
        return cost;
    }

📊 6. Additional Graph Algorithms
===================================

Minimum Spanning Tree - Prim's Algorithm
-----------------------------------------

.. code-block:: c

    int prims_mst(const GraphList* g, int edges_out[][2]) {
        bool in_mst[MAX_NODES] = {false};
        int key[MAX_NODES];
        int parent[MAX_NODES];
        
        for (int i = 0; i < g->num_nodes; i++) {
            key[i] = INFINITY;
            parent[i] = -1;
        }
        
        key[0] = 0;
        int edge_count = 0;
        
        for (int count = 0; count < g->num_nodes; count++) {
            // Find minimum key
            int u = -1;
            int min_key = INFINITY;
            for (int i = 0; i < g->num_nodes; i++) {
                if (!in_mst[i] && key[i] < min_key) {
                    min_key = key[i];
                    u = i;
                }
            }
            
            if (u == -1) break;
            
            in_mst[u] = true;
            
            if (parent[u] != -1) {
                edges_out[edge_count][0] = parent[u];
                edges_out[edge_count][1] = u;
                edge_count++;
            }
            
            // Update keys
            const AdjList* list = &g->lists[u];
            for (int i = 0; i < list->count; i++) {
                int v = list->neighbors[i];
                int weight = list->weights[i];
                
                if (!in_mst[v] && weight < key[v]) {
                    key[v] = weight;
                    parent[v] = u;
                }
            }
        }
        
        return edge_count;
    }

🛠️ Performance Tips for Embedded
===================================

1. Use Static Arrays
---------------------

.. code-block:: c

    // GOOD: Static allocation
    GraphList graph;
    
    // BAD: Dynamic allocation (avoid in embedded)
    GraphList* graph = malloc(sizeof(GraphList));

2. Limit Graph Size
-------------------

.. code-block:: c

    #define MAX_NODES 32  // Tune based on RAM
    #define MAX_EDGES_PER_NODE 8

3. Use Bit Arrays for Visited
------------------------------

.. code-block:: c

    // Memory efficient for large graphs
    uint32_t visited_bits[(MAX_NODES + 31) / 32];
    
    void set_visited(int node) {
        visited_bits[node / 32] |= (1u << (node % 32));
    }
    
    bool is_visited(int node) {
        return (visited_bits[node / 32] & (1u << (node % 32))) != 0;
    }

4. Prefer Iterative over Recursive
-----------------------------------

.. code-block:: c

    // GOOD: Iterative (no stack overflow risk)
    void dfs_iterative(...);
    
    // RISKY: Recursive (stack depth = graph depth)
    void dfs_recursive(...);

📚 References
=============

* Algorithms in a Nutshell (O'Reilly) - Chapter 6: Graph Algorithms
* Introduction to Algorithms (CLRS) - Graphs section
* Embedded graph algorithms for real-time systems

🎓 Key Takeaways
================

1. **BFS** for shortest unweighted paths, level traversal
2. **DFS** for cycles, topological sort, connectivity
3. **Dijkstra** for weighted shortest paths (no negative weights)
4. **Topological sort** essential for dependency resolution
5. **Adjacency lists** better than matrices for sparse graphs
6. **Static allocation** preferred (no malloc)
7. **Iterative implementations** safer than recursive
8. **Limit graph size** based on available RAM

==========================================
✅ Completion Checklist
==========================================

- [x] Graph representations (matrix, list)
- [x] BFS implementation and applications
- [x] DFS (iterative and recursive)
- [x] Cycle detection
- [x] Topological sort (2 methods)
- [x] Dijkstra's shortest path
- [x] Minimum spanning tree
- [x] Embedded optimization tips
- [x] Real-world examples

==========================================
