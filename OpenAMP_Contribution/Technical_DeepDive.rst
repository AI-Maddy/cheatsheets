🔬 OpenAMP Technical Deep Dive
===============================

.. contents:: 📑 Navigation
   :depth: 3
   :local:

This guide covers advanced technical details for serious contributors.

🏗️ Architecture Deep Dive
===========================

1. Memory Layout & Shared Memory
---------------------------------

Typical AMP System Memory Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Physical Memory Layout:
   
   0x00000000  ┌─────────────────────────────────┐
               │  Host (Linux) Code & Data       │
               │  - Kernel                       │
               │  - User space                   │
   0x40000000  ├─────────────────────────────────┤
               │  Remote Code (Firmware)         │
               │  - .text, .data, .bss           │
   0x50000000  ├─────────────────────────────────┤
               │  Shared Memory Region           │
               │  ┌───────────────────────────┐  │
               │  │ Resource Table            │  │
   0x50000100  │  ├───────────────────────────┤  │
               │  │ Vring 0 (Host→Remote)     │  │
               │  │  - Descriptor table       │  │
               │  │  - Available ring         │  │
               │  │  - Used ring              │  │
   0x50004000  │  ├───────────────────────────┤  │
               │  │ Vring 1 (Remote→Host)     │  │
   0x50008000  │  ├───────────────────────────┤  │
               │  │ Buffer Pool               │  │
               │  │  - Fixed-size buffers     │  │
               │  │  - Typically 512 bytes    │  │
   0x50100000  │  └───────────────────────────┘  │
               └─────────────────────────────────┘

Shared Memory Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-----------------------+------------------+--------------------------------+
| Region                | Size             | Alignment                      |
+=======================+==================+================================+
| Resource Table        | ~256 bytes       | 4-byte aligned                 |
+-----------------------+------------------+--------------------------------+
| Vring (each)          | ~16KB typical    | **Page aligned** (4KB/16KB)    |
+-----------------------+------------------+--------------------------------+
| Buffer Pool           | Configurable     | Cache-line aligned (64 bytes)  |
+-----------------------+------------------+--------------------------------+

**Why Alignment Matters:**

.. code-block:: c

   // BAD: Unaligned vring (crashes on some platforms)
   uint8_t vring_mem[16384];  // May not be page-aligned!
   
   // GOOD: Properly aligned vring
   __attribute__((aligned(4096)))
   uint8_t vring_mem[16384];
   
   // Better: Use linker script
   // In linker script:
   .shared_mem (NOLOAD) : ALIGN(4K) {
       *(.vring)
       *(.buffers)
   } > SRAM_SHARED

2. VirtIO & Virtqueue Internals
--------------------------------

Virtqueue Structure
~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Simplified virtqueue structure
   struct virtqueue {
       uint16_t num_descs;           // Number of descriptors
       
       struct vring_desc *desc;      // Descriptor table
       struct vring_avail *avail;    // Available ring
       struct vring_used *used;      // Used ring
       
       void **desc_buf;              // Buffer pointers
       uint16_t last_avail_idx;      // Consumer index
       uint16_t last_used_idx;       // Producer index
   };
   
   // Descriptor entry
   struct vring_desc {
       uint64_t addr;     // Buffer physical address
       uint32_t len;      // Buffer length
       uint16_t flags;    // Descriptor flags
       uint16_t next;     // Next descriptor (if chained)
   };
   
   // Available ring (written by driver)
   struct vring_avail {
       uint16_t flags;
       uint16_t idx;      // Next descriptor to add
       uint16_t ring[];   // Descriptor indices
   };
   
   // Used ring (written by device)
   struct vring_used {
       uint16_t flags;
       uint16_t idx;      // Next descriptor consumed
       struct vring_used_elem ring[];
   };

Message Flow Through Virtqueue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Sender (Host) side:
   
   1. Get free descriptor from pool
      ┌──────────────────────┐
      │  desc_pool[0..255]   │
      │  ┌────┐              │
      │  │ 42 │ ◄── allocate │
      │  └────┘              │
      └──────────────────────┘
   
   2. Fill buffer with message
      ┌─────────────────┐
      │ Buffer #42      │
      │ ┌─────────────┐ │
      │ │"Hello RPMsg"│ │
      │ └─────────────┘ │
      └─────────────────┘
   
   3. Add descriptor to available ring
      avail_ring:
      ┌─────┬─────┬─────┬─────┐
      │ ... │ 42  │     │     │
      └─────┴─────┴─────┴─────┘
              ↑
           idx = N
   
   4. Increment avail->idx (atomic!)
      avail->idx++  (N → N+1)
   
   5. Send interrupt to remote
      kick_remote()
   
   
   Receiver (Remote) side:
   
   1. Interrupt handler wakes up
      IRQ → virtqueue_service()
   
   2. Check for new buffers
      while (last_used_idx != avail->idx) {
   
   3. Get descriptor from available ring
      desc_idx = avail_ring[last_used_idx]
   
   4. Process message
      memcpy(local_buf, desc[desc_idx].addr, len)
      rpmsg_callback(endpoint, local_buf, len)
   
   5. Return descriptor to used ring
      used_ring[used_idx] = desc_idx
      used->idx++
   
   6. Send interrupt back (if needed)
      kick_host()

Cache Coherency Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Problem: CPU cache may have stale data
   
   // Sender side:
   memcpy(buffer, data, len);          // Write to buffer
   // ⚠️ Data might still be in cache, not in RAM!
   
   metal_cache_flush(buffer, len);     // ✅ Flush cache to RAM
   virtqueue_add_buffer(...);
   kick_remote();
   
   // Receiver side:
   metal_cache_invalidate(buffer, len); // ✅ Invalidate cache
   memcpy(local_data, buffer, len);     // Now read fresh data

3. RPMsg Protocol Details
--------------------------

RPMsg Packet Format
~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Wire format (sent over virtqueue)
   struct rpmsg_hdr {
       uint32_t src;       // Source endpoint address
       uint32_t dst;       // Destination endpoint address
       uint32_t reserved;  // Reserved (must be 0)
       uint16_t len;       // Payload length
       uint16_t flags;     // Flags (none currently defined)
       uint8_t  data[];    // Variable-length payload
   } __attribute__((packed));
   
   // Total packet size = sizeof(hdr) + len
   // Max payload: RPMSG_BUFFER_SIZE - sizeof(struct rpmsg_hdr)
   //            = 512 - 16 = 496 bytes (typical)

Endpoint Addressing
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Endpoint Address Space:
   
   0x00000000 - 0x000003FF : Reserved
   0x00000400 - 0xFFFFFFFF : Dynamic allocation
   
   Special addresses:
   - RPMSG_NS_ADDR (0x35) : Name service endpoint
   - RPMSG_ADDR_ANY (-1)  : Auto-allocate address

Name Service Protocol
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Name service announcement message
   struct rpmsg_ns_msg {
       char name[32];      // Service name (e.g., "rpmsg-client")
       uint32_t addr;      // Endpoint address
       uint32_t flags;     // CREATE or DESTROY
   } __attribute__((packed));
   
   #define RPMSG_NS_CREATE  0
   #define RPMSG_NS_DESTROY 1
   
   // Flow:
   // 1. Remote creates endpoint
   rpmsg_create_ept(&ept, "my-service", 0x400, ...)
   
   // 2. Send NS announcement to host
   ns_msg.name = "my-service"
   ns_msg.addr = 0x400
   ns_msg.flags = RPMSG_NS_CREATE
   rpmsg_send(ns_ept, &ns_msg, sizeof(ns_msg))
   
   // 3. Host receives NS message, creates matching endpoint
   // 4. Communication channel established!

4. RemoteProc Life Cycle
-------------------------

Firmware Loading States
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   State Machine:
   
   OFFLINE ──load()──► LOADED ──start()──► RUNNING
      ▲                                         │
      │                                         │
      └─────────────────stop()─────────────────┘
   
   Detailed flow:
   
   1. OFFLINE (initial state)
      - Remote core powered off or in reset
   
   2. Load firmware:
      - Parse ELF/binary
      - Copy .text, .data to remote memory
      - Parse resource table
      - Allocate vrings
   
   3. LOADED
      - Firmware in memory
      - Resources allocated
      - Ready to start
   
   4. Start:
      - Initialize vrings
      - Setup interrupts
      - Release remote from reset
   
   5. RUNNING
      - Remote executing
      - RPMsg active
      - Can send/receive messages
   
   6. Stop:
      - Send shutdown signal
      - Wait for ACK
      - Put remote in reset
      - Free resources

Resource Table Parsing
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Parse and process resource table
   int process_resource_table(struct fw_rsc_table *table) {
       for (int i = 0; i < table->num; i++) {
           struct fw_rsc_hdr *rsc = 
               (void *)table + table->offset[i];
           
           switch (rsc->type) {
           case RSC_CARVEOUT:
               // Allocate memory region
               struct fw_rsc_carveout *co = (void *)rsc;
               allocate_memory(co->da, co->pa, co->len);
               break;
           
           case RSC_DEVMEM:
               // Map device memory
               struct fw_rsc_devmem *dm = (void *)rsc;
               map_device_memory(dm->da, dm->pa, dm->len);
               break;
           
           case RSC_VDEV:
               // Setup VirtIO device
               struct fw_rsc_vdev *vd = (void *)rsc;
               setup_virtio_device(vd);
               
               // For each vring:
               for (int j = 0; j < vd->num_of_vrings; j++) {
                   struct fw_rsc_vdev_vring *vring = &vd->vring[j];
                   allocate_vring(vring->da, vring->align,
                                vring->num);
               }
               break;
           
           case RSC_TRACE:
               // Setup trace buffer
               struct fw_rsc_trace *tr = (void *)rsc;
               setup_trace_buffer(tr->da, tr->len);
               break;
           }
       }
   }

🔧 Advanced Porting Guide
==========================

Complete Platform Port Checklist
---------------------------------

**Phase 1: libmetal Port**

.. code-block:: text

   lib/system/<your_platform>/
   ├── sys.h               ☐ Platform definitions
   ├── sys.c               ☐ Init/finish functions
   ├── io.c                ☐ Memory-mapped I/O
   ├── irq.c               ☐ Interrupt handling
   ├── cpu.h               ☐ CPU-specific (cache, barriers)
   └── CMakeLists.txt      ☐ Build configuration

**Phase 2: Platform-Specific Code**

.. code-block:: c

   // 1. Implement memory I/O mapping
   int metal_sys_io_mem_map(struct metal_io_region *io) {
       // Map physical address to virtual
       io->virt = mmap(io->physmap, io->size, ...);
       return 0;
   }
   
   // 2. Implement mutex operations
   void __metal_mutex_init(metal_mutex_t *m) {
       // Your RTOS mutex init
       xSemaphoreCreateMutex(m);
   }
   
   // 3. Implement interrupt handling
   int metal_irq_register(int irq, metal_irq_handler handler,
                         void *arg) {
       // Register interrupt handler
       NVIC_SetVector(irq, (uint32_t)handler);
       NVIC_EnableIRQ(irq);
       return 0;
   }
   
   // 4. Implement cache operations
   void metal_cache_flush(void *addr, size_t len) {
       SCB_CleanDCache_by_Addr(addr, len);
   }
   
   void metal_cache_invalidate(void *addr, size_t len) {
       SCB_InvalidateDCache_by_Addr(addr, len);
   }

**Phase 3: Resource Table**

.. code-block:: c

   // Define resource table for your platform
   #define VRING0_DA    0x20040000  // Your shared mem base
   #define VRING1_DA    0x20044000
   #define VRING_SIZE   256
   #define VRING_ALIGN  4096
   
   struct my_platform_resource_table {
       struct resource_table table_hdr;
       uint32_t offset[2];  // vdev + carveout
       
       struct fw_rsc_vdev vdev;
       struct fw_rsc_vdev_vring vring[2];
       
       struct fw_rsc_carveout carveout;
   } __attribute__((section(".resource_table")));
   
   struct my_platform_resource_table resources = {
       .table_hdr = {
           .ver = 1,
           .num = 2,
       },
       .offset = {
           offsetof(struct my_platform_resource_table, vdev),
           offsetof(struct my_platform_resource_table, carveout),
       },
       .vdev = {
           .type = RSC_VDEV,
           .id = VIRTIO_ID_RPMSG,
           .notifyid = 0,
           .dfeatures = 1 << VIRTIO_RPMSG_F_NS,
           .config_len = 0,
           .num_of_vrings = 2,
       },
       .vring[0] = {
           .da = VRING0_DA,
           .align = VRING_ALIGN,
           .num = VRING_SIZE,
           .notifyid = 0,
       },
       .vring[1] = {
           .da = VRING1_DA,
           .align = VRING_ALIGN,
           .num = VRING_SIZE,
           .notifyid = 1,
       },
       .carveout = {
           .type = RSC_CARVEOUT,
           .da = 0x20040000,
           .pa = 0x20040000,
           .len = 0x80000,  // 512KB shared memory
           .name = "vdev0buffer",
       },
   };

**Phase 4: Linker Script**

.. code-block:: text

   /* Place resource table at known address */
   SECTIONS {
       .resource_table (NOLOAD) : {
           KEEP(*(.resource_table))
       } > SRAM AT> FLASH
       
       .vring0 (NOLOAD) : ALIGN(4K) {
           *(.vring0)
       } > SHARED_SRAM
       
       .vring1 (NOLOAD) : ALIGN(4K) {
           *(.vring1)
       } > SHARED_SRAM
   }

🐛 Debugging Techniques
=======================

Common Issues & Solutions
-------------------------

**Issue 1: "No buffer available" (-ENOMEM)**

.. code-block:: c

   // Debug: Check vring state
   void dump_vring_state(struct virtqueue *vq) {
       printf("Vring stats:\n");
       printf("  num_descs: %u\n", vq->vq_nentries);
       printf("  avail idx: %u\n", vq->vq_ring.avail->idx);
       printf("  used idx:  %u\n", vq->vq_ring.used->idx);
       printf("  free descs: %u\n",
              vq->vq_nentries - (vq->vq_ring.avail->idx -
                                 vq->vq_ring.used->idx));
   }
   
   // Common causes:
   // 1. Remote not returning buffers → Check interrupt delivery
   // 2. Vring too small → Increase VRING_SIZE
   // 3. Buffer leak → Check all code paths free buffers

**Issue 2: Messages corrupted**

.. code-block:: c

   // Enable cache debugging
   #define DEBUG_CACHE 1
   
   #ifdef DEBUG_CACHE
   static void verify_cache_coherency(void *addr, size_t len) {
       // Flush cache
       metal_cache_flush(addr, len);
       
       // Read back from RAM (bypassing cache)
       volatile uint8_t *p = (volatile uint8_t *)addr;
       uint8_t checksum = 0;
       for (size_t i = 0; i < len; i++) {
           checksum ^= p[i];
       }
       
       printf("Cache checksum: 0x%02x\n", checksum);
   }
   #endif
   
   // Use before sending
   memcpy(buffer, msg, len);
   verify_cache_coherency(buffer, len);
   rpmsg_send(...);

**Issue 3: Remote not booting**

.. code-block:: bash

   # Debug firmware loading
   
   # 1. Verify resource table location
   arm-none-eabi-objdump -t firmware.elf | grep resource_table
   # Should show address matching linker script
   
   # 2. Check memory regions
   arm-none-eabi-size firmware.elf
   # Verify .text, .data fit in remote memory
   
   # 3. Dump resource table
   arm-none-eabi-objdump -s -j .resource_table firmware.elf
   # Verify structure is correct

Performance Optimization
------------------------

**1. Reduce Cache Flushes**

.. code-block:: c

   // BAD: Flush for each message
   for (int i = 0; i < 1000; i++) {
       memcpy(buf[i], data[i], len);
       metal_cache_flush(buf[i], len);  // ❌ Slow!
   }
   
   // GOOD: Batch flushes
   for (int i = 0; i < 1000; i++) {
       memcpy(buf[i], data[i], len);
   }
   metal_cache_flush(buf, 1000 * len);  // ✅ Fast!

**2. Zero-Copy for Large Data**

.. code-block:: c

   // Share pointer instead of copying
   struct large_data *shared_data = allocate_shared();
   populate_data(shared_data);
   
   // Send only pointer (not data)
   struct msg {
       uint64_t data_ptr;
       uint32_t data_len;
   };
   rpmsg_send(&ept, &msg, sizeof(msg));

**3. Increase Vring Size**

.. code-block:: c

   // Default: 256 buffers
   #define VRING_SIZE 256
   
   // High throughput: 1024 buffers
   #define VRING_SIZE 1024
   
   // Memory cost: ~16KB per vring
   // Worth it for >100 msg/sec workloads

📊 Performance Benchmarking
============================

Measuring Latency
-----------------

.. code-block:: c

   uint64_t get_time_ns(void) {
       struct timespec ts;
       clock_gettime(CLOCK_MONOTONIC, &ts);
       return ts.tv_sec * 1000000000ULL + ts.tv_nsec;
   }
   
   void benchmark_rpmsg_latency(void) {
       char msg[] = "ping";
       uint64_t start, end;
       uint64_t latencies[1000];
       
       for (int i = 0; i < 1000; i++) {
           start = get_time_ns();
           rpmsg_send(&ept, msg, sizeof(msg));
           wait_for_reply();
           end = get_time_ns();
           
           latencies[i] = end - start;
       }
       
       // Calculate statistics
       qsort(latencies, 1000, sizeof(uint64_t), compare);
       printf("Min:    %llu ns\n", latencies[0]);
       printf("Median: %llu ns\n", latencies[500]);
       printf("P95:    %llu ns\n", latencies[950]);
       printf("Max:    %llu ns\n", latencies[999]);
   }

Measuring Throughput
---------------------

.. code-block:: c

   void benchmark_rpmsg_throughput(void) {
       char msg[496];  // Max RPMsg payload
       uint64_t start, end;
       int count = 10000;
       
       start = get_time_ns();
       for (int i = 0; i < count; i++) {
           rpmsg_send(&ept, msg, sizeof(msg));
       }
       end = get_time_ns();
       
       uint64_t duration_ns = end - start;
       double duration_s = duration_ns / 1e9;
       double msgs_per_sec = count / duration_s;
       double mbps = (count * sizeof(msg) * 8) / duration_s / 1e6;
       
       printf("Throughput: %.2f msgs/sec\n", msgs_per_sec);
       printf("Bandwidth:  %.2f Mbps\n", mbps);
   }

===============================================
🎓 Additional Resources
===============================================

Official Documentation
----------------------

* OpenAMP Spec: https://www.openampproject.org/docs/
* Linux RemoteProc: https://www.kernel.org/doc/html/latest/staging/remoteproc.html
* VirtIO Spec: https://docs.oasis-open.org/virtio/virtio/v1.1/virtio-v1.1.html

Academic Papers
---------------

* "OpenAMP: An Open Source Solution for Heterogeneous Multiprocessing"
* "RPMsg: A Virtio-Based Messaging Bus for Remote Processors"

Example Platforms
-----------------

* STM32MP1: https://wiki.st.com/stm32mpu/wiki/OpenAMP
* i.MX: https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/nxp
* Zynq: https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841831/OpenAMP

===============================================
Last Updated: January 2026
===============================================
