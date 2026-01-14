═══════════════════════════════════════════════════════════════════════════════
🎛️ ESAM - Event Signaling and Management
═══════════════════════════════════════════════════════════════════════════════

Overview
───────────────────────────────────────────────────────────────────────────────
ESAM (Event Signaling and Management) is a standardized API specification developed
by CableLabs for communication between video processing systems and ad decision
servers in dynamic ad insertion workflows. Published as part of the CableLabs
specification suite, ESAM provides a vendor-neutral interface that enables packagers,
transcoders, and origin servers to interact with ad servers using a consistent
protocol, simplifying integration and enabling multi-vendor interoperability.

ESAM acts as a bridge between SCTE-35 cue points in video streams and the business
logic that determines which ads to insert. When a video processor encounters a
SCTE-35 marker, it uses ESAM to query an ad decision server (ADS), providing context
about the content, viewer, and opportunity. The ADS responds with specific instructions
about which ads to insert, their duration, tracking beacons, and other metadata.
This separation of concerns allows specialized ad platforms to make sophisticated
targeting decisions while video infrastructure handles the technical splicing.

Key Features
───────────────────────────────────────────────────────────────────────────────
- RESTful XML/JSON API: HTTP-based communication protocol
- SCTE-35 abstraction: Translates cue points into ad opportunities
- Request/response model: Processor queries ADS for ad decisions
- Rich context: Passes content, viewer, and opportunity metadata
- Multiple ad pods: Support for complex multi-ad breaks
- Tracking URLs: Beacons for ad impressions, quartiles, completion
- Blackout signaling: Regional content restrictions
- Alternate content: Non-ad replacements (promos, slates)
- Companion ads: Synchronized banner/overlay ads
- Error handling: Fallback and timeout behaviors

ESAM Message Types
───────────────────────────────────────────────────────────────────────────────
Requests (Processor → Ad Server):
1. SignalProcessingNotification: Reports SCTE-35 cue detection
2. SignalProcessingEvent: Detailed event with context
3. ConditioningInfo: Content metadata for ad decisions

Responses (Ad Server → Processor):
1. SignalProcessingNotificationResponse: Ad insertion instructions
2. AcquisitionPointInfo: Specific ads to insert
3. Alternative: Replacement content details
4. UTCPoint: Timing information for execution

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. Server-side dynamic ad insertion (SSAI/DAI)
2. Cloud-based video processing with ad integration
3. OTT streaming ad decisioning (HLS, DASH)
4. IPTV headend ad replacement systems
5. Multi-platform ad serving (web, mobile, TV)
6. Personalized ad targeting based on viewer data
7. Regional blackout enforcement
8. Ad pod management for live and VOD
9. Programmatic ad buying integration
10. Cross-platform ad campaign tracking

💡 Memory Aid
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: ESAM as Restaurant Order System                        │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of a video packager as a WAITER at a restaurant:                  │
│                                                                           │
│  🍽️ [Video Packager/Waiter]                                              │
│      Sees SCTE-35 cue = "Table 5 wants to order"                         │
│                                                                           │
│  Waiter doesn't decide WHAT food to serve—they ask the kitchen!          │
│                                                                           │
│  📋 ESAM Request = Order Ticket to Kitchen:                              │
│     "Table 5, 2 people, vegetarian, 30-minute meal window"                │
│                                                                           │
│  👨‍🍳 [Ad Decision Server/Kitchen]                                          │
│     Checks inventory, dietary restrictions, timing                        │
│     Decides: "Serve pasta (Ad 1), then salad (Ad 2)"                     │
│                                                                           │
│  📝 ESAM Response = Kitchen Ticket:                                       │
│     "Dish URLs, cooking times, plating instructions"                      │
│                                                                           │
│  🍝 [Packager Fetches Ads from CDN]                                       │
│     Gets ad creative, splices into stream                                 │
│                                                                           │
│  📊 [Tracking Beacons] = Customer feedback:                               │
│     "Started eating, halfway done, finished meal, loved it!"              │
│                                                                           │
│  ESAM separates WHAT to serve (ADS logic) from HOW to serve (packager)!  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

⚡ ESAM Workflow Visualization
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Complete ESAM Request-Response Cycle                                     │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  T-4s         T=0 (Splice)        T+15s         T+30s                    │
│   │               │                  │             │                      │
│   │               │                  │             │                      │
│   📺 [Program Content flowing through packager]                          │
│   │               │                  │             │                      │
│   └─► 🔔 SCTE-35 cue detected!                                           │
│       splice_event_id=12345                                              │
│       break_duration=30s                                                 │
│       │                                                                   │
│       └──► 📤 ESAM SignalProcessingNotification                          │
│            │                                                              │
│            │  POST /esam/signal                                           │
│            │  {                                                           │
│            │    "contentId": "movie-12345",                              │
│            │    "duration": "PT30S",                                     │
│            │    "acquisitionSignalID": "scte35-12345",                  │
│            │    "viewerContext": {                                       │
│            │      "location": "US-CA-94102",                            │
│            │      "device": "smart-tv"                                  │
│            │    }                                                         │
│            │  }                                                           │
│            │                                                              │
│            └──────► 🤖 [Ad Decision Server]                              │
│                      │                                                    │
│                      ├─ Query ad inventory                                │
│                      ├─ Apply targeting rules (geo, device)              │
│                      ├─ Select ads to fit 30s break:                     │
│                      │   • Ad 1: 15s (car commercial)                    │
│                      │   • Ad 2: 15s (beverage ad)                       │
│                      │                                                    │
│            ┌─────────┘                                                    │
│            │                                                              │
│       ◄────┘ 📥 ESAM SignalProcessingNotificationResponse                │
│            │                                                              │
│            │  {                                                           │
│            │    "alternatives": [                                        │
│            │      {                                                       │
│            │        "uri": "https://cdn.ex.com/ads/car.mp4",             │
│            │        "duration": "PT15S",                                 │
│            │        "trackingEvents": {                                  │
│            │          "impression": "https://track.ex/imp?id=ad1"       │
│            │        }                                                     │
│            │      },                                                      │
│            │      {                                                       │
│            │        "uri": "https://cdn.ex.com/ads/beverage.mp4",       │
│            │        "duration": "PT15S"                                  │
│            │      }                                                       │
│            │    ]                                                         │
│            │  }                                                           │
│            │                                                              │
│       └────┴──► 📦 Packager fetches ads from CDN                         │
│               │                                                           │
│               └──► 🎬 [Ad 1: 15s]══► 🎬 [Ad 2: 15s]                     │
│                       │                    │                              │
│                       └─► 📊 Beacon        └─► 📊 Beacon                 │
│                          (impression)          (impression)               │
│                                                                           │
│                                           └──► 📺 [Program Resumes]      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

📊 ESAM vs SCTE-35 vs POIS
───────────────────────────────────────────────────────────────────────────────
┌─────────────┬──────────────────────┬──────────────────────┬─────────────┐
│ Protocol    │ Purpose              │ Timing               │ Abstraction │
├─────────────┼──────────────────────┼──────────────────────┼─────────────┤
│ SCTE-35     │ Cue marker           │ Real-time (in-band)  │ Low         │
│             │ "Splice here!"       │ 0-8s pre-roll        │ (PTS/bits)  │
├─────────────┼──────────────────────┼──────────────────────┼─────────────┤
│ ESAM        │ Ad decision request  │ Real-time (seconds)  │ Medium      │
│             │ "Which ads to serve?"|  before splice       │ (REST API)  │
├─────────────┼──────────────────────┼──────────────────────┼─────────────┤
│ POIS        │ Opportunity metadata │ Advance (hours/days) │ High        │
│             │ "What's available?"  │ Pre-planning         │ (business)  │
└─────────────┴──────────────────────┴──────────────────────┴─────────────┘

Typical Integration:
  POIS (planning) → ESAM (decisioning) → SCTE-35 (execution)

Technical Workflow
───────────────────────────────────────────────────────────────────────────────
1. Video processor detects SCTE-35 splice_insert message
2. Processor sends SignalProcessingNotification to ADS via ESAM
   - Includes content ID, timestamp, duration, viewer context
3. ADS evaluates ad opportunity:
   - Checks ad inventory and campaigns
   - Applies targeting rules (geo, demographic, behavioral)
   - Selects ads to fill break duration
4. ADS responds with SignalProcessingNotificationResponse:
   - List of ads with URLs, durations, tracking beacons
   - Timing instructions (immediate, scheduled)
5. Processor retrieves ad media (from CDN/origin)
6. Processor splices ads into stream at specified time
7. Processor fires tracking beacons as playback progresses
8. Stream returns to main content after ad break

Request Example (Simplified)
───────────────────────────────────────────────────────────────────────────────
POST /esam/signal HTTP/1.1
Content-Type: application/xml

<SignalProcessingNotification>
  <conditioningInfo>
    <contentId>movie-12345</contentId>
    <duration>PT30S</duration>
  </conditioningInfo>
  <acquisitionPointIdentity>
    <acquisitionSignalID>scte35-event-001</acquisitionSignalID>
    <acquisitionTime>2026-01-13T10:30:00Z</acquisitionTime>
  </acquisitionPointIdentity>
  <signalProcessingEventList>
    <signalProcessingEvent>
      <startUTC>2026-01-13T10:30:05Z</startUTC>
      <duration>PT30S</duration>
    </signalProcessingEvent>
  </signalProcessingEventList>
</SignalProcessingNotification>

Response Example (Simplified)
───────────────────────────────────────────────────────────────────────────────
<SignalProcessingNotificationResponse>
  <acquisitionPointInfoList>
    <acquisitionPointInfo>
      <acquisitionSignalID>scte35-event-001</acquisitionSignalID>
      <alternativeList>
        <alternative>
          <duration>PT15S</duration>
          <contentIdentifier>
            <uri>https://cdn.example.com/ads/ad1.mp4</uri>
          </contentIdentifier>
          <trackingEvents>
            <impressionURL>https://tracker.example.com/imp?id=ad1</impressionURL>
            <quartileURL>https://tracker.example.com/q1?id=ad1</quartileURL>
          </trackingEvents>
        </alternative>
        <alternative>
          <duration>PT15S</duration>
          <contentIdentifier>
            <uri>https://cdn.example.com/ads/ad2.mp4</uri>
          </contentIdentifier>
        </alternative>
      </alternativeList>
    </acquisitionPointInfo>
  </acquisitionPointInfoList>
</SignalProcessingNotificationResponse>

Context Parameters
───────────────────────────────────────────────────────────────────────────────
Processor Provides to ADS:
- Content metadata: Title, genre, rating, duration
- Viewer information: Device type, location, user ID (privacy-compliant)
- Opportunity context: Break position, available duration
- Network conditions: Bandwidth, latency
- Session info: Live vs VOD, stream quality
- SCTE-35 details: Event ID, segmentation descriptors

ADS Returns:
- Ad creative URLs (video files)
- Ad duration and sequencing
- Impression tracking pixels/beacons
- Quartile tracking URLs (start, 25%, 50%, 75%, complete)
- Click-through URLs
- Companion banner creative
- Fallback instructions if primary ad unavailable

Integration Architecture
───────────────────────────────────────────────────────────────────────────────
Components:
1. Origin/Packager: Video processing, detects SCTE-35, calls ESAM
2. Ad Decision Server (ADS): Business logic, ad selection
3. Ad Server/SSP: Ad inventory, campaign management
4. CDN: Delivers ad creative to processor
5. Tracking Server: Collects impression/quartile events

Dataflow:
  [Video Stream] → [Packager]
                       ↓ ESAM Request
                   [Ad Decision Server]
                       ↓ Ad URLs
                   [Ad CDN]
                       ↓ Ad Media
                   [Packager] → [Manifest with Ads]
                       ↓
                   [Player]
                       ↓ Tracking Beacons
                   [Analytics]

Related Standards
───────────────────────────────────────────────────────────────────────────────
- SCTE-35: In-stream cue markers (what ESAM processes)
- SCTE-224: Higher-level ad scheduling and management
- VAST/VPAID: Client-side ad serving (complementary to ESAM)
- POIS: Placement Opportunity Information Service (similar concept)

🔧 Troubleshooting Guide
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: ADS not responding or timing out                                 │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Set timeout: 3-5 seconds max (or splice point will be missed)          │
│ ✓ Fallback ads: Configure local slate/house ad for ADS failures          │
│ ✓ Retry logic: Exponential backoff for transient failures                │
│ ✓ Health checks: Monitor ADS availability before relying on it           │
│ ✓ Circuit breaker: Auto-switch to fallback if ADS fails repeatedly       │
│ ✓ Network: Check firewall, DNS, SSL cert validation issues               │
│ ✓ Logging: Enable verbose ESAM request/response logging                  │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Ads not fitting break duration (overfill/underfill)             │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Send accurate duration: Include break_duration from SCTE-35 in request │
│ ✓ ADS logic: Ensure ADS respects requested duration in response          │
│ ✓ Tolerance: Allow ±1 second buffer for segment boundaries               │
│ ✓ Filler content: Use bumpers/slates to fill undersold inventory         │
│ ✓ Early return: Send SCTE-35 return cue if ads end early                 │
│ ✓ Ad pod pacing: Break duration = Σ(ad durations) + transitions          │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Tracking beacons not firing                                     │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Parse response: Extract impressionURL, quartileURL from ESAM response  │
│ ✓ Timing: Fire impression at ad start, quartiles at 25/50/75/100%        │
│ ✓ HTTP method: Usually GET requests with query parameters                │
│ ✓ Async firing: Don't block video playback waiting for beacon response   │
│ ✓ CORS: Server-side beacons don't have CORS issues (vs client-side)      │
│ ✓ Macros: Replace ${TIMESTAMP}, ${CONTENT_ID} in beacon URLs             │
│ ✓ Retry: Failed beacons should be retried (best-effort tracking)         │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Wrong ads served (targeting not working)                        │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Viewer context: Ensure geo, device, user ID passed accurately          │
│ ✓ Content metadata: Include genre, rating, keywords for contextual ads   │
│ ✓ Privacy compliance: Check GDPR/CCPA consent flags before sharing data  │
│ ✓ IP geolocation: Verify IP-to-geo mapping accuracy                      │
│ ✓ Device detection: User-Agent parsing for device type                   │
│ ✓ ADS logs: Check ADS side for targeting rule evaluation                 │
│ ✓ Test mode: Use ADS debug endpoints to see targeting decisions          │
└───────────────────────────────────────────────────────────────────────────┘

⚡ Configuration Best Practices
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Timeout Strategy                                                          │
├───────────────────────────────────────────────────────────────────────────┤
│  Pre-roll time: 4-8 seconds (from SCTE-35 to splice point)               │
│  ESAM request budget: 2-3 seconds max                                     │
│  ├─ Network RTT: ~500ms                                                   │
│  ├─ ADS processing: 1-2 seconds                                           │
│  └─ Buffer: 500ms safety margin                                           │
│                                                                           │
│  Remaining time: 1-5 seconds for ad fetch from CDN                        │
│                                                                           │
│  If timeout exceeded → serve fallback ad immediately                      │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Context Data to Include                                                   │
├───────────────────────────────────────────────────────────────────────────┤
│  ✅ Always Send:                                                          │
│     • Content ID (movie, show, episode)                                   │
│     • Break duration (from SCTE-35 break_duration)                        │
│     • Acquisition signal ID (SCTE-35 event ID)                            │
│     • Timestamp (acquisition time)                                        │
│                                                                           │
│  ✅ Highly Recommended:                                                   │
│     • Geographic location (country, region, DMA)                          │
│     • Device type (smart TV, mobile, desktop)                             │
│     • Stream type (live vs VOD)                                           │
│     • Content genre, rating (G, PG, R)                                    │
│                                                                           │
│  ⚠️  Privacy-Sensitive (check regulations):                              │
│     • User ID / viewer ID                                                 │
│     • Demographics (age, gender)                                          │
│     • Behavioral data (viewing history)                                   │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Error Handling Tiers                                                      │
├───────────────────────────────────────────────────────────────────────────┤
│  Tier 1: ESAM request succeeds → Use returned ads                         │
│  Tier 2: ESAM timeout/500 error → Serve pre-configured house ad           │
│  Tier 3: House ad unavailable → Serve black slate with station ID         │
│  Tier 4: Total failure → Return to program immediately (no ad)            │
│                                                                           │
│  Always log failures for monitoring and alerting!                         │
└───────────────────────────────────────────────────────────────────────────┘

Important Notes
───────────────────────────────────────────────────────────────────────────────
- ESAM is primarily server-side; client never sees ESAM transactions
- Reduces processor complexity by offloading ad logic to specialized servers
- Enables A/B testing and dynamic optimization by ADS
- Supports both synchronous (real-time) and asynchronous (pre-cached) workflows
- XML and JSON encodings both supported; JSON more common in modern implementations
- Timeout handling critical: processor must have fallback if ADS unavailable
- Privacy regulations impact what viewer data can be passed to ADS
- CableLabs maintains specification; implementations vary by vendor
- Complementary to, not a replacement for, SCTE-35
- ESAM v2 added JSON support and simplified some workflows
