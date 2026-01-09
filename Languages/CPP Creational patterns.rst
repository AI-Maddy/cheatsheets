
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for Creational Design Patterns in C++** (Gang of Four + modern C++ idioms, 2025–2026 🟢 🟢 best practices).

Creational patterns deal with **object creation mechanisms**, trying to create objects in a manner suitable to the situation.

| Pattern                  | Intent / Problem it solves                                                                 | Classic GoF Approach (C++98/03)                              | Modern C++ (11/14/17/20/23) preferred style & improvements                                                                 | Typical Code Skeleton (modern style) |
|--------------------------|--------------------------------------------------------------------------------------------|---------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| **Singleton**            | Ensure a class has only one instance and provide global access point                       | Static instance + private constructor + double-checked locking | ``static`` local variable (Meyers' Singleton), ``std::call_once``, ``std::once_flag`` or ``inline static`` (C++17)                 | ``class Singleton { public: static Singleton& instance() { static Singleton s; return s; } private: Singleton(); };`` |
| **Factory Method**       | Define an interface for creating an object, but let subclasses decide which class to instantiate | Virtual ``createProduct()`` in Creator, overridden in ConcreteCreator | Use ``std::function`` or lambdas for factory; CRTP for static polymorphism; ``std::unique_ptr`` return type                     | ``class Product { virtual ~Product() = default; };`` <br> ``class Creator { public: virtual std::unique_ptr<Product> create() = 0; };`` |
| **Abstract Factory**     | Provide an interface for creating families of related/dependent objects without specifying concrete classes | AbstractFactory interface with multiple creation methods      | Return ``std::unique_ptr`` or ``std::shared_ptr``; factory registry with ``std::function``; dependency injection style           | ``class AbstractFactory { virtual std::unique_ptr<Button> createButton() = 0; virtual std::unique_ptr<Checkbox> createCheckbox() = 0; };`` |
| **Builder**              | Separate construction of complex object from its representation (step-by-step, immutable) | Director + Builder interface + ConcreteBuilder                | Fluent builder (method chaining), ``std::optional`` for optional fields, designated initializers (C++20), ``std::span`` for lists | ``class ProductBuilder { public: ProductBuilder& setA(int) &; ProductBuilder&& setB(std::string) &&; Product build(); };`` |
| **Prototype**            | Create new objects by cloning existing ones (🔴 🔴 avoid expensive creation)                     | ``clone()`` method returning new object (deep copy)             | ``std::unique_ptr`` return type, CRTP for ``clone_impl()``, ``std::enable_shared_from_this`` if shared ownership needed          | ``class Prototype { public: virtual std::unique_ptr<Prototype> clone() const = 0; };`` <br> ``class Concrete : public Prototype { std::unique_ptr<Prototype> clone() const override { return std::make_unique<Concrete>(*this); } };`` |

💡 Modern C++ Creational Patterns – 🟢 🟢 Best Practices Summary (2025–2026)

| Pattern                  | Recommended Modern C++ Style (C++17/20/23)                               | Key Advantages / Why Better                                                                 | 🔴 🔴 Avoid / Deprecated in Modern Code |
|--------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **Singleton**            | Meyers' Singleton (``static`` local) or ``inline static`` member            | Thread-safe by language guarantee, no double-checked locking needed                         | Manual double-checked locking, global/namespace statics |
| **Factory Method**       | ``std::function`` factory or CRTP static factory                           | No vtable overhead, compile-time polymorphism possible                                      | Raw pointer returns, manual ``new``/``delete`` |
| **Abstract Factory**     | Return ``std::unique_ptr`` / ``std::shared_ptr``, factory registry           | RAII, ownership clear, easy dependency injection                                            | Manual memory management, concrete class names in client code |
| **Builder**              | Fluent interface (method chaining) + ``std::move`` semantics               | Readable, immutable objects, optional fields via ``std::optional``                            | Telescoping constructor hell, many overloaded constructors |
| **Prototype**            | Return ``std::unique_ptr<T>`` from ``clone()``, CRTP base class              | Type-safe, no slicing, easy deep copy with ``=default`` copy ctor                             | Raw pointer ``clone()``, manual deep copy logic |

🏗️ Quick Decision Table – Which Creational Pattern to Use When

| Situation / Requirement                          | Recommended Pattern (Classic) | Modern C++ Preference (2025–2026)              | Why |
|--------------------------------------------------|-------------------------------|------------------------------------------------|-----|
| Only one instance ever needed                    | Singleton                     | Meyers' Singleton or ``inline static``           | Thread-safe & simple |
| Want to defer concrete class choice to subclass  | Factory Method                | ``std::function`` factory or CRTP                | Flexible, no vtable cost |
| Need families of related objects                 | Abstract Factory              | Smart-pointer returning factories              | RAII, dependency injection friendly |
| Complex object construction with many options    | Builder                       | Fluent builder + ``std::optional`` / designated init | Readable, immutable result |
| Expensive object creation → want to clone instead| Prototype                     | ``std::unique_ptr`` + CRTP clone                 | 🔴 🔴 Avoids expensive setup |

⚙️ One-liner Modern C++ Creational Advice

- Prefer **smart pointers** (``std::unique_ptr`` / ``std::shared_ptr``) for all factory/builder/prototype returns
- 🔴 🔴 Avoid raw ``new``/``delete`` — always use ``std::make_unique`` / ``std::make_shared``
- Use **CRTP** when you want static polymorphism without virtual functions
- Prefer **named constructors** / factory functions over public constructors
- Use **designated initializers** (C++20) or fluent builder for complex initialization
- **Never** expose concrete classes in public APIs — hide behind factory / interface

This cheatsheet covers ~95% of creational pattern usage in modern C++ projects (embedded, games, servers, libraries, automotive, etc.).

🟢 🟢 Good luck with your C++ design!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
