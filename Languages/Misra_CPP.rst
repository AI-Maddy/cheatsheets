================================================================================
🛡️ MISRA C++:2023 – Safety-Critical Modern C++ Cheatsheet
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

Modern successor to MISRA C++:2008 ✅ Pragmatic approach to C++17 safety-critical development combining MISRA rigor with AUTOSAR flexibility.

Quick Legend – MISRA C++:2023
================================================================================

📋 **Rule Classification:**
   Dir = Directive (design/process guidance)
   R = Rule (code enforcement, checkable by tools)

🔴 **Compliance Levels:**
   🔴 MANDATORY → must comply (ZERO deviations allowed)
   🟡 REQUIRED → shall comply (deviations possible, must be justified & documented)
   🟢 ADVISORY → should follow (good practice, flexibility permitted)

**What This Means:**
   ⭐ = Violation frequency in 2024-2026 projects
   💥 = Impact severity when violated


Current Status – January 2026
================================================================================

✅ **Version:** MISRA C++:2023 (October 2023 release)
✅ **Language:** C++17 (ISO/IEC 14882:2017)
✅ **Total Guidelines:** ~179 rules + 4 directives
✅ **Philosophy:** Much more pragmatic than 2008 version
✅ **Updates from 2008:**
   🟢 Exceptions now ALLOWED (was banned)
   🟢 Multiple returns ALLOWED (no forced SESE)
   🟢 STL more usable (still restricted)
   🟢 Templates more practical (still limited)
   🟢 AUTOSAR C++14 integration
   
🎯 **Best For:** New safety-critical C++17 projects

### Most Important / Most Frequently Checked Rules in MISRA C++:2023

| #   | Category                     | Rule ID example              | Description / Main Requirement                                                                                  | Severity      | Pain level (2024–2026 projects) |
|-----|------------------------------|------------------------------|------------------------------------------------------------------------------------------------------------------|---------------|---------------------------------|
| 1   | Fundamental / UB             | **6.0.x / 11.6.x**           | No **undefined behavior** – very strong umbrella rule (like old R1.3 in C)                                      | Mandatory/Req | ★★★★★                          |
| 2   | Initialization               | **11.6.2**                   | Object value **shall not** be read before it is **set** (no use of uninitialized variables)                    | Required      | ★★★★★                          |
| 3   | Type safety                  | **10.x.y** series            | Very strict **type conversion/promotion** rules (similar to MISRA C 10.x but adapted to C++)                    | Required      | ★★★★                           |
| 4   | Pointers / References        | **11.x** family              | Very restricted pointer arithmetic, casts, `reinterpret_cast` usage, etc.                                       | Required      | ★★★★                           |
| 5   | Lifetime / dangling          | **11.3.x / 18.x**            | No **dangling pointers/references**, strict lifetime rules (very important in modern C++)                      | Required      | ★★★★                           |
| 6   | Exceptions                   | **15.x** series              | **Exceptions are allowed** (big change!) but with many restrictions (no throwing in destructors, etc.)         | Mixed         | ★★★                            |
| 7   | RAII & Resource management   | **15.5.x / 18.x**            | Prefer **RAII**, prohibit raw `new/delete` in many contexts, prefer smart pointers                              | Required/Adv  | ★★★★                           |
| 8   | Loops                        | **9.x / 18.x**               | All loops shall be **well-bounded**, no infinite loops without clear escape                                    | Required      | ★★★                            |
| 9   | Control flow                 | **9.6.x**                    | No **goto**, restricted **continue/break** usage (more relaxed than 2008)                                      | Required      | ★★★                            |
| 10  | Switch / Variants            | **9.7.x**                    | Every **switch** shall have **default**, no implicit fall-through without comment                               | Required      | ★★★★                           |
| 11  | Single point of exit         | —                            | **No longer required**! Multiple returns are allowed (huge improvement over 2008)                              | —             | ★                              |
| 12  | Virtual functions            | **17.x**                     | Heavy restrictions on **virtual functions**, multiple inheritance, dynamic dispatch in many contexts          | Required      | ★★★                            |
| 13  | Templates                    | **19.x**                     | Very restricted template usage (often only very simple templates are permitted)                                 | Required      | ★★★★                           |
| 14  | Concurrency                  | **22.x** (C++17)             | Rules for atomics, mutexes, thread safety (similar to MISRA C AMD4 additions)                                   | Required      | ★★                             |
| 15  | STL usage                    | **20.x**                     | Very restricted STL usage – many containers/algorithms are banned or heavily restricted                         | Required      | ★★★★                           |
| 16  | `const` / `constexpr`        | Various                      | Strong encouragement of **const**/**constexpr** – many rules push toward immutability                           | Advisory/Req  | ★★★                            |
| 17  | `auto`                       | **10.x**                     | Very restricted use of **auto** (often only when type is obvious from context)                                 | Required      | ★★★                            |
| 18  | Lambdas                      | **19.x / 5.x**               | Lambdas allowed but with strong restrictions (no capture-by-reference in many cases, etc.)                     | Required      | ★★★                            |
| 19  | Macros                       | **20.x**                     | Very strong restrictions – almost same as MISRA C (parenthesize, no token pasting abuse, etc.)                 | Required      | ★★★★                           |
| 20  | `union` / `variant`          | **12.x**                     | Unions generally **discouraged** or heavily restricted (type punning is dangerous)                              | Advisory/Req  | ★★★                            |

### Top 10 Most Painful / Frequently Violated Rules (2024–2026 projects)

1. **Initialization & UB** (11.6.x family) – uninitialized objects
2. **Type conversions & casts** (10.x & 11.x series) – very strict
3. **Dangling pointers/references** – lifetime rules are tough with modern C++
4. **Raw new/delete** – must use smart pointers almost everywhere
5. **STL usage** – many containers (vector, map, string…) restricted
6. **Templates & auto** – much more restricted than most modern codebases
7. **Virtual functions & inheritance** – often forces interface-based design
8. **Switch fall-through** – same classic problem as in C
9. **Macros** – same pain as MISRA C
10. **Lambdas & captures** – especially capture-by-reference

### Quick Comparison: MISRA C++:2008 vs 2023

| Aspect                        | MISRA C++:2008               | MISRA C++:2023                     |
|-------------------------------|------------------------------|-------------------------------------|
| Language version              | C++03                        | **C++17**                           |
| Exceptions                    | Almost completely banned     | **Allowed** (with restrictions)     |
| Multiple return statements    | Strongly discouraged         | **Allowed**                         |
| STL                           | Very limited                 | Still limited, but more usable      |
| Templates                     | Very restricted              | Still restricted, but better        |
| Base philosophy               | Very conservative            | Much more pragmatic                 |
| Relation to AUTOSAR           | Almost none                  | **Heavily based** on AUTOSAR C++14  |

**Bottom line (2026)**:  
If you're starting a new safety-critical C++17 project → **use MISRA C++:2023**  
If you're maintaining old code → expect significant work when migrating from 2008.

Good luck — and prepare for many discussions about STL, templates, lambdas and smart pointers! 🚀