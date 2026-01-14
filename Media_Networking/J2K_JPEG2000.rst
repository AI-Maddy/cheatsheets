═══════════════════════════════════════════════════════════════════════════════
🌊 JPEG 2000 (J2K) - Wavelet-Based Professional Codec
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **J2K = Just 2 Keyframes (every frame is a keyframe!)** 🎬🔑

🧠 **Memory Palace**: Imagine a HOLLYWOOD CINEMA 🎭 where every single film frame is a 
MASTER COPY 🖼️ (not compressed from previous frames). Ocean WAVES 🌊 represent the 
wavelet compression. Each frame is PRISTINE but needs a BIG TRUCK 🚚 to deliver (high 
bitrate). Ultra-low delay = projectionist can switch frames INSTANTLY!

Overview
--------
JPEG 2000 is a wavelet-based codec offering high quality at low latency. Used in digital cinema, broadcast contribution, and medical imaging.

Key Features
------------
- **Wavelet Compression**: Not DCT-based like most codecs
- **Intra-Frame Only**: Every frame independently coded
- **Low Latency**: <1 frame delay
- **Scalability**: Quality/resolution can be extracted from bitstream
- **Error Resilience**: Graceful degradation

Common Use Cases
----------------
1. **Digital Cinema** (DCI specification)
   - 2K/4K movie distribution to theaters
   - 250 Mbps for 4K content

2. **Broadcast Contribution**
   - Live sports remote production
   - SMPTE 2022-6 over IP

3. **Archive/Preservation**
   - Lossless or near-lossless storage
   - National archives, film restoration

4. **Medical Imaging**
   - DICOM standard
   - X-rays, MRI scans

Typical Bitrates
----------------
+----------------+-------------------+
| Application    | Bitrate           |
+================+===================+
| DCI 2K Cinema  | 125 Mbps          |
| DCI 4K Cinema  | 250 Mbps          |
| Broadcast HD   | 50-100 Mbps       |
| Contribution 4K| 200-400 Mbps      |
+----------------+-------------------+

J2K vs H.264/HEVC
-----------------
+--------------------+------------------+------------------+
| Feature            | JPEG 2000        | H.264/HEVC       |
+====================+==================+==================+
| Compression Type   | Intra-frame only | Inter-frame      |
| Latency            | Ultra-low (<1ms) | Higher (GOP)     |
| Compression Ratio  | 10:1 - 20:1      | 50:1 - 200:1     |
| Editing            | Frame-accurate   | GOP boundaries   |
| Quality            | Very high        | Good             |
| Computational Cost | Moderate         | High (HEVC)      |
+--------------------+------------------+------------------+

Profiles
--------
**DCI Profile**
  - Digital cinema mastering
  - XYZ color space
  - 12-bit depth

**Broadcast Profile**
  - YCbCr 4:2:2 or 4:4:4
  - 10-bit depth
  - SMPTE standards

Encoding Example
----------------
FFmpeg with OpenJPEG::

    ffmpeg -i input.mov -c:v libopenjpeg \
      -format j2k \
      -profile:v cinema2k \
      -b:v 125M \
      output.mxf

Advantages
----------
- **Low Latency**: Ideal for live production
- **Frame Accurate**: Every frame is a keyframe
- **High Quality**: Visually lossless at moderate bitrates
- **Scalable**: Resolution/quality layers in bitstream

Disadvantages
-------------
- **High Bitrate**: 10-20x more than H.264 for same resolution
- **Not Consumer-Friendly**: Limited device support
- **Expensive**: Requires dedicated hardware encoders/decoders
- **Not Suitable for Internet**: Too much bandwidth

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 MEMORY AIDS - Wavelet vs DCT                                            │
└─────────────────────────────────────────────────────────────────────────────┘

🎯 **Wavelet = WAVE-let = Ocean waves 🌊 of compression**
🎯 **Intra-only = Every frame is an I-frame = Independent!**
🎯 **DCI = Digital Cinema = 250 Mbps for 4K**
🎯 **J2K vs JPEG**: Completely different! J2K is professional, JPEG is consumer

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📊 BITRATE COMPARISON - Quality vs File Size                               │
└─────────────────────────────────────────────────────────────────────────────┘

4K Professional Content (visually lossless):

    J2K:     ████████████████████████████████  250 Mbps  (Cinema)
    HEVC:    ████                              15 Mbps   (Streaming)
    H.264:   ████████                          30 Mbps   (Broadcast)
    
    💡 J2K trades bandwidth for ZERO latency & perfect frames!

HD Contribution Feed:

    J2K:     ████████████████  100 Mbps  (Broadcast truck)
    HEVC:    ██                8 Mbps    (Not suitable - latency!)
    MPEG-2:  ████████          50 Mbps   (I-frame only)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎬 DIGITAL CINEMA WORKFLOW                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Post-Production → Theater Delivery::

    [Master File]
         |
         v
    [J2K Encode: 250 Mbps, XYZ color, 12-bit]
         |
         v
    [DCP Package: MXF container + XML metadata]
         |
         v
    [Encrypted with KDM keys]
         |
         v
    [Delivered to Theater via hard drive]
         |
         v
    [Projection: 2K/4K Digital Projector]

🔑 Key Specs:
  • 2K: 2048×1080 @ 24fps = 125 Mbps
  • 4K: 4096×2160 @ 24fps = 250 Mbps
  • XYZ color space (not RGB!)
  • 12-bit color depth
  • MXF container format

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔧 TROUBLESHOOTING                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: Extremely large file sizes
└─ 🔍 **Cause**: Every frame is keyframe = high bitrate
   └─ **Solution**: This is normal for J2K! Use for contribution, not distribution

**Problem**: Can't play J2K files on consumer devices
└─ 🔍 **Cause**: Consumer devices lack J2K decoder
   └─ **Solution**: Transcode to H.264/HEVC for delivery, keep J2K for mastering

**Problem**: Latency still too high for contribution
└─ 🔍 **Cause**: J2K is ~1 frame delay
   └─ **Solution**: Try JPEG-XS (even lower latency, <1ms)

**Problem**: Wrong color space (looks washed out)
└─ 🔍 **Cause**: DCI uses XYZ, not YCbCr/RGB
   └─ **Solution**: Verify color space in encoding settings

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ QUICK REFERENCE - Use Cases                                              │
└─────────────────────────────────────────────────────────────────────────────┘

✅ **USE J2K When**:
  • Digital cinema mastering (DCP)
  • Live sports contribution (remote production)
  • Medical imaging (lossless critical)
  • Archive preservation (frame accuracy)
  • Low-latency live production
  • SMPTE 2022-6 over IP workflows

❌ **DON'T USE When**:
  • Internet streaming (too much bandwidth)
  • Consumer distribution
  • Storage space limited
  • Budget constrained (hardware expensive)

🎯 **Application Matrix**::

    Cinema (DCP)        → J2K @ 250 Mbps ✅
    Contribution Feed   → J2K @ 100 Mbps ✅
    Streaming (4K)      → HEVC @ 15 Mbps ❌ (use HEVC)
    VOD Platform        → H.264 @ 8 Mbps ❌ (use H.264)
    Archive Master      → J2K lossless ✅

📊 **Latency Comparison**:
  • J2K: <1 frame (~40ms @ 24fps)
  • JPEG-XS: <1ms (emerging standard)
  • H.264: 100-500ms (GOP delay)
  • HEVC: 200-1000ms (larger GOP)

Important Notes
---------------
- Used in SMPTE 2022-6 for IP contribution
- Being challenged by JPEG-XS (even lower latency, lighter compression)
- Still standard for digital cinema (DCP format)
- Not related to legacy JPEG image format
- Every frame = keyframe = perfect for frame-accurate editing
- Broadcast trucks use J2K for remote production (SMPTE 2022-6)
- Medical imaging relies on lossless J2K for diagnosis
