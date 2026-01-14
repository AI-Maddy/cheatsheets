═══════════════════════════════════════════════════════════════════════════════
🎭 Dolby AC-3 / Dolby Digital - Legacy Multichannel Audio
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **AC-3 = Audio Codec 3 = 3rd generation = DVD era!** 💿🎬

🧠 **Memory Palace**: Picture a 1990s HOME THEATER 🏠🎭 with a DVD player 💿 and 
FIVE speakers around you + one SUBWOOFER (5.1). This is the DOLBY DIGITAL revolution! 
The center speaker 📢 is for DIALOGUE, side speakers for EFFECTS 💥, rear speakers 
for AMBIENCE 🌳, and the subwoofer for EXPLOSIONS 💣. Every DVD must play AC-3 
(mandatory standard).

Overview
───────────────────────────────────────────────────────────────────────────────
Dolby Digital, officially known as AC-3 (Audio Codec 3), is a lossy multichannel
audio compression technology developed by Dolby Laboratories. First introduced in 1991
and standardized as ATSC A/52, AC-3 revolutionized home theater by bringing 5.1
surround sound to consumers through DVD, Blu-ray, digital television, and cinema.

The codec uses perceptual coding techniques to compress audio while maintaining
subjective quality, operating at bit rates from 64 kbps to 640 kbps. AC-3's 5.1
channel configuration (Left, Center, Right, Left Surround, Right Surround, plus LFE)
became the industry standard for home theater systems. Despite being succeeded by
Dolby Digital Plus and Dolby Atmos, AC-3 remains mandatory in many broadcast and
physical media standards due to its widespread decoder availability.

Key Features
───────────────────────────────────────────────────────────────────────────────
- Channel configurations: Mono, stereo, 3.0, 2.1, 3.1, 2.2, 5.0, 5.1
- Bit rates: 64 kbps to 640 kbps (typically 192-448 kbps for 5.1)
- Sampling rates: 32 kHz, 44.1 kHz, 48 kHz
- Perceptual coding: Frequency-domain compression using MDCT
- Dynamic range control: Metadata for playback level adjustment
- Downmixing metadata: Instructions for converting multichannel to stereo
- Dialog normalization (dialnorm): Consistent loudness across programs
- Low complexity decoding: Efficient implementation on consumer hardware
- Bit stream modes: Multiple audio service types (main, commentary, etc.)

Channel Configuration (5.1)
───────────────────────────────────────────────────────────────────────────────
Main Channels:
- L (Left front)
- C (Center front)
- R (Right front)
- LS (Left surround)
- RS (Right surround)
- LFE (Low Frequency Effects): 3-120 Hz subwoofer channel

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. DVD video mandatory audio format (all DVD players must decode AC-3)
2. Blu-ray disc audio (mandatory for players to decode)
3. Digital television broadcasting (ATSC, DVB mandatory/optional)
4. Digital cinema distribution (Cinema DCP)
5. Cable television HD channels
6. Streaming services (legacy support/fallback codec)
7. Video game console audio output
8. Professional video production and post-production

⚡ AC-3 5.1 Channel Layout Visualization
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Home Theater Speaker Arrangement (5.1 Surround Sound)                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│                          📢 CENTER (C)                                      │
│                         Dialogue, vocals                                   │
│                                                                           │
│         🔊 LEFT (L)               🔊 RIGHT (R)                              │
│         Music, effects           Music, effects                          │
│                                                                           │
│                                                                           │
│                          📺 LISTENER 💂                                  │
│                         (sweet spot)                                      │
│                                                                           │
│                                                                           │
│      🔉 LEFT SURROUND (LS)    🔉 RIGHT SURROUND (RS)                     │
│      Ambient, rear effects     Ambient, rear effects                       │
│                                                                           │
│                                                                           │
│                       🔊 SUBWOOFER (LFE)                                  │
│                       Low frequency effects                               │
│                       3-120 Hz (explosions)                               │
│                                                                           │
│  Total: 5.1 = 5 full-range + 1 LFE (Low Frequency Effects)                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Technical Specifications
───────────────────────────────────────────────────────────────────────────────
Encoding:
- Transform: Modified Discrete Cosine Transform (MDCT)
- Block size: 512 samples
- Frame size: 1536 samples (32 ms at 48 kHz)
- Coupling: Shared high-frequency information across channels
- Exponent strategy: Adaptive spectral envelope coding
- Bit allocation: Psychoacoustic model-based quantization

Typical Bit Rates:
- 5.1 channels: 384-448 kbps (common for broadcast/DVD)
- Stereo: 192-256 kbps
- Mono: 96-128 kbps

Metadata:
- Dialnorm: Target dialogue level (-31 to -1 dBFS)
- Compression profile: Dynamic range control settings
- Surround mode: Lt/Rt or Lo/Ro downmix

File Extensions:
- .ac3 (raw AC-3 elementary stream)
- .ec3 (Enhanced AC-3/E-AC-3)
- Typically muxed in .ts, .m2ts, .vob, .mkv containers

Important Notes
───────────────────────────────────────────────────────────────────────────────
- Patent encumbered: Licensing required through Dolby Laboratories
- Maximum 640 kbps total bit rate limits quality compared to lossless formats
- Mandatory decode support ensures universal playback compatibility
- Dialog normalization must be set correctly to avoid level mismatches
- Not suitable for music production/archival due to lossy compression
- Superseded by E-AC-3 (Dolby Digital Plus) for streaming and Blu-ray
- Most modern receivers support AC-3 via S/PDIF or HDMI passthrough
