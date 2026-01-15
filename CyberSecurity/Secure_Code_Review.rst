====================================================================
Secure Code Review for Embedded Systems
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: OWASP Code Review Guide, CERT

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Code Review Checklist:**

✅ **Input validation:** Bounds checking, sanitization
✅ **Crypto:** No hardcoded keys, strong algorithms
✅ **Authentication:** No default passwords
✅ **Memory safety:** No buffer overflows, use-after-free

Common Vulnerabilities
=======================

**1. Hardcoded Credentials**

.. code-block:: c

    // BAD
    const char *password = "admin123";
    
    // GOOD
    const char *password = getenv("ADMIN_PASSWORD");

**2. Integer Overflow**

.. code-block:: c

    // BAD
    uint16_t size = user_input_size;  // Can be 65535
    char *buf = malloc(size + 10);  // Wraps to 9 if size=65535!
    
    // GOOD
    if (size > MAX_SIZE - 10) return -1;
    char *buf = malloc(size + 10);

Standards
=========

- **OWASP Code Review Guide**
- **CERT C Secure Coding**

**END OF DOCUMENT**
