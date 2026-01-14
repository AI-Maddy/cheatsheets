═══════════════════════════════════════════════════════════════════════════════
🎼 AES67 - Audio-Over-IP Interoperability Standard
═══════════════════════════════════════════════════════════════════════════════

Overview
───────────────────────────────────────────────────────────────────────────────
AES67 is an Audio Engineering Society (AES) standard published in 2013 that defines
interoperability requirements for transporting professional-grade uncompressed audio
over IP networks. Before AES67, proprietary audio-over-IP systems (Dante, Ravenna,
Livewire, Q-LAN) were incompatible, creating vendor lock-in. AES67 establishes a
common baseline using open standards: RTP for transport, PTP (IEEE 1588) for
synchronization, SDP for session description, and SAP for session announcement.

AES67 enables multi-vendor audio systems to coexist and interoperate on the same
network, facilitating hybrid installations, equipment transitions, and broadcast
facility integration. It supports high-channel-count audio (up to 8 channels per
stream typical), low latency (sub-5ms achievable), and synchronized playback across
distributed devices. AES67 is widely adopted in broadcast studios, live sound
reinforcement, installed sound systems, and production facilities where multiple
audio technologies need to work together seamlessly.

Key Features
───────────────────────────────────────────────────────────────────────────────
- Interoperability: Vendor-neutral, works across different systems
- Uncompressed audio: Linear PCM (L16, L24) for maximum quality
- Low latency: Sub-5ms end-to-end achievable
- Scalable: Hundreds of channels per network
- PTP synchronization: IEEE 1588 for sub-microsecond timing accuracy
- RTP transport: RFC 3550 for audio packet delivery
- Multicast and unicast: Flexible routing options
- SDP session description: RFC 4566 for stream metadata
- SAP announcement: RFC 2974 for stream discovery
- Sample rates: 48 kHz, 96 kHz (44.1 kHz optional)

Technical Architecture
───────────────────────────────────────────────────────────────────────────────
Core Components:
1. Audio Transport: RTP (Real-time Transport Protocol)
2. Timing/Sync: PTP IEEE 1588-2008 (PTPv2)
3. Stream Description: SDP (Session Description Protocol)
4. Stream Discovery: SAP (Session Announcement Protocol)
5. Network: Layer 3 (IP multicast/unicast)

Audio Encoding:
- Format: Linear PCM (no compression)
- Bit depths: 16-bit (L16) or 24-bit (L24)
- Sample rates: 48 kHz (mandatory), 96 kHz (optional), 44.1 kHz (optional)
- Channels per stream: 1-8 (typical), up to 16 possible
- Packet size: 48 samples typical (1 ms @ 48 kHz)

RTP Payload
───────────────────────────────────────────────────────────────────────────────
RTP Header:
- Payload type: Dynamic (96-127)
- SSRC: Unique stream identifier
- Timestamp: Sample clock reference
- Sequence number: Packet ordering

Audio Payload:
- Samples interleaved or channel-grouped
- Network byte order (big-endian)
- Padding for alignment

Packet Timing:
- Packet time: Typically 1 ms (48 samples @ 48 kHz)
- Sub-ms possible for ultra-low latency
- RTP timestamp increments by sample count

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. Broadcast studio audio routing and mixing
2. Live sound reinforcement (concerts, events)
3. Installed sound systems (stadiums, conference centers)
4. Production facilities with multi-vendor equipment
5. Remote production (REMI) audio transport
6. OB van audio distribution
7. Intercom systems
8. Multi-room audio installations
9. Theater sound systems
10. Houses of worship audio infrastructure

💡 Memory Aid
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: AES67 as Synchronized Choir                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of AES67 audio network as a CHOIR PERFORMANCE:                    │
│                                                                           │
│  🎶 [Audio Samples] = VOICES singing                                   │
│     24-bit depth = wide dynamic range (whispers to forte!)               │
│     48 kHz sample rate = 48,000 "notes" per second                        │
│                                                                           │
│  👨‍🎼 [PTP Clock] = CONDUCTOR'S BATON                                      │
│     Keeps everyone singing at EXACTLY the same tempo                     │
│     Sub-microsecond timing = perfect unison                               │
│     Without PTP: Everyone slightly off-time → CHAOS! 😱                  │
│                                                                           │
│  📦 [RTP Packets] = SHEET MUSIC PAGES                                    │
│     Each packet = 1 millisecond of audio (48 samples @ 48 kHz)           │
│     Delivered every 1ms like clockwork                                    │
│                                                                           │
│  📝 [SDP Description] = PROGRAM NOTES                                    │
│     "2-channel stereo, 48 kHz, 24-bit, multicast 239.1.2.3"              │
│     Tells receivers what to expect                                        │
│                                                                           │
│  📢 [SAP Announcements] = CONCERT POSTERS                                 │
│     "New stream available! Here's the description..."                     │
│     Automatic discovery, no manual setup                                  │
│                                                                           │
│  The magic: With PTP, audio from 100+ devices plays SAMPLE-ACCURATE!     │
│  Mix them together → perfect phase alignment, no comb filtering! ✅      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

⚡ PTP Synchronization for Audio
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Why PTP is CRITICAL for AES67                                            │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  WITHOUT PTP (Clock Drift):                                              │
│                                                                           │
│  Device A: 48,000.0 Hz ← Local oscillator                               │
│  Device B: 48,001.2 Hz ← Slightly faster crystal (+25 ppm error)       │
│                                                                           │
│  After 1 minute:                                                         │
│   Device A: 2,880,000 samples                                           │
│   Device B: 2,880,072 samples ← 72 samples ahead!                       │
│                                                                           │
│  Result: ❌ Audio buffer overrun/underrun                                │
│          ❌ Clicks, pops, glitches every few seconds                       │
│          ❌ Cannot mix sources (phase drift)                               │
│                                                                           │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                           │
│  WITH PTP (Synchronized):                                                │
│                                                                           │
│         ┌───────────────────┐                                           │
│         │ PTP Grandmaster   │                                           │
│         │ 48,000.00000 Hz   │ ← Reference clock                       │
│         └────────┬──────────┘                                           │
│                  │                                                        │
│      ┌───────────┼───────────┐                                       │
│      │            │            │                                       │
│      ↓            ↓            ↓                                       │
│  Device A     Device B     Device C                                      │
│  48,000.00    48,000.00    48,000.00 Hz ← All locked!                   │
│  ±0.5 ns      ±0.8 ns      ±0.3 ns     ← Sub-microsecond accuracy        │
│                                                                           │
│  Result: ✅ Sample-accurate playback                                       │
│          ✅ No drift, no clicks                                            │
│          ✅ Perfect phase alignment for mixing                            │
│          ✅ Can run for DAYS without resync                                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

📊 RTP Audio Packet Structure
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Complete AES67 RTP Packet @ 48 kHz, 24-bit, 2-channel                   │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Ethernet Header (14 bytes)                                          │  │
│  ├─────────────────────────────────────────────────────────────────┤  │
│  │  Dest MAC: 01:00:5E:xx:xx:xx (multicast)                            │  │
│  │  Src MAC:  AA:BB:CC:DD:EE:FF (sender)                                │  │
│  │  EtherType: 0x0800 (IPv4)                                            │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ IP Header (20 bytes)                                                │  │
│  ├─────────────────────────────────────────────────────────────────┤  │
│  │  Src IP:  192.168.1.10                                               │  │
│  │  Dest IP: 239.1.2.3 (multicast group)                                │  │
│  │  DSCP: EF (Expedited Forwarding for low latency)                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ UDP Header (8 bytes)                                                │  │
│  ├─────────────────────────────────────────────────────────────────┤  │
│  │  Src Port: 53214 (ephemeral)                                         │  │
│  │  Dest Port: 5004 (RTP audio)                                         │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ RTP Header (12 bytes)                                               │  │
│  ├─────────────────────────────────────────────────────────────────┤  │
│  │  Version: 2                                                          │  │
│  │  Payload Type: 97 (dynamic, defined in SDP as L24/48000/2)          │  │
│  │  Sequence #: 54321 (increments each packet)                          │  │
│  │  Timestamp: 2304000000 (sample clock, increments by 48)              │  │
│  │  SSRC: 0xABCD1234 (unique stream identifier)                         │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ AUDIO PAYLOAD (288 bytes for 1 ms @ 48 kHz, 24-bit, 2-ch)          │  │
│  ├─────────────────────────────────────────────────────────────────┤  │
│  │  48 samples × 3 bytes (24-bit) × 2 channels = 288 bytes              │  │
│  │                                                                      │  │
│  │  Sample 0: [L_MSB][L_MID][L_LSB][R_MSB][R_MID][R_LSB]                │  │
│  │  Sample 1: [L_MSB][L_MID][L_LSB][R_MSB][R_MID][R_LSB]                │  │
│  │  ...                                                                 │  │
│  │  Sample 47: [L_MSB][L_MID][L_LSB][R_MSB][R_MID][R_LSB]               │  │
│  │                                                                      │  │
│  │  Network byte order (big-endian)                                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Ethernet FCS (4 bytes CRC)                                          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  Total Packet Size: 346 bytes                                            │
│  Sent 1000 times per second (1 packet every 1 ms)                        │
│  Bandwidth: 346 bytes × 8 bits × 1000 packets/s = 2.768 Mbps              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Synchronization (PTP)
───────────────────────────────────────────────────────────────────────────────
AES67 requires PTP for timing:
- Domain: Any (commonly 0 or 127)
- Profile: Default or media-specific
- Accuracy: Sub-microsecond typical
- Purpose: Synchronize sample clocks across devices

Benefits:
- Eliminates word clock cables
- Phase-coherent audio across network
- Enables distributed sample-accurate mixing
- Supports genlock for video integration

Without PTP:
- Audio drift between devices
- Clicks/pops at buffer boundaries
- Inability to mix synchronized sources

Session Description (SDP)
───────────────────────────────────────────────────────────────────────────────
SDP describes audio stream parameters:

Example SDP:
  v=0
  o=- 123456 1 IN IP4 192.168.1.10
  s=Microphone 1
  c=IN IP4 239.1.2.3/32
  t=0 0
  a=recvonly
  m=audio 5004 RTP/AVP 97
  a=rtpmap:97 L24/48000/2
  a=ptime:1
  a=ts-refclk:ptp=IEEE1588-2008:00-11-22-FF-FE-33-44-55:0
  a=mediaclk:direct=0

Key Fields:
- c=IN IP4 239.1.2.3: Multicast address
- m=audio 5004: UDP port
- a=rtpmap:97 L24/48000/2: 24-bit, 48 kHz, 2 channels
- a=ptime:1: 1 ms packet time
- a=ts-refclk: PTP clock reference
- a=mediaclk: Media clock source

Session Announcement (SAP)
───────────────────────────────────────────────────────────────────────────────
SAP broadcasts SDP to multicast address:
- Address: 224.2.127.254 (IPv4)
- Port: 9875
- Purpose: Automatic stream discovery
- Interval: Every 30 seconds typical

Receiver workflow:
1. Listen to SAP multicast
2. Parse SDP announcements
3. Present available streams to user
4. Subscribe to selected stream's multicast group
5. Receive RTP audio packets

Network Configuration
───────────────────────────────────────────────────────────────────────────────
Multicast Addressing:
- AES67 uses IP multicast for efficiency
- Address range: 239.x.x.x (organization-local)
- One multicast group per audio stream
- IGMP snooping on switches to optimize traffic

Unicast Alternative:
- Point-to-point streams
- Higher bandwidth utilization
- Easier firewall traversal
- No multicast routing required

Quality of Service (QoS):
- DSCP marking: EF (Expedited Forwarding) or AF41
- Low jitter/latency network required
- Dedicated VLAN recommended for large installations
- Bandwidth: ~1.5 Mbps per stereo 48kHz/24-bit stream

Bandwidth Calculation
───────────────────────────────────────────────────────────────────────────────
Per Stream:
  Bitrate = SampleRate × BitDepth × Channels + RTP/UDP/IP/Ethernet overhead

Example (2-channel, 48 kHz, 24-bit):
  Audio: 48,000 × 24 × 2 = 2,304,000 bps = 2.304 Mbps
  Overhead: ~10% = 0.23 Mbps
  Total: ~2.5 Mbps

For 1 ms packets @ 48 kHz:
  48 samples × 3 bytes × 2 channels = 288 bytes/packet
  + RTP (12B) + UDP (8B) + IP (20B) + Ethernet (14B + 4B CRC) = 346 bytes/packet
  1000 packets/sec × 346 bytes × 8 bits = 2.768 Mbps

AES67 vs Proprietary Systems
───────────────────────────────────────────────────────────────────────────────
AES67:
- Open standard, vendor-neutral
- Baseline interoperability
- May lack advanced features
- Requires manual configuration in some cases

Dante / Ravenna / Livewire:
- Proprietary enhancements
- Advanced discovery, control, routing
- Vendor-specific management software
- AES67 mode often available for interop

Hybrid Approach:
- Core system uses proprietary for features
- AES67 mode for interfacing with external equipment
- Best of both worlds: features + interoperability

Implementation Considerations
───────────────────────────────────────────────────────────────────────────────
Network Requirements:
- Gigabit Ethernet minimum (10G for large systems)
- Managed switches with IGMP snooping
- PTP-aware switches for best sync accuracy
- Low latency (<1 ms switch latency preferred)
- Dedicated audio VLAN

Latency Sources:
- Encoding/packetization: <1 ms
- Network transit: 1-3 ms typical
- Jitter buffer: 1-5 ms
- Decoding: <1 ms
- Total: 3-10 ms achievable

Device Configuration:
- Enable AES67 mode (if device is primarily another protocol)
- Configure PTP domain and priority
- Set sample rate (48 kHz common)
- Assign multicast addresses (or use SAP discovery)
- Configure SDP parameters
- Verify PTP sync status before audio operation

Troubleshooting
───────────────────────────────────────────────────────────────────────────────
Common Issues:

No Audio:
- Check PTP synchronization (most common issue)
- Verify multicast routing/IGMP
- Confirm sample rate match
- Check firewall rules

Audio Dropouts:
- Network congestion or packet loss
- Insufficient QoS
- CPU overload on endpoint
- PTP sync loss

Audio Drift/Clicks:
- PTP not synchronized
- Clock domain mismatch
- Network jitter exceeding buffer

Tools:
- Wireshark: Capture and analyze RTP/PTP/SDP packets
- VLC/ffplay: Test receive RTP streams
- ptp4l: Linux PTP daemon
- Audio analyzer: Measure latency, dropouts

🔧 Troubleshooting Guide
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: No audio / stream not discovered                                │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ PTP not synchronized (MOST COMMON):                                    │
│   $ ptp4l -i eth0 -m -H -s                                               │
│   Watch: "rms" value (should be <1000 ns for good audio sync)            │
│   Without PTP: Audio buffers drift, causing clicks/silence               │
│                                                                           │
│ ✓ SAP not working (multicast discovery):                                │
│   $ tcpdump -i eth0 port 9875                                            │
│   Should see SAP announcements every 30 seconds                          │
│   Check IGMP snooping on switches                                        │
│                                                                           │
│ ✓ Not subscribed to multicast group:                                     │
│   Receiver must join multicast group (e.g., 239.1.2.3)                   │
│   $ ip maddr show eth0  ← Check subscribed groups                       │
│                                                                           │
│ ✓ Firewall blocking RTP:                                                 │
│   UDP port 5004 (typical for audio) must be open                         │
│   $ iptables -L | grep 5004                                              │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Audio dropouts / clicks / pops                                  │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Network packet loss:                                                   │
│   $ tcpdump -i eth0 -c 1000 port 5004 | wc -l                           │
│   Should be ~1000 packets (1 packet/ms)                                  │
│   Check: $ ethtool -S eth0 | grep errors                                │
│                                                                           │
│ ✓ Network congestion / jitter:                                           │
│   - Enable QoS (DSCP EF) for audio traffic                               │
│   - Use dedicated VLAN for audio                                         │
│   - Check switch queue depths                                            │
│                                                                           │
│ ✓ PTP clock instability:                                                 │
│   $ ptp4l -i eth0 -m -H -s  (watch offset variance)                     │
│   Should be stable ±<5 µs; if jumping wildly, check network            │
│                                                                           │
│ ✓ Jitter buffer too small:                                               │
│   Increase receiver buffer size (5-10 ms typical)                        │
│   Larger buffer = more latency but better dropout immunity               │
│                                                                           │
│ ✓ CPU overload on receiver:                                              │
│   Check: $ top  (high CPU usage during audio playback?)                 │
│   Reduce processing load or upgrade hardware                             │
└───────────────────────────────────────────────────────────────────────────┘

⚡ Quick Diagnostic Commands
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Check PTP Sync Status:                                                   │
│   $ ptp4l -i eth0 -m -H -s                                               │
│   Watch: "rms" value (should be <1000 ns for good audio sync)            │
│                                                                           │
│ Monitor SAP Announcements:                                               │
│   $ tcpdump -i eth0 -vv port 9875                                        │
│   Should see periodic SDP announcements                                  │
│                                                                           │
│ Capture RTP Audio Packets:                                               │
│   $ tcpdump -i eth0 -c 1000 port 5004                                    │
│   $ tcpdump -i eth0 -w audio.pcap host 239.1.2.3                         │
│   Analyze with Wireshark: Statistics → RTP → Stream Analysis             │
│                                                                           │
│ Test Audio Stream with VLC:                                              │
│   $ vlc rtp://239.1.2.3:5004                                             │
│   Or: Media → Open Network Stream → rtp://239.1.2.3:5004                 │
│                                                                           │
│ Check Multicast Subscriptions:                                           │
│   $ ip maddr show eth0                                                   │
│   $ netstat -g                                                           │
│                                                                           │
│ Verify Network Performance:                                              │
│   $ iperf3 -c <server> -u -b 10M -t 60  ← Test UDP bandwidth/jitter     │
│   $ ethtool -S eth0 | grep -E '(error|drop)'                            │
└───────────────────────────────────────────────────────────────────────────┘


Related Standards
───────────────────────────────────────────────────────────────────────────────
- SMPTE ST 2110-30: Professional media AES67-based audio
- SMPTE ST 2059: PTP profile for broadcast
- NMOS IS-04/IS-05: Discovery and connection management
- Dante: Can operate in AES67 mode
- Ravenna: AES67-compliant by design
- Livewire+: AES67-compatible

Important Notes
───────────────────────────────────────────────────────────────────────────────
- AES67 is a compatibility standard, not a complete audio networking solution
- Devices must be configured for AES67 mode (often not default)
- PTP synchronization is mandatory; without it, AES67 audio will fail
- Multicast requires proper network configuration (IGMP snooping, PIM routing)
- Latency requirements drive packet size; smaller packets = lower latency but more overhead
- Not all AES67 implementations are equal; test interoperability before deployment
- Security not defined in AES67; consider network segmentation and VLANs
- AES67 defines audio transport only; control/routing varies by vendor
- Sample rate conversion may be needed when interfacing 48 kHz and 44.1 kHz systems
- SMPTE 2110-30 extends AES67 for broadcast-specific requirements
