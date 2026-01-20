================================================================================
Porting from RTOS to Embedded Linux
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Embedded Linux System Design and Development (2006)
:Focus: VxWorks/pSOS/RTOS migration, OSPL design, pthreads

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. RTOS vs Linux Architecture
================================================================================

1.1 Traditional RTOS Model
--------------------------------------------------------------------------------

**Flat Memory Model:**

::

   +--------------------------------------------------+
   | Single Physical Address Space                    |
   |                                                  |
   | +---------------+  +---------------+             |
   | | Kernel Code   |  | Application 1 |             |
   | | - Scheduler   |  | - UI Task     |             |
   | | - Timers      |  | - Data Task   |             |
   | | - IPC         |  +---------------+             |
   | +---------------+                                |
   |                     +---------------+             |
   | +---------------+  | Application 2 |             |
   | | Device Drivers|  | - Network     |             |
   | +---------------+  +---------------+             |
   |                                                  |
   | All in same physical memory (no MMU protection)  |
   +--------------------------------------------------+

**Characteristics:**

- Single address space for kernel + applications
- No memory protection between tasks
- Direct function calls to kernel services
- Shared global variables between tasks
- Fast context switching (no TLB flush)
- Simple programming model

**Common RTOSes:**

- VxWorks
- pSOS
- Nucleus RTOS
- ThreadX
- QNX (has MMU support)
- FreeRTOS

1.2 Linux Memory Model
--------------------------------------------------------------------------------

**Protected Virtual Address Space:**

::

   Process 1            Process 2            Process 3
   Virtual Space        Virtual Space        Virtual Space
   +-------------+      +-------------+      +-------------+
   | 0xFFFFFFFF  |      | 0xFFFFFFFF  |      | 0xFFFFFFFF  |
   |             |      |             |      |             |
   | Kernel      |      | Kernel      |      | Kernel      |
   | (shared)    |      | (shared)    |      | (shared)    |
   | 0xC0000000  |      | 0xC0000000  |      | 0xC0000000  |
   +-------------+      +-------------+      +-------------+
   | User Stack  |      | User Stack  |      | User Stack  |
   | Libraries   |      | Libraries   |      | Libraries   |
   | Heap        |      | Heap        |      | Heap        |
   | Data        |      | Data        |      | Data        |
   | Text        |      | Text        |      | Text        |
   | 0x00000000  |      | 0x00000000  |      | 0x00000000  |
   +-------------+      +-------------+      +-------------+
         |                    |                    |
         +--------------------+--------------------+
                              ↓
                       Physical Memory
                       (MMU Translation)

**Characteristics:**

- Separate virtual address space per process
- MMU-based memory protection
- System calls for kernel services (not direct calls)
- Protected kernel space
- Isolated process memory
- IPC required for inter-process communication

1.3 Key Differences
--------------------------------------------------------------------------------

+---------------------------+---------------------------+---------------------------+
| Feature                   | RTOS (Flat)               | Linux (Protected)         |
+===========================+===========================+===========================+
| **Memory Protection**     | None                      | Per-process + kernel      |
+---------------------------+---------------------------+---------------------------+
| **Address Space**         | Single shared             | Per-process virtual       |
+---------------------------+---------------------------+---------------------------+
| **Kernel Access**         | Direct function calls     | System calls (trap)       |
+---------------------------+---------------------------+---------------------------+
| **Task Communication**    | Shared memory, globals    | IPC (pipes, sockets, etc.)|
+---------------------------+---------------------------+---------------------------+
| **Task Creation**         | taskSpawn(), taskCreate() | fork(), pthread_create()  |
+---------------------------+---------------------------+---------------------------+
| **Synchronization**       | semTake(), semGive()      | pthread_mutex, semaphore  |
+---------------------------+---------------------------+---------------------------+
| **Message Queues**        | msgQSend(), msgQReceive() | mqueue, pipe, socket      |
+---------------------------+---------------------------+---------------------------+
| **Timers**                | wdCreate(), wdStart()     | timer_create(), setitimer()|
+---------------------------+---------------------------+---------------------------+
| **Interrupts**            | intConnect()              | request_irq() (kernel)    |
+---------------------------+---------------------------+---------------------------+
| **Real-Time**             | Hard real-time            | Soft real-time (PREEMPT_RT|
|                           |                           | for hard)                 |
+---------------------------+---------------------------+---------------------------+

================================================================================
2. Porting Strategy
================================================================================

2.1 Task Categorization
--------------------------------------------------------------------------------

**Step 1: Classify RTOS Tasks**

1. **User-Space Tasks:**
   - UI tasks
   - Application logic
   - File processing
   - Network protocol stacks

2. **Kernel Tasks:**
   - Hardware initialization
   - Interrupt handlers
   - Device drivers
   - Real-time control loops (if hard real-time)

**Step 2: Identify Functions**

1. **User-Space Functions:**
   - File I/O
   - Network communication
   - Data processing
   - UI rendering

2. **Kernel Functions:**
   - Register manipulation
   - DMA operations
   - Interrupt handling
   - Hardware initialization

2.2 Migration Models
--------------------------------------------------------------------------------

**Option 1: One-Process Model**

::

   RTOS                         Linux
   
   User Task 1   ───────────▶   Thread 1  ┐
   User Task 2   ───────────▶   Thread 2  ├─ Single Process
   User Task 3   ───────────▶   Thread 3  ┘
   
   Kernel Task 1 ───────────▶   Kernel Thread 1
   Kernel Task 2 ───────────▶   Kernel Thread 2

**Advantages:**

- Minimal code changes
- Shared global variables work as-is
- Fast inter-thread communication
- Faster porting timeline

**Disadvantages:**

- No memory protection between threads
- One thread crash can corrupt entire process
- Cannot exploit full Linux protection

**Use When:**

- Quick proof-of-concept needed
- Tight schedule constraints
- Tasks heavily share data structures
- Legacy code with complex dependencies

**Option 2: Multi-Process Model**

::

   RTOS                         Linux
   
   User Task 1   ───────────▶   Process 1
   User Task 2   ───────────▶   Process 2
   User Task 3   ───────────▶   Thread 1  ┐
   User Task 4   ───────────▶   Thread 2  ├─ Process 3
                                          ┘
   Key Task      ───────────▶   Process 4 (isolated)
   
   Kernel Task   ───────────▶   Kernel Thread

**Task Categories:**

1. **Unrelated Tasks → Separate Processes**
   - Stand-alone functionality
   - Use IPC for communication
   - Example: Watchdog, logger

2. **Related Tasks → Threads in Same Process**
   - Share global variables
   - Use function callbacks
   - Example: UI components

3. **Key Tasks → Isolated Processes**
   - Critical system functions
   - Must be protected
   - Example: System monitor, safety task

**Advantages:**

- Full memory protection
- Crash isolation (one process doesn't kill others)
- Extensible architecture
- Exploits Linux security model

**Disadvantages:**

- Significant code redesign needed
- Global variables require IPC
- Longer porting time
- Shared libraries need careful handling

================================================================================
3. Operating System Porting Layer (OSPL)
================================================================================

3.1 OSPL Architecture
--------------------------------------------------------------------------------

**Purpose:** Minimize code changes by emulating RTOS APIs using Linux APIs

::

   ┌────────────────────────────────────┐
   │     Application Code (unchanged)   │
   │  taskSpawn(), semTake(), msgQSend() │
   └──────────────┬─────────────────────┘
                  ↓
   ┌──────────────────────────────────────┐
   │  OSPL (Operating System Porting Layer)│
   │  - Maps RTOS APIs to Linux APIs      │
   │  - Handles differences in semantics  │
   └──────────────┬───────────────────────┘
                  ↓
   ┌──────────────────────────────────────┐
   │     Linux/POSIX APIs                 │
   │  pthread_create(), pthread_mutex,    │
   │  mq_send(), timer_create()           │
   └──────────────────────────────────────┘

3.2 API Mapping Categories
--------------------------------------------------------------------------------

**Category 1: One-to-One Mapping**

Direct equivalent exists in Linux:

.. code-block:: c

   /* VxWorks semGive() → pthread_mutex_unlock() */
   
   STATUS semGive(SEM_ID semId)
   {
       return pthread_mutex_unlock((pthread_mutex_t *)semId);
   }

**Category 2: One-to-Many Mapping**

Multiple Linux calls needed:

.. code-block:: c

   /* VxWorks taskSpawn() needs multiple pthread calls */
   
   int taskSpawn(char *name, int priority, int options,
                 int stackSize, FUNCPTR entryPt, int arg1,
                 /* ... */)
   {
       pthread_t tid;
       pthread_attr_t attr;
       struct sched_param param;
       
       /* Initialize attributes */
       pthread_attr_init(&attr);
       pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
       pthread_attr_setstacksize(&attr, stackSize);
       
       /* Set priority */
       param.sched_priority = priority;
       pthread_attr_setschedparam(&attr, &param);
       pthread_attr_setschedpolicy(&attr, SCHED_RR);
       
       /* Create thread */
       if (pthread_create(&tid, &attr, entryPt, (void *)arg1) != 0)
           return ERROR;
       
       pthread_attr_destroy(&attr);
       return (int)tid;
   }

**Category 3: No Direct Equivalent**

Requires redesign or kernel module:

.. code-block:: c

   /* VxWorks intConnect() - no user-space equivalent */
   /* Must move to kernel driver and use request_irq() */

3.3 OSPL Implementation Example
--------------------------------------------------------------------------------

**Header File: ospl.h**

.. code-block:: c

   #ifndef __KERNEL__
   #include <pthread.h>
   #include <semaphore.h>
   #else
   #include <linux/kthread.h>
   #include <linux/mutex.h>
   #endif
   
   /* Task/Thread API */
   #define TASK_ID pthread_t
   #define FUNCPTR void *(*)(void *)
   
   TASK_ID taskSpawn(char *name, int priority, int options,
                     int stackSize, FUNCPTR func, void *arg);
   STATUS taskDelete(TASK_ID tid);
   STATUS taskSuspend(TASK_ID tid);
   STATUS taskResume(TASK_ID tid);
   
   /* Semaphore API */
   typedef struct {
       pthread_mutex_t mutex;
       pthread_cond_t cond;
       int count;
   } SEM_ID_STRUCT;
   
   typedef SEM_ID_STRUCT *SEM_ID;
   
   SEM_ID semBCreate(int options, int initialState);
   SEM_ID semCCreate(int options, int count);
   STATUS semTake(SEM_ID semId, int timeout);
   STATUS semGive(SEM_ID semId);
   STATUS semDelete(SEM_ID semId);
   
   /* Message Queue API */
   typedef struct {
       int mqd;
       int maxMsgs;
       int maxMsgSize;
   } MSG_Q_ID_STRUCT;
   
   typedef MSG_Q_ID_STRUCT *MSG_Q_ID;
   
   MSG_Q_ID msgQCreate(int maxMsgs, int maxMsgLength, int options);
   STATUS msgQSend(MSG_Q_ID msgQId, char *buffer, int nBytes,
                   int timeout, int priority);
   int msgQReceive(MSG_Q_ID msgQId, char *buffer, int maxNBytes,
                   int timeout);
   STATUS msgQDelete(MSG_Q_ID msgQId);

**Implementation: ospl_task.c**

.. code-block:: c

   #include "ospl.h"
   #include <stdlib.h>
   
   TASK_ID taskSpawn(char *name, int priority, int options,
                     int stackSize, FUNCPTR func, void *arg)
   {
       pthread_t *tid;
       pthread_attr_t attr;
       struct sched_param param;
       int ret;
       
       tid = malloc(sizeof(pthread_t));
       if (!tid)
           return (TASK_ID)NULL;
       
       pthread_attr_init(&attr);
       
       /* Set stack size */
       if (stackSize > 0)
           pthread_attr_setstacksize(&attr, stackSize);
       
       /* Set scheduling policy and priority */
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       param.sched_priority = priority;
       pthread_attr_setschedparam(&attr, &param);
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       /* Create thread */
       ret = pthread_create(tid, &attr, func, arg);
       pthread_attr_destroy(&attr);
       
       if (ret != 0) {
           free(tid);
           return (TASK_ID)NULL;
       }
       
       /* Store thread name (optional, using pthread_setname_np) */
       if (name)
           pthread_setname_np(*tid, name);
       
       return (TASK_ID)tid;
   }
   
   STATUS taskDelete(TASK_ID tid)
   {
       pthread_t *thread = (pthread_t *)tid;
       
       if (!thread)
           return ERROR;
       
       pthread_cancel(*thread);
       pthread_join(*thread, NULL);
       free(thread);
       
       return OK;
   }

**Implementation: ospl_sem.c**

.. code-block:: c

   #include "ospl.h"
   #include <stdlib.h>
   #include <errno.h>
   #include <time.h>
   
   /* Binary semaphore */
   SEM_ID semBCreate(int options, int initialState)
   {
       SEM_ID_STRUCT *sem = malloc(sizeof(SEM_ID_STRUCT));
       
       if (!sem)
           return NULL;
       
       pthread_mutex_init(&sem->mutex, NULL);
       pthread_cond_init(&sem->cond, NULL);
       sem->count = initialState ? 1 : 0;
       
       return sem;
   }
   
   /* Counting semaphore */
   SEM_ID semCCreate(int options, int initialCount)
   {
       SEM_ID_STRUCT *sem = malloc(sizeof(SEM_ID_STRUCT));
       
       if (!sem)
           return NULL;
       
       pthread_mutex_init(&sem->mutex, NULL);
       pthread_cond_init(&sem->cond, NULL);
       sem->count = initialCount;
       
       return sem;
   }
   
   STATUS semTake(SEM_ID semId, int timeout)
   {
       SEM_ID_STRUCT *sem = (SEM_ID_STRUCT *)semId;
       struct timespec ts;
       int ret = OK;
       
       pthread_mutex_lock(&sem->mutex);
       
       if (timeout == WAIT_FOREVER) {
           /* Wait indefinitely */
           while (sem->count == 0)
               pthread_cond_wait(&sem->cond, &sem->mutex);
           sem->count--;
       } else if (timeout == NO_WAIT) {
           /* Don't wait */
           if (sem->count > 0)
               sem->count--;
           else
               ret = ERROR;
       } else {
           /* Timed wait */
           clock_gettime(CLOCK_REALTIME, &ts);
           ts.tv_sec += timeout / 1000;
           ts.tv_nsec += (timeout % 1000) * 1000000;
           
           while (sem->count == 0) {
               if (pthread_cond_timedwait(&sem->cond, &sem->mutex, &ts)
                   == ETIMEDOUT) {
                   ret = ERROR;
                   break;
               }
           }
           
           if (ret == OK)
               sem->count--;
       }
       
       pthread_mutex_unlock(&sem->mutex);
       return ret;
   }
   
   STATUS semGive(SEM_ID semId)
   {
       SEM_ID_STRUCT *sem = (SEM_ID_STRUCT *)semId;
       
       pthread_mutex_lock(&sem->mutex);
       sem->count++;
       pthread_cond_signal(&sem->cond);
       pthread_mutex_unlock(&sem->mutex);
       
       return OK;
   }
   
   STATUS semDelete(SEM_ID semId)
   {
       SEM_ID_STRUCT *sem = (SEM_ID_STRUCT *)semId;
       
       pthread_mutex_destroy(&sem->mutex);
       pthread_cond_destroy(&sem->cond);
       free(sem);
       
       return OK;
   }

**Implementation: ospl_msgq.c**

.. code-block:: c

   #include "ospl.h"
   #include <mqueue.h>
   #include <fcntl.h>
   #include <stdlib.h>
   #include <string.h>
   #include <stdio.h>
   
   static int msgq_counter = 0;
   
   MSG_Q_ID msgQCreate(int maxMsgs, int maxMsgLength, int options)
   {
       MSG_Q_ID_STRUCT *mq = malloc(sizeof(MSG_Q_ID_STRUCT));
       struct mq_attr attr;
       char name[32];
       
       if (!mq)
           return NULL;
       
       /* Generate unique name */
       snprintf(name, sizeof(name), "/ospl_mq_%d", msgq_counter++);
       
       /* Set attributes */
       attr.mq_flags = 0;
       attr.mq_maxmsg = maxMsgs;
       attr.mq_msgsize = maxMsgLength;
       attr.mq_curmsgs = 0;
       
       /* Create message queue */
       mq->mqd = mq_open(name, O_CREAT | O_RDWR, 0644, &attr);
       if (mq->mqd == -1) {
           free(mq);
           return NULL;
       }
       
       mq->maxMsgs = maxMsgs;
       mq->maxMsgSize = maxMsgLength;
       
       mq_unlink(name);  /* Unlink so it's removed when closed */
       
       return mq;
   }
   
   STATUS msgQSend(MSG_Q_ID msgQId, char *buffer, int nBytes,
                   int timeout, int priority)
   {
       MSG_Q_ID_STRUCT *mq = (MSG_Q_ID_STRUCT *)msgQId;
       struct timespec ts;
       int ret;
       
       if (timeout == NO_WAIT) {
           ret = mq_send(mq->mqd, buffer, nBytes, priority);
       } else if (timeout == WAIT_FOREVER) {
           ret = mq_send(mq->mqd, buffer, nBytes, priority);
       } else {
           clock_gettime(CLOCK_REALTIME, &ts);
           ts.tv_sec += timeout / 1000;
           ts.tv_nsec += (timeout % 1000) * 1000000;
           ret = mq_timedsend(mq->mqd, buffer, nBytes, priority, &ts);
       }
       
       return (ret == 0) ? OK : ERROR;
   }
   
   int msgQReceive(MSG_Q_ID msgQId, char *buffer, int maxNBytes,
                   int timeout)
   {
       MSG_Q_ID_STRUCT *mq = (MSG_Q_ID_STRUCT *)msgQId;
       struct timespec ts;
       ssize_t bytes;
       
       if (timeout == WAIT_FOREVER) {
           bytes = mq_receive(mq->mqd, buffer, maxNBytes, NULL);
       } else {
           clock_gettime(CLOCK_REALTIME, &ts);
           ts.tv_sec += timeout / 1000;
           ts.tv_nsec += (timeout % 1000) * 1000000;
           bytes = mq_timedreceive(mq->mqd, buffer, maxNBytes, NULL, &ts);
       }
       
       return (int)bytes;
   }
   
   STATUS msgQDelete(MSG_Q_ID msgQId)
   {
       MSG_Q_ID_STRUCT *mq = (MSG_Q_ID_STRUCT *)msgQId;
       
       mq_close(mq->mqd);
       free(mq);
       
       return OK;
   }

================================================================================
4. Pthread Programming
================================================================================

4.1 Thread Creation
--------------------------------------------------------------------------------

.. code-block:: c

   #include <pthread.h>
   
   void *thread_function(void *arg)
   {
       int id = *(int *)arg;
       printf("Thread %d running\n", id);
       
       /* Do work */
       
       return NULL;
   }
   
   int main()
   {
       pthread_t thread1, thread2;
       int id1 = 1, id2 = 2;
       
       /* Create threads */
       pthread_create(&thread1, NULL, thread_function, &id1);
       pthread_create(&thread2, NULL, thread_function, &id2);
       
       /* Wait for threads to finish */
       pthread_join(thread1, NULL);
       pthread_join(thread2, NULL);
       
       return 0;
   }

**Thread Attributes:**

.. code-block:: c

   pthread_t thread;
   pthread_attr_t attr;
   struct sched_param param;
   
   pthread_attr_init(&attr);
   
   /* Set detached state */
   pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
   
   /* Set stack size */
   pthread_attr_setstacksize(&attr, 1024 * 1024);  /* 1MB */
   
   /* Set scheduling policy */
   pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
   
   /* Set priority */
   param.sched_priority = 50;
   pthread_attr_setschedparam(&attr, &param);
   pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
   
   pthread_create(&thread, &attr, thread_func, arg);
   pthread_attr_destroy(&attr);

4.2 Synchronization
--------------------------------------------------------------------------------

**Mutex:**

.. code-block:: c

   pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
   
   /* Lock */
   pthread_mutex_lock(&mutex);
   /* Critical section */
   pthread_mutex_unlock(&mutex);
   
   /* Try lock (non-blocking) */
   if (pthread_mutex_trylock(&mutex) == 0) {
       /* Got lock */
       pthread_mutex_unlock(&mutex);
   }
   
   /* Timed lock */
   struct timespec ts;
   clock_gettime(CLOCK_REALTIME, &ts);
   ts.tv_sec += 5;  /* 5 second timeout */
   if (pthread_mutex_timedlock(&mutex, &ts) == 0) {
       /* Got lock */
       pthread_mutex_unlock(&mutex);
   }

**Condition Variables:**

.. code-block:: c

   pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
   pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
   int ready = 0;
   
   /* Producer */
   pthread_mutex_lock(&mutex);
   ready = 1;
   pthread_cond_signal(&cond);  /* Signal one waiter */
   pthread_mutex_unlock(&mutex);
   
   /* Consumer */
   pthread_mutex_lock(&mutex);
   while (!ready)
       pthread_cond_wait(&cond, &mutex);  /* Atomically unlock and wait */
   /* Process data */
   pthread_mutex_unlock(&mutex);

**Read-Write Locks:**

.. code-block:: c

   pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;
   
   /* Reader */
   pthread_rwlock_rdlock(&rwlock);
   /* Read data */
   pthread_rwlock_unlock(&rwlock);
   
   /* Writer */
   pthread_rwlock_wrlock(&rwlock);
   /* Write data */
   pthread_rwlock_unlock(&rwlock);

4.3 Thread-Specific Data
--------------------------------------------------------------------------------

.. code-block:: c

   pthread_key_t key;
   
   void destructor(void *data)
   {
       free(data);
   }
   
   /* Create key (once) */
   pthread_key_create(&key, destructor);
   
   /* Set thread-specific data */
   void *data = malloc(100);
   pthread_setspecific(key, data);
   
   /* Get thread-specific data */
   void *my_data = pthread_getspecific(key);

================================================================================
5. Inter-Process Communication (IPC)
================================================================================

5.1 POSIX Message Queues
--------------------------------------------------------------------------------

.. code-block:: c

   #include <mqueue.h>
   #include <fcntl.h>
   
   /* Create/open queue */
   mqd_t mq;
   struct mq_attr attr = {
       .mq_flags = 0,
       .mq_maxmsg = 10,
       .mq_msgsize = 256,
   };
   
   mq = mq_open("/myqueue", O_CREAT | O_RDWR, 0644, &attr);
   
   /* Send message */
   char msg[] = "Hello";
   mq_send(mq, msg, strlen(msg) + 1, 0);
   
   /* Receive message */
   char buffer[256];
   ssize_t bytes = mq_receive(mq, buffer, 256, NULL);
   
   /* Close and unlink */
   mq_close(mq);
   mq_unlink("/myqueue");

5.2 Shared Memory
--------------------------------------------------------------------------------

.. code-block:: c

   #include <sys/mman.h>
   #include <fcntl.h>
   
   /* Create shared memory */
   int fd = shm_open("/myshm", O_CREAT | O_RDWR, 0644);
   ftruncate(fd, 4096);
   
   /* Map to address space */
   void *ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                    MAP_SHARED, fd, 0);
   
   /* Use shared memory */
   strcpy(ptr, "Shared data");
   
   /* Unmap and close */
   munmap(ptr, 4096);
   close(fd);
   shm_unlink("/myshm");

5.3 Pipes and FIFOs
--------------------------------------------------------------------------------

.. code-block:: c

   /* Pipe (anonymous) */
   int pipefd[2];
   pipe(pipefd);
   
   write(pipefd[1], "data", 4);
   char buf[4];
   read(pipefd[0], buf, 4);
   
   /* FIFO (named pipe) */
   mkfifo("/tmp/myfifo", 0666);
   
   /* Process 1 */
   int fd = open("/tmp/myfifo", O_WRONLY);
   write(fd, "data", 4);
   close(fd);
   
   /* Process 2 */
   fd = open("/tmp/myfifo", O_RDONLY);
   read(fd, buf, 4);
   close(fd);

================================================================================
6. Kernel API Driver
================================================================================

6.1 When Needed
--------------------------------------------------------------------------------

**Problem:** Function calls both user-space and kernel functions:

.. code-block:: c

   void mixed_function()
   {
       user_space_func();   /* Can run in user space */
       kernel_func();       /* Needs kernel space */
   }

**Solution:** Kernel API driver provides user-space access to kernel functions

6.2 Implementation
--------------------------------------------------------------------------------

**Kernel Module (kernel_api.c):**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/uaccess.h>
   
   #define DEVICE_NAME "kernel_api"
   #define IOCTL_KERNEL_FUNC _IOW('k', 1, int)
   
   static long device_ioctl(struct file *file, unsigned int cmd,
                           unsigned long arg)
   {
       switch (cmd) {
       case IOCTL_KERNEL_FUNC:
           /* Call kernel function */
           return kernel_func(arg);
       default:
           return -EINVAL;
       }
   }
   
   static struct file_operations fops = {
       .unlocked_ioctl = device_ioctl,
   };
   
   static int major;
   
   static int __init kernel_api_init(void)
   {
       major = register_chrdev(0, DEVICE_NAME, &fops);
       return 0;
   }
   
   module_init(kernel_api_init);

**User Space Usage:**

.. code-block:: c

   void mixed_function()
   {
       int fd;
       
       /* User-space part */
       user_space_func();
       
       /* Kernel part via ioctl */
       fd = open("/dev/kernel_api", O_RDWR);
       ioctl(fd, IOCTL_KERNEL_FUNC, arg);
       close(fd);
   }

================================================================================
7. Real-Time Considerations
================================================================================

7.1 Scheduling Policies
--------------------------------------------------------------------------------

.. code-block:: c

   /* Set real-time priority */
   struct sched_param param;
   param.sched_priority = 50;
   
   /* SCHED_FIFO: First-In-First-Out, no time slicing */
   pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
   
   /* SCHED_RR: Round-Robin, time slicing */
   pthread_setschedparam(pthread_self(), SCHED_RR, &param);
   
   /* Requires root or CAP_SYS_NICE capability */

7.2 Memory Locking
--------------------------------------------------------------------------------

.. code-block:: c

   #include <sys/mman.h>
   
   /* Lock all current and future pages */
   mlockall(MCL_CURRENT | MCL_FUTURE);
   
   /* Prevents paging, ensures real-time performance */

7.3 PREEMPT_RT Kernel
--------------------------------------------------------------------------------

For hard real-time, use PREEMPT_RT patched kernel:

.. code-block:: bash

   # Check if running RT kernel
   uname -v | grep PREEMPT_RT

================================================================================
8. Common Pitfalls and Solutions
================================================================================

**Pitfall 1: Shared Library Global Variables**

.. code-block:: c

   /* Problem: Global in shared library is per-process */
   int global_counter = 0;  /* Each process has its own copy */
   
   /* Solution: Use shared memory */
   int *global_counter = mmap(..., MAP_SHARED, ...);

**Pitfall 2: Priority Inversion**

Use priority inheritance mutexes:

.. code-block:: c

   pthread_mutexattr_t attr;
   pthread_mutexattr_init(&attr);
   pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
   pthread_mutex_init(&mutex, &attr);

**Pitfall 3: Signal Handling**

Block signals in threads except one designated handler:

.. code-block:: c

   sigset_t set;
   sigfillset(&set);
   pthread_sigmask(SIG_BLOCK, &set, NULL);

================================================================================
9. Migration Checklist
================================================================================

**Phase 1: Planning**

- [ ] Categorize all tasks (user/kernel)
- [ ] Choose migration model (one-process vs multi-process)
- [ ] Identify RTOS API usage
- [ ] Map RTOS APIs to Linux APIs
- [ ] Identify no-equivalent APIs

**Phase 2: OSPL Development**

- [ ] Design OSPL interface
- [ ] Implement task APIs
- [ ] Implement semaphore APIs
- [ ] Implement message queue APIs
- [ ] Implement timer APIs
- [ ] Test OSPL with simple programs

**Phase 3: Application Porting**

- [ ] Port kernel tasks as kernel threads/drivers
- [ ] Port user tasks as processes/threads
- [ ] Replace direct kernel calls with system calls
- [ ] Update shared memory to use IPC
- [ ] Test individual components

**Phase 4: Integration & Testing**

- [ ] Integration testing
- [ ] Performance profiling
- [ ] Real-time testing
- [ ] Stress testing
- [ ] Memory leak testing

================================================================================
End of RTOS to Linux Porting Cheatsheet
================================================================================
