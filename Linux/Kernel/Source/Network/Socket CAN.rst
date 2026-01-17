**cheatsheet for SocketCAN** in Linux (kernel perspective + userspace usage, valid for kernels 6.x / 2025–2026 era).

SocketCAN is the standard Linux networking stack for **Controller Area Network (CAN)** buses — treats CAN as a network protocol family like TCP/IP.

🎓 1. Core Concepts & Comparison

| Concept                  | SocketCAN (Linux)                          | Classical CAN drivers (pre-SocketCAN) |
|--------------------------|--------------------------------------------|---------------------------------------|
| API                      | Berkeley sockets (AF_CAN)                  | ioctl / read/write on char device     |
| Multi-interface support  | Yes (multiple CAN devices)                 | Usually one at a time                 |
| Filtering                | Kernel-level efficient filters             | Often userspace or limited            |
| Broadcasting             | Yes (send to all listeners)                | No native support                     |
| Timestamping             | Hardware RX/TX timestamps (if driver supports) | Rarely                                |
| CAN FD support           | Full (since ~4.1)                          | No                                    |
| Virtual CAN (vcan)       | Yes (testing)                              | No                                    |

🌐 2. Socket Types

| Socket Type              | Purpose                                      | When to use                          |
|--------------------------|----------------------------------------------|--------------------------------------|
| ``SOCK_RAW``               | Raw CAN frames (incl. ID + data)             | Most common – full control           |
| ``SOCK_DGRAM``             | CAN ID filtering + broadcast (like UDP)      | When you want simple multicast       |
| ``CAN_RAW_FD_FRAMES``      | Enable CAN FD frames on RAW socket           | Modern vehicles / high-speed buses   |

⭐ 📌 3. Key Structures

.. code-block:: c

struct can_frame {                  // Classic CAN (8 bytes max)
    canid_t can_id;
    __u8    can_dlc;                // 0–8
    __u8    data[8] __attribute__((aligned(8)));
};

struct canfd_frame {                // CAN FD (up to 64 bytes)
    canid_t can_id;
    __u8    len;                    // 0–64 (non-linear mapping)
    __u8    __pad;
    __u8    __res0;
    __u8    flags;                  // CANFD flags (BRS, ESI)
    __u8    data[64] __attribute__((aligned(8)));
};

**CAN ID flags** (in ``can_id``):

- ``CAN_EFF_FLAG`` (0x80000000) → extended 29-bit ID
- ``CAN_RTR_FLAG``  (0x40000000) → Remote Transmission Request
- ``CAN_ERR_FLAG``  (0x20000000) → Error frame

⭐ 🌐 4. Important ioctls & Socket Options

| ioctl / setsockopt       | Purpose                                      | Typical Value / Example |
|--------------------------|----------------------------------------------|-------------------------|
| ``SIOCSCAN``               | Bind to CAN interface (use ``bind()``)         | —                       |
| ``CAN_RAW_FILTER``         | Set array of receive filters                 | ``struct can_filter filters[]`` |
| ``CAN_RAW_LOOPBACK``       | Enable/disable loopback of sent frames       | 1 / 0                   |
| ``CAN_RAW_RECV_OWN_MSGS``  | Receive own sent messages                    | Usually 0               |
| ``CAN_RAW_FD``             | Enable CAN FD frames                         | 1                       |
| ``CAN_RAW_FD_FRAMES``      | Allow sending/receiving CAN FD frames        | 1 (required for FD)     |
| ``CAN_RAW_ERR_FILTER``     | Receive error frames (CAN_ERR_FLAG)          | ``CAN_ERR_MASK``          |
| ``SO_TIMESTAMPING``        | Enable hardware timestamps                   | ``SOF_TIMESTAMPING_RX_HARDWARE`` |
| ``SIOCSCANGETTIMESTAMP``   | Get hardware timestamp (if supported)        | —                       |

💻 5. Quick Userspace Examples (C)

**Send classic CAN frame**

.. code-block:: c

int s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
struct sockaddr_can addr = { .can_family = AF_CAN, .can_ifindex = if_nametoindex("can0") };
bind(s, (struct sockaddr*)&addr, sizeof(addr));

struct can_frame frame = { .can_id = 0x123, .can_dlc = 8, .data = {1,2,3,4,5,6,7,8} };
write(s, &frame, sizeof(frame));

**Receive with filter (only ID 0x200–0x2FF)**

.. code-block:: c

struct can_filter rfilter[1];
rfilter[0].can_id   = 0x200;
rfilter[0].can_mask = CAN_SFF_MASK & ~0x0FF;  // accept 0x200–0x2FF

setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER, &rfilter, sizeof(rfilter));

**CAN FD send/receive**

.. code-block:: c

int s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
setsockopt(s, SOL_CAN_RAW, CAN_RAW_FD_FRAMES, &enable_fd, sizeof(enable_fd));

struct canfd_frame fdframe = { .can_id = 0x7DF | CAN_EFF_FLAG, .len = 64, .flags = CANFD_BRS };
memcpy(fdframe.data, large_payload, 64);
write(s, &fdframe, CANFD_MTU);   // CANFD_MTU = 72

🐧 6. Kernel Structures & Drivers (Quick Ref)

| Component                | Location / Driver                            | Notes |
|--------------------------|----------------------------------------------|-------|
| ``struct can_priv``        | ``include/linux/can/dev.h``                    | Per-device private data |
| ``can_rx_offload``         | ``net/can/rx_offload.c``                       | NAPI RX offload (high perf) |
| ``vcan``                   | ``net/can/vcan.c``                             | Virtual CAN for testing |
| ``can-gw``                 | ``net/can/gw.c``                               | CAN-to-CAN gateway/routing |
| Popular drivers          | ``mcp251xfd``, ``flexcan``, ``peak_usb``, ``slcan``, ``esdcan``, ``kvaser`` | Mainline + out-of-tree |

📌 7. Useful Command-Line Tools

.. code-block:: bash

================================================================================
Bring up interface
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



ip link set can0 type can bitrate 500000   # classic CAN
ip link set can0 type can bitrate 2000000 dbitrate 8000000 fd on  # CAN FD

ip link set can0 up

================================================================================
💾 Send frame (cansend from can-utils)
================================================================================

cansend can0 123#1122334455667788
cansend can0 18ABCDEF#00112233445566778899AABBCCDDEEFF  # CAN FD

================================================================================
Dump traffic
================================================================================

candump -l can0                                    # human readable
candump -t a -l can0                               # absolute timestamp

================================================================================
💻 Filter example
================================================================================

candump -i can0,123:7FF                            # only ID 0x123

================================================================================
CAN FD stats
================================================================================

ip -details -statistics link show can0

🐛 8. Debugging & Tuning Tips

- Check capabilities: ``ip -d link show can0``
- Error counters: ``ip -s -d link show can0`` (rx/tx errors, bus-off)
- Use ``can-utils`` package (candump, cansniffer, canplayer, cangen…)
- For high load: enable ``can_rx_offload``, tune RX FIFO size
- Virtual testing: ``modprobe vcan; ip link add dev vcan0 type vcan``

This cheatsheet covers the most practical parts of SocketCAN for embedded automotive, industrial, robotics, and testing use cases in Linux.

🟢 🟢 Good luck with your CAN development!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
