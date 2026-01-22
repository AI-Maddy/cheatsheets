🚀 OpenAMP Quick Reference & Contribution Guide
===============================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

🎯 TL;DR - What is OpenAMP?
===========================

**OpenAMP** = **Open Asymmetric Multi-Processing Framework**

+-------------------+----------------------------------------------------------------+
| **What**          | Framework for heterogeneous multi-core communication           |
+-------------------+----------------------------------------------------------------+
| **Why**           | Standardize IPC between different OS/cores in embedded systems|
+-------------------+----------------------------------------------------------------+
| **Where**         | Automotive, Industrial IoT, Aerospace, Medical devices         |
+-------------------+----------------------------------------------------------------+
| **License**       | BSD-3-Clause (permissive, commercial-friendly)                 |
+-------------------+----------------------------------------------------------------+
| **Language**      | C (portable, RTOS/bare-metal/Linux)                            |
+-------------------+----------------------------------------------------------------+

**Key Use Case:** Linux (Cortex-A) controlling/communicating with RTOS (Cortex-R/M)

📚 Core Concepts (5-Minute Overview)
=====================================

1. AMP vs SMP
-------------

+---------------------+----------------------------------+----------------------------------+
| Feature             | **SMP** (Symmetric)              | **AMP** (Asymmetric)             |
+=====================+==================================+==================================+
| Cores               | Identical (homogeneous)          | Different (heterogeneous)        |
+---------------------+----------------------------------+----------------------------------+
| OS                  | Single OS across all cores       | Multiple OS per core             |
+---------------------+----------------------------------+----------------------------------+
| Tasks               | Load balancing, shared tasks     | Independent tasks per core       |
+---------------------+----------------------------------+----------------------------------+
| Example             | Desktop CPU, Server              | **Automotive ECU, IoT devices**  |
+---------------------+----------------------------------+----------------------------------+

**Why AMP in Embedded?**

* Real-time core (Cortex-R) for safety-critical tasks (braking, airbag)
* Application core (Cortex-A) for infotainment, connectivity
* Low-power core (Cortex-M) for always-on sensors

2. OpenAMP Architecture
------------------------

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │              Linux Host (Cortex-A)                      │
   │  ┌──────────────┐         ┌──────────────┐             │
   │  │  User Space  │         │ Kernel Space │             │
   │  │              │  ioctl  │              │             │
   │  │ Application  │◄───────►│ RPMsg Driver │             │
   │  └──────────────┘         └──────┬───────┘             │
   │                                  │                      │
   │         ┌────────────────────────┴─────────┐            │
   │         │   RemoteProc (Life Cycle Mgmt)   │            │
   │         │   - Load firmware                │            │
   │         │   - Start/Stop remote cores      │            │
   │         └────────────────┬─────────────────┘            │
   └──────────────────────────┼──────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Shared Memory    │
                    │  ┌─────────────┐  │
                    │  │   VirtIO    │  │ ◄─── Transport Layer
                    │  │  (Virtqueues)  │
                    │  └─────────────┘  │
                    └─────────┬─────────┘
                              │
   ┌──────────────────────────┼──────────────────────────────┐
   │                          │                              │
   │         ┌────────────────┴─────────────────┐            │
   │         │   OpenAMP Library (open-amp)     │            │
   │         │   - RPMsg API                    │            │
   │         │   - VirtIO handling              │            │
   │         └────────────────┬─────────────────┘            │
   │                          │                              │
   │         ┌────────────────▼─────────────────┐            │
   │         │   libmetal (abstraction layer)   │            │
   │         │   - Memory I/O                   │            │
   │         │   - Mutex/locks                  │            │
   │         │   - Platform abstraction         │            │
   │         └──────────────────────────────────┘            │
   │              RTOS or Bare Metal (Cortex-R/M)            │
   └─────────────────────────────────────────────────────────┘

🧩 Key Components
=================

1. RemoteProc (Life Cycle Management)
--------------------------------------

**Purpose:** Load, start, stop remote firmware

**Capabilities:**

* Firmware loading into remote core memory
* Resource table parsing (memory regions, interrupts)
* Remote core boot/shutdown
* Crash detection and recovery

**Example Flow:**

.. code-block:: c

   // Main controller (Linux/RTOS)
   struct remoteproc *rproc;
   
   // 1. Create remoteproc instance
   rproc = remoteproc_init(...);
   
   // 2. Load firmware image
   remoteproc_load(rproc, firmware_addr, firmware_size, ...);
   
   // 3. Start remote processor
   remoteproc_start(rproc);
   
   // 4. Communicate via RPMsg...
   
   // 5. Shutdown when done
   remoteproc_shutdown(rproc);

2. RPMsg (Inter-Processor Communication)
-----------------------------------------

**Purpose:** Message passing between cores

**Features:**

* Point-to-point communication channels
* Named endpoints (like sockets)
* Variable-length messages (up to 512 bytes typical)
* Zero-copy for large messages

**Message Format:**

.. code-block:: c

   struct rpmsg_hdr {
       uint32_t src;      // Source endpoint address
       uint32_t dst;      // Destination endpoint address
       uint32_t reserved;
       uint16_t len;      // Message length
       uint16_t flags;
       uint8_t  data[];   // Message payload
   };

**API Usage:**

.. code-block:: c

   // Initialize endpoint
   struct rpmsg_endpoint ept;
   rpmsg_create_ept(&ept, rdev, "rpmsg-channel",
                    RPMSG_ADDR_ANY, RPMSG_ADDR_ANY,
                    msg_callback, NULL);
   
   // Send message
   char msg[] = "Hello from remote!";
   rpmsg_send(&ept, msg, strlen(msg));
   
   // Callback receives messages
   static int msg_callback(struct rpmsg_endpoint *ept,
                          void *data, size_t len, ...) {
       printf("Received: %s\n", (char *)data);
       return 0;
   }

3. VirtIO (Transport Abstraction)
----------------------------------

**Purpose:** Hardware abstraction for communication

**Components:**

* **Virtqueues:** Ring buffers for message passing
* **Vrings:** Virtual ring buffer implementation
* **Shared Memory:** Common memory region for both cores

**Vring Structure:**

.. code-block:: text

   Shared Memory Layout:
   
   ┌──────────────────────────────────┐
   │   Available Ring (Host→Remote)   │  ◄─── Descriptors of buffers
   ├──────────────────────────────────┤
   │   Used Ring (Remote→Host)        │  ◄─── Consumed buffer notifications
   ├──────────────────────────────────┤
   │   Descriptor Table               │  ◄─── Buffer descriptors
   ├──────────────────────────────────┤
   │   Buffer Pool                    │  ◄─── Actual message buffers
   └──────────────────────────────────┘

4. libmetal (Platform Abstraction)
-----------------------------------

**Purpose:** Portability across OS/platforms

**Abstractions:**

+------------------+------------------------------------------------+
| Function         | Purpose                                        |
+==================+================================================+
| metal_alloc      | Memory allocation                              |
+------------------+------------------------------------------------+
| metal_mutex      | Mutual exclusion locks                         |
+------------------+------------------------------------------------+
| metal_io_*       | Memory-mapped I/O                              |
+------------------+------------------------------------------------+
| metal_sleep_usec | Microsecond delays                             |
+------------------+------------------------------------------------+
| metal_irq_*      | Interrupt handling                             |
+------------------+------------------------------------------------+

**Porting Checklist:**

.. code-block:: c

   // System-specific implementations needed:
   void *__metal_allocate_memory(size_t size);
   void __metal_free_memory(void *ptr);
   
   void __metal_mutex_init(metal_mutex_t *mutex);
   void __metal_mutex_acquire(metal_mutex_t *mutex);
   void __metal_mutex_release(metal_mutex_t *mutex);
   
   void __metal_sleep_usec(unsigned int usec);
   
   int metal_sys_init(const struct metal_init_params *params);
   void metal_sys_finish(void);

📋 Resource Table (Critical Concept)
=====================================

**What:** Firmware metadata telling host about resources needed

**Location:** Embedded in firmware binary (usually `.resource_table` section)

**Structure:**

.. code-block:: c

   struct resource_table {
       uint32_t ver;              // Version (always 1)
       uint32_t num;              // Number of entries
       uint32_t reserved[2];
       uint32_t offset[];         // Offsets to resource entries
   };
   
   // Common resource types:
   #define RSC_CARVEOUT   0  // Memory region
   #define RSC_DEVMEM     1  // Device memory
   #define RSC_TRACE      2  // Trace buffer
   #define RSC_VDEV       3  // VirtIO device

**Example Resource Table:**

.. code-block:: c

   #define RPMSG_VRING0_DA  0x90000000
   #define RPMSG_VRING1_DA  0x90004000
   #define VRING_SIZE       0x4000
   
   struct resource_table resources = {
       .ver = 1,
       .num = 2,
       .offset = {
           offsetof(struct resource_table, vdev),
           offsetof(struct resource_table, carveout),
       },
       
       // VirtIO device for RPMsg
       .vdev = {
           .type = RSC_VDEV,
           .id = VIRTIO_ID_RPMSG,
           .num_of_vrings = 2,
           .vring[0] = { RPMSG_VRING0_DA, 4096, 256 },
           .vring[1] = { RPMSG_VRING1_DA, 4096, 256 },
       },
       
       // Shared memory carveout
       .carveout = {
           .type = RSC_CARVEOUT,
           .da = 0x90000000,
           .pa = 0x90000000,
           .len = 0x100000,  // 1MB
       },
   };

🛠️ Getting Started - Development Setup
========================================

1. Clone Repositories
----------------------

.. code-block:: bash

   # Main repositories
   git clone https://github.com/OpenAMP/open-amp.git
   git clone https://github.com/OpenAMP/libmetal.git
   
   # Documentation
   git clone --recurse https://github.com/OpenAMP/openamp-docs.git
   
   # System reference (demos)
   git clone https://github.com/OpenAMP/openamp-system-reference.git

2. Build libmetal
-----------------

.. code-block:: bash

   cd libmetal
   mkdir build && cd build
   
   # For Linux
   cmake .. -DCMAKE_BUILD_TYPE=Debug
   
   # For bare metal/RTOS (example: Cortex-M)
   cmake .. \
     -DCMAKE_TOOLCHAIN_FILE=../cmake/platforms/arm-none-eabi-gcc.cmake \
     -DWITH_DEFAULT_LOGGER=OFF \
     -DWITH_TESTS=OFF
   
   make
   sudo make install

3. Build OpenAMP
----------------

.. code-block:: bash

   cd open-amp
   mkdir build && cd build
   
   cmake .. \
     -DCMAKE_BUILD_TYPE=Debug \
     -DWITH_PROXY=ON \
     -DWITH_APPS=ON
   
   make
   sudo make install

4. Run Examples
---------------

.. code-block:: bash

   # Echo test (simplest example)
   cd open-amp/apps/examples/echo
   
   # Matrix multiply demo
   cd open-amp/apps/examples/matrix_multiply

🎓 Learning Path (Recommended Order)
=====================================

+------+------------------------+----------------------------------+----------------+
| Step | Topic                  | Resources                        | Time           |
+======+========================+==================================+================+
| 1    | AMP Fundamentals       | Read openamp/overview.rst        | 30 min         |
+------+------------------------+----------------------------------+----------------+
| 2    | RPMsg Protocol         | protocol_details/rpmsg.rst       | 1 hour         |
+------+------------------------+----------------------------------+----------------+
| 3    | libmetal Basics        | libmetal/README.md               | 1 hour         |
+------+------------------------+----------------------------------+----------------+
| 4    | Resource Table         | protocol_details/resource_tbl    | 1 hour         |
+------+------------------------+----------------------------------+----------------+
| 5    | Echo Demo              | demos/echo.rst                   | 2 hours        |
+------+------------------------+----------------------------------+----------------+
| 6    | Porting Guide          | docs/porting_guide.rst           | 3 hours        |
+------+------------------------+----------------------------------+----------------+
| 7    | Advanced Topics        | RemoteProc design                | 4 hours        |
+------+------------------------+----------------------------------+----------------+

💡 Good First Contributions (Beginner-Friendly)
================================================

1. Documentation Improvements (⭐ EASIEST)
-------------------------------------------

**Why Good for Beginners:**

* No code changes needed
* Learn codebase by documenting
* Community always needs docs

**Ideas:**

+------------------+-------------------------------------------------------+
| Task             | Description                                           |
+==================+=======================================================+
| Fix typos        | Search docs for spelling/grammar errors              |
+------------------+-------------------------------------------------------+
| Add examples     | Document how you set up your first demo              |
+------------------+-------------------------------------------------------+
| Clarify README   | Add "troubleshooting" or "FAQ" sections              |
+------------------+-------------------------------------------------------+
| Improve diagrams | Create SVG diagrams for complex concepts             |
+------------------+-------------------------------------------------------+
| API docs         | Add missing function descriptions in Doxygen         |
+------------------+-------------------------------------------------------+

**How to Start:**

.. code-block:: bash

   # 1. Fork openamp-docs on GitHub
   # 2. Clone your fork
   git clone https://github.com/YOUR_USERNAME/openamp-docs.git
   cd openamp-docs
   
   # 3. Create branch
   git checkout -b fix-typo-in-overview
   
   # 4. Edit RST files
   vim openamp/overview.rst
   
   # 5. Build locally to test
   make html
   xdg-open _build/html/index.html
   
   # 6. Commit and push
   git add openamp/overview.rst
   git commit -m "docs: fix typo in OpenAMP overview"
   git push origin fix-typo-in-overview
   
   # 7. Create Pull Request on GitHub

2. Add Platform Support (⭐⭐ MEDIUM)
-------------------------------------

**Good Platforms to Port:**

+-------------------+---------------------------+----------------------------+
| Platform          | Difficulty                | Why Useful                 |
+===================+===========================+============================+
| STM32MP1 (ST)     | ⭐⭐ (already has examples)| Very popular               |
+-------------------+---------------------------+----------------------------+
| i.MX8 (NXP)       | ⭐⭐ (reference available) | Industrial/automotive      |
+-------------------+---------------------------+----------------------------+
| Zynq UltraScale+  | ⭐⭐⭐ (complex)           | High-performance FPGA+ARM  |
+-------------------+---------------------------+----------------------------+
| RaspberryPi Pico2 | ⭐⭐⭐⭐ (new, challenging) | Low-cost, RP2350 dual-core |
+-------------------+---------------------------+----------------------------+

**Steps:**

1. Implement libmetal port (see porting guide)
2. Create resource table for your platform
3. Write demo application (echo test)
4. Document setup in openamp-system-reference

3. Fix Existing Issues (⭐⭐⭐)
-----------------------------

**Where to Find Issues:**

* https://github.com/OpenAMP/open-amp/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
* https://github.com/OpenAMP/libmetal/issues
* https://github.com/OpenAMP/openamp-docs/issues

**Good Labels to Search:**

* ``good first issue``
* ``documentation``
* ``help wanted``
* ``bug`` (small, well-defined bugs)

**Example Good First Issues:**

.. code-block:: text

   ✅ Add CMake option to disable logging
      - Simple CMakeLists.txt change
      - Test build with/without logging
   
   ✅ Fix compiler warnings on newer GCC
      - Clean code quality improvement
      - Easy to verify
   
   ✅ Add unit test for rpmsg_send()
      - Learn testing framework
      - Improve code coverage

4. Improve Examples/Demos (⭐⭐)
--------------------------------

**Ideas:**

* Add error handling to echo demo
* Create "hello world" with comments
* Port example to new RTOS (Zephyr, FreeRTOS)
* Add performance benchmarking

**Example: Enhanced Echo Demo**

.. code-block:: c

   // Current echo demo is minimal
   // You could add:
   
   #include <openamp/rpmsg.h>
   
   // 1. Better error messages
   if (ret < 0) {
       printf("ERROR: Failed to send message (code: %d)\n", ret);
       printf("Possible causes:\n");
       printf("  - Buffer full (try again)\n");
       printf("  - Endpoint not ready\n");
       return ret;
   }
   
   // 2. Statistics tracking
   static struct {
       uint32_t msgs_sent;
       uint32_t msgs_received;
       uint32_t errors;
       uint64_t total_bytes;
   } stats;
   
   // 3. Performance measurement
   uint64_t start_time = get_time_us();
   ret = rpmsg_send(&ept, data, len);
   uint64_t latency = get_time_us() - start_time;
   printf("Message sent in %llu µs\n", latency);

🐛 How to Find & Report Bugs
==============================

1. Testing Workflow
-------------------

.. code-block:: bash

   # Build with warnings enabled
   cmake .. -DCMAKE_C_FLAGS="-Wall -Wextra -Werror"
   make
   
   # Run static analysis
   cppcheck --enable=all lib/
   
   # Run unit tests (if available)
   make test
   
   # Test on real hardware
   # - Flash firmware to remote core
   # - Run host application
   # - Check for memory leaks, race conditions

2. Good Bug Report Template
----------------------------

.. code-block:: markdown

   **Environment:**
   - OpenAMP version: v2023.10
   - libmetal version: v2023.04
   - Platform: STM32MP157C
   - Host OS: Linux 5.15
   - Remote: FreeRTOS 10.4.6
   
   **Expected Behavior:**
   RPMsg should send messages reliably
   
   **Actual Behavior:**
   Messages are dropped after 100 sends
   
   **Steps to Reproduce:**
   1. Build echo demo
   2. Send 150 messages in loop
   3. Observe message 101+ fail
   
   **Logs:**
   ```
   [ERROR] rpmsg_send: no buffer available
   ```
   
   **Additional Context:**
   - Only happens with messages > 256 bytes
   - Works fine with smaller messages

📊 Contribution Statistics & Tips
==================================

**OpenAMP GitHub Stats (as of 2026):**

+-------------------+----------+-------------+-------------------+
| Metric            | Value    | Difficulty  | Good for Beginners|
+===================+==========+=============+===================+
| Open Issues       | ~50      | Varies      | Look for labels   |
+-------------------+----------+-------------+-------------------+
| Contributors      | ~150     | N/A         | Welcoming!        |
+-------------------+----------+-------------+-------------------+
| Avg PR Time       | 2-4 weeks| N/A         | Be patient        |
+-------------------+----------+-------------+-------------------+
| Code Review       | Strict   | N/A         | Learn best        |
|                   |          |             | practices         |
+-------------------+----------+-------------+-------------------+

**Tips for Successful Contribution:**

✅ **DO:**

* Read CONTRIBUTING.md first
* Start small (typo fix, then bigger)
* Ask questions in issues before coding
* Follow existing code style
* Add tests for new features
* Update documentation with code changes
* Be patient with review process

❌ **DON'T:**

* Submit large PRs without discussion
* Change unrelated code
* Ignore reviewer feedback
* Skip testing on real hardware
* Forget to sign-off commits (DCO)

🔧 Development Tools & Workflow
================================

Essential Tools
---------------

.. code-block:: bash

   # Code analysis
   sudo apt install cppcheck clang-tidy
   
   # Cross-compilation (for ARM)
   sudo apt install gcc-arm-none-eabi
   
   # Documentation building
   pip install sphinx sphinx-rtd-theme breathe
   
   # Debugging
   sudo apt install gdb-multiarch openocd

Recommended IDE Setup
----------------------

**VS Code Extensions:**

* C/C++ (Microsoft)
* CMake Tools
* Remote - SSH (for board debugging)
* Git Graph
* reStructuredText (for docs)

**settings.json:**

.. code-block:: json

   {
       "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools",
       "cmake.buildDirectory": "${workspaceFolder}/build",
       "files.associations": {
           "*.rst": "restructuredtext"
       }
   }

📱 Community & Support
======================

+-------------------+-------------------------------------------------------+
| Resource          | Link / Details                                        |
+===================+=======================================================+
| GitHub            | https://github.com/OpenAMP                            |
+-------------------+-------------------------------------------------------+
| Mailing List      | openamp-rp@lists.openampproject.org                   |
+-------------------+-------------------------------------------------------+
| Website           | https://www.openampproject.org                        |
+-------------------+-------------------------------------------------------+
| Documentation     | https://openamp.readthedocs.io                        |
+-------------------+-------------------------------------------------------+
| Meetings          | Monthly technical meetings (check website)            |
+-------------------+-------------------------------------------------------+
| Slack/Discord     | Check openampproject.org for invite                   |
+-------------------+-------------------------------------------------------+

**How to Ask for Help:**

1. Check documentation first
2. Search existing issues
3. Post on mailing list with:
   
   * Clear problem description
   * Platform/environment details
   * What you've already tried
   * Relevant logs/code snippets

🚀 Your First Contribution Checklist
=====================================

.. code-block:: text

   Week 1: Learning
   ☐ Read OpenAMP overview documentation
   ☐ Clone repositories
   ☐ Build libmetal and open-amp
   ☐ Run echo demo (on simulator or hardware)
   ☐ Join mailing list
   
   Week 2: Exploring
   ☐ Read 3-5 existing issues
   ☐ Understand resource table format
   ☐ Study one example in detail
   ☐ Compile documentation locally
   
   Week 3: Contributing
   ☐ Find a "good first issue" or doc improvement
   ☐ Fork repository
   ☐ Make your changes
   ☐ Test thoroughly
   ☐ Create pull request
   
   Week 4: Iterating
   ☐ Respond to review comments
   ☐ Update PR based on feedback
   ☐ Celebrate merge! 🎉
   ☐ Plan next contribution

📚 Reference Commands Cheat Sheet
==================================

.. code-block:: bash

   # Quick build & test
   cd open-amp/build
   make clean && cmake .. && make -j$(nproc)
   
   # Run unit tests
   ctest --verbose
   
   # Build docs
   cd openamp-docs
   make html
   firefox _build/html/index.html
   
   # Cross-compile for ARM
   cmake .. \
     -DCMAKE_TOOLCHAIN_FILE=../cmake/toolchain-arm-none-eabi.cmake \
     -DCMAKE_BUILD_TYPE=Debug
   
   # Check code style
   clang-format -i lib/rpmsg/*.c
   
   # Generate Doxygen
   cd open-amp
   doxygen Doxyfile
   
   # Search for TODOs in code
   grep -r "TODO\|FIXME\|XXX" lib/ --include="*.c" --include="*.h"

🎯 Specific Beginner Tasks (Start Here!)
=========================================

Task 1: Fix Documentation Typo
-------------------------------

**Estimated Time:** 15 minutes

.. code-block:: bash

   # Example: Fix typo in overview.rst
   git clone https://github.com/OpenAMP/openamp-docs.git
   cd openamp-docs
   git checkout -b fix-overview-typo
   
   # Edit file (fix "proces" → "process")
   vim openamp/overview.rst
   
   # Test build
   make html
   
   # Commit
   git add openamp/overview.rst
   git commit -m "docs: fix typo in overview - proces -> process"
   git push origin fix-overview-typo

Task 2: Add Example Comment
----------------------------

**Estimated Time:** 30 minutes

.. code-block:: c

   // In open-amp/apps/examples/echo/echo.c
   // Add helpful comment explaining the flow
   
   /**
    * Echo test main function
    * 
    * This example demonstrates basic RPMsg communication:
    * 1. Initialize OpenAMP framework
    * 2. Create RPMsg endpoint
    * 3. Wait for messages from remote
    * 4. Echo received messages back
    * 
    * @return 0 on success, negative on error
    */
   int main(void)
   {
       // Your enhanced comments here...
   }

Task 3: Report a Build Warning
-------------------------------

**Estimated Time:** 20 minutes

.. code-block:: bash

   # Build with strict warnings
   cd open-amp/build
   cmake .. -DCMAKE_C_FLAGS="-Wall -Wextra"
   make 2>&1 | tee build.log
   
   # If you find warnings, report them
   # Create issue on GitHub with:
   # - Warning message
   # - GCC version
   # - Platform
   # - How to reproduce

🏆 Success Metrics
==================

After 1 Month, You Should Be Able To:
--------------------------------------

✅ Explain AMP vs SMP  
✅ Describe RPMsg protocol basics  
✅ Build OpenAMP from source  
✅ Run echo demo  
✅ Navigate the codebase  
✅ Understand resource tables  
✅ Make your first PR (doc or code)  

After 3 Months:
---------------

✅ Port OpenAMP to new RTOS  
✅ Debug communication issues  
✅ Write custom RPMsg services  
✅ Contribute meaningful code changes  
✅ Help other newcomers  

===============================================
✅ Quick Start Summary
===============================================

1. **Learn:** Read overview.rst, understand AMP concept
2. **Build:** Clone repos, build libmetal + open-amp
3. **Try:** Run echo demo
4. **Contribute:** Fix docs → Add examples → Fix bugs → New features
5. **Engage:** Join mailing list, ask questions, attend meetings

**Your First PR Should Be:** Documentation improvement (safest, fastest)

**Best Resources:**

* Docs: https://openamp.readthedocs.io
* Code: https://github.com/OpenAMP/open-amp
* Issues: Search "good first issue" label

**Remember:** Everyone was a beginner once. Don't hesitate to ask questions!

===============================================
📅 Last Updated: January 2026
===============================================
