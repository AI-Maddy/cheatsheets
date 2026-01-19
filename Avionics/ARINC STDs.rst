============================================================
ARINC Standards — Quick Reference Guide for Avionics
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

================================================================================
Overview
================================================================================

**ARINC (Aeronautical Radio, Incorporated)** standards are industry specifications for avionics equipment, interfaces, and protocols used in commercial and military aircraft. Now managed by **SAE International** under SAE ITC (Information Technology Committee), ARINC standards cover hundreds of technical specifications spanning data buses, software interfaces, physical connectors, cabin systems, and maintenance protocols.

**Key Categories:**
- Data Bus Protocols (429, 629, 664, 717, 825)
- Software Interfaces (653, 661, IMA/CPIOM)
- Hardware Form Factors (404, 600)
- Data Loading & Software Management (615, 615A, 645, 665, 667)
- Security & Electronic Distribution (827, 835, 842)
- Video/Display (818, 708)
- Cabin Systems (485, 628, 800 series, 809, 854)
- Navigation & Flight Management (424, 702)
- Communications (618, 633, 791)

**2026 Status:** Many ARINC standards have multiple parts (e.g., ARINC 429 Parts 1-3, ARINC 664 Parts 1-7) and undergo regular revisions. Refer to SAE ITC ARINC Industry Activities for latest versions.

**Standards with Detailed Cheatsheets:**
The following ARINC standards have comprehensive dedicated cheatsheets available:

- 📘 `ARINC 404 <ARINC_404.rst>`_ — ATR Equipment Form Factors (packaging, mounting)
- 📘 `ARINC 424 <ARINC_424.rst>`_ — Navigation System Data Base (FMS databases)
- 📘 `ARINC 429 <ARINC_429.rst>`_ — Mark 33 DITS (most widely used data bus)
- 📘 `ARINC 600 <ARINC_600.rst>`_ — Equipment Connectors (power, signals, ARINC 429)
- 📘 `ARINC 615 <ARINC_615.rst>`_ — Software Data Loading
- 📘 `ARINC 629 <ARINC_629.rst>`_ — Bidirectional Multi-Access Databus
- 📘 `ARINC 653 <ARINC_653.rst>`_ — Partitioned RTOS (APEX interface)
- 📘 `ARINC 661 <ARINC_661.rst>`_ — Cockpit Display System Interface
- 📘 `ARINC 664 AFDX <ARINC_664_AFDX.rst>`_ — Aircraft Data Network (AFDX)
- 📘 `ARINC 702/702A <ARINC_702_FMS.rst>`_ — Flight Management System (FMS)
- 📘 `ARINC 708 <ARINC_708.rst>`_ — Weather Radar Digital Interface
- 📘 `ARINC 717 <ARINC_717.rst>`_ — Flight Data Acquisition & Recording
- 📘 `ARINC 818 <ARINC_818.rst>`_ — Digital Video Bus (FLIR, EVS, HMD)
- 📘 `ARINC 825 <ARINC_825.rst>`_ — CAN Bus for General Aviation
- 📘 `ARINC Software Standards <ARINC_Software_Standards.rst>`_ — 613/614/615/615A/645/665/667
- 📘 `ARINC Security Standards <ARINC_Security_Standards.rst>`_ — 827/835/842 (Cybersecurity)

================================================================================
1. Data Bus Standards
================================================================================

**ARINC 429** — Mark 33 Digital Information Transfer System (DITS)
   - **Most widely used** unidirectional avionics data bus (since 1970s)
   - **Speed:** 12.5 or 100 kbps
   - **Topology:** Point-to-point, simplex (one transmitter, up to 20 receivers)
   - **Word Format:** 32-bit words with label, SDI, data, SSM, parity
   - **Parts:** Part 1 (functional), Part 2 (discrete words), Part 3 (file transfer)
   - **Applications:** Flight controls, navigation, engine data, weather radar
   - **Key Feature:** Differential voltage signaling (Tx High/Low, Rx High/Low)
   - 📘 **Detailed Cheatsheet:** `ARINC_429.rst <ARINC_429.rst>`_

**ARINC 629** — Bidirectional Multi-Access Databus
   - **Topology:** Bidirectional, multi-transmitter (up to 120 terminals)
   - **Speed:** 2 Mbps
   - **Access Method:** Time-division multiplexing (periodic and aperiodic messages)
   - **Applications:** Boeing 777 primary avionics databus
   - **Advantage:** Higher bandwidth than 429, multi-drop capability
   - **Status:** Less common on new aircraft (replaced by ARINC 664/AFDX)
   - 📘 **Detailed Cheatsheet:** `ARINC_629.rst <ARINC_629.rst>`_

**ARINC 664** — Aircraft Data Network (AFDX - Avionics Full-Duplex Switched Ethernet)
   - **Technology:** Deterministic Ethernet with guaranteed bandwidth
   - **Speed:** 10/100 Mbps (Gigabit in newer revisions)
   - **Topology:** Redundant switched star (dual networks for fault tolerance)
   - **Key Feature:** Virtual Links (VL) with guaranteed bandwidth allocation
   - **Parts:**
     - Part 1: Concepts and overview
     - Part 2: Ethernet physical/data-link layer
     - Part 7: **AFDX** (deterministic profile) — most referenced
   - **Applications:** Airbus A380, A350, Boeing 787, modern avionics architectures
   - **Advantage:** High bandwidth, commercial Ethernet compatibility, scalability
   - 📘 **Detailed Cheatsheet:** `ARINC_664_AFDX.rst <ARINC_664_AFDX.rst>`_

**ARINC 717** — High-Speed Digital Flight Data Acquisition
   - **Purpose:** Flight Data Recorder (FDR) interface
   - **Speed:** 64, 128, 256, 512, 1024, 2048, 4096 words/second
   - **Encoding:** Harvard Bi-Phase (self-clocking)
   - **Applications:** Flight data acquisition units (FDAU), quick access recorders (QAR)
   - **Replaces:** ARINC 573 (older FDR standard)
   - 📘 **Detailed Cheatsheet:** `ARINC_717.rst <ARINC_717.rst>`_

**ARINC 825** — CAN Bus for Avionics (Controller Area Network)
   - **Purpose:** General aviation and smaller aircraft data bus
   - **Technology:** Based on ISO 11898 CAN
   - **Speed:** Up to 1 Mbps
   - **Applications:** Engine monitoring, sensor networks, general aviation avionics
   - **Advantage:** Lower cost than ARINC 429, automotive heritage
   - 📘 **Detailed Cheatsheet:** `ARINC_825.rst <ARINC_825.rst>`_

================================================================================
2. Software Interface Standards
================================================================================

**ARINC 613** — Guidance for Using the Ada Programming Language in Avionics Systems
   - **Published:** Dec 31, 1987
   - **Purpose:** Ada domain guidance for avionics software development
   - **Scope:** Compiler requirements, programming practices, subset definitions
   - **Historical Context:** Ada selected as high-order language for avionics (1986)
   - **Applications:** Guidance for Ada compiler developers and programmers
   - **Status:** Historical reference (most modern avionics use C/C++)

**ARINC 653** — Avionics Application Software Standard Interface (APEX)
   - **Purpose:** Partitioned Real-Time Operating System (RTOS) interface
   - **Key Concept:** **Time and space partitioning** for safety-critical software
   - **Parts:**
     - Part 1: Core APEX interface (process management, IPC, health monitoring)
     - Part 2: Extended services (additional APIs)
     - Part 3: Conformity test specifications
   - **IPC Mechanisms:**
     - **Sampling Ports:** Latest-value, unidirectional (low latency)
     - **Queuing Ports:** FIFO messaging (guaranteed delivery)
     - **Blackboard:** Shared memory within partition
   - **Applications:** DO-178C DAL A/B software (flight controls, FADEC, TCAS)
   - **2026 RTOS:** VxWorks 653, PikeOS, Lynx MOSA.ic, Integrity-178B
   - **LSAP (Local Sampling Port):** Intra-partition sampling communication
   - 📘 **Detailed Cheatsheet:** `ARINC_653.rst <ARINC_653.rst>`_

**ARINC 661** — Cockpit Display System (CDS) Interface
   - **Purpose:** Standardized interface between display hardware and user applications
   - **Architecture:** Server (display system) + Clients (user apps)
   - **Widgets:** Buttons, text fields, graphical primitives, custom widgets
   - **Protocol:** XML-based definition file + binary runtime protocol
   - **Applications:** Primary Flight Display (PFD), Multifunction Display (MFD), EICAS
   - **Advantage:** Hardware-independent cockpit applications, reusability
   - 📘 **Detailed Cheatsheet:** `ARINC_661.rst <ARINC_661.rst>`_

**Integrated Modular Avionics (IMA) & CPIOM**
   - **Concept:** Hardware consolidation for avionics functions (not a single ARINC standard)
   - **CPIOM (Core Processing Input/Output Module):**
     - Airbus-specific terminology for IMA computing modules (A380, A350)
     - **Form Factor:** ARINC 600 3-MCU enclosures
     - **Operating System:** ARINC 653-compliant partitioned RTOS
       - Common implementations: VxWorks 653, INTEGRITY-178B, PikeOS, Deos
     - **Partitioning:** Time and space isolation per ARINC 653 APEX
     - **Networking:** ARINC 664 (AFDX) interconnects between CPIOMs
     - **I/O Interfaces:** ARINC 429, discrete, CAN, analog
     - **Certification:** DO-178C DAL A/B levels
   - **Architecture Benefits:**
     - Reduced weight, part numbers, and maintenance costs
     - Shared hardware for multiple avionics functions
     - 20+ partitions per CPIOM (A350 has ~21 CPIOM variants)
   - **Boeing Equivalent:** Common Core System (CCS) on 787, AIMS on 777
   - **Key Standards:** ARINC 653 (partitioning), 664 (networking), 600 (form factor)

================================================================================
3. Hardware Form Factor Standards
================================================================================

**ARINC 404** — Air Transport Rack (ATR) Form Factors
   - **Purpose:** Standard mounting cases and racking for avionics LRUs
   - **Sizes:** 1/4 ATR, 1/2 ATR, 3/4 ATR, 1 ATR (full)
   - **Dimensions:** Based on 6U rack height (10.5 inches)
   - **Features:** EMI shielding, cooling airflow, mounting rails
   - **Applications:** Universal LRU packaging (FMS, radios, sensors, displays)
   - 📘 **Detailed Cheatsheet:** `ARINC_404.rst <ARINC_404.rst>`_

**ARINC 407** — Synchro Systems
   - **Purpose:** Electromechanical angular position sensors/actuators
   - **Technology:** Synchro transmitters/receivers for analog signals
   - **Applications:** Legacy flight instruments, control position feedback

**ARINC 600** — Air Transport Avionics Equipment Interfaces
   - **Purpose:** Connector pin assignments, power, cooling, mounting
   - **Scope:** Comprehensive standard covering physical/electrical interfaces
   - **Related:** Works with ARINC 404 form factors
   - 📘 **Detailed Cheatsheet:** `ARINC_600.rst <ARINC_600.rst>`_

================================================================================
4. Data Loading & Software Management
================================================================================

**ARINC 615** — Software Data Loading (Part 1)
   - **Published:** Jul 31, 1992 (615-3), Apr 30, 2002 (615-4)
   - **Purpose:** Load software/databases into avionics LRUs
   - **Transport:** ARINC 429, RS-232, RS-422
   - **Protocol:** File transfer over slow serial buses
   - **Media:** Originally 3.5" floppy disk (615-3/615-4)
   - **Tools:** Portable Data Loader (PDL), Airborne Data Loader (ADL)
   - **Applications:** Loading navigation databases, flight plans, configurations
   - **Typical Speed:** Slow (limited by ARINC 429 100 kbps)
   - 📘 **Detailed Cheatsheet:** `ARINC_615.rst <ARINC_615.rst>`_

**ARINC 614** — Standard Firmware Loader for Avionics Shops
   - **Published:** Aug 31, 1989
   - **Purpose:** Shop-level firmware loading for memory devices
   - **Scope:** Circuit card assemblies, Line Replaceable Modules (LRMs)
   - **Applications:** Avionics maintenance facilities, repair shops
   - **Related:** Precursor to airborne data loading standards (615/615A)

**ARINC 615A** — Portable Data Loader Using Ethernet Interface
   - **Published:** Jul 23, 2023 (615A-4, current version)
   - **Purpose:** High-speed data loading via Ethernet, USB, or ARINC 664
   - **Transport:** Ethernet (primary), CAN, USB, ARINC 664 (AFDX)
   - **Speed:** Much faster than 615 (Mbps vs kbps)
   - **Primary Function:** Upload Loadable Software Parts (LSPs) to airborne computers
   - **Secondary Function:** Download data from airborne systems (logs, configurations)
   - **Applications:** Modern avionics software updates, database loading
   - **Tools:** Portable data loaders (PDL), laptop-based loading systems
   - **Integration:** Works with ARINC 665 (LSP standards) and 827 (security)

**ARINC 645** — Software Data Loading Terminology
   - **Purpose:** Common terminology and functions for software distribution/loading
   - **Key Concept:** Aircraft-controlled software delivery standards
   - **Scope:** LSAP (Loadable Software Airplane Part) definitions and protocols
   - **Terminology:** Standardizes vocabulary across data loading ecosystem
   - **Related:** Foundation for ARINC 615/615A implementation
   - **Integration:** Referenced by ARINC 665, 667, 827, 835

**ARINC 665** — Loadable Software Standards (Current: 665-5)
   - **Purpose:** Standards for Loadable Software Parts (LSPs) and Media Set Parts (MSPs)
   - **Scope:** Formatting, part numbering, labeling, content, compatibility rules
   - **Key Concept:** LSAPs (Loadable Software Airplane Parts) as subset of LSPs
   - **Part Numbering:** Standard format for software part identification
   - **Compatibility:** Rules for determining software/hardware compatibility
   - **Applications:** Ensures interoperability for data loading across aircraft systems
   - **Quality Control:** Content validation, checksums, version management
   - **Relationship:** All LSAP requirements inherit from LSP specifications
   - **Used By:** Airlines, OEMs, software providers for consistent packaging

**ARINC 667** — Guidance for Field Loadable Software Management
   - **Purpose:** Best practices for managing Field Loadable Software (FLS)
   - **Scope:** LSAPs, databases, operational data loaded aboard aircraft
   - **Content:** Configuration management, version control, compatibility verification
   - **Lifecycle:** Software distribution, installation, activation, rollback
   - **Documentation:** Required records, audit trails, change tracking
   - **Applications:** Software lifecycle management for avionics systems
   - **Target Audience:** Airlines maintenance planners, avionics managers, software integrators

================================================================================
5. Security & Electronic Distribution Standards
================================================================================

**ARINC 827** — Electronic Distribution Security
   - **Purpose:** Security for Electronic Distribution of Software (EDS)
   - **Scope:** Digital signatures, authentication, secure software delivery
   - **Key Technologies:**
     - PKI (Public Key Infrastructure) - certificate-based authentication
     - Digital signatures (RSA, ECDSA) for integrity verification
     - Encryption for confidentiality (AES-256)
   - **EDS Crate:** Secure container for LSAP distribution
   - **Applications:** Secure LSAP/FLS distribution to aircraft
   - **Certificate Management:** Issuance, renewal, revocation, validation
   - **Integration:** Works with ARINC 615A for encrypted software loading
   - **Compliance:** DO-326A/DO-356A cybersecurity requirements

**ARINC 835** — Software Security Framework
   - **Purpose:** Digital signature standards for avionics software
   - **Scope:** Authentication, integrity verification, secure boot
   - **Digital Signatures:** Code signing for LSAPs, firmware, databases
   - **Integrity Protection:** Hash algorithms (SHA-256, SHA-384) for tamper detection
   - **Applications:** Protecting LSAPs/EDS crates from tampering
   - **Chain of Trust:** From software development through aircraft installation
   - **Related Standards:** ATA Spec 42 (electronic distribution security)
   - **Validation:** Pre-load signature verification, post-load integrity checks
   - **2026 Status:** Critical for DO-326A/DO-356A cybersecurity compliance

**ARINC 842** — Continued Airworthiness & Security
   - **Purpose:** Security of loadable parts for continued airworthiness
   - **Scope:** Vulnerability management, security updates, patch distribution
   - **Security Updates:** Process for distributing security patches to fleet
   - **Vulnerability Management:** Tracking, assessment, remediation procedures
   - **Applications:** Long-term software security maintenance
   - **Patch Distribution:** Secure delivery of security fixes via ARINC 615A/827
   - **Audit Requirements:** Record-keeping for security-related software changes
   - **Integration:** Complements ARINC 665/667 for secure lifecycle management
   - **DO-326A Alignment:** Cybersecurity threat response and mitigation

================================================================================
6. Video & Display Standards
================================================================================

**ARINC 818** — Avionics Digital Video Bus (ADVB)
   - **Purpose:** Uncompressed digital video transport
   - **Speed:** Up to 2.5 Gbps (Fibre Channel-based)
   - **Latency:** Low latency (< 1 ms typical)
   - **Formats:** Multiple resolutions (VGA to 4K), RGB/YCbCr
   - **Revisions:** 818-2, 818-3 (enhanced features)
   - **Applications:** Cameras (FLIR, EVS), synthetic vision, video recorders, displays
   - **Advantage:** Deterministic, low-latency video for safety-critical displays

**ARINC 708** — Weather Radar Digital Interface
   - **Purpose:** Radar display data transfer protocol
   - **Data:** Radar returns, range rings, altitude, weather intensity
   - **Applications:** Weather radar displays, EGPWS terrain displays
   - 📘 **Detailed Cheatsheet:** `ARINC_708.rst <ARINC_708.rst>`_

================================================================================
6. Navigation & Flight Management
================================================================================

**ARINC 424** — Navigation System Data Base
   - **Purpose:** Standard file format for aircraft navigation databases
   - **Content:** Waypoints, airways, runways, procedures (SIDs, STARs, approaches)
   - **Format:** Fixed-length records, hierarchical structure
   - **Cycle:** 28-day update cycle (aligned with AIRAC)
   - **Applications:** Flight Management Systems (FMS), GPS navigators
   - **2026 Status:** ARINC 424-19 (ongoing revisions for new RNAV procedures)
   - 📘 **Detailed Cheatsheet:** `ARINC_424.rst <ARINC_424.rst>`_

**ARINC 702** — Flight Management Computer System (FMCS)
   - **Purpose:** FMS interfaces and functional requirements
   - **Scope:** Autopilot coupling, navigation modes, fuel management
   - **Applications:** Commercial airliner FMS architecture
   - 📘 **Detailed Cheatsheet:** `ARINC_702_FMS.rst <ARINC_702_FMS.rst>`_

**ARINC 702A** — Advanced FMS Characteristics
   - **Updates:** Enhanced navigation (RNAV, RNP), 4D trajectories
   - **Applications:** Modern FMS with performance-based navigation (PBN)
   - 📘 **Detailed Cheatsheet:** `ARINC_702_FMS.rst <ARINC_702_FMS.rst>`_

================================================================================
7. Communications Standards
================================================================================

**ARINC 618** — Air/Ground Character-Oriented Protocol
   - **Purpose:** Air-ground datalink communications
   - **Technology:** Character-based messaging (similar to ACARS)
   - **Applications:** AOC (Airline Operations Center) communications

**ARINC 633** — Air Operator Control (AOC) Data Exchange
   - **Purpose:** Standardized message formats for air-ground operations
   - **Content:** Flight plans, weather, maintenance, ATC clearances
   - **Applications:** ACARS, FANS, CPDLC

**ARINC 791** — Aviation Satellite Communications
   - **Purpose:** Ku-band and Ka-band satellite antenna installation
   - **Scope:** Antenna specifications, mounting, certification
   - **Applications:** Broadband internet, cabin connectivity, cockpit datalink

================================================================================
8. Cabin Systems & In-Flight Entertainment
================================================================================

**ARINC 485** — Cabin Equipment Interfaces
   - **Purpose:** In-seat IFE (In-Flight Entertainment) protocols
   - **Parts:** Part 2 covers in-seat protocol for passenger systems
   - **Applications:** Seat power, video distribution, passenger controls

**ARINC 628** — Cabin Equipment Interfaces (Extended)
   - **Purpose:** Power, protocols, galley equipment interfaces
   - **Scope:** Multiple parts covering cabin systems (IFE, galleys, lavatories)
   - **Applications:** Cabin management systems, crew call panels

**ARINC 800 Series** — Modern Cabin Connectivity
   - **Standards:** 800, 810, 812, etc.
   - **Purpose:** Cables, connectors, IFE networking, USB power
   - **Applications:** Modern cabin systems, wireless IFE, passenger device charging
   - **Example:** ARINC 810 (cabin Ethernet), ARINC 812 (USB power sockets)

**ARINC 809** — 3GCN (3rd Generation Cabin Network)
   - **Purpose:** Seat Distribution System for modern IFES (In-Flight Entertainment System)
   - **Scope:** Electrical/mechanical interfaces at seat level
   - **Components:** Seat Video Display (SVD), Integrated Seat Box (ISB), Passenger Control Unit (PCU)
   - **Features:** Power outlets, USB charging, Ethernet-based seat connectivity
   - **Applications:** Seatback displays, entertainment controls, device charging
   - **Advantage:** Standardized seat integration across aircraft manufacturers

**ARINC 854** — CENBUS (Cabin Equipment Network Bus)
   - **Purpose:** High-speed cabin network bus (successor to ARINC 485)
   - **Technology:** 100BASE-T1 Ethernet-based (automotive Ethernet)
   - **Speed:** 100 Mbps (vs. ARINC 485's low-speed serial)
   - **Applications:** Modern IFE, cabin management systems, seat controls
   - **Advantages:** Lower latency, reduced weight, higher bandwidth
   - **Status:** Replacing older low-speed in-seat protocols in 2020s aircraft

================================================================================
9. Miscellaneous & Specialized Standards
================================================================================

**ARINC 419** — Wiring Topologies (Legacy)
   - **Purpose:** Early digital air data system wiring
   - **Technology:** Serial twisted-pair for DADS/ARINC 575
   - **Status:** Largely obsolete (superseded by ARINC 429/664)

**ARINC 573** — Flight Data Recorder Formats (Legacy)
   - **Purpose:** Digital flight data recording formats
   - **Status:** Predecessor to ARINC 717 (modern FDR standard)
   - **Note:** Still referenced for legacy systems

**ARINC 660** — CNS/ATM Avionics Architecture
   - **Purpose:** Communications, Navigation, Surveillance/Air Traffic Management
   - **Scope:** Functional allocation, recommended architectures
   - **Applications:** NextGen/SESAR avionics modernization

**ARINC 811** — COTS (Commercial Off-The-Shelf) Selection
   - **Purpose:** Guidance for using COTS in avionics
   - **Scope:** Qualification, obsolescence management, DO-254/DO-178C considerations
   - **Applications:** Selecting processors, memories, operating systems for avionics

================================================================================
10. Quick Reference Table
================================================================================

+---------------+-------------------------+-------------------+---------------------------+
| ARINC         | Category                | Key Feature       | Primary Application       |
+===============+=========================+===================+===========================+
| **404**       | Hardware                | ATR form factors  | LRU packaging             |
+---------------+-------------------------+-------------------+---------------------------+
| **424**       | Navigation              | Nav database      | FMS navigation data       |
+---------------+-------------------------+-------------------+---------------------------+
| **429**       | Data Bus                | Unidirectional    | Flight controls, sensors  |
+---------------+-------------------------+-------------------+---------------------------+
| **573**       | Data Recording          | FDR formats       | Legacy flight recorders   |
+---------------+-------------------------+-------------------+---------------------------+
| **615/615A**  | Software Loading        | PDL protocols     | Software/database updates |
+---------------+-------------------------+-------------------+---------------------------+
| **618**       | Communications          | Air/ground        | ACARS messaging           |
+---------------+-------------------------+-------------------+---------------------------+
| **629**       | Data Bus                | Bidirectional     | Boeing 777 databus        |
+---------------+-------------------------+-------------------+---------------------------+
| **633**       | Communications          | AOC messages      | Airline operations        |
+---------------+-------------------------+-------------------+---------------------------+
| **645**       | Software Loading        | Terminology       | LSAP definitions          |
+---------------+-------------------------+-------------------+---------------------------+
| **653**       | Software (RTOS)         | Partitioning      | Safety-critical software  |
+---------------+-------------------------+-------------------+---------------------------+
| **660**       | Architecture            | CNS/ATM           | Modern avionics systems   |
+---------------+-------------------------+-------------------+---------------------------+
| **661**       | Software (Display)      | CDS interface     | Cockpit displays          |
+---------------+-------------------------+-------------------+---------------------------+
| **664**       | Data Bus (Ethernet)     | AFDX              | A380, 787 networks        |
+---------------+-------------------------+-------------------+---------------------------+
| **665**       | Software Loading        | LSP/MSP standards | Software part management  |
+---------------+-------------------------+-------------------+---------------------------+
| **667**       | Software Loading        | FLS management    | Field loadable software   |
+---------------+-------------------------+-------------------+---------------------------+
| **702/702A**  | Flight Management       | FMS interfaces    | FMS architecture          |
+---------------+-------------------------+-------------------+---------------------------+
| **708**       | Display                 | Radar data        | Weather radar displays    |
+---------------+-------------------------+-------------------+---------------------------+
| **717**       | Data Recording          | High-speed FDR    | Flight data acquisition   |
+---------------+-------------------------+-------------------+---------------------------+
| **791**       | Communications          | Satellite         | Cabin broadband internet  |
+---------------+-------------------------+-------------------+---------------------------+
| **809**       | Cabin Systems           | 3GCN seat network | Seatback IFE              |
+---------------+-------------------------+-------------------+---------------------------+
| **811**       | COTS Selection          | Qualification     | COTS component use        |
+---------------+-------------------------+-------------------+---------------------------+
| **818**       | Video                   | Digital video bus | Cameras, displays         |
+---------------+-------------------------+-------------------+---------------------------+
| **825**       | Data Bus (CAN)          | Automotive CAN    | General aviation          |
+---------------+-------------------------+-------------------+---------------------------+
| **827**       | Security                | EDS security      | Secure software delivery  |
+---------------+-------------------------+-------------------+---------------------------+
| **835**       | Security                | Digital signatures| Software authentication   |
+---------------+-------------------------+-------------------+---------------------------+
| **842**       | Security                | Airworthiness sec | Security lifecycle mgmt   |
+---------------+-------------------------+-------------------+---------------------------+
| **854**       | Cabin Systems           | CENBUS Ethernet   | High-speed cabin network  |
+---------------+-------------------------+-------------------+---------------------------+
| **485/628**   | Cabin Systems           | IFE protocols     | Passenger entertainment   |
+---------------+-------------------------+-------------------+---------------------------+
| **800 series**| Cabin Systems           | Modern IFE        | Cabin connectivity        |
+---------------+-------------------------+-------------------+---------------------------+

================================================================================
11. Key Terminology
================================================================================

**AFDX (Avionics Full-Duplex Switched Ethernet):**
- ARINC 664 Part 7 deterministic Ethernet profile
- Redundant networks (A/B) for fault tolerance
- Virtual Links (VL) guarantee bandwidth and latency

**APEX (Application Executive):**
- ARINC 653 application programming interface
- Provides time/space partitioning services
- Standard API for portable safety-critical software

**ATR (Air Transport Rack):**
- ARINC 404 standard mounting form factors
- Sizes: 1/4, 1/2, 3/4, 1 ATR (full)
- Enables interchangeable LRUs

**Sampling Port (ARINC 653):**
- Latest-value communication (overwrites old data)
- Unidirectional, low latency
- Used for periodic sensor data, control outputs

**Queuing Port (ARINC 653):**
- FIFO message queues
- Guaranteed delivery (no data loss if queue not full)
- Used for event-driven communication

**Virtual Link (VL) - AFDX:**
- Logical communication channel with guaranteed bandwidth
- Source → Destination(s) unidirectional path
- BAG (Bandwidth Allocation Gap) defines transmission rate

**LRU (Line-Replaceable Unit):**
- Modular avionics component (FMS, radio, display, etc.)
- Conforms to ARINC 404/600 physical interfaces
- Quickly replaceable for maintenance

================================================================================
12. 2026 Update Notes
================================================================================

**Standards Management:**
- ARINC standards now maintained by **SAE International** (SAE ITC)
- Regular revisions published (check SAE Aerospace Standards portal)
- Many standards have EUROCAE/RTCA equivalents (e.g., ED-247 for ARINC 664)

**Emerging Trends:**
- **Gigabit AFDX:** Higher-speed ARINC 664 variants (1/10 Gbps)
- **TSN (Time-Sensitive Networking):** IEEE 802.1 TSN being evaluated as AFDX successor
- **Wireless Cabin:** ARINC 800 series expanding for 5G, Wi-Fi 6E cabin systems
- **Cybersecurity:** New revisions adding security requirements (encryption, authentication)
- **DO-326A/DO-356A Integration:** Cybersecurity requirements for ARINC 664/653 implementations

**Common Aircraft Usage (2026):**
- **Boeing 787:** ARINC 664 (AFDX), 653, 661, 717
- **Airbus A350:** ARINC 664 (AFDX), 653, 661, 825
- **Boeing 777X:** ARINC 664, 629 (legacy), 653, 661
- **General Aviation:** ARINC 429, 825 (CAN), 615A

**For Detailed Specifications:**
Refer to SAE ITC ARINC Industry Activities (https://www.sae.org/works/committeeHome.do?comtID=TEAAIR) for official standards documents, revision history, and purchase options.

**Related Industry Standards:**
- **ATA Spec 42:** Electronic distribution security (complements ARINC 827/835)
- **DO-326A/DO-356A:** Airworthiness security requirements (integrates with ARINC 664/653)
- **EUROCAE ED-247:** European equivalent to ARINC 664 (AFDX)

================================================================================

**Last Updated:** January 16, 2026  
**Document Version:** 2.1 (Added security standards, IMA/CPIOM, modern cabin systems)

================================================================================