
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheat sheet for sorting algorithms in C**  
(including **pseudocode**, **time complexity**, **space complexity**, **stability**, and **typical embedded C usage notes**).

🧮 1. Comparison-Based Sorting Algorithms

| Algorithm          | Pseudocode (core idea)                                                                 | Time Complexity (avg / worst) | Space | Stable? | Embedded C Notes / When to use |
|---------------------|------------------------------------------------------------------------------------------|--------------------------------|-------|---------|--------------------------------|
| Bubble Sort        | for i in 0..n-2<br>  for j in 0..n-i-2<br>    if a[j] > a[j+1] swap(a[j], a[j+1]) | O(n²) / O(n²)                 | O(1)  | Yes     | Very small arrays (< 20–30), educational |
| Insertion Sort     | for i = 1 to n-1<br>  key = a[i]<br>  j = i-1<br>  while j≥0 and a[j]>key<br>    a[j+1]=a[j], j--<br>  a[j+1]=key | O(n²) / O(n²)                 | O(1)  | Yes     | **🟢 🟢 Best for small n (< 50)** or nearly sorted data |
| Selection Sort     | for i = 0 to n-2<br>  min_idx = i<br>  for j = i+1 to n-1<br>    if a[j] < a[min_idx] min_idx=j<br>  swap a[i] ↔ a[min_idx] | O(n²) / O(n²)                 | O(1)  | No      | Rarely used – many swaps, 🔴 🔴 bad cache behavior |
| Quick Sort (Lomuto) | quicksort(arr, low, high):<br>  if low < high<br>    p = partition(arr, low, high)<br>    quicksort(low, p-1)<br>    quicksort(p+1, high)<br><br>partition:<br>  pivot = arr[high]<br>  i = low-1<br>  for j=low to high-1<br>    if arr[j] ≤ pivot<br>      i++, swap arr[i] ↔ arr[j]<br>  swap arr[i+1] ↔ arr[high]<br>  return i+1 | O(n log n) / O(n²)            | O(log n) stack | No      | **Most common general-purpose sort** – but watch stack & worst-case |
| Merge Sort         | mergesort(arr, l, r):<br>  if l < r<br>    m = (l+r)/2<br>    mergesort(l, m)<br>    mergesort(m+1, r)<br>    merge(l, m, r) | O(n log n) / O(n log n)       | O(n)  | Yes     | Very stable, 🟢 🟢 good worst-case – but needs extra space |
| Heap Sort          | Build max-heap → repeatedly extract max to end | O(n log n) / O(n log n)       | O(1)  | No      | In-place, predictable time – 🟢 🟢 good when memory is tight |

📚 2. Quick Reference Table – When to Choose Which Sort in Embedded C

| Scenario                              | Recommended Algorithm       | Reason / Notes |
|---------------------------------------|------------------------------|----------------|
| Very small array (n ≤ 20–30)          | Insertion Sort              | Fastest in practice, minimal code |
| Nearly sorted or small updates        | Insertion Sort              | O(n) 🟢 🟢 best case |
⭐ | General purpose, RAM not critical     | Quick Sort (3-way or Hoare) | Fast average case, widely implemented |
| Memory extremely tight & predictable time needed | Heap Sort               | O(1) extra space, O(n log n) worst case |
⭐ | Stability required (keep equal keys order) | Merge Sort or Insertion | Stable sorts |
| No extra space + worst-case guarantee | Heap Sort                   | No recursion, no stack risk |
| Already almost sorted (online data)   | Insertion Sort or Timsort-like | Adaptive behavior |
⭐ | Safety-critical / certifiable code    | Insertion / Selection / Heap | No recursion, predictable timing |

📌 3. Useful Embedded C Sorting Snippets

**1. Insertion Sort (very common in small embedded arrays)**

.. code-block:: c

void insertion_sort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
⭐         int key = arr[i];
        int j = i - 1;
⭐         while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
⭐         arr[j + 1] = key;
    }
}

**2. Quick Sort (classic Lomuto partition – be careful with stack)**

.. code-block:: c

static int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            // swap arr[i] ↔ arr[j]
            int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
        }
    }
    // swap arr[i+1] ↔ arr[high]
    int temp = arr[i+1]; arr[i+1] = arr[high]; arr[high] = temp;
    return i + 1;
}

void quick_sort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

**3. Tiny sorting macro (for very small fixed-size arrays)**

.. code-block:: c

#define SORT_ARRAY(arr) 🟢 🟢 do { \
    for (size_t i = 1; i < sizeof(arr)/sizeof(arr[0]); i++) { \
        for (size_t j = 0; j < sizeof(arr)/sizeof(arr[0])-i; j++) { \
            if ((arr)[j] > (arr)[j+1]) { \
                typeof(arr[0]) tmp = (arr)[j]; \
                (arr)[j] = (arr)[j+1]; (arr)[j+1] = tmp; \
            } \
        } \
    } } while(0)

📌 4. Embedded-Specific Advice (2025–2026)

| Advice                                      | Reason / Impact |
|---------------------------------------------|-----------------|
| Prefer Insertion Sort for n ≤ 40–50         | Often faster than quicksort on small data due to cache & low overhead |
| 🔴 🔴 Avoid recursive quicksort on deep stacks    | Stack overflow risk on small MCUs (use iterative version if needed) |
| Use ``qsort()`` from ``<stdlib.h>`` only if...  | You trust the library version & don’t need strict determinism |
| For deterministic timing → prefer Heap Sort | Fixed O(n log n) – no pivot selection issues |
| For flash-only code → Insertion or Bubble   | Very small code size |
| For sorted insert into fixed buffer         | Use binary search + shift (like insertion sort logic) |

Pick wisely based on **array size**, **RAM**, **stack size**, **real-time requirements**, and **code size constraints**.  
Most real embedded projects in 2026 use **Insertion Sort** for small arrays and **Quick Sort** (or library ``qsort``) for larger ones.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
