═══════════════════════════════════════════════════════════════════════════════
📦 RTP - Real-time Transport Protocol 🎬
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **R**eal-**T**ime **P**ackets = Like a postal service for live video! 📬

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔵 OVERVIEW - The Universal Real-Time Delivery Protocol                    │
└─────────────────────────────────────────────────────────────────────────────┘

RTP (RFC 3550) is the **foundation protocol** for delivering audio and video over IP networks in real-time. Almost universally used in broadcast contribution, VoIP, video conferencing, and IPTV.

🎯 **Think of it as**: The "envelope" that carries your video/audio packets across the internet, with tracking numbers (sequence) and timestamps!

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⭐ KEY FEATURES - What Makes RTP Special                                    │
└─────────────────────────────────────────────────────────────────────────────┘

🚀 **Transport Layer**: Runs over UDP for low latency
   └─ 💡 Memory: "UDP = Under Delivery Protection" (no guarantees, but FAST!)

🔢 **Sequence Numbers**: Detects packet loss and reordering
   └─ 💡 Like tracking numbers on mail - you know if package #5 never arrived!

⏱️ **Timestamps**: Enables synchronization and jitter calculation
   └─ 💡 Clock inside every packet = lip-sync perfection

🎭 **Payload Type**: Identifies codec (H.264, HEVC, AAC, etc.)
   └─ 💡 "This box contains: H.264 video" label

🆔 **SSRC**: Unique source identifier for stream multiplexing
   └─ 💡 Like a radio station ID - "This is WKRP Camera 1"

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎬 COMMON USE CASES - Where You'll Find RTP                                │
└─────────────────────────────────────────────────────────────────────────────┘

1. 📡 **Live video contribution** (with SMPTE 2022)
   └─ Stadium → Broadcast center

2. 💬 **WebRTC real-time communications**
   └─ Zoom, Google Meet, Microsoft Teams

3. 📺 **IPTV multicast distribution**
   └─ Cable provider → Set-top boxes

4. 🎥 **Video conferencing systems**
   └─ Corporate meeting rooms

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📐 RTP HEADER STRUCTURE - The Anatomy                                      │
└─────────────────────────────────────────────────────────────────────────────┘

::

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |V=2|P|X|  CC   |M|     PT      |       sequence number  📫     |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                      timestamp  ⏰                             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         synchronization source (SSRC) identifier  🆔          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

**Field Meanings**:
  - V = Version (always 2)
  - P = Padding flag
  - X = Extension header present
  - CC = Contributing source count
  - M = Marker bit (frame boundaries)
  - PT = Payload Type (codec identifier)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔴 TROUBLESHOOTING - Common RTP Issues                                     │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: Video freezing/stuttering
└─ 🔍 **Check**: Sequence number gaps (packet loss)
   └─ **Solution**: Add FEC (SMPTE 2022-1) or use SRT/Zixi

**Problem**: Audio/video out of sync
└─ 🔍 **Check**: Timestamp drift
   └─ **Solution**: Verify clock synchronization (PTP/NTP)

**Problem**: No video received
└─ 🔍 **Check**: Firewall blocking UDP ports
   └─ **Solution**: Open ports or use SRT (NAT traversal)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE - Visual Story to Remember RTP                            │
└─────────────────────────────────────────────────────────────────────────────┘

Imagine a **📬 Post Office for Live Video**:

1. **📦 Packages** = RTP packets (each contains one video frame slice)
2. **🔢 Tracking numbers** = Sequence numbers (detect lost packages)
3. **⏰ Timestamp on box** = When this frame should play
4. **🆔 Return address** = SSRC (which camera sent this)
5. **🏃 Express delivery** = UDP (fast, but no guarantees)
6. **📋 Companion RTCP** = Quality reports ("5% packages lost!")

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUICK REFERENCE                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

📊 **Typical Configuration**::

    RTP Port:  5004 (even number)
    RTCP Port: 5005 (RTP + 1, odd number)
    Protocol:  UDP
    MTU:       1500 bytes (Ethernet standard)

🎯 **Pro Tips**:
  ✅ Always pair RTP with FEC or ARQ for reliability
  ✅ Monitor RTCP reports for quality metrics
  ✅ Use multicast for one-to-many distribution
  ✅ Set proper QoS/DSCP markings on switches

🚫 **Common Mistakes**:
  ❌ Using TCP instead of UDP (adds latency)
  ❌ Ignoring sequence number gaps
  ❌ Not monitoring RTCP feedback
  ❌ Forgetting firewall rules for UDP

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📚 IMPORTANT NOTES                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

⚠️ **RTP alone does NOT provide reliability** (use with FEC or ARQ)
📊 Typically paired with **RTCP** for quality monitoring
🔢 **Port convention**: RTP on even port, RTCP on odd (e.g., 5004/5005)
🌐 Defined in **RFC 3550** (2003, successor to RFC 1889)
🎬 Used in **99% of live video** workflows worldwide!
