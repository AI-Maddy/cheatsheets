===================================
Linux Network Performance Guide
===================================

:Author: Linux Network Documentation
:Date: January 2026
:Version: 1.0

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Quick Performance Test
----------------------

.. code-block:: bash

   # Bandwidth test with iperf3
   # Server
   iperf3 -s
   
   # Client
   iperf3 -c server_ip -t 30
   
   # Check interface stats
   ip -s link show eth0
   
   # Monitor bandwidth
   iftop -i eth0
   nethogs eth0
   
   # Check TCP settings
   sysctl -a | grep tcp
   
   # View queue discipline
   tc qdisc show dev eth0

Kernel Network Tuning
======================

TCP Buffer Sizes
----------------

.. code-block:: bash

   # View current settings
   sysctl net.ipv4.tcp_rmem
   sysctl net.ipv4.tcp_wmem
   sysctl net.core.rmem_max
   sysctl net.core.wmem_max
   
   # Increase TCP read buffer
   sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
   
   # Increase TCP write buffer
   sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"
   
   # Increase max buffer sizes
   sysctl -w net.core.rmem_max=16777216
   sysctl -w net.core.wmem_max=16777216
   
   # UDP buffers
   sysctl -w net.core.rmem_default=262144
   sysctl -w net.core.wmem_default=262144
   
   # Make permanent in /etc/sysctl.conf
   net.ipv4.tcp_rmem = 4096 87380 16777216
   net.ipv4.tcp_wmem = 4096 65536 16777216
   net.core.rmem_max = 16777216
   net.core.wmem_max = 16777216

TCP Congestion Control
-----------------------

.. code-block:: bash

   # View available algorithms
   sysctl net.ipv4.tcp_available_congestion_control
   
   # View current algorithm
   sysctl net.ipv4.tcp_congestion_control
   
   # Set to BBR (recommended for modern networks)
   modprobe tcp_bbr
   sysctl -w net.ipv4.tcp_congestion_control=bbr
   
   # Or CUBIC (default)
   sysctl -w net.ipv4.tcp_congestion_control=cubic
   
   # Permanent
   echo "tcp_bbr" >> /etc/modules-load.d/modules.conf
   echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf

TCP Performance Tuning
-----------------------

.. code-block:: bash

   # Enable TCP window scaling
   sysctl -w net.ipv4.tcp_window_scaling=1
   
   # Enable timestamps
   sysctl -w net.ipv4.tcp_timestamps=1
   
   # Enable SACK
   sysctl -w net.ipv4.tcp_sack=1
   
   # Enable TCP Fast Open
   sysctl -w net.ipv4.tcp_fastopen=3
   
   # Reduce TIME_WAIT sockets
   sysctl -w net.ipv4.tcp_fin_timeout=15
   sysctl -w net.ipv4.tcp_tw_reuse=1
   
   # Increase max connections
   sysctl -w net.core.somaxconn=4096
   sysctl -w net.ipv4.tcp_max_syn_backlog=8192
   
   # Enable ECN (Explicit Congestion Notification)
   sysctl -w net.ipv4.tcp_ecn=1
   
   # MTU probing
   sysctl -w net.ipv4.tcp_mtu_probing=1

Network Stack Tuning
---------------------

.. code-block:: bash

   # Increase netdev budget (packet processing)
   sysctl -w net.core.netdev_budget=600
   sysctl -w net.core.netdev_budget_usecs=5000
   
   # Increase max backlog
   sysctl -w net.core.netdev_max_backlog=5000
   
   # Increase local port range
   sysctl -w net.ipv4.ip_local_port_range="10000 65535"
   
   # Reduce ARP cache timeout
   sysctl -w net.ipv4.neigh.default.gc_stale_time=120
   
   # Increase ARP cache size
   sysctl -w net.ipv4.neigh.default.gc_thresh1=1024
   sysctl -w net.ipv4.neigh.default.gc_thresh2=2048
   sysctl -w net.ipv4.neigh.default.gc_thresh3=4096

Interface Optimization
======================

Offload Features
----------------

.. code-block:: bash

   # View offload settings
   ethtool -k eth0
   
   # Enable/disable features
   ethtool -K eth0 gso on        # Generic Segmentation Offload
   ethtool -K eth0 tso on        # TCP Segmentation Offload
   ethtool -K eth0 gro on        # Generic Receive Offload
   ethtool -K eth0 lro on        # Large Receive Offload
   ethtool -K eth0 tx on         # TX checksumming
   ethtool -K eth0 rx on         # RX checksumming
   ethtool -K eth0 sg on         # Scatter-Gather
   
   # For maximum throughput (enable all)
   ethtool -K eth0 gso on tso on gro on lro on tx on rx on sg on
   
   # For low latency (disable some)
   ethtool -K eth0 gro off lro off

Ring Buffers
------------

.. code-block:: bash

   # View ring buffer sizes
   ethtool -g eth0
   
   # Increase RX ring buffer
   ethtool -G eth0 rx 4096
   
   # Increase TX ring buffer
   ethtool -G eth0 tx 4096
   
   # Set both
   ethtool -G eth0 rx 4096 tx 4096

Interrupt Coalescing
--------------------

.. code-block:: bash

   # View interrupt settings
   ethtool -c eth0
   
   # Set RX interrupt coalescing
   ethtool -C eth0 rx-usecs 50
   
   # Set TX interrupt coalescing
   ethtool -C eth0 tx-usecs 50
   
   # Adaptive coalescing
   ethtool -C eth0 adaptive-rx on adaptive-tx on
   
   # For low latency
   ethtool -C eth0 rx-usecs 10 tx-usecs 10
   
   # For high throughput
   ethtool -C eth0 rx-usecs 100 tx-usecs 100

Multi-Queue NICs
----------------

.. code-block:: bash

   # View queue count
   ethtool -l eth0
   
   # Set combined queues (RX + TX)
   ethtool -L eth0 combined 4
   
   # Set separate RX/TX queues
   ethtool -L eth0 rx 4 tx 4
   
   # View queue-to-CPU mapping
   cat /proc/interrupts | grep eth0
   
   # Set IRQ affinity (manual)
   echo 1 > /proc/irq/125/smp_affinity  # CPU 0
   echo 2 > /proc/irq/126/smp_affinity  # CPU 1
   echo 4 > /proc/irq/127/smp_affinity  # CPU 2
   echo 8 > /proc/irq/128/smp_affinity  # CPU 3

Traffic Control
===============

Queue Disciplines
-----------------

.. code-block:: bash

   # View current qdisc
   tc qdisc show dev eth0
   
   # Default qdisc (pfifo_fast)
   tc qdisc add dev eth0 root pfifo_fast
   
   # Fair Queue (FQ)
   tc qdisc add dev eth0 root fq
   
   # FQ with pacing
   tc qdisc add dev eth0 root fq pacing
   
   # Stochastic Fair Queueing (SFQ)
   tc qdisc add dev eth0 root sfq perturb 10
   
   # Hierarchical Token Bucket (HTB) for rate limiting
   tc qdisc add dev eth0 root handle 1: htb default 30
   tc class add dev eth0 parent 1: classid 1:1 htb rate 1gbit
   tc class add dev eth0 parent 1:1 classid 1:30 htb rate 100mbit
   
   # Delete qdisc
   tc qdisc del dev eth0 root

Rate Limiting
-------------

.. code-block:: bash

   # Simple rate limit with TBF (Token Bucket Filter)
   tc qdisc add dev eth0 root tbf rate 100mbit burst 32kbit latency 400ms
   
   # Per-class rate limit with HTB
   tc qdisc add dev eth0 root handle 1: htb
   tc class add dev eth0 parent 1: classid 1:1 htb rate 1gbit
   tc class add dev eth0 parent 1:1 classid 1:10 htb rate 100mbit ceil 200mbit
   tc class add dev eth0 parent 1:1 classid 1:20 htb rate 50mbit ceil 100mbit
   
   # Add filter to classify traffic
   tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 \
       match ip dst 192.168.1.0/24 flowid 1:10

Priority Queueing
-----------------

.. code-block:: bash

   # PRIO qdisc with 3 bands
   tc qdisc add dev eth0 root handle 1: prio bands 3
   
   # Assign filters to bands
   tc filter add dev eth0 parent 1: protocol ip prio 1 u32 \
       match ip tos 0x10 0xff flowid 1:1  # High priority
   tc filter add dev eth0 parent 1: protocol ip prio 2 u32 \
       match ip tos 0x00 0xff flowid 1:2  # Normal
   tc filter add dev eth0 parent 1: protocol ip prio 3 u32 \
       match ip protocol 6 0xff flowid 1:3  # Low priority

Performance Monitoring
======================

Bandwidth Monitoring
--------------------

.. code-block:: bash

   # iftop - interface bandwidth
   iftop -i eth0
   iftop -i eth0 -n  # No DNS resolution
   iftop -i eth0 -P  # Show ports
   
   # nethogs - per-process bandwidth
   nethogs eth0
   
   # nload - simple bandwidth monitor
   nload eth0
   
   # bmon - detailed statistics
   bmon -p eth0
   
   # vnstat - long-term statistics
   vnstat -i eth0
   vnstat -i eth0 -h  # Hourly
   vnstat -i eth0 -d  # Daily
   vnstat -i eth0 -l  # Live

Interface Statistics
--------------------

.. code-block:: bash

   # Basic stats
   ip -s link show eth0
   
   # Detailed stats
   ip -s -s link show eth0
   
   # ethtool statistics
   ethtool -S eth0
   
   # netstat interface stats
   netstat -i
   
   # /proc/net/dev
   cat /proc/net/dev
   
   # Watch for changes
   watch -n 1 'ip -s link show eth0'

Connection Statistics
---------------------

.. code-block:: bash

   # Active connections
   ss -s
   
   # TCP statistics
   ss -ti
   
   # Protocol statistics
   netstat -s
   
   # Per-connection stats
   ss -tiepm
   
   # Connection tracking
   cat /proc/net/nf_conntrack | wc -l
   sysctl net.netfilter.nf_conntrack_count
   sysctl net.netfilter.nf_conntrack_max

Performance Testing
===================

iperf3
------

.. code-block:: bash

   # Server
   iperf3 -s
   
   # Client - TCP test
   iperf3 -c server_ip
   
   # Test duration
   iperf3 -c server_ip -t 60
   
   # Parallel streams
   iperf3 -c server_ip -P 4
   
   # UDP test
   iperf3 -c server_ip -u -b 1G
   
   # Bidirectional test
   iperf3 -c server_ip --bidir
   
   # Reverse test (server sends)
   iperf3 -c server_ip -R
   
   # JSON output
   iperf3 -c server_ip -J
   
   # Interval reporting
   iperf3 -c server_ip -i 1

netperf
-------

.. code-block:: bash

   # Server
   netserver
   
   # TCP stream test
   netperf -H server_ip -t TCP_STREAM
   
   # TCP request/response
   netperf -H server_ip -t TCP_RR
   
   # UDP stream
   netperf -H server_ip -t UDP_STREAM
   
   # UDP request/response
   netperf -H server_ip -t UDP_RR
   
   # Custom test length
   netperf -H server_ip -t TCP_STREAM -l 60

HTTP Performance
----------------

.. code-block:: bash

   # Apache Bench
   ab -n 1000 -c 10 http://example.com/
   
   # wrk
   wrk -t4 -c100 -d30s http://example.com/
   
   # siege
   siege -c 100 -t 30s http://example.com/

Latency Measurement
-------------------

.. code-block:: bash

   # ICMP ping
   ping -c 100 8.8.8.8
   
   # TCP ping
   hping3 -S -p 80 example.com
   
   # Measure with timestamps
   ping -c 10 -D 8.8.8.8
   
   # sockperf for latency
   sockperf server &
   sockperf ping-pong -i server_ip -t 10

Packet Loss Detection
---------------------

.. code-block:: bash

   # Extended ping
   ping -c 1000 8.8.8.8 | tail -2
   
   # mtr report
   mtr --report --report-cycles 100 8.8.8.8

Optimization Techniques
=======================

CPU Affinity
------------

.. code-block:: bash

   # Set IRQ affinity
   echo 1 > /proc/irq/125/smp_affinity  # Pin to CPU 0
   
   # Use irqbalance for automatic distribution
   systemctl enable irqbalance
   systemctl start irqbalance
   
   # Or disable for manual control
   systemctl stop irqbalance
   systemctl disable irqbalance

Receive Packet Steering (RPS)
------------------------------

.. code-block:: bash

   # Enable RPS
   echo f > /sys/class/net/eth0/queues/rx-0/rps_cpus  # Use CPUs 0-3
   
   # Check setting
   cat /sys/class/net/eth0/queues/rx-0/rps_cpus

Receive Flow Steering (RFS)
----------------------------

.. code-block:: bash

   # Set RFS
   echo 32768 > /proc/sys/net/core/rps_sock_flow_entries
   echo 2048 > /sys/class/net/eth0/queues/rx-0/rps_flow_cnt

XPS (Transmit Packet Steering)
-------------------------------

.. code-block:: bash

   # Enable XPS
   echo 1 > /sys/class/net/eth0/queues/tx-0/xps_cpus
   echo 2 > /sys/class/net/eth0/queues/tx-1/xps_cpus

Jumbo Frames
------------

.. code-block:: bash

   # Set MTU to 9000
   ip link set eth0 mtu 9000
   
   # Test with ping
   ping -M do -s 8972 192.168.1.10
   
   # Verify
   ip link show eth0

Best Practices
==============

1. **Use BBR** congestion control for high-speed networks
2. **Increase buffer sizes** for high-bandwidth links
3. **Enable offload features** on capable NICs
4. **Tune ring buffers** based on traffic patterns
5. **Use multi-queue** NICs with RSS/RPS
6. **Monitor continuously** to establish baselines
7. **Test with realistic** workloads
8. **Document all changes**
9. **Use jumbo frames** on capable networks
10. **Pin interrupts** to specific CPUs for latency-sensitive apps

Common Pitfalls
===============

1. **Over-tuning** without measurement
2. **Disabling checksums** (dangerous)
3. **Too many parallel** iperf streams
4. **Not testing** under realistic conditions
5. **Ignoring CPU** as bottleneck
6. **Wrong MTU** for network path
7. **Not persisting** sysctl changes

Troubleshooting Performance
============================

.. code-block:: bash

   # Check for packet drops
   ip -s link show eth0 | grep -i drop
   ethtool -S eth0 | grep -i drop
   
   # Check for errors
   ip -s link show eth0 | grep -i err
   ethtool -S eth0 | grep -i err
   
   # Check CPU usage
   mpstat -P ALL 1
   
   # Check interrupts
   watch -n 1 'cat /proc/interrupts | grep eth0'
   
   # Check softirq
   mpstat -I SCPU 1
   
   # Check retransmissions
   netstat -s | grep retransmit
   ss -ti | grep retrans
   
   # Check queue discipline drops
   tc -s qdisc show dev eth0

Performance Checklist
======================

.. code-block:: bash

   # 1. Check offloads
   ethtool -k eth0
   
   # 2. Check ring buffers
   ethtool -g eth0
   
   # 3. Check interrupt coalescing
   ethtool -c eth0
   
   # 4. Check queue count
   ethtool -l eth0
   
   # 5. Check TCP settings
   sysctl -a | grep tcp | grep -E "(rmem|wmem|congestion)"
   
   # 6. Check network drops
   ip -s -s link show eth0
   
   # 7. Baseline test
   iperf3 -c server_ip -t 30
   
   # 8. Monitor during load
   iftop -i eth0

See Also
========

- Linux_Network_Configuration.rst
- Linux_Network_Tools.rst
- Linux_Network_Protocols.rst

References
==========

- https://fasterdata.es.net/
- https://www.kernel.org/doc/Documentation/networking/
- man tc
- man ethtool
