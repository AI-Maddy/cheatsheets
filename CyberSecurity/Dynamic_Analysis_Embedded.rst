====================================================================
Dynamic Analysis for Embedded Security
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: Valgrind, AddressSanitizer

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Dynamic Analysis:**

- Test running application
- **Detect:** Memory leaks, use-after-free, race conditions

**Tools:**

✅ **Valgrind:** Memory error detector (x86/ARM)
✅ **AddressSanitizer:** Google's fast memory checker
✅ **ThreadSanitizer:** Data race detector

AddressSanitizer Example
=========================

.. code-block:: c

    // Heap overflow
    int *arr = malloc(10 * sizeof(int));
    arr[10] = 42;  // Out of bounds!

**Compile with ASan:**

.. code-block:: bash

    gcc -fsanitize=address -g firmware.c -o firmware
    ./firmware
    
    # Output:
    # ==1234==ERROR: AddressSanitizer: heap-buffer-overflow
    # WRITE of size 4 at 0x602000000034

Standards
=========

- **Google AddressSanitizer Documentation**

**END OF DOCUMENT**
