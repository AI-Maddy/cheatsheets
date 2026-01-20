═══════════════════════════════════════════════════════════════════════
VIRTUALIZATION & CONTAINERS FOR IN-FLIGHT ENTERTAINMENT SYSTEMS
═══════════════════════════════════════════════════════════════════════

**Comprehensive Guide to Containerization and Virtualization in IFE**  
**Domain:** Avionics IFE Systems 🛫 | Embedded Linux 🐧 | Platform Architecture  
**Purpose:** LXC, Docker, Kubernetes for In-Flight Entertainment platforms

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Containerization** enables isolated, resource-controlled execution environments for IFE services without full VM overhead.

**Key Technologies:**
- **LXC:** Lightweight OS-level virtualization (process/network isolation)
- **Docker:** Application containerization (portable, immutable deployments)
- **Kubernetes (K3s):** Container orchestration (scaling, load balancing)
- **Use Cases:** Per-seat isolation, video streaming, content delivery, passenger apps

**IFE Architecture Pattern:**
```
Head-End Server (Linux) → [Content | Video | Audio | Games] Containers
         ↓ Cabin Network (Ethernet/AFDX Part 10)
   [Seat 1A] [Seat 1B] ... [Seat 9F] ← LXC Containers per seat
```

═══════════════════════════════════════════════════════════════════════

🏗️ **1. CONTAINERIZATION FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**1.1 Container vs VM vs Bare Metal**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Comparison Table:**

+-------------------+------------------+------------------+------------------+
| **Aspect**        | **Bare Metal**   | **Virtual Machine** | **Container**   |
+===================+==================+==================+==================+
| **Isolation**     | None (processes) | Full (hypervisor)| OS-level (cgroups)|
| **Boot Time**     | Seconds          | Minutes          | Milliseconds     |
| **Resource**      | Native           | 5-15% overhead   | 1-3% overhead    |
| **Overhead**      |                  |                  |                  |
| **Memory**        | Direct access    | Allocated (fixed)| Shared kernel    |
| **Portability**   | Hardware-bound   | Image-based      | Image-based      |
| **Use Case**      | Maximum perf     | Different OS     | Same OS, isolated|
+-------------------+------------------+------------------+------------------+

**IFE Application:**
- **Bare Metal:** Legacy single-function IFE systems
- **VMs:** Running Windows/QNX alongside Linux
- **Containers:** Modern microservices architecture (video, audio, games isolated)

**1.2 Linux Kernel Features for Containers**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Core Technologies:**

.. code-block:: text

   ┌──────────────────────────────────────────────┐
   │         Linux Kernel Features                │
   ├──────────────────────────────────────────────┤
   │ 1. Namespaces → Process/Network Isolation    │
   │ 2. cgroups → Resource Limiting (CPU/Memory)  │
   │ 3. Capabilities → Fine-grained Privileges    │
   │ 4. Seccomp → Syscall Filtering               │
   │ 5. SELinux/AppArmor → MAC Security           │
   └──────────────────────────────────────────────┘

**Namespaces (7 Types):**

+-------------------+---------------------------------------+---------------------------+
| **Namespace**     | **Isolation**                         | **IFE Use Case**          |
+===================+=======================================+===========================+
| **PID**           | Process IDs (separate process trees)  | Seat app isolation        |
| **NET**           | Network stack (interfaces, routing)   | Per-seat network config   |
| **MNT**           | Filesystem mount points               | Separate content views    |
| **UTS**           | Hostname and domain name              | Seat identification       |
| **IPC**           | Inter-process communication           | Prevent cross-seat comm   |
| **USER**          | User and group IDs                    | Passenger privilege sep   |
| **CGROUP**        | Cgroup hierarchy view                 | Resource limit isolation  |
+-------------------+---------------------------------------+---------------------------+

**cgroups v2 Example:**

.. code-block:: bash

   # Create cgroup for seat 1A video service
   mkdir /sys/fs/cgroup/seat1a_video
   
   # Limit CPU to 50% (500000µs per 1000000µs period)
   echo 500000 > /sys/fs/cgroup/seat1a_video/cpu.max
   
   # Limit memory to 256MB
   echo 268435456 > /sys/fs/cgroup/seat1a_video/memory.max
   
   # Add video player process
   echo $PID > /sys/fs/cgroup/seat1a_video/cgroup.procs

═══════════════════════════════════════════════════════════════════════

🐧 **2. LXC (LINUX CONTAINERS)**
─────────────────────────────────────────────────────────────────────────

**2.1 LXC Overview**
~~~~~~~~~~~~~~~~~~~~

**What is LXC?**
- OS-level virtualization (system containers, not application containers)
- Runs full Linux init system (systemd, OpenRC)
- Closer to lightweight VMs than Docker containers
- Direct kernel feature usage (namespaces, cgroups)

**LXC vs Docker:**

+-----------------------+-------------------------+-------------------------+
| **Feature**           | **LXC**                 | **Docker**              |
+=======================+=========================+=========================+
| **Abstraction**       | System container        | Application container   |
| **Init System**       | Yes (systemd/OpenRC)    | No (single process)     |
| **Image Format**      | Templates/rootfs        | Layered images (OCI)    |
| **Networking**        | Bridge, macvlan         | Bridge, overlay         |
| **Use Case**          | Full OS environment     | Microservices           |
| **Startup Time**      | 2-5 seconds             | <100ms                  |
| **IFE Application**   | Per-seat OS instances   | Individual services     |
+-----------------------+-------------------------+-------------------------+

**2.2 LXC Installation and Configuration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Installation:**

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install lxc lxc-templates
   
   # Enable unprivileged containers
   sudo usermod -aG lxc $USER
   echo "$USER veth lxcbr0 10" | sudo tee -a /etc/lxc/lxc-usernet
   
   # Check configuration
   lxc-checkconfig

**Create First Container:**

.. code-block:: bash

   # Create Ubuntu container for IFE seat
   sudo lxc-create -n seat-1a -t ubuntu -- -r jammy
   
   # Start container
   sudo lxc-start -n seat-1a
   
   # Attach to container
   sudo lxc-attach -n seat-1a
   
   # Check status
   lxc-ls -f

**Output:**
```
NAME    STATE   IPV4        IPV6  AUTOSTART
seat-1a RUNNING 10.0.3.100  -     NO
```

**2.3 LXC Configuration for IFE Seats**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**IFE Seat Container Config:** ``/var/lib/lxc/seat-1a/config``

.. code-block:: bash

   # Container identity
   lxc.utsname = seat-1a
   lxc.arch = x86_64
   
   # Root filesystem
   lxc.rootfs.path = dir:/var/lib/lxc/seat-1a/rootfs
   
   # Resource limits (256MB RAM, 1 CPU core)
   lxc.cgroup2.memory.max = 268435456
   lxc.cgroup2.cpu.max = 100000 100000
   
   # Network configuration (dedicated VLAN for seats)
   lxc.net.0.type = veth
   lxc.net.0.flags = up
   lxc.net.0.link = lxcbr0
   lxc.net.0.ipv4.address = 10.10.1.10/24
   lxc.net.0.ipv4.gateway = 10.10.1.1
   
   # Mount shared content library (read-only)
   lxc.mount.entry = /ife/content opt/content none bind,ro 0 0
   
   # Security: Drop dangerous capabilities
   lxc.cap.drop = sys_module sys_admin
   
   # Auto-start on boot
   lxc.start.auto = 1
   lxc.start.delay = 5

**2.4 IFE Seat Management Script**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # ife-seat-manager.sh - Manage IFE seat containers
   
   SEAT_PREFIX="seat-"
   ROWS=30
   COLS="ABCDEF"
   
   # Create all seat containers
   create_all_seats() {
       for row in $(seq 1 $ROWS); do
           for col in $(echo $COLS | grep -o .); do
               SEAT="${SEAT_PREFIX}${row}${col}"
               IP_LAST=$(printf "%d" "'$col")
               IP="10.10.${row}.${IP_LAST}"
               
               echo "Creating $SEAT with IP $IP..."
               lxc-copy -n seat-template -N $SEAT
               
               # Update IP address
               sed -i "s/10.10.1.10/${IP}/" /var/lib/lxc/$SEAT/config
               
               lxc-start -n $SEAT
           done
       done
   }
   
   # Monitor all seats
   monitor_seats() {
       lxc-ls -f | grep "^${SEAT_PREFIX}"
   }
   
   # Update content across all seats
   update_content() {
       local CONTENT_VERSION=$1
       for seat in $(lxc-ls | grep "^${SEAT_PREFIX}"); do
           echo "Updating $seat to content version $CONTENT_VERSION..."
           lxc-attach -n $seat -- /opt/scripts/update-content.sh $CONTENT_VERSION
       done
   }
   
   # Restart failed seats
   restart_failed() {
       for seat in $(lxc-ls -f | grep STOPPED | awk '{print $1}'); do
           echo "Restarting $seat..."
           lxc-start -n $seat
       done
   }
   
   case "$1" in
       create) create_all_seats ;;
       monitor) monitor_seats ;;
       update) update_content "$2" ;;
       restart) restart_failed ;;
       *) echo "Usage: $0 {create|monitor|update|restart}" ;;
   esac

**Usage:**

.. code-block:: bash

   # Create all 180 seat containers (30 rows × 6 columns)
   sudo ./ife-seat-manager.sh create
   
   # Monitor seat status
   sudo ./ife-seat-manager.sh monitor
   
   # Update content to version 2024.12
   sudo ./ife-seat-manager.sh update 2024.12

═══════════════════════════════════════════════════════════════════════

🐳 **3. DOCKER FOR EMBEDDED IFE**
─────────────────────────────────────────────────────────────────────────

**3.1 Docker Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Components:**

.. code-block:: text

   ┌───────────────────────────────────────────┐
   │         Docker Architecture               │
   ├───────────────────────────────────────────┤
   │  Client (docker CLI)                      │
   │      ↓ REST API                           │
   │  Docker Daemon (dockerd)                  │
   │      ↓ containerd API                     │
   │  containerd (container runtime)           │
   │      ↓ runc                               │
   │  Container (isolated process)             │
   └───────────────────────────────────────────┘

**Docker vs LXC for IFE:**

**Use Docker when:**
- Running single-purpose services (video encoder, game server)
- Need portability across hardware platforms
- Microservices architecture (head-end server)
- Frequent updates and deployments

**Use LXC when:**
- Need full OS environment per seat
- Running multiple services in one container
- Legacy applications requiring systemd
- Tighter resource control

**3.2 Docker Installation for Embedded**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install Docker on embedded Linux
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Configure for embedded (limit logs, use overlay2)
   sudo tee /etc/docker/daemon.json << EOF
   {
     "storage-driver": "overlay2",
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "10m",
       "max-file": "3"
     },
     "live-restore": true,
     "default-ulimits": {
       "nofile": {
         "Name": "nofile",
         "Hard": 64000,
         "Soft": 64000
       }
     }
   }
   EOF
   
   sudo systemctl restart docker

**3.3 IFE Video Streaming Service (Dockerfile)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Dockerfile for Video Service:**

.. code-block:: dockerfile

   # Multi-stage build for size optimization
   FROM ubuntu:22.04 AS builder
   
   # Install build dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       libavcodec-dev \
       libavformat-dev \
       libswscale-dev \
       git
   
   # Build custom video streamer
   WORKDIR /build
   COPY src/ .
   RUN make video-streamer
   
   # Runtime image (much smaller)
   FROM ubuntu:22.04
   
   # Install only runtime libraries
   RUN apt-get update && apt-get install -y \
       libavcodec58 \
       libavformat58 \
       libswscale5 \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy binary from builder
   COPY --from=builder /build/video-streamer /usr/local/bin/
   
   # Create non-root user
   RUN useradd -m -u 1000 ife && \
       mkdir -p /content && \
       chown -R ife:ife /content
   
   USER ife
   WORKDIR /content
   
   # Expose RTSP port
   EXPOSE 8554
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=3s \
     CMD curl -f http://localhost:8554/health || exit 1
   
   CMD ["video-streamer", "--port", "8554", "--content-dir", "/content"]

**Build and Run:**

.. code-block:: bash

   # Build image
   docker build -t ife-video-streamer:1.0 .
   
   # Run with resource limits
   docker run -d \
     --name seat-1a-video \
     --cpus="0.5" \
     --memory="256m" \
     --read-only \
     --tmpfs /tmp:rw,noexec,nosuid,size=64m \
     -v /ife/content:/content:ro \
     -p 8554:8554 \
     --restart=unless-stopped \
     ife-video-streamer:1.0

**3.4 Docker Compose for IFE Head-End**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**docker-compose.yml:**

.. code-block:: yaml

   version: '3.8'
   
   services:
     # Content Management Service
     content-manager:
       image: ife-content-mgr:1.0
       container_name: ife-content-mgr
       volumes:
         - /ife/content:/content
         - content-db:/var/lib/postgresql
       networks:
         - ife-backend
       environment:
         - DB_HOST=postgres
         - DB_NAME=ife_content
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
       restart: unless-stopped
   
     # Video Encoder Service (H.264/H.265)
     video-encoder:
       image: ife-video-encoder:1.0
       container_name: ife-encoder
       volumes:
         - /ife/content:/content
       devices:
         - /dev/video0:/dev/video0  # Hardware encoder
       networks:
         - ife-backend
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 1G
       restart: unless-stopped
   
     # RTSP Streaming Server
     rtsp-server:
       image: ife-rtsp-server:1.0
       container_name: ife-rtsp
       ports:
         - "8554:8554"
         - "8555:8555"
       volumes:
         - /ife/content:/content:ro
       networks:
         - ife-frontend
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 2G
       restart: unless-stopped
   
     # Game Server
     game-server:
       image: ife-games:1.0
       container_name: ife-games
       ports:
         - "9000-9010:9000-9010"
       networks:
         - ife-frontend
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
       restart: unless-stopped
   
     # PostgreSQL Database
     postgres:
       image: postgres:15-alpine
       container_name: ife-db
       volumes:
         - content-db:/var/lib/postgresql/data
       networks:
         - ife-backend
       environment:
         - POSTGRES_DB=ife_content
         - POSTGRES_USER=ife_admin
         - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
       secrets:
         - db_password
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
       restart: unless-stopped
   
   networks:
     ife-backend:
       driver: bridge
       ipam:
         config:
           - subnet: 172.20.0.0/24
     ife-frontend:
       driver: bridge
       ipam:
         config:
           - subnet: 172.21.0.0/24
   
   volumes:
     content-db:
   
   secrets:
     db_password:
       file: ./secrets/db_password.txt

**Deploy:**

.. code-block:: bash

   # Start all services
   docker-compose up -d
   
   # Check status
   docker-compose ps
   
   # View logs
   docker-compose logs -f rtsp-server
   
   # Scale RTSP servers for load balancing
   docker-compose up -d --scale rtsp-server=3

═══════════════════════════════════════════════════════════════════════

☸️ **4. KUBERNETES (K3s) FOR IFE**
─────────────────────────────────────────────────────────────────────────

**4.1 Why Kubernetes for IFE?**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Benefits:**
- **Auto-scaling:** Handle passenger load dynamically
- **Self-healing:** Restart failed services automatically
- **Load balancing:** Distribute video streams across servers
- **Rolling updates:** Zero-downtime content/firmware updates
- **Service discovery:** Automatic endpoint management

**K3s vs K8s:**

+-----------------------+-------------------------+-------------------------+
| **Feature**           | **Kubernetes (K8s)**    | **K3s**                 |
+=======================+=========================+=========================+
| **Binary Size**       | ~1 GB                   | ~50 MB                  |
| **Memory Footprint**  | 2-4 GB                  | 512 MB                  |
| **Components**        | Many separate binaries  | Single binary           |
| **Storage**           | Requires external       | Built-in SQLite/etcd    |
| **Use Case**          | Cloud, data centers     | Edge, embedded, IoT     |
| **IFE Application**   | Ground servers          | Aircraft head-end       |
+-----------------------+-------------------------+-------------------------+

**4.2 K3s Installation on IFE Head-End**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install K3s (single-node cluster for aircraft)
   curl -sfL https://get.k3s.io | sh -s - \
     --write-kubeconfig-mode 644 \
     --disable traefik \
     --disable servicelb \
     --node-name ife-headend-1
   
   # Verify installation
   k3s kubectl get nodes
   
   # Configure kubectl
   export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
   kubectl get pods -A

**4.3 IFE Video Streaming Deployment**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**video-streamer-deployment.yaml:**

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: video-streamer
     namespace: ife-services
   spec:
     replicas: 3  # High availability
     selector:
       matchLabels:
         app: video-streamer
     template:
       metadata:
         labels:
           app: video-streamer
       spec:
         containers:
         - name: streamer
           image: ife-video-streamer:1.0
           ports:
           - containerPort: 8554
             name: rtsp
           resources:
             requests:
               cpu: "500m"
               memory: "256Mi"
             limits:
               cpu: "1000m"
               memory: "512Mi"
           volumeMounts:
           - name: content-storage
             mountPath: /content
             readOnly: true
           livenessProbe:
             httpGet:
               path: /health
               port: 8554
             initialDelaySeconds: 10
             periodSeconds: 30
           readinessProbe:
             httpGet:
               path: /ready
               port: 8554
             initialDelaySeconds: 5
             periodSeconds: 10
         volumes:
         - name: content-storage
           persistentVolumeClaim:
             claimName: ife-content-pvc
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: video-streamer-svc
     namespace: ife-services
   spec:
     selector:
       app: video-streamer
     ports:
     - port: 8554
       targetPort: 8554
       protocol: TCP
     type: LoadBalancer  # Distribute load across pods

**Deploy:**

.. code-block:: bash

   # Create namespace
   kubectl create namespace ife-services
   
   # Apply deployment
   kubectl apply -f video-streamer-deployment.yaml
   
   # Check status
   kubectl get pods -n ife-services
   kubectl get svc -n ife-services
   
   # Scale replicas
   kubectl scale deployment video-streamer --replicas=5 -n ife-services

**4.4 Horizontal Pod Autoscaler (HPA)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Autoscale based on CPU/memory:**

.. code-block:: yaml

   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: video-streamer-hpa
     namespace: ife-services
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: video-streamer
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
     - type: Resource
       resource:
         name: memory
         target:
           type: Utilization
           averageUtilization: 80
     behavior:
       scaleDown:
         stabilizationWindowSeconds: 300
         policies:
         - type: Percent
           value: 50
           periodSeconds: 60
       scaleUp:
         stabilizationWindowSeconds: 0
         policies:
         - type: Percent
           value: 100
           periodSeconds: 15

**Apply:**

.. code-block:: bash

   kubectl apply -f video-streamer-hpa.yaml
   
   # Monitor autoscaling
   kubectl get hpa -n ife-services -w

**4.5 ConfigMaps and Secrets for IFE**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**ConfigMap for IFE settings:**

.. code-block:: yaml

   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: ife-config
     namespace: ife-services
   data:
     content-library-path: "/ife/content"
     video-codec: "h265"
     audio-codec: "aac"
     max-bitrate: "8000"  # kbps
     seat-count: "180"
     language-default: "en"
     languages-available: "en,es,fr,de,ja,zh"

**Secret for database credentials:**

.. code-block:: bash

   # Create secret
   kubectl create secret generic ife-db-secret \
     --from-literal=username=ife_admin \
     --from-literal=password='SecureP@ssw0rd!' \
     -n ife-services
   
   # Use in deployment
   kubectl set env deployment/content-manager \
     --from=secret/ife-db-secret \
     -n ife-services

**4.6 Rolling Updates for Content**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Update container image:**

.. code-block:: bash

   # Build new image with updated content
   docker build -t ife-video-streamer:1.1 .
   
   # Update deployment (rolling update)
   kubectl set image deployment/video-streamer \
     streamer=ife-video-streamer:1.1 \
     -n ife-services
   
   # Monitor rollout
   kubectl rollout status deployment/video-streamer -n ife-services
   
   # Rollback if needed
   kubectl rollout undo deployment/video-streamer -n ife-services

═══════════════════════════════════════════════════════════════════════

🏗️ **5. IFE SYSTEM ARCHITECTURE WITH CONTAINERS**
─────────────────────────────────────────────────────────────────────────

**5.1 Complete IFE Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────────┐
   │              GROUND INFRASTRUCTURE                              │
   │  ┌──────────────┐      ┌──────────────┐                        │
   │  │ Content CMS  │─────▶│ Satellite    │                        │
   │  │ (Cloud K8s)  │      │ Uplink       │                        │
   │  └──────────────┘      └──────┬───────┘                        │
   └────────────────────────────────┼────────────────────────────────┘
                                    │ Satellite Link (Ku/Ka-band)
                                    ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │                    AIRCRAFT (In-Flight)                         │
   │  ┌───────────────────────────────────────────────────────────┐ │
   │  │           IFE Head-End Server (Linux + K3s)               │ │
   │  ├───────────────────────────────────────────────────────────┤ │
   │  │  Pod: Content Manager  │ Pod: Video Encoder               │ │
   │  │  - Content updates     │ - H.264/H.265 encoding           │ │
   │  │  - Metadata DB         │ - Live TV processing             │ │
   │  ├────────────────────────┼──────────────────────────────────┤ │
   │  │  Pod: RTSP Server      │ Pod: Game Server                 │ │
   │  │  - Stream routing      │ - Multiplayer games              │ │
   │  │  - Load balancing      │ - Leaderboards                   │ │
   │  └────────────┬───────────┴──────────────┬───────────────────┘ │
   │               │                          │                      │
   │               │  Cabin Ethernet Network (VLAN 100)             │
   │               │  IGMP Multicast for Video Streams              │
   │               │                                                 │
   │  ┌────────────┴──────────────────────────┴──────────────────┐ │
   │  │              Managed Ethernet Switch (AFDX Part 10)       │ │
   │  │  - VLAN isolation (Video: 100, WiFi: 200, Crew: 300)     │ │
   │  │  - QoS (video traffic priority)                           │ │
   │  │  - IGMP snooping (efficient multicast)                    │ │
   │  └─┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬─┘ │
   │    │    │    │    │    │    │    │    │    │    │    │    │   │
   │  ┌─▼──┐ │  ┌─▼──┐ │  ┌─▼──┐ │  ┌─▼──┐ │  ┌─▼──┐ │  ┌─▼──┐   │
   │  │1A  │ │  │1B  │ │  │2A  │...│9E  │ │  │9F  │ │  │WiFi│   │
   │  │LXC │ │  │LXC │ │  │LXC │ │ │LXC │ │  │LXC │ │  │AP  │   │
   │  └────┘ │  └────┘ │  └────┘ │ └────┘ │  └────┘ │  └────┘   │
   │  Display│  Display│  Display│ Display│  Display│  Passengers│
   └─────────┴─────────┴─────────┴────────┴─────────┴───────────────┘

**5.2 Resource Allocation Strategy**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Head-End Server Specs (Example: NXP i.MX 93 or Qualcomm SA8295P):**

+-------------------------+------------------+----------------------+
| **Component**           | **Resources**    | **Purpose**          |
+=========================+==================+======================+
| **Total CPU**           | 8 cores (A78AE)  | Heterogeneous SoC    |
| **Total Memory**        | 16 GB LPDDR5     | Content + streaming  |
| **Storage**             | 2 TB NVMe SSD    | Content library      |
+=========================+==================+======================+

**Pod Resource Allocation:**

.. code-block:: yaml

   # resource-quotas.yaml
   apiVersion: v1
   kind: ResourceQuota
   metadata:
     name: ife-quota
     namespace: ife-services
   spec:
     hard:
       requests.cpu: "6"       # Reserve 6 cores for IFE
       requests.memory: 12Gi   # Reserve 12GB RAM
       limits.cpu: "7"         # Max 7 cores
       limits.memory: 14Gi     # Max 14GB RAM
       persistentvolumeclaims: "5"
       services.loadbalancers: "3"

**Per-Seat Resource Limits (LXC):**

.. code-block:: bash

   # Each seat gets limited resources
   CPU: 5% of one core (50ms per 1000ms)
   Memory: 128 MB
   Network: 10 Mbps (HD video stream)
   
   # Example for 180 seats:
   Total CPU: 180 × 5% = 9 cores equivalent (spread across 8 physical cores)
   Total Memory: 180 × 128MB = 23 GB (requires careful management)

**5.3 Network Segmentation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**VLAN Configuration:**

.. code-block:: text

   VLAN 10:  Flight Control (AFDX Part 7) - Isolated
   VLAN 20:  Navigation Systems - Isolated
   ─────────────────────────────────────────────────────
   VLAN 100: IFE Video Streaming (Multicast)
   VLAN 200: Passenger WiFi (Internet)
   VLAN 300: Crew Tablets (Controlled access)
   VLAN 400: Maintenance Systems (Secured)

**Linux Bridge Configuration:**

.. code-block:: bash

   # Create bridge for IFE network
   ip link add name br-ife type bridge
   ip link set br-ife up
   
   # Add VLAN interface
   ip link add link eth0 name eth0.100 type vlan id 100
   ip link set eth0.100 master br-ife
   ip link set eth0.100 up
   
   # Assign IP to bridge
   ip addr add 10.10.0.1/16 dev br-ife
   
   # Enable IGMP snooping for multicast efficiency
   echo 1 > /sys/class/net/br-ife/bridge/multicast_snooping

**5.4 Security Hardening**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Container Security Best Practices:**

.. code-block:: dockerfile

   # Dockerfile security hardening
   
   # 1. Use minimal base image
   FROM alpine:3.19
   
   # 2. Run as non-root user
   RUN adduser -D -u 1000 ife
   USER ife
   
   # 3. Read-only root filesystem
   # (Specify in docker run: --read-only)
   
   # 4. Drop all capabilities, add only needed
   # (Specify in docker run: --cap-drop=ALL --cap-add=NET_BIND_SERVICE)
   
   # 5. Use secrets for sensitive data
   # (Never hardcode passwords in images)

**AppArmor Profile for IFE Containers:**

.. code-block:: text

   # /etc/apparmor.d/docker-ife-video
   
   #include <tunables/global>
   
   profile docker-ife-video flags=(attach_disconnected,mediate_deleted) {
     #include <abstractions/base>
     
     # Allow network access
     network inet stream,
     network inet dgram,
     
     # Allow reading content
     /content/** r,
     
     # Deny dangerous syscalls
     deny /proc/sys/** w,
     deny /sys/** w,
     deny @{PROC}/sys/kernel/modprobe w,
     
     # Allow tmp writes
     /tmp/** rw,
   }

**Load profile:**

.. code-block:: bash

   # Load AppArmor profile
   sudo apparmor_parser -r /etc/apparmor.d/docker-ife-video
   
   # Run container with profile
   docker run --security-opt apparmor=docker-ife-video ife-video-streamer:1.0

═══════════════════════════════════════════════════════════════════════

⚡ **6. PERFORMANCE OPTIMIZATION**
─────────────────────────────────────────────────────────────────────────

**6.1 Container Performance Tuning**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Reduce Container Startup Time:**

.. code-block:: dockerfile

   # Multi-stage build to minimize image size
   FROM golang:1.21 AS builder
   WORKDIR /app
   COPY . .
   RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
   
   # Minimal runtime image
   FROM scratch
   COPY --from=builder /app/app /app
   ENTRYPOINT ["/app"]

**Result:** Image size reduced from 800MB to 15MB, startup time <50ms

**CPU Pinning for Real-Time Performance:**

.. code-block:: bash

   # Pin video encoder to cores 4-5 (isolated from OS)
   docker run -d \
     --cpuset-cpus="4-5" \
     --cpu-rt-runtime=950000 \
     ife-video-encoder:1.0

**6.2 Memory Optimization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Huge Pages for Large Memory Access:**

.. code-block:: bash

   # Enable huge pages (2MB pages instead of 4KB)
   echo 1024 > /proc/sys/vm/nr_hugepages
   
   # Mount huge pages
   mkdir -p /dev/hugepages
   mount -t hugetlbfs none /dev/hugepages
   
   # Run container with huge pages
   docker run -d \
     --shm-size=2g \
     --memory=4g \
     -v /dev/hugepages:/dev/hugepages \
     ife-content-cache:1.0

**6.3 Network Performance**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use SR-IOV for High-Performance Networking:**

.. code-block:: bash

   # Enable SR-IOV on NIC (creates virtual functions)
   echo 4 > /sys/class/net/eth0/device/sriov_numvfs
   
   # Assign VF to container (bypasses kernel network stack)
   docker run -d \
     --device=/dev/vfio/1 \
     --cap-add=NET_ADMIN \
     ife-rtsp-server:1.0

**Kernel Tuning for Streaming:**

.. code-block:: bash

   # Increase network buffers for high-throughput streaming
   sysctl -w net.core.rmem_max=134217728
   sysctl -w net.core.wmem_max=134217728
   sysctl -w net.ipv4.tcp_rmem="4096 87380 67108864"
   sysctl -w net.ipv4.tcp_wmem="4096 65536 67108864"
   
   # Enable TCP BBR congestion control (better for streaming)
   sysctl -w net.core.default_qdisc=fq
   sysctl -w net.ipv4.tcp_congestion_control=bbr

═══════════════════════════════════════════════════════════════════════

🛡️ **7. MONITORING AND DEBUGGING**
─────────────────────────────────────────────────────────────────────────

**7.1 Container Monitoring**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**cAdvisor (Container Advisor):**

.. code-block:: bash

   # Run cAdvisor for container metrics
   docker run -d \
     --name=cadvisor \
     --volume=/:/rootfs:ro \
     --volume=/var/run:/var/run:ro \
     --volume=/sys:/sys:ro \
     --volume=/var/lib/docker/:/var/lib/docker:ro \
     --publish=8080:8080 \
     --restart=always \
     gcr.io/cadvisor/cadvisor:latest
   
   # Access metrics: http://localhost:8080

**Prometheus + Grafana for IFE Metrics:**

.. code-block:: yaml

   # prometheus.yml
   global:
     scrape_interval: 15s
   
   scrape_configs:
     - job_name: 'ife-services'
       kubernetes_sd_configs:
         - role: pod
           namespaces:
             names:
               - ife-services
       relabel_configs:
         - source_labels: [__meta_kubernetes_pod_label_app]
           action: keep
           regex: video-streamer|game-server

**7.2 Debugging Containers**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Inspect Running Container:**

.. code-block:: bash

   # Enter running container
   docker exec -it seat-1a-video /bin/sh
   
   # Check process list
   docker top seat-1a-video
   
   # View resource usage
   docker stats seat-1a-video
   
   # Inspect container config
   docker inspect seat-1a-video | jq '.[0].HostConfig.Memory'

**LXC Debugging:**

.. code-block:: bash

   # Attach to container console
   lxc-attach -n seat-1a
   
   # View container logs
   lxc-console -n seat-1a
   
   # Check cgroup resource usage
   systemd-cgtop
   
   # Network troubleshooting
   lxc-attach -n seat-1a -- ip addr show
   lxc-attach -n seat-1a -- ping -c3 10.10.0.1

**Kubernetes Debugging:**

.. code-block:: bash

   # Get pod logs
   kubectl logs video-streamer-abc123 -n ife-services
   
   # Follow logs in real-time
   kubectl logs -f video-streamer-abc123 -n ife-services
   
   # Exec into pod
   kubectl exec -it video-streamer-abc123 -n ife-services -- /bin/sh
   
   # Port forward for local testing
   kubectl port-forward svc/video-streamer-svc 8554:8554 -n ife-services
   
   # Describe pod (events, status)
   kubectl describe pod video-streamer-abc123 -n ife-services

═══════════════════════════════════════════════════════════════════════

🎯 **8. INTERVIEW TALKING POINTS**
─────────────────────────────────────────────────────────────────────────

**8.1 Demonstrate Containerization Understanding**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Question: "How would you architect containerization for an IFE system?"**

**Answer Framework:**

1. **Head-End Server (K3s/Docker):**
   - "I'd use Kubernetes (K3s for embedded) on the head-end server to orchestrate microservices"
   - "Services: Content manager, video encoder, RTSP server, game server"
   - "Benefits: Auto-scaling during peak usage, self-healing, rolling updates"

2. **Seat Units (LXC):**
   - "For seat units, LXC provides lightweight OS-level isolation"
   - "Each seat runs in its own container with limited resources (128MB RAM, 5% CPU)"
   - "Shared read-only content library mounted to all seats"

3. **Networking:**
   - "VLAN segmentation: IFE (VLAN 100), WiFi (VLAN 200), Crew (VLAN 300)"
   - "IGMP multicast for efficient video streaming (no duplicate streams)"
   - "QoS prioritization for video traffic"

4. **Security:**
   - "AppArmor/SELinux profiles for container MAC"
   - "Drop dangerous capabilities (sys_admin, sys_module)"
   - "Read-only root filesystems with tmpfs for writable areas"

**8.2 Relate to Your Experience**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Connect Past Projects:**

1. **i.MX 93 Platform (Current Role):**
   - "At Universal Electronics, I developed secure boot and OTA updates for i.MX 93"
   - "Similar architecture could apply to IFE: A/B partitions, signed images, rollback"
   - "i.MX 93 experience directly transferable to IFE seat units"

2. **AFIRS SDU Platform (FLYHT):**
   - "Developed Linux-based satellite communication platform"
   - "Similar to IFE connectivity: Satcom downlink for content, network applications"
   - "Experience with hardware integration and aircraft interfaces"

3. **Flight Deck Video Displays (Boeing):**
   - "Implemented RTSP video streaming and H.264 codec integration"
   - "Optimized display pipeline for real-time performance"
   - "Directly applicable to IFE video streaming architecture"

**8.3 Address Gaps Proactively**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Question: "What's your experience with QNX?"**

**Answer:**
"While my hands-on QNX experience is limited, I have extensive RTOS background with MQX, ThreadX, and Integrity across multiple safety-critical avionics projects. I understand QNX's microkernel architecture and its advantages for mixed-criticality systems. In preparation for this role, I've studied QNX hypervisor architecture and how it integrates with Linux guests for IFE applications. Given my deep embedded systems experience, I'm confident I can quickly ramp up on QNX-specific development."

**Question: "Have you worked with Docker/Kubernetes in production?"**

**Answer:**
"My primary experience has been with bare-metal embedded Linux and custom virtualization solutions. However, I've recently studied containerization for IFE architectures and understand the benefits: lightweight isolation, microservices orchestration, and efficient resource utilization. I've experimented with Docker on development boards and see how K3s would fit perfectly in aircraft head-end servers. My experience optimizing embedded Linux systems for performance and resource constraints translates well to container environments."

**8.4 Ask Intelligent Questions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Demonstrate Domain Knowledge:**

1. "What SOCs are currently used in Panasonic's IFE platform? Are you using Qualcomm Snapdragon Ride or MediaTek solutions?"

2. "How is virtualization architected - are you running QNX hypervisor with Linux guests, or primarily Linux with containerization?"

3. "What's the typical content library size across the fleet, and how do you handle synchronization between aircraft?"

4. "For commissioning, how do you handle seat discovery and enumeration during aircraft power-up?"

5. "What's your OTA update strategy - incremental updates for content, A/B partitions for firmware?"

═══════════════════════════════════════════════════════════════════════

📚 **9. QUICK REFERENCE COMMANDS**
─────────────────────────────────────────────────────────────────────────

**LXC Commands:**

.. code-block:: bash

   # Container lifecycle
   lxc-create -n <name> -t <template>
   lxc-start -n <name>
   lxc-stop -n <name>
   lxc-destroy -n <name>
   
   # Management
   lxc-ls -f                        # List with details
   lxc-attach -n <name>             # Enter container
   lxc-console -n <name>            # Attach console
   lxc-info -n <name>               # Container info
   
   # Resource monitoring
   lxc-cgroup -n <name> memory.usage_in_bytes
   lxc-cgroup -n <name> cpu.stat

**Docker Commands:**

.. code-block:: bash

   # Image management
   docker build -t <image>:<tag> .
   docker images
   docker rmi <image>
   
   # Container lifecycle
   docker run -d --name <name> <image>
   docker start/stop/restart <name>
   docker rm <name>
   
   # Inspection
   docker ps -a
   docker logs <name>
   docker exec -it <name> /bin/sh
   docker stats
   docker inspect <name>
   
   # Cleanup
   docker system prune -a          # Remove unused data
   docker volume prune             # Remove unused volumes

**Kubernetes (kubectl) Commands:**

.. code-block:: bash

   # Pod management
   kubectl get pods -n <namespace>
   kubectl describe pod <pod> -n <namespace>
   kubectl logs <pod> -n <namespace>
   kubectl exec -it <pod> -n <namespace> -- /bin/sh
   
   # Deployments
   kubectl apply -f <file.yaml>
   kubectl scale deployment <name> --replicas=5
   kubectl rollout status deployment/<name>
   kubectl rollout undo deployment/<name>
   
   # Services
   kubectl get svc -n <namespace>
   kubectl port-forward svc/<service> 8080:80
   
   # Resource usage
   kubectl top pods -n <namespace>
   kubectl top nodes

═══════════════════════════════════════════════════════════════════════

✅ **KEY TAKEAWAYS**
─────────────────────────────────────────────────────────────────────────

**Containerization for IFE:**

1. ✅ **LXC** for per-seat OS-level isolation (lightweight, full init system)
2. ✅ **Docker** for microservices (video encoder, RTSP server, games)
3. ✅ **K3s** for orchestration (auto-scaling, self-healing, rolling updates)
4. ✅ **VLAN segmentation** for network isolation (safety vs passenger systems)
5. ✅ **Resource limits** via cgroups (prevent seat from hogging resources)
6. ✅ **Security hardening** (AppArmor, capabilities, read-only root)
7. ✅ **IGMP multicast** for efficient video distribution (no duplicate streams)
8. ✅ **Monitoring** with Prometheus/Grafana for real-time metrics

**Architecture Pattern:**
```
K3s Head-End Server → Microservices (Docker)
           ↓ Cabin Ethernet (VLAN 100)
  LXC Seat Containers (1A-9F) → Isolated passengers
```

**Interview Success Formula:**
- Lead with **Linux/ARM expertise** (proven with i.MX 93, DaVinci)
- Demonstrate **avionics knowledge** (AFIRS, FDVD, safety-critical)
- Show **container understanding** (LXC, Docker, K3s concepts)
- Address **QNX gap** with "RTOS background + ready to learn"
- Ask **intelligent questions** about SOC selection, architecture

═══════════════════════════════════════════════════════════════════════

**References:**

- LXC Documentation: https://linuxcontainers.org/lxc/
- Docker Documentation: https://docs.docker.com/
- K3s Documentation: https://docs.k3s.io/
- Kubernetes Documentation: https://kubernetes.io/docs/
- ARINC 664 (AFDX): Avionics Full-Duplex Switched Ethernet
- Container Networking: CNI (Container Network Interface)

**Last Updated:** January 2026 | **Compatibility:** Linux 5.15+, Docker 24+, K3s 1.28+

═══════════════════════════════════════════════════════════════════════
