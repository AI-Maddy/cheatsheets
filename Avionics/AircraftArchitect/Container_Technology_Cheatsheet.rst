🐳 **CONTAINER TECHNOLOGY — Docker & Containerd for Aircraft IFE**
═══════════════════════════════════════════════════════════════════

**Context:** Containerization for IFE apps and microservices
**Focus:** Docker, containerd, security hardening, resource limits
**Use Cases:** IFE app deployment, A/B testing, rollback

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — CONTAINERS IN 60 SECONDS**
────────────────────────────────────────

**What is a Container:**

::

    Container = Isolated process + filesystem + network
    
    NOT a VM: Shares kernel with host
    Lighter: Start in <1 second, use <100 MB RAM

**Docker vs containerd:**

+----------------+-------------------+----------------------+
| **Feature**    | **Docker**        | **containerd**       |
+================+===================+======================+
| CLI            | docker            | ctr, nerdctl         |
+----------------+-------------------+----------------------+
| Image build    | ✅ Yes            | ❌ No (use buildkit) |
+----------------+-------------------+----------------------+
| Size           | ~200 MB           | ~50 MB               |
+----------------+-------------------+----------------------+
| Kubernetes     | Via dockershim    | ✅ Native            |
+----------------+-------------------+----------------------+

**Aviation Use Cases:**

- 🎬 IFE app isolation (each airline's custom app)
- 🔄 A/B testing (deploy new version to 10% of seats)
- 🚀 Fast rollback (revert to previous image)
- 📦 Consistent deployment (dev = staging = prod)

════════════════════════════════════════════════════════════════════

📖 **1. DOCKER BASICS**
═══════════════════════

**1.1 Dockerfile**
-----------------

.. code-block:: dockerfile

    # IFE Media Player
    FROM ubuntu:22.04
    
    # Metadata
    LABEL maintainer="ife-team@airline.com"
    LABEL version="2.0"
    
    # Install dependencies
    RUN apt-get update && apt-get install -y \
        ffmpeg \
        libgstreamer1.0-0 \
        libqt5widgets5 \
        && rm -rf /var/lib/apt/lists/*
    
    # Create non-root user
    RUN useradd -m -u 1000 ifeuser
    
    # Copy application
    WORKDIR /app
    COPY --chown=ifeuser:ifeuser ife-player /app/
    COPY --chown=ifeuser:ifeuser config/ /app/config/
    
    # Set permissions
    RUN chmod +x /app/ife-player
    
    # Switch to non-root user
    USER ifeuser
    
    # Expose port
    EXPOSE 8080
    
    # Health check
    HEALTHCHECK --interval=30s --timeout=3s \
      CMD curl -f http://localhost:8080/health || exit 1
    
    # Start application
    CMD ["/app/ife-player", "--config", "/app/config/app.conf"]

**1.2 Build & Run**
------------------

::

    # Build image
    docker build -t ife-player:2.0 .
    
    # Run container
    docker run -d \
      --name ife-seat-42 \
      -p 8080:8080 \
      -v /data/movies:/media:ro \
      --memory=512m \
      --cpus=1.0 \
      --restart=unless-stopped \
      ife-player:2.0
    
    # View logs
    docker logs -f ife-seat-42
    
    # Execute command in container
    docker exec -it ife-seat-42 /bin/bash
    
    # Stop container
    docker stop ife-seat-42
    
    # Remove container
    docker rm ife-seat-42

**1.3 Image Layers**
-------------------

**Concept:** Images built from layers (cached for reuse)

::

    FROM ubuntu:22.04          ← Layer 1 (base OS)
    RUN apt-get update         ← Layer 2 (package index)
    RUN apt-get install ffmpeg ← Layer 3 (dependencies)
    COPY ife-player /app/      ← Layer 4 (application)
    
    Total size: 300 MB
    
    If only Layer 4 changes → Rebuild only Layer 4 (fast!)

**Best Practices:**

.. code-block:: dockerfile

    # ❌ Bad: Creates 3 layers
    RUN apt-get update
    RUN apt-get install -y ffmpeg
    RUN apt-get install -y libqt5widgets5
    
    # ✅ Good: Creates 1 layer
    RUN apt-get update && apt-get install -y \
        ffmpeg \
        libqt5widgets5 \
        && rm -rf /var/lib/apt/lists/*

**1.4 Multi-Stage Build**
-------------------------

**Purpose:** Reduce final image size (exclude build tools)

.. code-block:: dockerfile

    # Stage 1: Build
    FROM golang:1.21 AS builder
    WORKDIR /src
    COPY . .
    RUN go build -o /app/ife-api main.go
    
    # Stage 2: Runtime
    FROM alpine:3.18
    RUN apk add --no-cache ca-certificates
    COPY --from=builder /app/ife-api /app/
    USER nobody
    CMD ["/app/ife-api"]

**Result:**

- Builder stage: 800 MB (Go compiler, tools)
- Final image: 20 MB (only binary + Alpine)

════════════════════════════════════════════════════════════════════

📖 **2. SECURITY HARDENING**
════════════════════════════

**2.1 Run as Non-Root User**
----------------------------

.. code-block:: dockerfile

    # Create user with specific UID
    RUN useradd -m -u 1000 -s /bin/bash ifeuser
    
    # Switch to non-root
    USER ifeuser
    
    # Files owned by ifeuser
    COPY --chown=ifeuser:ifeuser app/ /app/

**Verify:**

::

    $ docker exec ife-seat-42 whoami
    ifeuser

**2.2 Read-Only Filesystem**
----------------------------

::

    docker run -d \
      --name ife-seat-42 \
      --read-only \
      --tmpfs /tmp:rw,noexec,nosuid,size=100m \
      ife-player:2.0

**Benefits:**

- Prevents malware from writing to disk
- Immutable runtime environment
- Temporary files in tmpfs (memory)

**2.3 Seccomp Profile**
----------------------

**Purpose:** Restrict system calls

**Default profile blocks ~44 dangerous syscalls (e.g., `reboot`, `mount`)**

**Custom profile:**

.. code-block:: json

    {
      "defaultAction": "SCMP_ACT_ERRNO",
      "architectures": ["SCMP_ARCH_X86_64"],
      "syscalls": [
        {
          "names": ["read", "write", "open", "close", "stat", "fstat",
                   "poll", "lseek", "mmap", "mprotect", "munmap"],
          "action": "SCMP_ACT_ALLOW"
        }
      ]
    }

**Apply:**

::

    docker run --security-opt seccomp=profile.json ife-player:2.0

**2.4 AppArmor/SELinux**
-----------------------

**AppArmor (Ubuntu):**

::

    # Create profile
    cat > /etc/apparmor.d/docker-ife <<EOF
    profile docker-ife flags=(attach_disconnected,mediate_deleted) {
      #include <abstractions/base>
      
      network inet stream,
      network inet6 stream,
      
      /app/** r,
      /media/** r,
      /tmp/** rw,
      
      deny /proc/sys/** w,
      deny /sys/** w,
    }
    EOF
    
    # Load profile
    apparmor_parser -r /etc/apparmor.d/docker-ife
    
    # Apply to container
    docker run --security-opt apparmor=docker-ife ife-player:2.0

**SELinux (Red Hat):**

::

    docker run --security-opt label=level:s0:c100,c200 ife-player:2.0

**2.5 Capability Dropping**
---------------------------

**Linux Capabilities:** Fine-grained privileges (e.g., CAP_NET_ADMIN, CAP_SYS_ADMIN)

.. code-block:: bash

    # Drop ALL capabilities, add only what's needed
    docker run -d \
      --cap-drop=ALL \
      --cap-add=NET_BIND_SERVICE \
      ife-player:2.0

**Common Capabilities:**

- `NET_BIND_SERVICE` - Bind to port <1024
- `CHOWN` - Change file ownership
- `SETUID`/`SETGID` - Change user/group
- `SYS_ADMIN` - Dangerous (avoid!)

════════════════════════════════════════════════════════════════════

📖 **3. RESOURCE LIMITS**
═════════════════════════

**3.1 CPU Limits**
-----------------

::

    # Limit to 1.5 CPUs
    docker run --cpus=1.5 ife-player:2.0
    
    # Set CPU shares (relative weight)
    docker run --cpu-shares=512 ife-player:2.0
    
    # Pin to specific CPUs (cores 0-1)
    docker run --cpuset-cpus=0-1 ife-player:2.0

**3.2 Memory Limits**
--------------------

::

    # Hard limit: 512 MB
    docker run --memory=512m ife-player:2.0
    
    # Memory + Swap: 1 GB total
    docker run --memory=512m --memory-swap=1g ife-player:2.0
    
    # Disable OOM killer (container won't be killed, but may hang)
    docker run --memory=512m --oom-kill-disable ife-player:2.0
    
    # Memory reservation (soft limit)
    docker run --memory-reservation=256m ife-player:2.0

**3.3 Disk I/O Limits**
-----------------------

::

    # Limit read/write bandwidth
    docker run \
      --device-read-bps=/dev/sda:10mb \
      --device-write-bps=/dev/sda:5mb \
      ife-player:2.0
    
    # Limit IOPS
    docker run \
      --device-read-iops=/dev/sda:1000 \
      --device-write-iops=/dev/sda:500 \
      ife-player:2.0

**3.4 PID Limit**
----------------

::

    # Maximum 100 processes
    docker run --pids-limit=100 ife-player:2.0

════════════════════════════════════════════════════════════════════

📖 **4. DOCKER COMPOSE**
════════════════════════

**Purpose:** Define multi-container applications

**File:** `docker-compose.yml`

.. code-block:: yaml

    version: '3.8'
    
    services:
      ife-player:
        image: ife-player:2.0
        container_name: ife-seat-42
        ports:
          - "8080:8080"
        volumes:
          - /data/movies:/media:ro
          - /var/log/ife:/logs
        environment:
          - SEAT_NUMBER=42A
          - LOG_LEVEL=INFO
        deploy:
          resources:
            limits:
              cpus: '1.0'
              memory: 512M
            reservations:
              cpus: '0.5'
              memory: 256M
        restart: unless-stopped
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
          interval: 30s
          timeout: 3s
          retries: 3
        security_opt:
          - no-new-privileges:true
          - apparmor=docker-ife
        read_only: true
        tmpfs:
          - /tmp:size=100m,noexec
      
      ife-backend:
        image: ife-backend:1.5
        container_name: ife-backend
        ports:
          - "9000:9000"
        depends_on:
          - ife-database
        environment:
          - DB_HOST=ife-database
          - DB_PORT=3306
        restart: unless-stopped
      
      ife-database:
        image: mysql:8.0
        container_name: ife-db
        volumes:
          - ife-data:/var/lib/mysql
        environment:
          - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_password
          - MYSQL_DATABASE=ife
        secrets:
          - db_password
        restart: unless-stopped
    
    volumes:
      ife-data:
    
    secrets:
      db_password:
        file: ./secrets/db_password.txt

**Commands:**

::

    # Start all services
    docker-compose up -d
    
    # View logs
    docker-compose logs -f ife-player
    
    # Stop all services
    docker-compose down
    
    # Scale service
    docker-compose up -d --scale ife-player=5

════════════════════════════════════════════════════════════════════

📖 **5. AVIATION USE CASES**
════════════════════════════

**5.1 A/B Testing**
------------------

**Scenario:** Test new IFE version on 10% of seats

::

    # Deploy v1.0 to 90% of seats
    for seat in {1..90}; do
      docker run -d --name ife-seat-$seat ife-player:1.0
    done
    
    # Deploy v2.0 to 10% of seats (A/B test)
    for seat in {91..100}; do
      docker run -d --name ife-seat-$seat ife-player:2.0
    done
    
    # Monitor metrics (crash rate, satisfaction)
    # If v2.0 is stable → rollout to remaining 90%

**5.2 Fast Rollback**
--------------------

::

    # Current: v2.0 (has bug)
    docker stop ife-seat-42
    docker rm ife-seat-42
    
    # Rollback to v1.0 (< 5 seconds)
    docker run -d --name ife-seat-42 ife-player:1.0

**5.3 Airline-Specific Customization**
--------------------------------------

::

    # Delta Air Lines custom app
    docker run -d \
      --name ife-seat-1A \
      -e AIRLINE=DELTA \
      -v /data/delta/movies:/media:ro \
      -v /data/delta/config:/config:ro \
      ife-player:2.0
    
    # United Airlines custom app
    docker run -d \
      --name ife-seat-1B \
      -e AIRLINE=UNITED \
      -v /data/united/movies:/media:ro \
      -v /data/united/config:/config:ro \
      ife-player:2.0

════════════════════════════════════════════════════════════════════

📖 **6. CONTAINERD**
════════════════════

**6.1 Why containerd?**
-----------------------

**Advantages over Docker:**

- ✅ Lighter (50 MB vs 200 MB)
- ✅ Faster startup
- ✅ Native Kubernetes support
- ✅ Industry standard (CNCF)

**6.2 CLI: nerdctl**
-------------------

::

    # nerdctl = Docker-compatible CLI for containerd
    
    # Build image
    nerdctl build -t ife-player:2.0 .
    
    # Run container
    nerdctl run -d \
      --name ife-seat-42 \
      -p 8080:8080 \
      --memory=512m \
      ife-player:2.0
    
    # List containers
    nerdctl ps
    
    # View logs
    nerdctl logs ife-seat-42

**6.3 Integration with Kubernetes**
-----------------------------------

**containerd as CRI:**

.. code-block:: yaml

    # /etc/containerd/config.toml
    version = 2
    
    [plugins."io.containerd.grpc.v1.cri"]
      sandbox_image = "k8s.gcr.io/pause:3.7"
      
      [plugins."io.containerd.grpc.v1.cri".containerd]
        default_runtime_name = "runc"
        
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true

**Kubernetes Pod with containerd:**

.. code-block:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
      name: ife-seat-42
    spec:
      runtimeClassName: runc  # Uses containerd
      containers:
      - name: ife-player
        image: ife-player:2.0
        resources:
          limits:
            memory: "512Mi"
            cpu: "1.0"
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
═════════════════════════

**Q1:** Explain the difference between Docker and containerd.

**A1:**

**Docker:**

- Full container platform (build, run, share)
- Includes CLI (`docker`), daemon (`dockerd`), registry
- Higher-level, user-friendly
- Larger footprint (~200 MB)

**containerd:**

- Container runtime only (run containers)
- Industry standard (CNCF project)
- Used by Kubernetes, Docker (under the hood)
- Lighter (~50 MB)
- CLI: `ctr` (low-level), `nerdctl` (Docker-compatible)

**When to use each:**

- **Docker:** Development, quick prototyping
- **containerd:** Production Kubernetes, minimal systems

────────────────────────────────────────────────────────────────────

**Q2:** How do you secure a container? List 5 hardening techniques.

**A2:**

1. **Run as non-root user**

   ::

       USER 1000

2. **Read-only filesystem**

   ::

       docker run --read-only --tmpfs /tmp

3. **Drop capabilities**

   ::

       docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE

4. **Apply seccomp profile**

   ::

       docker run --security-opt seccomp=profile.json

5. **Resource limits**

   ::

       docker run --memory=512m --cpus=1.0

**Bonus:** AppArmor/SELinux, network policies, image scanning

────────────────────────────────────────────────────────────────────

**Q3:** You need to rollback IFE app from v2.0 to v1.0 quickly. Show the commands.

**A3:**

.. code-block:: bash

    # Stop and remove current version (v2.0)
    docker stop ife-seat-42
    docker rm ife-seat-42
    
    # Start previous version (v1.0) - takes < 5 seconds
    docker run -d \
      --name ife-seat-42 \
      -p 8080:8080 \
      -v /data/movies:/media:ro \
      --memory=512m \
      --restart=unless-stopped \
      ife-player:1.0
    
    # Verify
    docker logs ife-seat-42

**Why fast:** Image already cached locally, no download needed

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Write efficient Dockerfile (minimize layers)
- [ ] Use multi-stage builds for small images
- [ ] Run containers as non-root user
- [ ] Apply read-only filesystem
- [ ] Drop unnecessary capabilities
- [ ] Set resource limits (CPU, memory, I/O)
- [ ] Use seccomp profiles
- [ ] Enable AppArmor/SELinux
- [ ] Implement health checks
- [ ] Use Docker Compose for multi-container apps
- [ ] Test A/B deployment strategy
- [ ] Practice fast rollback
- [ ] Scan images for vulnerabilities
- [ ] Document airline-specific customizations

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Containers are NOT VMs** → Share kernel, lighter, start in <1 second

2️⃣ **Multi-stage builds reduce size** → Exclude build tools from final image 
(800 MB → 20 MB)

3️⃣ **Always run as non-root** → Security best practice, prevents privilege 
escalation

4️⃣ **Read-only filesystem prevents tampering** → Immutable runtime, use tmpfs 
for temp files

5️⃣ **Resource limits prevent resource exhaustion** → --memory, --cpus protect 
other containers

6️⃣ **A/B testing enables safe rollouts** → Deploy to 10% of seats first

7️⃣ **containerd is Kubernetes standard** → Lighter than Docker, production-ready

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **CONTAINER TECHNOLOGY COMPLETE**
**Created:** January 14, 2026
**Coverage:** Docker, Security Hardening, Resource Limits, containerd, Aviation Use Cases

════════════════════════════════════════════════════════════════════
