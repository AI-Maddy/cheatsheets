**Cheat Sheet for Trees & Related Algorithms in C**  
(2025–2026 style – focus on static allocation, minimal recursion, deterministic behavior, small code & RAM footprint)

### 1. Binary Tree Node (most common base structure)

```c
typedef struct TreeNode {
    int               value;        // or any payload type
    struct TreeNode  *left;
    struct TreeNode  *right;
} TreeNode;

// Optional: parent pointer (for some traversals / deletions)
typedef struct TreeNodeP {
    int                value;
    struct TreeNodeP  *left;
    struct TreeNodeP  *right;
    struct TreeNodeP  *parent;
} TreeNodeP;
```

### 2. Static Binary Tree (fixed max nodes – no malloc)

```c
#define MAX_TREE_NODES  127

static TreeNode nodes[MAX_TREE_NODES];
static uint8_t  used[MAX_TREE_NODES] = {0};   // 0 = free, 1 = used
static TreeNode *root = NULL;

TreeNode *tree_alloc(void) {
    for (int i = 0; i < MAX_TREE_NODES; i++) {
        if (!used[i]) {
            used[i] = 1;
            nodes[i].left = nodes[i].right = NULL;
            return &nodes[i];
        }
    }
    return NULL;
}

void tree_free(TreeNode *node) {
    if (!node) return;
    ptrdiff_t idx = node - nodes;
    if (idx >= 0 && idx < MAX_TREE_NODES) used[idx] = 0;
}
```

### 3. Classic Recursive Traversals (use with caution in embedded)

```c
// In-order   (left → root → right)  → sorted order for BST
void inorder(TreeNode *node) {
    if (!node) return;
    inorder(node->left);
    printf("%d ", node->value);   // or process(node->value)
    inorder(node->right);
}

// Pre-order  (root → left → right) → good for copying tree
void preorder(TreeNode *node) {
    if (!node) return;
    printf("%d ", node->value);
    preorder(node->left);
    preorder(node->right);
}

// Post-order (left → right → root) → good for deletion / expression tree
void postorder(TreeNode *node) {
    if (!node) return;
    postorder(node->left);
    postorder(node->right);
    printf("%d ", node->value);
}
```

### 4. Iterative Traversals (safer – no stack overflow risk)

```c
// Iterative In-order (Morris traversal – O(1) extra space)
void inorder_iterative_morris(TreeNode *root) {
    TreeNode *curr = root;
    while (curr) {
        if (!curr->left) {
            printf("%d ", curr->value);
            curr = curr->right;
        } else {
            TreeNode *pred = curr->left;
            while (pred->right && pred->right != curr)
                pred = pred->right;
            if (!pred->right) {
                pred->right = curr;
                curr = curr->left;
            } else {
                pred->right = NULL;
                printf("%d ", curr->value);
                curr = curr->right;
            }
        }
    }
}

// Iterative Pre-order (using stack – needs O(h) space)
#include <stdbool.h>
#define MAX_STACK 64

typedef struct {
    TreeNode *nodes[MAX_STACK];
    int top;
} StackTree;

void push(StackTree *s, TreeNode *node) { if (s->top < MAX_STACK-1) s->nodes[++s->top] = node; }
TreeNode *pop(StackTree *s) { return s->top >= 0 ? s->nodes[s->top--] : NULL; }
bool empty(StackTree *s) { return s->top < 0; }

void preorder_iterative(TreeNode *root) {
    if (!root) return;
    StackTree s = {.top = -1};
    push(&s, root);
    while (!empty(&s)) {
        TreeNode *node = pop(&s);
        printf("%d ", node->value);
        if (node->right) push(&s, node->right);
        if (node->left)  push(&s, node->left);
    }
}
```

### 5. Binary Search Tree (BST) – Core Operations

```c
// Insert (recursive – careful with stack depth)
TreeNode *bst_insert(TreeNode *node, int val) {
    if (!node) {
        TreeNode *new = tree_alloc();
        if (new) new->value = val;
        return new;
    }
    if (val < node->value)
        node->left = bst_insert(node->left, val);
    else if (val > node->value)
        node->right = bst_insert(node->right, val);
    return node;
}

// Search
TreeNode *bst_search(TreeNode *root, int val) {
    while (root) {
        if (val == root->value) return root;
        root = (val < root->value) ? root->left : root->right;
    }
    return NULL;
}

// Find min / max
TreeNode *bst_min(TreeNode *node) {
    while (node && node->left) node = node->left;
    return node;
}
```

### 6. Binary Heap (Priority Queue) – Very common in embedded schedulers

```c
#define MAX_HEAP  100

typedef struct {
    int      data[MAX_HEAP];
    uint16_t size;
} MinHeap;

void heapify_up(MinHeap *h, int idx) {
    while (idx > 0) {
        int parent = (idx - 1) / 2;
        if (h->data[parent] <= h->data[idx]) break;
        // swap
        int t = h->data[parent]; h->data[parent] = h->data[idx]; h->data[idx] = t;
        idx = parent;
    }
}

void heap_push(MinHeap *h, int val) {
    if (h->size >= MAX_HEAP) return;
    h->data[h->size] = val;
    heapify_up(h, h->size++);
}

void heapify_down(MinHeap *h, int idx) {
    int smallest = idx;
    int left  = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < h->size && h->data[left] < h->data[smallest])   smallest = left;
    if (right < h->size && h->data[right] < h->data[smallest]) smallest = right;

    if (smallest != idx) {
        int t = h->data[idx]; h->data[idx] = h->data[smallest]; h->data[smallest] = t;
        heapify_down(h, smallest);
    }
}

int heap_pop(MinHeap *h) {
    if (h->size == 0) return -1;
    int min = h->data[0];
    h->data[0] = h->data[--h->size];
    heapify_down(h, 0);
    return min;
}
```

### 7. Quick Decision Table – Which Tree/Structure in Embedded C?

Use case                              | Recommended Structure       | Why / Trade-off
--------------------------------------|------------------------------|------------------
Small lookup table / sorted data      | Sorted array + binary search | Fast, no pointers, cache friendly
Dynamic insert/delete, keep sorted    | BST (balanced if possible)   | O(log n) average, recursion risk
Priority queue / scheduler            | Binary Heap (min/max)        | O(log n) insert/pop, O(1) peek
Event queue / UART buffer             | Ring buffer                  | O(1), fixed memory
Graph / tree with parent pointers     | TreeNodeP (with parent)      | Easier deletion / traversal
Very limited RAM, small n             | Static array                 | Zero overhead, predictable

Good luck implementing tree structures in your embedded project!  
Most real-world embedded code in 2025–2026 prefers **binary heaps** for priority queues and **ring buffers** over trees whenever possible — real trees are rare unless you really need logarithmic operations and can afford the pointer overhead.