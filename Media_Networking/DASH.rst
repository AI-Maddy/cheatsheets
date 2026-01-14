═══════════════════════════════════════════════════════════════════════════════
🌍 DASH - Dynamic Adaptive Streaming over HTTP
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **DASH = Dynamic Adaptive Streaming HTTP** 🌍⚡

🧠 **Memory Palace**: Picture a WORLD MAP 🌍 with open-source roads (no tolls!) 
connecting video warehouses. Unlike Apple's proprietary HLS highway 🍎, DASH roads 
are MPEG STANDARD roads anyone can use. The manifest is an XML BLUEPRINT 📐 
(more detailed than HLS's simple text menu). YouTube's delivery trucks 🚚 use 
these roads with VP9/AV1 cargo (not just H.264).

Overview
--------
DASH (MPEG-DASH) is an open international standard for adaptive bitrate streaming (ISO/IEC 23009-1). Codec-agnostic and platform-independent.

Key Features
------------
- **Open Standard**: No licensing fees (unlike HLS initially)
- **Codec Agnostic**: Supports H.264, HEVC, VP9, AV1
- **XML Manifest**: MPD (Media Presentation Description)
- **Flexible**: Supports live and VOD
- **CDN-Friendly**: HTTP-based delivery

How DASH Works
--------------
::

    MPD Manifest (XML)
        |
        ├── AdaptationSet (Video)
        |    ├── Representation 1080p @ 5 Mbps
        |    ├── Representation 720p @ 3 Mbps
        |    └── Representation 480p @ 1 Mbps
        |
        └── AdaptationSet (Audio)
             ├── English AAC
             └── Spanish AAC

    Player: Parses MPD, adapts to network conditions

MPD Example (Simplified)
------------------------
::

    <?xml version="1.0"?>
    <MPD xmlns="urn:mpeg:dash:schema:mpd:2011">
      <Period>
        <AdaptationSet mimeType="video/mp4" codecs="avc1.4d401f">
          <Representation id="1080p" bandwidth="5000000" width="1920" height="1080">
            <BaseURL>1080p/</BaseURL>
            <SegmentTemplate media="$Number$.m4s" startNumber="1" duration="4"/>
          </Representation>
          <Representation id="720p" bandwidth="3000000" width="1280" height="720">
            <BaseURL>720p/</BaseURL>
            <SegmentTemplate media="$Number$.m4s" startNumber="1" duration="4"/>
          </Representation>
        </AdaptationSet>
      </Period>
    </MPD>

Common Use Cases
----------------
1. YouTube (uses DASH with VP9/AV1)
2. Netflix (uses both HLS and DASH)
3. Multi-platform OTT services
4. Live sports streaming
5. Educational video platforms

Encoding DASH
-------------
Using MP4Box (GPAC)::

    # Create fragmented MP4s
    ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -s 1920x1080 1080p.mp4
    ffmpeg -i input.mp4 -c:v libx264 -b:v 3M -s 1280x720 720p.mp4

    # Package for DASH
    MP4Box -dash 4000 -frag 4000 -rap \
      -segment-name segment_ \
      -out manifest.mpd \
      1080p.mp4 720p.mp4

Using Shaka Packager::

    packager \
      in=input.mp4,stream=video,output=1080p.mp4 \
      in=input.mp4,stream=video,output=720p.mp4 \
      --mpd_output manifest.mpd

DASH Profiles
-------------
**On-Demand Profile**
  - Pre-encoded VOD content
  - All segments available

**Live Profile**
  - Dynamic segment generation
  - Time-based availability

**Main Profile**
  - Most features enabled
  - SegmentBase, SegmentList, SegmentTemplate

DASH vs HLS
-----------
+--------------------+------------------+------------------+
| Feature            | DASH             | HLS              |
+====================+==================+==================+
| Standard Body      | MPEG/ISO         | Apple/IETF       |
| Manifest           | XML (MPD)        | M3U8 (text)      |
| Codec Support      | Any (H.264/VP9/  | H.264, HEVC      |
|                    | AV1/HEVC)        |                  |
| Browser Support    | Via library      | Native (Safari)  |
| Android            | Native           | Via library      |
| Licensing          | Royalty-free     | Royalty-free now |
+--------------------+------------------+------------------+

Segmentation Modes
------------------
1. **SegmentTemplate**: URL pattern with $Number$
2. **SegmentList**: Explicit list of segment URLs
3. **SegmentBase**: Single file with byte ranges

Latency
-------
- **Standard DASH**: 10-30 seconds
- **Low-Latency DASH**: 3-5 seconds (chunked transfer encoding)
- **Ultra-Low-Latency**: <2 seconds (LL-DASH extensions)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 MEMORY AIDS - Quick Recall                                              │
└─────────────────────────────────────────────────────────────────────────────┘

🎯 **MPD = Media Presentation Description (XML blueprint)**
🎯 **AdaptationSet = Group of similar streams (all video OR all audio)**
🎯 **Representation = One quality level (1080p, 720p, etc.)**
🎯 **DASH = YouTube's choice** (VP9/AV1 friendly)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📊 CODEC FLEXIBILITY - DASH vs HLS                                         │
└─────────────────────────────────────────────────────────────────────────────┘

DASH supports ANY codec::

    Video Codecs:
    ├── H.264/AVC    ✅ (Universal)
    ├── HEVC/H.265   ✅ (4K/HDR)
    ├── VP9          ✅ (YouTube, royalty-free)
    ├── AV1          ✅ (Next-gen, best compression)
    └── VP8          ✅ (Legacy WebM)

    Audio Codecs:
    ├── AAC          ✅
    ├── Opus         ✅ (Low-latency, VoIP)
    ├── Vorbis       ✅ (WebM)
    └── AC-3/E-AC-3  ✅ (Dolby)

    HLS Limited To:
    ├── H.264/HEVC   ✅
    ├── AAC          ✅
    └── VP9/AV1      ❌ (Not in standard)

💡 **YouTube uses DASH + VP9/AV1 for better compression = lower CDN costs!**

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MPD STRUCTURE - Visual Hierarchy                                        │
└─────────────────────────────────────────────────────────────────────────────┘

::

    MPD Manifest (manifest.mpd)
      |
      └── Period (e.g., Movie Part 1, Ad Break, Part 2)
           |
           ├── AdaptationSet (Video)
           │    ├── Representation: 4K @ 15 Mbps (codecs="avc1.640028")
           │    ├── Representation: 1080p @ 8 Mbps
           │    ├── Representation: 720p @ 5 Mbps
           │    └── Representation: 480p @ 2 Mbps
           │
           ├── AdaptationSet (Audio - English)
           │    ├── Representation: AAC 128 kbps
           │    └── Representation: AAC 64 kbps
           │
           ├── AdaptationSet (Audio - Spanish)
           │    └── Representation: AAC 128 kbps
           │
           └── AdaptationSet (Subtitles)
                ├── English WebVTT
                └── Spanish WebVTT

💡 **Key Difference**: DASH separates video/audio/subtitles into different 
    AdaptationSets (more flexible than HLS's variant streams)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📺 ABR LADDER EXAMPLE                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

YouTube-style DASH ladder (VP9 codec)::

    4K:     ████████████████████████████  12 Mbps  (VP9 50% better than H.264)
    1440p:  ████████████████████          9 Mbps
    1080p:  ████████████                  5 Mbps
    720p:   ████████                      3 Mbps
    480p:   █████                         1.5 Mbps
    360p:   ███                           0.8 Mbps
    240p:   █                             0.4 Mbps
            Auto                          0.1 Mbps (Audio-only)

🎯 **Segmentation Modes**::

    SegmentTemplate:  video_$Number$.m4s  ← Most common
    SegmentList:      [seg1.m4s, seg2.m4s, ...]  ← Explicit
    SegmentBase:      video.mp4 (byte ranges)  ← Single file

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔧 TROUBLESHOOTING                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: Player can't parse MPD
└─ 🔍 **Cause**: Invalid XML or missing required elements
   └─ **Solution**: Validate MPD with DASH-IF validator, check xmlns declaration

**Problem**: Video plays but no audio
└─ 🔍 **Cause**: Separate AdaptationSets not properly configured
   └─ **Solution**: Verify audio AdaptationSet has correct mimeType and codecs

**Problem**: Subtitle timing off by several seconds
└─ 🔍 **Cause**: presentationTimeOffset mismatch
   └─ **Solution**: Align subtitle timeline with video segments

**Problem**: Player stuck on one quality
└─ 🔍 **Cause**: ABR algorithm not switching
   └─ **Solution**: Check Representation bandwidth values are accurate

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUICK REFERENCE - Pro Tips                                               │
└─────────────────────────────────────────────────────────────────────────────┘

✅ **DO**:
  • Use SegmentTemplate for efficient URL patterns
  • Separate video/audio AdaptationSets (more flexibility)
  • Include multiple audio languages as separate AdaptationSets
  • Use Common Encryption (CENC) for multi-DRM
  • Set @maxSegmentDuration for better seeking

❌ **DON'T**:
  • Don't mix container formats (MP4 + WebM) in same Period
  • Don't forget @profiles attribute (indicates DASH profile)
  • Don't use overly complex MPD (keep it simple for debugging)
  • Don't skip @codecs parameter (players need it!)

🎯 **Player Libraries**::

    dash.js       ← Reference implementation (JavaScript)
    Shaka Player  ← Google's robust player
    ExoPlayer     ← Android native
    Video.js      ← Popular with DASH plugin

🌍 **Platform Support**::

    Android:      Native (ExoPlayer) ✅
    iOS:          Via Shaka/dash.js ⚠️ (no native support)
    Chrome:       Via JavaScript ✅
    Firefox:      Via JavaScript ✅
    Edge:         Via JavaScript ✅

📊 **Use DASH When**:
  ✅ Need codec flexibility (VP9, AV1)
  ✅ Multi-platform beyond iOS
  ✅ Avoid licensing (royalty-free)
  ✅ Complex multi-language requirements
  ✅ YouTube-like deployment

Important Notes
---------------
- Requires JavaScript player (dash.js, Shaka Player, Video.js)
- Supports multiple audio languages/tracks
- Supports subtitle tracks (WebVTT, TTML)
- DRM: Common Encryption (CENC) with Widevine, PlayReady, FairPlay
- Low-Latency DASH (LL-DASH) achieves 3-5 second latency
- More complex than HLS but more flexible for advanced use cases
- YouTube's VP9 DASH streams use ~40% less bandwidth than H.264
