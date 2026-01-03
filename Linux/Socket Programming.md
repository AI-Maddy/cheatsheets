**cheatsheet for socket programming in Linux** (POSIX/BSD-style sockets, applicable to modern kernels 6.x / 2025–2026 era).  
Focus: TCP, UDP, UNIX domain, common patterns, error handling, and best practices for server/client applications.

### 1. Socket Families & Types (Most Common)

| Family              | Constant             | Use Case                              | Typical Protocol |
|---------------------|----------------------|---------------------------------------|------------------|
| `AF_INET`           | IPv4                 | Internet (most common)                | `SOCK_STREAM` / `SOCK_DGRAM` |
| `AF_INET6`          | IPv6                 | Modern dual-stack servers             | same             |
| `AF_UNIX` / `AF_LOCAL` | UNIX domain       | Inter-process on same machine         | `SOCK_STREAM` / `SOCK_DGRAM` |
| `AF_PACKET`         | Raw packets          | Packet sniffing / custom protocols    | —                |

| Type                | Constant             | Semantics                             | Reliable? |
|---------------------|----------------------|---------------------------------------|-----------|
| `SOCK_STREAM`       | TCP                  | Connection-oriented, byte stream      | Yes       |
| `SOCK_DGRAM`        | UDP                  | Datagram, connectionless              | No        |
| `SOCK_RAW`          | Raw IP/CAN/...       | Direct access to lower layer          | Varies    |
| `SOCK_SEQPACKET`    | Rarely used          | Reliable datagrams (SCTP-like)        | Yes       |

### 2. Basic Socket Lifecycle (TCP Server Example)

```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

int main() {
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) { perror("socket"); return 1; }

    int opt = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr = {0};
    addr.sin_family      = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port        = htons(8080);

    if (bind(listen_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind"); return 1;
    }

    if (listen(listen_fd, SOMAXCONN) < 0) {  // SOMAXCONN ≈ 128–4096
        perror("listen"); return 1;
    }

    printf("Listening on port 8080...\n");

    while (1) {
        int client_fd = accept(listen_fd, NULL, NULL);
        if (client_fd < 0) { perror("accept"); continue; }

        char buf[1024];
        ssize_t n = read(client_fd, buf, sizeof(buf));
        if (n > 0) {
            write(client_fd, buf, n);           // echo
        }
        close(client_fd);
    }

    close(listen_fd);
    return 0;
}
```

### 3. Most Important Socket Options (setsockopt / getsockopt)

| Level          | Option                     | Purpose / Common Value                              | When to set |
|----------------|----------------------------|-----------------------------------------------------|-------------|
| `SOL_SOCKET`   | `SO_REUSEADDR`             | Allow bind after quick close                        | Server always |
| `SOL_SOCKET`   | `SO_REUSEPORT`             | Multiple processes bind same port (load balancing)  | Multi-worker server |
| `SOL_SOCKET`   | `SO_KEEPALIVE`             | Enable TCP keepalive probes                         | Long-lived connections |
| `SOL_SOCKET`   | `SO_RCVBUF` / `SO_SNDBUF`  | Set receive/send buffer size                        | High-throughput |
| `SOL_SOCKET`   | `SO_RCVTIMEO` / `SO_SNDTIMEO` | Set recv/send timeout (struct timeval)           | Non-blocking style |
| `SOL_SOCKET`   | `SO_TIMESTAMP` / `SO_TIMESTAMPNS` | Enable RX timestamping                        | Precise timing |
| `IPPROTO_TCP`  | `TCP_NODELAY`              | Disable Nagle (low-latency)                         | Real-time / gaming |
| `IPPROTO_TCP`  | `TCP_QUICKACK`             | Send ACKs immediately (low-latency)                 | Interactive apps |
| `IPPROTO_TCP`  | `TCP_USER_TIMEOUT`         | Override default timeout (ms)                       | Detect dead peers faster |

### 4. Common Patterns & Idioms

| Pattern                     | Code snippet / Tip                                                                 |
|-----------------------------|-------------------------------------------------------------------------------------|
| Non-blocking I/O            | `fcntl(fd, F_SETFL, O_NONBLOCK)` + `select()` / `poll()` / `epoll()`               |
| Edge-triggered epoll        | Use `EPOLLET` flag + loop until `EAGAIN`                                            |
| Accept4 (modern)            | `accept4(listen_fd, NULL, NULL, SOCK_CLOEXEC)` — atomic CLOEXEC                     |
| Dual-stack server           | Bind `AF_INET6` + `IPV6_V6ONLY=0` → accepts both IPv4 & IPv6                        |
| UNIX domain socket          | `struct sockaddr_un sun; sun.sun_family=AF_UNIX; strcpy(sun.sun_path, "/tmp/mysock");` |
| UDP broadcast               | `setsockopt(fd, SOL_SOCKET, SO_BROADCAST, &one, sizeof(one))`                      |
| Multicast                   | `setsockopt(fd, IPPROTO_IP, IP_ADD_MEMBERSHIP, ...)`                               |
| Zero-copy send              | `sendfile()` / `splice()` / `MSG_ZEROCOPY` (kernel ≥4.14)                          |

### 5. Error Handling & Return Values (Critical)

| Function    | Success       | Failure                  | Common errno                          |
|-------------|---------------|--------------------------|---------------------------------------|
| `socket()`  | fd ≥ 0        | -1                       | `EAFNOSUPPORT`, `EMFILE`              |
| `bind()`    | 0             | -1                       | `EADDRINUSE`, `EACCES`                |
| `listen()`  | 0             | -1                       | `EINVAL`                              |
| `accept()`  | new fd ≥ 0    | -1                       | `EAGAIN` (non-blocking), `ECONNABORTED` |
| `connect()` | 0             | -1                       | `EINPROGRESS` (non-blocking), `ECONNREFUSED` |
| `read()/recv()` | bytes > 0 | 0 (EOF), -1              | `EAGAIN`, `ECONNRESET`                |
| `write()/send()` | bytes ≥ 0 | -1                       | `EPIPE` (broken pipe)                 |

**Always check**:
```c
if ((n = recv(fd, buf, len, 0)) <= 0) {
    if (n == 0) { /* EOF */ } else if (errno != EAGAIN && errno != EWOULDBLOCK) { /* error */ }
}
```

### 6. Modern Alternatives / Helpers

- **libevent** / **libev** / **libuv** → event loops
- **epoll** (Linux-specific) → best performance for many connections
- **io_uring** (kernel ≥5.1) → async I/O, zero-copy possible
- **getaddrinfo()** → modern name resolution (replaces `gethostbyname`)
- **inet_pton() / inet_ntop()** → safe IP string ↔ binary conversion

### 7. Quick One-liners (Testing / Debugging)

```bash
# Simple TCP echo server (netcat)
nc -l -p 12345 -k -e /bin/cat

# UDP test
nc -u -l 12345                  # server
echo "test" | nc -u 127.0.0.1 12345  # client

# Check listening sockets
ss -ltnp
netstat -tuln

# Show socket statistics
ss -m -i  # memory & info
```

This cheatsheet covers 90% of day-to-day socket programming tasks in Linux user-space applications (servers, clients, proxies, IoT, embedded networking).  
For kernel-level networking (netfilter, eBPF, custom protocols) look at `net/socket.c` and `include/linux/net.h`.

Good luck with your socket code!