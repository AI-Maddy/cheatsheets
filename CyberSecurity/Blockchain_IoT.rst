====================================================================
Blockchain for IoT Security
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEEE 2418.1

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Blockchain for IoT:**

- **Immutable audit log:** Device actions recorded on blockchain
- **Decentralized identity:** No central authority
- **Smart contracts:** Automated security policies

**Challenges:**

- High power consumption (PoW consensus)
- Latency (block confirmation time)
- Scalability (limited TPS)

Use Case: Supply Chain Security
=================================

.. code-block:: python

    # Track pharmaceutical cold-chain with blockchain
    
    from web3 import Web3
    
    # Connect to Ethereum
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    
    # Smart contract for temperature monitoring
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # IoT sensor records temperature
    def record_temperature(sensor_id, temp_celsius):
        tx = contract.functions.recordTemperature(
            sensor_id,
            temp_celsius,
            int(time.time())
        ).transact({'from': sensor_address})
        
        # Wait for confirmation
        w3.eth.wait_for_transaction_receipt(tx)

**Benefits:**

- Temperature history immutable (cannot be tampered)
- Auditable by regulators
- Automatic alerts if cold-chain broken

Exam Questions
==============

**Q1: Blockchain vs Traditional Database (Medium)**

When to use blockchain for IoT vs centralized database?

**Answer:**

**Use Blockchain when:**
- Multiple untrusted parties (supply chain)
- Audit trail critical (compliance)
- No central authority desired

**Use Database when:**
- Single organization
- Real-time requirements (<1 sec latency)
- High transaction volume (>1000 TPS)

Standards
=========

- **IEEE 2418.1:** Blockchain for IoT

**END OF DOCUMENT**
