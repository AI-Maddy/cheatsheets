================================================
SMP & AMP Multicore Processing Complete Guide
================================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

Comparison
----------

+---------------------------+----------------------------------+----------------------------------+
| **Feature**               | **SMP (Symmetric)**              | **AMP (Asymmetric)**             |
+===========================+==================================+==================================+
| OS Instances              | Single shared OS                 | Multiple independent OS          |
+---------------------------+----------------------------------+----------------------------------+
| Core Types                | Homogeneous (identical)          | Can be heterogeneous             |
+---------------------------+----------------------------------+----------------------------------+
| Memory Model              | Shared memory                    | Shared or partitioned            |
+---------------------------+----------------------------------+----------------------------------+
| Load Balancing            | Automatic by OS                  | Manual/static assignment         |
+---------------------------+----------------------------------+----------------------------------+
| IPC                       | Kernel primitives                | Explicit messaging (RPMsg, etc.) |
+---------------------------+----------------------------------+----------------------------------+
| Use Cases                 | General computing, servers       | Real-time + non-RT, heterogeneous|
+---------------------------+----------------------------------+----------------------------------+
| Complexity                | Lower (OS handles scheduling)    | Higher (manual orchestration)    |
+---------------------------+----------------------------------+----------------------------------+
| Examples                  | Linux on quad-core CPU           | Linux on A53 + FreeRTOS on M4    |
+---------------------------+----------------------------------+----------------------------------+

Architecture Patterns
---------------------

.. code-block:: text

   SMP:
   ┌─────────────────────────────────┐
   │      Linux Kernel (SMP)         │
   ├────────┬────────┬────────┬──────┤
   │ Core 0 │ Core 1 │ Core 2 │ Core 3│
   │ (A53)  │ (A53)  │ (A53)  │ (A53) │
   └────────┴────────┴────────┴──────┘
         Shared Memory (DDR)
   
   AMP:
   ┌──────────────┐  ┌──────────────┐
   │ Linux Kernel │  │  FreeRTOS    │
   ├────┬────────┬┤  ├──────────────┤
   │ A53│  A53   ││  │     M4       │
   └────┴────────┴┘  └──────────────┘
        │                   │
        │    RPMsg/IPC      │
        └───────────────────┘
         Shared Memory Region

🔧 SMP Configuration
=====================

Linux Kernel SMP
----------------

**Enable SMP in Kernel:**

.. code-block:: kconfig

   CONFIG_SMP=y
   CONFIG_NR_CPUS=8
   CONFIG_SCHED_SMT=y
   CONFIG_SCHED_MC=y

**CPU Hotplug:**

.. code-block:: bash

   # Check online CPUs
   lscpu
   cat /sys/devices/system/cpu/online
   
   # Disable CPU
   echo 0 > /sys/devices/system/cpu/cpu1/online
   
   # Enable CPU
   echo 1 > /sys/devices/system/cpu/cpu1/online
   
   # Check CPU info
   cat /proc/cpuinfo

**CPU Affinity:**

.. code-block:: bash

   # Run process on specific CPUs
   taskset -c 0,1 ./myapp
   
   # Get affinity of running process
   taskset -p 1234
   
   # Set affinity of running process
   taskset -p -c 2,3 1234
   
   # Use cpuset for process groups
   mkdir /sys/fs/cgroup/cpuset/mygroup
   echo 0-3 > /sys/fs/cgroup/cpuset/mygroup/cpus
   echo 0 > /sys/fs/cgroup/cpuset/mygroup/mems
   echo $$ > /sys/fs/cgroup/cpuset/mygroup/tasks

**IRQ Affinity:**

.. code-block:: bash

   # View IRQ affinity
   cat /proc/irq/*/smp_affinity
   
   # Set IRQ to specific CPU (bitmask)
   echo 2 > /proc/irq/50/smp_affinity  # CPU 1 (bit 1 = 0x2)
   echo f > /proc/irq/50/smp_affinity  # CPUs 0-3 (0xF)
   
   # Use irqbalance daemon
   sudo apt install irqbalance
   sudo systemctl start irqbalance

Device Tree for SMP
--------------------

.. code-block:: dts

   / {
       cpus {
           #address-cells = <1>;
           #size-cells = <0>;
           
           cpu@0 {
               device_type = "cpu";
               compatible = "arm,cortex-a53";
               reg = <0>;
               enable-method = "psci";
               next-level-cache = <&L2_0>;
           };
           
           cpu@1 {
               device_type = "cpu";
               compatible = "arm,cortex-a53";
               reg = <1>;
               enable-method = "psci";
               next-level-cache = <&L2_0>;
           };
           
           cpu@2 {
               device_type = "cpu";
               compatible = "arm,cortex-a53";
               reg = <2>;
               enable-method = "psci";
               next-level-cache = <&L2_0>;
           };
           
           cpu@3 {
               device_type = "cpu";
               compatible = "arm,cortex-a53";
               reg = <3>;
               enable-method = "psci";
               next-level-cache = <&L2_0>;
           };
       };
       
       psci {
           compatible = "arm,psci-0.2";
           method = "smc";
       };
   };

Programming for SMP
-------------------

**Pthreads (POSIX Threads):**

.. code-block:: c

   #include <pthread.h>
   #include <stdio.h>
   
   void *thread_function(void *arg) {
       int thread_id = *(int*)arg;
       printf("Thread %d running on CPU %d\n", thread_id, sched_getcpu());
       return NULL;
   }
   
   int main() {
       pthread_t threads[4];
       int thread_ids[4];
       
       for (int i = 0; i < 4; i++) {
           thread_ids[i] = i;
           pthread_create(&threads[i], NULL, thread_function, &thread_ids[i]);
       }
       
       for (int i = 0; i < 4; i++) {
           pthread_join(threads[i], NULL);
       }
       
       return 0;
   }

**OpenMP:**

.. code-block:: c

   #include <omp.h>
   #include <stdio.h>
   
   int main() {
       #pragma omp parallel num_threads(4)
       {
           int thread_id = omp_get_thread_num();
           int num_threads = omp_get_num_threads();
           printf("Thread %d of %d\n", thread_id, num_threads);
       }
       
       // Parallel for loop
       int sum = 0;
       #pragma omp parallel for reduction(+:sum)
       for (int i = 0; i < 1000; i++) {
           sum += i;
       }
       
       return 0;
   }

**CPU Pinning:**

.. code-block:: c

   #define _GNU_SOURCE
   #include <pthread.h>
   #include <sched.h>
   
   void *pinned_thread(void *arg) {
       cpu_set_t cpuset;
       CPU_ZERO(&cpuset);
       CPU_SET(2, &cpuset);  // Pin to CPU 2
       
       pthread_t current_thread = pthread_self();
       pthread_setaffinity_np(current_thread, sizeof(cpu_set_t), &cpuset);
       
       // Thread code here
       return NULL;
   }

🔀 AMP Configuration
=====================

OpenAMP Framework
-----------------

**Architecture:**

.. code-block:: text

   ┌──────────────────────────────────┐
   │      Host OS (Linux)             │
   ├──────────────────────────────────┤
   │         OpenAMP                  │
   │  ┌────────────┬──────────────┐   │
   │  │ Remoteproc │    RPMsg     │   │
   │  │ (Lifecycle)│  (Messaging) │   │
   │  └────────────┴──────────────┘   │
   │         VirtIO                   │
   │         libmetal                 │
   └──────────────────────────────────┘
            │         ▲
            │  Shared │
            │  Memory │
            ▼         │
   ┌──────────────────────────────────┐
   │   Remote OS (RTOS/Bare-metal)    │
   │         OpenAMP                  │
   │  ┌────────────┬──────────────┐   │
   │  │ Resource   │    RPMsg     │   │
   │  │   Table    │              │   │
   │  └────────────┴──────────────┘   │
   │         VirtIO                   │
   │         libmetal                 │
   └──────────────────────────────────┘

Linux Remoteproc
----------------

**Device Tree Configuration:**

.. code-block:: dts

   reserved-memory {
       #address-cells = <1>;
       #size-cells = <1>;
       ranges;
       
       rproc_reserved: rproc@80000000 {
           no-map;
           reg = <0x80000000 0x1000000>;  /* 16MB */
       };
       
       vdev0vring0: vdev0vring0@81000000 {
           reg = <0x81000000 0x8000>;
       };
       
       vdev0vring1: vdev0vring1@81008000 {
           reg = <0x81008000 0x8000>;
       };
       
       vdev0buffer: vdev0buffer@81010000 {
           compatible = "shared-dma-pool";
           reg = <0x81010000 0xF0000>;
       };
   };
   
   remoteproc_m4: remoteproc@38000000 {
       compatible = "fsl,imx8mn-cm7";
       clocks = <&clk IMX8MN_CLK_M7_DIV>;
       syscon = <&src>;
       memory-region = <&rproc_reserved>, <&vdev0vring0>,
                       <&vdev0vring1>, <&vdev0buffer>;
   };

**Load Firmware:**

.. code-block:: bash

   # Check remoteproc status
   cat /sys/class/remoteproc/remoteproc0/state
   
   # Load firmware
   echo firmware.elf > /sys/class/remoteproc/remoteproc0/firmware
   
   # Start remote processor
   echo start > /sys/class/remoteproc/remoteproc0/state
   
   # Stop remote processor
   echo stop > /sys/class/remoteproc/remoteproc0/state
   
   # Firmware location
   ls /lib/firmware/

**Resource Table (Remote Side):**

.. code-block:: c

   #include "rsc_table.h"
   
   #define RPMSG_IPU_C0_FEATURES  1
   
   struct remote_resource_table {
       unsigned int version;
       unsigned int num;
       unsigned int reserved[2];
       unsigned int offset[1];
       
       /* rpmsg vdev entry */
       struct fw_rsc_vdev rpmsg_vdev;
       struct fw_rsc_vdev_vring rpmsg_vring0;
       struct fw_rsc_vdev_vring rpmsg_vring1;
   } __attribute__((packed));
   
   #pragma DATA_SECTION(ti_ipc_remoteproc_ResourceTable, ".resource_table")
   #pragma DATA_ALIGN(ti_ipc_remoteproc_ResourceTable, 4096)
   
   struct remote_resource_table ti_ipc_remoteproc_ResourceTable = {
       .version = 1,
       .num = 1,
       .offset = {
           offsetof(struct remote_resource_table, rpmsg_vdev),
       },
       
       .rpmsg_vdev = {
           .type = RSC_VDEV,
           .id = VIRTIO_ID_RPMSG,
           .notifyid = 0,
           .dfeatures = RPMSG_IPU_C0_FEATURES,
           .gfeatures = 0,
           .config_len = 0,
           .status = 0,
           .num_of_vrings = 2,
           .reserved = {0, 0},
       },
       
       .rpmsg_vring0 = {
           .da = 0x81000000,
           .align = 0x1000,
           .num = 256,
           .notifyid = 0,
           .reserved = 0,
       },
       
       .rpmsg_vring1 = {
           .da = 0x81008000,
           .align = 0x1000,
           .num = 256,
           .notifyid = 1,
           .reserved = 0,
       },
   };

RPMsg (Inter-Processor Communication)
--------------------------------------

**Linux RPMsg Driver:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/rpmsg.h>
   
   static int rpmsg_sample_cb(struct rpmsg_device *rpdev, void *data,
                              int len, void *priv, u32 src)
   {
       dev_info(&rpdev->dev, "Received: %s (len=%d, src=%d)\n",
                (char *)data, len, src);
       
       /* Echo back */
       rpmsg_send(rpdev->ept, data, len);
       
       return 0;
   }
   
   static int rpmsg_sample_probe(struct rpmsg_device *rpdev)
   {
       dev_info(&rpdev->dev, "RPMsg sample driver probed\n");
       
       /* Send initial message */
       rpmsg_send(rpdev->ept, "Hello from Linux!", 18);
       
       return 0;
   }
   
   static void rpmsg_sample_remove(struct rpmsg_device *rpdev)
   {
       dev_info(&rpdev->dev, "RPMsg sample driver removed\n");
   }
   
   static struct rpmsg_device_id rpmsg_sample_id_table[] = {
       { .name = "rpmsg-client-sample" },
       { },
   };
   
   static struct rpmsg_driver rpmsg_sample_driver = {
       .drv.name   = "rpmsg_sample_driver",
       .id_table   = rpmsg_sample_id_table,
       .probe      = rpmsg_sample_probe,
       .callback   = rpmsg_sample_cb,
       .remove     = rpmsg_sample_remove,
   };
   
   module_rpmsg_driver(rpmsg_sample_driver);

**FreeRTOS RPMsg Application:**

.. code-block:: c

   #include "rpmsg_lite.h"
   #include "rpmsg_ns.h"
   
   #define RPMSG_LITE_LINK_ID      (0)
   #define RPMSG_LITE_NS_ANNOUNCE_STRING  "rpmsg-client-sample"
   
   struct rpmsg_lite_instance *rpmsg_instance;
   struct rpmsg_lite_endpoint *rpmsg_ept;
   
   int32_t rpmsg_callback(void *payload, uint32_t payload_len,
                          uint32_t src, void *priv)
   {
       printf("Received: %s\n", (char *)payload);
       
       /* Send response */
       rpmsg_lite_send(rpmsg_instance, rpmsg_ept, src,
                       "Hello from FreeRTOS!", 21, RL_BLOCK);
       
       return RL_RELEASE;
   }
   
   void rpmsg_task(void *param)
   {
       /* Initialize RPMsg */
       rpmsg_instance = rpmsg_lite_remote_init(
           (void *)RPMSG_LITE_SHMEM_BASE,
           RPMSG_LITE_LINK_ID,
           RL_NO_FLAGS
       );
       
       /* Wait for link up */
       while (!rpmsg_lite_is_link_up(rpmsg_instance))
           ;
       
       /* Create endpoint */
       rpmsg_ept = rpmsg_lite_create_ept(
           rpmsg_instance,
           RL_ADDR_ANY,
           rpmsg_callback,
           NULL
       );
       
       /* Announce service */
       rpmsg_ns_announce(
           rpmsg_instance,
           rpmsg_ept,
           RPMSG_LITE_NS_ANNOUNCE_STRING,
           RL_NS_CREATE
       );
       
       /* Run forever */
       while (1) {
           vTaskDelay(pdMS_TO_TICKS(1000));
       }
   }

**User-Space RPMsg:**

.. code-block:: c

   #include <stdio.h>
   #include <fcntl.h>
   #include <unistd.h>
   #include <string.h>
   
   int main() {
       int fd;
       char buf[512];
       int ret;
       
       /* Open RPMsg char device */
       fd = open("/dev/rpmsg_ctrl0", O_RDWR);
       if (fd < 0) {
           perror("Failed to open rpmsg device");
           return -1;
       }
       
       /* Send message */
       const char *msg = "Hello from user-space!";
       ret = write(fd, msg, strlen(msg));
       if (ret < 0) {
           perror("Write failed");
           close(fd);
           return -1;
       }
       
       /* Receive message */
       ret = read(fd, buf, sizeof(buf));
       if (ret > 0) {
           buf[ret] = '\0';
           printf("Received: %s\n", buf);
       }
       
       close(fd);
       return 0;
   }

Platform-Specific AMP
---------------------

**NXP i.MX 8M:**

.. code-block:: bash

   # i.MX 8M Plus (Cortex-A53 + Cortex-M7)
   
   # Build M7 firmware
   cd imx-m7-demos
   ./build.sh hello_world
   
   # Copy firmware
   sudo cp hello_world.bin /lib/firmware/
   
   # Start M7
   echo hello_world.bin > /sys/class/remoteproc/remoteproc0/firmware
   echo start > /sys/class/remoteproc/remoteproc0/state
   
   # Check M7 output
   dmesg | grep remoteproc

**TI AM64x:**

.. code-block:: bash

   # AM64x (Cortex-A53 + Cortex-R5F + Cortex-M4F)
   
   # Load R5F firmware
   echo am64-main-r5f0_0-fw > /sys/class/remoteproc/remoteproc2/firmware
   echo start > /sys/class/remoteproc/remoteproc2/state
   
   # Load M4F firmware
   echo am64-mcu-m4f0_0-fw > /sys/class/remoteproc/remoteproc3/firmware
   echo start > /sys/class/remoteproc/remoteproc3/state

**STM32MP1:**

.. code-block:: bash

   # STM32MP157 (Cortex-A7 + Cortex-M4)
   
   # Load M4 firmware
   echo firmware.elf > /sys/class/remoteproc/remoteproc0/firmware
   echo start > /sys/class/remoteproc/remoteproc0/state
   
   # Use TTY interface
   cat /dev/ttyRPMSG0 &
   echo "Hello M4" > /dev/ttyRPMSG0

**Xilinx Zynq UltraScale+:**

.. code-block:: bash

   # Zynq MPSoC (Cortex-A53 + Cortex-R5 + MicroBlaze)
   
   # Load R5 firmware
   echo firmware.elf > /sys/class/remoteproc/remoteproc0/firmware
   echo start > /sys/class/remoteproc/remoteproc0/state
   
   # OpenAMP with RPMsg
   modprobe rpmsg_char

💻 Multicore Programming
=========================

Synchronization Primitives
---------------------------

**Atomic Operations:**

.. code-block:: c

   #include <stdatomic.h>
   
   atomic_int counter = 0;
   
   void increment() {
       atomic_fetch_add(&counter, 1);
   }
   
   int get_value() {
       return atomic_load(&counter);
   }

**Mutexes:**

.. code-block:: c

   #include <pthread.h>
   
   pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
   int shared_data = 0;
   
   void *thread_func(void *arg) {
       pthread_mutex_lock(&lock);
       shared_data++;
       pthread_mutex_unlock(&lock);
       return NULL;
   }

**Spinlocks:**

.. code-block:: c

   #include <pthread.h>
   
   pthread_spinlock_t spinlock;
   
   void init() {
       pthread_spin_init(&spinlock, PTHREAD_PROCESS_PRIVATE);
   }
   
   void critical_section() {
       pthread_spin_lock(&spinlock);
       // Fast critical section
       pthread_spin_unlock(&spinlock);
   }

**Barriers:**

.. code-block:: c

   #include <pthread.h>
   
   pthread_barrier_t barrier;
   
   void init(int num_threads) {
       pthread_barrier_init(&barrier, NULL, num_threads);
   }
   
   void *thread_func(void *arg) {
       // Phase 1
       pthread_barrier_wait(&barrier);  // Sync point
       // Phase 2
       return NULL;
   }

**Read-Write Locks:**

.. code-block:: c

   #include <pthread.h>
   
   pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;
   int data = 0;
   
   void reader() {
       pthread_rwlock_rdlock(&rwlock);
       printf("Data: %d\n", data);
       pthread_rwlock_unlock(&rwlock);
   }
   
   void writer() {
       pthread_rwlock_wrlock(&rwlock);
       data++;
       pthread_rwlock_unlock(&rwlock);
   }

Lock-Free Programming
---------------------

**Lock-Free Queue:**

.. code-block:: c

   #include <stdatomic.h>
   
   typedef struct node {
       void *data;
       struct node *next;
   } node_t;
   
   typedef struct {
       atomic_ptr head;
       atomic_ptr tail;
   } queue_t;
   
   void enqueue(queue_t *q, void *data) {
       node_t *node = malloc(sizeof(node_t));
       node->data = data;
       node->next = NULL;
       
       node_t *tail = atomic_load(&q->tail);
       node_t *next;
       
       while (1) {
           next = atomic_load(&tail->next);
           if (next == NULL) {
               if (atomic_compare_exchange_weak(&tail->next, &next, node)) {
                   break;
               }
           } else {
               atomic_compare_exchange_weak(&q->tail, &tail, next);
               tail = atomic_load(&q->tail);
           }
       }
       atomic_compare_exchange_strong(&q->tail, &tail, node);
   }

Memory Ordering
---------------

.. code-block:: c

   #include <stdatomic.h>
   
   atomic_int data = 0;
   atomic_int flag = 0;
   
   // Producer
   void produce() {
       atomic_store_explicit(&data, 42, memory_order_relaxed);
       atomic_store_explicit(&flag, 1, memory_order_release);
   }
   
   // Consumer
   int consume() {
       while (atomic_load_explicit(&flag, memory_order_acquire) == 0)
           ;
       return atomic_load_explicit(&data, memory_order_relaxed);
   }

🔍 Performance Tuning
======================

CPU Frequency Scaling
---------------------

.. code-block:: bash

   # Check current governor
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
   
   # Set performance governor (maximum frequency)
   echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
   
   # Set powersave governor
   echo powersave | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
   
   # Available frequencies
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
   
   # Set specific frequency
   echo 1500000 | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed

NUMA Tuning
-----------

.. code-block:: bash

   # Check NUMA topology
   numactl --hardware
   
   # Run on specific NUMA node
   numactl --cpunodebind=0 --membind=0 ./myapp
   
   # Interleave memory across nodes
   numactl --interleave=all ./myapp
   
   # Check process NUMA policy
   numactl --show

Cache Optimization
------------------

.. code-block:: c

   // Cache line padding to avoid false sharing
   #define CACHE_LINE_SIZE 64
   
   typedef struct {
       int data;
       char padding[CACHE_LINE_SIZE - sizeof(int)];
   } cache_aligned_t __attribute__((aligned(CACHE_LINE_SIZE)));
   
   // Prefetch data
   __builtin_prefetch(&data, 0, 3);  // Read prefetch, high temporal locality

Real-Time Configuration
-----------------------

.. code-block:: bash

   # Set real-time priority
   chrt -f 99 ./myapp
   
   # Set CPU isolation (kernel cmdline)
   isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3

**RT Priority in Code:**

.. code-block:: c

   #include <sched.h>
   
   void set_realtime() {
       struct sched_param param;
       param.sched_priority = 99;
       
       if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
           perror("sched_setscheduler failed");
       }
   }

🛠️ Debugging & Profiling
==========================

Multicore Debugging
-------------------

**GDB Multi-Process:**

.. code-block:: bash

   # Debug with GDB
   gdb ./myapp
   (gdb) set detach-on-fork off
   (gdb) set follow-fork-mode parent
   (gdb) run
   (gdb) info threads
   (gdb) thread 2
   (gdb) bt

**Performance Counters:**

.. code-block:: bash

   # CPU-wide statistics
   perf stat -a sleep 5
   
   # Per-thread statistics
   perf stat -t <tid> sleep 5
   
   # Cache misses
   perf stat -e cache-misses,cache-references ./myapp
   
   # Record and analyze
   perf record -g ./myapp
   perf report

**Trace Events:**

.. code-block:: bash

   # Enable tracing
   cd /sys/kernel/debug/tracing
   echo 1 > events/sched/enable
   echo 1 > tracing_on
   
   # View trace
   cat trace
   
   # Or use trace-cmd
   trace-cmd record -e sched ./myapp
   trace-cmd report

Lock Contention Analysis
-------------------------

.. code-block:: bash

   # Analyze lock contention
   perf lock record ./myapp
   perf lock report
   
   # Lock statistics
   perf lock contention

Memory Debugging
----------------

.. code-block:: bash

   # Valgrind with thread analysis
   valgrind --tool=helgrind ./myapp
   valgrind --tool=drd ./myapp
   
   # Thread sanitizer
   gcc -fsanitize=thread myapp.c -o myapp
   ./myapp

📚 Best Practices
==================

SMP Best Practices
------------------

1. **Minimize Lock Contention**: Use fine-grained locks
2. **Avoid False Sharing**: Align to cache lines
3. **Use Lock-Free When Possible**: For high-performance paths
4. **Profile First**: Identify bottlenecks before optimizing
5. **Consider NUMA**: Pin threads/memory to nodes

AMP Best Practices
------------------

1. **Clear Resource Partitioning**: Define memory regions explicitly
2. **Minimize Shared Memory**: Reduce cache coherency overhead
3. **Efficient IPC**: Batch messages when possible
4. **Error Handling**: Handle remote core failures gracefully
5. **Debugging Infrastructure**: Plan for multi-core debugging

📖 References
==============

Standards
---------

* **OpenAMP**: https://github.com/OpenAMP/open-amp
* **POSIX Threads**: IEEE 1003.1c
* **VirtIO**: https://docs.oasis-open.org/virtio/
* **RPMsg**: Linux kernel Documentation/rpmsg.txt

Documentation
-------------

* **Linux SMP**: Documentation/scheduler/
* **Remoteproc**: Documentation/remoteproc.txt
* **RPMsg**: Documentation/rpmsg.txt
* **OpenMP**: https://www.openmp.org/specifications/

Tools
-----

* **perf**: Linux performance analysis
* **trace-cmd**: Kernel tracing
* **numactl**: NUMA control
* **taskset**: CPU affinity

================================
Last Updated: January 2026
Version: 3.0
================================
