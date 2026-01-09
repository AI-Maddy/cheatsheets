
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **AUTOSAR (AUTomotive Open System ARchitecture) Classic Platform**, the industry standard for deeply embedded, real-time, and safety-critical automotive ECUs.

---

🏗️ **1. The 3-Layer Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary goal of AUTOSAR is to decouple application software from the underlying hardware.

⭐ | Layer | Responsibility | Key Elements |
| --- | --- | --- |
| **Application Layer** | Hardware-independent functional logic. | Software Components (SWCs), Ports, Runnables. |
| **RTE (Runtime Environment)** | The "Glue." Manages communication between SWCs and between SWCs and BSW. | Rte_Read, Rte_Write, Rte_Call. |
| **BSW (Basic Software)** | Standardized services and hardware drivers. | Services, Abstraction, MCAL, CDD. |

---

📡 **2. Deep Dive: BSW (Basic Software)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The BSW is further divided into sub-layers to maximize portability:

- **Services Layer (Top):** Provides high-level services like Network Management (CanNm), Memory Management (NvM), Diagnostics (DCM, DEM), and the Operating System (OS).
- **ECU Abstraction Layer:** Bridges the gap between hardware-specific drivers and the Services layer. It makes software independent of whether a sensor is connected via internal pins or an external bus.
- **MCAL (Microcontroller Abstraction Layer):** The lowest layer. It contains drivers (CAN, SPI, ADC, DIO) that talk directly to the microcontroller registers.
⭐ - **Complex Device Driver (CDD):** A "bypass" for non-standardized or timing-critical hardware that requires direct access to the MCAL or hardware.

---

🎓 **3. Communication Concepts**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AUTOSAR uses a **Virtual Functional Bus (VFB)** concept, meaning an SWC doesn't care if it's talking to another SWC on the same chip or across the vehicle.

- **Sender-Receiver (S/R):** Data-centric (e.g., "Current Speed"). One sender to many receivers.
- **Client-Server (C/S):** Operation-centric (e.g., "Reset Trip Meter"). A client calls an operation; a server executes it and returns a result.
- **Ports:** The "entry/exit" points of a component.
- **P-Port (Provided):** Offers data or a service.
- **R-Port (Required):** Needs data or a service.

---

⭐ 📌 **4. Key Terminology**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **SWC (Software Component):** An atomic unit of application logic.
- **Runnable:** The smallest piece of executable code within an SWC (mapped to an OS Task).
- **ARXML:** The XML format used for all AUTOSAR configuration and exchange.
- **PDU (Protocol Data Unit):** The data structure used in the communication stack.
- **ComStack:** The "Communication Stack" (COM → PduR → CanIf → CanDrv).

---

📌 **5. Methodology & Workflow**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AUTOSAR follows a strict configuration-based development cycle:

1. **System Design:** Define SWCs and their connections in an Authoring Tool.
2. **ECU Extraction:** Filter the system description for a specific ECU.
3. **Configuration:** Configure BSW modules (e.g., set CAN bitrates, define NVM blocks) and the RTE.
4. **Generation:** Tools generate ``.c`` and ``.h`` files based on the configuration.
5. **Build:** Compile the generated code with the handwritten application code.

---

⚖️ 📌 **6. Classic vs. Adaptive (Quick Comparison)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Feature | Classic Platform | Adaptive Platform |
| --- | --- | --- |
| **Target** | Hard real-time (Brakes, Airbags) | High-performance (ADAS, Infotainment) |
| **Language** | C | C++ |
| **OS** | OSEK-based (Static) | POSIX-compliant (Dynamic) |
| **Communication** | Signal-based (CAN, LIN) | Service-oriented (SOME/IP) |

Would you like me to create a detailed breakdown of a specific BSW module, like the **Communication Stack (ComStack)** or **Memory Stack (MemStack)**?

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
