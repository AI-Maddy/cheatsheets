═══════════════════════════════════════════════════════════════════════════════
📅 ESNI - Event Scheduling and Notification Interface
═══════════════════════════════════════════════════════════════════════════════

Overview
───────────────────────────────────────────────────────────────────────────────
ESNI (Event Scheduling and Notification Interface) is a CableLabs specification
that defines a standardized API for coordinating scheduled events across video
processing infrastructure. ESNI enables centralized scheduling systems to communicate
event information to distributed video processors, packagers, and other systems that
need to execute time-sensitive operations. Unlike real-time signaling protocols
like ESAM, ESNI focuses on advance scheduling, allowing systems to prepare and
coordinate complex workflows involving multiple components and time zones.

The specification supports various event types including ad breaks, content
transitions, regional blackouts, emergency alerts, and stream quality changes.
ESNI provides mechanisms for creating, updating, and canceling scheduled events,
along with notification delivery to ensure all participating systems maintain
consistent state. This advance coordination improves reliability and reduces
real-time processing burden, particularly valuable for high-scale operations
where last-minute failures can impact large audiences.

Key Features
───────────────────────────────────────────────────────────────────────────────
- RESTful API: HTTP-based event management interface
- Advance scheduling: Events defined hours or days ahead
- Event types: Ads, blackouts, transitions, alerts, configuration changes
- Notification delivery: Push and pull models for event updates
- Event lifecycle: Create, update, cancel, query operations
- Multi-system coordination: Synchronize actions across infrastructure
- Time zone handling: Consistent UTC-based timing
- Event priorities: Handle conflicts and preemption
- Recurrence patterns: Repeating events (daily, weekly)
- Subscription model: Systems subscribe to relevant event types

Event Types
───────────────────────────────────────────────────────────────────────────────
Content Events:
- Program start/end
- Commercial break (ad opportunity)
- Content transition (program to program)
- Chapter markers

Ad Insertion Events:
- Scheduled ad break
- Ad pod configuration
- Ad decision service selection
- Fallback ad instructions

Distribution Events:
- Regional blackout start/end
- Stream quality change (bitrate, resolution)
- Audio track switching
- Closed caption enable/disable

System Events:
- Emergency Alert System (EAS) activation
- Maintenance window
- Configuration reload
- Health check trigger

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. Pre-scheduling ad breaks for live events (sports, awards shows)
2. Coordinating regional blackouts across distribution network
3. Programming emergency alert system tests and activations
4. Scheduling content transitions at broadcast facilities
5. Advance notification of planned maintenance windows
6. Coordinating stream quality changes for major events
7. Scheduling recurring weekly/daily program events
8. Pre-configuring ad decision server selection for shows
9. Synchronizing encoder/packager configuration updates
10. Coordinating multi-region simulcast events

Technical Workflow
───────────────────────────────────────────────────────────────────────────────
Event Creation:
1. Scheduling system creates event via ESNI API
   - POST /esni/events
   - Includes event type, time, target systems, parameters
2. ESNI service validates and stores event
3. ESNI notifies subscribed systems (push or pull)
4. Systems acknowledge receipt and prepare for execution
5. At scheduled time, systems execute event
6. Systems report completion status back to ESNI

Event Update:
1. Scheduling system updates existing event
   - PUT /esni/events/{eventId}
2. ESNI propagates update to affected systems
3. Systems adjust prepared workflows

Event Cancellation:
1. Scheduling system cancels event
   - DELETE /esni/events/{eventId}
2. ESNI notifies all subscribed systems
3. Systems abort preparation and cleanup

API Examples (Conceptual)
───────────────────────────────────────────────────────────────────────────────
Create Scheduled Ad Break:
  POST /esni/events
  {
    "eventType": "ad_break",
    "eventId": "game-12345-break-1",
    "scheduledTime": "2026-01-13T15:30:00Z",
    "duration": 120,
    "targetSystems": ["packager-01", "packager-02"],
    "parameters": {
      "adDecisionServer": "https://ads.example.com/esam",
      "maxAdPods": 4,
      "fallbackSlate": "https://cdn.example.com/slate.mp4"
    },
    "priority": "normal",
    "notifyBefore": 300
  }

Create Regional Blackout:
  POST /esni/events
  {
    "eventType": "blackout",
    "eventId": "blackout-region-45",
    "scheduledTime": "2026-01-13T19:00:00Z",
    "endTime": "2026-01-13T22:00:00Z",
    "targetSystems": ["regional-edge-servers"],
    "parameters": {
      "regions": ["US-CA-SF", "US-CA-LA"],
      "contentId": "espn-game-789",
      "replacementContent": "https://cdn.example.com/alternate-programming.m3u8"
    }
  }

Query Upcoming Events:
  GET /esni/events?start=2026-01-13T00:00:00Z&end=2026-01-14T00:00:00Z&type=ad_break

  Response:
  {
    "events": [
      {
        "eventId": "game-12345-break-1",
        "eventType": "ad_break",
        "scheduledTime": "2026-01-13T15:30:00Z",
        "status": "scheduled",
        "targetSystems": ["packager-01", "packager-02"],
        "acknowledgedBy": ["packager-01", "packager-02"]
      }
    ]
  }

Notification Model
───────────────────────────────────────────────────────────────────────────────
Push (Webhook):
- Systems register webhook URLs
- ESNI pushes event notifications to registered endpoints
- Immediate notification delivery
- Requires systems to expose HTTP endpoint

Pull (Polling):
- Systems periodically query ESNI for new/updated events
- GET /esni/events?since=<lastQueryTime>
- Simpler integration, higher latency
- No inbound firewall requirements

Hybrid:
- Push for critical/high-priority events
- Pull for routine/low-priority events
- Fallback to pull if push fails

Event Status Tracking
───────────────────────────────────────────────────────────────────────────────
Lifecycle States:
- scheduled: Event created, waiting for execution time
- acknowledged: Target systems confirmed receipt
- preparing: Systems preparing for event execution
- executing: Event in progress
- completed: Event successfully executed
- failed: Event execution failed
- canceled: Event canceled before execution

Status Reporting:
- Systems report status updates to ESNI
- ESNI aggregates status across all target systems
- Monitoring dashboards consume ESNI status API

Integration Architecture
───────────────────────────────────────────────────────────────────────────────
  [Traffic/Scheduling System]
          ↓
      [ESNI Service]
          ↓
   ┌──────┴──────┬──────────┬────────┐
   ↓             ↓          ↓        ↓
[Packagers]  [Encoders]  [CDN]  [Ad Servers]

ESNI acts as central coordinator:
- Receives schedules from traffic systems
- Distributes to all relevant infrastructure
- Tracks acknowledgment and execution
- Provides status visibility

Benefits
───────────────────────────────────────────────────────────────────────────────
- Advance coordination: Systems prepare ahead of time
- Reduced real-time failures: Pre-validation and preparation
- Centralized scheduling: Single source of truth
- Multi-system synchronization: Consistent event execution
- Auditability: Event history and status tracking
- Flexibility: Update/cancel events if plans change
- Scalability: Broadcast to many systems efficiently
- Visibility: Operational dashboards for event monitoring

ESNI vs ESAM vs POIS
───────────────────────────────────────────────────────────────────────────────
ESNI:
- Focus: Scheduled event coordination
- Timing: Hours to days in advance
- Direction: Scheduler → Infrastructure
- Use: Preparation, resource allocation

ESAM:
- Focus: Real-time ad decisions
- Timing: Seconds before execution
- Direction: Processor ↔ Ad Server
- Use: Dynamic ad selection

POIS:
- Focus: Opportunity discovery
- Timing: Minutes to hours ahead
- Direction: Ad System → Opportunity Service
- Use: Inventory query, campaign planning

Relationship:
  ESNI schedules the event → POIS provides opportunity metadata → ESAM executes insertion

Challenges
───────────────────────────────────────────────────────────────────────────────
- Live content timing: Scheduled times may shift for live events
- System failures: Handling systems that don't acknowledge or fail
- Time synchronization: Ensuring all systems have accurate clocks (NTP critical)
- Event conflicts: Resolving overlapping or conflicting events
- Scale: Managing thousands of events for large networks
- Network partitions: Ensuring event delivery despite connectivity issues

Important Notes
───────────────────────────────────────────────────────────────────────────────
- ESNI is part of the CableLabs content delivery ecosystem
- Designed for large-scale IPTV, cable, and streaming operations
- All times should be UTC to avoid time zone confusion
- Systems must implement NTP synchronization for accurate timing
- Event IDs must be unique across the scheduling domain
- Notification delivery should be idempotent (safe to receive duplicates)
- Critical for high-reliability operations (live sports, breaking news)
- Enables "lights out" automated workflows with minimal human intervention
- Complementary to real-time signaling, not a replacement
- Adoption varies; more common in MSO and large streaming platforms
