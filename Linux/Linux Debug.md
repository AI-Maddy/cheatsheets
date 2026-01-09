Here is a comprehensive **cheatsheet for Linux kernel debug, trace, profile tools, frameworks, and methodologies** (as of early 2026, kernel ~6.12+ era). This focuses on the most relevant and actively used technologies.

### Debugging Fundamentals

**Three Core Activities:**

1. **Profiling** - Measuring resource usage (CPU, memory, I/O) to find bottlenecks
2. **Tracing** - Recording all events/calls to understand behavior sequence
3. **Debugging** - Stepping through code, inspecting state at runtime

**Performance Analysis Checklist:**

- **Is the system responsive?** (latency vs throughput trade-off)
- **Which process/thread is slow?** (userspace or kernel?)
- **What resource is bottleneck?** (CPU, memory, disk I/O, network)
- **How much overhead do tools add?** (measurement bias)
- **Can I reproduce the issue?** (race conditions are hard)

**Sampling vs Instrumentation Trade-off:**

| Approach | Overhead | Accuracy | Best For |
|----------|----------|----------|----------|
| **Sampling** (Periodic snapshots) | Low | Good (statistical) | CPU profiles, sustained issues |
| **Instrumentation** (Every event) | High | Exact | Rare/specific events, counting |
| **Hybrid** (Smart sampling + instrumentation) | Low–Medium | Very good | bpftrace, perf with filters |

### Tool Deep Dives

**ftrace (Function Tracer – Always Built-in)**

Kernel tracing framework, no special packages needed. Located at `/sys/kernel/tracing/` (or `/sys/kernel/debug/tracing/` on older kernels).

Key features:
- Function-level tracing with `function` tracer
- Call graph visualization with `function_graph` tracer
- Tracepoints (stable ABI) via `trace-on-off` mechanism
- Low overhead when not active
- Ring buffer (circular, doesn't fill up)

Common tracers:
```bash
# List available tracers
cat /sys/kernel/tracing/available_tracers

# Enable function tracer (trace all kernel functions)
echo function > /sys/kernel/tracing/current_tracer

# Function graph tracer (shows call tree with timings)
echo function_graph > /sys/kernel/tracing/current_tracer

# Nop (disable)
echo nop > /sys/kernel/tracing/current_tracer

# View current trace
cat /sys/kernel/tracing/trace

# Clear trace buffer
echo > /sys/kernel/tracing/trace

# Enable tracepoints (more selective than function)
echo 1 > /sys/kernel/tracing/events/syscalls/sys_enter_read/enable
echo 1 > /sys/kernel/tracing/events/block/block_rq_issue/enable
```

Filtering:
```bash
# Only trace specific functions (glob patterns OK)
echo 'vfs*' > /sys/kernel/tracing/set_ftrace_filter

# Exclude functions
echo '!vfs_read' > /sys/kernel/tracing/set_ftrace_notrace

# Show which functions matched
cat /sys/kernel/tracing/available_filter_functions | grep vfs | head

# Function trace specific process (PID filter)
echo 'p:my_event do_syscall_trace_enter' > /sys/kernel/tracing/kprobe_events
echo 'filter: common_pid == 1234' > /sys/kernel/tracing/events/tracepoints/my_event/filter
```

**perf (Performance Events – Best General-Purpose Tool)**

Userspace tool + kernel subsystem (`perf_events`) for profiling and event tracing.

Installation: Usually pre-installed on most distros, or `apt install linux-tools`

Common operations:
```bash
# Record CPU profile (sampling at 99 Hz)
perf record -F 99 -g -- sleep 30

# View profile in TUI
perf report

# Show all available events
perf list

# CPU cycles and instructions with branches
perf stat -e cycles,instructions,branch-misses ./myapp

# Record only user-space (exclude kernel)
perf record -F 99 --exclude-kernel -- ./myapp

# Record with specific event
perf record -e cache-misses -g -- sleep 10

# Show live profiling (like top)
perf top -F 99 -g

# Annotate specific function
perf annotate my_function

# System-wide profiling (all processes, needs root)
perf record -a -F 99 sleep 30

# Trace specific syscalls
perf trace -e open,read,write -- ./myapp

# Measure context switches
perf stat -e context-switches -i 0.1 sleep 5

# Lock contention analysis
perf lock record -- ./myapp
perf lock report
```

**bpftrace (High-Level eBPF One-Liners)**

Modern tool for ad-hoc kernel tracing without writing C code.

Installation: `apt install bpftrace` (requires kernel 4.18+, LLVM)

Strengths:
- Very concise syntax (like awk/DTrace)
- Runs directly in kernel (low overhead)
- Supports maps, histograms, aggregation
- Fast prototyping

Examples:
```bash
# Trace all open() syscalls with arguments
bpftrace -e 'tracepoint:syscalls:sys_enter_open* { printf("%s(%s)\n", comm, str(args[0])); }'

# Print system call count by process
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

# Histogram of system call latencies (nanoseconds)
bpftrace -e 'tracepoint:syscalls:sys_enter_read { @start[tid] = nsecs; }
             tracepoint:syscalls:sys_exit_read /@start[tid]/ { 
               @lat[comm] = hist(nsecs - @start[tid]); 
               delete(@start[tid]); 
             }'

# Block I/O latency (device I/O performance)
bpftrace -e 'tracepoint:block:block_rq_issue { @start[args[0]] = nsecs; }
             tracepoint:block:block_rq_complete /@start[args[0]]/ {
               @usecs = hist((nsecs - @start[args[0]]) / 1000);
               delete(@start[args[0]]);
             }'

# CPU profile (what functions running most)
bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'

# Find slow malloc() calls
bpftrace -e 'uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc { @malloc_time[tid] = nsecs; }
             uretprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc /@malloc_time[tid]/ {
               @malloc_latency = hist(nsecs - @malloc_time[tid]);
               delete(@malloc_time[tid]);
             }'

# Count page faults by process
bpftrace -e 'software:page-faults { @[comm] = count(); }'

# Trace file reads and write sizes
bpftrace -e 'tracepoint:syscalls:sys_enter_read { @reads[comm] = sum(args[2]); }
             tracepoint:syscalls:sys_enter_write { @writes[comm] = sum(args[2]); }'
```

**bcc (BPF Compiler Collection – Reusable Tools)**

Python + C framework for building eBPF tools and agents.

Installation: `apt install bpfcc-tools` or build from source

Common pre-built tools:
```bash
# Block device I/O latency
biolatency

# Off-CPU time (why threads not running)
offcputime

# CPU flame graph
profile

# Memory allocation tracking
memleak

# File system reads/writes
vfscount

# Syscall tracing
trace

# TCP connection tracking
tcpconnect
tcpaccept

# Network packet loss
tcpdrop
```

Example: Off-CPU analysis
```bash
# Record 10 seconds of off-CPU time for specific process
offcputime -f -p 1234 10 > offcpu.stacks

# Convert to flame graph
cat offcpu.stacks | FlameGraph/flamegraph.pl > offcpu.svg
```

**trace-cmd & KernelShark (ftrace GUI)**

Graphical frontend to ftrace, great for exploring complex traces.

```bash
# Record trace with multiple events
trace-cmd record -e sched:sched_switch -e block:* -e irq:* -- sleep 10

# Generate report
trace-cmd report

# Launch GUI
kernelshark trace.dat

# Record and view live
trace-cmd record -e '*'
```

**SystemTap (Powerful but Declining)**

Scripting language for dynamic kernel instrumentation (pre-kernel-6.0 era).

Being phased out in favor of bpftrace/bcc (simpler, no kernel module compilation).

```bash
# List available probes
stap -L 'kernel.function("*")'

# Simple syscall counter
stap -e 'probe syscall.read { println("read") }' -p2
```

**dmesg / journalctl (System Logs)**

Simple but often overlooked:

```bash
# Watch kernel logs in real-time
dmesg -W

# Filter by subsystem
dmesg | grep -i block
dmesg | grep -i memory
dmesg | grep -i usb

# journalctl integration
journalctl -b                  # Current boot
journalctl -f                  # Follow (like tail -f)
journalctl PRIORITY=err        # Errors only
```

**Decision Tree – Which to Use in 2026?**

```
You need to debug/trace/profile kernel or system?

├── Quick function call graph / latency? 
│   └── → **ftrace** (function_graph / trace-cmd)
│
├── Standard CPU profiling, flame graphs, PMU counters?
│   └── → **perf** (record/report/top/flamegraph)
│
├── Need custom logic, histograms, in-kernel aggregation, ad-hoc query?
│   ├── One-liner / fast experiment? 
│   │   └── → **bpftrace** (highly recommended!)
│   └── Complex tool/agent/daemon? 
│       └── → **bcc**
│
└── Full-system detailed trace (with user-space too)?
    └── → **LTTng** or **perf + tracepoints**

Bottom line 2026 motto:
"Start with **perf**, one-off custom → **bpftrace**, reusable → **bcc**"
```

### Core Methodologies & Advanced Techniques

**1. USE Method (Utilization / Saturation / Errors)**

Systematic approach to identify bottleneck:

- **Utilization**: % of resource in use (CPU%, memory%, disk I/O%)
- **Saturation**: How much queuing/waiting (runqueue, I/O queue depth)
- **Errors**: Count of errors (dropped packets, allocation failures)

Example workflow:
```bash
# Step 1: Utilization
top                              # Overall CPU utilization
iostat -x 1                       # Disk utilization
free -h                           # Memory utilization

# Step 2: Saturation
vmstat 1 10                       # runqueue size in 'r' column
iostat -x 1 | grep '%' | awk '{print $NF}'  # %util (queue saturation)
ps aux | grep Z                   # Zombie processes (system saturation)

# Step 3: Errors
dmesg | tail                      # System errors
cat /proc/pressure/cpu            # CPU pressure stall info
cat /proc/pressure/io             # I/O pressure stall info
cat /proc/pressure/memory         # Memory pressure stall info
```

**2. Off-CPU Analysis (Why Threads Not Running)**

Understand why performance is poor despite low CPU usage:

```bash
# Using bcc tools
offcputime -f -p `pgrep myprocess` 5 > offcpu.stacks
cat offcpu.stacks | FlameGraph/flamegraph.pl --color=io > offcpu.svg

# Using bpftrace (scheduler context switches)
bpftrace -e 'tracepoint:sched:sched_switch { @[stack] = count(); }'

# Using perf
perf record -e sched:sched_switch -g -p 1234 -- sleep 10
perf script > out.perf.txt
stackcollapse-perf.pl out.perf.txt > out.folded
flamegraph.pl out.folded > out.svg
```

**3. Hot/Cold Code Paths (Flame Graphs)**

Most effective bottleneck visualization:

```bash
# Record with call stacks
perf record -F 99 -g -a -- sleep 30

# Convert to flame graph (need FlameGraph repo)
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg

# or using bpftrace
bpftrace -e 'profile:hz:99 { @[kstack] = count(); }' -o stacks.txt
cat stacks.txt | stackcollapse-bpftrace.pl | flamegraph.pl > flame.svg

# View in browser
python3 -m http.server 8000
# Then open http://localhost:8000/flame.svg
```

Interpret flame graphs:
- Width = CPU time spent
- Height = call depth
- Left-to-right = function name (alphabetical within same parent)
- Look for wide/flat sections (hot spots)

**4. Latency Analysis & Heat Maps**

Understand distribution of latencies (not just average):

```bash
# Block I/O latency distribution
bpftrace -e 'tracepoint:block:block_rq_issue { @start[args[0]] = nsecs; }
             tracepoint:block:block_rq_complete /@start[args[0]]/ {
               @latency[comm] = hist((nsecs - @start[args[0]]) / 1000);
               delete(@start[args[0]]);
             }'

# Scheduler runqueue latency
bpftrace -e 'tracepoint:sched:sched_wakeup_new { @start[args[1]] = nsecs; }
             tracepoint:sched:sched_switch /args[1]/ {
               @runq_lat = hist((nsecs - @start[args[1]]) / 1000000);
               delete(@start[args[1]]);
             }'

# System call latency breakdown
perf record -e syscalls:sys_enter -a -- sleep 10
perf script | perf stat
```

**5. Static vs Dynamic Tracing**

| Type | Stability | Use Cases | Tools |
|------|-----------|-----------|-------|
| **Tracepoints** (static) | Stable ABI | Common events (syscalls, block I/O, sched) | ftrace, perf, bpftrace, LTTng |
| **Kprobes** (dynamic) | Unstable, can break on updates | Debug functions, custom events | ftrace, perf, bpftrace, bcc |
| **Kfuncs** (BTF-based) | Modern, safer than kprobes | Kernel internal functions (5.8+) | bpftrace, bcc |
| **Uprobes** (userspace) | Works on user binaries | User function tracing | perf, bpftrace, bcc |

**Preference order**: Tracepoints > Kfuncs > Kprobes > Uprobes (most to least stable)

**6. Lock Contention Analysis**

Identify mutex/spinlock bottlenecks:

```bash
# Using perf
perf record -e contention:lock_acquire -g -- sleep 10
perf report

# Using bpftrace
bpftrace -e 'kprobe:__mutex_lock_slowpath { @[stack] = count(); }'

# Using bcc
/usr/share/bcc/tools/lockstat

# Measure lock wait time
perf stat -e lock-misses,lock-acquires -- myapp
```

**7. Memory Profiling**

Understand memory allocation patterns:

```bash
# Memory allocation frequency
bpftrace -e 'uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc { @[ustack] = count(); }'

# Memory leak detection (bcc)
memleak -p `pgrep myprocess`

# Page fault tracking
bpftrace -e 'software:page-faults { @[ustack] = count(); }'

# Memory hotness (L3 cache misses)
perf record -e mem_load_uops_retired.l3_miss -g -- sleep 30
```

**8. Network Performance Analysis**

```bash
# TCP connection tracking
tcpconnect -t                    # Show new TCP connections with timestamps

# Network packet loss
tcpdrop -t                       # Show dropped packets

# TCP retransmits
trace 'tracepoint:tcp:tcp_retransmit_skb'

# Socket buffer statistics
ss -s                            # Summary

# Network packet distribution
bpftrace -e 'tracepoint:net:net_dev_xmit { @[args[0]] = count(); }'
```

### Key One-Liners & Commands (2026 favorites)

**CPU Profiling:**
```bash
# 1. Classic CPU flame graph (perf)
perf record -F 99 -g -- sleep 30; perf script | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > flame.svg

# 2. Quick kernel hot spots
bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'   # Ctrl-C to stop

# 3. Live top-like with perf
perf top -F 99 -g --sort comm,dso,sym

# 4. CPU usage by process
ps aux | sort -rn -k3 | head
```

**Tracing & Event Analysis:**
```bash
# 5. List all tracepoints
perf list tracepoint:*   # or ls /sys/kernel/tracing/events

# 6. Function call count (ftrace)
cd /sys/kernel/tracing
echo function > current_tracer
echo 'vfs*' > set_ftrace_filter
echo 1 > tracing_on; sleep 5; echo 0 > tracing_on; cat trace

# 7. Syscall count by process (bpftrace)
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

# 8. Block I/O latency histogram (bpftrace)
bpftrace -e 'tracepoint:block:block_rq_issue { @start[tid] = nsecs; }
             tracepoint:block:block_rq_complete /@start[tid]/ { 
               @usecs = hist((nsecs - @start[tid]) / 1000); 
               delete(@start[tid]); 
             }'
```

**I/O Analysis:**
```bash
# 9. Block device I/O latency (bcc)
biolatency

# 10. File system reads/writes
vfscount

# 11. Disk I/O statistics
iostat -x 1
```

**Off-CPU & Scheduling:**
```bash
# 12. Off-CPU time flame graph (bcc)
offcputime -f -p `pgrep myprocess` 10 > offcpu.stacks

# 13. Scheduler runqueue latency
runqlat

# 14. Context switch analysis
perf record -e sched:sched_switch -g -- sleep 10
perf report
```

**Latency & Performance:**
```bash
# 15. Kernel function latency (bpftrace + kprobe)
bpftrace -e 'kprobe:my_kernel_func { @start[tid] = nsecs; }
             kretprobe:my_kernel_func /@start[tid]/ { 
               @ns = hist(nsecs - @start[tid]); 
               delete(@start[tid]); 
             }'

# 16. Measure lock contention
perf lock record -- ./myapp
perf lock report

# 17. Measure context switches
perf stat -e context-switches -i 0.1 sleep 5
```

### Monitoring & Troubleshooting One-Liners

```bash
# System overview (CPU, memory, I/O)
top -b -n1 | head -20
free -h
iostat -x 1 5

# Hardware counter statistics
perf stat -ddd sleep 5

# Check for IRQ storms
cat /proc/interrupts | watch -n 0.1 'tac | head -20'

# View running eBPF programs
bpftool prog list
bpftool perf show

# Load eBPF program stats
bpftool map show
bpftool map dump name my_map

# See loaded eBPF programs (kernel 5.8+)
bpftool prog show

# System-wide tracing (trace-cmd)
trace-cmd record -e sched:sched_switch -e block:* -- sleep 10
trace-cmd report

# Real-time kernel event monitoring
journalctl -f

# Check for system pressure (resource contention)
cat /proc/pressure/cpu
cat /proc/pressure/io
cat /proc/pressure/memory

# Find slow disk operations
ioping -LS /dev/sda1

# Network queue statistics
ss -s
netstat -ans | wc -l

# Memory pressure analysis
cat /proc/meminfo | grep Pressure
echo 3 > /proc/sys/vm/drop_caches  # Clear caches
```

### Real-World Debugging Scenarios

**Scenario 1: High CPU but slow application**

```bash
# Step 1: Check utilization
top -b -n1 | head

# Step 2: Profile CPU
perf record -F 99 -g -- sleep 30
perf report

# Step 3: Identify hot functions
perf annotate my_hot_function

# Step 4: Identify context switches
perf record -e sched:sched_switch -g -- sleep 10
```

**Scenario 2: Application stalled (not responding)**

```bash
# Step 1: Check if process running
ps aux | grep myapp

# Step 2: Check for blocked I/O
lsof -p `pgrep myapp` | grep REG

# Step 3: Check system load
vmstat 1 5

# Step 4: Off-CPU analysis
offcputime -p `pgrep myapp` 10

# Step 5: Check for locks
perf lock record -p `pgrep myapp`
```

**Scenario 3: High memory usage**

```bash
# Step 1: Check memory stats
free -h
cat /proc/meminfo

# Step 2: Track memory allocations
memleak -p `pgrep myapp`

# Step 3: Memory pressure
cat /proc/pressure/memory

# Step 4: Page fault rate
perf stat -e page-faults -p `pgrep myapp`
```

**Scenario 4: Slow I/O**

```bash
# Step 1: Check I/O stats
iostat -x 1 5

# Step 2: Track I/O latency
biolatency

# Step 3: Detailed block layer tracing
trace-cmd record -e block:* -- sleep 10

# Step 4: Check specific process I/O
lsof -p `pgrep myapp`
ioping -LS /path/to/file
```

### Installation & Setup

**Most Distros (Debian/Ubuntu):**
```bash
# Install essential tools
sudo apt install -y \
    linux-tools-generic \
    linux-tools-`uname -r` \
    trace-cmd \
    kernelshark

# Install bpftrace and bcc
sudo apt install -y bpftrace bpfcc-tools

# Install FlameGraph
git clone https://github.com/brendangregg/FlameGraph.git
export PATH="$PATH:$PWD/FlameGraph"
```

**Kernel Configuration (ensure enabled):**
```bash
# Check if CONFIG_FTRACE enabled
zcat /proc/config.gz | grep CONFIG_FTRACE

# Check perf_events
zcat /proc/config.gz | grep CONFIG_PERF_EVENTS

# Check eBPF
zcat /proc/config.gz | grep CONFIG_BPF
```

### Summary – 2026 Best Practices

**Starting Point (Best Practices Order):**

1. **Always start with perf** — it's safe, built-in, and powerful
   ```bash
   perf record -F 99 -g -- sleep 30
   perf report
   ```

2. **Need custom quick insight?** → **bpftrace** one-liner (fastest way)
   ```bash
   bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'
   ```

3. **Building production tools/agents?** → **bcc** (reusable Python/C)

4. **Deep function flow?** → **ftrace function_graph**
   ```bash
   echo function_graph > /sys/kernel/tracing/current_tracer
   ```

5. **Full-system historical trace?** → **trace-cmd / KernelShark** (GUI)

6. **Memory issues?** → **memleak, flame graphs**

7. **Scheduling/latency?** → **runqlat, offcputime, perf record**

**Key Takeaways:**

- **Measure before optimizing** (measurement bias is real)
- **Flame graphs are your friend** (best visualization for stacks)
- **Prefer tracepoints** over kprobes (stable ABI)
- **Use histograms** for distributions (not just averages)
- **Start simple** (perf → bpftrace → bcc → custom)
- **Know your tools' overhead** (sampling lower than instrumentation)

**Happy kernel hunting!** ⚡🐧

(Brendan Gregg's resources still rule in 2026 — check https://www.brendangregg.com for the latest flame graphs, bpftrace cheatsheets, and performance analysis methodologies.)