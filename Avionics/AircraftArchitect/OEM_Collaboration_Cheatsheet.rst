✈️ **OEM Collaboration & Integration Cheatsheet**
════════════════════════════════════════════════

**Focus:** Collaboration between airlines/suppliers and aircraft OEMs (Boeing, Airbus)  
**Scope:** Integration processes, ICD development, certification coordination  
**Application:** Commercial aviation, line-fit and retrofit programs

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — OEM COLLABORATION ESSENTIALS**
──────────────────────────────────────────

**Quick Reference:**

✅ **Boeing:** BDAS (Boeing Design Assurance System), supplier portals, 737/787 platforms  
✅ **Airbus:** OAA (Open Avionics Architecture), MSN tracking, A350/A380 programs  
✅ **ICD Development:** Define interfaces early, manage changes rigorously  
✅ **Certification:** Coordinate with OEM DER, align with type certificate amendments  
✅ **Post-Delivery:** Warranty support, service bulletins, continuous airworthiness

**Key Success Factors:**

🔹 Early engagement with OEM architecture teams  
🔹 Rigorous configuration management and change control  
🔹 Clear communication channels (technical, commercial, certification)  
🔹 Compliance with OEM design standards and processes  
🔹 Long-term support planning (10-30 year aircraft lifecycle)

════════════════════════════════════════════════════════════════════

🛫 **BOEING INTEGRATION**
─────────────────────────

**📋 Boeing Design Assurance System (BDAS):**

Boeing's comprehensive framework for managing supplier design activities:

**Key Components:**

1. **Delegated Design Authority (DDA):**
   - Boeing delegates design tasks to qualified suppliers
   - Supplier responsible for compliance with Boeing requirements
   - Boeing retains oversight and approval authority

2. **Design Organization Approval (DOA):**
   - Supplier must demonstrate design capability
   - Quality system assessment by Boeing
   - Ongoing surveillance and audits

3. **Supplier Portal Access:**
   - MyBoeingFleet for airlines
   - Boeing Supplier Portal for vendors
   - Access to specifications, standards, and tools

**🔧 Boeing Aircraft Programs:**

**737 MAX Integration:**

```
Platform: 737 MAX 7/8/9/10
Avionics: Rockwell Collins (now Collins Aerospace)
Key Systems:
  - Flight Management System (FMS)
  - Display Electronics
  - Communications Management

Integration Points:
  ✓ ARINC 429 buses (legacy)
  ✓ ARINC 664 (AFDX) for newer systems
  ✓ 28V DC power distribution
  ✓ Environmental constraints (-55°C to +70°C)
```

**787 Dreamliner Integration:**

```
Platform: 787-8/9/10
Architecture: Fully networked (AFDX backbone)
Key Features:
  - Common Core System (CCS) - central computing
  - Integrated Modular Avionics (IMA)
  - Cabin Systems Network (CSN)
  - Airplane Information Management System (AIMS)

Integration Approach:
  ✓ Line Replaceable Module (LRM) design
  ✓ Ethernet-based communication (AFDX)
  ✓ 235V AC power with smart power management
  ✓ Electronic Flight Bag (EFB) integration
```

**📄 Boeing Interface Control Documents (ICD):**

Boeing uses rigorous ICD templates:

```rst
ICD Structure (Boeing Standard):

1. Document Control
   - Document number (e.g., D6-54321)
   - Revision history
   - Approval signatures

2. Scope
   - System description
   - Interface boundaries
   - Applicable aircraft models

3. Applicable Documents
   - Boeing specifications (D1-xxx, D6-xxx)
   - Industry standards (ARINC, RTCA)
   - Regulatory requirements

4. Interface Definition
   - Electrical interfaces (power, signals)
   - Mechanical interfaces (mounting, connectors)
   - Environmental interfaces (cooling, EMI)
   - Data interfaces (protocol, message definitions)

5. Performance Requirements
   - Functional requirements
   - Timing requirements
   - Error handling

6. Verification & Validation
   - Test procedures
   - Acceptance criteria
   - Qualification testing

7. Configuration Management
   - Change process
   - Effectivity (aircraft serial numbers)
```

**Example: IFE System ICD with Boeing 787:**

```yaml
ICD: D6-87654 Rev C
Title: "In-Flight Entertainment System Interface"
Aircraft: 787-9/10
System: Thales AVANT IFE

Electrical Interface:
  Power:
    Input: 115V AC, 400Hz, 3-phase
    Max Current: 40A per phase
    Protection: Circuit breakers on aircraft side
  
  Data:
    Protocol: AFDX (ARINC 664 Part 7)
    Network: Cabin Systems Network (CSN)
    Virtual Links:
      VL_IFE_CONTROL: Bandwidth 10 Mbps, BAG 8ms
      VL_IFE_VIDEO: Bandwidth 100 Mbps, BAG 1ms
      VL_IFE_AUDIO: Bandwidth 5 Mbps, BAG 4ms
  
  Discrete Signals:
    - Seatbelt Sign (28V DC input)
    - Emergency Announcement (28V DC input)
    - System Reset (28V DC input, active low)

Mechanical Interface:
  LRU Location: Overhead rack, PSU E3
  Mounting: Boeing standard rail system
  Connectors:
    - Power: MS3116F20-41P (circular, 41-pin)
    - Data: Ethernet RJ45 (shielded, AFDX qualified)
  
Environmental:
  Operating Temperature: -20°C to +55°C
  Storage Temperature: -55°C to +70°C
  Altitude: Up to 43,000 ft
  Vibration: Per RTCA DO-160G Section 8, Category S
  EMI: Per RTCA DO-160G Section 21, Category M

Software Interface:
  AFDX Message Format:
    - Standard UDP/IP over AFDX
    - Custom Application Layer per Boeing D6-87654-1
    - Message encryption: AES-256 (for payment data)
  
  Seatback Unit Communication:
    - Ethernet switch per seat row
    - Cat 6 cabling, shielded
    - PoE (Power over Ethernet) for displays

Certification:
  Software: DO-178C Level C (IFE app), Level A (emergency announcement)
  Hardware: DO-254 Level C
  Environmental: DO-160G
  Cybersecurity: ED-202A/DO-326A
```

**🤝 Boeing Collaboration Process:**

```
Phase 1: Concept & Requirements (Months 0-6)
  ├─ Initial engagement with Boeing program office
  ├─ NDA and teaming agreements
  ├─ Review Boeing architecture documents
  ├─ Preliminary design review (PDR) with Boeing
  └─ ICD draft version 0.1

Phase 2: Detailed Design (Months 6-18)
  ├─ ICD version 1.0 (baselined)
  ├─ Boeing design review and approval
  ├─ Prototype development
  ├─ Interface testing at Boeing labs
  └─ Critical Design Review (CDR)

Phase 3: Integration & Test (Months 18-30)
  ├─ Hardware/software integration
  ├─ Boeing Iron Bird testing (system integration rig)
  ├─ Aircraft ground testing
  ├─ Flight testing (if line-fit)
  └─ Certification activities

Phase 4: Production & Support (Ongoing)
  ├─ Production approval from Boeing
  ├─ Manufacturing quality oversight
  ├─ Service bulletin coordination
  └─ Continuous airworthiness support
```

════════════════════════════════════════════════════════════════════

🛬 **AIRBUS INTEGRATION**
─────────────────────────

**📋 Airbus Open Avionics Architecture (OAA):**

Airbus promotes modularity and interoperability:

**Key Principles:**

1. **IMA (Integrated Modular Avionics):**
   - Common computing platforms
   - Multiple applications share resources
   - ARINC 653 partitioning for safety isolation

2. **Open Standards:**
   - ARINC specifications (429, 664, 653)
   - DO-178C, DO-254, DO-160 compliance
   - Standardized interfaces reduce integration cost

3. **Supplier Engagement:**
   - Airbus Supplier Portal
   - Collaborative engineering (digital twins)
   - Configuration control via Airbus systems

**🔧 Airbus Aircraft Programs:**

**A350 XWB Integration:**

```
Platform: A350-900/1000
Architecture: Full IMA with Core Processing Input/Output Modules (CPIOM)
Key Systems:
  - CPIOM (central computing, hosted functions)
  - Cabin Intercommunication Data System (CIDS)
  - Aircraft Network System (ANS)

Integration Points:
  ✓ ARINC 664 Part 7 (AFDX) backbone
  ✓ 230V AC / 28V DC hybrid power
  ✓ Cabin Ethernet network
  ✓ Wireless LAN for cabin systems

Supplier Coordination:
  - Thales (avionics, IFE)
  - Panasonic (IFE for some airlines)
  - Rockwell Collins (now Collins) - communications
```

**A380 Integration:**

```
Platform: A380-800 (production ended 2021, still in service)
Architecture: Distributed avionics with AFDX
Key Features:
  - Dual-deck cabin networks
  - Extensive IFE capacity (up to 500 passengers)
  - Advanced environmental controls

Integration Challenges:
  ✓ Weight constraints (larger aircraft, still critical)
  ✓ Dual-deck wiring complexity
  ✓ Retrofit coordination (aging fleet)
```

**📄 Airbus Interface Control Documents:**

Airbus uses a structured ICD process similar to Boeing:

```rst
Airbus ICD Structure:

1. Introduction
   - Document reference (e.g., AI/SE-123456)
   - Revision and approval
   - Scope and applicability (MSN ranges)

2. System Overview
   - Functional description
   - Architecture context
   - Interface boundaries

3. Requirements
   - Functional requirements (derived from ATA chapters)
   - Performance requirements
   - Environmental requirements

4. Interface Specifications
   - Physical interfaces (connectors, mounting)
   - Electrical interfaces (power, signals, grounding)
   - Data interfaces (AFDX, ARINC 429, discrete I/O)
   - Software interfaces (APIs, data formats)

5. Verification
   - Interface test procedures
   - Compliance matrix
   - Test facilities (Airbus integration labs)

6. Configuration Control
   - Change request process
   - Effectivity management (MSN tracking)
   - Supplier documentation requirements
```

**Example: Cabin Management System ICD with A350:**

```yaml
ICD: AI/SE-350-5678 Rev B
Title: "Cabin Management System - Aircraft Interface"
Aircraft: A350-900
System: Panasonic eX3 CMS

Electrical Interface:
  Primary Power:
    Input: 230V AC, 400Hz, 3-phase
    Max Power: 15 kVA
    Power Quality: Per Airbus ABD0100 standard
  
  Emergency Power:
    Input: 28V DC (from emergency bus)
    Max Current: 50A
    Transition: Seamless switchover within 50ms

Data Interface:
  AFDX Network:
    Network: Cabin Network (CN)
    Redundancy: Dual redundant AFDX switches
    End Systems: 2x Ethernet ports (A/B channels)
    Virtual Links:
      VL_CMS_CMD: 5 Mbps, BAG 16ms
      VL_CMS_STATUS: 2 Mbps, BAG 32ms
      VL_CMS_MEDIA: 200 Mbps, BAG 2ms
  
  Discrete I/O:
    Inputs:
      - Cabin Ready (28V DC, active high)
      - Emergency Mode (28V DC, active high)
    Outputs:
      - System Healthy (28V DC, 1A max)
      - Fault Indication (28V DC, 1A max)

Mechanical Interface:
  Installation: Overhead avionics bay, Zone 321
  Mounting: Airbus standard rack (19-inch compatible)
  Connectors:
    - Power: Amphenol 97-3102A-28-21P
    - AFDX: 2x RJ45 (ruggedized, per EN3744-002)
    - Discrete: Amphenol 97-3106A-24-10P
  
  Weight: 12 kg (including mounting hardware)
  Dimensions: 480mm x 350mm x 200mm (W x D x H)

Environmental:
  Operating: -15°C to +55°C
  Non-Operating: -55°C to +70°C
  Humidity: Up to 95% non-condensing
  Altitude: Sea level to 43,000 ft
  Shock: Per DO-160G Section 7, Category D
  Vibration: Per DO-160G Section 8, Category S

Software Interface:
  Operating System: Linux-based (custom Airbus-approved)
  Communication:
    - AFDX stack per ARINC 664 Part 7
    - Airbus Cabin Data Protocol (ACDP) v2.3
    - JSON over HTTPS for content management
  
  APIs:
    - Cabin Lighting Control API (RESTful)
    - Passenger Service Unit (PSU) API
    - In-Seat Power (ISP) management API

Certification:
  Software: DO-178C Level D (cabin management), Level C (emergency)
  Hardware: DO-254 Level D
  Environmental: DO-160G Category S/M
  Cybersecurity: ED-202A baseline requirements
```

**🤝 Airbus Collaboration Process:**

```
Phase 0: Pre-Contract (Months -6 to 0)
  ├─ Supplier capability assessment
  ├─ NDA execution
  ├─ Access to Airbus Supplier Portal
  └─ Review of Airbus standards (ABD, ASD, AIPS)

Phase 1: Design Definition (Months 0-8)
  ├─ System Requirement Review (SRR)
  ├─ ICD negotiation and baseline
  ├─ Preliminary Design Review (PDR)
  ├─ Supplier Design Approval (SDA) application
  └─ Interface mockup and early prototyping

Phase 2: Development (Months 8-20)
  ├─ Critical Design Review (CDR)
  ├─ First Article Inspection (FAI)
  ├─ Integration at Airbus labs (Toulouse or Hamburg)
  ├─ Aircraft Integration Test (AIT)
  └─ Certification evidence generation

Phase 3: Qualification & Validation (Months 20-30)
  ├─ Qualification testing (DO-160G, DO-178C)
  ├─ Ground testing on aircraft (iron bird + actual aircraft)
  ├─ Flight testing (if applicable)
  ├─ EASA/FAA certification coordination
  └─ Production Release

Phase 4: In-Service Support (Years 1-30)
  ├─ Airbus Service Bulletin coordination
  ├─ Technical publications update
  ├─ Warranty management
  ├─ Obsolescence management
  └─ Continuous airworthiness
```

════════════════════════════════════════════════════════════════════

📋 **INTERFACE CONTROL DOCUMENT (ICD) DEVELOPMENT**
───────────────────────────────────────────────────

**🔑 ICD Best Practices:**

**1. Early Development:**

```
Timeline:
  Week 1-2: Initial draft (80% assumptions, 20% facts)
  Week 3-4: First review with OEM (identify gaps)
  Month 2-3: Iterate based on OEM feedback
  Month 4: Baseline ICD version 1.0 (design freeze)
  Ongoing: Controlled changes via CCB
```

**2. Key Sections:**

```rst
Essential ICD Content:

✅ **Electrical Interfaces:**
   - Voltage, current, frequency
   - Pin assignments (connector pinout)
   - Grounding and shielding requirements
   - Inrush current limits
   - Power sequencing

✅ **Data Interfaces:**
   - Protocol specifications (AFDX, ARINC 429, CAN, Ethernet)
   - Message definitions (format, units, range)
   - Timing requirements (latency, jitter, periodicity)
   - Error handling and redundancy
   - Security (encryption, authentication)

✅ **Mechanical Interfaces:**
   - Mounting dimensions and tolerances
   - Connector types and locations
   - Thermal management (cooling requirements)
   - Vibration isolation
   - Weight and center of gravity

✅ **Environmental Requirements:**
   - Temperature (operating and storage)
   - Altitude, pressure
   - Humidity, condensation
   - Salt fog, fungus, sand/dust
   - EMI/EMC (DO-160G categories)

✅ **Software Interfaces:**
   - API specifications (function calls, parameters)
   - Data structures and encoding
   - Protocol stacks (TCP/IP, AFDX, etc.)
   - Initialization and shutdown sequences
   - Error codes and logging

✅ **Testing & Verification:**
   - Interface test procedures
   - Test equipment requirements
   - Acceptance criteria
   - Compliance matrix (requirement vs. test)
```

**3. Change Management:**

```bash
# ICD Change Control Board (CCB) Process

Step 1: Change Request Initiated
$ submit_change_request \
  --icd "D6-87654" \
  --section "4.3.2 AFDX Virtual Link Bandwidth" \
  --change "Increase VL_IFE_VIDEO from 100 Mbps to 150 Mbps" \
  --rationale "4K video streaming requires more bandwidth"

Step 2: Impact Analysis
$ analyze_change_impact \
  --systems "IFE, AFDX Network, Power Distribution" \
  --stakeholders "OEM, Supplier, Airline" \
  --cost-schedule "Estimate additional 2 months, $50K"

Step 3: CCB Review
$ schedule_ccb_meeting \
  --attendees "Boeing System Architect, IFE Supplier, Network Engineer" \
  --date "2026-02-15" \
  --agenda "Review CR-2026-045"

Step 4: Approval & Implementation
$ approve_change \
  --cr-id "CR-2026-045" \
  --icd-revision "D6-87654 Rev D" \
  --effectivity "MSN 12345 and subsequent"

Step 5: Verification
$ verify_icd_change \
  --test "AFDX bandwidth allocation test" \
  --result "PASS - 4K video streams successfully"
```

**📊 ICD Version Control:**

```
Version Numbering Scheme:

Major.Minor.Patch (e.g., 2.3.1)

Major (X.0.0): Breaking changes
  - Interface incompatible with previous version
  - Requires hardware/software redesign
  - Example: Change from ARINC 429 to AFDX

Minor (2.X.0): Backward-compatible additions
  - New optional features
  - Additional signals or messages
  - Example: Add new AFDX virtual link

Patch (2.3.X): Clarifications and corrections
  - Typos, formatting
  - Clarify ambiguous requirements
  - No functional impact
```

════════════════════════════════════════════════════════════════════

🛡️ **CERTIFICATION PLANNING WITH OEMs**
───────────────────────────────────────

**📜 Regulatory Framework:**

```
Certification Authority:
  USA: FAA (Federal Aviation Administration)
  Europe: EASA (European Union Aviation Safety Agency)
  Other: TCCA (Canada), CASA (Australia), CAAC (China)

OEM Responsibilities:
  - Type Certificate (TC) holder
  - Approve design changes
  - Coordinate with certification authorities
  - Delegate authority to suppliers (DER, DOA)

Supplier Responsibilities:
  - Develop certification plans
  - Generate certification data
  - Support OEM in authority interactions
  - Maintain design approval (if DOA)
```

**🔧 Certification Approaches:**

**1. Line-Fit Certification (New Aircraft Production):**

```
Approach: Amend Type Certificate (TC)
Process:
  ├─ Supplier develops system per OEM requirements
  ├─ OEM integrates system into aircraft design
  ├─ Certification data package submitted to authority
  ├─ Authority reviews and approves TC amendment
  └─ System installed on production aircraft

Timeline: 2-4 years
Cost: High (shared between OEM and supplier)
Authority Interaction: Moderate (OEM leads)

Example: New IFE system for 787-10
  - Thales AVANT IFE certified as part of 787-10 TC
  - FAA and EASA reviewed DO-178C/DO-254 evidence
  - Approved for line-fit installation starting MSN 800
```

**2. Retrofit Certification (Existing Aircraft):**

```
Approach: Supplemental Type Certificate (STC)
Process:
  ├─ Airline or modification shop initiates STC
  ├─ Supplier provides system and certification data
  ├─ Installer performs modification per STC
  ├─ Authority approves STC
  └─ System installed on in-service aircraft

Timeline: 1-2 years
Cost: Lower than line-fit (focused on modified systems)
Authority Interaction: High (airline or modifier leads)

Example: Gogo 2Ku connectivity retrofit for 737NG
  - STC obtained for antenna and cabin equipment
  - Installed on existing Alaska Airlines 737-800 fleet
  - FAA STC ST01234LA approved in 2020
```

**📋 Certification Plan Template:**

```rst
Certification Plan Outline:

1. Introduction
   - System description
   - Certification basis (regulations: 14 CFR Part 25, CS-25)
   - Certification approach (TC amendment, STC, PMA)

2. Compliance Matrix
   | Regulation | Requirement | Compliance Method | Responsibility |
   |:-----------|:------------|:------------------|:---------------|
   | 25.1301 | Function & installation | Test + Analysis | Supplier |
   | 25.1309 | Safety assessment | FHA, PSSA, SSA | OEM + Supplier |
   | 25.1431 | Electronic equipment | DO-160G testing | Supplier |

3. Design Assurance
   - Software: DO-178C Level X
   - Hardware: DO-254 Level X
   - System: ARP4754A / ARP4761

4. Verification & Validation
   - Requirements-based testing
   - Integration testing (aircraft level)
   - Flight testing (if required)

5. Certification Schedule
   - Milestones (PDR, CDR, FAI, Flight Test)
   - Authority engagement points
   - Certification completion date

6. Roles & Responsibilities
   - OEM: Design authority, TC holder
   - Supplier: Design, testing, data generation
   - Authority: Review, approval, oversight
```

**🤝 Working with OEM Designated Engineering Representatives (DER):**

```
DER Role:
  - FAA-authorized individual to approve specific designs
  - Acts on behalf of FAA for defined scope
  - Reduces FAA workload, speeds approval

Types:
  - DER-Manufacturing: Production processes
  - DER-Flight Test: Flight test planning and conduct
  - DER-Equipment: Systems and equipment design

Supplier Coordination:
  1. Identify appropriate DER (OEM provides list)
  2. Submit design data to DER
  3. DER reviews and provides findings
  4. Supplier addresses findings
  5. DER approves and signs FAA Form 8110-3

Example:
  - IFE supplier submits DO-178C data to OEM's software DER
  - DER reviews source code, verification results
  - DER issues approval for DAL Level C software
  - OEM includes DER approval in TC amendment package
```

════════════════════════════════════════════════════════════════════

🔧 **POST-DELIVERY SUPPORT PROCEDURES**
───────────────────────────────────────

**📦 Support Lifecycle:**

```
Aircraft Lifecycle: 20-30 years (typical commercial aircraft)

Support Phases:
  Year 0-5: Warranty period, high engagement
  Year 5-15: Mature operations, routine support
  Year 15-25: Aging fleet, obsolescence management
  Year 25+: Phase-out or major retrofit
```

**🛠️ Service Bulletin Coordination:**

```rst
Service Bulletin (SB) Process:

1. Issue Identification
   - In-service issue reported (airline or OEM)
   - Design improvement opportunity
   - Regulatory directive (AD - Airworthiness Directive)

2. Root Cause Analysis
   - Supplier investigates issue
   - Coordinate with OEM engineering
   - Determine corrective action

3. Service Bulletin Development
   - SB document prepared by supplier
   - Reviewed and approved by OEM
   - Published to airlines via OEM portal

4. Implementation
   - Airlines review SB (mandatory vs. optional)
   - Schedule maintenance downtime
   - Install modification per SB instructions
   - Return-to-service inspection

5. Effectiveness Monitoring
   - Track implementation across fleet
   - Monitor for recurrence
   - Close out SB once effective

Example SB Format:

---
SERVICE BULLETIN

SB Number: IFE-2026-001
Date: January 15, 2026
Subject: Software Update for Seat Display Unit
Aircraft: Boeing 787-9, MSN 45000-45100
System: Thales AVANT IFE

REASON:
Customers reported intermittent display freezing during flight.
Root cause identified as memory leak in video codec driver.

ACCOMPLISHMENT:
Install software version 5.2.3 on all Seat Display Units.

COMPLIANCE:
Recommended within 90 days. No airworthiness impact.

LABOR: 2 hours per aircraft (320 displays)

PARTS:
  - USB flash drive with software (provided by Thales)
  - No hardware changes required

PROCEDURE:
  1. Power down IFE system
  2. Access SDU service port (behind overhead panel)
  3. Connect USB drive and initiate update
  4. Verify software version 5.2.3 installed
  5. Test functionality per checklist
  6. Update aircraft maintenance log

WARRANTY:
Labor reimbursed if installed within warranty period.
---
```

**📞 Technical Support Channels:**

```yaml
Support Tiers:

Tier 1: Airline Maintenance Technicians
  - Troubleshoot basic issues (resets, connector checks)
  - Follow maintenance manuals and SBs
  - Escalate to Tier 2 if unresolved

Tier 2: OEM Regional Support Centers
  - Remote diagnosis (log file analysis)
  - Provide technical guidance
  - Coordinate parts shipment
  - Escalate to Tier 3 for design issues

Tier 3: Supplier Engineering (original designer)
  - Deep technical analysis
  - Design investigations
  - Software patches or hardware redesign
  - Issue Service Bulletins

Example Support Request:

Ticket #: SUP-2026-7890
Date: 2026-01-14
Aircraft: Airbus A350-900, MSN 12345
System: IFE Server (LRU P/N 12345-001)
Issue: Server fails to boot, no LED indication

Tier 1 Action:
  - Checked power input: 115V AC present
  - Reseated LRU: No change
  - Escalated to Tier 2

Tier 2 Action:
  - Requested log files: None (system not booting)
  - Recommended LRU replacement
  - Shipped spare LRU (P/N 12345-001-05) overnight
  - Escalated to Tier 3 for failed unit analysis

Tier 3 Action:
  - Received failed LRU at depot
  - Analysis: Power supply capacitor failure
  - Root cause: Component from bad manufacturing lot
  - Action: Inspect all LRUs from same lot (SB issued)
  - Resolution: Replace capacitors, update BOM
```

**💰 Warranty Management:**

```
Warranty Terms (typical):

Standard Warranty:
  - Duration: 24 months from delivery or 5,000 flight hours (whichever first)
  - Coverage: Material and workmanship defects
  - Exclusions: Damage from misuse, environmental extremes

Extended Warranty:
  - Duration: Up to 10 years (purchased separately)
  - Coverage: Broader, includes design defects
  - Service: Enhanced support (dedicated engineers)

Warranty Claim Process:
  1. Airline identifies failure
  2. Supplier authorizes return (RMA - Return Material Authorization)
  3. Failed unit shipped to supplier depot
  4. Supplier analyzes failure (warranty or non-warranty)
  5. If warranty: Repair/replace at no charge
  6. If non-warranty: Quote for repair provided to airline
```

════════════════════════════════════════════════════════════════════

📞 **COMMUNICATION PROTOCOLS (AIRLINE/OEM)**
───────────────────────────────────────────

**🔀 Communication Channels:**

```
Technical Communication:
  - Engineering meetings (weekly/monthly)
  - Interface Control Working Groups (ICWG)
  - Technical reviews (PDR, CDR)
  - Problem reporting and corrective action (PRACA)

Commercial Communication:
  - Contract negotiations (legal, procurement)
  - Pricing and delivery schedules
  - Change order management
  - Business reviews (quarterly)

Certification Communication:
  - Certification plan reviews
  - Authority coordination (FAA/EASA meetings)
  - Compliance demonstration
  - Certification milestone tracking

Tools:
  - SharePoint sites (Boeing, Airbus portals)
  - Email and video conferencing
  - Collaborative design tools (CAD integration)
  - Problem tracking systems (Jira, ServiceNow)
```

**📊 Stakeholder Communication Matrix:**

```rst
| Stakeholder | Frequency | Topics | Lead |
|:------------|:----------|:-------|:-----|
| OEM Program Office | Weekly | Schedule, risks, issues | Supplier PM |
| OEM System Architect | Bi-weekly | Design, ICD changes | Supplier Architect |
| OEM Certification | Monthly | Cert plan, evidence | Supplier Cert Lead |
| OEM Supply Chain | Monthly | Delivery, quality | Supplier Ops |
| OEM Engineering | As needed | Technical issues | Supplier Engineering |
| Airline (if direct) | Quarterly | In-service performance | Supplier Support |
| FAA/EASA | Milestones | Certification progress | OEM + Supplier |
```

**📧 Communication Best Practices:**

```
✅ Use standardized templates for technical communication
✅ Document all decisions (meeting minutes, decision logs)
✅ Maintain traceability (requirements to design to verification)
✅ Escalate issues promptly (risk management)
✅ Respect OEM configuration control processes
✅ Protect proprietary information (NDAs, ITAR/EAR)
✅ Establish clear points of contact (RACI matrix)
```

════════════════════════════════════════════════════════════════════

📝 **EXAM QUESTIONS**
─────────────────────

**Question 1: Boeing ICD Process**

**Q:** You are developing an IFE system for the Boeing 787. During the ICD review, 
Boeing requests that you change the AFDX virtual link bandwidth allocation from 
100 Mbps to 50 Mbps due to network capacity constraints. This change would require 
reducing video quality from 1080p to 720p. How should you proceed?

**Answer:**

**Step 1: Impact Analysis**
- Assess impact on system performance (video quality degradation)
- Identify affected requirements (video quality specs)
- Estimate cost and schedule impact (software changes, re-testing)
- Review customer (airline) requirements (may specify 1080p minimum)

**Step 2: Negotiate with Boeing**
- Present analysis showing customer impact
- Propose alternatives:
  * Implement more efficient video codec (H.265 vs. H.264)
  * Use adaptive bitrate streaming (lower bandwidth, maintain quality)
  * Request additional AFDX virtual links if available
  * Negotiate bandwidth increase on less critical VLs

**Step 3: Formal Change Process**
- If change accepted: Initiate ICD Change Request (CR)
- Update ICD document to new revision
- Conduct Change Control Board (CCB) meeting
- Obtain approvals from all stakeholders
- Update design and re-verify interface

**Step 4: Certification Impact**
- Assess if change affects certification (likely minimal)
- Update certification data if required
- Inform DER if approval previously obtained

**Best Approach:** Propose technical alternative (better codec) rather than 
accepting performance degradation. Always document rationale for decisions.

────────────────────────────────────────────────────────────────────

**Question 2: Airbus Collaboration**

**Q:** Your company has been selected to provide a cabin management system for 
the Airbus A350-1000. Airbus requires integration with the Common Core System (CCS) 
via AFDX. You've never integrated with CCS before. What are the first steps to 
ensure successful collaboration?

**Answer:**

**Phase 1: Onboarding (Week 1-2)**
1. Execute NDA with Airbus
2. Obtain access to Airbus Supplier Portal
3. Request CCS interface specifications from Airbus
4. Identify Airbus technical point of contact
5. Download relevant Airbus standards (ABD, AIPS documents)

**Phase 2: Requirements Clarification (Week 3-6)**
1. Review CCS AFDX interface specifications
2. Identify any ambiguities or gaps
3. Schedule technical meeting with Airbus CCS team
4. Request access to Airbus integration lab (if available)
5. Obtain sample AFDX message definitions and protocols

**Phase 3: Design Approach (Month 2-3)**
1. Develop preliminary architecture
2. Create ICD draft (cabin management to CCS interface)
3. Conduct Preliminary Design Review (PDR) with Airbus
4. Baseline ICD version 1.0
5. Begin prototype development

**Phase 4: Early Integration (Month 4-6)**
1. Request CCS simulator or test bench access
2. Develop AFDX communication software
3. Perform interface testing at supplier facility
4. Schedule integration testing at Airbus lab
5. Resolve any interface issues

**Key Success Factors:**
- Early engagement with Airbus technical team
- Understand ARINC 653 partitioning (if hosted on CCS)
- Proactive communication of risks and issues
- Leverage existing Airbus supplier relationships
- Budget for travel to Airbus sites (Toulouse, Hamburg)

────────────────────────────────────────────────────────────────────

**Question 3: ICD Change Management**

**Q:** Six months into production, an airline reports that the cabin Wi-Fi system 
intermittently loses connectivity during cruise. Investigation reveals that the 
issue is caused by electrical noise from the nearby galley equipment, which was 
not specified in the original ICD. The OEM wants you to fix the issue. How do you 
handle this situation from an ICD perspective?

**Answer:**

**Step 1: Root Cause Analysis**
- Confirm electrical noise as root cause (EMI testing)
- Determine why this wasn't caught earlier:
  * ICD did not specify galley equipment EMI environment
  * DO-160G testing performed to Category M (typical), but galley is Category Q
  * Aircraft wiring routing not per ICD installation drawing
- Identify responsible party (supplier, OEM, installer)

**Step 2: Technical Solution**
- Short-term fix: Re-route Wi-Fi cabling away from galley
- Long-term fix: Add EMI filtering to Wi-Fi equipment
- Update ICD to specify:
  * Galley equipment EMI levels
  * Minimum separation distance
  * Cable shielding requirements
  * Installation guidelines

**Step 3: ICD Update Process**
- Initiate ICD Change Request (CR-2026-XXX)
- Update ICD Section 4.5 "Environmental Requirements":
  * Add: "EMI Environment: DO-160G Category Q (galley vicinity)"
  * Add: "Minimum separation from galley: 300mm"
- Increment ICD revision (e.g., Rev C to Rev D)
- Conduct CCB review and approval

**Step 4: Retrofit Coordination**
- Issue Service Bulletin (SB) for affected aircraft
- Provide retrofit kit (EMI filters, new cables)
- Coordinate with OEM for SB distribution to airlines
- Track implementation across fleet

**Step 5: Lessons Learned**
- Update design checklists to consider adjacent equipment EMI
- Improve ICD review process (include EMI specialists)
- Ensure aircraft-level EMI survey during integration testing

**Cost/Responsibility:**
- If ICD was ambiguous: Shared cost (supplier + OEM)
- If supplier design defect: Supplier bears cost
- If installation error: Installer bears cost
- Negotiate based on root cause and contract terms

────────────────────────────────────────────────────────────────────

**Question 4: Certification Coordination**

**Q:** Your cabin connectivity system requires DO-178C Level C certification for 
the core router software and Level D for the content management software. The OEM 
is pursuing a Type Certificate amendment for a new aircraft variant. What 
certification artifacts do you need to provide to the OEM, and how do you 
coordinate with their DER?

**Answer:**

**DO-178C Level C Artifacts (Core Router Software):**

1. **Planning Documents:**
   - Plan for Software Aspects of Certification (PSAC)
   - Software Development Plan (SDP)
   - Software Verification Plan (SVP)
   - Software Configuration Management Plan (SCMP)
   - Software Quality Assurance Plan (SQAP)

2. **Requirements:**
   - Software Requirements Standards (SRS)
   - Software Requirements Data (SRD)
   - Traceability: System Requirements → Software Requirements

3. **Design:**
   - Software Design Standards (SDS)
   - Software Design Description (SDD)
   - Traceability: Software Requirements → Design

4. **Implementation:**
   - Source Code (C/C++)
   - Coding Standards compliance (MISRA, etc.)
   - Traceability: Design → Source Code

5. **Verification:**
   - Test Cases and Procedures
   - Test Results
   - Structural Coverage Analysis (Decision Coverage for Level C)
   - Traceability: Requirements → Test Cases

6. **Configuration Management:**
   - Software Configuration Index (SCI)
   - Problem Reports and Change Requests
   - Software Accomplishment Summary (SAS)

**DO-178C Level D Artifacts (Content Management Software):**
- Similar to Level C, but reduced rigor:
  - No structural coverage analysis required
  - Simplified verification (less test cases)
  - Relaxed independence requirements

**DER Coordination Process:**

**Step 1: Initial Engagement (Month 0)**
- OEM identifies DER (software specialist)
- Supplier provides certification plan (PSAC) for review
- DER provides feedback on approach
- Establish review schedule

**Step 2: Incremental Reviews (Months 1-18)**
- Submit planning documents (PSAC, SDP, SVP, etc.) → DER reviews
- Submit requirements (SRD) → DER reviews traceability
- Submit design (SDD) → DER reviews architecture
- Submit code and verification results → DER reviews coverage

**Step 3: Final Review (Month 18-20)**
- Submit Software Accomplishment Summary (SAS)
- DER conducts final audit:
  * Review all artifacts for completeness
  * Verify objectives met per DO-178C Table A-3 (Level C), A-6 (Level D)
  * Check configuration management records
  * Ensure traceability throughout

**Step 4: DER Approval (Month 20)**
- DER issues FAA Form 8110-3 (Statement of Compliance)
- DER signs off that software meets DO-178C Level C/D
- OEM includes DER approval in Type Certificate amendment package
- FAA reviews OEM submission (DER approval expedites process)

**Step 5: FAA Acceptance (Month 22)**
- FAA accepts Type Certificate amendment
- Software approved for installation on certified aircraft
- Production can commence

**Best Practices:**
- Start DER engagement early (certification planning phase)
- Conduct incremental reviews (don't wait until the end)
- Address DER findings promptly (delays ripple through schedule)
- Maintain rigorous configuration management (DER will audit)
- Build good relationship with DER (repeat engagements likely)

────────────────────────────────────────────────────────────────────

**Question 5: Post-Delivery Support**

**Q:** Three years after delivery, an airline reports that your in-flight 
entertainment system is experiencing display failures on a specific aircraft 
(MSN 45678). The failure rate is 2-3 displays per month, which is abnormal 
(fleet average is 0.1 per month). How do you manage this support issue?

**Answer:**

**Phase 1: Initial Triage (Day 1-3)**
1. **Gather Data:**
   - Aircraft details (MSN, configuration, flight hours)
   - Failure symptoms (display goes blank, frozen, etc.)
   - Frequency and conditions (takeoff, cruise, landing?)
   - Maintenance actions taken (resets, replacements)

2. **Check Known Issues:**
   - Search problem database for similar reports
   - Review Service Bulletins (already issued?)
   - Check if aircraft has unique configuration

3. **Tier 1 Support:**
   - Guide airline maintenance to basic troubleshooting
   - Check power connections, reseat displays
   - Collect log files from IFE server

**Phase 2: Root Cause Analysis (Week 1-2)**
1. **Data Analysis:**
   - Review log files: Any error patterns?
   - Compare failed displays: Same seat positions? Same hardware revision?
   - Environmental factors: Temperature, vibration, humidity?

2. **Hypothesis:**
   - Bad manufacturing lot (check serial numbers)
   - Aircraft-specific issue (wiring, power quality)
   - Software bug triggered by specific content

3. **Testing:**
   - Request failed displays be shipped to depot
   - Perform failure analysis (electrical, mechanical)
   - Attempt to reproduce failure in lab

**Phase 3: Root Cause Identified (Week 3)**
**Finding:** Displays on MSN 45678 are from manufacturing lot L2023-05, which 
used a defective batch of LCD driver ICs. High vibration during takeoff causes 
solder joint failures.

**Verification:**
- Check other aircraft with lot L2023-05 displays → same issue
- Inspect solder joints → cracks visible under microscope
- Thermal cycling + vibration test → failures reproduced

**Phase 4: Corrective Action (Week 4-6)**
1. **Immediate Action:**
   - Identify all displays from lot L2023-05 (50 aircraft, 10,000 displays)
   - Issue Fleet Campaign (urgent notification to all airlines)
   - Provide interim inspection procedure (visual solder joint check)

2. **Long-Term Fix:**
   - Issue Service Bulletin: SB-IFE-2026-010
   - Replace all lot L2023-05 displays
   - Provide replacement displays at no charge (warranty extension)

3. **Process Improvement:**
   - Update manufacturing process (better solder joint inspection)
   - Add vibration testing to acceptance criteria
   - Screen all existing inventory for same issue

**Phase 5: Implementation (Month 2-6)**
1. **Logistics:**
   - Ship replacement displays to affected airlines (priority: MSN 45678)
   - Coordinate installation during scheduled maintenance
   - Track progress (spreadsheet or database)

2. **Verification:**
   - Monitor failure rates post-replacement
   - Confirm issue resolved (no failures after 3 months)
   - Close out Service Bulletin

**Phase 6: Lessons Learned (Month 6)**
1. **Documentation:**
   - Update Failure Modes and Effects Analysis (FMEA)
   - Revise manufacturing quality plan
   - Document root cause for future reference

2. **Communication:**
   - Inform OEM of issue and resolution
   - Update certification authorities if required
   - Share lessons learned with engineering team

**Cost Management:**
- Warranty claim: Supplier bears cost (~$500K for 10,000 displays)
- Labor reimbursement: Negotiate with airlines (~$100K)
- Root cause analysis: Internal cost (~$50K)
- **Total impact: $650K** (painful but necessary for customer satisfaction)

**Outcome:**
- Issue resolved within 6 months
- No aircraft grounded (interim inspection allowed continued operation)
- Customer satisfaction maintained (proactive communication, no-charge fix)
- Process improved (prevent future similar issues)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
──────────────────────────

**OEM Collaboration Essentials:**

□ Understand Boeing and Airbus integration processes  
□ Develop comprehensive Interface Control Documents  
□ Establish change control procedures  
□ Coordinate certification with OEM and authorities  
□ Plan for long-term post-delivery support  
□ Maintain effective communication channels  
□ Manage warranty and service bulletins  
□ Build relationships with OEM technical teams

════════════════════════════════════════════════════════════════════

🎓 **KEY TAKEAWAYS**
───────────────────

1. **Early Engagement:** Start ICD development and OEM coordination early
2. **Rigorous Change Control:** All interface changes must go through CCB
3. **Certification Planning:** Coordinate with OEM DER from day one
4. **Long-Term Support:** Aircraft operate 20-30 years, plan accordingly
5. **Communication:** Clear, frequent communication prevents issues
6. **Standards Compliance:** Follow OEM design standards rigorously
7. **Flexibility:** Be prepared to adapt to OEM requirements and feedback

════════════════════════════════════════════════════════════════════

**End of OEM Collaboration & Integration Cheatsheet** 🎯
