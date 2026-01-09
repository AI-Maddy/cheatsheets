
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


Modern C++ (C++11 through C++23) has moved away from "magic" behavior toward explicit control. This cheat sheet covers the essential constructor types, syntax, and 🟢 🟢 best practices.

---

📌 **1. The Big Five (and Zero)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In modern C++, you must manage the lifecycle of your class. The **Rule of Zero** suggests you should design your classes so that you 🔴 🔴 don't need to manually define any of these.

| Constructor | Syntax Example (``T`` is class name) |
| --- | --- |
| **Default** | ``T() = default;`` |
| **Copy** | ``T(const T& other);`` |
| **Move** | ``T(T&& other) noexcept;`` |
| **Copy Assignment** | ``T& operator=(const T& other);`` |
| **Move Assignment** | ``T& operator=(T&& other) noexcept;`` |

---

📌 **2. Core Constructor Syntax**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

📌 Member Initializer Lists

**Always** use initializer lists instead of assignment inside the constructor body. It is more efficient as it 🔴 🔴 avoids double-initialization.

.. code-block:: cpp

class Player {
    std::string name;
    int health;
public:
    // Preferred Method
    Player(std::string n, int h) : name(std::move(n)), health(h) {} 
};

📌 Delegating Constructors

One constructor can call another constructor in the same class to 🔴 🔴 avoid code duplication.

.. code-block:: cpp

Player() : Player("Guest", 100) {} // Calls the constructor above

📌 Inheriting Constructors

Use ``using`` to pull base class constructors into a derived class.

.. code-block:: cpp

class Boss : public Player {
    using Player::Player; // Boss now has all Player constructors
};

---

⭐ 📌 **3. Modern Keywords**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

📌 ``explicit``

⭐ **Critical Rule:** Mark all single-argument constructors as ``explicit`` to prevent implicit type conversions.

.. code-block:: cpp

class Window {
    explicit Window(int width); 
};

Window w = 10;      // Error! (Implicit conversion blocked)
Window w{10};       // OK (Explicit)

📌 ``delete`` and ``default``

- ``= default``: Tells the compiler to generate the standard version (even if you've defined other constructors).
- ``= delete``: Prevents the compiler from generating a function or allows you to "ban" certain types.

.. code-block:: cpp

class UniqueLogic {
    UniqueLogic(const UniqueLogic&) = delete; // Disable copying
    void process(double d);
    void process(int) = delete;               // Disable calling with int
};

---

⚙️ **4. Uniform Initialization (Braces ``{}``)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modern C++ prefers ``{}`` over ``()`` to prevent the "Most Vexing Parse" and to disallow **narrowing conversions**.

.. code-block:: cpp

int a = 5.5;    // Compiles (a becomes 5)
int b{5.5};     // Compiler Error (Narrowing conversion)

> **Note:** If a class has a ``std::initializer_list`` constructor (like ``std::vector``), brace initialization will prioritize that constructor over others.

---

📌 **5. Move Semantics & ``noexcept``**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When writing **Move Constructors**, always mark them ``noexcept``. This allows STL containers (like ``std::vector``) to move your objects safely during a resize rather than copying them.

.. code-block:: cpp

// Move Constructor
Buffer(Buffer&& other) noexcept 
    : data(other.data), size(other.size) {
    other.data = nullptr; // Leave 'other' in a valid empty state
    other.size = 0;
}

---

💡 **6. 🟢 🟢 Best Practices Checklist**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- [ ] **Rule of Zero:** Use smart pointers and standard containers so you 🔴 🔴 don't have to write any constructors.
- [ ] **Rule of Five:** If you must define a Destructor, you likely need to define all five lifecycle functions.
- [ ] **Prefer ``{}``:** Use brace initialization to catch narrowing errors.
- [ ] **Explicit:** Default to making constructors ``explicit``.
- [ ] **Noexcept:** Always mark move constructors ``noexcept``.
- [ ] **In-class Initializers:** Initialize members at their declaration site for default values.

Would you like me to expand on the **Rule of Five** with a full code example including a raw resource?

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
