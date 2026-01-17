================================================================================
Linux Networking & Socket Programming - Comprehensive Reference
================================================================================

**Focus:** Socket programming, CAN bus (SocketCAN), network interfaces, protocols  
**Target Audience:** Embedded systems engineers, network developers  
**Kernel Versions:** 6.1–6.12+ (2026 best practices)  
**Last Updated:** January 2026

================================================================================

TL;DR - Quick Reference
================================================================================

**Socket Family Comparison:**

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Family
     - Constant
     - Use Case
     - Protocol
     - Performance
   * - **IPv4**
     - AF_INET
     - Internet (most common)
     - TCP/UDP
     - High
   * - **IPv6**
     - AF_INET6
     - Modern dual-stack
     - TCP/UDP
     - High
   * - **UNIX Domain**
     - AF_UNIX
     - IPC same machine
     - Stream/Dgram
     - Very High
   * - **CAN**
     - AF_CAN
     - Automotive/Industrial
     - CAN_RAW
     - Medium
   * - **Packet**
     - AF_PACKET
     - Raw packet access
     - ETH_P_ALL
     - Low-level

**Essential Socket Commands:**

.. code-block:: bash

    # Network interfaces
    ip link show                          # List interfaces
    ip addr show eth0                     # Show IP config
    ip link set eth0 up                   # Bring up interface
    ethtool eth0                          # Interface stats
    
    # Socket statistics
    ss -ltnp                              # Listening TCP sockets
    ss -lunp                              # Listening UDP sockets
    netstat -tuln                         # Legacy socket list
    
    # CAN bus
    ip link set can0 type can bitrate 500000
    ip link set can0 up
    cansend can0 123#1122334455667788
    candump can0
    
    # Packet capture
    tcpdump -i eth0 -w capture.pcap
    wireshark

**Quick Socket Templates:**

.. code-block:: c

    // TCP Server
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    bind(fd, &addr, sizeof(addr));
    listen(fd, SOMAXCONN);
    int client = accept(fd, NULL, NULL);
    
    // UDP Server
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    bind(fd, &addr, sizeof(addr));
    recvfrom(fd, buf, len, 0, &from, &fromlen);
    
    // CAN Socket
    int fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    bind(fd, (struct sockaddr*)&addr, sizeof(addr));
    write(fd, &frame, sizeof(frame));

================================================================================

1. Socket Programming Fundamentals
================================================================================

1.1 Socket Families & Types
----------------------------

**Socket Address Families:**

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Family
     - Constant
     - Description
   * - Internet Protocol v4
     - AF_INET
     - Most common, 32-bit addresses
   * - Internet Protocol v6
     - AF_INET6
     - 128-bit addresses, modern
   * - UNIX Domain Sockets
     - AF_UNIX / AF_LOCAL
     - IPC on same host (fast)
   * - CAN
     - AF_CAN
     - Controller Area Network
   * - Packet
     - AF_PACKET
     - Raw packet interface
   * - Netlink
     - AF_NETLINK
     - Kernel-user communication

**Socket Types:**

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Type
     - Constant
     - Protocol
     - Characteristics
   * - **Stream**
     - SOCK_STREAM
     - TCP
     - Reliable, ordered, connection-oriented
   * - **Datagram**
     - SOCK_DGRAM
     - UDP
     - Unreliable, connectionless
   * - **Raw**
     - SOCK_RAW
     - Custom
     - Direct protocol access
   * - **Sequential Packet**
     - SOCK_SEQPACKET
     - SCTP
     - Reliable datagrams

1.2 TCP Server Implementation
------------------------------

**Complete TCP Echo Server:**

.. code-block:: c

    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <stdio.h>
    #include <string.h>
    #include <errno.h>
    
    #define PORT 8080
    #define BACKLOG 128
    
    int main(void)
    {
        int listen_fd, client_fd;
        struct sockaddr_in server_addr, client_addr;
        socklen_t client_len;
        char buffer[1024];
        ssize_t n;
        int opt = 1;
        
        /* Create socket */
        listen_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (listen_fd < 0) {
            perror("socket");
            return 1;
        }
        
        /* Set socket options */
        if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR,
                       &opt, sizeof(opt)) < 0) {
            perror("setsockopt SO_REUSEADDR");
            close(listen_fd);
            return 1;
        }
        
        if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEPORT,
                       &opt, sizeof(opt)) < 0) {
            perror("setsockopt SO_REUSEPORT");
            close(listen_fd);
            return 1;
        }
        
        /* Bind to address */
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(PORT);
        
        if (bind(listen_fd, (struct sockaddr*)&server_addr,
                 sizeof(server_addr)) < 0) {
            perror("bind");
            close(listen_fd);
            return 1;
        }
        
        /* Listen for connections */
        if (listen(listen_fd, BACKLOG) < 0) {
            perror("listen");
            close(listen_fd);
            return 1;
        }
        
        printf("TCP server listening on port %d...\n", PORT);
        
        /* Accept loop */
        while (1) {
            client_len = sizeof(client_addr);
            client_fd = accept(listen_fd,
                               (struct sockaddr*)&client_addr,
                               &client_len);
            if (client_fd < 0) {
                perror("accept");
                continue;
            }
            
            printf("Accepted connection from %s:%d\n",
                   inet_ntoa(client_addr.sin_addr),
                   ntohs(client_addr.sin_port));
            
            /* Echo loop */
            while ((n = recv(client_fd, buffer, sizeof(buffer), 0)) > 0) {
                if (send(client_fd, buffer, n, 0) != n) {
                    perror("send");
                    break;
                }
            }
            
            if (n < 0)
                perror("recv");
            else if (n == 0)
                printf("Client disconnected\n");
            
            close(client_fd);
        }
        
        close(listen_fd);
        return 0;
    }

1.3 UDP Server Implementation
------------------------------

**Complete UDP Echo Server:**

.. code-block:: c

    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <stdio.h>
    #include <string.h>
    
    #define PORT 8080
    
    int main(void)
    {
        int sockfd;
        struct sockaddr_in server_addr, client_addr;
        socklen_t client_len;
        char buffer[1024];
        ssize_t n;
        
        /* Create UDP socket */
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (sockfd < 0) {
            perror("socket");
            return 1;
        }
        
        /* Bind to address */
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(PORT);
        
        if (bind(sockfd, (struct sockaddr*)&server_addr,
                 sizeof(server_addr)) < 0) {
            perror("bind");
            close(sockfd);
            return 1;
        }
        
        printf("UDP server listening on port %d...\n", PORT);
        
        /* Receive and echo loop */
        while (1) {
            client_len = sizeof(client_addr);
            n = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                         (struct sockaddr*)&client_addr,
                         &client_len);
            if (n < 0) {
                perror("recvfrom");
                continue;
            }
            
            printf("Received %zd bytes from %s:%d\n",
                   n, inet_ntoa(client_addr.sin_addr),
                   ntohs(client_addr.sin_port));
            
            /* Echo back */
            if (sendto(sockfd, buffer, n, 0,
                       (struct sockaddr*)&client_addr,
                       client_len) != n) {
                perror("sendto");
            }
        }
        
        close(sockfd);
        return 0;
    }

1.4 Socket Options (setsockopt/getsockopt)
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 25 35 20

   * - Level
     - Option
     - Purpose
     - Typical Value
   * - SOL_SOCKET
     - SO_REUSEADDR
     - Reuse local address (bind after crash)
     - 1
   * - SOL_SOCKET
     - SO_REUSEPORT
     - Multiple processes bind same port
     - 1
   * - SOL_SOCKET
     - SO_KEEPALIVE
     - Enable TCP keepalive
     - 1
   * - SOL_SOCKET
     - SO_RCVBUF
     - Set receive buffer size (bytes)
     - 262144
   * - SOL_SOCKET
     - SO_SNDBUF
     - Set send buffer size (bytes)
     - 262144
   * - SOL_SOCKET
     - SO_RCVTIMEO
     - Receive timeout (struct timeval)
     - {5, 0}
   * - SOL_SOCKET
     - SO_SNDTIMEO
     - Send timeout (struct timeval)
     - {5, 0}
   * - SOL_SOCKET
     - SO_TIMESTAMP
     - Enable RX timestamping
     - 1
   * - IPPROTO_TCP
     - TCP_NODELAY
     - Disable Nagle algorithm (low latency)
     - 1
   * - IPPROTO_TCP
     - TCP_QUICKACK
     - Send ACKs immediately
     - 1
   * - IPPROTO_TCP
     - TCP_USER_TIMEOUT
     - Override TCP timeout (ms)
     - 30000

**Socket Option Usage Example:**

.. code-block:: c

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    /* Enable address reuse */
    int opt = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    /* Set receive timeout */
    struct timeval tv = { .tv_sec = 5, .tv_usec = 0 };
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    
    /* Increase receive buffer */
    int bufsize = 262144;  // 256 KB
    setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize));
    
    /* Disable Nagle (low latency) */
    int nodelay = 1;
    setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &nodelay, sizeof(nodelay));

1.5 Non-Blocking I/O & epoll
-----------------------------

**Setting Non-Blocking Mode:**

.. code-block:: c

    #include <fcntl.h>
    
    int flags = fcntl(sockfd, F_GETFL, 0);
    fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);

**epoll Event Loop (Modern Scalable I/O):**

.. code-block:: c

    #include <sys/epoll.h>
    
    #define MAX_EVENTS 10
    
    int epfd = epoll_create1(0);
    if (epfd < 0) {
        perror("epoll_create1");
        return 1;
    }
    
    /* Add listening socket to epoll */
    struct epoll_event ev, events[MAX_EVENTS];
    ev.events = EPOLLIN;
    ev.data.fd = listen_fd;
    
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev) < 0) {
        perror("epoll_ctl");
        return 1;
    }
    
    /* Event loop */
    while (1) {
        int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);
        if (nfds < 0) {
            perror("epoll_wait");
            break;
        }
        
        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == listen_fd) {
                /* Accept new connection */
                int client_fd = accept(listen_fd, NULL, NULL);
                if (client_fd < 0) {
                    perror("accept");
                    continue;
                }
                
                /* Set non-blocking */
                int flags = fcntl(client_fd, F_GETFL, 0);
                fcntl(client_fd, F_SETFL, flags | O_NONBLOCK);
                
                /* Add to epoll */
                ev.events = EPOLLIN | EPOLLET;  // Edge-triggered
                ev.data.fd = client_fd;
                epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &ev);
            } else {
                /* Handle client data */
                int fd = events[i].data.fd;
                char buffer[1024];
                ssize_t n;
                
                while ((n = read(fd, buffer, sizeof(buffer))) > 0) {
                    write(fd, buffer, n);
                }
                
                if (n == 0 || (n < 0 && errno != EAGAIN)) {
                    /* Connection closed or error */
                    epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
                    close(fd);
                }
            }
        }
    }

================================================================================

2. CAN Bus (SocketCAN)
================================================================================

2.1 CAN Overview
-----------------

**CAN vs CAN FD Comparison:**

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - Classic CAN 2.0B
     - CAN FD
     - CAN XL (2026)
   * - **Max Payload**
     - 8 bytes
     - 64 bytes
     - 2048 bytes
   * - **Bit Rate**
     - 1 Mbit/s max
     - 1-5 Mbit/s nominal, 8-15 Mbit/s data
     - 20-100 Mbit/s data
   * - **Arbitration**
     - Non-destructive bitwise
     - Same (nominal phase)
     - Same + higher-speed
   * - **Error Detection**
     - CRC + bit stuffing + ACK
     - Enhanced CRC + stuff count
     - Stronger CRC
   * - **Typical Use**
     - Powertrain, chassis, body
     - ADAS, gateways, zonal ECUs
     - High-bandwidth backbone

**CAN Physical Layer:**

::

    ┌────────────┐      ┌────────────┐      ┌────────────┐
    │  ECU 1     │      │  ECU 2     │      │  ECU 3     │
    │            │      │            │      │            │
    └──┬─────┬───┘      └──┬─────┬───┘      └──┬─────┬───┘
       │CAN_H│            │CAN_H│            │CAN_H│
       │CAN_L│            │CAN_L│            │CAN_L│
    ───┴─────┴────────────┴─────┴────────────┴─────┴────
       120Ω                                      120Ω
    
    - Differential signaling: CAN_H and CAN_L
    - Recessive: ~2.5V on both lines
    - Dominant: CAN_H ~3.5V, CAN_L ~1.5V
    - 120Ω termination resistors at both ends

**Common CAN Bit Rates:**

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Bit Rate
     - Use Case
     - Typical Network
   * - 125 kbit/s
     - Body electronics
     - Door modules, lights
   * - 250 kbit/s
     - Comfort systems
     - Climate control, seats
   * - 500 kbit/s
     - Powertrain
     - Engine, transmission, ABS
   * - 1 Mbit/s
     - High-speed
     - Gateway, diagnostics

2.2 SocketCAN Structures
-------------------------

**CAN Frame Structures:**

.. code-block:: c

    #include <linux/can.h>
    #include <linux/can/raw.h>
    
    /* Classic CAN frame (max 8 bytes) */
    struct can_frame {
        canid_t can_id;   // 32-bit: ID + flags
        __u8    can_dlc;  // Data Length Code (0-8)
        __u8    __pad;
        __u8    __res0;
        __u8    __res1;
        __u8    data[8] __attribute__((aligned(8)));
    };
    
    /* CAN FD frame (up to 64 bytes) */
    struct canfd_frame {
        canid_t can_id;   // 32-bit: ID + flags
        __u8    len;      // Data length (0-64)
        __u8    flags;    // CANFD_BRS, CANFD_ESI
        __u8    __res0;
        __u8    __res1;
        __u8    data[64] __attribute__((aligned(8)));
    };
    
    /* CAN ID flags (in can_id field) */
    #define CAN_EFF_FLAG 0x80000000U  // Extended Frame Format (29-bit ID)
    #define CAN_RTR_FLAG 0x40000000U  // Remote Transmission Request
    #define CAN_ERR_FLAG 0x20000000U  // Error frame
    
    /* Extract actual CAN ID */
    #define CAN_SFF_MASK 0x000007FFU  // Standard Frame Format (11-bit)
    #define CAN_EFF_MASK 0x1FFFFFFFU  // Extended Frame Format (29-bit)

2.3 SocketCAN Programming
--------------------------

**Complete CAN Send/Receive Example:**

.. code-block:: c

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <unistd.h>
    #include <net/if.h>
    #include <sys/ioctl.h>
    #include <sys/socket.h>
    #include <linux/can.h>
    #include <linux/can/raw.h>
    
    int main(int argc, char *argv[])
    {
        int s;
        struct sockaddr_can addr;
        struct ifreq ifr;
        struct can_frame frame;
        
        /* Create CAN socket */
        s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
        if (s < 0) {
            perror("socket");
            return 1;
        }
        
        /* Get interface index */
        strcpy(ifr.ifr_name, "can0");
        if (ioctl(s, SIOCGIFINDEX, &ifr) < 0) {
            perror("SIOCGIFINDEX");
            close(s);
            return 1;
        }
        
        /* Bind socket to CAN interface */
        memset(&addr, 0, sizeof(addr));
        addr.can_family = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;
        
        if (bind(s, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            perror("bind");
            close(s);
            return 1;
        }
        
        /* Send CAN frame */
        memset(&frame, 0, sizeof(frame));
        frame.can_id = 0x123;  // 11-bit standard ID
        frame.can_dlc = 8;
        frame.data[0] = 0x11;
        frame.data[1] = 0x22;
        frame.data[2] = 0x33;
        frame.data[3] = 0x44;
        frame.data[4] = 0x55;
        frame.data[5] = 0x66;
        frame.data[6] = 0x77;
        frame.data[7] = 0x88;
        
        if (write(s, &frame, sizeof(frame)) != sizeof(frame)) {
            perror("write");
            close(s);
            return 1;
        }
        
        printf("Sent CAN frame: ID=0x%03X DLC=%d Data=%02X %02X %02X %02X %02X %02X %02X %02X\n",
               frame.can_id, frame.can_dlc,
               frame.data[0], frame.data[1], frame.data[2], frame.data[3],
               frame.data[4], frame.data[5], frame.data[6], frame.data[7]);
        
        /* Receive CAN frame */
        ssize_t nbytes = read(s, &frame, sizeof(frame));
        if (nbytes < 0) {
            perror("read");
            close(s);
            return 1;
        }
        
        if (nbytes < sizeof(struct can_frame)) {
            fprintf(stderr, "Incomplete CAN frame\n");
            close(s);
            return 1;
        }
        
        printf("Received CAN frame: ID=0x%03X DLC=%d Data=%02X %02X %02X %02X %02X %02X %02X %02X\n",
               frame.can_id & CAN_SFF_MASK, frame.can_dlc,
               frame.data[0], frame.data[1], frame.data[2], frame.data[3],
               frame.data[4], frame.data[5], frame.data[6], frame.data[7]);
        
        close(s);
        return 0;
    }

2.4 CAN Filtering
-----------------

**CAN Filter Configuration:**

.. code-block:: c

    #include <linux/can.h>
    #include <linux/can/raw.h>
    
    /* Define filter: accept only ID 0x200-0x2FF */
    struct can_filter rfilter[1];
    rfilter[0].can_id   = 0x200;
    rfilter[0].can_mask = CAN_SFF_MASK & ~0x0FF;  // Mask lower 8 bits
    
    if (setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER,
                   &rfilter, sizeof(rfilter)) < 0) {
        perror("setsockopt CAN_RAW_FILTER");
        return 1;
    }
    
    /* Multiple filters example */
    struct can_filter rfilter[3];
    rfilter[0].can_id   = 0x123;
    rfilter[0].can_mask = CAN_SFF_MASK;  // Exact match 0x123
    
    rfilter[1].can_id   = 0x200;
    rfilter[1].can_mask = 0x7F0;         // Accept 0x200-0x20F
    
    rfilter[2].can_id   = 0x100 | CAN_EFF_FLAG;
    rfilter[2].can_mask = CAN_EFF_MASK;  // Extended ID 0x100
    
    setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER, &rfilter, sizeof(rfilter));

2.5 CAN FD Programming
-----------------------

**CAN FD Send/Receive:**

.. code-block:: c

    #include <linux/can.h>
    #include <linux/can/raw.h>
    
    /* Enable CAN FD */
    int enable_fd = 1;
    if (setsockopt(s, SOL_CAN_RAW, CAN_RAW_FD_FRAMES,
                   &enable_fd, sizeof(enable_fd)) < 0) {
        perror("setsockopt CAN_RAW_FD_FRAMES");
        return 1;
    }
    
    /* Send CAN FD frame */
    struct canfd_frame fdframe;
    memset(&fdframe, 0, sizeof(fdframe));
    fdframe.can_id = 0x7DF | CAN_EFF_FLAG;  // Extended ID
    fdframe.len = 64;                       // Max CAN FD payload
    fdframe.flags = CANFD_BRS;              // Bit Rate Switch
    
    for (int i = 0; i < 64; i++)
        fdframe.data[i] = i;
    
    if (write(s, &fdframe, CANFD_MTU) != CANFD_MTU) {
        perror("write CAN FD");
        return 1;
    }
    
    /* Receive CAN FD frame */
    ssize_t nbytes = read(s, &fdframe, CANFD_MTU);
    if (nbytes == CANFD_MTU) {
        printf("Received CAN FD frame: ID=0x%08X len=%d\n",
               fdframe.can_id & CAN_EFF_MASK, fdframe.len);
    }

2.6 CAN Tools & Debugging
--------------------------

**CAN Interface Configuration:**

.. code-block:: bash

    # Classic CAN setup
    ip link set can0 type can bitrate 500000
    ip link set can0 up
    
    # CAN FD setup
    ip link set can0 type can bitrate 2000000 dbitrate 8000000 fd on
    ip link set can0 up
    
    # Virtual CAN (testing)
    modprobe vcan
    ip link add dev vcan0 type vcan
    ip link set vcan0 up

**CAN Utilities (can-utils package):**

.. code-block:: bash

    # Send CAN frame (ID 0x123, data 01 02 03 04 05 06 07 08)
    cansend can0 123#0102030405060708
    
    # Send CAN FD frame
    cansend can0 18ABCDEF##100112233445566778899AABBCCDDEEFF
    
    # Dump all CAN traffic
    candump can0
    
    # Dump with timestamps
    candump -t a -l can0
    
    # Filter specific IDs
    candump can0,123:7FF
    
    # Generate random traffic
    cangen can0 -g 10 -I 123 -L 8
    
    # Sniffer with terminal UI
    cansniffer can0
    
    # Replay captured traffic
    canplayer -I capture.log
    
    # Show statistics
    ip -details -statistics link show can0

================================================================================

3. Network Interfaces
================================================================================

3.1 Network Interface Management
---------------------------------

**Interface Configuration:**

.. code-block:: bash

    # List all interfaces
    ip link show
    ifconfig -a
    
    # Bring interface up/down
    ip link set eth0 up
    ip link set eth0 down
    ifconfig eth0 up
    
    # Set IP address
    ip addr add 192.168.1.100/24 dev eth0
    ifconfig eth0 192.168.1.100 netmask 255.255.255.0
    
    # Set MAC address
    ip link set eth0 address 00:11:22:33:44:55
    
    # Set MTU
    ip link set eth0 mtu 9000
    
    # Show interface statistics
    ip -s link show eth0
    ethtool -S eth0

**Interface Types:**

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Interface Type
     - Description
     - Example
   * - Physical Ethernet
     - Hardware NIC
     - eth0, eno1, enp0s3
   * - VLAN
     - Virtual LAN
     - eth0.10 (VLAN ID 10)
   * - Bridge
     - Software switch
     - br0
   * - Bond
     - Link aggregation
     - bond0
   * - TUN/TAP
     - Virtual network device
     - tun0, tap0
   * - VXLAN
     - Virtual Extensible LAN
     - vxlan0
   * - CAN
     - Controller Area Network
     - can0, vcan0

3.2 Routing & Forwarding
-------------------------

**Routing Table Management:**

.. code-block:: bash

    # Show routing table
    ip route show
    route -n
    
    # Add default gateway
    ip route add default via 192.168.1.1
    route add default gw 192.168.1.1
    
    # Add static route
    ip route add 10.0.0.0/8 via 192.168.1.254
    
    # Delete route
    ip route del 10.0.0.0/8
    
    # Enable IP forwarding
    echo 1 > /proc/sys/net/ipv4/ip_forward
    sysctl -w net.ipv4.ip_forward=1

3.3 Interface Statistics & Monitoring
--------------------------------------

**Network Statistics:**

.. code-block:: bash

    # Interface statistics
    cat /proc/net/dev
    ip -s link show eth0
    ethtool -S eth0
    
    # Socket statistics
    ss -s                          # Summary
    ss -ltnp                       # Listening TCP
    ss -lunp                       # Listening UDP
    ss -tunap                      # All TCP/UDP
    
    # Connection tracking
    cat /proc/net/nf_conntrack
    conntrack -L
    
    # Network performance
    iperf3 -s                      # Server
    iperf3 -c 192.168.1.100        # Client
    
    # Bandwidth monitoring
    iftop -i eth0
    nethogs eth0

================================================================================

4. Exam Question: Multi-Protocol Network System
================================================================================

**Question (18 points):**

Design and implement a multi-protocol embedded gateway with the following requirements:

- **Ethernet (eth0):** TCP server on port 5000, receives commands
- **CAN (can0):** Translates TCP commands to CAN frames (500 kbit/s)
- **UNIX Domain Socket:** Logs all transactions to /tmp/gateway.sock
- **UDP:** Broadcasts status on port 6000 every 5 seconds

**Part A (6 points):** Implement the main event loop using epoll to handle all sockets.

**Part B (5 points):** Implement the TCP → CAN translation function. Command format: "CAN <ID> <data>" where ID is hex (e.g., "CAN 0x123 01020304").

**Part C (4 points):** Implement the UDP status broadcast. Include: uptime, received frames count, CAN bus state.

**Part D (3 points):** Write a bash script to configure the system and test all interfaces.

**Answer:**

**Part A: Main Event Loop**

.. code-block:: c

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <unistd.h>
    #include <sys/socket.h>
    #include <sys/epoll.h>
    #include <sys/un.h>
    #include <netinet/in.h>
    #include <net/if.h>
    #include <linux/can.h>
    #include <linux/can/raw.h>
    #include <time.h>
    
    #define MAX_EVENTS 10
    #define TCP_PORT 5000
    #define UDP_PORT 6000
    #define UNIX_SOCK_PATH "/tmp/gateway.sock"
    
    struct gateway_state {
        int tcp_fd;
        int can_fd;
        int unix_fd;
        int udp_fd;
        unsigned long rx_count;
        time_t start_time;
    };
    
    int setup_tcp_server(int port);
    int setup_can_socket(const char *ifname);
    int setup_unix_socket(const char *path);
    int setup_udp_broadcast(int port);
    void handle_tcp_command(int fd, struct gateway_state *state);
    void broadcast_status(struct gateway_state *state);
    
    int main(void)
    {
        struct gateway_state state = {0};
        struct epoll_event ev, events[MAX_EVENTS];
        int epfd;
        
        state.start_time = time(NULL);
        
        /* Setup sockets */
        state.tcp_fd = setup_tcp_server(TCP_PORT);
        state.can_fd = setup_can_socket("can0");
        state.unix_fd = setup_unix_socket(UNIX_SOCK_PATH);
        state.udp_fd = setup_udp_broadcast(UDP_PORT);
        
        if (state.tcp_fd < 0 || state.can_fd < 0 ||
            state.unix_fd < 0 || state.udp_fd < 0) {
            fprintf(stderr, "Failed to setup sockets\n");
            return 1;
        }
        
        /* Create epoll instance */
        epfd = epoll_create1(0);
        if (epfd < 0) {
            perror("epoll_create1");
            return 1;
        }
        
        /* Add TCP server socket */
        ev.events = EPOLLIN;
        ev.data.fd = state.tcp_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, state.tcp_fd, &ev);
        
        /* Add CAN socket */
        ev.events = EPOLLIN;
        ev.data.fd = state.can_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, state.can_fd, &ev);
        
        printf("Gateway started: TCP=%d CAN=%d UNIX=%d UDP=%d\n",
               TCP_PORT, state.can_fd, state.unix_fd, UDP_PORT);
        
        /* Main event loop */
        time_t last_broadcast = time(NULL);
        
        while (1) {
            int nfds = epoll_wait(epfd, events, MAX_EVENTS, 1000);
            
            for (int i = 0; i < nfds; i++) {
                if (events[i].data.fd == state.tcp_fd) {
                    /* Accept TCP connection */
                    int client_fd = accept(state.tcp_fd, NULL, NULL);
                    if (client_fd >= 0) {
                        ev.events = EPOLLIN;
                        ev.data.fd = client_fd;
                        epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &ev);
                        printf("TCP client connected\n");
                    }
                } else if (events[i].data.fd == state.can_fd) {
                    /* Receive CAN frame */
                    struct can_frame frame;
                    if (read(state.can_fd, &frame, sizeof(frame)) > 0) {
                        state.rx_count++;
                        printf("CAN RX: ID=0x%03X DLC=%d\n",
                               frame.can_id, frame.can_dlc);
                    }
                } else {
                    /* Handle TCP client data */
                    handle_tcp_command(events[i].data.fd, &state);
                }
            }
            
            /* Broadcast status every 5 seconds */
            time_t now = time(NULL);
            if (now - last_broadcast >= 5) {
                broadcast_status(&state);
                last_broadcast = now;
            }
        }
        
        return 0;
    }

**Part B: TCP → CAN Translation**

.. code-block:: c

    #include <ctype.h>
    
    void handle_tcp_command(int fd, struct gateway_state *state)
    {
        char buffer[256];
        ssize_t n = read(fd, buffer, sizeof(buffer) - 1);
        
        if (n <= 0) {
            epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
            close(fd);
            printf("TCP client disconnected\n");
            return;
        }
        
        buffer[n] = '\0';
        
        /* Parse "CAN <ID> <data>" */
        if (strncmp(buffer, "CAN ", 4) == 0) {
            unsigned int can_id;
            char data_str[64];
            
            if (sscanf(buffer + 4, "%x %s", &can_id, data_str) == 2) {
                struct can_frame frame;
                memset(&frame, 0, sizeof(frame));
                
                frame.can_id = can_id & CAN_SFF_MASK;
                frame.can_dlc = 0;
                
                /* Parse hex data bytes */
                for (int i = 0; i < strlen(data_str) && i < 16; i += 2) {
                    if (frame.can_dlc >= 8)
                        break;
                    
                    char byte_str[3] = { data_str[i], data_str[i+1], '\0' };
                    frame.data[frame.can_dlc++] =
                        (unsigned char)strtoul(byte_str, NULL, 16);
                }
                
                /* Send CAN frame */
                if (write(state->can_fd, &frame, sizeof(frame)) ==
                    sizeof(frame)) {
                    /* Log to UNIX socket */
                    char log[128];
                    snprintf(log, sizeof(log),
                             "CAN TX: ID=0x%03X DLC=%d\n",
                             frame.can_id, frame.can_dlc);
                    write(state->unix_fd, log, strlen(log));
                    
                    /* Acknowledge to TCP client */
                    write(fd, "OK\n", 3);
                    
                    printf("Translated TCP → CAN: ID=0x%03X DLC=%d\n",
                           frame.can_id, frame.can_dlc);
                } else {
                    write(fd, "ERROR: CAN send failed\n", 23);
                }
            } else {
                write(fd, "ERROR: Invalid format\n", 22);
            }
        } else {
            write(fd, "ERROR: Unknown command\n", 23);
        }
    }

**Part C: UDP Status Broadcast**

.. code-block:: c

    void broadcast_status(struct gateway_state *state)
    {
        struct sockaddr_in broadcast_addr;
        char status[256];
        time_t uptime = time(NULL) - state->start_time;
        
        /* Get CAN bus state */
        char can_state[32] = "ACTIVE";
        FILE *fp = fopen("/sys/class/net/can0/operstate", "r");
        if (fp) {
            fscanf(fp, "%s", can_state);
            fclose(fp);
        }
        
        /* Format status message */
        snprintf(status, sizeof(status),
                 "GATEWAY_STATUS uptime=%ld rx_count=%lu can_state=%s\n",
                 uptime, state->rx_count, can_state);
        
        /* Broadcast to UDP */
        memset(&broadcast_addr, 0, sizeof(broadcast_addr));
        broadcast_addr.sin_family = AF_INET;
        broadcast_addr.sin_addr.s_addr = inet_addr("255.255.255.255");
        broadcast_addr.sin_port = htons(UDP_PORT);
        
        sendto(state->udp_fd, status, strlen(status), 0,
               (struct sockaddr*)&broadcast_addr,
               sizeof(broadcast_addr));
        
        printf("Status broadcast: %s", status);
    }
    
    int setup_udp_broadcast(int port)
    {
        int fd = socket(AF_INET, SOCK_DGRAM, 0);
        if (fd < 0)
            return -1;
        
        int broadcast = 1;
        setsockopt(fd, SOL_SOCKET, SO_BROADCAST,
                   &broadcast, sizeof(broadcast));
        
        return fd;
    }

**Part D: System Configuration & Test Script**

.. code-block:: bash

    #!/bin/bash
    
    echo "=== Network Gateway Configuration & Test ==="
    echo
    
    # 1. Configure CAN interface
    echo "1. Configuring CAN interface..."
    sudo modprobe can
    sudo modprobe can_raw
    sudo modprobe vcan  # Virtual CAN for testing
    
    sudo ip link add dev vcan0 type vcan
    sudo ip link set vcan0 up
    
    # If using real CAN hardware:
    # sudo ip link set can0 type can bitrate 500000
    # sudo ip link set can0 up
    
    echo "   ✓ CAN interface configured"
    ip link show can0 2>/dev/null || ip link show vcan0
    echo
    
    # 2. Configure network
    echo "2. Configuring network..."
    sudo ip addr add 192.168.7.2/24 dev eth0 2>/dev/null || true
    echo "   ✓ Network configured"
    echo
    
    # 3. Start gateway (in background)
    echo "3. Starting gateway..."
    ./gateway &
    GATEWAY_PID=$!
    sleep 2
    echo "   ✓ Gateway started (PID: $GATEWAY_PID)"
    echo
    
    # 4. Test TCP → CAN translation
    echo "4. Testing TCP → CAN translation..."
    echo "CAN 0x123 01020304" | nc localhost 5000 &
    sleep 1
    echo "   ✓ TCP command sent"
    echo
    
    # 5. Monitor CAN traffic
    echo "5. Monitoring CAN traffic (5 seconds)..."
    timeout 5 candump vcan0 &
    echo
    
    # 6. Listen for UDP broadcasts
    echo "6. Listening for UDP status broadcasts (10 seconds)..."
    timeout 10 nc -lu 6000 &
    echo
    
    # 7. Check UNIX socket log
    echo "7. Checking UNIX socket log..."
    if [ -e /tmp/gateway.sock ]; then
        echo "   ✓ UNIX socket exists: /tmp/gateway.sock"
        nc -U /tmp/gateway.sock &
        UNIX_NC_PID=$!
        sleep 2
        kill $UNIX_NC_PID 2>/dev/null
    fi
    echo
    
    # 8. Statistics
    echo "8. System statistics:"
    echo "   TCP connections:"
    ss -tn | grep :5000
    echo "   CAN interface stats:"
    ip -s link show vcan0 | grep -A 2 "RX:"
    echo
    
    # Cleanup
    echo "=== Test Complete ==="
    echo "Press Ctrl+C to stop gateway..."
    wait $GATEWAY_PID

================================================================================

5. Key Takeaways
================================================================================

**Socket Programming Best Practices (2026):**

1. **Always set SO_REUSEADDR** on server sockets
2. **Use epoll for scalability** (handles 10k+ connections efficiently)
3. **Set timeouts** (SO_RCVTIMEO, SO_SNDTIMEO) to prevent hangs
4. **Disable Nagle** (TCP_NODELAY) for low-latency applications
5. **Check all return values** - network errors are common
6. **Use non-blocking I/O** for production servers
7. **Implement proper error recovery** (especially for EPIPE, ECONNRESET)

**CAN Bus Best Practices:**

1. **Use filters** to reduce CPU load (kernel-space filtering)
2. **Enable hardware timestamps** for precise timing
3. **Check bus state** regularly (/sys/class/net/can0/operstate)
4. **Implement error handling** for bus-off conditions
5. **Use CAN FD** for modern vehicles (higher bandwidth)
6. **Virtual CAN** (vcan) for development/testing
7. **Monitor error counters** (ip -s link show can0)

**Common Pitfalls:**

::

    ✗ Socket: Forgetting SO_REUSEADDR (bind fails after crash)
    ✗ Socket: Not handling SIGPIPE (write to closed socket kills process)
    ✗ Socket: Hardcoding buffer sizes (use dynamic allocation)
    ✗ CAN: Not checking can_dlc before accessing data array
    ✗ CAN: Assuming CAN ID is always standard (check CAN_EFF_FLAG)
    ✗ CAN: Not filtering frames (receives all bus traffic)
    ✗ Network: Not checking MTU for large packets

**Performance Tuning:**

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Parameter
     - Default
     - Optimized
   * - Socket receive buffer
     - 128 KB
     - 256-512 KB
   * - Socket send buffer
     - 128 KB
     - 256-512 KB
   * - TCP congestion control
     - cubic
     - bbr (2026)
   * - CAN RX queue length
     - 10
     - 100-1000
   * - epoll timeout
     - -1 (blocking)
     - 100 ms (responsive)

================================================================================

**Last Updated:** January 2026  
**Kernel Version:** 6.8+  
**Status:** Production Ready

================================================================================
