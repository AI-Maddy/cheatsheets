**Structural Design Patterns**—the patterns that deal with class and object composition—implemented using Modern C++ (C++11/14/17/20/23) features like smart pointers, templates, and `std::variant`.

---

## 1. Adapter Pattern

**Purpose:** Converts the interface of a class into another interface clients expect.

* **Modern Approach:** Use `std::function` or lambdas for simple functional adapters, or composition with `unique_ptr`.
* **Key Concept:** Wrap the "Legacy" class inside the "Adapter" class.

```cpp
class LegacyScanner {
public:
    void legacyScan() { /* ... */ }
};

class IScanner { // New interface
public:
    virtual ~IScannable() = default;
    virtual void scan() = 0;
};

class ScannerAdapter : public IScanner {
    std::unique_ptr<LegacyScanner> legacyScanner;
public:
    void scan() override { legacyScanner->legacyScan(); }
};

```

---

## 2. Bridge Pattern

**Purpose:** Decouples an abstraction from its implementation so the two can vary independently. In C++, this is often referred to as the **Pimpl (Pointer to Implementation) Idiom**.

* **Modern Approach:** Use `std::unique_ptr` to manage the implementation pointer to ensure exception safety and automatic cleanup.

```cpp
// In .h file
class Renderer {
    struct Impl; 
    std::unique_ptr<Impl> pimpl;
public:
    Renderer();
    ~Renderer(); // Must be defined in .cpp where Impl is complete
    void draw();
};

```

---

## 3. Composite Pattern

**Purpose:** Composes objects into tree structures to represent part-whole hierarchies. Clients treat individual objects and compositions uniformly.

* **Modern Approach:** Use `std::vector<std::shared_ptr<Component>>` to manage children. Use `std::enable_shared_from_this` if components need to manage their own lifecycle.

```cpp
class Graphic {
public:
    virtual void draw() = 0;
};

class CompositeGraphic : public Graphic {
    std::vector<std::shared_ptr<Graphic>> children;
public:
    void draw() override {
        for (auto& child : children) child->draw();
    }
};

```

---

## 4. Decorator Pattern

**Purpose:** Attaches additional responsibilities to an object dynamically.

* **Modern Approach:** Use **Static Polymorphism (CRTP)** or **Templates** if the decoration is known at compile time to avoid virtual call overhead.

```cpp
// Compile-time (Static) Decorator
template <typename T>
class BoldText : public T {
public:
    void render() {
        std::cout << "<b>";
        T::render();
        std::cout << "</b>";
    }
};

```

---

## 5. Facade Pattern

**Purpose:** Provides a unified interface to a set of interfaces in a subsystem.

* **Modern Approach:** Often implemented as a header-only utility or a singleton-like manager using `std::string_view` for efficient string passing across the subsystem.

---

## 6. Flyweight Pattern

**Purpose:** Uses sharing to support large numbers of fine-grained objects efficiently.

* **Modern Approach:** Use `std::shared_ptr` combined with a `std::unordered_map` (the factory) to manage and share instances. Use `const` heavily to ensure the shared state isn't accidentally modified.

---

## 7. Proxy Pattern

**Purpose:** Provides a surrogate or placeholder for another object to control access to it.

* **Modern Approach:** Smart pointers (`std::shared_ptr`, `std::weak_ptr`) are themselves built-in examples of the Proxy pattern.
* **Virtual Proxy:** Use `std::optional` or a "lazy" wrapper to delay the creation of expensive objects until they are accessed.

```cpp
class HeavyObjectProxy {
    mutable std::unique_ptr<HeavyObject> realSubject;
public:
    void request() const {
        if (!realSubject) realSubject = std::make_unique<HeavyObject>();
        realSubject->request();
    }
};

```

---

## Modern C++ Specific Tools for Patterns

| Feature | Benefit for Structural Patterns |
| --- | --- |
| **`std::variant` / `std::visit**` | A modern alternative to the **Visitor** (behavioral) and **Composite** patterns for fixed sets of types. |
| **`std::span` (C++20)** | Acts as a proxy/view for contiguous memory (arrays/vectors) without ownership. |
| **Concepts (C++20)** | Replaces interfaces in static structural patterns, ensuring templates meet specific criteria at compile time. |
| **`std::unique_ptr`** | The default choice for **Pimpl** and **Adapter** to express clear ownership. |

Would you like me to dive deeper into the **Pimpl Idiom** or provide a **Static Decorator** code example using C++20 Concepts?