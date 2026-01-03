# Modern C++ Advanced Pointers Cheat Sheet  
(C++11 / C++14 / C++17 / C++20 / C++23)

Focuses on safe, modern alternatives to raw pointers, plus advanced raw pointer techniques when needed.

## 1. Core Philosophy
**Prefer smart pointers and references over raw pointers.**  
Raw pointers only when you need observer semantics or interfacing with C/low-level code.

## 2. Smart Pointers (from `<memory>`)

| Pointer Type       | Ownership          | Deleter Customizable | Copyable | Thread-Safe Transfer | Use Case |
|--------------------|--------------------|----------------------|----------|----------------------|----------|
| `std::unique_ptr<T>` | Exclusive ownership | Yes (default/delete or custom) | No (movable only) | Move-only | Single owner, RAII for dynamic objects |
| `std::shared_ptr<T>` | Shared ownership   | Yes                  | Yes      | Atomic ref-count     | Multiple owners, reference-counted resources |
| `std::weak_ptr<T>`   | Non-owning observer| —                    | Yes      | —                    | Break cycles in shared_ptr graphs |

### unique_ptr

```cpp
#include <memory>

std::unique_ptr<int> p1 = std::make_unique<int>(42);  // Preferred (C++14+)
auto p2 = std::make_unique<std::vector<int>>({1,2,3});

std::unique_ptr<int[]> arr = std::make_unique<int[]>(100);  // Array form

// Custom deleter
auto deleter = [](FILE* f) { fclose(f); };
std::unique_ptr<FILE, decltype(deleter)> file(fopen("log.txt","w"), deleter);

// Move semantics
std::unique_ptr<int> p3 = std::move(p1);  // p1 now null
```

### shared_ptr

```cpp
#include <memory>

auto sp1 = std::make_shared<std::string>("hello");  // Preferred
std::shared_ptr<int> sp2 = sp1;  // ref count = 2

long count = sp1.use_count();
if (sp2) { /* non-null check */ }

std::shared_ptr<Base> base = std::make_shared<Derived>();
// Automatic downcast via aliasing constructor if needed
```

### weak_ptr

```cpp
std::shared_ptr<Node> parent = std::make_shared<Node>();
std::weak_ptr<Node> weak_parent = parent;  // Non-owning

if (auto locked = weak_parent.lock()) {
    // Use locked-> safely (may be expired)
} else {
    // Object destroyed
}
```

## 3. Observer Pointers (C++20+)

```cpp
#include <memory>

std::observer_ptr<int> obs(raw_ptr);        // Non-owning, no overhead
std::observer_ptr<Widget> w = &my_widget;   // Explicit observer semantics
w.get();   // -> raw pointer
w.release(); // Returns raw and sets to nullptr
```

**Note**: `std::observer_ptr` is currently in `<experimental/observer_ptr>` or TS; not yet in standard (as of C++23).

## 4. Raw Pointers – When & How to Use Safely

```cpp
int* raw = nullptr;                 // Always initialize!
int* raw2 = new int(10);            // Avoid manual new/delete
delete raw2;                        // Prefer RAII instead

// Prefer references when possible
void func(int& ref);                // No null possible

// Raw pointers as optional parameters
void func(int* ptr = nullptr) {
    if (ptr) { /* use */ }
}
```

**Never** do:
- Return raw pointers to local stack objects
- Manual `new`/`delete` in normal code

## 5. Pointer Traits & Utilities

```cpp
#include <memory>

std::to_address(ptr);               // C++20: safe raw pointer from fancy pointer
                                    // Works with unique_ptr, shared_ptr, raw, iterators

auto raw = std::to_address(my_unique_ptr);
```

## 6. Advanced: Custom Deleters & Allocators

```cpp
struct PoolDeleter {
    void operator()(MyObject* ptr) const {
        pool.release(ptr);  // Return to custom pool
    }
};

std::unique_ptr<MyObject, PoolDeleter> pooled_obj(obj, PoolDeleter{});

// Polymorphic allocators (C++17+)
#include <memory_resource>
std::pmr::monotonic_buffer_resource buffer(raw_buffer, size);
std::pmr::polymorphic_allocator<int> alloc(&buffer);
std::pmr::vector<int> vec(alloc);
```

## 7. Pointer Casting (Modern)

```cpp
#include <memory>

// Static
Derived* d = static_cast<Derived*>(base_ptr);

// Dynamic (safe downcast)
std::shared_ptr<Derived> derived = std::dynamic_pointer_cast<Derived>(base_shared);

// Const cast
std::shared_ptr<const Widget> cwidget = std::const_pointer_cast<const Widget>(widget);

// Reinterpret (dangerous, avoid)
void* vp = reinterpret_cast<void*>(raw_ptr);
```

## 8. nullptr (C++11+)

```cpp
void func(int* p);     // Can accept nullptr
void func(std::nullptr_t); // Overload for explicit null

int* p = nullptr;      // Preferred over NULL or 0
if (p) { }             // false
p = nullptr;           // Reset
```

## 9. Smart Pointer Guidelines Summary

| Scenario                              | Recommended Pointer Type                     |
|---------------------------------------|----------------------------------------------|
| Single owner, no transfer needed      | `std::unique_ptr<T>`                         |
| Transfer ownership                    | `std::unique_ptr<T>` (move)                  |
| Multiple owners                       | `std::shared_ptr<T>`                         |
| Break cycles (parent → child)         | Child holds `std::weak_ptr<Parent>`          |
| Non-owning reference                  | Raw pointer, reference, or `std::weak_ptr`   |
| Optional parameter / return           | Raw pointer or `std::optional<T&>` (C++17)   |
| C API / legacy code                   | Raw pointers (but wrap in RAII when possible)|
| Container of polymorphic objects      | `std::vector<std::unique_ptr<Base>>`         |

## 10. Best Practices (Modern C++)

- Always use `std::make_unique` / `std::make_shared` (exception-safe)
- Never use `new`/`delete` directly
- Prefer `auto` with `make_` functions
- Avoid raw owning pointers entirely
- Use `std::to_address` for generic code
- Enable `-Wshadow` and `-fno-delete-null-pointer-checks`
- For performance-critical code: `unique_ptr` preferred over `shared_ptr`

**Golden Rule**:  
If it owns a resource → smart pointer  
If it observes → raw pointer or reference  
If it's optional → consider `std::optional<T>` with reference or pointer inside

This cheat sheet emphasizes safe, modern C++ practices while showing advanced pointer features when raw control is needed.