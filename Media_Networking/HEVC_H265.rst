═══════════════════════════════════════════════════════════════════════════════
🚀 HEVC / H.265 - High Efficiency Video Coding
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **H.265 = Half the size, 2x the pixels!** 🎬✨

🧠 **Memory Palace**: Picture a SUPER-EFFICIENT WAREHOUSE 🏭 where everything is 
compressed TWICE as tight as the old H.264 warehouse. 4K boxes 📦 fit where 1080p 
used to be! The workers (encoders) move SLOWER but pack things WAY better.

Overview
--------
HEVC is the successor to H.264, offering ~50% better compression. Essential for 4K/8K streaming and HDR content.

Key Features
------------
- **Larger Blocks**: Up to 64x64 CTUs (Coding Tree Units)
- **Better Compression**: Half the bitrate of H.264 at same quality
- **4K/8K Ready**: Supports up to 8192x4320 resolution
- **HDR Support**: 10-bit color depth, wide color gamut

Profiles
--------
**Main Profile** (8-bit)
  - HD and 4K streaming
  - Most common deployment

**Main 10 Profile** (10-bit)
  - HDR content (HDR10, Dolby Vision)
  - Professional workflows

**Main Still Picture Profile**
  - HEIF image format
  - iPhone photos

Common Bitrates
---------------
+----------------+-------------------+-------------------+
| Resolution     | H.264 Bitrate     | HEVC Bitrate      |
+================+===================+===================+
| 1080p          | 8 Mbps            | 4 Mbps            |
| 4K (UHD)       | 25 Mbps           | 12-15 Mbps        |
| 8K             | 100+ Mbps         | 50-70 Mbps        |
+----------------+-------------------+-------------------+

Common Use Cases
----------------
1. 4K streaming (Netflix, Apple TV+)
2. 4K Blu-ray (UHD Blu-ray)
3. HDR video production
4. Mobile video (lower bandwidth)
5. Broadcast ATSC 3.0

Encoding Example
----------------
FFmpeg with HEVC::

    ffmpeg -i input.mp4 -c:v libx265 \
      -preset medium \
      -crf 28 \
      -pix_fmt yuv420p10le \
      -tag:v hvc1 \
      output.mp4

**Parameters**:
- **crf**: 28 (equivalent to H.264 crf 23)
- **pix_fmt**: yuv420p10le for 10-bit HDR
- **tag:v hvc1**: Apple compatibility

HEVC vs H.264
-------------
+--------------------+------------------+------------------+
| Feature            | H.264            | HEVC             |
+====================+==================+==================+
| Compression        | Baseline         | 2x better        |
| Max Resolution     | 4K               | 8K               |
| HDR Support        | Limited          | Native           |
| Encoding Speed     | Fast             | Slower (3-5x)    |
| Device Support     | Universal        | Growing          |
| Licensing          | Complex          | Very complex     |
+--------------------+------------------+------------------+

Challenges
----------
- **Patent Complexity**: Multiple patent pools
- **Encoding Cost**: 3-5x slower than H.264
- **Hardware Decode**: Requires modern devices (2016+)
- **Browser Support**: Limited (Safari yes, Chrome conditional)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 MEMORY AIDS - Quick Recall                                              │
└─────────────────────────────────────────────────────────────────────────────┘

🎯 **265 = 2x efficiency for 6K+ and 5K screens!**
🎯 **HEVC = Half Everything Via Compression**
🎯 **CTU Size**: 64x64 (think: "64 = 4K-friendly blocks")
🎯 **Main 10**: 10-bit = HDR essentials

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 COMPRESSION LADDER - Bitrate Visualization                              │
└─────────────────────────────────────────────────────────────────────────────┘

4K HDR Content (same quality):

    H.264:  ████████████████████████  25 Mbps
    HEVC:   ████████████              12 Mbps  ← 50% savings!
    AV1:    ████████                  8 Mbps   ← Future

1080p Content:

    H.264:  ████████  8 Mbps
    HEVC:   ████      4 Mbps  ← Same quality, half size

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔧 TROUBLESHOOTING                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: Video won't play on older devices
└─ 🔍 **Cause**: Device lacks HEVC hardware decoder
   └─ **Solution**: Re-encode in H.264 or upgrade device (2016+ phones/TVs)

**Problem**: Encoding extremely slow
└─ 🔍 **Cause**: HEVC is 3-5x more complex than H.264
   └─ **Solution**: Use hardware encoder (NVENC, QuickSync, VCE) or faster preset

**Problem**: Chrome won't play HEVC
└─ 🔍 **Cause**: Google doesn't support HEVC (patent issues)
   └─ **Solution**: Use Safari, Edge, or re-encode to VP9/AV1

**Problem**: Blocking artifacts in dark scenes
└─ 🔍 **Cause**: 8-bit encoding with HDR content
   └─ **Solution**: Use Main 10 Profile (10-bit) with yuv420p10le

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUICK REFERENCE - Pro Tips & Common Mistakes                            │
└─────────────────────────────────────────────────────────────────────────────┘

✅ **DO**:
  • Use Main 10 Profile for HDR content
  • Set CRF 28 (equivalent to H.264 CRF 23)
  • Use hardware encoding for real-time
  • Test playback on target devices first
  • Use hvc1 tag for Apple compatibility

❌ **DON'T**:
  • Don't use veryslow preset for live encoding
  • Don't assume universal browser support
  • Don't use 8-bit for HDR (causes banding)
  • Don't forget patent licensing implications

🎯 **Profile Selection**::

    SDR 1080p → Main Profile (8-bit)
    4K HDR    → Main 10 Profile (10-bit)
    iPhone    → Main 10 + hvc1 tag
    Cinema    → Main 10 + 4:2:2 chroma

📊 **Device Support Timeline**:
  2015: iPhone 6s (A9 chip)
  2016: Most flagship phones
  2017: Mid-range phones, smart TVs
  2018+: Widespread
  Browsers: Safari ✅, Edge ✅, Chrome ❌ (platform-dependent)

Important Notes
---------------
- Also known as H.265 or MPEG-H Part 2
- Successor: VVC (H.266) in development
- Dolby Vision typically uses HEVC Main 10 Profile
- Patent situation complex (multiple pools: HEVC Advance, MPEG LA)
- 50% bitrate savings = 50% CDN cost savings at scale
