═══════════════════════════════════════════════════════════════════════════════
📋 POIS - Placement Opportunity Information Service
═══════════════════════════════════════════════════════════════════════════════

Overview
───────────────────────────────────────────────────────────────────────────────
POIS (Placement Opportunity Information Service) is a standardized interface
specification developed by CableLabs for communicating ad placement opportunities
and content metadata between video processing systems and ad management platforms.
Part of the broader content preparation and ad insertion ecosystem, POIS provides
a consistent API for querying and exchanging information about ad breaks, content
segmentation, and scheduling data, enabling coordinated decision-making across
distributed video infrastructure.

POIS operates at a higher abstraction level than SCTE-35 markers, focusing on
placement opportunity metadata rather than low-level splice commands. It allows
ad management systems to query upcoming ad opportunities, retrieve content context,
and coordinate multi-platform ad campaigns. POIS is particularly valuable in complex
workflows involving multiple video processors, regional variations, and advanced
targeting scenarios where centralized opportunity management improves efficiency
and consistency across distribution networks.

Key Features
───────────────────────────────────────────────────────────────────────────────
- RESTful API: HTTP-based query and response protocol
- Opportunity metadata: Detailed info about ad placement points
- Content context: Program information, genre, ratings
- Timing information: Start times, durations, pre-roll windows
- Regional variations: Support for geo-specific opportunities
- Schedule lookups: Query future placement opportunities
- Audience targeting data: Demographics and segmentation hints
- Multi-platform support: Coordinate opportunities across delivery methods
- SCTE-35 correlation: Maps to underlying cue markers
- Real-time updates: Push notifications for schedule changes

POIS Data Elements
───────────────────────────────────────────────────────────────────────────────
Placement Opportunity:
- Unique opportunity ID
- Start time (absolute or relative)
- Duration/available time
- Position within program (pre-roll, mid-roll, post-roll)
- Break number and total breaks
- Content context (before/after opportunity)
- Allowed ad formats and restrictions

Content Metadata:
- Program title, episode, season
- Content ID (EIDR, Ad-ID, etc.)
- Genre and sub-genre
- Ratings (TV-Y, TV-PG, TV-14, etc.)
- Target audience demographics
- Keywords and tags

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. Multi-platform ad opportunity synchronization
2. Advance ad opportunity discovery for programmatic buying
3. Content scheduling systems querying placement inventory
4. Ad sales systems checking available inventory
5. Cross-regional ad opportunity management
6. VOD content preparation with embedded opportunities
7. Dynamic ad pod optimization across platforms
8. Coordination between linear and streaming ad breaks
9. Pre-caching ad decisions for high-traffic events
10. Audience-based opportunity segmentation

💡 Memory Aid
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: POIS as Real Estate Listing Service                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of ad placement opportunities as COMMERCIAL REAL ESTATE:           │
│                                                                           │
│  🏢 [POIS] = Real Estate Listing Website (Zillow for ad inventory)       │
│                                                                           │
│  📋 Listings show AVAILABLE PROPERTIES (ad opportunities):                │
│     • Location: "Lakers vs Celtics, halftime" (content context)           │
│     • Lot size: "60 seconds available" (duration)                         │
│     • Zoning: "Sports fans, 18-49" (target audience)                      │
│     • Available: "January 15, 8:30 PM EST" (start time)                  │
│     • Neighborhood: "Premium live sports" (content tier)                  │
│                                                                           │
│  🏗️ [Ad Sales/DSP] = Real Estate Investors:                             │
│     Browse listings, evaluate properties, make offers                     │
│                                                                           │
│  vs.                                                                      │
│                                                                           │
│  🏪 [ESAM] = Real Estate Agent at Open House:                            │
│     Only shows up when buyer is at doorstep (real-time decisioning)       │
│                                                                           │
│  POIS gives you the FULL CATALOG to plan ahead.                           │
│  ESAM gives you the KEYS when it's time to move in.                       │
│                                                                           │
│  POIS = "What inventory exists?" (hours/days ahead)                       │
│  ESAM = "Which ad right now?" (seconds before insertion)                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

📅 Opportunity Discovery Timeline
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ POIS-Enabled Planning vs Real-Time-Only Decisioning                      │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  T-24 hours         T-4 hours          T-4 seconds       T=0             │
│   │                    │                   │              │               │
│   │ WITHOUT POIS (Real-Time Only):                                        │
│   │                    │                   │              │               │
│   │                    │                   │              └─► 🔔 SCTE-35  │
│   │                    │                   │                  ↓           │
│   │                    │                   │                  ESAM query  │
│   │                    │                   │                  ↓           │
│   │                    │                   │                  ADS decides │
│   │                    │                   │                  (3 sec)     │
│   │                    │                   │                  ↓           │
│   │                    │                   │                  😰 PANIC!   │
│   │                    │                   │                  Limited     │
│   │                    │                   │                  options     │
│                                                                           │
│  ═══════════════════════════════════════════════════════════════════════  │
│                                                                           │
│   │ WITH POIS (Advance Planning):                                         │
│   │                    │                   │              │               │
│   └─► 📊 POIS Query   │                   │              │               │
│        "Show upcoming opportunities"       │              │               │
│        ↓               │                   │              │               │
│        Ad sales sees   │                   │              │               │
│        inventory       │                   │              │               │
│        ↓               │                   │              │               │
│        Pre-sell ads    │                   │              │               │
│        Campaign setup  │                   │              │               │
│                        ↓                   │              │               │
│                        ADS pre-caches      │              │               │
│                        ad decisions        │              │               │
│                                            │              │               │
│                                            └─► ESAM       └─► 🔔 SCTE-35  │
│                                                gets           ↓           │
│                                                pre-made       Execute     │
│                                                decision       instantly!  │
│                                                (100ms)        😌 Smooth   │
│                                                                           │
│  Result: Better fill rates, higher CPMs, faster execution                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

⚡ POIS API Query Examples
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Query 1: Find opportunities in next 2 hours for specific channel         │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  GET /pois/opportunities?channel=ESPN&                                    │
│      start=2026-01-13T10:00:00Z&                                          │
│      end=2026-01-13T12:00:00Z                                             │
│                                                                           │
│  Response:                                                                │
│  {                                                                        │
│    "opportunities": [                                                    │
│      {                                                                    │
│        "id": "opp-12345",                                                │
│        "startTime": "2026-01-13T10:15:30Z",                             │
│        "duration": 90,         ← 90 seconds available                    │
│        "position": "mid-roll", ← Within program                          │
│        "contentId": "espn-lakers-celtics",                              │
│        "contentTitle": "Lakers vs Celtics",                             │
│        "genre": "Sports",                                               │
│        "rating": "TV-G",                                                │
│        "targetAudience": ["adults-18-49", "sports-fans"],              │
│        "availNumber": 2,       ← 2nd ad break in program                 │
│        "availsInBreak": 3,     ← 3 total breaks                          │
│        "estimatedViewers": 250000                                        │
│      },                                                                   │
│      ...                                                                  │
│    ]                                                                      │
│  }                                                                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Query 2: Get content metadata for ad targeting                           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  GET /pois/content/espn-lakers-celtics                                    │
│                                                                           │
│  Response:                                                                │
│  {                                                                        │
│    "contentId": "espn-lakers-celtics",                                  │
│    "title": "Lakers vs Celtics",                                        │
│    "genre": "Sports",                                                   │
│    "subGenre": "Basketball",                                            │
│    "rating": "TV-G",                                                    │
│    "duration": 9000,          ← 2.5 hours in seconds                     │
│    "live": true,                                                         │
│    "adBreaks": [               ← Planned ad break schedule               │
│      {                                                                    │
│        "position": "pre-roll",                                          │
│        "duration": 60,         ← 1 minute pre-game                       │
│        "estimatedTime": "2026-01-13T10:00:00Z"                          │
│      },                                                                   │
│      {                                                                    │
│        "position": "mid-roll-1",                                        │
│        "timestamp": 1800,      ← 30 min into game (timeout)              │
│        "duration": 90                                                    │
│      },                                                                   │
│      {                                                                    │
│        "position": "halftime",                                          │
│        "timestamp": 5400,      ← ~90 min mark                            │
│        "duration": 300         ← 5 minutes! (premium inventory)          │
│      },                                                                   │
│      {                                                                    │
│        "position": "post-roll",                                         │
│        "duration": 60                                                    │
│      }                                                                    │
│    ],                                                                     │
│    "keywords": ["NBA", "basketball", "live-sports", "prime-time"],    │
│    "demographics": {                                                     │
│      "primaryAge": "18-49",                                             │
│      "genderSplit": {"male": 65, "female": 35}                         │
│    }                                                                      │
│  }                                                                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Query 3: Reserve specific opportunity (programmatic buying)              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  POST /pois/opportunities/opp-12345/reserve                               │
│  {                                                                        │
│    "buyerId": "ad-network-xyz",                                         │
│    "campaignId": "campaign-789",                                        │
│    "bidAmount": 25.00,         ← $25 CPM bid                             │
│    "duration": 30,              ← Want 30s of the 90s available          │
│    "targetingConfirmed": true                                            │
│  }                                                                        │
│                                                                           │
│  Response:                                                                │
│  {                                                                        │
│    "reservationId": "res-54321",                                        │
│    "status": "confirmed",                                               │
│    "expiresAt": "2026-01-13T10:00:00Z",  ← Must confirm by this time   │
│    "remainingDuration": 60     ← 60s still available for other buyers   │
│  }                                                                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Technical Workflow
───────────────────────────────────────────────────────────────────────────────
Query-Based:
1. Ad management system queries POIS for upcoming opportunities
   - Specifies time range, content, region
2. POIS returns list of placement opportunities with metadata
3. Ad system evaluates opportunities against campaigns
4. Ad system reserves or bids on specific opportunities
5. When opportunity occurs, ESAM/processor executes insertion

Push-Based:
1. POIS monitors content schedule and SCTE-35 streams
2. POIS identifies placement opportunities in advance
3. POIS notifies subscribed ad management systems
4. Systems prepare ad decisions before real-time execution
5. Reduces latency at insertion time

API Examples (Conceptual)
───────────────────────────────────────────────────────────────────────────────
Query Opportunities:
  GET /pois/opportunities?start=2026-01-13T10:00:00Z&end=2026-01-13T11:00:00Z&channel=ESPN

Response:
  {
    "opportunities": [
      {
        "id": "opp-12345",
        "startTime": "2026-01-13T10:15:30Z",
        "duration": 90,
        "position": "mid-roll",
        "contentId": "espn-game-456",
        "contentTitle": "Lakers vs Celtics",
        "genre": "Sports",
        "rating": "TV-G",
        "targetAudience": ["adults-18-49", "sports-fans"],
        "availNumber": 2,
        "availsInBreak": 3
      },
      ...
    ]
  }

Query Content Metadata:
  GET /pois/content/espn-game-456

Response:
  {
    "contentId": "espn-game-456",
    "title": "Lakers vs Celtics",
    "genre": "Sports",
    "subGenre": "Basketball",
    "rating": "TV-G",
    "duration": 9000,
    "adBreaks": [
      {"position": "pre-roll", "duration": 60},
      {"position": "mid-roll-1", "timestamp": 1800, "duration": 90},
      {"position": "mid-roll-2", "timestamp": 3600, "duration": 90},
      {"position": "post-roll", "duration": 60}
    ],
    "keywords": ["NBA", "basketball", "live-sports"]
  }

Integration with Other Systems
───────────────────────────────────────────────────────────────────────────────
POIS ← Content Management System:
- Ingests program schedules
- Extracts metadata from EPG (Electronic Program Guide)
- Identifies planned ad breaks from rundowns

POIS → Ad Management/DSP:
- Exposes opportunities for bidding
- Provides context for targeting
- Enables advance reservation of inventory

POIS ↔ ESAM/Processor:
- Correlates opportunities with SCTE-35 events
- Validates timing and duration
- Confirms execution of planned opportunities

POIS vs ESAM
───────────────────────────────────────────────────────────────────────────────
POIS:
- Focus: Opportunity metadata and discovery
- Timing: Advance queries, minutes to hours ahead
- Use: Planning, inventory management, campaign setup
- Abstraction: High-level business concepts

ESAM:
- Focus: Real-time ad decision execution
- Timing: Seconds before insertion point
- Use: Dynamic insertion, creative selection
- Abstraction: Technical signaling and stitching

Relationship:
  POIS provides "what opportunities exist"
  ESAM provides "which ads to insert now"
  Systems often use both: POIS for planning, ESAM for execution

Architecture Patterns
───────────────────────────────────────────────────────────────────────────────
Centralized:
- Single POIS instance for entire network
- Aggregates opportunities from all sources
- Provides unified view to ad systems

Distributed:
- Regional POIS instances
- Federated queries across regions
- Localized opportunity management

Hybrid:
- Central POIS for planning
- Edge POIS for real-time execution
- Synchronization between tiers

Benefits
───────────────────────────────────────────────────────────────────────────────
- Advance visibility: Ad systems see opportunities ahead of time
- Better targeting: Rich metadata enables sophisticated decisions
- Inventory optimization: Prevent underselling or overselling
- Multi-platform consistency: Same opportunities across delivery methods
- Programmatic efficiency: Automated opportunity discovery
- Reduced latency: Pre-cached decisions execute faster
- Standardization: Vendor-neutral interface

Challenges
───────────────────────────────────────────────────────────────────────────────
- Live content: Opportunities may shift due to live events
- Synchronization: Keeping POIS data current across systems
- Granularity: Balancing detail vs simplicity
- Privacy: Managing viewer data in compliance with regulations
- Scale: High query volumes during peak events

Important Notes
───────────────────────────────────────────────────────────────────────────────
- POIS is complementary to SCTE-35 and ESAM, not a replacement
- CableLabs specification; implementations vary by vendor
- More commonly deployed in large-scale IPTV and streaming operations
- JSON is typical encoding format for modern implementations
- Often integrated with content scheduling and traffic systems
- Enables "programmatic TV" by exposing inventory like web display ads
- Future evolution may include real-time bidding protocol integration
- Success depends on accurate content metadata from upstream systems
- Can reduce load on real-time ad decision systems by pre-filtering opportunities
