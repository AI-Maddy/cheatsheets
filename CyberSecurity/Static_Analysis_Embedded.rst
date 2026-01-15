====================================================================
Static Analysis for Embedded Security
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: MISRA C, CERT C

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Static Analysis:**

- Analyze source code without executing
- **Find:** Buffer overflows, null pointer dereferences, data races

**Tools:**

✅ **Coverity:** Commercial, comprehensive
✅ **Clang Static Analyzer:** Open-source
✅ **Cppcheck:** Lightweight C/C++ checker

Example: Buffer Overflow Detection
====================================

.. code-block:: c

    // Vulnerable code
    void process_input(char *input) {
        char buffer[64];
        strcpy(buffer, input);  // No bounds check!
    }

**Cppcheck detects:**

.. code-block:: bash

    $ cppcheck firmware.c
    [firmware.c:3]: (error) Buffer overflow: strcpy

**Fix:**

.. code-block:: c

    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';

Standards
=========

- **MISRA C:2012**
- **CERT C Secure Coding Standard**

**END OF DOCUMENT**
