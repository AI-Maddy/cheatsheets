===================================
Linux Process Management
===================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Focus: Process lifecycle, creation, termination, and management

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Process Lifecycle
-----------------

.. code-block:: text

   Process States:
   
   TASK_RUNNING ──┐
                  ├──→ Running on CPU
                  └──→ Runnable (waiting for CPU)
   
   TASK_INTERRUPTIBLE ──→ Sleeping (can be interrupted by signals)
   
   TASK_UNINTERRUPTIBLE ──→ Sleeping (cannot be interrupted)
   
   __TASK_STOPPED ──→ Stopped (SIGSTOP, SIGTSTP)
   
   __TASK_TRACED ──→ Being traced (ptrace, debugger)
   
   EXIT_ZOMBIE ──→ Terminated, waiting for parent
   
   EXIT_DEAD ──→ Final state, being removed
   
   Process Creation:
   fork() → clone() → copy_process() → wake_up_new_task()
   
   Process Termination:
   exit() → do_exit() → EXIT_ZOMBIE → wait() → EXIT_DEAD

Essential Process APIs
----------------------

.. code-block:: c

   // Process creation
   pid_t fork(void);
   pid_t vfork(void);
   int clone(int (*fn)(void *), void *stack, int flags, void *arg);
   
   // Process termination
   void exit(int status);
   void _exit(int status);
   
   // Wait for child
   pid_t wait(int *status);
   pid_t waitpid(pid_t pid, int *status, int options);
   
   // Execute new program
   int execve(const char *filename, char *const argv[], char *const envp[]);
   
   // Process info
   pid_t getpid(void);
   pid_t getppid(void);
   uid_t getuid(void);
   gid_t getgid(void);

Process Representation
=======================

Task Struct
-----------

.. code-block:: c

   // include/linux/sched.h
   struct task_struct {
       // Process state
       volatile long state;              // -1=unrunnable, 0=runnable, >0=stopped
       unsigned int flags;               // Per-process flags
       int exit_state;                   // Exit state
       int exit_code, exit_signal;       // Exit code and signal
       
       // Process IDs
       pid_t pid;                        // Process ID
       pid_t tgid;                       // Thread group ID (main thread PID)
       
       // Process relationships
       struct task_struct __rcu *real_parent;  // Real parent
       struct task_struct __rcu *parent;       // Recipient of SIGCHLD
       struct list_head children;        // List of children
       struct list_head sibling;         // Sibling processes
       struct task_struct *group_leader; // Thread group leader
       
       // Credentials
       const struct cred __rcu *real_cred;     // Objective credentials
       const struct cred __rcu *cred;          // Effective credentials
       
       // Scheduling
       int prio, static_prio, normal_prio;  // Priority values
       unsigned int policy;              // Scheduling policy
       cpumask_t cpus_allowed;           // CPU affinity mask
       struct sched_entity se;           // CFS scheduling entity
       struct sched_rt_entity rt;        // RT scheduling entity
       struct sched_dl_entity dl;        // Deadline scheduling entity
       
       // Memory management
       struct mm_struct *mm, *active_mm; // Memory descriptor
       
       // File system
       struct fs_struct *fs;             // Filesystem information
       struct files_struct *files;       // Open file descriptors
       struct nsproxy *nsproxy;          // Namespaces
       
       // Signal handling
       struct signal_struct *signal;     // Signal handlers
       struct sighand_struct *sighand;   // Signal handlers
       sigset_t blocked, real_blocked;   // Blocked signals
       struct sigpending pending;        // Pending signals
       
       // CPU state
       struct thread_struct thread;      // CPU-specific context
       void *stack;                      // Kernel stack
       
       // Timers
       struct task_cputime cputime_expires;
       struct list_head cpu_timers[3];
       
       // Audit
       kuid_t loginuid;
       unsigned int sessionid;
       
       // Performance monitoring
       struct perf_event_context *perf_event_ctxp;
       
       // ... hundreds more fields
   };

PID Management
--------------

.. code-block:: c

   struct pid {
       atomic_t count;
       unsigned int level;               // Namespace level
       struct hlist_head tasks[PIDTYPE_MAX];  // Tasks using this PID
       struct rcu_head rcu;
       struct upid numbers[1];           // PID namespace
   };
   
   enum pid_type {
       PIDTYPE_PID,                      // Process ID
       PIDTYPE_TGID,                     // Thread group ID
       PIDTYPE_PGID,                     // Process group ID
       PIDTYPE_SID,                      // Session ID
       PIDTYPE_MAX
   };
   
   // Get task from PID
   struct task_struct *find_task_by_vpid(pid_t nr) {
       return find_task_by_pid_ns(nr, task_active_pid_ns(current));
   }
   
   struct task_struct *find_task_by_pid_ns(pid_t nr, struct pid_namespace *ns) {
       return pid_task(find_pid_ns(nr, ns), PIDTYPE_PID);
   }

Process Creation
================

Fork System Call
----------------

.. code-block:: c

   // Fork creates child process
   SYSCALL_DEFINE0(fork) {
       return _do_fork(SIGCHLD, 0, 0, NULL, NULL, 0);
   }
   
   // Vfork: child runs first, parent waits
   SYSCALL_DEFINE0(vfork) {
       return _do_fork(CLONE_VFORK | CLONE_VM | SIGCHLD,
                      0, 0, NULL, NULL, 0);
   }
   
   // Clone: flexible process/thread creation
   SYSCALL_DEFINE5(clone, unsigned long, clone_flags,
                   unsigned long, newsp,
                   int __user *, parent_tidptr,
                   int __user *, child_tidptr,
                   unsigned long, tls) {
       return _do_fork(clone_flags, newsp, 0, parent_tidptr,
                      child_tidptr, tls);
   }

Clone Flags
-----------

.. code-block:: c

   // Clone flags
   #define CLONE_VM        0x00000100  // Share memory space
   #define CLONE_FS        0x00000200  // Share filesystem info
   #define CLONE_FILES     0x00000400  // Share file descriptors
   #define CLONE_SIGHAND   0x00000800  // Share signal handlers
   #define CLONE_PIDFD     0x00001000  // Return pidfd
   #define CLONE_PTRACE    0x00002000  // Child is traced
   #define CLONE_VFORK     0x00004000  // Parent waits for child
   #define CLONE_PARENT    0x00008000  // Same parent as caller
   #define CLONE_THREAD    0x00010000  // Same thread group
   #define CLONE_NEWNS     0x00020000  // New mount namespace
   #define CLONE_SYSVSEM   0x00040000  // Share SysV semaphore undo
   #define CLONE_SETTLS    0x00080000  // Set TLS
   #define CLONE_PARENT_SETTID  0x00100000  // Set parent TID
   #define CLONE_CHILD_CLEARTID 0x00200000  // Clear child TID
   #define CLONE_DETACHED  0x00400000  // Unused
   #define CLONE_UNTRACED  0x00800000  // Not traced
   #define CLONE_CHILD_SETTID   0x01000000  // Set child TID
   #define CLONE_NEWCGROUP 0x02000000  // New cgroup namespace
   #define CLONE_NEWUTS    0x04000000  // New utsname namespace
   #define CLONE_NEWIPC    0x08000000  // New IPC namespace
   #define CLONE_NEWUSER   0x10000000  // New user namespace
   #define CLONE_NEWPID    0x20000000  // New PID namespace
   #define CLONE_NEWNET    0x40000000  // New network namespace
   #define CLONE_IO        0x80000000  // Clone I/O context

Copy Process
------------

.. code-block:: c

   // Create new process
   static struct task_struct *copy_process(unsigned long clone_flags,
                                          unsigned long stack_start,
                                          unsigned long stack_size,
                                          int __user *parent_tidptr,
                                          int __user *child_tidptr,
                                          unsigned long tls) {
       struct task_struct *p;
       int retval;
       
       // Allocate new task_struct
       p = dup_task_struct(current);
       if (!p)
           return ERR_PTR(-ENOMEM);
       
       // Check limits
       if (atomic_read(&p->real_cred->user->processes) >=
           task_rlimit(p, RLIMIT_NPROC)) {
           if (p->real_cred->user != INIT_USER &&
               !capable(CAP_SYS_ADMIN) && !capable(CAP_SYS_RESOURCE))
               goto bad_fork_free;
       }
       
       // Initialize fields
       retval = copy_creds(p, clone_flags);
       if (retval < 0)
           goto bad_fork_free;
       
       retval = copy_semundo(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_audit;
       
       retval = copy_files(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_semundo;
       
       retval = copy_fs(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_files;
       
       retval = copy_sighand(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_fs;
       
       retval = copy_signal(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_sighand;
       
       retval = copy_mm(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_signal;
       
       retval = copy_namespaces(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_mm;
       
       retval = copy_io(clone_flags, p);
       if (retval)
           goto bad_fork_cleanup_namespaces;
       
       retval = copy_thread_tls(clone_flags, stack_start, stack_size, p, tls);
       if (retval)
           goto bad_fork_cleanup_io;
       
       // Assign PID
       if (pid != &init_struct_pid) {
           pid = alloc_pid(p->nsproxy->pid_ns_for_children);
           if (IS_ERR(pid)) {
               retval = PTR_ERR(pid);
               goto bad_fork_cleanup_thread;
           }
       }
       
       p->pid = pid_nr(pid);
       
       if (clone_flags & CLONE_THREAD) {
           p->tgid = current->tgid;
       } else {
           p->tgid = p->pid;
       }
       
       return p;
       
   bad_fork_cleanup_thread:
       // Cleanup on error...
       free_task(p);
       return ERR_PTR(retval);
   }

Wake New Task
-------------

.. code-block:: c

   void wake_up_new_task(struct task_struct *p) {
       struct rq *rq;
       unsigned long flags;
       
       raw_spin_lock_irqsave(&p->pi_lock, flags);
       
       // Set task CPU
       set_task_cpu(p, select_task_rq(p, task_cpu(p), SD_BALANCE_FORK, 0));
       
       p->state = TASK_RUNNING;
       
       rq = __task_rq_lock(p);
       activate_task(rq, p, ENQUEUE_NOCLOCK);
       p->on_rq = TASK_ON_RQ_QUEUED;
       check_preempt_curr(rq, p, WF_FORK);
       task_rq_unlock(rq, p, &flags);
   }

Process Termination
===================

Exit System Call
----------------

.. code-block:: c

   SYSCALL_DEFINE1(exit, int, error_code) {
       do_exit((error_code & 0xff) << 8);
   }
   
   // Process exit
   void __noreturn do_exit(long code) {
       struct task_struct *tsk = current;
       int group_dead;
       
       // Set exit code
       tsk->exit_code = code;
       
       // Exit signals
       exit_signals(tsk);
       
       // Release resources
       exit_mm(tsk);           // Release memory
       exit_sem(tsk);          // Release semaphores
       exit_shm(tsk);          // Release shared memory
       exit_files(tsk);        // Close files
       exit_fs(tsk);           // Release filesystem
       exit_thread(tsk);       // Arch-specific cleanup
       exit_notify(tsk, group_dead);  // Notify parent
       
       // Become zombie
       tsk->state = TASK_DEAD;
       tsk->exit_state = EXIT_ZOMBIE;
       
       // Schedule out (never returns)
       schedule();
       BUG();
   }

Zombie Process
--------------

.. code-block:: c

   // Zombie: terminated but not yet reaped by parent
   // Remains in process table until parent calls wait()
   
   static void exit_notify(struct task_struct *tsk, int group_dead) {
       bool autoreap;
       struct task_struct *p, *n;
       
       // Reparent children to init
       forget_original_parent(tsk);
       
       // Notify parent
       if (thread_group_leader(tsk)) {
           autoreap = do_notify_parent(tsk, tsk->exit_signal);
       } else {
           autoreap = true;
       }
       
       tsk->exit_state = autoreap ? EXIT_DEAD : EXIT_ZOMBIE;
       
       // Wake up parent
       if (tsk->exit_state == EXIT_ZOMBIE && unlikely(tsk->ptrace))
           wake_up_parent(tsk);
   }

Wait System Call
----------------

.. code-block:: c

   SYSCALL_DEFINE4(wait4, pid_t, upid, int __user *, stat_addr,
                   int, options, struct rusage __user *, ru) {
       struct wait_opts wo;
       struct pid *pid = NULL;
       enum pid_type type;
       long ret;
       
       if (options & ~(WNOHANG|WUNTRACED|WCONTINUED|__WNOTHREAD|
                      __WCLONE|__WALL))
           return -EINVAL;
       
       if (upid == -1)
           type = PIDTYPE_MAX;
       else if (upid < 0)
           type = PIDTYPE_PGID, pid = find_get_pid(-upid);
       else if (upid == 0)
           type = PIDTYPE_PGID, pid = get_task_pid(current, PIDTYPE_PGID);
       else
           type = PIDTYPE_PID, pid = find_get_pid(upid);
       
       wo.wo_type = type;
       wo.wo_pid = pid;
       wo.wo_flags = options;
       wo.wo_info = NULL;
       wo.wo.wo_stat = stat_addr;
       wo.wo_rusage = ru;
       
       ret = do_wait(&wo);
       put_pid(pid);
       
       return ret;
   }
   
   // Reap zombie child
   static long do_wait(struct wait_opts *wo) {
       struct task_struct *tsk;
       int retval;
       
       do {
           // Check for eligible children
           tsk = current;
           do {
               retval = do_wait_thread(wo, tsk);
               if (retval)
                   goto end;
               
               retval = ptrace_do_wait(wo, tsk);
               if (retval)
                   goto end;
               
               if (wo->wo_flags & __WNOTHREAD)
                   break;
           } while_each_thread(current, tsk);
           
           // Sleep if no children ready
           if (!(wo->wo_flags & WNOHANG)) {
               set_current_state(TASK_INTERRUPTIBLE);
               if (!signal_pending(current)) {
                   schedule();
                   continue;
               }
           }
           retval = -ECHILD;
       } while (!retval);
       
   end:
       __set_current_state(TASK_RUNNING);
       return retval;
   }

Exec System Call
================

Exec Implementation
-------------------

.. code-block:: c

   // Replace current process image
   SYSCALL_DEFINE3(execve,
                   const char __user *, filename,
                   const char __user *const __user *, argv,
                   const char __user *const __user *, envp) {
       return do_execve(getname(filename), argv, envp);
   }
   
   static int do_execve(struct filename *filename,
                       const char __user *const __user *argv,
                       const char __user *const __user *envp) {
       struct linux_binprm *bprm;
       int retval;
       
       // Allocate binary parameter structure
       bprm = alloc_bprm(0, NULL);
       if (IS_ERR(bprm))
           return PTR_ERR(bprm);
       
       // Prepare execution
       retval = prepare_bprm_creds(bprm);
       if (retval)
           goto out_free;
       
       // Copy arguments and environment
       retval = copy_strings_kernel(1, &bprm->filename, bprm);
       if (retval < 0)
           goto out;
       
       bprm->exec = bprm->p;
       retval = copy_strings(bprm->envc, envp, bprm);
       if (retval < 0)
           goto out;
       
       retval = copy_strings(bprm->argc, argv, bprm);
       if (retval < 0)
           goto out;
       
       // Execute binary
       retval = exec_binprm(bprm);
       if (retval < 0)
           goto out;
       
       return retval;
       
   out_free:
       free_bprm(bprm);
   out:
       return retval;
   }

Signal Handling
===============

Signal Structure
----------------

.. code-block:: c

   struct signal_struct {
       atomic_t sigcnt;
       atomic_t live;
       int nr_threads;
       
       wait_queue_head_t wait_chldexit;
       struct task_struct *curr_target;
       struct sigpending shared_pending;
       
       int group_exit_code;
       int notify_count;
       struct task_struct *group_exit_task;
       
       // Statistics
       cputime_t utime, stime, cutime, cstime;
       cputime_t gtime, cgtime;
       struct prev_cputime prev_cputime;
       unsigned long nvcsw, nivcsw, cnvcsw, cnivcsw;
       unsigned long min_flt, maj_flt, cmin_flt, cmaj_flt;
   };
   
   struct sighand_struct {
       atomic_t count;
       struct k_sigaction action[_NSIG];
       spinlock_t siglock;
       wait_queue_head_t signalfd_wqh;
   };

Send Signal
-----------

.. code-block:: c

   // Send signal to process
   int send_sig(int sig, struct task_struct *p, int priv) {
       return send_sig_info(sig, __si_special(priv), p);
   }
   
   int send_sig_info(int sig, struct siginfo *info, struct task_struct *p) {
       return do_send_sig_info(sig, info, p, PIDTYPE_PID);
   }
   
   static int do_send_sig_info(int sig, struct siginfo *info,
                               struct task_struct *p, enum pid_type type) {
       unsigned long flags;
       int ret = -ESRCH;
       
       if (lock_task_sighand(p, &flags)) {
           ret = send_signal(sig, info, p, type);
           unlock_task_sighand(p, &flags);
       }
       
       return ret;
   }

Best Practices
==============

1. **Handle fork errors** - check return value
2. **Reap zombies** - always wait() for children
3. **Close file descriptors** in child after fork
4. **Use vfork carefully** - only when immediately exec'ing
5. **Check exec errors** - exec only returns on error
6. **Handle signals properly** - set handlers before fork
7. **Clean up resources** on exit
8. **Avoid orphans** - ensure proper process hierarchy
9. **Use clone flags correctly** - understand sharing implications
10. **Monitor process limits** - RLIMIT_NPROC

Common Pitfalls
===============

1. **Zombie processes** - not calling wait()
2. **Resource leaks** - not closing fds in child
3. **Double fork** - forgetting to exit in middle process
4. **Signal race** - signals lost during fork
5. **Memory leaks** - COW not working as expected
6. **File descriptor** inheritance issues
7. **PID namespace** confusion

Quick Reference
===============

.. code-block:: c

   // Process creation
   pid = fork();
   if (pid == 0) {
       // Child process
       execve("/bin/sh", argv, envp);
       _exit(1);
   } else if (pid > 0) {
       // Parent process
       waitpid(pid, &status, 0);
   }
   
   // Thread creation
   clone(CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD);
   
   // Exit
   exit(0);        // Clean exit with stdio flush
   _exit(0);       // Direct exit without cleanup

See Also
========

- Linux_Kernel_Architecture.rst
- Linux_CPU_Scheduling_Internals.rst
- Linux_Memory_Management_Internals.rst

References
==========

- kernel/fork.c in Linux source
- kernel/exit.c in Linux source
- https://www.kernel.org/doc/html/latest/
