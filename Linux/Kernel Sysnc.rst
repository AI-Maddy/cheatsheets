
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


Here is a concise **Linux Kernel Synchronization Cheat Sheet**  
(oriented toward modern kernels 5.15–6.12+, as of early 2026)

⚙️ 1. Quick Comparison Table – Main Synchronization Primitives

Primitive              | Scope              | Reentrant? | Can sleep? | 🟢 🟢 Best for                          | Overhead | Notes / Modern Preference
-----------------------|--------------------|------------|------------|-----------------------------------|----------|---------------------------
⭐ spinlock_t             | CPU / short critical | No         | No         | Very short, IRQ / softirq / BH    | Very low | Still king for hot paths
raw_spinlock_t         | CPU                | No         | No         | NMI / very low-level (irqdesc etc)| Lowest   | Rarely use directly
rwlock_t               | CPU                | No (read)  | No         | Read-mostly, short sections       | Low      | Deprecated in favor of RCU
⭐ mutex                  | Process            | Yes        | Yes        | Longer critical sections, sleep OK| Medium   | Most common “sleeping lock”
semaphore              | Process            | No         | Yes        | Counting (rare now)               | Medium   | Mostly legacy
completion             | Process            | —          | Yes        | Wait for one-time event           | —        | Very clean pattern
wait_queue_head_t      | Process            | —          | Yes        | Wait for condition                | —        | Use with wake_up()
rcu_read_lock()        | Global (grace)     | Yes        | No         | Read-mostly data structures       | Extremely low | Preferred for read-side scaling
srcu_struct            | Per-instance       | Yes        | Yes (sleepable) | Sleepable RCU variant          | Low      | 🟢 🟢 Good for module unload paths
seqlock_t              | CPU                | No         | No (reader) | Fast reader, infrequent writer    | Very low | seqcount + spinlock combo
seqcount_t             | CPU                | No         | No         | Pure sequence lock (no spin)      | Lowest   | Reader must retry on seq change

🏗️ 2. Most Common Patterns (2025–2026 style)

**Spinlock (classic hot-path protection)**

.. code-block:: c

spinlock_t my_lock;
spin_lock_init(&my_lock);

spin_lock(&my_lock);
⭐ ... very short critical section ...
spin_unlock(&my_lock);

IRQ-safe variants:

.. code-block:: c

spin_lock_irqsave(&lock, flags);   // disable interrupts on this CPU
spin_unlock_irqrestore(&lock, flags);

spin_lock_bh(&lock);               // disable softirqs
spin_unlock_bh(&lock);

**Mutex (longer sections, can sleep)**

.. code-block:: c

struct mutex my_mutex;
mutex_init(&my_mutex);

mutex_lock(&my_mutex);
... can sleep, can be preempted ...
mutex_unlock(&my_mutex);

**RCU – Read-mostly classic (preferred when reads >> writes)**

.. code-block:: c

rcu_read_lock();
p = rcu_dereference(my_pointer);
if (p)
    do_something_read_only(p);
rcu_read_unlock();

Writer side (two common styles):

.. code-block:: c

// Style 1: synchronize_rcu() – blocks until old readers finish
old = my_pointer;
rcu_assign_pointer(my_pointer, new_struct);
synchronize_rcu();          // wait for grace period
kfree(old);

// Style 2: call_rcu() – non-blocking (preferred in hot paths)
old = my_pointer;
rcu_assign_pointer(my_pointer, new_struct);
call_rcu(&old->rcu, my_free_cb);

**Sleepable RCU (SRCU) – when reader can sleep**

.. code-block:: c

static struct srcu_struct my_srcu;

idx = srcu_read_lock(&my_srcu);
... can sleep ...
srcu_read_unlock(&my_srcu, idx);

synchronize_srcu(&my_srcu);     // or call_srcu()

**Seqlock (very fast readers)**

.. code-block:: c

seqlock_t my_seqlock;
seqcount_init(&my_seqlock);

🟢 🟢 do {
    seq = read_seqbegin(&my_seqlock);
⭐     copy_important_data(...);
} while (read_seqretry(&my_seqlock, seq));

write_seqlock(&my_seqlock);
... update data ...
write_sequnlock(&my_seqlock);

🐛 3. Lockdep & Debugging Helpers

Macro / Function               | Purpose
-------------------------------|--------------------------------------------------
``lockdep_assert_held(&lock)``   | Compile-time + runtime check that lock is held
``assert_spin_locked(&lock)``    | Same for spinlocks (shorter)
``lockdep_is_held(&lock)``       | Runtime check (returns bool)
``might_sleep()``                | Warn if called from atomic context
``debug_lockdep_rcu_enabled()``  | Check if lockdep+RCU debugging is active
``/proc/lockdep*``               | lockdep statistics & dependency chains
``CONFIG_PROVE_LOCKING=y``       | Enable full lockdep (expensive)
``CONFIG_DEBUG_SPINLOCK=y``      | Catch common spinlock bugs
``CONFIG_DEBUG_MUTEXES=y``       | Catch double-unlock, use-after-free etc.

📚 4. Atomic Operations Quick Reference

Operation                       | Use when
--------------------------------|-------------------------------------------------
``atomic_t`` / ``atomic64_t``       | Simple counters (refcounts, stats)
``atomic_read()``, ``atomic_set()`` | —
``atomic_inc_not_zero()``         | Safe refcount increment
``atomic_add_unless()``           | Increment unless == value
``atomic_xchg()``                 | Exchange value, return old
``atomic_cmpxchg()``              | Compare-and-swap

**refcount_t** (preferred over plain atomic_t for references)

.. code-block:: c

refcount_t ref;
refcount_set(&ref, 1);
refcount_inc(&ref);
if (refcount_dec_and_test(&ref))
    kfree(obj);

🐧 5. Modern Recommendations (2025–2026 kernels)

Scenario                              | Preferred primitive
--------------------------------------|-------------------------
⭐ Very short critical section (< few μs) | ``spin_lock()``
Read-mostly data structure            | RCU (rcu_read_lock / call_rcu)
Longer section, can sleep             | ``mutex_lock()``
Fast readers, rare writers            | ``seqlock_t`` / ``seqcount_t``
Need to wait for event                | ``wait_event()`` + ``wake_up()``
One-time wait (probe / init)          | ``completion``
Per-CPU data                          | ``this_cpu_*`` / per_cpu variables + RCU
Module unload safety                  | SRCU or ``rcu_access_pointer()``
Reference counting                    | ``refcount_t`` (not plain atomic_t)

📌 6. Quick Lock Order Rules (🔴 🔴 avoid ABBA deadlock)

Always acquire locks in the same order:

.. code-block:: text

irq_desc->lock → task_struct->pi_lock → rq->lock → mm->mmap_lock
                ↑
             page lock
                ↑
             inode->i_lock

Use lockdep to catch violations automatically.

🟢 🟢 Good luck writing lock-safe kernel code!  
⭐ Most new drivers in 2026 use **mutex + RCU** combo or pure **RCU** for performance-critical paths. Start simple with mutex, graduate to RCU when profiling shows contention.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
