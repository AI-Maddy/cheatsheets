═══════════════════════════════════════════════════════════════════════
STORAGE SYSTEMS FOR EMBEDDED LINUX
═══════════════════════════════════════════════════════════════════════

**Comprehensive Guide to Storage Architecture in Embedded Systems**  
**Domain:** Embedded Linux 🐧 | Storage 💾 | High Availability 🛡️  
**Purpose:** RAID, flash optimization, distributed filesystems, IFE content storage

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Embedded Storage** requires reliability, performance, and longevity optimizations.

**Key Technologies:**
- **RAID:** Redundancy for fault tolerance (mirroring, parity)
- **Flash Optimization:** Wear leveling, TRIM, over-provisioning for eMMC/SSD longevity
- **Distributed Storage:** NFS, GlusterFS for multi-node systems
- **Filesystems:** ext4, F2FS, SquashFS optimized for flash/read-only
- **Content Management:** Deduplication, compression for large libraries (IFE)

**IFE Use Case:**
- 2-5 TB content library (50-100 movies)
- RAID 1 mirroring for redundancy
- NVMe SSD for performance
- Read-mostly workload (streaming)

═══════════════════════════════════════════════════════════════════════

🏗️ **1. STORAGE HARDWARE FOR EMBEDDED**
─────────────────────────────────────────────────────────────────────────

**1.1 Storage Technology Comparison**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+----------------+-------------+------------+-------------+
| **Technology**   | **Capacity**   | **Speed**   | **Cost**   | **Use Case**|
+==================+================+=============+============+=============+
| **eMMC**         | 8-256 GB       | 200 MB/s    | Low        | Seat units, |
|                  |                | (seq read)  |            | IoT devices |
+------------------+----------------+-------------+------------+-------------+
| **UFS 3.1**      | 128-512 GB     | 2 GB/s      | Medium     | Mobile,     |
| (Universal Flash)|                | (seq read)  |            | automotive  |
+------------------+----------------+-------------+------------+-------------+
| **SATA SSD**     | 256 GB - 4 TB  | 550 MB/s    | Medium     | Industrial, |
|                  |                | (seq read)  |            | legacy      |
+------------------+----------------+-------------+------------+-------------+
| **NVMe SSD**     | 512 GB - 8 TB  | 7 GB/s      | Medium-High| IFE head-   |
|                  |                | (seq read)  |            | end, servers|
+------------------+----------------+-------------+------------+-------------+
| **SD Card**      | 16 GB - 1 TB   | 100 MB/s    | Very Low   | Dev boards, |
|                  |                | (seq read)  |            | prototyping |
+------------------+----------------+-------------+------------+-------------+

**1.2 IFE Head-End Storage Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical Configuration:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │           IFE Head-End Server                           │
   ├─────────────────────────────────────────────────────────┤
   │  SOC: Qualcomm SA8295P (8-core ARM Cortex-A78AE)        │
   │  RAM: 32 GB LPDDR5                                      │
   │                                                         │
   │  ┌───────────────────────────────────────────────────┐  │
   │  │  Boot Storage (eMMC 32 GB)                        │  │
   │  │  - Bootloader (U-Boot)                            │  │
   │  │  - Linux kernel + initramfs                       │  │
   │  │  - Root filesystem (SquashFS, read-only)          │  │
   │  │  - Config partition (ext4, read-write)            │  │
   │  └───────────────────────────────────────────────────┘  │
   │                                                         │
   │  ┌───────────────────────────────────────────────────┐  │
   │  │  Content Storage (RAID 1)                         │  │
   │  │  ┌─────────────────────┐  ┌─────────────────────┐ │  │
   │  │  │ NVMe SSD 1 (2 TB)   │  │ NVMe SSD 2 (2 TB)   │ │  │
   │  │  │ /dev/nvme0n1        │  │ /dev/nvme1n1        │ │  │
   │  │  └──────────┬──────────┘  └──────────┬──────────┘ │  │
   │  │             │                        │            │  │
   │  │             └────────┬───────────────┘            │  │
   │  │                      │                            │  │
   │  │                ┌─────▼─────┐                      │  │
   │  │                │ md0 (RAID)│                      │  │
   │  │                │ 2 TB usable│                      │  │
   │  │                └─────┬─────┘                      │  │
   │  │                      │                            │  │
   │  │                ┌─────▼─────────────┐              │  │
   │  │                │ ext4 filesystem   │              │  │
   │  │                │ /mnt/content      │              │  │
   │  │                │ - Movies (H.265)  │              │  │
   │  │                │ - TV shows        │              │  │
   │  │                │ - Games           │              │  │
   │  │                │ - Moving maps     │              │  │
   │  │                └───────────────────┘              │  │
   │  └───────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────┘

**Storage Sizing:**

.. code-block:: text

   IFE Content Library:
   
   Movies (50 titles):
   - Resolution: 1080p (1920×1080)
   - Codec: H.265 (HEVC)
   - Bitrate: 3 Mbps (average)
   - Duration: 120 minutes (average)
   - File size: 3 Mbps × 7200s ÷ 8 = 2.7 GB per movie
   - Total: 50 × 2.7 GB = 135 GB
   
   TV Shows (500 episodes):
   - Resolution: 1080p
   - Codec: H.265
   - Bitrate: 2 Mbps
   - Duration: 45 minutes
   - File size: 2 Mbps × 2700s ÷ 8 = 675 MB per episode
   - Total: 500 × 675 MB = 337 GB
   
   Games (20 titles):
   - HTML5 + Unity WebGL
   - Average: 500 MB per game
   - Total: 20 × 500 MB = 10 GB
   
   Moving Maps:
   - World map tiles + textures
   - Total: 5 GB
   
   Metadata + Artwork:
   - Thumbnails, posters, subtitles
   - Total: 3 GB
   
   ──────────────────────────────────────
   Grand Total: 490 GB
   
   With 20% headroom: 600 GB
   
   Recommended: 2 TB NVMe SSD × 2 (RAID 1)
   - Usable: 2 TB
   - Headroom: 1.4 TB for future content

═══════════════════════════════════════════════════════════════════════

🛡️ **2. RAID (REDUNDANT ARRAY OF INDEPENDENT DISKS)**
─────────────────────────────────────────────────────────────────────────

**2.1 RAID Levels Comparison**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------+------------------+----------------+--------------+---------------+
| **RAID**   | **Redundancy**   | **Capacity**   | **Speed**    | **Use Case**  |
+============+==================+================+==============+===============+
| **RAID 0** | None (striping)  | 100% (N disks) | Fast (2×)    | Performance,  |
|            |                  |                |              | no redundancy |
+------------+------------------+----------------+--------------+---------------+
| **RAID 1** | Mirror           | 50% (N/2)      | Read: 2×     | **IFE head-   |
|            |                  |                | Write: 1×    | end (best)**  |
+------------+------------------+----------------+--------------+---------------+
| **RAID 5** | Parity (1 disk)  | (N-1) disks    | Good         | NAS, servers  |
|            |                  |                |              | (min 3 disks) |
+------------+------------------+----------------+--------------+---------------+
| **RAID 6** | Parity (2 disks) | (N-2) disks    | Good         | Large arrays  |
|            |                  |                |              | (min 4 disks) |
+------------+------------------+----------------+--------------+---------------+
| **RAID 10**| Mirror + stripe  | 50% (N/2)      | Very fast    | Databases,    |
|            |                  |                |              | high I/O      |
+------------+------------------+----------------+--------------+---------------+

**Why RAID 1 for IFE:**
- ✅ Simple (only 2 disks needed)
- ✅ Fast read (can read from either disk)
- ✅ Instant recovery (no rebuild parity)
- ✅ Survives 1 disk failure
- ✅ No performance penalty on write (mirror copy)

**2.2 Create RAID 1 Array**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Using mdadm (Linux Software RAID):**

.. code-block:: bash

   #!/bin/bash
   # Create RAID 1 mirror for IFE content storage
   
   DISK1="/dev/nvme0n1"
   DISK2="/dev/nvme1n1"
   RAID_DEVICE="/dev/md0"
   MOUNT_POINT="/mnt/content"
   
   # Install mdadm
   apt-get update
   apt-get install -y mdadm
   
   # Wipe disks (DANGEROUS - erases all data)
   echo "⚠️  WARNING: This will erase all data on $DISK1 and $DISK2"
   read -p "Continue? (yes/no): " confirm
   if [ "$confirm" != "yes" ]; then
       echo "Aborted"
       exit 1
   fi
   
   wipefs -a $DISK1
   wipefs -a $DISK2
   
   # Create RAID 1 array
   mdadm --create --verbose $RAID_DEVICE \
       --level=1 \
       --raid-devices=2 \
       $DISK1 $DISK2
   
   # Wait for sync to complete (can take hours for large disks)
   echo "Waiting for RAID sync..."
   while [ -n "$(mdadm --detail $RAID_DEVICE | grep -i 'State.*resyncing')" ]; do
       mdadm --detail $RAID_DEVICE | grep -i "sync status"
       sleep 10
   done
   
   echo "✅ RAID sync complete"
   
   # Create filesystem (ext4)
   mkfs.ext4 -L IFE_CONTENT $RAID_DEVICE
   
   # Create mount point
   mkdir -p $MOUNT_POINT
   
   # Mount filesystem
   mount $RAID_DEVICE $MOUNT_POINT
   
   # Add to /etc/fstab for auto-mount
   echo "$RAID_DEVICE $MOUNT_POINT ext4 defaults,noatime 0 2" >> /etc/fstab
   
   # Save RAID configuration
   mdadm --detail --scan >> /etc/mdadm/mdadm.conf
   update-initramfs -u
   
   echo "✅ RAID 1 array created and mounted at $MOUNT_POINT"
   
   # Verify
   mdadm --detail $RAID_DEVICE
   df -h $MOUNT_POINT

**2.3 RAID Monitoring**
~~~~~~~~~~~~~~~~~~~~~~~~

**Check RAID Status:**

.. code-block:: bash

   # Quick status
   cat /proc/mdstat
   
   # Example output:
   # md0 : active raid1 nvme1n1[1] nvme0n1[0]
   #       2000000000 blocks super 1.2 [2/2] [UU]
   #       bitmap: 0/15 pages [0KB], 65536KB chunk
   
   # [UU] = Both disks healthy
   # [U_] = Disk 1 healthy, Disk 2 failed
   # [_U] = Disk 0 failed, Disk 1 healthy

**Detailed RAID Info:**

.. code-block:: bash

   # Detailed status
   mdadm --detail /dev/md0
   
   # Example output:
   # /dev/md0:
   #    Version : 1.2
   #    State : clean
   #    Active Devices : 2
   #    Failed Devices : 0
   #    Spare Devices : 0
   #    
   #    Number   Major   Minor   RaidDevice State
   #       0     259        0        0      active sync   /dev/nvme0n1
   #       1     259        1        1      active sync   /dev/nvme1n1

**Automated Monitoring (cron):**

.. code-block:: bash

   #!/bin/bash
   # /usr/local/bin/check_raid.sh
   # Monitor RAID health and send alerts
   
   RAID_DEVICE="/dev/md0"
   LOG_FILE="/var/log/raid_health.log"
   
   # Check RAID status
   STATUS=$(mdadm --detail $RAID_DEVICE | grep "State" | awk '{print $3}')
   
   if [ "$STATUS" != "clean" ]; then
       # RAID degraded or rebuilding
       echo "$(date): ❌ RAID status: $STATUS" >> $LOG_FILE
       
       # Send alert (syslog, email, SNMP trap, etc.)
       logger -t RAID_MONITOR "CRITICAL: RAID array $RAID_DEVICE is $STATUS"
       
       # Optionally send email
       echo "RAID array $RAID_DEVICE is $STATUS" | \
           mail -s "RAID ALERT" admin@aircraft.local
   else
       echo "$(date): ✅ RAID status: $STATUS" >> $LOG_FILE
   fi

**Add to crontab:**

.. code-block:: bash

   # Run every 5 minutes
   */5 * * * * /usr/local/bin/check_raid.sh

**2.4 RAID Disk Failure Recovery**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario: One Disk Fails**

.. code-block:: bash

   # 1. Identify failed disk
   mdadm --detail /dev/md0
   # Output shows:
   #    Number   Major   Minor   RaidDevice State
   #       0     259        0        0      active sync   /dev/nvme0n1
   #       -       0        0        1      removed       /dev/nvme1n1
   
   # 2. Remove failed disk from array
   mdadm --manage /dev/md0 --remove /dev/nvme1n1
   
   # 3. Physically replace disk (hot-swap if supported)
   # Power off, replace disk, power on
   
   # 4. Add new disk to array
   mdadm --manage /dev/md0 --add /dev/nvme2n1
   
   # 5. RAID rebuilds automatically
   watch cat /proc/mdstat
   # Output:
   # md0 : active raid1 nvme2n1[2] nvme0n1[0]
   #       2000000000 blocks super 1.2 [2/1] [U_]
   #       [>....................]  recovery =  5.3% (106000000/2000000000)
   #       finish=15.2min speed=207000K/sec
   
   # Wait for rebuild to complete
   # Total time: ~15-30 minutes for 2 TB @ 200 MB/s

**Zero Downtime:**
- System continues running during rebuild
- Performance may degrade slightly (rebuild uses I/O bandwidth)
- Data remains accessible (reads from healthy disk)

═══════════════════════════════════════════════════════════════════════

💾 **3. FLASH OPTIMIZATION**
─────────────────────────────────────────────────────────────────────────

**3.1 Flash Memory Characteristics**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**NAND Flash Basics:**

+-------------------------+----------------------------------+
| **Characteristic**      | **Impact**                       |
+=========================+==================================+
| **Write Cycles**        | 3,000-100,000 (TLC-SLC)          |
| **Write Granularity**   | Page (4 KB - 16 KB)              |
| **Erase Granularity**   | Block (128 KB - 2 MB)            |
| **Read Speed**          | Fast (100-7000 MB/s)             |
| **Write Speed**         | Slower (50-3000 MB/s)            |
| **Write Amplification** | Erase-before-write overhead      |
+-------------------------+----------------------------------+

**Flash Types:**

+----------+------------------+------------------+------------------+
| **Type** | **Endurance**    | **Speed**        | **Cost**         |
+==========+==================+==================+==================+
| **SLC**  | 100,000 cycles   | Fastest          | Very High        |
| **MLC**  | 10,000 cycles    | Fast             | High             |
| **TLC**  | 3,000 cycles     | Medium           | Medium (common)  |
| **QLC**  | 1,000 cycles     | Slower           | Low              |
+----------+------------------+------------------+------------------+

**3.2 Filesystem Choice for Flash**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Filesystem Comparison:**

+---------------+-------------------+------------------+-------------------+
| **Filesystem**| **Flash-Aware**   | **Performance**  | **Use Case**      |
+===============+===================+==================+===================+
| **ext4**      | Partial (discard) | Good             | General-purpose   |
| **F2FS**      | Yes (Flash-       | Excellent        | eMMC, UFS, SSD    |
|               | Friendly FS)      | (optimized)      | (write-heavy)     |
| **SquashFS**  | Read-only         | Excellent reads  | Root filesystem   |
|               |                   |                  | (embedded)        |
| **UBIFS**     | Yes (raw NAND)    | Good             | Raw NAND (no FTL) |
| **JFFS2**     | Yes (raw NAND)    | Slow (legacy)    | Small flash       |
+---------------+-------------------+------------------+-------------------+

**ext4 with Flash Optimizations:**

.. code-block:: bash

   # Format with optimal settings for SSD/eMMC
   mkfs.ext4 \
       -L IFE_CONTENT \
       -O ^has_journal \               # Disable journal (SSD has FTL)
       -E stride=2,stripe-width=1024 \ # Align to erase block size
       /dev/md0
   
   # Mount with TRIM support
   mount -o defaults,noatime,discard /dev/md0 /mnt/content

**F2FS (Flash-Friendly File System):**

.. code-block:: bash

   # Install F2FS tools
   apt-get install -y f2fs-tools
   
   # Format eMMC/SSD with F2FS
   mkfs.f2fs -l IFE_BOOT /dev/mmcblk0p1
   
   # Mount with optimizations
   mount -t f2fs -o background_gc=on,inline_data /dev/mmcblk0p1 /boot

**3.3 TRIM/DISCARD**
~~~~~~~~~~~~~~~~~~~~~

**What is TRIM:**
- Tells SSD which blocks are no longer in use (deleted files)
- SSD can erase blocks in advance (improves write performance)
- Reduces write amplification

**Enable TRIM:**

.. code-block:: bash

   # Option 1: Continuous TRIM (mount option)
   mount -o discard /dev/nvme0n1 /mnt/content
   
   # Or in /etc/fstab:
   /dev/nvme0n1 /mnt/content ext4 defaults,noatime,discard 0 2
   
   # Option 2: Periodic TRIM (systemd timer) - RECOMMENDED
   systemctl enable fstrim.timer
   systemctl start fstrim.timer
   
   # Runs weekly TRIM on all mounted filesystems
   systemctl status fstrim.timer

**Manual TRIM:**

.. code-block:: bash

   # TRIM all filesystems
   fstrim -av
   
   # TRIM specific filesystem
   fstrim /mnt/content

**3.4 Over-Provisioning**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Concept: Reserve Space for Wear Leveling**

.. code-block:: text

   SSD Physical Capacity: 2048 GB (2 TB)
   User-Accessible: 2000 GB
   Over-Provisioning: 48 GB (2.4%)
   
   Benefits:
   - SSD controller uses OP space for wear leveling
   - Improves write performance (more free blocks)
   - Extends lifespan (spreads writes across more blocks)

**Create Over-Provisioning (Unpartitioned Space):**

.. code-block:: bash

   # Example: 2 TB SSD, create 1.9 TB partition (leaving 100 GB OP)
   
   # Create partition (90% of disk)
   parted /dev/nvme0n1 mklabel gpt
   parted /dev/nvme0n1 mkpart primary 0% 90%
   
   # Format partition
   mkfs.ext4 /dev/nvme0n1p1
   
   # Remaining 10% is unpartitioned (used by SSD for OP)

**3.5 Write Amplification**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem: Small Writes Become Large Erases**

.. code-block:: text

   Application writes 4 KB:
   
   ❌ Without Optimization:
   1. Read entire 128 KB block to buffer
   2. Modify 4 KB in buffer
   3. Erase 128 KB block
   4. Write 128 KB back
   
   Write Amplification Factor (WAF) = 128 KB / 4 KB = 32×
   
   ✅ With Optimization (FTL):
   1. Write 4 KB to new location
   2. Update mapping table
   3. Old block marked for background garbage collection
   
   WAF = 1-2× (much better)

**Minimize Write Amplification:**

1. **Use ext4 without journal:**
   - Journal doubles writes (data + journal)
   - SSDs have internal power-loss protection

2. **Align writes to erase block size:**
   - Use ``stride`` and ``stripe-width`` in mkfs.ext4

3. **Batch small writes:**
   - Buffer small writes in RAM, flush periodically

4. **Use F2FS:**
   - Designed for log-structured writes (minimizes WAF)

═══════════════════════════════════════════════════════════════════════

🌐 **4. DISTRIBUTED STORAGE**
─────────────────────────────────────────────────────────────────────────

**4.1 NFS (Network File System)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Case: Share Content Between Head-End Servers**

.. code-block:: text

   ┌──────────────────┐         ┌──────────────────┐
   │  Server 1        │         │  Server 2        │
   │  (NFS Server)    │◀───────▶│  (NFS Client)    │
   │  /mnt/content    │  NFS    │  /mnt/content    │
   │  (RAID 1, 2 TB)  │         │  (mounted)       │
   └──────────────────┘         └──────────────────┘

**NFS Server Configuration:**

.. code-block:: bash

   # Install NFS server
   apt-get install -y nfs-kernel-server
   
   # Create export directory
   mkdir -p /mnt/content
   
   # Configure NFS exports (/etc/exports)
   cat >> /etc/exports << EOF
   /mnt/content 10.1.1.0/24(ro,sync,no_subtree_check,no_root_squash)
   EOF
   
   # Apply exports
   exportfs -a
   
   # Start NFS server
   systemctl enable nfs-kernel-server
   systemctl start nfs-kernel-server
   
   # Verify exports
   showmount -e localhost

**NFS Client Configuration:**

.. code-block:: bash

   # Install NFS client
   apt-get install -y nfs-common
   
   # Create mount point
   mkdir -p /mnt/content
   
   # Mount NFS share
   mount -t nfs 10.1.1.10:/mnt/content /mnt/content
   
   # Add to /etc/fstab for auto-mount
   echo "10.1.1.10:/mnt/content /mnt/content nfs defaults,ro,noatime 0 0" >> /etc/fstab
   
   # Verify
   df -h /mnt/content

**NFS Performance Tuning:**

.. code-block:: bash

   # Mount with performance options
   mount -t nfs \
       -o rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 \
       10.1.1.10:/mnt/content /mnt/content
   
   # Options explained:
   # rsize=1048576    : 1 MB read buffer (larger = faster reads)
   # wsize=1048576    : 1 MB write buffer
   # hard             : Retry indefinitely on failure (vs soft timeout)
   # timeo=600        : 60-second timeout (0.1s × 600)
   # retrans=2        : Retry 2 times before increasing timeout

**4.2 GlusterFS (Distributed Filesystem)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Case: Replicated Content Across Multiple Servers**

.. code-block:: text

   ┌──────────────────┐         ┌──────────────────┐
   │  Server 1        │◀───────▶│  Server 2        │
   │  /data/brick1    │ Replicate│  /data/brick2    │
   │  1 TB            │         │  1 TB            │
   └────────┬─────────┘         └─────────┬────────┘
            │                             │
            │     GlusterFS Volume        │
            │     (2 TB replicated)       │
            └──────────┬──────────────────┘
                       │
                  Client Mount
                  /mnt/gluster

**Install GlusterFS:**

.. code-block:: bash

   # On all nodes (Server 1, Server 2)
   apt-get update
   apt-get install -y glusterfs-server
   
   # Start GlusterFS service
   systemctl enable glusterd
   systemctl start glusterd

**Create Gluster Cluster:**

.. code-block:: bash

   # On Server 1: Probe Server 2
   gluster peer probe 10.1.1.11
   
   # Verify peer status
   gluster peer status
   # Output:
   # Number of Peers: 1
   # Hostname: 10.1.1.11
   # State: Peer in Cluster (Connected)

**Create Replicated Volume:**

.. code-block:: bash

   # On Server 1: Create brick directory
   mkdir -p /data/brick1/ife_content
   
   # On Server 2: Create brick directory
   mkdir -p /data/brick2/ife_content
   
   # On Server 1: Create volume (replica 2)
   gluster volume create ife_content replica 2 \
       10.1.1.10:/data/brick1/ife_content \
       10.1.1.11:/data/brick2/ife_content \
       force
   
   # Start volume
   gluster volume start ife_content
   
   # Verify volume
   gluster volume info ife_content

**Mount Gluster Volume (Client):**

.. code-block:: bash

   # Install GlusterFS client
   apt-get install -y glusterfs-client
   
   # Mount volume
   mkdir -p /mnt/gluster
   mount -t glusterfs 10.1.1.10:/ife_content /mnt/gluster
   
   # Add to /etc/fstab
   echo "10.1.1.10:/ife_content /mnt/gluster glusterfs defaults,_netdev 0 0" >> /etc/fstab
   
   # Verify
   df -h /mnt/gluster

**Benefits:**
- ✅ Automatic replication (write to one server, replicated to both)
- ✅ High availability (if Server 1 fails, Server 2 serves data)
- ✅ No single point of failure
- ✅ Transparent failover

═══════════════════════════════════════════════════════════════════════

📦 **5. CONTENT MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**5.1 Deduplication**
~~~~~~~~~~~~~~~~~~~~~

**Scenario: Multiple Aircraft with Same Content**

.. code-block:: text

   Without Deduplication:
   
   Aircraft 1: 50 movies × 2.7 GB = 135 GB
   Aircraft 2: 50 movies × 2.7 GB = 135 GB
   Aircraft 3: 50 movies × 2.7 GB = 135 GB
   
   Total storage (3 aircraft): 405 GB
   
   With Deduplication (Ground CMS):
   
   Ground CMS: 50 unique movies = 135 GB
   - Store once
   - Copy to aircraft as needed
   
   Savings: 405 GB → 135 GB (67% reduction)

**Deduplication with Duperemove:**

.. code-block:: bash

   # Install duperemove
   apt-get install -y duperemove
   
   # Scan directory for duplicate blocks
   duperemove -rd /mnt/content/movies
   
   # Output example:
   # Total files scanned: 50
   # Total blocks: 34560
   # Duplicate blocks: 1234
   # Space saved: 4.8 GB

**5.2 Compression**
~~~~~~~~~~~~~~~~~~~

**Transparent Compression (SquashFS for Read-Only):**

.. code-block:: bash

   # Create compressed SquashFS image
   mksquashfs /mnt/content /mnt/content.sqsh -comp xz -b 1M
   
   # Mount read-only compressed filesystem
   mkdir -p /mnt/content_ro
   mount -t squashfs /mnt/content.sqsh /mnt/content_ro
   
   # Compression ratio: ~20-30% for video files (already H.265 compressed)

**Compression with Btrfs:**

.. code-block:: bash

   # Format with Btrfs
   mkfs.btrfs -L IFE_CONTENT /dev/md0
   
   # Mount with compression
   mount -o compress=zstd:3 /dev/md0 /mnt/content
   
   # zstd levels: 1 (fast, low compression) to 15 (slow, high compression)
   # Level 3: Good balance for real-time

**5.3 Content Synchronization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Rsync for Incremental Updates:**

.. code-block:: bash

   #!/bin/bash
   # sync_content.sh - Sync content from ground CMS to aircraft
   
   SOURCE="/media/usb/content/"
   DEST="/mnt/content/"
   LOG_FILE="/var/log/content_sync.log"
   
   echo "$(date): Starting content sync..." >> $LOG_FILE
   
   # Rsync with options:
   # -a : Archive mode (recursive, preserve permissions/timestamps)
   # -v : Verbose
   # -h : Human-readable sizes
   # --progress : Show progress
   # --checksum : Verify with checksum (not just timestamp)
   # --delete : Delete files from dest not in source
   
   rsync -avh \
       --progress \
       --checksum \
       --delete \
       --log-file=$LOG_FILE \
       $SOURCE $DEST
   
   if [ $? -eq 0 ]; then
       echo "$(date): ✅ Sync completed successfully" >> $LOG_FILE
   else
       echo "$(date): ❌ Sync failed" >> $LOG_FILE
   fi

**Bandwidth-Limited Sync (for satellite links):**

.. code-block:: bash

   # Limit to 1 Mbps (125 KB/s)
   rsync -avh --bwlimit=125 \
       /media/usb/content/ /mnt/content/

═══════════════════════════════════════════════════════════════════════

🔧 **6. PERFORMANCE TUNING**
─────────────────────────────────────────────────────────────────────────

**6.1 I/O Schedulers**
~~~~~~~~~~~~~~~~~~~~~~~

**Linux I/O Schedulers:**

+---------------+---------------------+-------------------+
| **Scheduler** | **Best For**        | **Algorithm**     |
+===============+=====================+===================+
| **noop**      | SSDs, NVMe          | FIFO (no sorting) |
| **deadline**  | Real-time, SSDs     | Deadline-based    |
| **cfq**       | HDDs (legacy)       | Completely Fair   |
| **bfq**       | Desktop, interactive| Budget Fair Queue |
| **kyber**     | NVMe, modern SSDs   | Token-based       |
+---------------+---------------------+-------------------+

**Check Current Scheduler:**

.. code-block:: bash

   cat /sys/block/nvme0n1/queue/scheduler
   # Output: [none] mq-deadline kyber bfq

**Set Scheduler (NVMe - use none or kyber):**

.. code-block:: bash

   # Temporarily (until reboot)
   echo none > /sys/block/nvme0n1/queue/scheduler
   
   # Permanently (add to /etc/udev/rules.d/60-ioscheduler.rules)
   cat > /etc/udev/rules.d/60-ioscheduler.rules << EOF
   # Set I/O scheduler for NVMe devices
   ACTION=="add|change", KERNEL=="nvme[0-9]n[0-9]", ATTR{queue/scheduler}="none"
   EOF

**6.2 Read-Ahead Tuning**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Increase Read-Ahead for Sequential Reads (Video Streaming):**

.. code-block:: bash

   # Check current read-ahead (KB)
   blockdev --getra /dev/nvme0n1
   # Default: 256 (128 KB)
   
   # Set read-ahead to 8 MB (good for video streaming)
   blockdev --setra 16384 /dev/nvme0n1  # 16384 × 512 bytes = 8 MB
   
   # Verify
   blockdev --getra /dev/nvme0n1

**Make Persistent (add to /etc/rc.local):**

.. code-block:: bash

   cat >> /etc/rc.local << EOF
   #!/bin/bash
   blockdev --setra 16384 /dev/nvme0n1
   exit 0
   EOF
   
   chmod +x /etc/rc.local

**6.3 Mount Options**
~~~~~~~~~~~~~~~~~~~~~~

**Optimized Mount Options for IFE Content:**

.. code-block:: bash

   # /etc/fstab entry
   /dev/md0 /mnt/content ext4 defaults,noatime,nodiratime,commit=60,data=writeback 0 2
   
   # Options explained:
   # noatime      : Don't update access time (reduces writes)
   # nodiratime   : Don't update directory access time
   # commit=60    : Sync every 60 seconds (vs 5 default) - reduces writes
   # data=writeback : Don't enforce data-before-metadata (fastest, less safe)

**For Read-Only Content (after loading):**

.. code-block:: bash

   # Remount as read-only
   mount -o remount,ro /mnt/content
   
   # Or in /etc/fstab:
   /dev/md0 /mnt/content ext4 ro,noatime 0 2

═══════════════════════════════════════════════════════════════════════

🎓 **7. INTERVIEW PREPARATION**
─────────────────────────────────────────────────────────────────────────

**7.1 Demonstrate Storage Knowledge**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Question: "How would you design storage for an IFE system?"**

**Answer:**

"I'd use a dual-SSD RAID 1 configuration with flash optimizations:

**Architecture:**
- **2× 2 TB NVMe SSDs** in RAID 1 (mdadm software RAID)
- **Filesystem:** ext4 with TRIM enabled, noatime mount option
- **Redundancy:** RAID 1 mirroring (survives 1 disk failure)
- **Capacity:** 2 TB usable (500 GB content + 1.5 TB headroom)

**Why RAID 1:**
- Simple (2 disks, no complex parity)
- Fast reads (can read from either disk)
- Instant failover (no rebuild parity)
- Zero downtime recovery (hot-swap failed disk)

**Flash Optimization:**
- TRIM support (weekly fstrim.timer)
- Over-provisioning (10% unpartitioned)
- Aligned writes (stride/stripe-width in mkfs.ext4)
- Read-ahead tuning (8 MB for sequential video streaming)

**Content Management:**
- Rsync for incremental updates from ground CMS
- Checksum verification (SHA-256) before/after copy
- Read-only mount during flight (remount ro)

This is similar to my experience with eMMC optimization on i.MX 93, where I implemented wear leveling and OTA update strategies."

**7.2 Technical Deep-Dive**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q: "Explain RAID 1 vs RAID 5 and why you'd choose one over the other."**

**A:**

**RAID 1 (Mirroring):**
- **Redundancy:** Exact copy on 2 disks
- **Capacity:** 50% (2 TB usable from 2× 2 TB)
- **Performance:** Fast reads (2×), normal writes
- **Rebuild:** Instant (just copy from good disk)
- **Minimum Disks:** 2

**RAID 5 (Parity):**
- **Redundancy:** Distributed parity across N disks
- **Capacity:** (N-1) disks (6 TB usable from 3× 2 TB)
- **Performance:** Good reads, slower writes (parity calculation)
- **Rebuild:** Slow (recalculate parity, can take hours)
- **Minimum Disks:** 3

**For IFE, I'd choose RAID 1:**
- ✅ Only 2 disks fit in head-end enclosure (space-constrained)
- ✅ Instant recovery (copy from mirror, no rebuild time)
- ✅ Better write performance (no parity calculation)
- ✅ Simpler (less complexity = higher reliability)

**RAID 5 makes sense for:**
- NAS with 4+ disks (better capacity efficiency)
- Write-once, read-many workloads
- Ground CMS (not aircraft)

From my automotive experience, I've seen RAID 1 used in similar safety-critical systems (ECU data logging) for its simplicity and reliability."

**Q: "How do you optimize storage for flash longevity?"**

**A:**

**Key Techniques:**

1. **TRIM/DISCARD:**
   - Enable periodic TRIM (fstrim.timer)
   - Tells SSD which blocks are free (improves garbage collection)

2. **Over-Provisioning:**
   - Leave 10-20% unpartitioned
   - SSD uses for wear leveling

3. **Minimize Writes:**
   - Mount with noatime (don't update access times)
   - Use read-only mount when possible
   - Disable journaling on ext4 (SSDs have power-loss protection)

4. **Align Writes:**
   - Align partitions to erase block size (128 KB typical)
   - Use stride/stripe-width in mkfs.ext4

5. **Use Flash-Friendly Filesystem:**
   - F2FS for write-heavy workloads
   - SquashFS for read-only content

**Example from i.MX 93 project:**
- eMMC boot partition: SquashFS read-only root
- Config partition: F2FS with inline_data
- Logs: tmpfs (RAM, no flash writes)
- Result: Estimated lifespan > 10 years (from 3 years without optimization)

**7.3 Ask Intelligent Questions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. "What's the typical content refresh rate for IFE - monthly, quarterly?"

2. "Do you use NFS to share content between redundant head-end servers?"

3. "How do you handle content updates - USB pre-flight or satellite download in-flight?"

4. "What's the average lifespan requirement for IFE storage - 5 years, 10 years?"

5. "Do you use any deduplication or compression for content libraries?"

═══════════════════════════════════════════════════════════════════════

📚 **QUICK REFERENCE**
─────────────────────────────────────────────────────────────────────────

**Essential Commands**

.. code-block:: bash

   # RAID
   mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/nvme0n1 /dev/nvme1n1
   mdadm --detail /dev/md0
   cat /proc/mdstat
   
   # Filesystem
   mkfs.ext4 -L IFE_CONTENT /dev/md0
   mount -o defaults,noatime,discard /dev/md0 /mnt/content
   
   # TRIM
   fstrim -av
   systemctl enable fstrim.timer
   
   # Performance
   blockdev --setra 16384 /dev/nvme0n1  # Set read-ahead
   echo none > /sys/block/nvme0n1/queue/scheduler  # I/O scheduler
   
   # NFS
   exportfs -a                      # Apply NFS exports
   showmount -e localhost           # Show exports
   mount -t nfs 10.1.1.10:/mnt/content /mnt/content

**Storage Sizing (IFE)**

- **50 movies:** 135 GB (H.265 @ 3 Mbps, 2 hours avg)
- **500 TV episodes:** 337 GB (H.265 @ 2 Mbps, 45 min avg)
- **Games + maps:** 15 GB
- **Total:** 490 GB
- **Recommended:** 2× 2 TB NVMe SSD (RAID 1)

═══════════════════════════════════════════════════════════════════════

✅ **KEY TAKEAWAYS**
─────────────────────────────────────────────────────────────────────────

**Storage Hardware:**
1. ✅ **NVMe SSD:** 7 GB/s, best for IFE head-end
2. ✅ **eMMC:** 200 MB/s, sufficient for seat units
3. ✅ **UFS 3.1:** 2 GB/s, good for automotive/mobile

**RAID:**
1. ✅ **RAID 1 (Mirror):** Best for IFE (2 disks, instant recovery)
2. ✅ **mdadm:** Linux software RAID (no hardware controller needed)
3. ✅ **Hot-swap:** Replace failed disk without downtime
4. ✅ **Monitoring:** Automated checks (cron + mdadm --detail)

**Flash Optimization:**
1. ✅ **TRIM:** Weekly fstrim.timer (improves performance + longevity)
2. ✅ **Over-Provisioning:** 10-20% unpartitioned space
3. ✅ **noatime:** Don't update access times (reduces writes)
4. ✅ **F2FS:** Flash-Friendly FS for write-heavy (eMMC, UFS)

**Distributed Storage:**
1. ✅ **NFS:** Share content between servers (read-only for clients)
2. ✅ **GlusterFS:** Replicated storage (high availability)
3. ✅ **Rsync:** Incremental sync (ground CMS → aircraft)

**Performance:**
1. ✅ **I/O Scheduler:** none/kyber for NVMe
2. ✅ **Read-Ahead:** 8 MB for sequential streaming
3. ✅ **Mount Options:** noatime, data=writeback

**Resume Connections:**
- ✅ **i.MX 93:** eMMC optimization, wear leveling, OTA updates
- ✅ **AFIRS:** Flash storage in satellite modem
- ✅ **Industrial:** RAID for data logging

═══════════════════════════════════════════════════════════════════════

**References:**

- Linux md(4): Multiple Device Driver (Software RAID)
- ext4: https://www.kernel.org/doc/html/latest/filesystems/ext4/
- F2FS: Flash-Friendly File System
- NFS: Network File System (RFC 7530)
- GlusterFS: https://www.gluster.org/

**Last Updated:** January 2026

═══════════════════════════════════════════════════════════════════════
