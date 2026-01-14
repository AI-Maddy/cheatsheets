═══════════════════════════════════════════════════════════════════════════════
🍎 HLS - HTTP Live Streaming (Apple)
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **HLS = HTTP Lives Streaming!** 📱🌍

🧠 **Memory Palace**: Picture an APPLE STORE 🍎 where videos are chopped into small 
BOXES 📦 (segments) on shelves. Customers grab boxes based on their internet speed 
(slow WiFi = small boxes 480p, fast 5G = big 4K boxes). Each shelf has a MENU 📋 
(M3U8 playlist) listing what's available. Everything ships via regular mail trucks 
🚚 (HTTP) so it gets through any gate (firewall).

Overview
--------
HLS is Apple's adaptive bitrate streaming protocol, now an IETF standard (RFC 8216). Dominant protocol for mobile and web video delivery.

Key Features
------------
- **Adaptive Bitrate**: Automatically adjusts quality based on bandwidth
- **HTTP-Based**: Works through firewalls, uses CDNs
- **Segmented**: Video split into 2-10 second chunks
- **M3U8 Playlist**: Text-based manifest format
- **Universal Support**: iOS, Android, web browsers

How HLS Works
-------------
::

    Origin Server
        |
        ├── Master Playlist (master.m3u8)
        |    ├── 1080p variant (bitrate 5 Mbps)
        |    ├── 720p variant (bitrate 3 Mbps)
        |    └── 480p variant (bitrate 1 Mbps)
        |
        └── Media Playlists + Segments
             ├── 1080p.m3u8 → seg_001.ts, seg_002.ts...
             ├── 720p.m3u8  → seg_001.ts, seg_002.ts...
             └── 480p.m3u8  → seg_001.ts, seg_002.ts...

    Player: Monitors bandwidth, switches between variants

Master Playlist Example
-----------------------
::

    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
    1080p.m3u8
    #EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720
    720p.m3u8
    #EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=854x480
    480p.m3u8

Media Playlist Example
----------------------
::

    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-TARGETDURATION:10
    #EXT-X-MEDIA-SEQUENCE:0
    #EXTINF:10.0,
    segment_000.ts
    #EXTINF:10.0,
    segment_001.ts
    #EXT-X-ENDLIST

Common Use Cases
----------------
1. Mobile video apps (YouTube, Netflix on iOS)
2. Live streaming (sports, concerts)
3. VOD platforms (on-demand content)
4. In-browser video players

Encoding HLS
------------
FFmpeg HLS generation::

    ffmpeg -i input.mp4 \
      -c:v libx264 -c:a aac \
      -hls_time 6 \
      -hls_playlist_type vod \
      -hls_segment_filename 'segment_%03d.ts' \
      output.m3u8

**Multi-bitrate generation**::

    ffmpeg -i input.mp4 \
      -filter_complex "[0:v]split=3[v1][v2][v3]; \
        [v1]scale=1920:1080[v1out]; \
        [v2]scale=1280:720[v2out]; \
        [v3]scale=854:480[v3out]" \
      -map "[v1out]" -b:v:0 5M -map "[v2out]" -b:v:1 3M -map "[v3out]" -b:v:2 1M \
      -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:0" \
      -master_pl_name master.m3u8 \
      -f hls -hls_time 6 stream_%v.m3u8

HLS Versions
------------
- **Version 3**: Most common, TS segments
- **Version 7**: fMP4 segments (fragmented MP4)
- **Low-Latency HLS**: Sub-2 second latency (Apple 2019+)

HLS vs DASH
-----------
+--------------------+------------------+------------------+
| Feature            | HLS              | DASH             |
+====================+==================+==================+
| Origin             | Apple (2009)     | MPEG (2012)      |
| Manifest Format    | M3U8 (text)      | XML (MPD)        |
| Segment Format     | TS or fMP4       | fMP4, WebM       |
| iOS Support        | Native           | Requires library |
| Android Support    | Native           | Native           |
+--------------------+------------------+------------------+

Latency
-------
- **Standard HLS**: 20-30 seconds
- **Low-Latency HLS**: 2-5 seconds
- **Live with chunked transfer**: 6-10 seconds

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 MEMORY AIDS - Quick Recall                                              │
└─────────────────────────────────────────────────────────────────────────────┘

🎯 **M3U8 = M3U + 8 (UTF-8 encoding)**
🎯 **TS = Transport Stream (188-byte MPEG-2 packets)**
🎯 **#EXTINF = EXTended INFormation (segment duration)**
🎯 **Apple = Apples come in segments (like orange slices!)** 🍊

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📊 ABR LADDER - Adaptive Bitrate Visualization                             │
└─────────────────────────────────────────────────────────────────────────────┘

Typical HLS bitrate ladder for streaming service::

    4K:     ████████████████████████████████  15 Mbps  (3840x2160)
    1080p:  ████████████████████              8 Mbps   (1920x1080)
    720p:   ████████████                      5 Mbps   (1280x720)
    540p:   ████████                          3 Mbps   (960x540)
    360p:   █████                             1.5 Mbps (640x360)
    240p:   ██                                0.8 Mbps (426x240)
            ↑
    Player switches based on measured bandwidth!

📱 **Mobile Scenario**::

    WiFi (10 Mbps)  → Player selects 720p ✅
    Move to car     → Drops to 4G (3 Mbps) → Switches to 540p 🔄
    Tunnel          → Poor signal → Drops to 360p ⚠️
    Back to WiFi    → Ramps up to 1080p 📈

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MANIFEST STRUCTURE - Visual Breakdown                                   │
└─────────────────────────────────────────────────────────────────────────────┘

::

    master.m3u8 ("Menu of Menus")
         |
         ├── #EXT-X-STREAM-INF: BANDWIDTH=8000000, RESOLUTION=1920x1080
         │   └─> 1080p.m3u8 (Media Playlist)
         │        ├── segment_000.ts (10 seconds)
         │        ├── segment_001.ts (10 seconds)
         │        └── segment_002.ts (10 seconds)
         │
         ├── #EXT-X-STREAM-INF: BANDWIDTH=5000000, RESOLUTION=1280x720
         │   └─> 720p.m3u8
         │
         └── #EXT-X-STREAM-INF: BANDWIDTH=1500000, RESOLUTION=640x360
             └─> 360p.m3u8

💡 **Think**: Master playlist = Restaurant menu, Media playlists = Recipe cards

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔧 TROUBLESHOOTING                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: Frequent buffering despite good bandwidth
└─ 🔍 **Cause**: Segment duration too long (30s segments)
   └─ **Solution**: Use 4-6 second segments for better adaptation

**Problem**: Initial loading delay (20-30 seconds)
└─ 🔍 **Cause**: Standard HLS playlist polling
   └─ **Solution**: Use Low-Latency HLS (LL-HLS) or reduce target duration

**Problem**: Video won't play on Android
└─ 🔍 **Cause**: Non-standard M3U8 format or fMP4 without browser support
   └─ **Solution**: Use TS segments (universal) or ensure fMP4 compatibility

**Problem**: Quality keeps dropping despite fast WiFi
└─ 🔍 **Cause**: CDN throttling or player bandwidth estimation issues
   └─ **Solution**: Check CDN analytics, verify player ABR algorithm

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUICK REFERENCE - Pro Tips                                               │
└─────────────────────────────────────────────────────────────────────────────┘

✅ **DO**:
  • Use 4-6 second segments (balance latency vs overhead)
  • Include multiple bitrate rungs (6-8 variants)
  • Test on real mobile networks, not just WiFi
  • Use fMP4 for modern workflows (easier DRM)
  • Set #EXT-X-VERSION correctly (3 for TS, 7 for fMP4)

❌ **DON'T**:
  • Don't use segments >10s (poor adaptation)
  • Don't have bitrate gaps >2x between rungs
  • Don't forget audio-only variant for background playback
  • Don't skip #EXT-X-TARGETDURATION (causes player errors)

🎯 **Segment Duration Trade-offs**::

    2s segments:  Low latency ✅  More HTTP overhead ❌  Frequent switching
    6s segments:  Balanced ✅      Good for most use cases
    10s segments: Less overhead ✅  Higher latency ❌     Slower adaptation

📱 **Platform Compatibility**::

    iOS/Safari:   Native support ✅ (no library needed)
    Android:      Native support ✅ (ExoPlayer)
    Chrome:       Via hls.js ⚠️
    Firefox:      Via hls.js ⚠️
    Edge:         Native support ✅

Important Notes
---------------
- Segment duration trade-off: shorter = lower latency, more overhead
- Requires CDN for scalability
- DRM: FairPlay (Apple), Widevine, PlayReady support
- Can use AES-128 encryption for content protection
- Low-Latency HLS (LL-HLS) achieves 2-5 second latency vs 20-30s standard
- fMP4 segments (v7) enable Common Encryption for multi-DRM
