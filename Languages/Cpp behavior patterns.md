**cheatsheet for the most important C++ behavioral design patterns** (Gang of Four + modern C++ idioms, 2025–2026 perspective).

Behavioral patterns focus on **how objects interact and distribute responsibilities**.

| Pattern                  | Intent / When to Use                                                                 | Core Idea / C++ Implementation Notes                                                                 | Modern C++ (11/14/17/20/23) idioms & improvements                                                                 | Typical Code Skeleton (simplified) |
|--------------------------|--------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------|
| **Strategy**             | Define a family of algorithms, encapsulate each one, make them interchangeable      | Context holds Strategy interface pointer/reference; concrete strategies implement algorithm       | Use `std::function`, lambdas, or `std::variant` of strategies; policy-based design common                      | `class Strategy { virtual void execute() = 0; };` <br> `class Context { std::unique_ptr<Strategy> s; };` |
| **Command**              | Encapsulate a request as an object (undo/redo, queuing, logging, macros)            | Command interface + concrete command + invoker + receiver                                            | `std::function<void()>` or lambda-based commands; `std::packaged_task` for async; ranges for macro commands     | `class Command { virtual void execute() = 0; };` <br> `class MacroCommand : public Command { std::vector<std::unique_ptr<Command>> cmds; };` |
| **Observer**             | Define one-to-many dependency; objects notified of state changes                     | Subject maintains list of observers; notify() calls update() on each                                | `std::function` callbacks, signals/slots (Boost.Signals2), `std::vector<std::weak_ptr<Observer>>` to avoid cycles | `class Observer { virtual void update() = 0; };` <br> `class Subject { std::vector<std::weak_ptr<Observer>> obs; };` |
| **State**                | Allow an object to alter its behavior when its internal state changes               | Context delegates to current State object; states transition themselves                              | Use `std::variant<State1, State2, ...>` + `std::visit` (C++17); CRTP for state machine (very clean)               | `class State { virtual void handle() = 0; };` <br> `class Context { std::unique_ptr<State> state; };` |
| **Visitor**              | Separate algorithm from object structure (double dispatch)                          | Element accepts visitor → calls visitor.visit(this); visitor has overloads for each element type     | Use `std::variant` + `std::visit` instead of classic visitor; Acyclic Visitor pattern with CRTP                    | `class Visitor { virtual void visit(ConcreteElement&) = 0; };` <br> `class Element { virtual void accept(Visitor&) = 0; };` |
| **Mediator**             | Define an object that encapsulates how a set of objects interact (reduces coupling)  | Colleagues talk only to mediator; mediator coordinates                                           | Use signals/slots or central event bus; `std::function` callbacks; modern → event queue + coroutines (C++20/23)   | `class Mediator { virtual void notify(Component*, std::string event) = 0; };` |
| **Chain of Responsibility** | Pass request along chain of handlers until one handles it                          | Handler has successor; each decides to handle or pass on                                         | Use `std::function` chain or `std::optional` return; ranges + views for pipeline style                           | `class Handler { std::unique_ptr<Handler> next; virtual bool handle(Request&) = 0; };` |
| **Template Method**      | Define skeleton of algorithm in superclass; let subclasses redefine steps           | Non-virtual skeleton calls virtual “hook” methods                                                 | Use CRTP (Curiously Recurring Template Pattern) instead of inheritance; lambdas for hooks                        | `class AbstractClass { void templateMethod() { step1(); step2(); } virtual void step2() = 0; };` |
| **Iterator**             | Provide way to access elements of aggregate object sequentially                     | Iterator interface + concrete iterator for container                                             | C++11+ → range-based for + `begin()/end()`; C++20 ranges + views; `std::ranges::views`                           | `class Iterator { virtual bool hasNext() = 0; virtual Item next() = 0; };` |
| **Memento**              | Capture & externalize object’s internal state without violating encapsulation       | Originator creates Memento; Caretaker stores it (undo/redo)                                      | Use `std::variant` for state or serialization; modern → `std::any` or CRTP memento                               | `class Memento { /* private state */ };` <br> `class Originator { Memento save() { return Memento(state); } };` |
| **Interpreter**          | Define grammar for simple language & interpreter to interpret sentences             | Abstract Expression + Terminal/Nonterminal expressions                                           | Rarely used today; replaced by parser generators (ANTLR, PEGTL) or DSLs (embedded languages)                    | `class Expression { virtual bool interpret(Context&) = 0; };` |

### Modern C++ Behavioral Patterns – Recommended Idioms (2025–2026)

| Classic Pattern       | Modern C++ Replacement / Improvement                          | Why Better / Cleaner                                                                 |
|-----------------------|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Strategy              | `std::function`, lambdas, policy-based design                  | No inheritance tax, compile-time composition                                         |
| Command               | `std::function<void()>` or `std::packaged_task`                | Lambda-based, async-ready, no boilerplate classes                                    |
| Observer              | Signals & slots (Boost.Signals2), `std::function` + `weak_ptr` | No manual list management, cycle-safe, C++20 coroutines possible                     |
| State                 | `std::variant<State1, State2, ...>` + `std::visit`             | No inheritance, exhaustive handling, type-safe                                       |
| Visitor               | `std::variant` + `std::visit` or Acyclic Visitor with CRTP     | Avoids double-dispatch boilerplate, better with variants                             |
| Chain of Responsibility | Range-based pipeline or `std::optional` return chain          | Functional style, composable, no linked-list overhead                                |
| Template Method       | CRTP + lambdas or `std::function` hooks                        | Avoid inheritance, more flexible                                                     |

### Quick Decision Table – Which Pattern When?

| Need to …                              | Recommended Pattern (Classic) | Modern C++ Preference (2025–2026)       |
|----------------------------------------|-------------------------------|------------------------------------------|
| Swap algorithms at runtime             | Strategy                      | `std::function` / lambdas / policy       |
| Queue, undo, log commands              | Command                       | `std::function<void()>` + lambda capture |
| Notify many objects of state change    | Observer                      | Signals/slots or callback list           |
| Change behavior based on internal state| State                         | `std::variant` + `std::visit`            |
| Add new operations without changing classes | Visitor                  | `std::variant` + overloads               |
| Encapsulate object interaction         | Mediator                      | Event bus / central dispatcher           |
| Pass request until handled             | Chain of Responsibility       | Range views or functional pipeline       |
| Define skeleton with customizable steps| Template Method               | CRTP + lambdas                           |

### One-liner Modern C++ Advice (Behavioral)

- Prefer **composition over inheritance** (most GoF behavioral patterns rely on inheritance → modern C++ avoids it)
- Use **std::function + lambdas** for Strategy/Command/Observer/Template Method
- Use **std::variant + std::visit** for State & Visitor
- Use **ranges / views** for Chain of Responsibility pipelines
- Use **CRTP** when you want static polymorphism without vtables
- Prefer **signals & slots** libraries when Observer gets complex

This cheatsheet covers ~90% of behavioral pattern usage in modern C++ projects.

Good luck with your design pattern work!