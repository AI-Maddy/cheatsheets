==================================
Linux Wait Queues Guide
==================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Wait Queue Operations
----------------------------

.. code-block:: c

   #include <linux/wait.h>
   
   /* Declaration and initialization */
   DECLARE_WAIT_QUEUE_HEAD(my_waitqueue);
   
   wait_queue_head_t my_waitqueue;
   init_waitqueue_head(&my_waitqueue);
   
   /* Wait for condition */
   wait_event(my_waitqueue, condition);
   wait_event_interruptible(my_waitqueue, condition);
   wait_event_timeout(my_waitqueue, condition, timeout);
   
   /* Wake up waiters */
   wake_up(&my_waitqueue);              // Wake one
   wake_up_all(&my_waitqueue);          // Wake all
   wake_up_interruptible(&my_waitqueue);

Common Wait Patterns
--------------------

.. code-block:: c

   /* Pattern 1: Simple wait */
   wait_event(wq, data_available);
   
   /* Pattern 2: Interruptible wait */
   if (wait_event_interruptible(wq, data_available))
       return -ERESTARTSYS;
   
   /* Pattern 3: Wait with timeout */
   ret = wait_event_timeout(wq, data_available, HZ * 5);
   if (ret == 0)
       return -ETIMEDOUT;
   
   /* Pattern 4: Custom wait condition */
   wait_event(wq, queue_not_empty(&queue) || shutdown_flag);

Manual Wait Entry
-----------------

.. code-block:: c

   DEFINE_WAIT(wait);
   
   prepare_to_wait(&wq, &wait, TASK_INTERRUPTIBLE);
   
   if (!condition) {
       schedule();
   }
   
   finish_wait(&wq, &wait);

Wait Queue Fundamentals
=======================

Introduction
------------

Wait queues allow kernel code to sleep until a condition becomes true. They are the primary mechanism for blocking in the kernel.

**Key Characteristics:**

- Tasks sleep until woken by an event
- Conditions checked automatically
- Support timeouts and interruption
- Efficient - no busy waiting
- Used throughout the kernel

**Common Use Cases:**

- Waiting for I/O completion
- Waiting for data availability
- Waiting for resource acquisition
- Device state changes
- Synchronizing with interrupts

Wait Queue Types
----------------

.. code-block:: c

   /* Simple wait queue */
   typedef struct wait_queue_head {
       spinlock_t lock;
       struct list_head head;
   } wait_queue_head_t;
   
   /* Wait queue entry */
   typedef struct wait_queue_entry {
       unsigned int flags;
       void *private;
       wait_queue_func_t func;
       struct list_head entry;
   } wait_queue_entry_t;

Initialization
==============

Static Initialization
---------------------

.. code-block:: c

   /* Declare and initialize */
   DECLARE_WAIT_QUEUE_HEAD(data_waitqueue);
   
   /* Multiple wait queues */
   static DECLARE_WAIT_QUEUE_HEAD(read_wq);
   static DECLARE_WAIT_QUEUE_HEAD(write_wq);

Dynamic Initialization
----------------------

.. code-block:: c

   struct device {
       wait_queue_head_t read_queue;
       wait_queue_head_t write_queue;
   };
   
   static int device_probe(struct platform_device *pdev) {
       struct device *dev;
       
       dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       init_waitqueue_head(&dev->read_queue);
       init_waitqueue_head(&dev->write_queue);
       
       return 0;
   }

Basic Waiting
=============

Simple Wait
-----------

.. code-block:: c

   static int data_available;
   static DECLARE_WAIT_QUEUE_HEAD(data_wq);
   
   /* Wait for data */
   static void consumer(void) {
       pr_info("Waiting for data...\n");
       
       wait_event(data_wq, data_available);
       
       pr_info("Data is available!\n");
       process_data();
       data_available = 0;
   }
   
   /* Provide data and wake */
   static void producer(void) {
       prepare_data();
       
       data_available = 1;
       wake_up(&data_wq);
   }

**Important:** Condition is re-checked after wake to avoid race conditions.

Interruptible Wait
------------------

Allows task to be interrupted by signals.

.. code-block:: c

   static int device_read(struct file *filp, char __user *buf,
                          size_t count, loff_t *f_pos) {
       struct device *dev = filp->private_data;
       int ret;
       
       /* Wait for data to be available */
       ret = wait_event_interruptible(dev->read_queue,
                                       !queue_empty(&dev->queue));
       if (ret)
           return -ERESTARTSYS;  /* Interrupted by signal */
       
       /* Data is available */
       return read_data(dev, buf, count);
   }

Wait with Timeout
-----------------

.. code-block:: c

   static int device_wait_ready(struct device *dev) {
       long ret;
       
       /* Wait up to 5 seconds */
       ret = wait_event_timeout(dev->ready_queue,
                                device_is_ready(dev),
                                msecs_to_jiffies(5000));
       
       if (ret == 0)
           return -ETIMEDOUT;  /* Timeout expired */
       
       return 0;  /* Success */
   }

Interruptible with Timeout
---------------------------

.. code-block:: c

   static int wait_for_response(struct device *dev) {
       long ret;
       
       ret = wait_event_interruptible_timeout(dev->response_queue,
                                               dev->response_ready,
                                               HZ * 10);
       
       if (ret == 0)
           return -ETIMEDOUT;
       if (ret == -ERESTARTSYS)
           return -EINTR;
       
       return 0;
   }

Waking Up Waiters
=================

Wake One vs Wake All
--------------------

.. code-block:: c

   static DECLARE_WAIT_QUEUE_HEAD(work_queue);
   
   /* Wake up one waiter (default process) */
   wake_up(&work_queue);
   
   /* Wake up all waiters */
   wake_up_all(&work_queue);
   
   /* Wake up interruptible waiters only */
   wake_up_interruptible(&work_queue);
   wake_up_interruptible_all(&work_queue);

Typical Producer-Consumer
--------------------------

.. code-block:: c

   #define BUFFER_SIZE 128
   
   struct buffer {
       wait_queue_head_t read_queue;
       wait_queue_head_t write_queue;
       spinlock_t lock;
       char data[BUFFER_SIZE];
       int read_pos;
       int write_pos;
       int count;
   };
   
   static int buffer_write(struct buffer *buf, char byte) {
       int ret = 0;
       
       /* Wait for space */
       wait_event_interruptible(buf->write_queue, buf->count < BUFFER_SIZE);
       
       spin_lock(&buf->lock);
       
       if (buf->count < BUFFER_SIZE) {
           buf->data[buf->write_pos] = byte;
           buf->write_pos = (buf->write_pos + 1) % BUFFER_SIZE;
           buf->count++;
       } else {
           ret = -EAGAIN;
       }
       
       spin_unlock(&buf->lock);
       
       /* Wake up readers */
       wake_up_interruptible(&buf->read_queue);
       
       return ret;
   }
   
   static int buffer_read(struct buffer *buf, char *byte) {
       int ret = 0;
       
       /* Wait for data */
       wait_event_interruptible(buf->read_queue, buf->count > 0);
       
       spin_lock(&buf->lock);
       
       if (buf->count > 0) {
           *byte = buf->data[buf->read_pos];
           buf->read_pos = (buf->read_pos + 1) % BUFFER_SIZE;
           buf->count--;
       } else {
           ret = -EAGAIN;
       }
       
       spin_unlock(&buf->lock);
       
       /* Wake up writers */
       wake_up_interruptible(&buf->write_queue);
       
       return ret;
   }

Advanced Wait Operations
========================

Custom Wait Conditions
----------------------

.. code-block:: c

   struct packet_queue {
       wait_queue_head_t wait;
       struct list_head packets;
       int count;
       int max_size;
   };
   
   /* Complex condition */
   static struct packet *dequeue_packet(struct packet_queue *q) {
       struct packet *pkt;
       
       /* Wait for: data available AND not shutting down */
       wait_event_interruptible(q->wait,
                                !list_empty(&q->packets) || 
                                shutdown_requested);
       
       if (shutdown_requested)
           return NULL;
       
       pkt = list_first_entry(&q->packets, struct packet, list);
       list_del(&pkt->list);
       q->count--;
       
       /* Wake writers if there's space */
       if (q->count < q->max_size)
           wake_up(&q->wait);
       
       return pkt;
   }

Manual Wait Queue Handling
---------------------------

For more control over the waiting process:

.. code-block:: c

   static int complex_wait(struct device *dev) {
       DEFINE_WAIT(wait);
       int ret = 0;
       
       /* Prepare to wait */
       prepare_to_wait(&dev->wait_queue, &wait, TASK_INTERRUPTIBLE);
       
       /* Check condition */
       while (!device_ready(dev)) {
           if (signal_pending(current)) {
               ret = -ERESTARTSYS;
               break;
           }
           
           /* Actually sleep */
           schedule();
           
           /* Re-prepare after waking */
           prepare_to_wait(&dev->wait_queue, &wait, TASK_INTERRUPTIBLE);
       }
       
       /* Cleanup */
       finish_wait(&dev->wait_queue, &wait);
       
       return ret;
   }

Exclusive Waits
---------------

Wake only one waiter instead of all (thundering herd avoidance):

.. code-block:: c

   static int exclusive_wait(struct device *dev) {
       DEFINE_WAIT(wait);
       
       prepare_to_wait_exclusive(&dev->wait_queue, &wait,
                                  TASK_INTERRUPTIBLE);
       
       if (!condition)
           schedule();
       
       finish_wait(&dev->wait_queue, &wait);
       
       return 0;
   }
   
   /* Wake up only one exclusive waiter */
   wake_up(&dev->wait_queue);

Wait Queue with Locking
========================

Typical Pattern
---------------

.. code-block:: c

   struct shared_resource {
       spinlock_t lock;
       wait_queue_head_t wait;
       int available;
       void *data;
   };
   
   static int acquire_resource(struct shared_resource *res) {
       int ret;
       
       /* Wait for resource */
       ret = wait_event_interruptible(res->wait, res->available > 0);
       if (ret)
           return -ERESTARTSYS;
       
       spin_lock(&res->lock);
       
       /* Double-check condition under lock */
       if (res->available > 0) {
           res->available--;
           ret = 0;
       } else {
           ret = -EAGAIN;  /* Race - try again */
       }
       
       spin_unlock(&res->lock);
       
       return ret;
   }
   
   static void release_resource(struct shared_resource *res) {
       spin_lock(&res->lock);
       res->available++;
       spin_unlock(&res->lock);
       
       wake_up(&res->wait);
   }

Lock Inside Wait
----------------

.. code-block:: c

   static int wait_and_acquire(struct device *dev) {
       int ret;
       
       ret = wait_event_interruptible(dev->wait_queue,
                                       try_acquire_locked(dev));
       
       return ret;
   }
   
   static bool try_acquire_locked(struct device *dev) {
       bool success = false;
       
       spin_lock(&dev->lock);
       
       if (dev->state == STATE_READY) {
           dev->state = STATE_BUSY;
           success = true;
       }
       
       spin_unlock(&dev->lock);
       
       return success;
   }

Complete Driver Example
=======================

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/wait.h>
   #include <linux/sched.h>
   #include <linux/uaccess.h>
   
   #define DEVICE_NAME "waitdev"
   #define BUFFER_SIZE 4096
   
   struct wait_device {
       struct cdev cdev;
       wait_queue_head_t read_queue;
       wait_queue_head_t write_queue;
       struct mutex lock;
       char buffer[BUFFER_SIZE];
       size_t read_pos;
       size_t write_pos;
       size_t data_len;
       bool eof;
   };
   
   static struct wait_device *wait_dev;
   static dev_t dev_num;
   
   static ssize_t waitdev_read(struct file *filp, char __user *buf,
                                size_t count, loff_t *f_pos) {
       struct wait_device *dev = filp->private_data;
       size_t to_copy;
       int ret;
       
       /* Wait for data or EOF */
       ret = wait_event_interruptible(dev->read_queue,
                                       dev->data_len > 0 || dev->eof);
       if (ret)
           return -ERESTARTSYS;
       
       mutex_lock(&dev->lock);
       
       if (dev->eof && dev->data_len == 0) {
           mutex_unlock(&dev->lock);
           return 0;  /* EOF */
       }
       
       to_copy = min(count, dev->data_len);
       
       if (copy_to_user(buf, dev->buffer + dev->read_pos, to_copy)) {
           mutex_unlock(&dev->lock);
           return -EFAULT;
       }
       
       dev->read_pos = (dev->read_pos + to_copy) % BUFFER_SIZE;
       dev->data_len -= to_copy;
       
       mutex_unlock(&dev->lock);
       
       /* Wake up writers if there's space */
       wake_up_interruptible(&dev->write_queue);
       
       return to_copy;
   }
   
   static ssize_t waitdev_write(struct file *filp, const char __user *buf,
                                 size_t count, loff_t *f_pos) {
       struct wait_device *dev = filp->private_data;
       size_t free_space;
       size_t to_copy;
       int ret;
       
       /* Wait for space */
       ret = wait_event_interruptible(dev->write_queue,
                                       dev->data_len < BUFFER_SIZE);
       if (ret)
           return -ERESTARTSYS;
       
       mutex_lock(&dev->lock);
       
       free_space = BUFFER_SIZE - dev->data_len;
       to_copy = min(count, free_space);
       
       if (copy_from_user(dev->buffer + dev->write_pos, buf, to_copy)) {
           mutex_unlock(&dev->lock);
           return -EFAULT;
       }
       
       dev->write_pos = (dev->write_pos + to_copy) % BUFFER_SIZE;
       dev->data_len += to_copy;
       
       mutex_unlock(&dev->lock);
       
       /* Wake up readers */
       wake_up_interruptible(&dev->read_queue);
       
       return to_copy;
   }
   
   static long waitdev_ioctl(struct file *filp, unsigned int cmd,
                              unsigned long arg) {
       struct wait_device *dev = filp->private_data;
       
       switch (cmd) {
       case 0:  /* Signal EOF */
           mutex_lock(&dev->lock);
           dev->eof = true;
           mutex_unlock(&dev->lock);
           wake_up_interruptible(&dev->read_queue);
           return 0;
       default:
           return -EINVAL;
       }
   }
   
   static int waitdev_open(struct inode *inode, struct file *filp) {
       struct wait_device *dev;
       
       dev = container_of(inode->i_cdev, struct wait_device, cdev);
       filp->private_data = dev;
       
       mutex_lock(&dev->lock);
       dev->read_pos = 0;
       dev->write_pos = 0;
       dev->data_len = 0;
       dev->eof = false;
       mutex_unlock(&dev->lock);
       
       return 0;
   }
   
   static const struct file_operations waitdev_fops = {
       .owner = THIS_MODULE,
       .open = waitdev_open,
       .read = waitdev_read,
       .write = waitdev_write,
       .unlocked_ioctl = waitdev_ioctl,
   };
   
   static int __init waitdev_init(void) {
       int ret;
       
       ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
       if (ret < 0)
           return ret;
       
       wait_dev = kzalloc(sizeof(*wait_dev), GFP_KERNEL);
       if (!wait_dev) {
           unregister_chrdev_region(dev_num, 1);
           return -ENOMEM;
       }
       
       init_waitqueue_head(&wait_dev->read_queue);
       init_waitqueue_head(&wait_dev->write_queue);
       mutex_init(&wait_dev->lock);
       
       cdev_init(&wait_dev->cdev, &waitdev_fops);
       wait_dev->cdev.owner = THIS_MODULE;
       
       ret = cdev_add(&wait_dev->cdev, dev_num, 1);
       if (ret) {
           kfree(wait_dev);
           unregister_chrdev_region(dev_num, 1);
           return ret;
       }
       
       pr_info("Wait device initialized: major=%d\n", MAJOR(dev_num));
       return 0;
   }
   
   static void __exit waitdev_exit(void) {
       cdev_del(&wait_dev->cdev);
       kfree(wait_dev);
       unregister_chrdev_region(dev_num, 1);
       pr_info("Wait device removed\n");
   }
   
   module_init(waitdev_init);
   module_exit(waitdev_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Kernel Developer");
   MODULE_DESCRIPTION("Wait Queue Example Driver");

Common Patterns
===============

Interrupt Handler Pattern
--------------------------

.. code-block:: c

   static irqreturn_t device_irq(int irq, void *dev_id) {
       struct device *dev = dev_id;
       
       /* Read and clear interrupt status */
       dev->status = read_status_register(dev);
       
       /* Wake up waiters */
       wake_up(&dev->irq_queue);
       
       return IRQ_HANDLED;
   }
   
   static int wait_for_interrupt(struct device *dev, u32 expected) {
       int ret;
       
       ret = wait_event_timeout(dev->irq_queue,
                                dev->status & expected,
                                HZ * 5);
       
       if (ret == 0)
           return -ETIMEDOUT;
       
       return 0;
   }

Polling with Wait
-----------------

.. code-block:: c

   static unsigned int device_poll(struct file *filp,
                                    struct poll_table_struct *wait) {
       struct device *dev = filp->private_data;
       unsigned int mask = 0;
       
       poll_wait(filp, &dev->read_queue, wait);
       poll_wait(filp, &dev->write_queue, wait);
       
       if (data_available(dev))
           mask |= POLLIN | POLLRDNORM;
       
       if (space_available(dev))
           mask |= POLLOUT | POLLWRNORM;
       
       return mask;
   }

Performance Considerations
==========================

Avoid Thundering Herd
---------------------

.. code-block:: c

   /* Bad: wake_up_all wakes everyone */
   wake_up_all(&work_queue);
   
   /* Good: wake_up wakes one exclusive waiter */
   wake_up(&work_queue);

Minimize Lock Hold Time
------------------------

.. code-block:: c

   /* Good pattern */
   spin_lock(&dev->lock);
   condition_met = check_and_update(dev);
   spin_unlock(&dev->lock);
   
   if (condition_met)
       wake_up(&dev->wait_queue);

Common Pitfalls
===============

1. **Not checking condition in loop**
2. **Forgetting wake_up after changing condition**
3. **Race between condition check and wait**
4. **Deadlock from lock ordering**
5. **Holding locks across schedule()**

Best Practices
==============

1. **Always use wait_event macros** when possible
2. **Check condition under lock** if needed
3. **Use interruptible waits** for user-space facing code
4. **Add timeouts** to avoid infinite waits
5. **Document** what condition you're waiting for
6. **Test** signal handling and timeouts
7. **Consider exclusive waits** for scalability

See Also
========

- Linux_Kernel_Synchronization.rst
- Linux_Mutexes_Semaphores.rst
- Linux_Spinlocks.rst
- Linux_Kernel_Locking_Patterns.rst

References
==========

- Documentation/scheduler/completion.rst
- include/linux/wait.h
- kernel/sched/wait.c
