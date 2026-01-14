✈️ **Aircraft Services Architect — Preparation Keywords & Study Guide**
═══════════════════════════════════════════════════════════════════════════

**Role:** Aircraft Services Architect @ PAC (Portland, 2026)  
**Focus:** Safety-critical avionics systems, security assurance, cloud-native aircraft infrastructure  
**Certification Path:** DO-178C, ED-203A, SAFe Agile, Linux kernel expertise

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════════════

🎯 **INTRODUCTION**
───────────────────

This comprehensive study guide covers **essential keywords, frameworks, and technical 
domains** for the Aircraft Services Architect role. Focus areas include safety-critical 
software certification, cybersecurity assurance, modern avionics architecture, and 
technical leadership in aerospace systems.

**Target Role Competencies:**

✅ Safety & security compliance (DO-178C, ED-203A)  
✅ Modern aircraft system architecture (cloud-native, virtualization)  
✅ Secure lifecycle management (OTA updates, Secure Boot, PKI)  
✅ Agile at scale (SAFe framework for aerospace)  
✅ Technical leadership & OEM collaboration

════════════════════════════════════════════════════════════════════════════

🛡️ **SAFETY & SECURITY COMPLIANCE** (Core Focus)
─────────────────────────────────────────────────

**Safety Standards:**

✈️ **DO-178C (ED-12C)**  
   *Software Considerations in Airborne Systems and Equipment Certification*

   📊 **Design Assurance Levels (DAL):**
   
   | Level | Failure Condition | Examples | Focus for Role |
   |:------|:------------------|:---------|:---------------|
   | **DAL A** | Catastrophic | Flight control, FADEC | Full rigor |
   | **DAL B** | Hazardous | Navigation, autopilot | High rigor |
   | **DAL C** | Major | Communication systems | Medium rigor |
   | **DAL D** | Minor | Passenger info systems | **⭐ Study focus** |
   | **DAL E** | No safety effect | Entertainment systems | **⭐ Study focus** |

   🎯 **Key Objectives for DAL D/E:**
   
   ✅ High-level requirements compliance  
   ✅ Low-level requirements compliance  
   ✅ Source code compliance (simpler than DAL A-C)  
   ✅ Testing requirements (reduced MC/DC for DAL D/E)  
   ✅ Traceability between requirements → design → code → tests

   **Why DAL D/E matters for Aircraft Services:**  
   → IFE (In-Flight Entertainment)  
   → Passenger connectivity systems  
   → Non-critical aircraft services  
   → Onboard e-commerce platforms

**Security Standards:**

🔐 **ED-203A / DO-356A**  
   *Airworthiness Security Process Specification / Airworthiness Security Methods*

   📊 **Security Assurance Levels (SAL 1–3):**
   
   | SAL | Threat Model | Attacker Profile | Verification Rigor |
   |:----|:-------------|:-----------------|:-------------------|
   | **SAL 1** | 🟢 Casual/Coincidental | Untrained, opportunistic | Basic testing |
   | **SAL 2** | 🟡 Intentional/Simple | Trained, limited resources | Security analysis |
   | **SAL 3** | 🔴 Sophisticated/Determined | Expert, significant resources | **Independent review** |

   🎯 **SAL 1** (Protection against casual violations):
   - Passenger attempting unauthorized network access
   - Accidental misconfiguration exposing services
   - Basic input validation failures
   
   🎯 **SAL 2** (Protection against intentional violations, simple means):
   - Insider threat with limited expertise
   - Off-the-shelf hacking tools
   - Social engineering attacks
   - Network sniffing attempts
   
   🎯 **SAL 3** (High assurance against sophisticated attacks):
   - Nation-state actors or organized crime
   - Custom exploit development
   - Zero-day vulnerability exploitation
   - Hardware tampering attempts
   - **Requires extensive evidence + independent security reviews**

**Architecture Security:**

🏗️ **Domain & Data Segregation**  
   Keeping non-critical systems (IFE, passenger services) isolated from flight-critical systems

   ```
   AIRCRAFT NETWORK ARCHITECTURE (Simplified):
   
   ┌─────────────────────────────────────────────────────────────┐
   │ FLIGHT-CRITICAL DOMAIN (ARINC 664 P10)                      │
   │ ├─ Flight Control Systems (DAL A)                           │
   │ ├─ Engine FADEC (DAL A)                                     │
   │ └─ Navigation Systems (DAL B)                               │
   │    ⚠️  NO CONNECTIVITY TO PASSENGER NETWORKS                │
   └─────────────────────────────────────────────────────────────┘
              │ One-Way Data Flow (if any) │
              ▼                             ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ INFORMATION SERVICES DOMAIN (ARINC 664 P7)                  │
   │ ├─ Aircraft Admin Systems                                   │
   │ ├─ Maintenance Diagnostics                                  │
   │ └─ Crew Services                                            │
   └─────────────────────────────────────────────────────────────┘
              │ Firewall/Gateway │
              ▼                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ PASSENGER SERVICES DOMAIN (Open)                            │
   │ ├─ IFE (In-Flight Entertainment) - DAL D/E                  │
   │ ├─ Wi-Fi & Internet Access                                  │
   │ ├─ E-Commerce & Payments                                    │
   │ └─ Passenger Device Connectivity                            │
   │    ✅ ARCHITECT'S PRIMARY RESPONSIBILITY                    │
   └─────────────────────────────────────────────────────────────┘
   ```

════════════════════════════════════════════════════════════════════════════

🏗️ **SYSTEM ARCHITECTURE & INFRASTRUCTURE**
────────────────────────────────────────────

**Modern Aircraft Compute:**

☁️ **Cloud-Native Virtualization**  
   Moving beyond traditional VMs to Kubernetes-style orchestration onboard aircraft

   **Traditional Approach (Legacy):**
   - Heavy hypervisors (VMware ESXi, Xen)
   - Static resource allocation
   - Manual scaling & updates
   
   **Modern Approach (2026+):**
   - Lightweight containers (Docker, containerd)
   - Dynamic orchestration (Kubernetes, K3s for edge)
   - Microservices architecture
   - Auto-scaling based on passenger load
   
   **Why Cloud-Native in Aircraft?**
   
   ✅ Rapid deployment of new services (IFE apps)  
   ✅ Efficient resource utilization (CPU/memory)  
   ✅ Resilience through container restart policies  
   ✅ Simplified OTA updates (rolling deployments)  
   ✅ Multi-tenancy for different airlines/services

**Security Infrastructure:**

🔒 **Secure Boot & PKI**  
   Managing cryptographic trust hierarchy for aircraft systems

   **UEFI Secure Boot Chain:**
   
   ```
   Platform Key (PK) — OEM Root Authority
        ↓
   Key Exchange Key (KEK) — Intermediate CA
        ↓
   Signature Database (DB) — Authorized Bootloaders/Kernels
        ↓
   Forbidden Signature Database (DBX) — Revoked/Compromised Keys
   ```

   ⚠️ **2026 CRITICAL EVENT: Secure Boot Certificate Expiration**
   
   - Many Secure Boot certificates expire **June 2026**
   - Requires mass firmware updates across aircraft fleets
   - Failure = systems won't boot after expiration
   - **Aircraft Services Architect must plan migration strategy**
   
   **PKI Management for Aircraft:**
   
   ✅ Certificate lifecycle management (issuance, renewal, revocation)  
   ✅ Hardware Security Module (HSM) integration  
   ✅ Offline signing for air-gapped systems  
   ✅ Multi-year certificate validity planning  
   ✅ Emergency revocation procedures

📡 **Over-the-Air (OTA) Updates**  
   Secure firmware/software update pathways for aircraft systems

   **OTA Update Architecture:**
   
   ```
   Ground Servers (Airline Data Center)
        ↓ Satellite/Cellular Link
   Aircraft Gateway (Secure)
        ↓ Internal Aircraft Network
   Onboard Update Manager
        ↓ Verification (Signature Check)
   Target Systems (IFE, Services, Firmware)
   ```

   🎯 **OTA Security Requirements:**
   
   ✅ **Authenticity:** Digital signatures (RSA-4096 or ECDSA-P384)  
   ✅ **Integrity:** Hash verification (SHA-256 minimum)  
   ✅ **Confidentiality:** Encrypted payloads (AES-256)  
   ✅ **Rollback protection:** Version monotonicity  
   ✅ **Atomic updates:** All-or-nothing (no partial failures)  
   ✅ **A/B partitions:** Fallback to previous version if update fails

🐧 **Linux Kernel Programming**  
   Low-level system design for embedded aircraft environments

   **Focus Areas for Architect:**
   
   🔧 **Device drivers:** Custom hardware interfaces (avionics buses, sensors)  
   🔧 **Real-time patches:** PREEMPT_RT for deterministic latency  
   🔧 **Security modules:** SELinux/AppArmor for mandatory access control  
   🔧 **Network stack:** Custom protocols (ARINC 664/AFDX)  
   🔧 **Power management:** Battery life optimization for portable devices  
   🔧 **Boot optimization:** Sub-5-second boot for critical services

   **Common Aircraft Linux Distributions:**
   - Wind River Linux (commercial, DO-178 certification available)
   - Embedded Debian/Ubuntu (open-source, customizable)
   - Yocto Project (build-your-own embedded Linux)

════════════════════════════════════════════════════════════════════════════

🔄 **MODERN FRAMEWORKS & DEVELOPMENT**
──────────────────────────────────────

**Agile Methodology:**

🎯 **SAFe (Scaled Agile Framework)**  
   Explicitly required for cross-team synchronization in aerospace programs

   **Key SAFe Concepts:**
   
   📅 **PI (Program Increment):**  
   - 8-12 week development cycle
   - Multiple agile teams synchronized
   - PI Planning event (all teams align on objectives)
   - PI execution with 2-week sprints
   - Inspect & Adapt workshop at end
   
   🎯 **ART (Agile Release Train):**  
   - Long-lived team of agile teams
   - 50-125 people working on related systems
   - Shared backlog, common cadence
   - System demo every 2 weeks
   
   🚀 **Innovation & Planning Sprint:**  
   - Final sprint in each PI
   - Technical debt reduction
   - Exploration of new technologies
   - PI planning preparation

   **SAFe in Aerospace Context:**
   
   ✅ Compliance artifacts generated continuously (not at end)  
   ✅ Safety analysis integrated into sprint reviews  
   ✅ V&V activities parallelized with development  
   ✅ Regulatory liaison involvement in PI planning

**Verification & Validation:**

✅ **V&V (Validation & Verification)**  
   Compliance-driven testing for aviation certification

   **Verification (Are we building it right?):**
   - Requirements-based testing
   - Structural coverage analysis (statement, branch, MC/DC)
   - Code reviews & static analysis
   - Integration testing
   
   **Validation (Are we building the right thing?):**
   - System-level testing
   - End-user acceptance testing
   - Operational scenario validation
   - Field trials & flight testing

🔍 **SQA (Software Quality Assurance)**  
   Independent oversight ensuring processes followed correctly

   **SQA Responsibilities:**
   - Process audits (are we following DO-178C?)
   - Tool qualification oversight
   - Configuration management verification
   - Problem report tracking
   - Certification liaison support

**Technology Stack:**

💻 **Programming Languages:**

   🔹 **C++** — High-performance systems, real-time processing  
      *Use cases:* IFE rendering engines, data processing pipelines
   
   🔹 **Go** — Concurrent services, microservices  
      *Use cases:* API gateways, service orchestration, network proxies  
      *Why Go in 2026?* Memory safety, fast compilation, excellent concurrency
   
   🔹 **Java** — Enterprise services, business logic  
      *Use cases:* Payment processing, content management, airline integration
   
   🔹 **Python** — Automation, data analysis, ML inference  
      *Use cases:* Recommendation engines, analytics, CI/CD scripts

💾 **Databases:**

   🔹 **MySQL / MariaDB** — Primary relational database  
      *Use cases:* User accounts, transaction records, content metadata
   
   🔹 **SQLite** — Embedded local storage  
      *Use cases:* Offline caching, seat preferences, downloaded content  
      *Why SQLite in aircraft?* No server, atomic writes, crash-resistant

════════════════════════════════════════════════════════════════════════════

🤝 **KEY PROFESSIONAL AREAS**
─────────────────────────────

**Industry Collaboration:**

✈️ **OEM Collaboration**  
   Working with aircraft manufacturers on system integration

   **Boeing:**
   - 737 MAX, 787 Dreamliner integration
   - Boeing Digital Aviation Solutions (BDAS)
   - Onboard Network System (ONS) architecture
   
   **Airbus:**
   - A350, A380 systems integration
   - Open Alliance for Airborne Systems (OAA)
   - ARINC 653 partitioning standards
   
   **Key Collaboration Activities:**
   - Early design reviews (system architecture)
   - Interface control documents (ICD) development
   - Certification planning & strategy
   - Post-delivery support & updates

**Security Engineering:**

🛡️ **Threat Modeling**  
   Systematic identification & mitigation of security risks

   **Common Methodologies:**
   
   🔹 **STRIDE** (Microsoft):  
      - **S**poofing, **T**ampering, **R**epudiation  
      - **I**nformation Disclosure, **D**enial of Service, **E**levation of Privilege
   
   🔹 **PASTA** (Process for Attack Simulation and Threat Analysis):  
      - Risk-centric approach
      - 7-stage process from business objectives to attack simulation
   
   🔹 **Attack Trees:**  
      - Visual representation of attack paths
      - Root = attacker goal, branches = attack steps

   **Aircraft-Specific Threats:**
   
   ⚠️ Unauthorized network access from passenger devices  
   ⚠️ Malicious content injection (IFE exploits)  
   ⚠️ Wi-Fi man-in-the-middle attacks  
   ⚠️ USB/media-based malware introduction  
   ⚠️ Supply chain compromises (counterfeit components)  
   ⚠️ Insider threats (maintenance personnel)

**Leadership & Management:**

👥 **Technical Leadership**  
   Mentoring teams & driving architectural decisions

   **Key Responsibilities:**
   
   ✅ **Architecture governance:** Ensuring design patterns followed  
   ✅ **Technical mentorship:** Growing junior architects/engineers  
   ✅ **Decision facilitation:** Leading architecture review boards  
   ✅ **Risk management:** Identifying technical & schedule risks  
   ✅ **Stakeholder communication:** Translating tech → business value

   **Leadership in Aerospace Context:**
   
   - Balancing innovation with regulatory compliance
   - Managing multi-year certification timelines
   - Coordinating with FAA/EASA authorities
   - Driving consensus across OEMs, suppliers, airlines

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — QUICK STUDY CHECKLIST**
────────────────────────────────────

**🎯 Must-Know Standards (Priority 1):**

✅ **DO-178C** — DAL D/E objectives, traceability, testing  
✅ **ED-203A/DO-356A** — SAL 1-3 threat models, security analysis  
✅ **ARINC 664** — Aircraft Ethernet (AFDX), network segregation  
✅ **SAFe** — PI planning, ART structure, agile at scale

**🔧 Technical Deep-Dives (Priority 2):**

✅ **Secure Boot** — PKI hierarchy, 2026 certificate expiration crisis  
✅ **OTA Updates** — Atomic updates, A/B partitions, signature verification  
✅ **Linux Kernel** — Device drivers, PREEMPT_RT, SELinux  
✅ **Cloud-Native** — Kubernetes, containers, microservices on aircraft

**💼 Professional Skills (Priority 3):**

✅ **Threat Modeling** — STRIDE methodology, attack trees  
✅ **OEM Collaboration** — Boeing/Airbus integration processes  
✅ **Technical Leadership** — Architecture governance, mentorship

**📊 Technology Stack Priorities:**

| Priority | Technology | Why It Matters |
|:---------|:-----------|:---------------|
| **High** | C++ | Core IFE performance |
| **High** | Go | Modern microservices |
| **High** | Linux Kernel | Embedded systems control |
| **Medium** | Java | Enterprise integration |
| **Medium** | Python | Automation & analytics |
| **Medium** | MySQL/MariaDB | Persistent storage |
| **Low** | SQLite | Local caching only |

════════════════════════════════════════════════════════════════════════════

🎓 **INTERVIEW PREPARATION QUESTIONS**
──────────────────────────────────────

**Safety & Certification:**

❓ *"How does DAL E differ from DAL A in DO-178C objectives?"*  
   → DAL E: No safety effect, minimal V&V rigor, no MC/DC required  
   → DAL A: Catastrophic failure, full MC/DC, formal methods encouraged

❓ *"What's the difference between SAL 2 and SAL 3?"*  
   → SAL 2: Intentional attacks with simple means, limited resources  
   → SAL 3: Sophisticated/determined attackers, requires independent review

❓ *"Why is domain segregation critical in aircraft networks?"*  
   → Prevents passenger network attacks from affecting flight-critical systems  
   → Regulatory compliance (ARINC 664 partitioning requirements)

**Architecture & Security:**

❓ *"How would you architect OTA updates for 1000+ aircraft?"*  
   → Ground server → satellite link → aircraft gateway → onboard manager  
   → Digital signatures (ECDSA), hash verification, A/B partitions  
   → Staged rollout: 10 aircraft → 100 → full fleet

❓ *"What's the impact of 2026 Secure Boot certificate expiration?"*  
   → Systems won't boot after June 2026 if not updated  
   → Requires mass OTA update campaign or physical access  
   → Plan 12-month migration window

❓ *"Why use Go instead of C++ for aircraft services?"*  
   → Memory safety (no buffer overflows)  
   → Built-in concurrency (goroutines)  
   → Faster development & compilation  
   → *BUT* C++ still needed for real-time performance

**Agile & Process:**

❓ *"How does SAFe apply to DO-178C certification?"*  
   → Continuous compliance: artifacts generated per sprint  
   → V&V parallelized with development  
   → PI planning includes safety analysis reviews  
   → SQA integrated into agile ceremonies

❓ *"What's the role of SQA in an agile aerospace project?"*  
   → Independent verification of process compliance  
   → Sprint retrospective attendance  
   → Configuration management audits  
   → Certification liaison coordination

════════════════════════════════════════════════════════════════════════════

📚 **RECOMMENDED STUDY RESOURCES**
──────────────────────────────────

**Standards (Must Read):**

📖 DO-178C / ED-12C (RTCA/EUROCAE)  
📖 ED-203A (Airworthiness Security Process Specification)  
📖 DO-356A (Airworthiness Security Methods and Considerations)  
📖 ARINC 664 Part 7 (Aircraft Data Network, IFE domain)

**Books:**

📘 *"DO-178C Software Development for Airborne Systems"* — Leanna Rierson  
📘 *"SAFe 6.0 Distilled"* — Richard Knaster & Dean Leffingwell  
📘 *"Threat Modeling: Designing for Security"* — Adam Shostack  
📘 *"Linux Kernel Development"* — Robert Love

**Online Courses:**

🎓 DO-178C Foundation (AFuzion, Rapita Systems)  
🎓 SAFe for Architects (Scaled Agile, Inc.)  
🎓 Linux Kernel Internals (Linux Foundation)  
🎓 Kubernetes Fundamentals (CNCF)

════════════════════════════════════════════════════════════════════════════

🚀 **90-DAY STUDY PLAN**
────────────────────────

**Month 1: Foundations**

Week 1-2: DO-178C fundamentals (DAL levels, objectives, traceability)  
Week 3-4: ED-203A/DO-356A (SAL levels, threat models, security analysis)

**Month 2: Architecture & Tech**

Week 5-6: ARINC 664 networks, domain segregation, cloud-native aircraft  
Week 7-8: Secure Boot, PKI, OTA updates, Linux kernel basics

**Month 3: Process & Leadership**

Week 9-10: SAFe framework (PI planning, ART structure)  
Week 11-12: Threat modeling, OEM collaboration, mock interviews

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Version:** 2.0 — Enhanced with emojis, diagrams & study plan  
**Target Role:** Aircraft Services Architect @ PAC (Portland)  
**Certification Focus:** DO-178C DAL D/E | ED-203A SAL 1-3 | SAFe Architect
