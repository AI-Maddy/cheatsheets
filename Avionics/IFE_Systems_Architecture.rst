═══════════════════════════════════════════════════════════════════════
IN-FLIGHT ENTERTAINMENT (IFE) SYSTEMS ARCHITECTURE
═══════════════════════════════════════════════════════════════════════

**Comprehensive Guide to Modern IFE Platform Design**  
**Domain:** Avionics ✈️ | Entertainment Systems 📺 | Aircraft Cabin  
**Purpose:** IFE architecture, head-end servers, seat units, content delivery

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**In-Flight Entertainment (IFE)** systems provide entertainment, information, and connectivity to aircraft passengers.

**Key Components:**
- **Head-End Server:** Central platform (Qualcomm/MediaTek SOC, Linux/QNX) distributing content
- **Seat Units:** Embedded displays (ARM SOCs) at each passenger seat
- **Cabin Network:** Ethernet backbone (AFDX Part 10 or TSN) connecting all components
- **Content Delivery:** Video streaming (multicast RTSP), games, WiFi, live TV
- **Ground Infrastructure:** Content management system (CMS) for pre-flight loading

**Modern Stack:**
- Linux + Docker/K3s for head-end services
- H.265 video encoding for bandwidth efficiency
- IGMP multicast for simultaneous streaming to 300+ seats
- QNX Hypervisor for safety-critical monitoring

═══════════════════════════════════════════════════════════════════════

🏗️ **1. IFE SYSTEM OVERVIEW**
─────────────────────────────────────────────────────────────────────────

**1.1 System Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**End-to-End IFE System:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────────┐
   │                    GROUND INFRASTRUCTURE                        │
   ├─────────────────────────────────────────────────────────────────┤
   │  Content Management System (CMS)                                │
   │  - Movie ingestion (studios)                                    │
   │  - Transcoding (H.265, multiple bitrates)                       │
   │  - Metadata (titles, subtitles, ratings)                        │
   │  - DRM licensing                                                │
   └───────────────────┬─────────────────────────────────────────────┘
                       │ USB/WiFi/Satellite Upload
   ┌───────────────────▼─────────────────────────────────────────────┐
   │                     AIRCRAFT (In Flight)                        │
   ├─────────────────────────────────────────────────────────────────┤
   │  ┌──────────────────────────────────────────────────────────┐   │
   │  │              HEAD-END SERVER RACK                        │   │
   │  │  ┌────────────────────────────────────────────────────┐  │   │
   │  │  │  Server 1 (Primary)                                │  │   │
   │  │  │  - SOC: Qualcomm SA8295P (8-core ARM A78AE)        │  │   │
   │  │  │  - RAM: 32 GB                                      │  │   │
   │  │  │  - Storage: 2TB NVMe SSD (RAID 1)                  │  │   │
   │  │  │  - OS: Linux 6.1 LTS + QNX Hypervisor             │  │   │
   │  │  │  - Services:                                       │  │   │
   │  │  │    * Video encoder (H.265, 8 streams)              │  │   │
   │  │  │    * RTSP server (multicast streaming)             │  │   │
   │  │  │    * Content DB (PostgreSQL)                       │  │   │
   │  │  │    * Game server (Unity, HTML5)                    │  │   │
   │  │  │    * WiFi controller (802.11ax)                    │  │   │
   │  │  │    * Moving maps (GPS integration)                 │  │   │
   │  │  └────────────────────────────────────────────────────┘  │   │
   │  │  ┌────────────────────────────────────────────────────┐  │   │
   │  │  │  Server 2 (Redundant) - Hot Standby                │  │   │
   │  │  └────────────────────────────────────────────────────┘  │   │
   │  └──────────────────────────────────────────────────────────┘   │
   │                          │                                       │
   │              ┌───────────┴───────────┐                           │
   │              │  CABIN NETWORK        │                           │
   │              │  - AFDX Part 10       │                           │
   │              │  - 1 Gbps Ethernet    │                           │
   │              │  - VLAN segmentation  │                           │
   │              │  - IGMP multicast     │                           │
   │              └───────────┬───────────┘                           │
   │                          │                                       │
   │        ┌─────────────────┼─────────────────┐                     │
   │        │                 │                 │                     │
   │   ┌────▼───┐        ┌────▼───┐       ┌────▼───┐                 │
   │   │ Seat 1 │  ...   │ Seat   │  ...  │ Seat   │  (300 seats)    │
   │   │ Unit   │        │ Unit   │       │ Unit   │                 │
   │   │ 1A     │        │ 15C    │       │ 30F    │                 │
   │   └────────┘        └────────┘       └────────┘                 │
   │   - Display: 15" touchscreen (1920x1080)                         │
   │   - SOC: NXP i.MX 8M Plus (Quad A53)                             │
   │   - RAM: 2 GB LPDDR4                                             │
   │   - Storage: 8 GB eMMC                                           │
   │   - Services: Video player, games, WiFi client                   │
   └─────────────────────────────────────────────────────────────────┘

**1.2 Key Requirements**
~~~~~~~~~~~~~~~~~~~~~~~~~

**Performance:**

+----------------------------+--------------------------------+
| **Metric**                 | **Target**                     |
+============================+================================+
| **Passenger Capacity**     | 300-400 seats (wide-body)      |
| **Video Streams**          | 8-12 concurrent channels       |
| **Resolution**             | 1080p @ 30fps                  |
| **Codec**                  | H.265 (HEVC) for bandwidth     |
| **Bitrate**                | 2-4 Mbps per stream            |
| **Total Bandwidth**        | 30-50 Mbps (8 streams)         |
| **Content Library**        | 50-100 movies, 500 TV episodes |
| **Storage**                | 2-5 TB                         |
| **Boot Time**              | < 60 seconds (head-end)        |
| **Failover Time**          | < 5 seconds (redundancy)       |
+----------------------------+--------------------------------+

**Reliability:**
- **MTBF:** > 20,000 hours
- **Redundancy:** Dual head-end servers (hot standby)
- **Power:** 28V DC aircraft power + backup
- **Temperature:** -20°C to +55°C (pressurized cabin)
- **Vibration:** DO-160G Section 8 (aircraft vibration)

**Certification:**
- **DO-160G:** Environmental testing (temperature, vibration, EMI)
- **TSO-C139:** Software approval (non-safety-critical entertainment)
- **EASA/FAA:** Type certification for aircraft installation
- **ETSI EN 301 489:** EMC compliance

═══════════════════════════════════════════════════════════════════════

🖥️ **2. HEAD-END SERVER ARCHITECTURE**
─────────────────────────────────────────────────────────────────────────

**2.1 SOC Selection**
~~~~~~~~~~~~~~~~~~~~~

**Top SOC Choices for IFE Head-End:**

+------------------------+---------------------------+------------------------+
| **SOC**                | **Specs**                 | **Advantages**         |
+========================+===========================+========================+
| **Qualcomm SA8295P**   | - 8× A78AE @ 2.4 GHz      | - Automotive-grade     |
|                        | - Adreno 740 GPU          | - Safety Island (R52)  |
|                        | - Hexagon DSP             | - Rich multimedia      |
|                        | - 32 GB LPDDR5            | - Video encode/decode  |
|                        | - PCIe Gen 4, USB 3.2     | - Long lifecycle       |
+------------------------+---------------------------+------------------------+
| **NXP i.MX 8QuadMax**  | - 6× A72 @ 1.8 GHz        | - Industrial-grade     |
|                        | - 4× M4F cores            | - TSN networking       |
|                        | - Vivante GC7000L GPU     | - NXP support          |
|                        | - 16 GB LPDDR4            | - Avionics history     |
+------------------------+---------------------------+------------------------+
| **Intel Atom C3958**   | - 16× Atom cores          | - High compute         |
|                        | - AVX-512 instructions    | - x86 compatibility    |
|                        | - 128 GB DDR4             | - Massive I/O          |
|                        | - 100G Ethernet           | - Server workloads     |
+------------------------+---------------------------+------------------------+
| **MediaTek Genio      | - 8× A78 @ 2.2 GHz        | - Cost-effective       |
| 1200**                 | - Mali G57 GPU            | - AI accelerator (APU) |
|                        | - 16 GB LPDDR4X           | - Rich multimedia      |
+------------------------+---------------------------+------------------------+

**Recommended:** **Qualcomm SA8295P**
- Automotive-grade (proven reliability)
- Excellent video encode/decode (12 streams @ 1080p)
- Safety Island (R52 cores for QNX watchdog)
- Long-term support (10+ years)

**2.2 Software Stack**
~~~~~~~~~~~~~~~~~~~~~~

**Head-End Server Software Architecture:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │                  Application Layer                      │
   ├─────────────────────────────────────────────────────────┤
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
   │  │ Video    │  │ Game     │  │ Content  │              │
   │  │ Encoder  │  │ Server   │  │ Manager  │              │
   │  │ (Docker) │  │ (K3s)    │  │ (Docker) │              │
   │  └──────────┘  └──────────┘  └──────────┘              │
   ├─────────────────────────────────────────────────────────┤
   │              Container Orchestration                    │
   │  - Docker Engine 24.0                                   │
   │  - K3s (Lightweight Kubernetes) 1.28                    │
   ├─────────────────────────────────────────────────────────┤
   │                  Linux Kernel                           │
   │  - Kernel: 6.1 LTS (long-term support)                  │
   │  - Scheduler: CFS (Completely Fair Scheduler)           │
   │  - Network: Bridge, VLAN, IGMP snooping                 │
   │  - Storage: ext4, RAID 1 (md)                           │
   ├─────────────────────────────────────────────────────────┤
   │              Hardware Abstraction                       │
   │  - Bootloader: U-Boot 2023.10                           │
   │  - Video: V4L2 (Video4Linux2)                           │
   │  - GPU: Mesa (OpenGL ES, Vulkan)                        │
   │  - Network: DPDK (Data Plane Development Kit) optional  │
   └─────────────────────────────────────────────────────────┘

**Docker Compose for Head-End Services:**

.. code-block:: yaml

   # docker-compose.yml for IFE Head-End
   version: '3.8'
   
   services:
     # Video Encoder Service
     video-encoder:
       image: ife/video-encoder:v2.1
       container_name: video_encoder
       restart: always
       devices:
         - /dev/video0:/dev/video0  # Hardware encoder
       volumes:
         - /mnt/content:/content:ro
         - /var/log/ife:/logs
       environment:
         - CODEC=h265
         - BITRATE=3000k
         - RESOLUTION=1920x1080
         - FPS=30
       networks:
         - ife_network
       deploy:
         resources:
           limits:
             cpus: '4.0'
             memory: 4G
     
     # RTSP Streaming Server
     rtsp-server:
       image: ife/rtsp-server:v1.5
       container_name: rtsp_server
       restart: always
       ports:
         - "554:554"      # RTSP
         - "8554:8554"    # HTTP tunneling
       volumes:
         - /mnt/content:/content:ro
       environment:
         - MULTICAST_BASE=239.255.1.1
         - MULTICAST_TTL=5
       networks:
         - ife_network
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 2G
     
     # Content Database
     content-db:
       image: postgres:15-alpine
       container_name: content_db
       restart: always
       volumes:
         - db-data:/var/lib/postgresql/data
       environment:
         - POSTGRES_DB=ife_content
         - POSTGRES_USER=ife_admin
         - POSTGRES_PASSWORD=secure_password
       networks:
         - ife_network
       deploy:
         resources:
           limits:
             memory: 1G
     
     # Content Manager API
     content-manager:
       image: ife/content-manager:v3.0
       container_name: content_manager
       restart: always
       ports:
         - "8080:8080"
       depends_on:
         - content-db
       volumes:
         - /mnt/content:/content
       environment:
         - DB_HOST=content-db
         - DB_NAME=ife_content
       networks:
         - ife_network
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 2G
     
     # Game Server
     game-server:
       image: ife/game-server:v2.0
       container_name: game_server
       restart: always
       ports:
         - "8888:8888"
       volumes:
         - /mnt/games:/games:ro
       networks:
         - ife_network
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
     
     # WiFi Hotspot Controller
     wifi-controller:
       image: ife/wifi-controller:v1.8
       container_name: wifi_controller
       restart: always
       network_mode: host  # Direct access to WiFi interfaces
       cap_add:
         - NET_ADMIN
       environment:
         - SSID=PanasonicWiFi
         - CHANNEL=36
         - BANDWIDTH=80MHz
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
     
     # Moving Maps Service
     moving-maps:
       image: ife/moving-maps:v1.3
       container_name: moving_maps
       restart: always
       ports:
         - "9000:9000"
       devices:
         - /dev/ttyS1:/dev/gps  # GPS serial port
       volumes:
         - /mnt/maps:/maps:ro
       networks:
         - ife_network
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 1G
     
     # Prometheus Monitoring
     prometheus:
       image: prom/prometheus:v2.45
       container_name: prometheus
       restart: always
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
         - prometheus-data:/prometheus
       networks:
         - ife_network
     
     # Grafana Dashboard
     grafana:
       image: grafana/grafana:10.0
       container_name: grafana
       restart: always
       ports:
         - "3000:3000"
       volumes:
         - grafana-data:/var/lib/grafana
       environment:
         - GF_SECURITY_ADMIN_PASSWORD=admin123
       networks:
         - ife_network
   
   networks:
     ife_network:
       driver: bridge
       ipam:
         config:
           - subnet: 172.20.0.0/16
   
   volumes:
     db-data:
     prometheus-data:
     grafana-data:

**2.3 Video Encoding Pipeline**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**H.265 (HEVC) Encoding with Hardware Acceleration:**

.. code-block:: python

   #!/usr/bin/env python3
   """
   IFE Video Encoder using Qualcomm hardware acceleration
   Encodes movies to H.265 for multicast streaming
   """
   
   import subprocess
   import json
   from pathlib import Path
   
   class IFEVideoEncoder:
       def __init__(self, input_dir="/mnt/content/raw",
                    output_dir="/mnt/content/encoded"):
           self.input_dir = Path(input_dir)
           self.output_dir = Path(output_dir)
           self.output_dir.mkdir(exist_ok=True)
       
       def encode_movie(self, input_file, bitrate="3000k"):
           """
           Encode movie using hardware H.265 encoder
           
           Args:
               input_file: Path to input video (e.g., movie.mp4)
               bitrate: Target bitrate (default: 3000k for 1080p)
           """
           input_path = self.input_dir / input_file
           output_path = self.output_dir / f"{input_path.stem}_h265.mp4"
           
           # FFmpeg command with Qualcomm hardware encoder
           cmd = [
               'ffmpeg',
               '-hwaccel', 'qsv',              # Qualcomm hardware accel
               '-i', str(input_path),
               '-c:v', 'hevc_qsv',             # H.265 hardware encoder
               '-preset', 'medium',            # Balance quality/speed
               '-b:v', bitrate,                # Video bitrate
               '-maxrate', bitrate,
               '-bufsize', f"{int(bitrate[:-1]) * 2}k",
               '-vf', 'scale=1920:1080',       # Normalize to 1080p
               '-r', '30',                     # 30 fps
               '-c:a', 'aac',                  # Audio codec
               '-b:a', '128k',                 # Audio bitrate
               '-ac', '2',                     # Stereo audio
               '-movflags', '+faststart',      # Web optimization
               '-y',                           # Overwrite output
               str(output_path)
           ]
           
           print(f"Encoding: {input_file}")
           print(f"Command: {' '.join(cmd)}")
           
           result = subprocess.run(cmd, capture_output=True, text=True)
           
           if result.returncode == 0:
               print(f"✅ Encoded successfully: {output_path}")
               self.extract_metadata(output_path)
           else:
               print(f"❌ Encoding failed: {result.stderr}")
       
       def extract_metadata(self, video_file):
           """Extract metadata using ffprobe"""
           cmd = [
               'ffprobe',
               '-v', 'quiet',
               '-print_format', 'json',
               '-show_format',
               '-show_streams',
               str(video_file)
           ]
           
           result = subprocess.run(cmd, capture_output=True, text=True)
           metadata = json.loads(result.stdout)
           
           # Save metadata for content manager
           metadata_file = video_file.with_suffix('.json')
           with open(metadata_file, 'w') as f:
               json.dump(metadata, f, indent=2)
           
           print(f"📄 Metadata saved: {metadata_file}")
       
       def encode_all(self):
           """Encode all movies in input directory"""
           video_files = list(self.input_dir.glob('*.mp4')) + \
                        list(self.input_dir.glob('*.mkv')) + \
                        list(self.input_dir.glob('*.avi'))
           
           for video in video_files:
               self.encode_movie(video.name)
   
   if __name__ == "__main__":
       encoder = IFEVideoEncoder()
       encoder.encode_all()

**Encoding Performance:**

+------------------+-----------------+-------------------+
| **Resolution**   | **Bitrate**     | **Encode Speed**  |
+==================+=================+===================+
| **720p**         | 1.5 Mbps        | 8× real-time      |
| **1080p**        | 3 Mbps          | 4× real-time      |
| **4K UHD**       | 10 Mbps         | 1× real-time      |
+------------------+-----------------+-------------------+

**Example:** 2-hour movie (7200 seconds)
- Encoding time @ 4× speed = 1800 seconds = 30 minutes
- File size @ 3 Mbps = 3 Mbps × 7200s / 8 = 2.7 GB

═══════════════════════════════════════════════════════════════════════

📺 **3. SEAT UNIT ARCHITECTURE**
─────────────────────────────────────────────────────────────────────────

**3.1 Seat Unit Hardware**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical Seat Unit (Seatback Display):**

+-----------------------+--------------------------------+
| **Component**         | **Specification**              |
+=======================+================================+
| **Display**           | 15.6" touchscreen (capacitive) |
| **Resolution**        | 1920×1080 (Full HD)            |
| **SOC**               | NXP i.MX 8M Plus (Quad A53)    |
| **CPU**               | 4× ARM Cortex-A53 @ 1.8 GHz    |
| **GPU**               | Vivante GC7000UL               |
| **RAM**               | 2 GB LPDDR4                    |
| **Storage**           | 8 GB eMMC                      |
| **Network**           | 100 Mbps Ethernet              |
| **Audio**             | 3.5mm headphone jack, Bluetooth|
| **USB**               | 2× USB-A (charging)            |
| **Power**             | 28V DC (aircraft power)        |
+-----------------------+--------------------------------+

**Block Diagram:**

.. code-block:: text

   ┌─────────────────────────────────────────────────┐
   │           Seat Unit (i.MX 8M Plus)              │
   ├─────────────────────────────────────────────────┤
   │  ┌────────────┐    ┌──────────────────────┐     │
   │  │ Touchscreen│    │  Video Decoder       │     │
   │  │ 15.6" FHD  │◀───│  (H.265 hardware)    │     │
   │  │ (MIPI-DSI) │    │  (Hantro VPU)        │     │
   │  └────────────┘    └──────────────────────┘     │
   │                              ▲                   │
   │                              │                   │
   │  ┌──────────────────────────┴───────────────┐   │
   │  │       Application Layer                  │   │
   │  │  - Video Player (GStreamer)              │   │
   │  │  - Game Engine (HTML5 WebView)           │   │
   │  │  - Moving Maps (OpenGL ES)               │   │
   │  │  - Media Library (Qt/QML)                │   │
   │  └──────────────────────────────────────────┘   │
   │                      ▲                           │
   │  ┌──────────────────┴───────────────────────┐   │
   │  │       Linux Kernel 6.1 LTS               │   │
   │  │  - Network: TCP/IP, IGMP client          │   │
   │  │  - Video: V4L2, Hantro driver            │   │
   │  │  - Audio: ALSA                           │   │
   │  │  - Touch: evdev input driver             │   │
   │  └──────────────────────────────────────────┘   │
   │                      ▲                           │
   │  ┌──────────────────┴───────────────────────┐   │
   │  │  U-Boot Bootloader                       │   │
   │  │  - Boot from eMMC                        │   │
   │  │  - OTA update support                    │   │
   │  └──────────────────────────────────────────┘   │
   └─────────────────────────────────────────────────┘
           │                    │
           │ Ethernet           │ Power
           │ (100 Mbps)         │ (28V DC)
           ▼                    ▼
      Cabin Network       Aircraft Power

**3.2 Seat Unit Software**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Yocto-based Linux Image:**

.. code-block:: bash

   # meta-ife/recipes-core/images/ife-seat-image.bb
   
   DESCRIPTION = "IFE Seat Unit Linux Image"
   LICENSE = "MIT"
   
   inherit core-image
   
   IMAGE_FEATURES += " \
       splash \
       ssh-server-dropbear \
       hwcodecs \
       package-management \
   "
   
   CORE_IMAGE_EXTRA_INSTALL += " \
       gstreamer1.0 \
       gstreamer1.0-plugins-base \
       gstreamer1.0-plugins-good \
       gstreamer1.0-plugins-bad \
       gstreamer1.0-libav \
       qtbase \
       qtdeclarative \
       qtmultimedia \
       qtwebengine \
       weston \
       wayland \
       mesa \
       alsa-utils \
       openssh \
       networkmanager \
       can-utils \
       i2c-tools \
       ife-video-player \
       ife-game-client \
       ife-moving-maps \
   "
   
   # Read-only root filesystem for reliability
   IMAGE_FEATURES += "read-only-rootfs"

**Video Player Application (GStreamer):**

.. code-block:: python

   #!/usr/bin/env python3
   """
   IFE Seat Video Player
   Receives H.265 multicast stream and displays on touchscreen
   """
   
   import gi
   gi.require_version('Gst', '1.0')
   gi.require_version('GstVideo', '1.0')
   from gi.repository import Gst, GLib, GstVideo
   
   import sys
   
   Gst.init(None)
   
   class IFEVideoPlayer:
       def __init__(self, multicast_ip="239.255.1.1", port=5004):
           self.multicast_ip = multicast_ip
           self.port = port
           self.pipeline = None
       
       def create_pipeline(self):
           """
           Create GStreamer pipeline for RTSP/RTP multicast reception
           Uses hardware H.265 decoder (Hantro VPU on i.MX 8M Plus)
           """
           pipeline_str = (
               f"udpsrc multicast-group={self.multicast_ip} "
               f"port={self.port} ! "
               "application/x-rtp,encoding-name=H265,payload=96 ! "
               "rtph265depay ! "
               "h265parse ! "
               "v4l2h265dec ! "          # Hardware decoder
               "waylandsink fullscreen=true sync=false"
           )
           
           print(f"Pipeline: {pipeline_str}")
           self.pipeline = Gst.parse_launch(pipeline_str)
           
           # Setup message bus for errors
           bus = self.pipeline.get_bus()
           bus.add_signal_watch()
           bus.connect("message", self.on_message)
       
       def on_message(self, bus, message):
           """Handle GStreamer messages"""
           t = message.type
           if t == Gst.MessageType.EOS:
               print("End of stream")
               self.pipeline.set_state(Gst.State.NULL)
           elif t == Gst.MessageType.ERROR:
               err, debug = message.parse_error()
               print(f"Error: {err}, {debug}")
               self.pipeline.set_state(Gst.State.NULL)
           elif t == Gst.MessageType.STATE_CHANGED:
               if message.src == self.pipeline:
                   old, new, pending = message.parse_state_changed()
                   print(f"State changed: {old.value_nick} -> {new.value_nick}")
       
       def play(self):
           """Start playback"""
           print("Starting playback...")
           self.pipeline.set_state(Gst.State.PLAYING)
       
       def stop(self):
           """Stop playback"""
           self.pipeline.set_state(Gst.State.NULL)
   
   if __name__ == "__main__":
       if len(sys.argv) < 2:
           print("Usage: ife_player.py <multicast_ip>")
           print("Example: ife_player.py 239.255.1.1")
           sys.exit(1)
       
       multicast_ip = sys.argv[1]
       
       player = IFEVideoPlayer(multicast_ip=multicast_ip)
       player.create_pipeline()
       player.play()
       
       # Run GLib main loop
       loop = GLib.MainLoop()
       try:
           loop.run()
       except KeyboardInterrupt:
           print("Interrupted by user")
           player.stop()

**3.3 Seat Unit Boot Sequence**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Boot Flow (from power-on to ready):**

.. code-block:: text

   Power On (28V DC)
        │
        ▼
   ┌─────────────────────────────────────┐
   │  U-Boot (1-2 seconds)               │
   │  - Initialize DDR, eMMC             │
   │  - Check for OTA updates            │
   │  - Load kernel from eMMC            │
   └───────────────┬─────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────┐
   │  Linux Kernel (3-5 seconds)         │
   │  - Mount root filesystem (squashfs) │
   │  - Initialize network (Ethernet UP) │
   │  - Load GPU driver (Vivante)        │
   │  - Load video decoder (Hantro VPU)  │
   └───────────────┬─────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────┐
   │  Systemd Init (2-3 seconds)         │
   │  - Start Wayland compositor         │
   │  - Start network manager            │
   │  - Start IFE services               │
   └───────────────┬─────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────┐
   │  IFE Application (3-5 seconds)      │
   │  - Display splash screen            │
   │  - Connect to head-end server       │
   │  - Fetch content catalog            │
   │  - Display main menu                │
   └───────────────┬─────────────────────┘
                   │
                   ▼
            Ready for Passenger
          (Total: 10-15 seconds)

**systemd Service for Video Player:**

.. code-block:: ini

   # /etc/systemd/system/ife-player.service
   [Unit]
   Description=IFE Video Player
   After=network.target wayland.service
   
   [Service]
   Type=simple
   User=ife
   Environment="XDG_RUNTIME_DIR=/run/user/1000"
   Environment="WAYLAND_DISPLAY=wayland-0"
   ExecStart=/usr/bin/ife_player.py 239.255.1.1
   Restart=always
   RestartSec=5
   
   [Install]
   WantedBy=multi-user.target

═══════════════════════════════════════════════════════════════════════

🌐 **4. CABIN NETWORK ARCHITECTURE**
─────────────────────────────────────────────────────────────────────────

**4.1 Network Topology**
~~~~~~~~~~~~~~~~~~~~~~~~~

**AFDX Part 10 (Switched Ethernet for IFE):**

.. code-block:: text

   ┌────────────────────────────────────────────────────────┐
   │              Head-End Server Rack                      │
   │  ┌──────────────┐    ┌──────────────┐                 │
   │  │  Server 1    │    │  Server 2    │                 │
   │  │ (Primary)    │    │ (Standby)    │                 │
   │  │ 10.1.1.10/24 │    │ 10.1.1.11/24 │                 │
   │  └──────┬───────┘    └──────┬───────┘                 │
   │         │                   │                          │
   │         └─────────┬─────────┘                          │
   │                   │                                    │
   └───────────────────┼────────────────────────────────────┘
                       │ Trunk (VLANs: 100, 200, 300)
                       │
   ┌───────────────────▼────────────────────────────────────┐
   │          Core Switch (VLAN-aware)                      │
   │  - Model: Cisco IE-3400-8T2S                           │
   │  - Ports: 8× 1GbE + 2× 10GbE SFP+                      │
   │  - Features: VLAN, IGMP snooping, QoS                  │
   └───┬───────────────┬────────────────┬───────────────────┘
       │               │                │
       │ VLAN 100      │ VLAN 200       │ VLAN 300
       │ (Video)       │ (WiFi)         │ (Crew)
       │               │                │
   ┌───▼─────┐    ┌────▼────┐      ┌───▼─────┐
   │ Access  │    │ Access  │      │ Crew    │
   │ Switch  │    │ Points  │      │ Panels  │
   │ Row 1-10│    │ (WiFi)  │      │         │
   └───┬─────┘    └─────────┘      └─────────┘
       │
       │ 100 Mbps per seat
       │
   ┌───▼────┐ ┌────────┐ ┌────────┐
   │ Seat 1A│ │ Seat 1B│ │ Seat 1C│  ... (300 seats)
   └────────┘ └────────┘ └────────┘

**VLAN Configuration:**

+-------------+----------------------+---------------------------+
| **VLAN ID** | **Purpose**          | **IP Subnet**             |
+=============+======================+===========================+
| **100**     | Video Streaming      | 10.100.0.0/16             |
| **200**     | Passenger WiFi       | 10.200.0.0/16             |
| **300**     | Crew Network         | 10.300.0.0/24             |
| **999**     | Management           | 192.168.1.0/24            |
+-------------+----------------------+---------------------------+

**4.2 Multicast Streaming**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**IGMP Configuration for Video Channels:**

.. code-block:: text

   Movie Channels (Multicast Groups):
   
   Channel 1 (Latest Movie 1):   239.255.1.1:5004
   Channel 2 (Latest Movie 2):   239.255.1.2:5004
   Channel 3 (Classic Movie):    239.255.1.3:5004
   Channel 4 (Kids Movie):       239.255.1.4:5004
   Channel 5 (TV Series 1):      239.255.1.5:5004
   Channel 6 (TV Series 2):      239.255.1.6:5004
   Channel 7 (Live TV):          239.255.1.7:5004
   Channel 8 (Moving Maps):      239.255.1.8:5004

**Head-End: Multicast Sender (FFmpeg):**

.. code-block:: bash

   #!/bin/bash
   # stream_movie.sh - Stream movie to multicast group
   
   MOVIE_FILE="/mnt/content/encoded/movie1_h265.mp4"
   MULTICAST_IP="239.255.1.1"
   PORT=5004
   BITRATE=3000k
   
   ffmpeg -re \
       -i "$MOVIE_FILE" \
       -c:v copy \
       -c:a copy \
       -f rtp_mpegts \
       -sdp_file /tmp/channel1.sdp \
       "rtp://${MULTICAST_IP}:${PORT}?ttl=5"

**Seat Unit: Multicast Receiver (GStreamer):**

.. code-block:: bash

   # Join multicast group and play
   gst-launch-1.0 \
       udpsrc multicast-group=239.255.1.1 port=5004 ! \
       application/x-rtp,encoding-name=H265,payload=96 ! \
       rtph265depay ! \
       h265parse ! \
       v4l2h265dec ! \
       waylandsink fullscreen=true

**Switch Configuration (IGMP Snooping):**

.. code-block:: text

   ! Enable IGMP snooping globally
   ip igmp snooping
   
   ! Enable IGMP snooping on VLAN 100 (video)
   ip igmp snooping vlan 100
   
   ! Set multicast router port (to head-end)
   ip igmp snooping vlan 100 mrouter interface GigabitEthernet1/0/1
   
   ! Enable querier
   ip igmp snooping vlan 100 querier

**Bandwidth Calculation:**

.. code-block:: text

   Scenario: 300 passengers, 8 video channels
   
   Option 1: Unicast (BAD)
   - If 100 passengers watch Channel 1 (3 Mbps each)
   - Bandwidth = 100 × 3 Mbps = 300 Mbps (exceeds 1 Gbps with other channels)
   
   Option 2: Multicast (GOOD)
   - Channel 1 streamed once at 3 Mbps
   - All 100 passengers receive same stream
   - Bandwidth = 3 Mbps (regardless of viewer count)
   - Total for 8 channels = 8 × 3 Mbps = 24 Mbps
   
   Savings: 300 Mbps → 24 Mbps (92% reduction)

═══════════════════════════════════════════════════════════════════════

📥 **5. CONTENT MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**5.1 Content Workflow**
~~~~~~~~~~~~~~~~~~~~~~~~~

**End-to-End Content Pipeline:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────┐
   │         1. Studio Delivery                           │
   │  - Format: DCP (Digital Cinema Package)             │
   │  - Resolution: 4K (mastered)                         │
   │  - DRM: Encrypted (studio keys)                      │
   └─────────────────┬────────────────────────────────────┘
                     │ Secure Transfer
   ┌─────────────────▼────────────────────────────────────┐
   │       2. Ground CMS (Content Management System)      │
   │  - Ingest movie files                                │
   │  - Transcode to H.265 (1080p @ 3 Mbps)               │
   │  - Extract metadata (title, cast, rating, subtitles) │
   │  - Add artwork (poster, thumbnails)                  │
   │  - Assign to flight playlists                        │
   └─────────────────┬────────────────────────────────────┘
                     │ USB Drive or WiFi Upload
   ┌─────────────────▼────────────────────────────────────┐
   │    3. Aircraft Head-End Server (Pre-Flight Load)     │
   │  - Verify checksums (SHA-256)                        │
   │  - Copy to RAID storage (2 TB NVMe SSD)              │
   │  - Update content database (PostgreSQL)              │
   │  - Generate playlists for seat units                 │
   └─────────────────┬────────────────────────────────────┘
                     │ Cabin Network
   ┌─────────────────▼────────────────────────────────────┐
   │         4. Seat Units (In-Flight Access)             │
   │  - Fetch catalog from head-end                       │
   │  - Display movie library                             │
   │  - Stream on-demand via multicast                    │
   └──────────────────────────────────────────────────────┘

**5.2 Content Database Schema**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**PostgreSQL Schema:**

.. code-block:: sql

   -- Content Database for IFE System
   
   CREATE TABLE movies (
       id SERIAL PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       description TEXT,
       release_year INT,
       runtime INT,  -- minutes
       rating VARCHAR(10),  -- G, PG, PG-13, R
       genre VARCHAR(100),  -- Action, Comedy, Drama, etc.
       language VARCHAR(50),
       file_path VARCHAR(500),
       file_size BIGINT,  -- bytes
       checksum VARCHAR(64),  -- SHA-256
       created_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE TABLE cast_crew (
       id SERIAL PRIMARY KEY,
       movie_id INT REFERENCES movies(id),
       person_name VARCHAR(255),
       role VARCHAR(50),  -- Actor, Director, Producer
       character_name VARCHAR(255)  -- For actors
   );
   
   CREATE TABLE subtitles (
       id SERIAL PRIMARY KEY,
       movie_id INT REFERENCES movies(id),
       language VARCHAR(50),
       file_path VARCHAR(500)
   );
   
   CREATE TABLE playlists (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255),
       description TEXT,
       created_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE TABLE playlist_movies (
       playlist_id INT REFERENCES playlists(id),
       movie_id INT REFERENCES movies(id),
       position INT,
       PRIMARY KEY (playlist_id, movie_id)
   );
   
   CREATE TABLE viewing_stats (
       id SERIAL PRIMARY KEY,
       seat_number VARCHAR(10),  -- e.g., "12A"
       movie_id INT REFERENCES movies(id),
       started_at TIMESTAMP,
       stopped_at TIMESTAMP,
       duration_watched INT  -- seconds
   );

**Example Data:**

.. code-block:: sql

   INSERT INTO movies (title, description, release_year, runtime, rating, genre, language, file_path, file_size, checksum)
   VALUES (
       'Top Gun: Maverick',
       'After thirty years, Maverick is still pushing the envelope as a top naval aviator.',
       2022,
       131,
       'PG-13',
       'Action',
       'English',
       '/mnt/content/encoded/top_gun_maverick_h265.mp4',
       2850000000,  -- ~2.85 GB
       'a1b2c3d4e5f6...'
   );
   
   INSERT INTO cast_crew (movie_id, person_name, role, character_name)
   VALUES
       (1, 'Tom Cruise', 'Actor', 'Pete "Maverick" Mitchell'),
       (1, 'Jennifer Connelly', 'Actor', 'Penny Benjamin'),
       (1, 'Joseph Kosinski', 'Director', NULL);

**5.3 Content Loading Process**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ground-to-Aircraft Transfer:**

.. code-block:: python

   #!/usr/bin/env python3
   """
   Content Loading Script
   Transfer movies from ground CMS to aircraft head-end
   """
   
   import hashlib
   import shutil
   from pathlib import Path
   import psycopg2
   
   class ContentLoader:
       def __init__(self, source_dir="/media/usb/content",
                    dest_dir="/mnt/content/encoded"):
           self.source_dir = Path(source_dir)
           self.dest_dir = Path(dest_dir)
           self.db_conn = psycopg2.connect(
               host="localhost",
               database="ife_content",
               user="ife_admin",
               password="secure_password"
           )
       
       def verify_checksum(self, file_path, expected_checksum):
           """Verify file integrity using SHA-256"""
           sha256 = hashlib.sha256()
           with open(file_path, 'rb') as f:
               for chunk in iter(lambda: f.read(4096), b""):
                   sha256.update(chunk)
           
           actual_checksum = sha256.hexdigest()
           return actual_checksum == expected_checksum
       
       def copy_movie(self, movie_file, metadata):
           """Copy movie to aircraft storage and update database"""
           source_path = self.source_dir / movie_file
           dest_path = self.dest_dir / movie_file
           
           # Verify checksum before copy
           if not self.verify_checksum(source_path, metadata['checksum']):
               print(f"❌ Checksum mismatch for {movie_file}")
               return False
           
           # Copy file
           print(f"Copying {movie_file}...")
           shutil.copy2(source_path, dest_path)
           
           # Verify checksum after copy
           if not self.verify_checksum(dest_path, metadata['checksum']):
               print(f"❌ Copy verification failed for {movie_file}")
               dest_path.unlink()
               return False
           
           # Update database
           cursor = self.db_conn.cursor()
           cursor.execute("""
               INSERT INTO movies (title, description, release_year, runtime,
                                  rating, genre, language, file_path, file_size, checksum)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """, (
               metadata['title'],
               metadata['description'],
               metadata['release_year'],
               metadata['runtime'],
               metadata['rating'],
               metadata['genre'],
               metadata['language'],
               str(dest_path),
               dest_path.stat().st_size,
               metadata['checksum']
           ))
           self.db_conn.commit()
           
           print(f"✅ Successfully loaded {movie_file}")
           return True
   
   if __name__ == "__main__":
       loader = ContentLoader()
       
       # Example metadata (normally read from manifest file)
       metadata = {
           'title': 'Top Gun: Maverick',
           'description': 'After thirty years...',
           'release_year': 2022,
           'runtime': 131,
           'rating': 'PG-13',
           'genre': 'Action',
           'language': 'English',
           'checksum': 'a1b2c3d4e5f6...'
       }
       
       loader.copy_movie('top_gun_maverick_h265.mp4', metadata)

═══════════════════════════════════════════════════════════════════════

🔒 **6. REDUNDANCY AND FAILOVER**
─────────────────────────────────────────────────────────────────────────

**6.1 Dual Head-End Servers**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Active-Standby Configuration:**

.. code-block:: text

   ┌──────────────────┐         ┌──────────────────┐
   │  Server 1        │         │  Server 2        │
   │  (PRIMARY)       │◀───────▶│  (STANDBY)       │
   │  10.1.1.10       │  sync   │  10.1.1.11       │
   │  ┌────────────┐  │         │  ┌────────────┐  │
   │  │  Services  │  │         │  │  Services  │  │
   │  │  ✅ ACTIVE │  │         │  │  ⏸️ STANDBY│  │
   │  └────────────┘  │         │  └────────────┘  │
   │  ┌────────────┐  │         │  ┌────────────┐  │
   │  │  Heartbeat │──┼────────▶│  │  Heartbeat │  │
   │  │  (1 Hz)    │  │         │  │  Monitor   │  │
   │  └────────────┘  │         │  └────────────┘  │
   └──────────────────┘         └──────────────────┘
            │                            │
            │   Virtual IP: 10.1.1.100   │
            └────────────┬───────────────┘
                         │
                    Cabin Network
                         │
                    Seat Units

**Heartbeat Monitoring (Keepalived):**

.. code-block:: bash

   # /etc/keepalived/keepalived.conf (Server 1 - Primary)
   
   vrrp_script check_services {
       script "/usr/local/bin/check_ife_services.sh"
       interval 2
       weight 2
   }
   
   vrrp_instance IFE_HEADEND {
       state MASTER
       interface eth0
       virtual_router_id 51
       priority 100
       advert_int 1
       
       authentication {
           auth_type PASS
           auth_pass ife_secret
       }
       
       virtual_ipaddress {
           10.1.1.100/24
       }
       
       track_script {
           check_services
       }
   }

**Service Health Check Script:**

.. code-block:: bash

   #!/bin/bash
   # /usr/local/bin/check_ife_services.sh
   
   # Check critical Docker services
   REQUIRED_SERVICES=(
       "video_encoder"
       "rtsp_server"
       "content_db"
       "content_manager"
   )
   
   for service in "${REQUIRED_SERVICES[@]}"; do
       if ! docker ps | grep -q "$service"; then
           echo "❌ Service $service is down"
           exit 1
       fi
   done
   
   # Check disk space (must have > 10% free)
   DISK_USAGE=$(df /mnt/content | tail -1 | awk '{print $5}' | sed 's/%//')
   if [ "$DISK_USAGE" -gt 90 ]; then
       echo "❌ Disk usage critical: ${DISK_USAGE}%"
       exit 1
   fi
   
   echo "✅ All services healthy"
   exit 0

**Automatic Failover Sequence:**

.. code-block:: text

   Normal Operation:
   - Server 1 (Primary) sends heartbeat every 1 second
   - Server 2 (Standby) monitors heartbeat
   - Virtual IP 10.1.1.100 points to Server 1
   
   Failure Detected:
   1. Server 2 doesn't receive heartbeat for 3 seconds
   2. Server 2 runs health check script
   3. Server 2 takes over virtual IP 10.1.1.100
   4. Server 2 starts Docker services (from standby)
   5. Seat units reconnect to 10.1.1.100 (now Server 2)
   
   Failover Time: < 5 seconds
   User Impact: Minimal (video buffering absorbs interruption)

**6.2 RAID Storage**
~~~~~~~~~~~~~~~~~~~~

**RAID 1 (Mirroring) for Content:**

.. code-block:: bash

   # Create RAID 1 array with 2× 2TB NVMe SSDs
   mdadm --create --verbose /dev/md0 \
       --level=1 \
       --raid-devices=2 \
       /dev/nvme0n1 /dev/nvme1n1
   
   # Create filesystem
   mkfs.ext4 /dev/md0
   
   # Mount at /mnt/content
   mkdir -p /mnt/content
   mount /dev/md0 /mnt/content
   
   # Add to /etc/fstab for auto-mount
   echo "/dev/md0 /mnt/content ext4 defaults 0 2" >> /etc/fstab

**Monitor RAID Status:**

.. code-block:: bash

   # Check RAID status
   cat /proc/mdstat
   
   # Detailed info
   mdadm --detail /dev/md0
   
   # Example output:
   # /dev/md0:
   #   State : clean
   #   Active Devices : 2
   #   Failed Devices : 0
   #   Spare Devices : 0

**Automatic Disk Failure Recovery:**

.. code-block:: bash

   # Scenario: /dev/nvme1n1 fails
   
   # 1. RAID detects failure automatically
   # 2. System continues running on /dev/nvme0n1
   
   # 3. Replace failed disk physically
   # 4. Add new disk to array
   mdadm --manage /dev/md0 --add /dev/nvme2n1
   
   # 5. RAID rebuilds automatically
   # Watch rebuild progress
   watch cat /proc/mdstat

═══════════════════════════════════════════════════════════════════════

📊 **7. MONITORING AND DIAGNOSTICS**
─────────────────────────────────────────────────────────────────────────

**7.1 Prometheus + Grafana**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Prometheus Configuration:**

.. code-block:: yaml

   # prometheus.yml
   global:
     scrape_interval: 15s
     evaluation_interval: 15s
   
   scrape_configs:
     # Head-End Server Metrics
     - job_name: 'head-end-server'
       static_configs:
         - targets: ['localhost:9100']  # Node Exporter
     
     # Docker Containers
     - job_name: 'docker-containers'
       static_configs:
         - targets: ['localhost:9323']  # Docker metrics
     
     # PostgreSQL
     - job_name: 'postgres'
       static_configs:
         - targets: ['localhost:9187']  # postgres_exporter
     
     # Network Switches (SNMP)
     - job_name: 'cabin-switches'
       static_configs:
         - targets:
             - '10.1.1.20'  # Core switch
             - '10.1.1.21'  # Access switch row 1-10
             - '10.1.1.22'  # Access switch row 11-20
       metrics_path: /snmp
       params:
         module: [if_mib]
       relabel_configs:
         - source_labels: [__address__]
           target_label: __param_target
         - source_labels: [__param_target]
           target_label: instance
         - target_label: __address__
           replacement: localhost:9116  # SNMP exporter address

**Key Metrics to Monitor:**

+---------------------------+------------------------------+
| **Metric**                | **Alerting Threshold**       |
+===========================+==============================+
| **CPU Usage**             | > 80% for 5 minutes          |
| **Memory Usage**          | > 90%                        |
| **Disk Space**            | < 10% free                   |
| **Network Bandwidth**     | > 800 Mbps (1 Gbps link)     |
| **Video Encoder Queue**   | > 10 pending requests        |
| **Database Connections**  | > 80 active connections      |
| **RAID Status**           | Degraded or failed disk      |
| **Heartbeat**             | No heartbeat for 3 seconds   |
+---------------------------+------------------------------+

**Grafana Dashboard (JSON):**

.. code-block:: json

   {
     "dashboard": {
       "title": "IFE System Dashboard",
       "panels": [
         {
           "title": "Active Video Streams",
           "type": "graph",
           "targets": [
             {
               "expr": "sum(rate(rtsp_streams_total[5m]))"
             }
           ]
         },
         {
           "title": "Seat Unit Health",
           "type": "stat",
           "targets": [
             {
               "expr": "count(up{job='seat-units'} == 1)"
             }
           ]
         },
         {
           "title": "Network Bandwidth",
           "type": "graph",
           "targets": [
             {
               "expr": "rate(node_network_transmit_bytes_total{device='eth0'}[5m]) * 8"
             }
           ]
         }
       ]
     }
   }

**7.2 Logging Architecture**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Centralized Logging with Loki:**

.. code-block:: yaml

   # docker-compose.yml (add to existing services)
   
   services:
     loki:
       image: grafana/loki:2.9.0
       container_name: loki
       ports:
         - "3100:3100"
       volumes:
         - ./loki-config.yaml:/etc/loki/local-config.yaml:ro
         - loki-data:/loki
       networks:
         - ife_network
     
     promtail:
       image: grafana/promtail:2.9.0
       container_name: promtail
       volumes:
         - /var/log:/var/log:ro
         - /var/lib/docker/containers:/var/lib/docker/containers:ro
         - ./promtail-config.yaml:/etc/promtail/config.yml:ro
       networks:
         - ife_network
   
   volumes:
     loki-data:

**Promtail Configuration:**

.. code-block:: yaml

   # promtail-config.yaml
   server:
     http_listen_port: 9080
     grpc_listen_port: 0
   
   positions:
     filename: /tmp/positions.yaml
   
   clients:
     - url: http://loki:3100/loki/api/v1/push
   
   scrape_configs:
     # Docker container logs
     - job_name: docker
       docker_sd_configs:
         - host: unix:///var/run/docker.sock
           refresh_interval: 5s
       relabel_configs:
         - source_labels: ['__meta_docker_container_name']
           target_label: 'container'
     
     # System logs
     - job_name: system
       static_configs:
         - targets:
             - localhost
           labels:
             job: system
             __path__: /var/log/*log

**Query Logs:**

.. code-block:: bash

   # Using LogCLI
   
   # Show last 100 lines from video encoder
   logcli query '{container="video_encoder"}' --limit=100
   
   # Search for errors in last hour
   logcli query '{job="system"} |= "error"' --since=1h
   
   # Count warnings by container
   logcli query 'count_over_time({container=~".+"} |= "warning" [1h])'

═══════════════════════════════════════════════════════════════════════

🎓 **8. INTERVIEW PREPARATION**
─────────────────────────────────────────────────────────────────────────

**8.1 Map Resume to IFE**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Project Connections:**

1. **AFIRS SDU Platform (FLYHT) → IFE Connectivity**
   - "Developed satellite communications platform for aircraft"
   - "Experience with aircraft data links applicable to IFE ground communication"
   - "Familiar with DO-160G environmental qualification (same for IFE)"

2. **Flight Deck Video Displays (Boeing) → IFE Streaming**
   - "Implemented RTSP video streaming for cockpit displays"
   - "Directly applicable to passenger seat video streaming"
   - "Experience with aircraft-grade hardware and certification"

3. **i.MX 93 Platform (Universal Electronics) → Seat Units**
   - "Developed embedded Linux BSP for i.MX 93 (similar to i.MX 8M Plus in seats)"
   - "Yocto experience transfers to IFE seat image creation"
   - "Implemented OTA updates (critical for fleet-wide content updates)"

4. **Multicore ARM Experience → Head-End Architecture**
   - "Worked with heterogeneous ARM systems (A+M cores)"
   - "Understand resource partitioning and isolation"
   - "Applicable to QNX Hypervisor + Linux VMs"

**8.2 Technical Deep-Dive Questions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q: "How would you design a video streaming system for 300 passengers?"**

**A:**

"I'd use IP multicast to minimize bandwidth:

**Architecture:**
- Head-End: 8 video channels (movies/TV) encoded in H.265 @ 3 Mbps each
- Multicast Groups: Each channel assigned to unique group (239.255.1.1 - 239.255.1.8)
- Cabin Network: 1 Gbps Ethernet with IGMP snooping enabled
- Seat Units: Join multicast group when passenger selects channel

**Benefits:**
- Bandwidth: 8 channels × 3 Mbps = 24 Mbps total (vs 900 Mbps for unicast to 300 seats)
- Scalability: Adding passengers doesn't increase bandwidth
- Efficiency: Network switch replicates packets only to interested seats

**Implementation:**
- Use GStreamer on seat units for H.265 hardware decoding
- Qualcomm SOC in head-end for parallel H.265 encoding (12 streams capable)
- VLAN segmentation to isolate video traffic from WiFi/crew networks

This is similar to my FDVD project at Boeing, where I implemented RTSP streaming to cockpit displays."

**Q: "How would you handle failover if the head-end server crashes?"**

**A:**

"I'd implement dual redundant servers with hot standby:

**Configuration:**
- Primary Server: 10.1.1.10 (actively streaming)
- Standby Server: 10.1.1.11 (services ready but not streaming)
- Virtual IP: 10.1.1.100 (managed by Keepalived)

**Heartbeat:**
- Primary sends heartbeat every 1 second
- Standby monitors heartbeat
- If 3 missed heartbeats (3 seconds), standby takes over

**Failover Process:**
1. Standby detects primary failure
2. Standby claims virtual IP 10.1.1.100
3. Standby starts Docker services (< 2 seconds)
4. Seat units automatically reconnect to 10.1.1.100

**Total failover time:** < 5 seconds  
**User impact:** Minimal (video players have 10-second buffer)

I've implemented similar redundancy in industrial control systems with dual MQX controllers."

**Q: "What SOC would you choose for the head-end server?"**

**A:**

"I'd choose **Qualcomm SA8295P** for these reasons:

**Technical Advantages:**
1. **Video Performance:** Hardware H.265 encoder (12 streams @ 1080p)
2. **Safety Island:** R52 cores for QNX watchdog (matches Panasonic's mixed-criticality approach)
3. **Automotive-Grade:** -40°C to +105°C (exceeds aircraft cabin requirements)
4. **Long Lifecycle:** 10+ year support (critical for aircraft 20-year lifespan)
5. **Rich Ecosystem:** Linux BSP, Docker support, multimedia frameworks

**Comparison:**
- NXP i.MX 8QuadMax: Good, but less video performance
- Intel Atom: High power consumption for aircraft
- MediaTek: Cost-effective but less proven in safety-critical applications

**Trade-offs:**
- Cost: Qualcomm is premium-priced
- Complexity: More cores = more thermal management
- Power: Need efficient power supply design

From my i.MX 93 experience, I understand the BSP bring-up, bootloader customization, and thermal management needed for Qualcomm SOCs."

**8.3 Demonstrate Domain Knowledge**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Intelligent Questions to Ask:**

1. "Does Panasonic's current IFE architecture use QNX Hypervisor for safety-critical functions, or is it Linux-only?"

2. "What's the typical content library size per aircraft? I'm thinking about RAID configuration and NVMe sizing."

3. "For multicast video streaming, are you using standard IGMP snooping or AVB/TSN for deterministic latency?"

4. "How do you handle content updates - is it USB-based pre-flight loading or satellite download in-flight?"

5. "What's the certification level for IFE - TSO-C139 or higher? I'm familiar with DO-160G from my avionics background."

═══════════════════════════════════════════════════════════════════════

📚 **QUICK REFERENCE**
─────────────────────────────────────────────────────────────────────────

**IFE System Components**

+-------------------+---------------------------+-------------------+
| **Component**     | **Technology**            | **Purpose**       |
+===================+===========================+===================+
| **Head-End**      | Qualcomm SA8295P, Linux   | Content server    |
| **Seat Units**    | i.MX 8M Plus, Linux       | Passenger display |
| **Network**       | 1 Gbps Ethernet, IGMP     | Content delivery  |
| **Encoding**      | H.265 (HEVC)              | Bandwidth saving  |
| **Streaming**     | RTSP multicast            | Efficient video   |
| **Storage**       | 2TB NVMe RAID 1           | Content library   |
| **Redundancy**    | Dual servers, Keepalived  | High availability |
| **Monitoring**    | Prometheus, Grafana       | System health     |
+-------------------+---------------------------+-------------------+

**Key Metrics**

- **Passengers:** 300-400 (wide-body aircraft)
- **Video Streams:** 8-12 concurrent channels
- **Bitrate:** 3 Mbps per stream (H.265, 1080p)
- **Total Bandwidth:** 24-36 Mbps (with multicast)
- **Failover Time:** < 5 seconds
- **Boot Time:** 10-15 seconds (seat units)
- **Content Library:** 50-100 movies, 2-5 TB

═══════════════════════════════════════════════════════════════════════

✅ **KEY TAKEAWAYS**
─────────────────────────────────────────────────────────────────────────

**IFE Architecture:**
1. ✅ **Head-End Servers:** Qualcomm/MediaTek SOC, Linux + Docker/K3s
2. ✅ **Seat Units:** i.MX 8M Plus, embedded Linux, GStreamer video
3. ✅ **Network:** AFDX Part 10 Ethernet, IGMP multicast, VLAN segmentation
4. ✅ **Video:** H.265 encoding (3 Mbps @ 1080p), RTSP streaming
5. ✅ **Storage:** 2-5 TB RAID 1 NVMe, PostgreSQL database

**Content Delivery:**
1. ✅ **Ground CMS:** Ingest, transcode, metadata extraction
2. ✅ **Aircraft Upload:** USB/WiFi/satellite transfer
3. ✅ **Multicast Streaming:** 8 channels, 300 passengers, 24 Mbps total
4. ✅ **Bandwidth Savings:** 92% reduction vs unicast

**High Availability:**
1. ✅ **Dual Servers:** Active-standby with Keepalived
2. ✅ **RAID 1:** Mirrored storage for fault tolerance
3. ✅ **Failover:** < 5 second automatic recovery
4. ✅ **Monitoring:** Prometheus + Grafana dashboards

**Resume Connections:**
- ✅ **AFIRS SDU:** Aircraft communications experience
- ✅ **FDVD:** RTSP video streaming for cockpit displays
- ✅ **i.MX 93:** Embedded Linux BSP, Yocto, OTA updates
- ✅ **Multicore ARM:** Heterogeneous systems, resource partitioning

**Interview Strategy:**
- Lead with video streaming experience (FDVD project)
- Emphasize Linux + ARM SOC expertise (i.MX 93)
- Show avionics understanding (DO-160G, aircraft constraints)
- Demonstrate multicast/networking knowledge
- Ask about QNX Hypervisor and mixed-criticality architecture

═══════════════════════════════════════════════════════════════════════

**References:**

- ARINC 664 Part 7/10: Avionics Ethernet Standards
- DO-160G: Environmental Conditions and Test Procedures for Airborne Equipment
- TSO-C139: Software Approval for IFE Systems
- H.265 (HEVC): High Efficiency Video Coding Standard
- IGMP: Internet Group Management Protocol (RFC 3376)

**Last Updated:** January 2026 | **IFE Standards:** ARINC 664, DO-160G, TSO-C139

═══════════════════════════════════════════════════════════════════════
