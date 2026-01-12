⚡ **ARM AMP (Asymmetric Multi-Processing) Cheatsheet** ⚡
================================================================

A concise **cheatsheet** for **AMP** on **ARM** architectures, focusing on internals in heterogeneous multicore SoCs:
- **Cortex-A** + **Cortex-M/R** combinations 
- Examples: *Zynq, i.MX, STM32MP1, Zynq UltraScale+*

🎯 **AMP vs SMP Quick Comparison**

.. container:: comparison-table

   | 📊 Aspect             | 🟦 **SMP (Symmetric)**                  | 🟪 **AMP (Asymmetric)**                        |
   |---------------------|----------------------------------------|------------------------------------------------|
   | 🔄 Core equality     | ✅ All cores identical & equal          | ❓ Heterogeneous (A+M/R) or independent       |
   | 💾 OS instance       | 1️⃣ Single OS/kernel across all cores   | 🔀 Multiple OS/firmware per core              |
   | 📦 Resource mgmt     | 🤖 Unified scheduler, dynamic          | 🔒 Static partitioning, manual coordination   |
   | 🧠 Memory model      | 🔗 Shared + coherent (cache)            | 🎯 Private + explicitly shared regions        |
   | 💡 Typical use       | ⚙️ General-purpose load balancing      | 🚀 Mixed-criticality (RT + general)           |
   | ⚙️ Complexity        | ✨ Easy programming (one OS)            | 🔧 More manual (IPC, partitioning)            |
   | 🔐 Cache coherency   | 🛡️ Hardware (CCI/ACE)                  | ❌ Often none; manual for shared              |


🏗️ **Typical ARM AMP Hardware Layout**
=======================================

**Master ↔ Remote Architecture** (e.g., Cortex-A ↔ Cortex-M/R)

::

    ┌─────────────────────────────────────────────────────────────┐
    │                    SYSTEM ON CHIP (SoC)                     │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │  Master (Cortex-A) - Linux / High-Performance       │  │
    │  │  ├─ L1/L2 Cache (coherent)                          │  │
    │  │  ├─ MMU (Virtual→Physical mapping)                  │  │
    │  │  └─ GIC Interrupt Controller                        │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                         ⬍                                   │
    │                    AXI/AHB Bridge                           │
    │                         ⬇                                   │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │  Remote (Cortex-M/R) - RTOS / Real-Time / BareM    │  │
    │  │  ├─ Private SRAM/TCM (tightly coupled)              │  │
    │  │  ├─ MPU (Region-based protection)                   │  │
    │  │  └─ NVIC Interrupt Controller                       │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                             │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │  🧠 Shared Memory Regions (DDR + OCM)                │  │
    │  │  ├─ VirtIO Rings (4KB aligned) [RPMsg]              │  │
    │  │  ├─ Shared Data Buffers                             │  │
    │  │  └─ Mailbox/MU Signaling (IPI)                      │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

**Key Hardware Components:**

- 🎯 **Master core(s)**: Cortex-A (Linux OS, application processor)
- 🎯 **Remote core(s)**: Cortex-M / Cortex-R (RTOS, bare-metal, real-time)

**Memory Hierarchy:**

- 🧠 **DDR / Shared DRAM**: Large buffers, shared data (slow but large)
- ⚡ **On-chip SRAM / TCM**: Per-core private memory (fast, tightly coupled)
- 🔥 **OCMC / OCM**: On-Chip Memory Controller for low-latency shared regions
- 🔐 **TrustZone / Secure RAM**: Protected memory regions (optional)

**Interconnect & Signaling:**

- 🔌 **AXI / AHB Bridges**: Core-to-memory fabric
- 📬 **Mailbox / MU**: Hardware messaging unit for IPI (Inter-Processor Interrupts)
- 🔒 **Firewalls / Access Control**: TZASC, address filtering
- ⚔️ **GIC (ARM Generic Interrupt Controller)**: A-core interrupts + cross-CPU signaling
- 🎪 **NVIC (Cortex-M)**: M-core vectored interrupt controller


🔒 **Memory Partitioning & Access Control**
============================================

**Static Memory Layout** (Boot-time defined, most common):

Bootloader/firmware defines regions in:
- Device tree 📋
- Linker scripts 📝
- Resource tables 📑

**Example Layout** (STM32MP1 / ZynqMP style):

.. code-block:: text

   Cortex-M Code (Private SRAM/TCM)
   0x0000_0000 ┌────────────────────────────┐
   │           │  M-Core Code (256KB TCM)  │  ⚡ FAST (tightly coupled)
   │           │  Stack, ISR vectors       │  🔐 PRIVATE TO M-CORE
   0x0004_0000 └────────────────────────────┘

   [GAP - Inaccessible]

   Linux Kernel & Rootfs
   0x1000_0000 ┌────────────────────────────┐
   │           │  Linux Kernel (DDR)        │  🐧 A-CORE ONLY
   │           │  Rootfs, Apps              │
   0x6FFF_FFFF └────────────────────────────┘

   Shared IPC Region (VirtIO Rings + Data)
   0xC000_0000 ┌────────────────────────────┐
   │           │  RPMsg VirtIO Rings        │  🔗 SHARED, 4KB aligned
   │           │  Mailbox notify area       │  📬 For IPC signaling
   0xC1FF_FFFF └────────────────────────────┘

   OCM (On-Chip Memory)
   0xFFE0_0000 ┌────────────────────────────┐
   │           │  Ultra-low-latency shared  │  🔥 FASTEST shared memory
   │           │  Spinlocks, sync primitives│
   0xFFFF_FFFF └────────────────────────────┘

**Access Control Mechanisms:**

🛡️ **MPU (Memory Protection Unit)** - Cortex-M:
   - 8–16 configurable regions
   - Per-region: Read, Write, eXecute permissions
   - Privilege levels: Privileged vs. User mode
   - Example: M-core can't write to Linux DDR (fault on access)

🛡️ **MMU (Memory Management Unit)** - Cortex-A:
   - Virtual→Physical address translation
   - Per-process permissions (Linux isolation)
   - Translation Lookaside Buffer (TLB) for caching
   - Shared regions mapped non-cached (bypass cache coherency complexity)

🛡️ **System-Level Protection:**
   - 🔐 **ARM TrustZone**: Secure/Non-Secure world separation
   - 🔥 **Firewalls / TZASC**: Interconnect-level access control
   - ❌ **XN (eXecute Never)**: Prevent code execution from data regions
   - 📡 **IOMMU / SMMU**: DMA peripheral access control (→ memory)

⚠️ **Cache Coherency Gotcha:**
   - ❌ **NO automatic coherency** between A & M cores for shared regions
   - ✅ **Solution**: Explicitly clean/invalidate cache lines:
      - ARM A-side: ``DC CVAC`` (clean to PoC), ``DC IVAC`` (invalidate)
      - Or use non-cached memory mapping for vrings
      - Or ensure software synchronization


🎛️ **OpenAMP Software Stack** (IPC Framework)
=============================================

The OpenAMP ecosystem provides **Linux ↔ RTOS** communication on ARM AMP systems.

.. container:: software-stack

   | 🔧 Component      | 📖 Purpose                             | 🐧 Master (Linux)        | 🔧 Remote (RTOS/BM)   | 📡 Transport      |
   |------------------|----------------------------------------|--------------------------|------------------------|-------------------|
   | **remoteproc**   | 🚀 Load firmware, start/stop remote    | ✅ Kernel driver         | ✅ Library             | —                 |
   |                  | 📊 Parse resource table                | (sys/class/remoteproc)   |                       |                   |
   | **RPMsg**        | 💬 Message-based IPC (named channels)  | ✅ Kernel + /dev/rpmsg   | ✅ User-level API     | 📌 **VirtIO**     |
   |                  | 🎯 Endpoint-to-endpoint communication | (character device)       |                       |                   |
   | **VirtIO**       | 🔄 Ring buffers + transport abstraction| ✅ Yes (kernel)          | ✅ Yes (user/lib)     | Shared Memory     |
   |                  | ⚡ Producer-consumer queues            |                         |                       |                   |
   | **Resource Tbl** | 🗂️ Memory carve-outs + vring locations| ✅ Parsed by master      | ✅ Published by remote | Firmware ELF hdr  |
   |                  | 🎪 Platform capabilities              |                         |                       |                   |
   | **Mailbox/MU**   | 📬 Low-level signaling (notify, ack)  | ✅ Often used (IPI)      | ✅ Often used         | Hardware IP       |
   |                  | 🚨 Interrupt-driven wakeup            |                         |                       |                   |

**Communication Flow Diagram:**

.. code-block:: text

   Linux (A-core)               Shared Memory              RTOS (M-core)
   ─────────────────────────────────────────────────────────────────
   
   User App (RPMsg client)
   ↓
   /dev/rpmsgX (char device)
   ↓
   [RPMsg Kernel Module]
   │                    ┌─────────────────┐
   │                    │  📌 VirtIO Ring │
   │                    │  (4KB aligned)  │
   │                    └─────────────────┘
   │                           ↕️  (shared memory)
   │                    ┌─────────────────┐
   │                    │ VirtIO Callback │
   │──Notify via IPI───→│ RPMsg Endpoint  │
   │                    │ Handler         │
   │                    └─────────────────┘
   │                            ↑
   │←────ACK via Mailbox────────┘
   ↑
   Reply data in shared buffer

**Key Points:**

🎯 **remoteproc lifecycle**:
   1. Load firmware ELF from Linux filesystem
   2. Parse resource table (carve-outs, vring locations)
   3. Start remote core (write start address to control register)
   4. Remote core boots, initializes RPMsg subsystem
   5. Endpoints register on both sides

💬 **RPMsg communication**:
   - Named channels (e.g., "rpmsg-omx", "my_service")
   - Max payload: 496–512 bytes (typical, Linux compat)
   - Request/response or pub-sub patterns
   - Automatically blocked until endpoint ready

⚡ **Performance hints**:
   - Keep vrings in OCM (on-chip memory) for lowest latency
   - Minimize cross-interconnect DDR traffic
   - Use spinlocks in shared memory for quick sync


🚀 **Quick Setup Flow** (Linux Master + Remote RTOS)
====================================================

**Step 1️⃣ : Firmware Build** (Cortex-M side):

.. code-block:: c

   /* Cortex-M firmware with resource table */
   #include <openamp/remoteproc.h>
   #include <openamp/rpmsg_virtio.h>
   
   /* 🗂️ Resource table defines memory carve-outs */
   struct resource_table *resource_init(...) {
       // Tell master: vring locations, memory regions
       // Master will NOT overwrite these regions
   }
   
   /* 💬 RPMsg callback handler */
   int rpmsg_endpoint_cb(struct rpmsg_device *rdev, void *data, 
                        int len, void *priv, uint32_t src) {
       printf("📨 Received: %s\n", (char *)data);
       rpmsg_send(endpoint, "ACK", 3);  // Reply
       return RPMSG_SUCCESS;
   }
   
   void main() {
       rpmsg_virtio_init(shmem_base, ...);  // ⚡ Initialize
       rpmsg_create_ept(&endpoint, "my_service", ...);  // 💬 Listen
       while(1) {
           // Handle events, process IRQs
       }
   }

**Step 2️⃣ : Device Tree** (Linux config):

.. code-block:: dts

   /* device tree snippet */
   remoteproc {
       compatible = "ti,k3-dsp-remoteproc";
       
       memory-regions = <&m4_reserved>;  // Carve-out
       mboxes = <&mailbox0 0 0>;         // 📬 Mailbox
       
       firmware = "m4_firmware.elf";     // 🚀 ELF to load
   };
   
   m4_reserved: memory@81000000 {
       reg = <0x81000000 0x04000000>;    // 64 MB reserved
       no-map;                           // Don't use for Linux
   };

**Step 3️⃣ : Linux Host Start Remote Core**:

.. code-block:: bash

   # List remote processors
   $ ls /sys/class/remoteproc/
   remoteproc0  remoteproc1
   
   # Start firmware (kernel loads ELF → parses resource table → starts M-core)
   $ echo start > /sys/class/remoteproc/remoteproc0/state
   
   # Firmware boots, RPMsg endpoints appear
   $ ls /dev/rpmsg*
   /dev/rpmsg0  /dev/rpmsg1
   
   # User app talks to remote RTOS
   $ cat /dev/rpmsg0  # Listen on channel 0
   📨 Received: Hello from M-core!

**Step 4️⃣ : IPC Communication Patterns**:

.. code-block:: python

   # Linux user app (Python example)
   import struct
   
   with open('/dev/rpmsg0', 'r+b') as rpmsg:
       # Send request 📨
       rpmsg.write(b'STATUS_REQUEST')
       
       # Receive response (blocking)
       response = rpmsg.read(512)
       print(f"🎉 Remote replied: {response}")
   
   # Behind scenes:
   # 1. write() → RPMsg kernel module queues to VirtIO ring
   # 2. Kernel sends IPI (Inter-Processor Interrupt) via Mailbox
   # 3. M-core NVIC wakes up, pulls from ring, invokes callback
   # 4. M-core processes, sends reply via VirtIO
   # 5. M-core sends IPI back (notify completion)
   # 6. A-core wakes, copies data to user buffer

**Communication Patterns:**

✅ **Request-Response** (synchronous):
   - A-core sends request, waits for reply
   - M-core processes, replies
   - Typical for control commands (e.g., "SET_FREQ=1200MHz")

✅ **Pub-Sub** (asynchronous):
   - M-core publishes sensor data periodically
   - A-core subscribes, receives notifications
   - Typical for streaming (camera, IMU, audio)

✅ **Bulk Data Transfer**:
   - RPMsg payload too small (512 bytes)
   - Use shared buffer regions instead
   - RPMsg only signals (e.g., "data ready @ 0xC000_0000")
   - Remote reads/writes buffer directly (fast!)


⚠️ **Common Pitfalls & Best Practices** (MEMORIZE THESE! 🎯)
===========================================================

🔴 **Cache Coherency Trap** (Most Common Bug):

   ❌ **Problem**: A-core writes to shared buffer, M-core reads stale data
   
   ✅ **Solution 1 - Cache Invalidation**:
      - A-core: ``DC CIVAC`` (clean & invalidate) after writing
      - M-core: ``IC IALLU`` (I-cache invalidate all) before reading code
      - Cost: Slow (cache flush blocks pipeline)
   
   ✅ **Solution 2 - Non-Cached Mapping** (Preferred):
      - Map vrings as ``Device-nGnRnE`` (non-cacheable)
      - Hardware skips cache (no coherency needed)
      - Cost: Slower but predictable
   
   ✅ **Solution 3 - Software Barriers**:
      - DSB (Data Synchronization Barrier)
      - DMB (Data Memory Barrier)
      - Use only when necessary (performance killer)

🔴 **VirtIO Ring Alignment Gotcha**:

   ❌ ❌ **MUST be 4096-byte aligned**
   
   .. code-block:: c

      struct vring rx_vring;
      // ✅ CORRECT: Place in linker script
      .shared_mem (NOLOAD) : { *(.vring) } > OCM AT > FLASH
      
      // ❌ WRONG: Stack allocation
      struct vring rx_vring;  // UNALIGNED!

🔴 **Buffer Size Limits**:

   ❌ **RPMsg payload**: 496–512 bytes max (kernel compat)
   ❌ **Cannot exceed** without custom configuration
   
   ✅ **For larger data**: Use shared buffers + RPMsg notifications

🔴 **Shutdown Sequence**:

   ❌ **Wrong**: Kill Linux, M-core keeps running (zombie state)
   
   ✅ **Correct sequence**:
      1. Send shutdown message via RPMsg
      2. Wait for M-core to acknowledge + clean up
      3. M-core enters idle/WFI (Wait For Interrupt)
      4. Then stop remoteproc: ``echo stop > /sys/class/.../state``

🟡 **Performance Optimization Tips**:

   ⚡ **VirtIO Ring Location**:
      - OCM (on-chip): Sub-microsecond latency ⭐
      - DDR: ~100-200ns higher latency
   
   ⚡ **Interrupt Coalescing**:
      - Don't notify on every packet (network-style)
      - Batch notifications (e.g., every 10 packets or 100µs)
      - Reduces interrupt overhead significantly
   
   ⚡ **Spinlocks in Shared Memory**:
      - For ultra-fast synchronization (no syscall)
      - Use atomic compare-and-swap
      - Example: Custom semaphore in OCM
   
   ⚡ **DMA for Bulk Transfers**:
      - Don't memcpy large regions
      - Use DMA controller (if available) to move data
      - RPMsg only signals completion

🟡 **Multi-Core Debugging** (Tricky!):

   💡 **Setup**:
      - ARM DS (Keil): Supports multi-inferiors
      - GDB + OpenOCD: Two separate GDB sessions
      - One debugger per core (A & M)
   
   💡 **Tips**:
      - Set breakpoints on both sides
      - Use shared memory watchpoints
      - Log to shared buffer instead of printing (faster)

📋 **Quick Checklist Before Shipping**:

   ✅ VirtIO rings 4KB aligned?
   ✅ Cache invalidation on shared buffer access?
   ✅ Resource table matches firmware layout?
   ✅ Memory carve-outs don't overlap?
   ✅ Endpoint names match on both sides?
   ✅ RPMsg payload ≤ 512 bytes?
   ✅ Shutdown sequence tested?
   ✅ Load/unload remoteproc doesn't crash?
   ✅ Multi-socket machines tested (NUMA)?
   ✅ Power management (suspend/resume) tested?

🌟 **Key Takeaways** (TL;DR - Memorize This! 🧠)
=================================================

**What is AMP?**
   Multiple independent OSes on different cores (Linux on A-core + RTOS on M-core).
   NOT load-balanced like SMP—fixed assignment. Real-time + general-purpose mixed.

**Hardware Blueprint** 🏗️:
   - A-core: Linux, MMU, large shared DDR, GIC interrupt controller
   - M-core: RTOS, MPU, private TCM/SRAM, NVIC interrupt controller
   - Interconnect: AXI/AHB bridges, Mailbox for IPI signaling

**Memory: Static > Dynamic** 💾:
   - Boot-time memory partitioning (no runtime carve-outs)
   - Shared regions explicit (VirtIO rings, buffers)
   - Cache coherency = **YOUR PROBLEM** (manual clean/invalidate)

**Communication: OpenAMP Stack** 🔌:
   - remoteproc: Firmware loading + lifecycle management
   - RPMsg: Message-based IPC (up to 512 bytes)
   - VirtIO: Ring buffers for efficient producer-consumer
   - Mailbox: Hardware signaling (interrupt each other)

**Critical Pitfalls** ⚠️:
   1. **Cache coherency bugs** (A-core writes, M-core reads stale)
   2. **VirtIO ring misalignment** (must be 4KB aligned)
   3. **RPMsg size limits** (≤512 bytes, use shared buffers for bulk data)
   4. **Improper shutdown** (M-core left running = zombie)

**Typical Performance** 📊:
   - VirtIO latency: 1–10 µs (if OCM) or 100–200 ns (if DDR) ⭐
   - RPMsg throughput: ~5 Mbps per channel (software-limited)
   - IPI + cache flush: Add 5–20 µs per round-trip

**When to Use AMP?** 🎯:

   ✅ Mixed real-time + non-RT requirements
   ✅ Heterogeneous cores available (A + M/R)
   ✅ Need isolated OS failures (RT unaffected by Linux crash)
   ✅ Separate firmware update cycles

   ❌ Pure compute load-balancing (use SMP instead)
   ❌ Full coherent memory model needed (pain in AMP)
   ❌ Frequent dynamic repartitioning (static is simpler)

---

📚 **Resources & Tools**
=========================

**Documentation**:
   - 🔗 OpenAMP GitHub: https://github.com/OpenAMP/open-amp
   - 📘 Zynq UltraScale+ TRM: Xilinx (excellent AMP reference)
   - 📘 STM32MP1 Reference Manual: STMicroelectronics
   - 📘 i.MX 8M Plus RM: NXP (A53 + M7 AMP setup)
   - 📘 TI Keystone Architecture: Texas Instruments

**Tools** 🔧:
   - remoteproc + RPMsg: Kernel drivers (drivers/remoteproc, drivers/rpmsg)
   - OpenAMP Libraries: C firmware API
   - **Arm Development Studio**: Multi-core debugging
   - **OpenOCD**: JTAG debugging (free)
   - **Device Tree Compiler (DTC)**: dts → dtb

**Pro Tips** ✨:
   - Use OCM for vrings (ultra-low latency) ⚡
   - Spinlocks in shared memory for fast sync (no syscall) 🔒
   - Batch RPMsg notifications (reduce interrupts) 📦
   - DMA for bulk data (don't memcpy in CPU) 🚀
   - Test power transitions (suspend/resume tricky) 😴
   - Monitor cache line sharing (perf penalty) 📊
   - **Log to shared buffer instead of UART** (UART is slow!) 🐢

---

✅ **Production-Ready Checklist**:

Before shipping ARM AMP systems:

🔍 **Functional**:
   ✓ Firmware loads correctly
   ✓ RPMsg endpoints register on both sides
   ✓ Request-response patterns work
   ✓ Bulk data transfers via shared buffers

🔐 **Safety**:
   ✓ Memory carve-outs don't overlap
   ✓ M-core can't write to Linux kernel (MPU guards)
   ✓ Cache coherency manual (all writes followed by clean)
   ✓ Shutdown sequence prevents zombie cores

⚡ **Performance**:
   ✓ VirtIO rings in OCM (< 10 µs latency)
   ✓ IPC throughput meets requirements
   ✓ Interrupt coalescing reduces CPU load
   ✓ DMA used for large transfers

🔧 **Robustness**:
   ✓ Load/unload remoteproc multiple times (no leaks)
   ✓ NUMA machines tested (if multi-socket)
   ✓ suspend/resume cycle tested
   ✓ Multi-core debugging works (Arm DS or gdb)

---

🎓 **Quick Mental Model**:

Think of ARM AMP like a **distributed embedded system inside one chip**:

   • A-core = General-purpose server (Linux, flexible, slower OK)
   • M-core = Dedicated worker (RTOS, real-time, predictable latency)
   • Shared memory = Network (explicit message passing, no auto-sync)
   • Mailbox/IPI = Ethernet packets (notify the other side)
   • VirtIO rings = TCP/IP (structured, efficient bulk transfer)

✅ **Happy multi-core programming!** 🚀

---

*Last updated: 2026-01-12 | Production ready for Zynq, STM32MP1, i.MX8/9, TI Keystone*
