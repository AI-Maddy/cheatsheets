☁️ **Cloud-Native Architecture for Aircraft Systems**
══════════════════════════════════════════════════════

**Last Updated:** January 2026  
**Target Role:** Aircraft Services Architect  
**Relevance:** Kubernetes/containers replacing hypervisors in modern IFE systems

════════════════════════════════════════════════════════════════════

📋 **TABLE OF CONTENTS**
────────────────────────

1. Overview & Context
2. Why Cloud-Native for Aircraft?
3. Kubernetes Variants (K3s, K8s, OpenShift)
4. Container Orchestration Fundamentals
5. Microservices Architecture for IFE
6. Service Mesh (Istio, Linkerd)
7. Storage & Persistence
8. Security & Isolation
9. CI/CD Pipelines
10. Monitoring & Observability
11. Practical Examples
12. Common Pitfalls
13. Quick Reference Card
14. Exam Questions
15. Further Reading

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — Quick Takeaways**
──────────────────────────────

✅ **K3s** (lightweight Kubernetes) for aircraft edge computing (<512 MB RAM vs. 4 GB for K8s)  
✅ **Containers** (Docker, Podman) replace VMs for faster startup (<5s vs. ~60s)  
✅ **Microservices** decompose IFE monoliths (video, audio, UI, backend services)  
✅ **Helm charts** for repeatable deployments across aircraft fleets  
✅ **Service mesh** (Istio) provides mTLS, traffic shaping, zero-trust networking  
✅ **Auto-scaling** based on passenger load (30 vs. 300 passengers = 10x resource difference)  
✅ **Edge-optimized** storage (local PVC with ReadWriteOnce, no cloud NFS)

════════════════════════════════════════════════════════════════════

🏢 **1. OVERVIEW & CONTEXT**
────────────────────────────

**Traditional vs. Cloud-Native**

+--------------------------------+--------------------------------+
| Legacy IFE (Pre-2020)          | Cloud-Native IFE (2024+)       |
+================================+================================+
| Monolithic C++ application     | Microservices (Go, Java, C++)  |
| Single-server deployment       | Container orchestration (K3s)  |
| Manual updates (USB stick)     | OTA with Helm/ArgoCD           |
| No horizontal scaling          | Auto-scale based on load       |
| Fixed resource allocation      | Dynamic resource limits (QoS)  |
| Proprietary OS (VxWorks)       | Linux + Kubernetes             |
+--------------------------------+--------------------------------+

**Aircraft-Specific Constraints:**

🛑 **No Internet Access** (in-flight):
   - Air-gapped container registry (Harbor)
   - Pre-loaded images on aircraft storage
   
🔋 **Power Budget** (typically 500W for IFE):
   - Idle pods must suspend (CPU throttling)
   
📡 **Satellite Bandwidth** (~10 Mbps shared):
   - OTA updates during ground connection only

════════════════════════════════════════════════════════════════════

☁️ **2. WHY CLOUD-NATIVE FOR AIRCRAFT?**
────────────────────────────────────────

**Benefits:**

1. **Resource Efficiency**
   - Containers share kernel (no hypervisor overhead)
   - Bin-packing: 20 containers on 1 server vs. 5 VMs
   
2. **Rapid Updates**
   - Blue-green deployments (zero downtime)
   - Rollback in <30 seconds
   
3. **Developer Productivity**
   - Standardized Docker images (dev = prod)
   - CI/CD integration (GitLab, GitHub Actions)
   
4. **Vendor Independence**
   - CNCF standards (not locked to AWS/Azure)
   - Multi-vendor hardware support

**Challenges:**

❌ **Complexity** (Kubernetes learning curve)  
❌ **Debugging** (logs across 50+ containers)  
❌ **Security** (container escape risks)  
❌ **Certification** (DO-178C not written for containers)

════════════════════════════════════════════════════════════════════

🏗️ **3. KUBERNETES VARIANTS**
──────────────────────────────

**K3s (Recommended for Aircraft)**

- **Lightweight:** 512 MB RAM, 200 MB binary (vs. 4 GB for K8s)
- **Single-node** or **multi-node** (HA with 3 masters)
- **Edge-optimized:** No cloud dependencies (etcd → SQLite)
- **Built-in Helm controller** (no separate Tiller)

.. code-block:: bash

   # Install K3s (aircraft master node)
   curl -sfL https://get.k3s.io | sh -
   
   # Check status
   kubectl get nodes

**K8s (Standard Kubernetes)**

- Full-featured distribution
- **Heavy:** 4 GB RAM minimum
- Requires external etcd cluster
- Best for ground data centers

**OpenShift (Red Hat)**

- Enterprise-grade (built on K8s)
- Integrated CI/CD (Tekton pipelines)
- **Expensive licensing** (~$100K/year per cluster)

**Comparison Table:**

+----------------+--------+-------+-----------+------------------+
| Feature        | K3s    | K8s   | OpenShift | Aircraft Fit     |
+================+========+=======+===========+==================+
| RAM footprint  | 512 MB | 4 GB  | 8 GB      | ✅ K3s wins      |
| Startup time   | <30s   | ~2min | ~5min     | ✅ K3s wins      |
| Security       | Basic  | RBAC  | RBAC+SEL  | ⚠️ Add Istio     |
| Certification  | None   | None  | None      | ❌ All need docs |
+----------------+--------+-------+-----------+------------------+

════════════════════════════════════════════════════════════════════

🎛️ **4. CONTAINER ORCHESTRATION FUNDAMENTALS**
────────────────────────────────────────────────

**Core Concepts:**

📦 **Pod:**
   - Smallest deployable unit (1+ containers)
   - Shared network namespace (localhost communication)
   - Example: IFE UI (nginx) + API sidecar

🔄 **Deployment:**
   - Manages replica sets (desired state = 3 replicas)
   - Rolling updates (maxUnavailable: 1, maxSurge: 1)

🌐 **Service:**
   - Stable IP/DNS for pod groups
   - Load balancing (round-robin by default)
   - Types: ClusterIP, NodePort, LoadBalancer

🗂️ **ConfigMap & Secret:**
   - Configuration decoupled from code
   - Secrets base64-encoded (not encrypted by default!)

**Example Deployment:**

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ife-video-service
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: video
     template:
       metadata:
         labels:
           app: video
       spec:
         containers:
         - name: video-server
           image: harbor.aircraft.local/ife/video:v2.3
           ports:
           - containerPort: 8080
           resources:
             requests:
               memory: "256Mi"
               cpu: "500m"
             limits:
               memory: "512Mi"
               cpu: "1000m"
           env:
           - name: DB_HOST
             valueFrom:
               configMapKeyRef:
                 name: ife-config
                 key: database_host

════════════════════════════════════════════════════════════════════

🔀 **5. MICROSERVICES ARCHITECTURE FOR IFE**
────────────────────────────────────────────

**Service Decomposition:**

::

   ┌─────────────────────────────────────────────────────────┐
   │                  API Gateway (Kong)                     │
   │             (Authentication, Rate Limiting)             │
   └───────────────────────────┬─────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
   ┌───────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐
   │ Video Service│   │  Audio Service  │  │ UI Service  │
   │   (Go, gRPC) │   │ (C++, REST API) │  │ (React+Nginx│
   └──────┬───────┘   └────────┬────────┘  └──────┬──────┘
          │                    │                   │
          └──────────┬─────────┴───────────────────┘
                     │
            ┌────────▼─────────┐
            │  Metadata DB     │
            │  (MySQL Cluster) │
            └──────────────────┘

**Service Responsibilities:**

1. **Video Service** (port 8080):
   - Streams movies (H.265 codec)
   - Adaptive bitrate (4K → 720p on congestion)
   
2. **Audio Service** (port 8081):
   - Music library, podcasts
   - Low-latency audio sync
   
3. **UI Service** (port 80):
   - Web frontend (HTML5, CSS, JS)
   - Touch interface for seat screens
   
4. **Auth Service** (port 8082):
   - Passenger ID validation
   - Session management

**Inter-Service Communication:**

.. code-block:: yaml

   # Service mesh traffic routing (Istio)
   apiVersion: networking.istio.io/v1alpha3
   kind: VirtualService
   metadata:
     name: video-routing
   spec:
     hosts:
     - video-service
     http:
     - match:
       - headers:
           x-passenger-tier:
             exact: premium
       route:
       - destination:
           host: video-service
           subset: 4k-streams
     - route:
       - destination:
           host: video-service
           subset: standard

════════════════════════════════════════════════════════════════════

🕸️ **6. SERVICE MESH (ISTIO, LINKERD)**
────────────────────────────────────────

**What is a Service Mesh?**

- **Sidecar proxies** (Envoy) injected into every pod
- Handles: mTLS, retries, circuit breaking, observability
- **Zero code changes** (network layer magic)

**Istio Architecture:**

::

   ┌─────────────────────────────────────────────┐
   │              Control Plane                  │
   │  (Istiod: Pilot, Citadel, Galley)           │
   └───────────────────┬─────────────────────────┘
                       │ (config push)
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐    ┌────▼────┐   ┌────▼────┐
   │ Pod A   │    │ Pod B   │   │ Pod C   │
   │ ┌─────┐ │    │ ┌─────┐ │   │ ┌─────┐ │
   │ │ App │ │    │ │ App │ │   │ │ App │ │
   │ └──┬──┘ │    │ └──┬──┘ │   │ └──┬──┘ │
   │ ┌──▼──┐ │    │ ┌──▼──┐ │   │ ┌──▼──┐ │
   │ │Envoy│ │◄───┼─┤Envoy│─┼──►│ │Envoy│ │
   │ └─────┘ │    │ └─────┘ │   │ └─────┘ │
   └─────────┘    └─────────┘   └─────────┘

**Benefits:**

✅ **Mutual TLS** (automatic certificate rotation)  
✅ **Traffic shifting** (A/B testing, canary releases)  
✅ **Fault injection** (test resilience)  
✅ **Distributed tracing** (Jaeger integration)

**Example: Circuit Breaker**

.. code-block:: yaml

   apiVersion: networking.istio.io/v1alpha3
   kind: DestinationRule
   metadata:
     name: video-circuit-breaker
   spec:
     host: video-service
     trafficPolicy:
       connectionPool:
         tcp:
           maxConnections: 100
         http:
           http1MaxPendingRequests: 10
           maxRequestsPerConnection: 2
       outlierDetection:
         consecutiveErrors: 5
         interval: 30s
         baseEjectionTime: 30s
         maxEjectionPercent: 50

════════════════════════════════════════════════════════════════════

💾 **7. STORAGE & PERSISTENCE**
────────────────────────────────

**Storage Classes:**

1. **Local PV** (fastest, not portable):
   - SSD/NVMe on aircraft server
   - ReadWriteOnce (single-node access)
   
2. **NFS** (not recommended for aircraft):
   - Requires network, adds latency
   
3. **Rook-Ceph** (distributed storage):
   - Replicates data across nodes (HA)
   - Overhead: ~20% of raw capacity

**Persistent Volume Claim (PVC):**

.. code-block:: yaml

   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: ife-media-storage
   spec:
     accessModes:
     - ReadWriteOnce
     storageClassName: local-ssd
     resources:
       requests:
         storage: 2Ti  # 2TB for movie library

**StatefulSets (For Databases):**

.. code-block:: yaml

   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: mysql-cluster
   spec:
     serviceName: mysql
     replicas: 3
     selector:
       matchLabels:
         app: mysql
     template:
       metadata:
         labels:
           app: mysql
       spec:
         containers:
         - name: mysql
           image: mysql:8.0
           ports:
           - containerPort: 3306
           volumeMounts:
           - name: data
             mountPath: /var/lib/mysql
     volumeClaimTemplates:
     - metadata:
         name: data
       spec:
         accessModes: ["ReadWriteOnce"]
         resources:
           requests:
             storage: 100Gi

════════════════════════════════════════════════════════════════════

🔒 **8. SECURITY & ISOLATION**
───────────────────────────────

**Network Policies (Zero Trust):**

.. code-block:: yaml

   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: isolate-passenger-services
   spec:
     podSelector:
       matchLabels:
         tier: passenger
     policyTypes:
     - Ingress
     - Egress
     ingress:
     - from:
       - podSelector:
           matchLabels:
             tier: passenger
     egress:
     - to:
       - podSelector:
           matchLabels:
             tier: database
       ports:
       - protocol: TCP
         port: 3306

**Pod Security Standards:**

.. code-block:: yaml

   # Restrict privileged containers
   apiVersion: v1
   kind: Pod
   metadata:
     name: secure-ife-pod
   spec:
     securityContext:
       runAsNonRoot: true
       runAsUser: 1000
       fsGroup: 2000
     containers:
     - name: app
       securityContext:
         allowPrivilegeEscalation: false
         readOnlyRootFilesystem: true
         capabilities:
           drop:
           - ALL

**Image Scanning (Trivy):**

.. code-block:: bash

   # Scan for vulnerabilities
   trivy image harbor.aircraft.local/ife/video:v2.3
   
   # Output: HIGH: 0, MEDIUM: 2, LOW: 15

════════════════════════════════════════════════════════════════════

🔄 **9. CI/CD PIPELINES**
──────────────────────────

**GitOps with ArgoCD:**

::

   Developer Push    Git Repo      ArgoCD        Kubernetes
   ─────────────────────────────────────────────────────────
   git push origin   ┌─────────┐   ┌─────────┐   ┌─────────┐
   main              │ GitLab  │──►│ ArgoCD  │──►│ K3s     │
                     │         │   │ (Sync)  │   │ Cluster │
                     └─────────┘   └─────────┘   └─────────┘

**Example GitLab CI/CD Pipeline:**

.. code-block:: yaml

   # .gitlab-ci.yml
   stages:
     - build
     - test
     - deploy
   
   build-image:
     stage: build
     script:
       - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
       - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
   
   unit-tests:
     stage: test
     script:
       - go test ./...
   
   deploy-staging:
     stage: deploy
     script:
       - kubectl config use-context staging-cluster
       - helm upgrade --install ife-app ./helm-chart \
           --set image.tag=$CI_COMMIT_SHA
     only:
       - main

**Helm Chart Structure:**

::

   helm-chart/
   ├── Chart.yaml
   ├── values.yaml
   ├── templates/
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   └── ingress.yaml

════════════════════════════════════════════════════════════════════

📊 **10. MONITORING & OBSERVABILITY**
──────────────────────────────────────

**Stack: Prometheus + Grafana + Loki**

1. **Prometheus** (metrics):
   - Scrapes `/metrics` endpoints
   - CPU, memory, request latency
   
2. **Grafana** (dashboards):
   - Visualizes metrics, alerts
   
3. **Loki** (logs):
   - Aggregates logs from all pods

**Example Prometheus Query:**

.. code-block:: promql

   # Average request latency (last 5 min)
   rate(http_request_duration_seconds_sum[5m]) /
   rate(http_request_duration_seconds_count[5m])

**Distributed Tracing (Jaeger):**

.. code-block:: go

   // Instrument Go service
   import "github.com/opentracing/opentracing-go"
   
   span := opentracing.StartSpan("video-fetch")
   defer span.Finish()
   
   // Trace ID propagates across services
   // View end-to-end latency in Jaeger UI

════════════════════════════════════════════════════════════════════

💻 **11. PRACTICAL EXAMPLES**
──────────────────────────────

**Example 1: Deploy IFE App with Helm**

.. code-block:: bash

   # Add Helm repo (ground network)
   helm repo add ife-charts https://charts.aircraft.local
   
   # Install app
   helm install ife-app ife-charts/video-service \
     --set replicas=5 \
     --set image.tag=v3.1.0 \
     --set resources.limits.memory=1Gi
   
   # Check status
   kubectl get pods -l app=video-service

**Example 2: Auto-Scaling Based on Passenger Load**

.. code-block:: yaml

   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: ife-autoscaler
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: ife-video-service
     minReplicas: 2
     maxReplicas: 20
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70

**Example 3: Blue-Green Deployment**

.. code-block:: bash

   # Deploy new version (green)
   kubectl apply -f deployment-green.yaml
   
   # Test green environment
   kubectl port-forward svc/ife-green 8080:80
   curl http://localhost:8080/health
   
   # Switch traffic (update service selector)
   kubectl patch service ife-app -p '{"spec":{"selector":{"version":"green"}}}'
   
   # Rollback if needed
   kubectl patch service ife-app -p '{"spec":{"selector":{"version":"blue"}}}'

════════════════════════════════════════════════════════════════════

⚠️ **12. COMMON PITFALLS**
───────────────────────────

❌ **Pitfall 1: No Resource Limits**
   - **Problem:** One pod consumes all CPU (noisy neighbor)
   - **Solution:** Always set `requests` and `limits`

❌ **Pitfall 2: Using `latest` Tag**
   - **Problem:** Non-deterministic deployments (which version is running?)
   - **Solution:** Use semantic versioning (e.g., `v2.3.1`)

❌ **Pitfall 3: Storing Secrets in ConfigMaps**
   - **Problem:** Exposed in etcd (unencrypted by default)
   - **Solution:** Use Secrets + encrypt etcd at rest

❌ **Pitfall 4: Single-Node Cluster**
   - **Problem:** No high availability (node failure = downtime)
   - **Solution:** 3-node cluster (master + 2 workers)

❌ **Pitfall 5: Ignoring Pod Disruption Budgets**
   - **Problem:** Rolling update kills all replicas
   - **Solution:** Set `minAvailable: 1`

════════════════════════════════════════════════════════════════════

📇 **13. QUICK REFERENCE CARD**
────────────────────────────────

**Essential kubectl Commands**

.. code-block:: bash

   # Pod management
   kubectl get pods -A                # List all pods
   kubectl describe pod <name>        # Detailed info
   kubectl logs -f <pod> -c <container>  # Stream logs
   kubectl exec -it <pod> -- /bin/sh  # Shell into pod
   
   # Deployments
   kubectl rollout status deployment/ife-app
   kubectl rollout undo deployment/ife-app
   kubectl scale deployment/ife-app --replicas=10
   
   # Services
   kubectl get svc                    # List services
   kubectl port-forward svc/ife-app 8080:80
   
   # Config
   kubectl create configmap app-config --from-file=config.yaml
   kubectl create secret generic db-creds \
     --from-literal=username=admin \
     --from-literal=password=secret
   
   # Debugging
   kubectl top nodes                  # Node resource usage
   kubectl top pods                   # Pod resource usage
   kubectl get events --sort-by=.metadata.creationTimestamp

**Helm Commands**

.. code-block:: bash

   helm list                          # List releases
   helm upgrade <release> <chart>     # Update release
   helm rollback <release> <revision> # Rollback
   helm template <chart>              # Dry-run (preview YAML)

════════════════════════════════════════════════════════════════════

📝 **14. EXAM QUESTIONS**
──────────────────────────

**Q1:** Why use K3s instead of standard K8s for aircraft?

**A1:** K3s footprint is 512 MB RAM vs. 4 GB for K8s. Aircraft edge computing has limited resources (CPU, power budget). K3s also uses SQLite instead of etcd (no distributed consensus overhead).

────────────────────────────────────────────────────────────────────

**Q2:** How does a service mesh (Istio) provide mTLS without code changes?

**A2:** Istio injects an Envoy sidecar proxy into every pod. All traffic is routed through Envoy, which handles TLS handshakes using certificates from Citadel (control plane). Applications communicate over localhost (no TLS in app code).

────────────────────────────────────────────────────────────────────

**Q3:** What's the difference between a Deployment and a StatefulSet?

**A3:**  
- **Deployment:** Stateless apps (pods are interchangeable, random names)  
- **StatefulSet:** Stateful apps (stable pod IDs like `mysql-0`, `mysql-1`; persistent volumes follow pods)

────────────────────────────────────────────────────────────────────

**Q4:** How do you prevent all replicas from being killed during a rolling update?

**A4:** Set a **PodDisruptionBudget** (PDB) with `minAvailable: 1`. This ensures at least 1 pod remains running during voluntary disruptions (updates, drains).

────────────────────────────────────────────────────────────────────

**Q5:** Your pod shows `CrashLoopBackOff`. How do you debug?

**A5:**  
1. Check logs: `kubectl logs <pod> --previous` (previous container logs)  
2. Describe pod: `kubectl describe pod <pod>` (events section)  
3. Check liveness probe (might be too aggressive)  
4. Exec into running container: `kubectl exec -it <pod> -- /bin/sh`

════════════════════════════════════════════════════════════════════

📚 **15. FURTHER READING**
───────────────────────────

**Books:**
- *Kubernetes: Up and Running* (3rd Edition) — Kelsey Hightower
- *Production Kubernetes* — Josh Rosso, Rich Lander
- *Istio in Action* — Christian Posta, Rinor Maloku

**Standards:**
- CNCF Cloud Native Glossary: https://glossary.cncf.io
- Kubernetes Best Practices: https://kubernetes.io/docs/concepts/

**Online:**
- K3s docs: https://docs.k3s.io
- Helm charts: https://artifacthub.io
- Istio patterns: https://istio.io/latest/docs/

**Courses:**
- CKAD (Certified Kubernetes Application Developer)
- CKA (Certified Kubernetes Administrator)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Deploy K3s on aircraft hardware
- [ ] Create Helm chart for IFE application
- [ ] Configure HorizontalPodAutoscaler
- [ ] Set up Istio service mesh with mTLS
- [ ] Implement blue-green deployment
- [ ] Configure persistent storage (local PV)
- [ ] Set up Prometheus/Grafana monitoring

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ COMPLETE  
**Created:** January 14, 2026  
**For:** Aircraft Services Architect Role (Portland, PAC)  
**Next:** Review [ARINC_664_Cheatsheet.rst](ARINC_664_Cheatsheet.rst)
