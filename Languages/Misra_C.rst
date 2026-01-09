================================================================================
🛡️ MISRA C:2023 – Safety-Critical Code Cheatsheet
================================================================================

A **practical, quick-reference guide** for the **most important & frequently
violated MISRA C:2023 rules** used in safety-critical systems (automotive,
aerospace, medical, industrial).

**Focus:** Mandatory & Required rules that cause the most trouble in real projects.

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

Quick Legend – MISRA C:2023
================================================================================

📋 **Rule Classification:**

.. code-block:: text

   Dir = Directive       (process / documentation related)
   R   = Rule            (code / compile-time enforcement)

🔴 **Compliance Levels:**

   🔴 MANDATORY  → must comply (ZERO deviations allowed)
   🟡 REQUIRED   → shall comply (deviation possible, must be justified)
   🟢 ADVISORY   → should follow (good practice, not enforced)

### Most Important / Most Painful MISRA Rules – Quick Reference

| #  | Rule ID | Category | Requirement | Severity | Violation Freq |
|:--:|---------|----------|-------------|:--------:|:--------------:|
| 1  | Dir 4.4 | Language | No compiler extensions | 🟡 Required | ⭐⭐⭐⭐⭐ |
| 2  | R 1.3 | Fundamentals | 🔴 No undefined behavior | 🔴 MANDATORY | ⭐⭐⭐⭐⭐ |
| 3  | R 1.1 | Fundamentals | No C standard violations | 🔴 MANDATORY | ⭐⭐⭐⭐ |
| 4  | R 1.5 | Types | No bit-fields (bool/enum/float) | 🟡 Required | ⭐⭐⭐ |
| 5  | R 5.1 | Declarations | External IDs distinct (31+ chars) | 🟡 Required | ⭐⭐⭐ |
| 6  | R 8.2 | Declarations | 🟢 Function prototypes in scope | 🟡 Required | ⭐⭐⭐⭐ |
| 7  | R 8.4 | Declarations | Exactly one function declaration | 🟡 Required | ⭐⭐⭐ |
| 8  | R 9.1 | Initialization | 🔴 Initialize all auto variables | 🔴 MANDATORY | ⭐⭐⭐⭐⭐ |
| 9  | R 9.2 | Initialization | No init side effects | 🟡 Required | ⭐⭐ |
| 10 | R 10.1 | Expressions | 🟢 Essential type compatibility | 🟡 Required | ⭐⭐⭐⭐ |
| 11 | R 10.3 | Expressions | No narrowing assignments | 🟡 Required | ⭐⭐⭐⭐ |
| 12 | R 10.4 | Expressions | Binary ops same essential type | 🟡 Required | ⭐⭐⭐ |
| 13 | R 10.8 | Expressions | No cast to narrower type | 🟡 Required | ⭐⭐⭐ |
| 14 | R 11.3 | Pointers | No pointer type changes | 🟡 Required | ⭐⭐⭐⭐ |
| 15 | R 11.4 | Pointers | Never remove const/volatile | 🟡 Required | ⭐⭐⭐ |
| 16 | R 11.5 | Pointers | No void* → object* without cast | 🟡 Required | ⭐⭐ |
| 17 | R 11.8 | Pointers | Never remove const from object | 🟡 Required | ⭐⭐⭐ |
| 18 | R 11.9 | Pointers | Only NULL for null pointer | 🟡 Required | ⭐⭐⭐ |
| 19 | R 13.2 | Side Effects | No side effects in && / \|\| RHS | 🟡 Required | ⭐⭐⭐ |
| 20 | R 14.4 | Control Flow | No goto | 🟡 Required | ⭐⭐⭐⭐ |
| 21 | R 15.1 | Control Flow | No goto (duplicate) | 🟡 Required | ⭐⭐⭐⭐ |
| 22 | R 15.5 | Control Flow | Single exit point | 🟢 Advisory | ⭐⭐⭐ |
| 23 | R 16.3 | Switch | 🔴 Explicit break in cases | 🟡 Required | ⭐⭐⭐⭐⭐ |
| 24 | R 16.4 | Switch | Default case required | 🟡 Required | ⭐⭐⭐⭐ |
| 25 | R 18.1 | Loops | Well-bounded loops | 🟡 Required | ⭐⭐⭐ |
| 26 | R 13.5 | Side Effects | No side effects in && / \|\| | 🟡 Required | ⭐⭐⭐ |
| 27 | R 10.6 | Expressions | Parenthesize wide assignments | 🟡 Required | ⭐⭐⭐ |
| 28 | R 19.2 | Data Structures | 🔴 Never use unions | 🟢 Advisory | ⭐⭐⭐⭐ |
| 29 | R 20.1 | Preprocessor | #include proper order | 🟡 Required | ⭐⭐ |
| 30 | R 20.4 | Preprocessor | Don't redefine keywords | 🟡 Required | ⭐⭐ |
| 31 | R 20.7 | Preprocessor | 🔴 Parenthesize macro params | 🟡 Required | ⭐⭐⭐⭐ |
| 32 | R 20.10 | Preprocessor | No variadic macros | 🟡 Required | ⭐⭐ |
| 33 | R 21.1 | Std Library | Don't redefine std functions | 🟡 Required | ⭐⭐ |
| 34 | R 21.6 | Std Library | No printf/scanf | 🟡 Required | ⭐⭐⭐ |
| 35 | R 22.11 | Multithreading | Destroy mutexes | 🟡 Required | ⭐⭐ |
| 36 | R 22.13 | Multithreading | Join/detach threads | 🟡 Required | ⭐⭐ |


================================================================================
1️⃣ TOP 10 MUST-KNOW RULES (80% of violations)
================================================================================

✅ **R 1.3** 🔴 MANDATORY
   No undefined or critical unspecified behavior
   💥 Impact: Prevents crashes, memory corruption
   
✅ **R 9.1** 🔴 MANDATORY  
   All automatic variables MUST be initialized
   💥 Impact: Eliminates random garbage values
   
✅ **R 16.3** 🟡 REQUIRED
   Explicit break in every switch case
   💥 Impact: Prevents accidental fall-through bugs
   
✅ **R 8.2** 🟡 REQUIRED
   Function prototypes required in scope
   💥 Impact: Enforces type checking
   
✅ **R 10.1** 🟡 REQUIRED
   Essential type compatibility strict
   💥 Impact: Prevents silent type promotion bugs
   
✅ **R 11.3 / 11.8** 🟡 REQUIRED
   Pointer casting & const safety
   💥 Impact: Prevents aliasing bugs
   
✅ **R 20.7** 🟡 REQUIRED
   Parenthesize macro parameters
   💥 Impact: Prevents operator precedence disasters
   
✅ **R 13.2** 🟡 REQUIRED
   No side effects in && / || right operand
   💥 Impact: Predictable behavior, avoids hidden state changes
   
✅ **R 18.1** 🟡 REQUIRED
   Well-bounded loops only
   💥 Impact: Prevents infinite loops, watchdog resets
   
✅ **Dir 4.4** 🟡 REQUIRED
   No compiler extensions
   💥 Impact: Portable code, standards compliance


================================================================================
2️⃣ VIOLATION PATTERNS & FIXES
================================================================================

🔴 **BAD #1: Uninitialized Variables (R 9.1)**

.. code-block:: c

   int main(void) {
       int x;              // 🔴 VIOLATION – no initialization
       x = x + 5;          // x is garbage!
       return x;
   }

✅ **FIX:**

.. code-block:: c

   int main(void) {
       int x = 0;          // 🟢 GOOD – initialized
       x = x + 5;
       return x;
   }

---

🔴 **BAD #2: Implicit Fall-Through (R 16.3)**

.. code-block:: c

   switch(alarm_type) {
       case FIRE:
           activate_alarm();     // 🔴 No break!
       case SMOKE:               // Falls through!
           sound_buzzer();
           break;
   }

✅ **FIX:**

.. code-block:: c

   switch(alarm_type) {
       case FIRE:
           activate_alarm();
           break;                // 🟢 Explicit break
       case SMOKE:
           sound_buzzer();
           break;                // 🟢 Explicit break
       default:                  // 🟢 Required (R 16.4)
           error_handler();
           break;
   }

---

🔴 **BAD #3: Unparenthesized Macros (R 20.7)**

.. code-block:: c

   #define DOUBLE(x) x * 2       // 🔴 VIOLATION

   int result = DOUBLE(3 + 4);   // Expands: 3 + 4 * 2 = 11 ❌
                                 // Expected: (3 + 4) * 2 = 14 ✓

✅ **FIX:**

.. code-block:: c

   #define DOUBLE(x) ((x) * 2)   // 🟢 GOOD – parenthesized

   int result = DOUBLE(3 + 4);   // Expands: ((3 + 4) * 2) = 14 ✓

---

🔴 **BAD #4: Side Effects in Logical Ops (R 13.2)**

.. code-block:: c

   int count = 0;
   if (value > 100 && ++count < 10) {  // 🔴 Hidden side effect!
       process();
   }

✅ **FIX:**

.. code-block:: c

   int count = 0;
   if (value > 100) {                  // 🟢 Explicit, obvious
       if (++count < 10) {
           process();
       }
   }

---

🔴 **BAD #5: Pointer Type Violations (R 11.3)**

.. code-block:: c

   int *p = malloc(sizeof(int) * 10);
   char *c = (char *)p;        // 🔴 Type changed! Aliasing bug
   *c = 'x';                   // Corrupts int array

✅ **FIX:**

.. code-block:: c

   // Either use correct type from start:
   unsigned char *bytes = malloc(10);
   bytes[0] = 'x';             // 🟢 GOOD
   
   // Or intentional cast with clear comment:
   int *p = malloc(sizeof(int) * 10);
   unsigned char *view = (unsigned char *)p;  // 🟢 Explicit intent
   view[0] = 0xFF;

---

🔴 **BAD #6: Type Narrowing (R 10.3)**

.. code-block:: c

   int big_value = 300000;
   uint8_t small = big_value;  // 🔴 Silently truncates!

✅ **FIX:**

.. code-block:: c

   int big_value = 300000;
   
   // Check range first:
   if (big_value >= 0 && big_value <= 255) {
       uint8_t small = (uint8_t)big_value;  // 🟢 Safe
   }


================================================================================
3️⃣ COMPLIANCE TOOLS
================================================================================

🛠️ **Static Analysis Tools:**

| Tool | Free | MISRA Support | Recommendation |
|------|:----:|:-------------:|---|
| 🥇 PC-Lint | ❌ | ⭐⭐⭐⭐⭐ | Industry standard, automotive |
| 🥈 Polyspace | ❌ | ⭐⭐⭐⭐⭐ | Formal verification |
| 🥉 Clang-Tidy | ✅ | ⭐⭐⭐ | Good for open-source |
| SonarQube | ✅ | ⭐⭐⭐ | DevOps-friendly |
| Cppcheck | ✅ | ⭐⭐⭐ | Quick baseline |
| Coverity | ❌ | ⭐⭐⭐⭐ | Enterprise |

🎯 **Strict Compiler Flags (Always Use):**

.. code-block:: bash

   gcc -Wall -Wextra -Wpedantic \
       -Wshadow -Wstrict-prototypes \
       -Wwrite-strings -Wconversion \
       -Wdouble-promotion -Wfloat-equal \
       -std=c99 -O2 myfile.c

📋 **Pre-Commit Checklist:**

.. code-block:: bash

   # 1. Check uninitialized variables
   grep -rn "^\s*[a-zA-Z_][a-zA-Z0-9_]*\s" src/ | grep -v "="
   
   # 2. Check fall-through in switch
   grep -A1 "case " src/ | grep -v "break\|default"
   
   # 3. Check macros are parenthesized
   grep "#define.*(" src/ | grep -v "((.*)"


================================================================================
4️⃣ SEVERITY LEVELS AT A GLANCE
================================================================================

🔴 **MANDATORY (Zero Exceptions):**
   ├─ R 1.3   – No undefined behavior
   ├─ R 9.1   – Initialize variables
   ├─ R 16.3  – Explicit switch breaks
   └─ R 1.1   – C standard compliance

🟡 **REQUIRED (Justified Deviations OK):**
   ├─ R 8.2   – Function prototypes
   ├─ R 10.x  – Essential type rules
   ├─ R 11.x  – Pointer safety
   ├─ R 20.7  – Macro parenthesization
   └─ R 13.2  – No hidden side effects

🟢 **ADVISORY (Best Practice):**
   ├─ R 15.5  – Single exit point
   ├─ R 19.2  – Avoid unions
   └─ (Most Level 2-3 rules)


================================================================================
5️⃣ RULE CATEGORIES QUICK REFERENCE
================================================================================

🔧 **Language Fundamentals** (R 1.x)
   → Foundation layer, defines basic compliance

🏷️ **Declarations** (R 5.x, R 8.x)
   → Names, scoping, function declarations

📊 **Initialization** (R 9.x)
   → All variables must have defined values

🧮 **Expressions & Types** (R 10.x)
   → Strict type checking, no silent conversions

⚡ **Pointers** (R 11.x)
   → Most dangerous area – aliasing, casting

🔀 **Control Flow** (R 14.x, R 15.x, R 16.x, R 18.x)
   → goto/switch/loop safety

😈 **Side Effects** (R 13.x)
   → Predictable evaluation order

🏗️ **Data Structures** (R 19.x)
   → Unions forbidden, unions dangerous

📌 **Preprocessor** (R 20.x)
   → Macro safety and consistency

📚 **Standard Library** (R 21.x)
   → Disable unsafe functions (printf, malloc)

🧵 **Multithreading** (R 22.x)
   → C11+ thread safety


================================================================================

🚀 **BOTTOM LINE**
================================================================================

**Master these 10 to solve 80% of MISRA violations:**

   1️⃣ R 1.3  (undefined behavior)
   2️⃣ R 9.1  (initialize variables)
   3️⃣ R 16.3 (explicit switch breaks)
   4️⃣ R 8.2  (function prototypes)
   5️⃣ R 10.x (essential types)
   6️⃣ R 11.x (pointer safety)
   7️⃣ R 20.7 (macro parameters)
   8️⃣ R 13.2 (no side effects)
   9️⃣ R 18.1 (well-bounded loops)
   🔟 Dir 4.4 (no extensions)

**Use a static analyzer** → automates checks, saves hours

**Enable compiler warnings** → catches 50% before analyzer

Good luck! Stay safe! 🛡️

================================================================================

**Last updated:** January 2026