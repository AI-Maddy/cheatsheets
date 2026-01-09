 **Linux udev cheat sheet** 
 (valid for modern systems using **systemd-udevd**, i.e. roughly Linux kernel 5.10–6.12+, systemd 250–257+, as of early 2026).

📌 1. Where to Put Rules

Location                          | Priority | Purpose
----------------------------------|----------|----------------------------------------------
``/etc/udev/rules.d/*.rules``       | Highest   | Custom / local overrides (recommended)
``/lib/udev/rules.d/*.rules``       | Medium    | Distribution-provided defaults
``/run/udev/rules.d/*.rules``       | Low       | Runtime / generated (🔴 🔴 avoid manual edits)

**Naming convention**: Use ``NN-name.rules`` (e.g. ``70-my-usb-serial.rules``, ``99-local.rules``). Lower number = processed earlier.

📌 2. Basic Rule Syntax

One rule = one line (can be continued with ``\``).

ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="1a86", ATTR{idProduct}=="7523", SYMLINK+="serial/myftdi", MODE="0660", GROUP="dialout", TAG+="uaccess"

**General format**:

⭐ match keys (conditions)   ,   assignment keys (actions)

Rules are evaluated **top to bottom** — first match usually wins for most assignments (later rules can still append with ``+=``).

⭐ 📌 3. Most Useful Match Keys (left side)

⭐ Key              | Matches on                             | Example value(s)                          | Singular / Plural
-----------------|----------------------------------------|-------------------------------------------|-------------------
``ACTION``         | "add", "remove", "change", "bind"…     | ``"add"``, ``"remove"``                       | —
``KERNEL`` / ``KERNELS`` | Device node name (sdX, ttyUSB0…)    | ``"ttyUSB[0-9]*"``                          | singular / parents
``SUBSYSTEM`` / ``SUBSYSTEMS`` | Block, usb, input, net…          | ``"usb"``, ``"tty"``, ``"block"``               | singular / parents
``DRIVER`` / ``DRIVERS`` | Kernel driver name                  | ``"ftdi_sio"``, ``"cdc_acm"``                 | singular / parents
``ATTR{…}`` / ``ATTRS{…}`` | /sys/device/…/file content          | ``ATTR{idVendor}=="0bda"``                  | singular / parents
``ENV{…}``         | Environment variable                   | ``ENV{ID_MODEL}=="Gamepad"``                | —
``PROGRAM``        | External script returns 0 → match      | ``PROGRAM="/usr/bin/check-serial.py %k"``   | —
``RESULT``         | Last PROGRAM output (string match)     | ``RESULT=="yes"``                           | —

**Tip**: Use ``ATTRS{…}`` for parent devices (most common pattern).

⭐ 📌 4. Most Useful Assignment Keys (right side)

⭐ Key               | Meaning                                      | Common operators     | Example
------------------|----------------------------------------------|----------------------|---------------------
``NAME``            | Device node name (/dev/…) — rarely used      | ``=``                  | ``NAME="myusb%d"``
``SYMLINK``         | Additional symlink(s)                        | ``+=``, ``=``            | ``SYMLINK+="myserial"``
``MODE``            | Permissions (octal)                          | ``=``                  | ``MODE="0660"``
``OWNER`` / ``GROUP`` | Owner / group of device node                 | ``=``                  | ``GROUP="plugdev"``
``TAG``             | Add tags (e.g. ``"uaccess"``, ``"seat"``)        | ``+=``, ``=``            | ``TAG+="uaccess"``
⭐ ``ENV{key}``        | Set environment variable                     | ``=``, ``+=``            | ``ENV{ID_SERIAL_SHORT}="abc123"``
``RUN``             | Execute program/script (after node creation) | ``+=``                 | ``RUN+="/usr/bin/my-notify.sh"``
``RUN{builtin}``    | Run udev built-in (e.g. ``hwdb``, ``path_id``)   | ``+=``                 | ``RUN{builtin}+="hwdb --subsystem=usb"``
``GOTO``, ``LABEL``   | Jump in the same file                        | —                    | ``GOTO="end"``

**Modern 🟢 🟢 best practice** (2024–2026):  
Instead of ``GROUP="plugdev"`` + ``MODE="0660"``, use  
``TAG+="uaccess"`` + ``MODE="0660"``  
(systemd-logind sets ACLs for active graphical/logged-in users)

🏗️ 5. Common Patterns (Copy-Paste Ready)

**USB serial adapter → fixed name + permissions**

.. code-block:: text

================================================================================
/etc/udev/rules.d/70-usb-serial.rules
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
    SYMLINK+="serial/ftdi-%s{serial}", MODE="0660", GROUP="dialout", TAG+="uaccess"

**Specific USB device (by serial number)**

.. code-block:: text

SUBSYSTEM=="usb", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", \
    ATTRS{serial}=="12345ABC", SYMLINK+="arduino", OWNER="user", MODE="0660"

**Webcam → fixed video number**

.. code-block:: text

SUBSYSTEM=="video4linux", KERNEL=="video*", \
    ATTRS{idVendor}=="046d", ATTRS{idProduct}=="082d", \
    SYMLINK+="video/conference"

**Block device (USB disk) → symlink by serial**

.. code-block:: text

SUBSYSTEM=="block", ACTION=="add", ATTRS{idVendor}=="0781", \
    SYMLINK+="usb/%E{idSerialShort}", OWNER="user"

**Run script on device plug**

.. code-block:: text

ACTION=="add", SUBSYSTEM=="usb", DRIVER=="usbhid", \
    RUN+="/usr/local/bin/notify-device.sh '%k' added"

📌 6. udevadm — The Swiss Army Knife

Command                                            | Purpose
---------------------------------------------------|-------------------------------------------------------
⭐ ``udevadm info -a -p /sys/class/tty/ttyUSB0``        | Show all match-able attributes (most important!)
``udevadm info -a -n /dev/ttyUSB0``                  | Same, using /dev node
``udevadm monitor --environment --udev``             | Watch real-time events
``udevadm trigger``                                  | Re-apply rules to all/current devices
``udevadm trigger --action=add /dev/ttyUSB0``        | Simulate add event for one device
``udevadm control --reload-rules``                   | Reload rules (no reboot needed)
``udevadm settle``                                   | Wait until event queue is processed
``udevadm test $(udevadm info -q path -n /dev/xxx)`` | Dry-run: simulate rule processing
``udevadm lock --device=/dev/sdb -- mycommand …``    | Take exclusive lock on device (since ~255)

**Quick debug workflow**:

.. code-block:: bash

================================================================================
🔧 1. Plug device
================================================================================

================================================================================
2. Find path
================================================================================

udevadm info -q path -n /dev/mydevice

================================================================================
3. Walk attributes
================================================================================

udevadm info -a -p /sys/.../that/path

================================================================================
🟢 ✅ 🟢 🟢 ✅ 4. Test rule syntax without applying
================================================================================

udevadm test /sys/.../that/path

💡 7. Quick Tips (2025–2026)

- Always prefer ``ATTRS{…}`` over ``ATTR{…}`` when matching parent USB/serial/PCI info.
- Use ``%k`` (kernel name), ``%n`` (device number), ``%E{ID_SERIAL_SHORT}`` in SYMLINK/RUN.
- 🔴 🔴 Avoid changing ``NAME=`` for block/video devices — prefer ``SYMLINK+=``.
- For network interfaces use ``.link`` files (``/etc/systemd/network/``) instead of udev.
- Debug logs: ``journalctl -u systemd-udevd`` or set ``udev.log-priority=debug`` in ``/etc/systemd/system.conf``.
- Modern systems no longer generate persistent-net.rules by default — use ``.link`` files or predictable interface names.

🟢 🟢 Good luck writing your rules! Start by using ``udevadm info -a`` on your device — 90% of the work is finding the right ``ATTRS{}`` values.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
