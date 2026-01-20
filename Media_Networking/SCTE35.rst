═══════════════════════════════════════════════════════════════════════════════
💰 SCTE-35 - Standard for Digital Program Insertion Cueing
═══════════════════════════════════════════════════════════════════════════════

Overview
───────────────────────────────────────────────────────────────────────────────
SCTE-35 is a standard developed by the Society of Cable Telecommunications Engineers
for inserting cue markers into digital video streams to signal ad insertion
opportunities and other program events. Published in 2001 and continuously updated,
SCTE-35 defines a message format embedded in MPEG-2 Transport Streams that allows
downstream systems to identify precise timing for local ad insertions, blackouts,
network transitions, and other program splicing events.

The standard works by inserting splice information messages into the transport stream,
typically as MPEG-2 private sections. These messages contain commands like
splice_insert, time_signal, and splice_schedule along with timing information that
enables frame-accurate insertion points. SCTE-35 is fundamental to modern television
advertising, enabling targeted advertising, local ad replacement, and dynamic ad
insertion (DAI) in both linear broadcast and streaming environments.

Key Features
───────────────────────────────────────────────────────────────────────────────
- Frame-accurate cueing: Precise timing for ad insertion points
- In-band signaling: Carried within the video transport stream
- Multiple message types: Insert, schedule, return, cancel commands
- Segmentation descriptors: Classify content type (program, ad, break)
- PTS/DTS timing: Synchronized with video presentation timestamps
- Splice immediate: Immediate splicing at message arrival
- Pre-roll signaling: Advance warning for preparation
- UPID (Unique Program Identifier): Content identification
- Multiple delivery: MPEG-TS sections, HLS manifests, DASH events
- Backward compatible: Works with legacy SCTE-30 systems

Common Message Types
───────────────────────────────────────────────────────────────────────────────
1. splice_insert: Immediate or scheduled content splice point
2. time_signal: Generic timing signal with descriptors
3. splice_schedule: Pre-scheduled splice events
4. bandwidth_reservation: Reserve bandwidth for future insertion
5. private_command: Vendor-specific extensions
6. splice_null: Cancels previous splice event

Segmentation Descriptor Types:
- Program Start/End
- Chapter Start/End
- Provider Advertisement Start/End
- Distributor Advertisement Start/End
- Unscheduled Event Start/End
- Network Start/End

💡 Memory Aid
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: SCTE-35 as Highway Exit Signs                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of a TV program as a highway journey:                              │
│                                                                           │
│  🚗 [Program Content] ══════════════════════════════════════► [Viewer]   │
│                                                                           │
│  SCTE-35 messages = EXIT SIGNS along the highway:                        │
│                                                                           │
│  🪧 "EXIT IN 5 SECONDS" ← splice_insert with pre-roll                   │
│     (Gives ad server time to prepare!)                                    │
│                                                                           │
│  🛣️  Exit Ramp ← Splice point (pts_time)                                │
│     Leave highway = out_of_network_indicator = 1                          │
│                                                                           │
│  🏪 [Ad Break Rest Stop] ← 30-second break_duration                      │
│                                                                           │
│  🛣️  On-Ramp ← Return cue (out_of_network = 0)                          │
│                                                                           │
│  🚗 Back to main highway ════════════════════════►                       │
│                                                                           │
│  The signs (SCTE-35) just tell you WHERE to exit and when to return—     │
│  the AD DECISION SERVER decides WHICH rest stop (ad) you visit!           │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

⚡ SCTE-35 Timeline Visualization
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Program Timeline with SCTE-35 Messages                                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  T-5s          T=0 (PTS)              T+30s                              │
│   │              │                      │                                 │
│   📨             🎬                     🔙                                │
│   SCTE-35      SPLICE                 RETURN                             │
│   OUT          POINT                   CUE                               │
│   │              │                      │                                 │
│   v              v                      v                                 │
│                                                                           │
│  [====== PROGRAM CONTENT ======]                                          │
│                                 \                                         │
│                                  \                                        │
│                                   ╲_____ splice_insert                    │
│                                         (out_of_network=1)                │
│                                                                           │
│                                 [== AD POD: 30s ==]                       │
│                                 [Ad1: 15s][Ad2: 15s]                      │
│                                                      \                    │
│                                                       \                   │
│                                                        ╲____ return cue   │
│                                                             (out=0)       │
│                                                                           │
│  [======================== PROGRAM RESUMES ========================]      │
│                                                                           │
├───────────────────────────────────────────────────────────────────────────┤
│ Key Timing Concepts:                                                      │
│  • T-5s: Pre-roll warning (splicer + ad server prepare)                  │
│  • T=0: Exact PTS (Presentation Time Stamp) to execute splice            │
│  • Break duration: 30s specified in break_duration field                  │
│  • Return: Automatic after duration OR explicit return cue                │
└───────────────────────────────────────────────────────────────────────────┘

📊 Message Structure Visualization
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ splice_info_section Anatomy                                               │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ HEADER                                                            │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ table_id: 0xFC (identifies this as SCTE-35)                       │  │
│  │ section_length: Total message size                                │  │
│  │ protocol_version: 0                                               │  │
│  │ pts_adjustment: Global timeline offset (usually 0)                │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ SPLICE COMMAND (variable based on command_type)                   │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ splice_insert (0x05):                                             │  │
│  │   ├─ splice_event_id: 12345                                       │  │
│  │   ├─ out_of_network_indicator: 1 (leaving for ads)                │  │
│  │   ├─ splice_immediate_flag: 0 (scheduled)                         │  │
│  │   ├─ pts_time: 3600000 (PTS ticks, 40 seconds at 90kHz)          │  │
│  │   ├─ break_duration: 2700000 (30 seconds)                         │  │
│  │   └─ unique_program_id: 0x0001                                    │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ DESCRIPTORS (optional, rich metadata)                             │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ Segmentation Descriptor:                                          │  │
│  │   ├─ segmentation_event_id: 67890                                 │  │
│  │   ├─ segmentation_type_id: 0x34 (Provider Ad Start)               │  │
│  │   ├─ segment_num: 1 (first ad in break)                           │  │
│  │   ├─ segments_expected: 2 (2 ads total)                           │  │
│  │   ├─ segmentation_upid_type: 0x08 (Ad-ID)                         │  │
│  │   └─ segmentation_upid: "ABC1234567H" (specific ad creative)      │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ CRC_32: 0x1A2B3C4D (integrity check)                              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. Linear TV ad insertion (cable, satellite, IPTV)
2. Server-side dynamic ad insertion (SSAI/DAI) for streaming
3. Regional blackout enforcement (sports)
4. Local station break signaling
5. Emergency alert system (EAS) triggers
6. Program boundary detection for DVR
7. Content replacement for localization
8. Targeted advertising based on viewer data
9. OTT streaming ad placement (HLS, DASH)
10. Broadcast automation system triggers

Technical Specifications
───────────────────────────────────────────────────────────────────────────────
Transport:
- PID: Typically 0x86 (134) or configurable
- Table ID: 0xFC (252) for splice_info_section
- Carried as MPEG-2 private sections in transport stream
- Can be carried in HLS (#EXT-X-DATERANGE) and DASH (EventStream)

Message Structure:
splice_info_section() {
    table_id (8 bits) = 0xFC
    section_length (12 bits)
    protocol_version (8 bits) = 0
    encrypted_packet (1 bit)
    pts_adjustment (33 bits)
    tier (12 bits)
    splice_command_length (12 bits)
    splice_command_type (8 bits)
    descriptor_loop_length (16 bits)
    splice_descriptor() [loop]
    CRC_32 (32 bits)
}

splice_insert() Fields:
- splice_event_id: Unique identifier for splice event
- out_of_network_indicator: 1=leaving network, 0=returning
- splice_immediate_flag: Execute immediately vs scheduled
- pts_time: Presentation timestamp for splice point (33 bits)
- duration_flag: Whether splice has defined duration
- break_duration: Length of ad break
- unique_program_id: Identifies the content
- avail_num: Ad avail number within break
- avails_expected: Total number of avails in break

Segmentation Descriptor:
- segmentation_event_id: Unique event identifier
- segmentation_duration: Length of segment
- segmentation_upid_type: Type of unique program ID
- segmentation_upid: Content identifier (various formats)
- segmentation_type_id: Category (0x30-0x3F = provider ad, etc.)
- segment_num: Position within sequence
- segments_expected: Total segments in sequence

Timing Example
───────────────────────────────────────────────────────────────────────────────
Pre-roll Timing:
- SCTE-35 message arrives 4-8 seconds before splice point
- Gives ad server time to prepare/fetch ads
- pts_time indicates exact frame to splice
- Splicer executes at pts_time

Immediate Splice:
- splice_immediate_flag = 1
- Execute splice as soon as message received
- Used for emergency alerts, live events

HLS/DASH Integration
───────────────────────────────────────────────────────────────────────────────
HLS (#EXT-X-DATERANGE):
  #EXT-X-DATERANGE:ID="splice-12345",START-DATE="2026-01-13T...",
  DURATION=30.0,SCTE35-OUT=0xFC3...

DASH (EventStream):
  <EventStream schemeIdUri="urn:scte:scte35:2013:xml">
    <Event presentationTime="123456" duration="30000">
      <scte35:SpliceInfoSection>...</scte35:SpliceInfoSection>
    </Event>
  </EventStream>

Workflow
───────────────────────────────────────────────────────────────────────────────
1. Content provider encodes video with SCTE-35 markers
2. Markers signal ad opportunity (splice_insert with out_of_network=1)
3. Ad decision server (ADS) receives SCTE-35 cue
4. ADS determines which ads to insert (targeting, duration)
5. Splicer/packager replaces content with ads at specified PTS
6. Return cue (out_of_network=0) signals end of ad break
7. Stream returns to main program

🎯 HLS Integration Deep Dive
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ SCTE-35 in HLS Manifests (#EXT-X-DATERANGE)                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Master Playlist: stream.m3u8                                             │
│  ├─ Variant 1: 1080p @ 5 Mbps                                            │
│  └─ Variant 2: 720p @ 2.5 Mbps                                           │
│                                                                           │
│  Media Playlist: 1080p.m3u8                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ #EXTM3U                                                              │ │
│  │ #EXT-X-VERSION:6                                                     │ │
│  │ #EXT-X-TARGETDURATION:6                                              │ │
│  │                                                                      │ │
│  │ #EXTINF:6.0                                                          │ │
│  │ segment0001.ts                                                       │ │
│  │ #EXTINF:6.0                                                          │ │
│  │ segment0002.ts                                                       │ │
│  │                                                                      │ │
│  │ #EXT-X-DATERANGE:ID="splice-12345",                                │ │
│  │   START-DATE="2026-01-13T10:30:05.000Z",                           │ │
│  │   DURATION=30.0,                                                     │ │
│  │   SCTE35-OUT=0xFC302F00000000000000FFF01405000001... (base64)       │ │
│  │        └─────┬─────┘                                                │ │
│  │              Base64-encoded SCTE-35 binary message                   │ │
│  │                                                                      │ │
│  │ #EXTINF:6.0  ← Segment at splice point                              │ │
│  │ segment0003.ts                                                       │ │
│  │                                                                      │ │
│  │ [Ad insertion happens here - SSAI replaces segments with ad content]│ │
│  │                                                                      │ │
│  │ #EXT-X-DATERANGE:ID="splice-12345-return",                         │ │
│  │   START-DATE="2026-01-13T10:30:35.000Z",                           │ │
│  │   SCTE35-IN=0xFC301100000000000000FFF00506... (return cue)          │ │
│  │                                                                      │ │
│  │ #EXTINF:6.0  ← Resume program content                               │ │
│  │ segment0009.ts                                                       │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

📺 DASH Integration Deep Dive
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ SCTE-35 in DASH MPD (EventStream)                                        │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  <MPD xmlns="urn:mpeg:dash:schema:mpd:2011">                            │
│    <Period id="period1" start="PT0S">                                   │
│                                                                           │
│      <!-- SCTE-35 Events in-band -->                                     │
│      <EventStream schemeIdUri="urn:scte:scte35:2013:xml"                │
│                   timescale="90000">                                     │
│                                                                           │
│        <!-- Ad Break Start -->                                           │
│        <Event presentationTime="324000000"   (3600s × 90kHz)             │
│               duration="2700000"              (30s × 90kHz)              │
│               id="12345">                                                │
│          <scte35:SpliceInfoSection>                                      │
│            <scte35:SpliceInsert spliceEventId="12345"                   │
│                                outOfNetworkIndicator="true"               │
│                                spliceImmediateFlag="false">              │
│              <scte35:Program><scte35:SpliceTime ptsTime="324000000"/>   │
│              </scte35:Program>                                           │
│              <scte35:BreakDuration duration="2700000"/>                 │
│            </scte35:SpliceInsert>                                        │
│          </scte35:SpliceInfoSection>                                     │
│        </Event>                                                          │
│                                                                           │
│        <!-- Ad Break End (Return) -->                                    │
│        <Event presentationTime="326700000"                               │
│               id="12345-return">                                         │
│          <scte35:SpliceInfoSection>                                      │
│            <scte35:SpliceInsert spliceEventId="12345"                   │
│                                outOfNetworkIndicator="false"/>           │
│          </scte35:SpliceInfoSection>                                     │
│        </Event>                                                          │
│                                                                           │
│      </EventStream>                                                      │
│                                                                           │
│      <AdaptationSet ...>                                                 │
│        <Representation bandwidth="5000000" ...>                          │
│          <SegmentTemplate .../>                                          │
│        </Representation>                                                 │
│      </AdaptationSet>                                                    │
│    </Period>                                                             │
│  </MPD>                                                                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

🔧 Troubleshooting Guide
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Ads not inserting at cue points                                 │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Check SCTE-35 PID: Verify splicer listening to correct PID (0x86)     │
│ ✓ Validate table_id: Must be 0xFC for splice_info_section               │
│ ✓ Check splice_event_id: Must be unique, non-zero                       │
│ ✓ Verify pts_time: Must be in future relative to current PCR             │
│ ✓ Pre-roll timing: Allow 4-8 seconds before splice for ad server prep   │
│ ✓ Check out_of_network_indicator: Must be 1 for ad break start          │
│ ✓ CRC validation: Corrupted messages silently dropped                    │
│ ✓ Tool: Use ffprobe to dump SCTE-35: ffprobe -show_data stream.ts       │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Splicing at wrong time / frame accuracy issues                  │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ PTS synchronization: Ensure pts_time aligned with video PTS            │
│ ✓ Check pts_adjustment field: Global offset, usually 0                   │
│ ✓ PCR accuracy: Verify Program Clock Reference continuity                │
│ ✓ splice_immediate_flag: If 1, executes immediately (no PTS check)       │
│ ✓ GOP boundaries: Best practice to splice at I-frame starts              │
│ ✓ Timescale: PTS at 90kHz (1 tick = 1/90000 second)                     │
│ ✓ Tool: Use MediaInfo or tstools to check PTS continuity                 │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: HLS/DASH players ignoring SCTE-35 markers                       │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ HLS: Ensure #EXT-X-VERSION:6+ (DATERANGE requires v6)                 │
│ ✓ HLS: Validate SCTE35-OUT base64 encoding (not binary)                  │
│ ✓ DASH: Check schemeIdUri="urn:scte:scte35:2013:xml"                    │
│ ✓ DASH: Verify timescale="90000" matches PTS timescale                  │
│ ✓ Player support: Not all players parse SCTE-35 (need SSAI instead)     │
│ ✓ SSAI: Server-side insertion bypasses client parsing entirely           │
│ ✓ Tool: Validate manifest with HLS/DASH validator tools                  │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Break duration mismatch (ads shorter/longer than break)         │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Check break_duration field: Specified in 90kHz ticks                   │
│ ✓ Ad server logic: Must respect break_duration from SCTE-35              │
│ ✓ Filler content: Use slate/black for undersold inventory                │
│ ✓ Early return: Send explicit return cue if ads end early                │
│ ✓ Auto-return: Some splicers auto-return after break_duration            │
│ ✓ avail_num/avails_expected: Helps ad server pack break correctly        │
└───────────────────────────────────────────────────────────────────────────┘

⚡ Quick Reference: Common segmentation_type_id Values
───────────────────────────────────────────────────────────────────────────────
┌────────┬───────────────────────────────────────────────────────────────┐
│  ID    │ Segmentation Type                                             │
├────────┼───────────────────────────────────────────────────────────────┤
│ 0x10   │ Program Start                                                 │
│ 0x11   │ Program End                                                   │
│ 0x22   │ Chapter Start                                                 │
│ 0x23   │ Chapter End                                                   │
│ 0x30   │ Provider Advertisement Start                                  │
│ 0x31   │ Provider Advertisement End                                    │
│ 0x32   │ Distributor Advertisement Start                               │
│ 0x33   │ Distributor Advertisement End                                 │
│ 0x34   │ Provider Placement Opportunity Start                          │
│ 0x35   │ Provider Placement Opportunity End                            │
│ 0x36   │ Distributor Placement Opportunity Start                       │
│ 0x37   │ Distributor Placement Opportunity End                         │
│ 0x40   │ Unscheduled Event Start                                       │
│ 0x41   │ Unscheduled Event End                                         │
│ 0x50   │ Network Start (joining network feed)                          │
│ 0x51   │ Network End (leaving network feed)                            │
└────────┴───────────────────────────────────────────────────────────────┘

Important Notes
───────────────────────────────────────────────────────────────────────────────
- SCTE-35 only provides cue points; ad decision logic is separate
- Encrypted packets require decryption key (typically not used in practice)
- HLS/DASH implementations may use simplified SCTE-35 subset
- Not all players/platforms support all SCTE-35 features
- Segmentation descriptors added in later revisions for richer metadata
- UPIDs enable content identification across systems (EIDR, Ad-ID, etc.)
- Multiple concurrent splice events require careful event_id management
- PTS adjustment allows global timeline correction
- CRC_32 ensures message integrity
- SCTE-224 and ESAM provide higher-level ad management on top of SCTE-35
