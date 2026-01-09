Here is a concise, expanded **AUTOSAR Classic Platform – BSW Cheat Sheet** (R25-11 / early 2026).
⭐ This enhanced version adds keywords, ComStack flows, configuration tooling, security/diagnostics notes, and a short comparison with AUTOSAR Adaptive.

.. contents:: Table of Contents
	:local:
	:depth: 2

=================================
AUTOSAR Classic Platform — BSW
=================================

📖 Overview
--------

AUTOSAR Classic provides a layered, configurable Basic Software (BSW) stack and a standardized Runtime Environment (RTE) that decouples application SW Components (SWC) from hardware.
⭐ This cheat sheet focuses on the BSW layer (services, ECU abstraction, MCAL, complex drivers) and adds practical keywords and integration notes useful for developers and integrators.

🏗️ Architecture Layers
-------------------

- **Application Layer** — SW Components (SWC), runnable entities, ports. Implement vehicle features.
- **RTE** — Runtime Environment; maps SWC ports/messages to communication primitives and provides scheduling hooks.
- **BSW** — Basic Software: Services, ECU Abstraction, MCAL, Complex Drivers (what this file documents).

BSW Layer Structure (top → bottom)

- Services Layer (OS, BswM, Com, Dem, Dcm, NvM)
- ECU Abstraction Layer (ECU peripheral abstraction, BusIf)
- Microcontroller Abstraction Layer (MCAL: Dio, Adc, Gpt, Mcu, Fls)
- Complex Drivers (special HW, vendor-specific)

⭐ Core Keywords & Glossary
------------------------

⭐ This quick glossary lists common AUTOSAR Classic keywords, short definition and typical usage.

- **AUTOSAR** — AUTomotive Open System ARchitecture standard for automotive software interoperability.
- **BSW (Basic Software)** — Standardized services & drivers between RTE and hardware.
- **RTE (Runtime Environment)** — Glue layer exposing ports/APIs to SWCs; generated from ARXML.
- **SWC (Software Component)** — Functional software module (implements features) communicating via ports.
- **ARXML** — AUTOSAR XML metadata files (module/config descriptions, SWC interfaces).
- **MCAL** — Microcontroller Abstraction Layer: hardware-specific drivers (Dio, Adc, Spi, Fls).
- **ECU Abstraction** — Abstracts board-level hardware (sensors/actuators) from upper services.
- **BswM** — BSW Mode Manager: central mode coordination (e.g., wake/sleep modes).
- **EcuM** — ECU Manager: ECU startup/shutdown sequencing and basic power management.
- **SchM** — Scheduler Module: provides exclusive areas and synchronization between BSW modules and OS.
- **Com** — AUTOSAR COM module: signal packing/unpacking, signal buffering for RTE.
- **PduR** — PDU Router: routes I-PDUs between Com, Tp, and lower-layer BusIf modules.
- **CanIf / EthIf / LinIf** — Bus Interface modules: abstract bus-specific frame handling.
- **CanTp / LinTp / FrTp** — Transport Protocol modules for segmentation/reassembly (UDS diagnostic transport).
- **DoIP / SOME/IP** — Ethernet-based transport/diagnostics (DoIP for diagnostics, SOME/IP for service-oriented communication).
- **SecOC** — Secure Onboard Communication: message authentication and freshness for CAN/Ethernet.
⭐ - **CryIf / Csm / KeyM** — Crypto Interface, Crypto Service Manager, Key Manager for centralized crypto usage.
- **Dem** — Diagnostic Event Manager: fault logging, event aging, status.
- **Dcm** — Diagnostic Communication Manager: UDS protocol handling (0x10, 0x22, 0x2E, 0x19, 0x31, 0x34, etc.).
- **NvM** — NVRAM Manager: manages non-volatile data (EA/FEE/FLS backends).
- **Fls / Ea / Fee** — Flash driver (on-chip), EEPROM abstraction (EA), Flash EEPROM Emulation (FEE).
- **Det** — Default Error Tracer API used during development for assertions.
- **WdgM** — Watchdog Manager coordinating watchdog supervision.
- **OS** — Real-time operating system (e.g., AUTOSAR-conformant scheduling, tasks, resources).
- **ECUextract** — ECU-specific configuration produced by toolchains (ARXML subset for that ECU).

ComStack Flow (practical)
-------------------------

Typical signal/message flow for an outgoing message (SWC → CAN/Ethernet):

1. SWC invokes RTE write API for a signal (e.g., Rte_Write_Sig_X()).
2. RTE forwards to **Com** (signal-level) which performs signal packing and scheduling.
3. **PduR** receives the I-PDU and decides route (local, CAN, Eth, diagnostics).
4. PduR calls the appropriate BusIf (e.g., CanIf) with the PDU.
5. BusIf interacts with the lower-level driver (CanDrv) or controller-specific driver to transmit frame on bus.
6. On reception, inverse path: CanDrv → CanIf → PduR → Com → RTE → SWC.

Transport & Routing notes:

- **Segmentation/reassembly** handled by CanTp/LinTp; transport choices impact timing and memory.
- **SOME/IP** uses service discovery and serialization; configuration differs from signal-based COM.
- **SecOC** often augments the Com/PduR path by inserting authentication fields and freshness counters.

⚙️ Configuration & Tooling
-----------------------

Common vendor tooling and recommended practices:

- **EB tresos** — BSW integration and configuration, commonly used with AUTOSAR Classic stacks.
- **Vector DaVinci / MICROSAR** — Module configuration and generation for Vector stacks.
- **Artop / Arctic Studio / AUTOSAR Builder** — ARXML manipulation, RTE generation helpers.
- **ARXML management** — Keep SWC descriptions, ECU extracts, and BSW configs in separate, versioned artifacts.

🟢 🟢 Best practices:

- Use CI to validate ARXML generation and RTE codegen.
- Maintain separate configurations for development, test, and production (feature flags, DET vs DEM behaviors).
- Validate PduR routing with automated tests simulating upper and lower layers.

Diagnostics, Boot & Update Flow
------------------------------

- **Startup**: BootROM → FBL → EcuM init (Mcu, Gpt, Wdg) → OS start → BswM orchestrates mode entry.
- **UDS Diagnostics**: Tester ↔ Dcm (UDS) ↔ Dem logs → NvM stores persistent data; transport via CanTp/DoIP.
⭐ - **FBL / OTA**: Secure boot verification via CryIf + KeyM, FLS/Ea/Fee used by bootloader to write images.

🔐 Security & Crypto
-----------------

⭐ - **Secure Boot**: Verify boot images using Csm/CryIf; manage keys with KeyM.
- **In-vehicle message security**: SecOC provides MACs and freshness counters (sequence counters). Ensure monotonic counters persist via NvM.
- **Crypto acceleration**: Use CryptoDrv for HW offload; fall back to software library where needed.

⚖️ Classic vs Adaptive — short comparison
-------------------------------------

- **Classic**: statically configured, deterministic, RTE-per-ECU, optimized for embedded controllers.
- **Adaptive**: dynamic, service-oriented (SOME/IP), POSIX-like, suited for high-performance domain controllers.
⭐ - Hybrid systems typically use Classic for safety-critical ECUs and Adaptive for compute-heavy functions; gateways map between them.

Quick Reference — Most-used BSW modules (2026)

- Core: `OS`, `EcuM`, `BswM`, `SchM`, `Det`, `Mcu`, `Port`, `Dio`.
- Communication: `Com`, `PduR`, `CanIf`, `EthIf`, `SoAd`, `CanTp`, `DoIP`.
- Diagnostics: `Dem`, `Dcm`, `Fbl`.
- Memory: `NvM`, `MemIf`, `Fls`, `Ea`, `Fee`.
⭐ - Security: `SecOC`, `CryIf`, `Csm`, `KeyM`.

📚 References & Standards
----------------------

- AUTOSAR Classic module specs (4.x / R25-11)
- ISO 26262 (Functional Safety), SAE J3061 (cybersecurity), ISO 14229 (UDS), ISO 11898 (CAN), SOME/IP and DoIP specs

----

Last updated: January 2026 (R25-11)

If you want, I can:

- add an ARXML signal & PDU example showing Com → PduR → CanIf routing,
- create a minimal integration checklist for ECU acceptance testing, or
- generate a PlantUML diagram showing the ComStack flow.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
