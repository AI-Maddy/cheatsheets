🎯 OpenAMP Contribution Workflow - Step by Step
================================================

.. contents:: 📑 Navigation
   :depth: 2
   :local:

🚦 Before You Start - Prerequisites
====================================

Development Environment Setup
------------------------------

.. code-block:: bash

   # 1. Install build tools
   sudo apt update
   sudo apt install -y \
       build-essential \
       cmake \
       git \
       gcc-arm-none-eabi \
       python3 python3-pip \
       doxygen graphviz

   # 2. For documentation
   pip3 install sphinx sphinx-rtd-theme breathe

   # 3. Configure Git
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"

   # 4. Create GitHub account (if you don't have one)
   # Go to https://github.com/join

Fork & Clone Strategy
----------------------

.. code-block:: bash

   # 1. Fork on GitHub web UI:
   #    - Go to https://github.com/OpenAMP/open-amp
   #    - Click "Fork" button (top right)
   
   # 2. Clone YOUR fork locally
   git clone https://github.com/YOUR_USERNAME/open-amp.git
   cd open-amp
   
   # 3. Add upstream remote (original OpenAMP repo)
   git remote add upstream https://github.com/OpenAMP/open-amp.git
   
   # 4. Verify remotes
   git remote -v
   # Should show:
   # origin    https://github.com/YOUR_USERNAME/open-amp.git (fetch)
   # origin    https://github.com/YOUR_USERNAME/open-amp.git (push)
   # upstream  https://github.com/OpenAMP/open-amp.git (fetch)
   # upstream  https://github.com/OpenAMP/open-amp.git (push)

📋 Contribution Types & Difficulty
===================================

+----+---------------------------+-----------+------------------+------------------+
| #  | Contribution Type         | Difficulty| Time Estimate    | Repos            |
+====+===========================+===========+==================+==================+
| 1  | Fix typos in docs         | ⭐         | 15-30 min        | openamp-docs     |
+----+---------------------------+-----------+------------------+------------------+
| 2  | Improve README            | ⭐         | 1-2 hours        | All repos        |
+----+---------------------------+-----------+------------------+------------------+
| 3  | Add code comments         | ⭐⭐       | 2-4 hours        | open-amp         |
+----+---------------------------+-----------+------------------+------------------+
| 4  | Fix compiler warnings     | ⭐⭐       | 3-6 hours        | open-amp/libmetal|
+----+---------------------------+-----------+------------------+------------------+
| 5  | Add example/demo          | ⭐⭐⭐     | 1-2 days         | open-amp         |
+----+---------------------------+-----------+------------------+------------------+
| 6  | Port to new platform      | ⭐⭐⭐⭐   | 1-2 weeks        | libmetal         |
+----+---------------------------+-----------+------------------+------------------+
| 7  | Fix bug                   | ⭐⭐⭐⭐⭐ | Varies           | open-amp/libmetal|
+----+---------------------------+-----------+------------------+------------------+
| 8  | Add new feature           | ⭐⭐⭐⭐⭐ | 2-4 weeks        | open-amp         |
+----+---------------------------+-----------+------------------+------------------+

🎯 Task #1: Fix Documentation Typo (START HERE!)
=================================================

Why Start Here?
---------------

* **Lowest risk** - Can't break code
* **Fast feedback** - Quick PR review
* **Learn workflow** - Git, PR process
* **Build confidence** - Easy win!

Step-by-Step Walkthrough
-------------------------

**1. Find a Typo**

.. code-block:: bash

   # Clone openamp-docs
   git clone https://github.com/YOUR_USERNAME/openamp-docs.git
   cd openamp-docs
   git remote add upstream https://github.com/OpenAMP/openamp-docs.git
   
   # Search for common typos
   grep -r "proces " openamp/  # Should be "process"
   grep -r "reciever" .        # Should be "receiver"
   grep -r "occured" .         # Should be "occurred"

**2. Create Feature Branch**

.. code-block:: bash

   # Always create branch from latest upstream/main
   git fetch upstream
   git checkout -b fix-typo-overview upstream/main
   
   # Branch naming convention:
   # - fix-*      for bug fixes
   # - feat-*     for features
   # - docs-*     for documentation
   # - refactor-* for code cleanup

**3. Make Your Changes**

.. code-block:: bash

   # Edit the file
   vim openamp/overview.rst
   
   # Example change:
   # Line 45: "the proces of loading" → "the process of loading"

**4. Build & Test Documentation**

.. code-block:: bash

   # Build HTML docs
   make html
   
   # Check output (no errors/warnings)
   # Open in browser
   firefox _build/html/index.html
   
   # Verify your change looks correct

**5. Commit Your Changes**

.. code-block:: bash

   # Stage the file
   git add openamp/overview.rst
   
   # Commit with good message
   git commit -s -m "docs: fix typo in overview - proces -> process"
   
   # Note: -s adds "Signed-off-by" (required for DCO)

**6. Push to Your Fork**

.. code-block:: bash

   git push origin fix-typo-overview

**7. Create Pull Request**

1. Go to https://github.com/YOUR_USERNAME/openamp-docs
2. Click "Compare & pull request" button
3. Fill in PR template:

.. code-block:: markdown

   **Description:**
   Fixed typo in openamp/overview.rst - changed "proces" to "process"
   
   **Type of change:**
   - [x] Documentation update
   - [ ] Bug fix
   - [ ] New feature
   
   **Testing:**
   - Built documentation locally
   - Verified change in HTML output
   
   **Checklist:**
   - [x] Signed-off commit (DCO)
   - [x] Builds without errors
   - [x] Follows existing style

4. Click "Create pull request"

**8. Respond to Review**

.. code-block:: bash

   # If reviewer requests changes:
   
   # 1. Make the changes
   vim openamp/overview.rst
   
   # 2. Add to existing commit
   git add openamp/overview.rst
   git commit --amend --no-edit
   
   # 3. Force push (updates PR)
   git push origin fix-typo-overview --force

**9. Celebrate! 🎉**

Once merged, you're an official OpenAMP contributor!

🔧 Task #2: Fix Compiler Warning
=================================

Finding Warnings
----------------

.. code-block:: bash

   cd open-amp
   mkdir build && cd build
   
   # Build with strict warnings
   cmake .. \
     -DCMAKE_C_FLAGS="-Wall -Wextra -Wpedantic" \
     -DCMAKE_BUILD_TYPE=Debug
   
   make 2>&1 | tee build.log
   
   # Look for warnings like:
   # warning: unused parameter 'foo' [-Wunused-parameter]
   # warning: implicit declaration of function 'bar'

Example Fix
-----------

**Before:**

.. code-block:: c

   int rpmsg_send(struct rpmsg_endpoint *ept, void *data,
                  size_t len, int flags)
   {
       // Warning: unused parameter 'flags'
       return rpmsg_send_offchannel_raw(ept, data, len, 1);
   }

**After:**

.. code-block:: c

   int rpmsg_send(struct rpmsg_endpoint *ept, void *data,
                  size_t len, int flags)
   {
       (void)flags;  // Mark as intentionally unused
       return rpmsg_send_offchannel_raw(ept, data, len, 1);
   }

Commit Message
--------------

.. code-block:: bash

   git commit -s -m "fix: suppress unused parameter warning in rpmsg_send
   
   Added explicit cast to void for 'flags' parameter to suppress
   compiler warning when building with -Wunused-parameter.
   
   The flags parameter is reserved for future use."

📝 Task #3: Improve Code Comments
==================================

Target Files
------------

Good candidates for comment improvements:

* ``lib/rpmsg/rpmsg.c`` - Core RPMsg functions
* ``lib/remoteproc/remoteproc.c`` - RemoteProc API
* ``apps/examples/echo/echo.c`` - Example code

Comment Style Guide
-------------------

.. code-block:: c

   /**
    * @brief Brief description (one line)
    * 
    * Detailed description explaining:
    * - What the function does
    * - Any important behavior/side effects
    * - Thread-safety considerations
    * - Memory ownership
    * 
    * @param ept       Pointer to RPMsg endpoint
    * @param data      Message buffer to send
    * @param len       Length of message in bytes (max 512)
    * @param flags     Reserved, must be 0
    * 
    * @return 0 on success, negative error code on failure
    * @retval -EINVAL  Invalid parameters
    * @retval -ENOMEM  No buffer available
    * @retval -ENODEV  Endpoint not ready
    * 
    * @note This function may block if no buffers are available
    * @warning data must remain valid until send completes
    * 
    * Example:
    * @code
    * char msg[] = "Hello";
    * ret = rpmsg_send(&my_ept, msg, sizeof(msg), 0);
    * if (ret < 0) {
    *     printf("Send failed: %d\n", ret);
    * }
    * @endcode
    */
   int rpmsg_send(struct rpmsg_endpoint *ept, void *data,
                  size_t len, int flags);

🐛 Task #4: Report a Bug
=========================

Bug Report Template
-------------------

Create issue on GitHub with this template:

.. code-block:: markdown

   ## Bug Description
   
   **Summary:** RPMsg messages fail after 100 sends
   
   **Expected behavior:**
   Messages should be sent reliably indefinitely
   
   **Actual behavior:**
   After ~100 messages, rpmsg_send() returns -ENOMEM
   
   ## Environment
   
   - **OpenAMP version:** v2023.10 (commit abc1234)
   - **libmetal version:** v2023.04
   - **Host platform:** Linux 5.15, x86_64
   - **Remote platform:** STM32MP157, Cortex-M4, FreeRTOS 10.4
   - **Compiler:** arm-none-eabi-gcc 10.3.1
   
   ## Steps to Reproduce
   
   1. Build echo example:
      ```bash
      cd open-amp/apps/examples/echo
      make
      ```
   
   2. Flash to STM32MP157
   
   3. Run host application
   
   4. Send messages in loop:
      ```c
      for (int i = 0; i < 200; i++) {
          ret = rpmsg_send(&ept, msg, len, 0);
          if (ret < 0) {
              printf("Failed at iteration %d\n", i);
              break;
          }
      }
      ```
   
   5. Observe failure around iteration 100
   
   ## Logs
   
   ```
   [  0.000] RPMsg initialized
   [  1.234] Endpoint created
   [  1.235] Sending message 1... OK
   [  1.240] Sending message 2... OK
   ...
   [ 10.125] Sending message 100... OK
   [ 10.130] Sending message 101... FAIL (-12)
   [ERROR] rpmsg_send: no buffer available
   ```
   
   ## Analysis
   
   Possible causes:
   - Buffer leak in remote side?
   - Virtqueue not being serviced?
   - Vring size too small?
   
   ## Additional Context
   
   - Only happens with high message rate (>50 msg/sec)
   - Works fine with delays between messages
   - Remote side shows all buffers "in use"
   
   ## Proposed Fix (optional)
   
   Increase vring size in resource table from 256 to 512 entries?

🔍 Finding Good First Issues
=============================

Where to Look
-------------

1. **GitHub Issue Labels:**

.. code-block:: bash

   # Search for beginner-friendly issues
   # Go to:
   https://github.com/OpenAMP/open-amp/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
   
   https://github.com/OpenAMP/libmetal/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22

2. **Code Scanning (Find TODOs):**

.. code-block:: bash

   cd open-amp
   
   # Find TODOs in code
   grep -rn "TODO\|FIXME\|XXX" lib/ --include="*.c" --include="*.h"
   
   # Example output:
   # lib/rpmsg/rpmsg.c:234:  // TODO: Add timeout support
   # lib/remoteproc/remoteproc.c:456:  /* FIXME: Handle error case */

3. **Missing Documentation:**

.. code-block:: bash

   cd openamp-docs
   
   # Find functions without descriptions
   grep -A5 "^.. doxygenfunction::" . -r | grep -B1 "undocumented"

Common Issue Types
------------------

+------------------------+--------------------+----------------------------------+
| Issue Type             | Difficulty         | Example                          |
+========================+====================+==================================+
| Missing NULL checks    | ⭐⭐               | Add validation in API functions  |
+------------------------+--------------------+----------------------------------+
| Memory leak            | ⭐⭐⭐             | Fix missing free() calls         |
+------------------------+--------------------+----------------------------------+
| Race condition         | ⭐⭐⭐⭐⭐         | Fix multi-thread access          |
+------------------------+--------------------+----------------------------------+
| Platform-specific bug  | ⭐⭐⭐⭐           | Fix endianness issue             |
+------------------------+--------------------+----------------------------------+
| Build system           | ⭐⭐               | Fix CMake warnings               |
+------------------------+--------------------+----------------------------------+

📊 Code Review Checklist
=========================

Before Submitting PR
--------------------

.. code-block:: text

   ☐ Code compiles without errors
   ☐ Code compiles without warnings (-Wall -Wextra)
   ☐ Follows existing code style
   ☐ Includes tests (if applicable)
   ☐ Documentation updated (if API changed)
   ☐ Commit message follows convention
   ☐ Signed-off with DCO (git commit -s)
   ☐ No unrelated changes included
   ☐ Tested on real hardware (if possible)
   ☐ Memory leaks checked (valgrind)

Commit Message Format
---------------------

.. code-block:: text

   <type>: <subject>
   
   <body>
   
   <footer>
   
   Examples:
   
   fix: prevent buffer overflow in rpmsg_send
   
   Added bounds checking before memcpy to prevent writing
   beyond buffer limits when message length exceeds
   maximum allowed size.
   
   Fixes #123
   Signed-off-by: Your Name <your.email@example.com>
   
   ---
   
   feat: add timeout support to rpmsg_recv
   
   Implemented configurable timeout for rpmsg_recv() to
   prevent indefinite blocking. Timeout of 0 means no wait,
   -1 means wait forever (existing behavior).
   
   Signed-off-by: Your Name <your.email@example.com>
   
   ---
   
   docs: clarify resource table format in porting guide
   
   Added detailed examples and diagram showing resource
   table structure with multiple vrings.
   
   Signed-off-by: Your Name <your.email@example.com>

Types:
------

* ``fix:`` Bug fix
* ``feat:`` New feature
* ``docs:`` Documentation only
* ``style:`` Code style (formatting, no logic change)
* ``refactor:`` Code refactoring
* ``test:`` Adding tests
* ``chore:`` Build system, dependencies

🧪 Testing Your Changes
========================

Unit Testing
------------

.. code-block:: bash

   cd open-amp/build
   
   # Run all tests
   ctest --verbose
   
   # Run specific test
   ctest -R rpmsg_test --verbose

Integration Testing
-------------------

.. code-block:: bash

   # Test on real hardware
   # 1. Build firmware for remote core
   cd apps/examples/echo
   make PLATFORM=stm32mp1
   
   # 2. Flash to board
   openocd -f board/stm32mp15x.cfg \
           -c "program echo.elf verify reset exit"
   
   # 3. Boot Linux and test
   modprobe rpmsg_char
   echo "test message" > /dev/rpmsg0

Memory Leak Testing
--------------------

.. code-block:: bash

   # Use valgrind
   valgrind --leak-check=full \
            --show-leak-kinds=all \
            --track-origins=yes \
            ./my_rpmsg_app

📞 Getting Help
===============

When Stuck
----------

1. **Check Documentation**

   * Read: https://openamp.readthedocs.io
   * Search existing issues
   * Check CONTRIBUTING.md

2. **Ask on Mailing List**

.. code-block:: text

   To: openamp-rp@lists.openampproject.org
   Subject: [Question] How to debug vring initialization?
   
   Hi OpenAMP team,
   
   I'm trying to port OpenAMP to a new platform (RaspberryPi Pico 2)
   and having issues with vring initialization.
   
   Environment:
   - libmetal: v2023.04
   - Platform: RP2350, dual Cortex-M33
   - RTOS: FreeRTOS 10.5
   
   Problem:
   The vring_init() call succeeds, but subsequent rpmsg_send()
   returns -ENOMEM immediately.
   
   What I've tried:
   - Verified shared memory is accessible from both cores
   - Checked alignment (16-byte aligned)
   - Increased vring size to 512 entries
   
   Logs attached.
   
   Any suggestions on what to check next?
   
   Thanks!

3. **Attend Tech Meetings**

   * Monthly OpenAMP meetings
   * Check https://www.openampproject.org for schedule
   * Ask to be added to calendar invite

🏆 Success Stories - Learn from Others
=======================================

Example Contributions
---------------------

**1. Documentation Fix by Beginner:**

.. code-block:: text

   PR #234: "docs: clarify vring alignment requirements"
   
   What: Added note that vrings must be 4KB aligned on ARM
   Impact: Saved hours of debugging for new users
   Time: 30 minutes
   Review: Approved in 2 days

**2. Platform Port:**

.. code-block:: text

   PR #456: "feat: add support for i.MX8M Mini"
   
   What: Ported libmetal and demo to i.MX8M platform
   Impact: Enabled OpenAMP on popular NXP platform
   Time: 2 weeks
   Review: Multiple iterations, merged after 1 month

**3. Bug Fix:**

.. code-block:: text

   PR #789: "fix: race condition in virtqueue notification"
   
   What: Fixed rare crash in multi-threaded environment
   Impact: Critical fix for production systems
   Time: 1 week investigation + 2 days fix
   Review: Thoroughly tested, merged in 2 weeks

📅 30-Day Contribution Plan
============================

Week 1: Learning
----------------

.. code-block:: text

   Day 1-2: Read OpenAMP overview and architecture docs
   Day 3-4: Build open-amp and libmetal from source
   Day 5-6: Run echo demo, understand the flow
   Day 7:   Join mailing list, introduce yourself

Week 2: Exploring
-----------------

.. code-block:: text

   Day 8-9:  Study resource table format
   Day 10-11: Read through rpmsg.c line by line
   Day 12-13: Try modifying echo example
   Day 14:    Find 3 "good first issue" candidates

Week 3: Contributing
--------------------

.. code-block:: text

   Day 15-16: Fix documentation typo (your first PR!)
   Day 17-18: Wait for review, respond to feedback
   Day 19-20: Add comments to confusing code section
   Day 21:    Submit second PR

Week 4: Growing
---------------

.. code-block:: text

   Day 22-25: Work on compiler warning fix
   Day 26-28: Test thoroughly on multiple platforms
   Day 29:    Submit PR, document testing done
   Day 30:    Celebrate 3 PRs submitted! Plan next steps

🎯 Measurable Goals
===================

After 1 Month:
--------------

☐ 1 merged PR (documentation)  
☐ 2 submitted PRs (in review)  
☐ Posted on mailing list  
☐ Attended 1 tech meeting  
☐ Built code on 2+ platforms  

After 3 Months:
---------------

☐ 5+ merged PRs  
☐ Ported to new platform OR fixed significant bug  
☐ Helped answer 1 newcomer question  
☐ Regular mailing list participant  

After 6 Months:
---------------

☐ 10+ merged PRs  
☐ Contributed new feature  
☐ Mentoring other beginners  
☐ Recognized community member  

===============================================
Remember: Every expert was once a beginner!
===============================================

The OpenAMP community is welcoming and supportive.
Don't be afraid to ask questions and make mistakes.

**Start small, stay consistent, keep learning.**

Good luck with your contributions! 🚀
