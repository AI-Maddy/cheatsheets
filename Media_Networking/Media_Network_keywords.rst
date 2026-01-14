═══════════════════════════════════════════════════════════════════════════════
📺 MEDIA NETWORKING KEYWORDS - VISUAL CHEATSHEET 🎬
═══════════════════════════════════════════════════════════════════════════════

Your **comprehensive visual guide** to video/audio compression, transmission protocols,
networking, and video-over-IP systems. Color-coded 🌈 with memory aids 🧠 for rapid recall!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎥 VIDEO COMPRESSION SYSTEMS, CODECS & TRANSMISSION PROTOCOLS              │
└─────────────────────────────────────────────────────────────────────────────┘

🔴 **PROFESSIONAL BROADCAST STANDARDS**

  📡 **SMPTE-2022** 
     └─ Suite of standards for professional media over IP
     └─ Includes FEC and seamless switching (ST 2022-1/2/5/6/7)
     └─ 💡 Memory Aid: "20-22 = Broadcast in the 2020s!"

  📦 **RTP** (Real-time Transport Protocol)
     └─ Core protocol for real-time audio/video delivery over IP
     └─ Almost always uses UDP for low latency
     └─ 💡 Memory Aid: "RTP = Real-Time Packets!"

🟠 **SECURE & RELIABLE TRANSPORT**

  🔐 **SRT** (Secure Reliable Transport)
     └─ Low-latency, reliable UDP-based with ARQ/FEC
     └─ Internet contribution standard
     └─ 💡 Memory Aid: "SRT = Super Reliable Transport"

  🛡️ **Zixi**
     └─ Proprietary low-latency, resilient transport (similar to SRT)
     └─ Live video over unreliable networks
     └─ 💡 Memory Aid: "Zixi = Zippy & Resilient!"

🟢 **ADAPTIVE BITRATE STREAMING (ABR)**

  🍎 **HLS** (HTTP Live Streaming)
     └─ Apple's adaptive bitrate protocol
     └─ Uses segmented TS/MP4 over HTTP
     └─ 💡 Memory Aid: "HLS = HTTP Lives Streaming"

  🌍 **DASH** (Dynamic Adaptive Streaming over HTTP)
     └─ MPEG open standard (MPEG-DASH)
     └─ Adaptive bitrate for all platforms
     └─ 💡 Memory Aid: "DASH = Dynamic Adaptive Streaming HTTP"

  🪟 **Smooth Streaming**
     └─ Microsoft adaptive streaming protocol
     └─ Predecessor to modern DASH/HLS hybrids
     └─ 💡 Memory Aid: "Smooth = Microsoft's early streaming"

🔵 **VIDEO COMPRESSION CODECS**

  🦖 **MPEG-2** (H.262)
     └─ Legacy standard for broadcast, DVD, early digital TV
     └─ Still used in some broadcast workflows
     └─ 💡 Memory Aid: "MPEG-2 = 2000s Legacy"

  🎯 **H.264** (AVC / MPEG-4 Part 10)
     └─ Widely adopted block-based HD codec
     └─ Industry workhorse for streaming
     └─ 💡 Memory Aid: "264 = 2-6-4K resolution support"

  🚀 **HEVC** (H.265)
     └─ Successor to H.264 with ~50% better compression
     └─ Ideal for 4K/8K content
     └─ 💡 Memory Aid: "HEVC = High Efficiency Video Coding (265 > 264)"

  🌊 **J2K** (JPEG 2000)
     └─ Wavelet-based codec for high-quality, low-latency
     └─ Used in contribution feeds and cinema
     └─ 💡 Memory Aid: "J2K = JPEG for 2000s broadcast"

🟣 **ERROR CORRECTION & PROTECTION**

  🛡️ **FEC** (Forward Error Correction)
     └─ Error recovery for packet loss in IP transport
     └─ SMPTE 2022-1/5 implementations
     └─ 💡 Memory Aid: "FEC = Fix Errors Continuously"

  📶 **Pro-MPEG FEC**
     └─ Early FEC scheme in SMPTE 2022-1
     └─ Designed for MPEG-2 TS over IP
     └─ 💡 Memory Aid: "Pro-MPEG = Professional FEC"

  🔄 **Seamless Protection Switching** (SMPTE 2022-7)
     └─ Hitless failover using redundant RTP streams
     └─ Zero downtime switching
     └─ 💡 Memory Aid: "2022-7 = Two streams, zero interruption!"

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎵 AUDIO COMPRESSION & RELATED STANDARDS                                    │
└─────────────────────────────────────────────────────────────────────────────┘

🔴 **LEGACY AUDIO CODECS**

  🎭 **Dolby AC-3** (Dolby Digital)
     └─ Legacy lossy multichannel audio (A/52 standard)
     └─ DVD and broadcast workhorse
     └─ 💡 Memory Aid: "AC-3 = Audio Codec 3rd generation"

  ➕ **Dolby Digital Plus** (E-AC-3 / DD+)
     └─ Enhanced successor to AC-3
     └─ Higher bitrates + more channels
     └─ 💡 Memory Aid: "Plus = More channels, more quality"

🟢 **MODERN AUDIO COMPRESSION**

  🎼 **AAC** (Advanced Audio Coding)
     └─ MPEG-2/4 perceptual audio codec
     └─ Better than MP3, widely used in streaming
     └─ 💡 Memory Aid: "AAC = Always Above (MP3) Codec"

🟣 **IMMERSIVE & HDR AUDIO/VIDEO**

  🌌 **Dolby Atmos**
     └─ Object-based immersive 3D spatial audio
     └─ Beyond channel-based (5.1, 7.1)
     └─ 💡 Memory Aid: "Atmos = Audio Through My Own Space"

  🌈 **Dolby Vision**
     └─ Dynamic HDR metadata format
     └─ Often paired with HEVC for video
     └─ 💡 Memory Aid: "Vision = Video Immersive Stunning Image Output Now"

🟠 **AD INSERTION & SIGNALING**

  💰 **SCTE-35**
     └─ Standard for ad insertion cues/markers in MPEG-2 TS
     └─ Industry standard for dynamic ad insertion
     └─ 💡 Memory Aid: "SCTE-35 = Standard Cue To Enter ads (35 types)"

  📋 **POIS** (Placement Opportunity Information Service)
     └─ SCTE-130 interface for managing ad policies
     └─ Defines placement constraints
     └─ 💡 Memory Aid: "POIS = Policies Of Insertion Spots"

  📅 **ESNI** (Event Scheduling and Notification Interface)
     └─ SCTE-224 protocol for event signaling
     └─ Ad decision and scheduling
     └─ 💡 Memory Aid: "ESNI = Event Scheduling Notification Interface"

  🎛️ **ESAM** (Event Signaling and Management)
     └─ CableLabs API for SCTE-35 cue insertion
     └─ Controls ad workflow
     └─ 💡 Memory Aid: "ESAM = Event Signaling And Management"

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🌐 NETWORKING FUNDAMENTALS & DIAGNOSTICS                                    │
└─────────────────────────────────────────────────────────────────────────────┘

🔵 **CORE PROTOCOLS**

  🌍 **TCP/IP**
     └─ Core internet protocol suite
     └─ TCP = Reliable | UDP = Fast & Unreliable
     └─ 💡 Memory Aid: "TCP = Transmission Control Protocol (checks delivery)"
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎬 VIDEO OVER IP NETWORKS                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

🔴 **DELIVERY MODES**

  📡 **Multicast**
     └─ One-to-many IP delivery (efficient broadcast)
     └─ Uses IGMP for group management
     └─ 💡 Memory Aid: "Multicast = Multiple viewers, one stream"

  👤 **Unicast**
     └─ One-to-one IP delivery (point-to-point)
     └─ Common for contribution or ABR streaming
     └─ 💡 Memory Aid: "Unicast = Unique connection per viewer"

🟢 **NETWORK SEGMENTATION**

  🏷️ **VLAN** (Virtual LAN / IEEE 802.1Q)
     └─ Segmentation of broadcast domains
     └─ Traffic isolation and security
     └─ 💡 Memory Aid: "VLAN = Virtual Lanes for traffic"

🟣 **MODERN IP MEDIA STANDARDS**

  🎥 **SMPTE 2110**
     └─ Modern suite for uncompressed video/audio/ANC over IP
     └─ Successor to SMPTE 2022-6 in many workflows
     └─ 💡 Memory Aid: "2110 = 21st century, 10-Gig networking"

  🎼 **AES67**
     └─ Interoperability standard for audio-over-IP
     └─ Often integrated with SMPTE 2110
     └─ 💡 Memory Aid: "AES67 = Audio Engineering Society standard"

🔵 **TIMING & SYNCHRONIZATION**

  ⏱️ **PTP** (Precision Time Protocol / IEEE 1588)
     └─ High-precision timing/sync for IP media
     └─ Nanosecond-level accuracy
     └─ 💡 Memory Aid: "PTP = Perfectly Timed Packets"

🟠 **TRANSPORT & RELIABILITY**

  📦 **UDP** (User Datagram Protocol)
     └─ Connectionless transport (no handshake)
     └─ Underlying most real-time video protocols
     └─ 💡 Memory Aid: "UDP = Unreliable, Delivers Packets (fast!)"

  🔄 **ARQ** (Automatic Repeat reQuest)
     └─ Retransmission mechanism for reliability
     └─ Used in SRT and other resilient protocols
     └─ 💡 Memory Aid: "ARQ = Ask for Retransmission Quickly"

═══════════════════════════════════════════════════════════════════════════════
🎯 QUICK REFERENCE GUIDE
═══════════════════════════════════════════════════════════════════════════════

📊 **PROTOCOL SELECTION CHEATSHEET**

   Need low latency + reliability?  → 🔐 **SRT** or 🛡️ **Zixi**
   Broadcasting to many?            → 📡 **Multicast** with **IGMP**
   Adaptive streaming (OTT)?        → 🍎 **HLS** or 🌍 **DASH**
   Professional broadcast?          → 📡 **SMPTE 2022** or 🎥 **SMPTE 2110**
   Uncompressed over IP?            → 🎥 **SMPTE 2110** + ⏱️ **PTP**
   Need error correction?           → 🛡️ **FEC** or 🔄 **ARQ**
   Best compression for 4K?         → 🚀 **HEVC (H.265)**
   Ad insertion?                    → 💰 **SCTE-35** + 🎛️ **ESAM**
   Immersive audio?                 → 🌌 **Dolby Atmos**

═══════════════════════════════════════════════════════════════════════════════
🧠 MEMORY PALACE TECHNIQUE
═══════════════════════════════════════════════════════════════════════════════

**Visual Story for Protocols:**

1. 📺 You enter a **broadcast studio** (SMPTE territory)
2. 🔐 The door has **SRT locks** (Secure Reliable Transport)
3. 📡 A **satellite dish** multicasts signals (Multicast)
4. 🎥 Inside, **2110 cameras** shoot uncompressed (SMPTE 2110)
5. ⏱️ The wall clock shows **PTP precision** (nanosecond sync)
6. 🚀 A **rocket labeled 265** launches (HEVC for 4K+)
7. 🌌 The ceiling is **Atmos** (Dolby Atmos immersive)
8. 💰 Ad posters have **35mm film** markers (SCTE-35)
9. 🦈 A **shark tank** (Wireshark) shows all traffic
10. 🍎 An **apple on desk** streams content (HLS)

═══════════════════════════════════════════════════════════════════════════════

These keywords represent the **core technical vocabulary** for:
  ✅ Broadcast/video contribution engineering
  ✅ OTT streaming platforms
  ✅ IP-based production workflows
  ✅ Network diagnostics and debugging

🎓 **Pro Tip:** Review this cheatsheet before interviews or troubleshooting sessions!
     Each emoji serves as a mental anchor for faster recall.

═══════════════════════════════════════════════════════════════════════════════
📚 For detailed deep-dives, refer to individual protocol cheatsheets!
═══════════════════════════════════════════════════════════════════════════════
     └─ Layer 3 = IP-based routing (between subnets)
     └─ 💡 Memory Aid: "L2 = Local (MAC), L3 = Long-distance (IP)"

  🎚️ **Switches**
     └─ Network devices forwarding frames (L2) or packets (L3)
     └─ Supports VLAN and QoS
     └─ 💡 Memory Aid: "Switch = Smart packet director"

🟠 **DIAGNOSTIC & ANALYSIS TOOLS**

  🦈 **Wireshark**
     └─ Open-source GUI packet analyzer
     └─ Captures and inspects all network traffic
     └─ 💡 Memory Aid: "Wireshark = See every byte swimming by"

  🐚 **tcpdump**
     └─ Command-line packet sniffer
     └─ Lightweight filtering and capture
     └─ 💡 Memory Aid: "tcpdump = Terminal Capture dump"

🟣 **MULTICAST & QOS**

  📢 **IGMP** (Internet Group Management Protocol)
     └─ Manages multicast group membership (v2/v3)
     └─ Routers use it to track who wants multicast
     └─ 💡 Memory Aid: "IGMP = I'm Going Multicast Please"

  ⚡ **QoS** (Quality of Service)
     └─ Mechanisms to prioritize video traffic
     └─ DiffServ, priority queuing, traffic shaping
     └─ 💡 Memory Aid: "QoS = Queue optimal (video) Service"

### Video over IP Networks
- **Multicast** — One-to-many IP delivery (efficient for broadcast-style distribution, uses IGMP).
- **Unicast** — One-to-one IP delivery (point-to-point, common for contribution or ABR streaming).
- **VLAN** (Virtual LAN) — IEEE 802.1Q segmentation of broadcast domains for traffic isolation.
- **SMPTE 2110** — Modern suite for uncompressed video/audio/ANC over IP (successor to 2022-6 in many cases).
- **AES67** — Interoperability standard for audio-over-IP (often integrated with SMPTE 2110).
- **PTP** (Precision Time Protocol / IEEE 1588) — High-precision timing/sync for IP media networks.
- **UDP** — Connectionless transport layer protocol underlying most real-time video protocols.
- **ARQ** (Automatic Repeat reQuest) — Retransmission mechanism in protocols like SRT for reliability.

These keywords represent the core technical vocabulary for roles involving broadcast/video contribution, OTT streaming, IP-based production, and related engineering/debugging tasks. Let me know if you'd like this expanded into categories, acronyms expanded, or focused on a specific sub-area!