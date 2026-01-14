═══════════════════════════════════════════════════════════════════════════════
🦖 MPEG-2 / H.262 - Legacy Broadcast Video Codec
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **MPEG-2 = 2000s Legacy!** (Like a reliable old truck 🚚)

🧠 **Memory Palace**: Imagine a 1990s BROADCAST STATION 📺 with OLD but RELIABLE 
equipment. The VHS tapes have been replaced with DVDs 💿, and huge satellite dishes 📡 
beam this "good enough" quality everywhere. Everything uses 188-byte packets (like 
standard mail envelopes 📬) that travel reliably but inefficiently.

Overview
--------
MPEG-2 is the legacy standard for DVD, broadcast television, and early digital video. Still deployed in many broadcast workflows despite being 30+ years old.

Key Features
------------
- **DCT-Based**: Discrete Cosine Transform compression
- **I/P/B Frames**: Intra, Predicted, Bidirectional
- **Transport Stream**: MPEG-2 TS container format
- **Simple Profiles**: Main Profile @ Main Level most common

Common Bitrates
---------------
+----------------+-------------------+
| Format         | Typical Bitrate   |
+================+===================+
| DVD            | 4-8 Mbps          |
| SDTV Broadcast | 3-6 Mbps          |
| HDTV Broadcast | 15-20 Mbps        |
| Contribution   | 50-100 Mbps (I-frame only) |
+----------------+-------------------+

Common Use Cases
----------------
1. Legacy broadcast television (ATSC 1.0, DVB)
2. DVD video
3. Satellite distribution
4. Cable television
5. Contribution feeds (MPEG-2 @ 50 Mbps)

MPEG-2 Transport Stream
-----------------------
Packet structure::

    188-byte packets
    ├── 4-byte header (sync byte 0x47)
    └── 184-byte payload

**Used in**:
- Broadcast TS files (.ts)
- HLS segments
- SMPTE 2022 over IP

Encoding Example
----------------
FFmpeg MPEG-2 encoding::

    ffmpeg -i input.mp4 -c:v mpeg2video \
      -b:v 15M \
      -maxrate 18M \
      -bufsize 2M \
      -f mpegts output.ts

Profiles & Levels
-----------------
**Simple Profile**
  - No B-frames
  - Low complexity

**Main Profile** (Most common)
  - I/P/B frames
  - SD and HD support

**4:2:2 Profile**
  - Professional production
  - Higher chroma resolution

MPEG-2 vs Modern Codecs
-----------------------
- **vs H.264**: 2x worse compression (needs 2x bitrate)
- **vs HEVC**: 4x worse compression
- **Advantage**: Ultra-low latency, simple decode

Why Still Used?
---------------
1. **Legacy Infrastructure**: Billions of dollars invested
2. **Low Latency**: Simple decoding = minimal delay
3. **Reliable**: Well-understood, battle-tested
4. **Contribution**: High bitrate I-frame for editing
5. **Broadcast Standards**: ATSC 1.0, DVB-T/S still mandate it

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 MEMORY AIDS - Transport Stream                                          │
└─────────────────────────────────────────────────────────────────────────────┘

🎯 **188 bytes = 1-8-8 like old TV channels 1, 8, and 8!**
🎯 **Sync byte 0x47**: Think "Channel 47" to sync your TV 📺
🎯 **TS = Television Standard**: Transport Stream for TV
🎯 **I/P/B = I Put Bi-directional**: Frame types

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📊 EFFICIENCY COMPARISON - Why MPEG-2 Is Inefficient                       │
└─────────────────────────────────────────────────────────────────────────────┘

720p HD Content (same visual quality):

    MPEG-2:  ████████████████████  15 Mbps  (Broadcast TV)
    H.264:   ████████              6 Mbps   (Streaming)
    HEVC:    ████                  3 Mbps   (4K streaming)
    AV1:     ██                    2 Mbps   (Future)

DVD Quality (480p):

    MPEG-2:  ████████  8 Mbps  (DVD standard)
    H.264:   ███       3 Mbps  (Modern equivalent)

💡 **Insight**: MPEG-2 needs 2-4x more bandwidth than modern codecs!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔧 TROUBLESHOOTING                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: Blocky artifacts in fast motion
└─ 🔍 **Cause**: Bitrate too low for MPEG-2's poor compression
   └─ **Solution**: Increase bitrate to 15-20 Mbps for HD or switch to H.264

**Problem**: Can't find sync bytes in transport stream
└─ 🔍 **Cause**: Corrupted TS file or wrong container format
   └─ **Solution**: Search for 0x47 every 188 bytes, use ffprobe to validate

**Problem**: Player shows only I-frames (slideshow effect)
└─ 🔍 **Cause**: Missing P/B frames or decode errors
   └─ **Solution**: Check GOP structure, validate stream integrity

**Problem**: Large file sizes compared to modern formats
└─ 🔍 **Cause**: MPEG-2's inefficient compression
   └─ **Solution**: Transcode to H.264 (50% savings) or HEVC (75% savings)

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUICK REFERENCE - When to Use MPEG-2                                     │
└─────────────────────────────────────────────────────────────────────────────┘

✅ **USE MPEG-2 When**:
  • Legacy broadcast requirement (ATSC 1.0, DVB-T)
  • DVD authoring
  • Ultra-low latency needed (I-frame only)
  • Contribution feeds (50-100 Mbps I-frame)
  • Target devices can't decode H.264

❌ **DON'T USE When**:
  • Internet streaming (use H.264/HEVC)
  • Storage space limited
  • Bandwidth constrained
  • Modern devices available

📺 **GOP Structure Example**::

    I  B  B  P  B  B  P  B  B  P  B  B  I
    ↑           ↑           ↑           ↑
    Keyframe    Predicted   Predicted   Keyframe
    
    Typical: GOP 12-15 (0.5 seconds @ 30fps)

🎯 **Transport Stream Packet**::

    [0x47][ 3-byte header ][ 184-byte payload ]
       ↑
    Sync byte (always 0x47 = ASCII 'G')

Important Notes
---------------
- Being phased out by ATSC 3.0 (uses HEVC)
- Still dominant in cable television
- Transport stream format lives on with newer codecs
- Patents expired (royalty-free)
