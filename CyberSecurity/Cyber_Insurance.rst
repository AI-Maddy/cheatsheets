====================================================================
Cyber Insurance for Embedded Products
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NAIC Cyber Insurance Guidelines

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Cyber Insurance:**

- Covers financial losses from cyber incidents
- **Typical coverage:** Data breach, ransomware, business interruption
- **Embedded-specific:** Product recall, liability for IoT device compromise

Policy Requirements
====================

**Underwriting Checklist:**

✅ Secure development lifecycle (SSDLC)
✅ Penetration testing (annual)
✅ Incident response plan
✅ Encryption (data at rest and in transit)
✅ Patch management process

**Example Premium:**

.. code-block:: text

    IoT Manufacturer (10,000 devices deployed):
    - Coverage: $5,000,000
    - Premium: $50,000/year
    - Deductible: $100,000
    
    Premium factors:
    - Security certifications (Common Criteria, FIPS) → -20% discount
    - No encryption → +50% surcharge
    - Previous breaches → +100% surcharge

Incident Response
==================

**Covered Costs:**

1. Forensic investigation: $50,000-$200,000
2. Legal fees: $100,000+
3. Customer notification: $5/customer
4. Credit monitoring: $20/customer/year
5. Regulatory fines: Up to $1,000,000
6. Product recall: $500,000-$5,000,000

**Example Claim:**

.. code-block:: text

    Incident: Ransomware encrypts smart thermostat cloud backend
    
    Costs:
    - Forensics: $75,000
    - Ransom payment: $100,000 (not covered by most policies)
    - Customer notification (10,000): $50,000
    - Business interruption (7 days): $500,000
    - Legal defense: $150,000
    
    Total: $875,000
    Insurance payout: $775,000 (after $100,000 deductible)

Exam Questions
==============

**Q1: Cyber Insurance vs Security Investment (Hard)**

Is cyber insurance a substitute for security investment?

**Answer:**

**No, complementary:**

- **Security investment:** Preventive (reduce likelihood)
- **Cyber insurance:** Reactive (reduce impact)

**Example:**

Company spends $100,000/year on security:
- Penetration testing: $30,000
- Security tools: $40,000
- Training: $30,000

Residual risk remains → Cyber insurance covers this gap.

**Best Practice:** Security investment + insurance = defense-in-depth.

**Q2: IoT Device Liability (Medium)**

Smart lock manufacturer's devices hacked, homes burgled. Is this covered by cyber insurance?

**Answer:**

**Depends on policy:**

**First-party coverage (your losses):**
- ✅ Forensics, legal defense, customer notification

**Third-party coverage (customer losses):**
- ⚠️  Bodily injury/property damage → General liability (not cyber)
- ✅ Data breach (stolen customer info) → Cyber insurance
- ❌ Burglary losses → Homeowner's insurance (not manufacturer's)

**Recommendation:** Product liability insurance + cyber insurance.

Standards
=========

- **NAIC Model Bulletin:** Cyber insurance guidelines
- **ISO Cyber Insurance Framework**

**END OF DOCUMENT**
