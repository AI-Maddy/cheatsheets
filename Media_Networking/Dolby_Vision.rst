═══════════════════════════════════════════════════════════════════════════════
🌈 Dolby Vision - Dynamic HDR Metadata Format
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
Dolby Vision is a proprietary HDR (High Dynamic Range) format that provides dynamic, scene-by-scene or frame-by-frame metadata to optimize picture quality. It offers superior brightness, contrast, and color accuracy compared to static HDR formats.

Key Features
------------
- **Dynamic Metadata**: Adjusts per scene or frame
- **12-bit Color Depth**: 68 billion colors (vs 1 billion in 10-bit)
- **10,000 nits Peak Brightness**: Future-proof for bright displays
- **Wide Color Gamut**: Rec. 2020 color space
- **Backward Compatible**: Includes SDR base layer

How It Works
------------
::

    Dolby Vision Content:
    ├─ Base Layer (SDR compatible - HEVC)
    ├─ Enhancement Layer (additional HDR data)
    └─ Metadata (scene-by-scene optimization)
    
    Display:
    1. Reads metadata
    2. Analyzes display capabilities
    3. Maps content to display's actual range
    4. Optimizes brightness/color per scene

Dolby Vision Profiles
---------------------
**Profile 5** (Streaming)
  - HEVC Main 10
  - Used by Netflix, Apple TV+, Disney+
  - Most common for OTT

**Profile 7** (OTT Streaming)
  - Single-layer HEVC
  - Better compatibility
  - Growing adoption

**Profile 8** (Broadcast/Blu-ray)
  - Dual-layer (base + enhancement)
  - Ultra HD Blu-ray standard
  - Professional mastering

Dolby Vision vs HDR10
---------------------
+----------------------+------------------+------------------+
| Feature              | Dolby Vision     | HDR10            |
+======================+==================+==================+
| Metadata             | Dynamic (scene)  | Static (content) |
| Color Depth          | 12-bit           | 10-bit           |
| Peak Brightness      | 10,000 nits      | 4,000 nits       |
| Licensing            | Proprietary fees | Royalty-free     |
| Adoption             | Premium content  | Widespread       |
| Quality              | Superior         | Good             |
+----------------------+------------------+------------------+

Common Use Cases
----------------
1. **Streaming Services**: Netflix, Apple TV+, Disney+
2. **Ultra HD Blu-ray**: Physical media releases
3. **Cinema**: Theatrical presentation (Dolby Cinema)
4. **Gaming**: Xbox Series X/S, PlayStation 5
5. **Mobile**: High-end smartphones

💡 Memory Aid: **Dolby Vision = Dynamic Vision = Adapts every scene!** 🎬🌈

🧠 Memory Palace: Picture a **SMART CHAMELEON** 🦎 that changes colors scene-by-scene.
A sunset scene? Chameleon goes BRIGHT ORANGE 🌅. Dark cave? Deep blacks 🌑. 
Unlike a regular lizard (HDR10 🦎 set once, stays same), this smart chameleon 
(Dolby Vision) reads scene instructions and adapts continuously = PERFECT colors always!

⚡ Dolby Vision HDR Processing Pipeline
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Step 1: Content Mastering (Studio Workflow)                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  🎬 Director & Colorist in Dolby Vision Grading Suite                        │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  Reference Monitor: 4000 nit peak, 12-bit color, Rec.2020 gamut      │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │  🌅 Scene 1: Sunset (bright, warm colors)                       │ │   │
│  │  │  📊 Metadata: Peak brightness = 800 nits, avg = 200 nits       │ │   │
│  │  │                                                                 │ │   │
│  │  │  🌑 Scene 2: Dark cave (deep blacks, low brightness)           │ │   │
│  │  │  📊 Metadata: Peak brightness = 50 nits, avg = 10 nits         │ │   │
│  │  │                                                                 │ │   │
│  │  │  💥 Scene 3: Explosion (HDR highlights, high contrast)         │ │   │
│  │  │  📊 Metadata: Peak brightness = 2000 nits, avg = 400 nits      │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  │  Colorist creates DYNAMIC METADATA for each scene or frame:          │   │
│  │  • MaxCLL (Max Content Light Level in nits)                          │   │
│  │  • MaxFALL (Max Frame Average Light Level)                           │   │
│  │  • Color grading adjustments (hue, saturation, tone curves)          │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
         ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│ Step 2: Encoding & Packaging                                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  📦 Dolby Vision Encoder Creates Multi-Layer Stream:                         │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  Layer 1: BASE LAYER (SDR - 8-bit Rec.709)                           │   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                          │   │
│  │  Compatible with old TVs (HEVC Main Profile)                         │   │
│  │                                                                       │   │
│  │  Layer 2: ENHANCEMENT LAYER (HDR data - 10 or 12-bit)                │   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                          │   │
│  │  Additional dynamic range information (Rec.2020)                     │   │
│  │                                                                       │   │
│  │  Layer 3: DYNAMIC METADATA (scene-by-scene instructions)             │   │
│  │  📊📊📊📊📊📊📊📊📊📊📊📊📊 (per-scene or per-frame)                 │   │
│  │  • Scene 1: MaxCLL=800, tone map curve #5, color boost +10%         │   │
│  │  • Scene 2: MaxCLL=50, tone map curve #2, shadow lift +15%          │   │
│  │  • Scene 3: MaxCLL=2000, tone map curve #8, highlight roll-off      │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  Profiles:                                                                    │
│  • Profile 5 (Streaming): Single-layer HEVC Main 10 + metadata               │
│  • Profile 7 (OTT): Enhanced backward compatibility                           │
│  • Profile 8 (Blu-ray): Dual-layer base + enhancement                         │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
         ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│ Step 3: Display Playback (Your TV at Home 🏠)                                │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  📺 Dolby Vision TV (e.g., LG OLED, Sony Bravia, Vizio)                      │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │           DOLBY VISION CHIP (Hardware Decoder)                        │   │
│  │                                                                       │   │
│  │  1️⃣ Reads Display Capabilities:                                      │   │
│  │     • Peak brightness: 700 nits (not 4000 like reference!)           │   │
│  │     • Color gamut: DCI-P3 (90% of Rec.2020)                          │   │
│  │     • Bit depth: 10-bit panel                                        │   │
│  │     • Local dimming zones: 384 zones                                 │   │
│  │                                                                       │   │
│  │  2️⃣ For EACH Scene, Reads Dynamic Metadata:                         │   │
│  │     📊 Scene 1 metadata: "Peak = 800 nits, use tone curve #5"        │   │
│  │                                                                       │   │
│  │  3️⃣ Performs Real-Time Tone Mapping:                                │   │
│  │     Master had 800 nits, but TV only does 700 nits max               │   │
│  │     → Apply tone curve #5 to compress 800→700 WITHOUT clipping       │   │
│  │     → Preserve relative brightness of other elements                 │   │
│  │     → Adjust colors to compensate for brightness change              │   │
│  │                                                                       │   │
│  │  4️⃣ Scene Changes to Scene 2 (dark cave):                           │   │
│  │     📊 Scene 2 metadata: "Peak = 50 nits, lift shadows +15%"         │   │
│  │     → TV reconfigures INSTANTLY for new scene                        │   │
│  │     → Local dimming zones go nearly BLACK (0.0005 nits OLED)        │   │
│  │     → Subtle details visible in shadows                              │   │
│  │                                                                       │   │
│  │  5️⃣ Display Output:                                                  │   │
│  │     ┌───────────────────────────────────────────────────────────┐   │   │
│  │     │  🌅 Sunset: Optimized for YOUR TV's 700 nit capability   │   │   │
│  │     │  🌑 Cave: Perfect blacks on YOUR TV's contrast ratio      │   │   │
│  │     │  💥 Explosion: Highlights mapped to YOUR TV's limits      │   │   │
│  │     │                                                           │   │   │
│  │     │  = PERFECT picture on YOUR specific display! 🎯          │   │   │
│  │     └───────────────────────────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  💡 Key Insight: Same Dolby Vision content looks OPTIMIZED on:               │
│     • Budget 400-nit TV → Toned down, still looks great                      │
│     • Premium 1000-nit TV → Full brightness, stunning highlights             │
│     • Future 4000-nit TV → Will look even better automatically!              │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

📊 Dynamic vs Static Metadata Comparison
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ HDR10 (Static Metadata) - Set Once, Never Changes                            │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  📹 Entire Movie Gets ONE Metadata Setting:                                  │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  MaxCLL: 1000 nits (brightest point in ENTIRE movie)                 │   │
│  │  MaxFALL: 400 nits (average brightness of ENTIRE movie)              │   │
│  │  Color: Rec.2020                                                     │   │
│  │  Bit depth: 10-bit                                                   │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│            ▼                                                                  │
│  📺 TV Tone Mapping (TV must guess how to handle each scene):                │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  🌅 Scene 1 (Sunset): TV guesses tone curve → may clip highlights    │   │
│  │  🌑 Scene 2 (Dark cave): TV guesses → may crush blacks               │   │
│  │  💥 Scene 3 (Explosion): TV guesses → may blow out highlights        │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ⚠️ Problem: One setting can't optimize for ALL scenes!                      │
│     • Sunset scene uses 800 nits, but metadata says 1000 nits max            │
│     • TV doesn't know actual scene brightness, applies generic curve          │
│     • May lose highlight detail or crush shadows                              │
│                                                                               │
├───────────────────────────────────────────────────────────────────────────────┤
│ DOLBY VISION (Dynamic Metadata) - Updates Every Scene or Frame! ⚡           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  📹 EACH Scene Gets Custom Metadata:                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  🌅 Scene 1: MaxCLL=800, tone curve #5, color boost +10%             │   │
│  │  🌑 Scene 2: MaxCLL=50, tone curve #2, shadow lift +15%              │   │
│  │  💥 Scene 3: MaxCLL=2000, tone curve #8, highlight roll-off          │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│            ▼                                                                  │
│  📺 TV Tone Mapping (TV KNOWS exact requirements for each scene):            │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  🌅 Scene 1: Applies tone curve #5 PRECISELY for 800 nits            │   │
│  │  🌑 Scene 2: Applies tone curve #2 PRECISELY for low-light           │   │
│  │  💥 Scene 3: Applies tone curve #8 PRECISELY for 2000 nit highlights │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ✅ ADVANTAGE: PERFECT optimization for EVERY scene!                         │
│     • Each scene gets custom treatment                                        │
│     • No guessing, TV follows director's exact instructions                   │
│     • Maximum highlight detail without clipping                               │
│     • Deep blacks without crushing shadow detail                              │
│                                                                               │
│  📈 Update Frequency:                                                         │
│     • Scene-by-scene: New metadata every scene change (most common)           │
│     • Frame-by-frame: New metadata every 1/24 sec (premium mastering)         │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

Supported Codecs
----------------
- **HEVC** (H.265): Primary codec
- **AV1**: Emerging support
- Typically Main 10 Profile minimum
- 10-bit or 12-bit color depth

Content Creation Workflow
-------------------------
1. **Master in Dolby Vision**: Professional grading suite
2. **Generate Metadata**: Scene-by-scene analysis
3. **Encode Video**: HEVC with Dolby Vision layers
4. **Package**: MP4 or streaming format
5. **Distribute**: Streaming or physical media

Display Requirements
--------------------
**Dolby Vision Capable Display**:
  - Hardware decoder for Dolby Vision
  - Dolby certification
  - Minimum brightness/color standards
  - Dynamic tone mapping

**Typical Specs**:
  - Peak brightness: 400-1000+ nits
  - Wide color gamut (P3 minimum)
  - Local dimming zones
  - 10-bit panel

Streaming Example
-----------------
Netflix Dolby Vision stream::

    Video:
      Codec: HEVC Main 10
      Profile: Dolby Vision Profile 5
      Resolution: 4K (3840x2160)
      Bitrate: 15-25 Mbps
      HDR: Dolby Vision + HDR10 fallback
    
    Audio:
      Codec: Dolby Atmos (often paired)
      Channels: Object-based spatial audio

Compatibility
-------------
**Supported Platforms**:
  - Apple TV 4K
  - Fire TV (select models)
  - Roku (select models)
  - Smart TVs (LG, Sony, Vizio, Samsung)
  - Xbox Series X/S
  - PlayStation 5
  - iOS devices (iPhone 12+)

**Fallback Behavior**:
  - Non-Dolby Vision displays: Play HDR10 layer
  - SDR displays: Play base SDR layer

Advantages
----------
- **Best Picture Quality**: Dynamic optimization
- **Creator Intent**: Preserves artistic vision
- **Display Optimization**: Adapts to screen capabilities
- **Future-Proof**: Supports advancing display tech
- **Ecosystem**: Strong industry support

Disadvantages
-------------
- **Licensing Costs**: Fees for manufacturers and studios
- **Proprietary**: Not an open standard
- **Limited Content**: Less than HDR10
- **Hardware Required**: Not software-upgradeable
- **File Size**: Larger than standard SDR

Competing Formats
-----------------
**HDR10**:
  - Open standard
  - Static metadata
  - Widespread adoption

**HDR10+**:
  - Dynamic metadata (like Dolby Vision)
  - Royalty-free
  - Samsung backing

**HLG** (Hybrid Log-Gamma):
  - Broadcast-friendly
  - No metadata needed
  - BBC/NHK standard

Content Availability
--------------------
**Streaming**:
  - Netflix (extensive library)
  - Apple TV+ (all originals)
  - Disney+ (select titles)
  - Vudu, iTunes

**Physical Media**:
  - Ultra HD Blu-ray discs
  - Premium releases

**Production**:
  - Cinema releases
  - High-end TV production

Important Notes
---------------
- Requires end-to-end Dolby Vision support (content + display)
- Often paired with Dolby Atmos audio
- Premium feature commanding higher prices
- Most new high-end TVs include Dolby Vision
- Content must be specifically mastered for Dolby Vision
