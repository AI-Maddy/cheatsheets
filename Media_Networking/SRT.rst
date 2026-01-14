═══════════════════════════════════════════════════════════════════════════════
🔐 SRT - Secure Reliable Transport 🚀
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **S**uper **R**eliable **T**ransport = Your video's bodyguard! 🛡️
    Think: "SRT = Security + Reliability + Transport" 🔒📦🚚

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔵 OVERVIEW - The Internet's Video Superhighway                            │
└─────────────────────────────────────────────────────────────────────────────┘

SRT is an **open-source, UDP-based protocol** for low-latency video transport over unpredictable networks. The superhero protocol that combines encryption, packet recovery, and bandwidth optimization.

🎯 **Think of it as**: A luxury armored vehicle for your video! It's fast (UDP), secure (AES encryption), and self-healing (ARQ+FEC)!

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⭐ KEY FEATURES - The Triple Threat!                                        │
└─────────────────────────────────────────────────────────────────────────────┘

🚀 **Low Latency**: Typically 2-8 seconds (configurable)
   └─ 💡 Memory: "SRT = Speedy Real-Time" - Fast enough for live sports!

🔄 **ARQ + FEC**: Hybrid error correction
   └─ 💡 Think: "Double protection" = Ask for retransmits AND preemptive fixes!

🔒 **AES-128/256 Encryption**: Built-in security
   └─ 💡 Remember: "Lock box" emoji = Your video is Fort Knox secure!

🎛️ **Congestion Control**: Adapts to network conditions
   └─ 💡 Smart cruise control for video - speeds up/slows down automatically

🧱 **Firewall Traversal**: Rendezvous mode for NAT
   └─ 💡 "Ninja mode" - sneaks through firewalls like a pro!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎬 COMMON USE CASES - Where SRT Shines                                     │
└─────────────────────────────────────────────────────────────────────────────┘

1. 🏟️ **Live sports contribution** over public internet
   └─ Stadium → Broadcast center (replacing expensive satellite trucks!)

2. 🎥 **Remote production workflows**
   └─ REMI (Remote Integration Model) - operators stay home

3. ☁️ **Cloud encoder/decoder connections**
   └─ AWS, Azure, GCP → Seamless cloud workflows

4. 🆘 **Disaster recovery backhaul**
   └─ When your fiber goes down, SRT saves the day!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📐 BASIC CONFIGURATION - SRT Connection Modes                              │
└─────────────────────────────────────────────────────────────────────────────┘

**🎧 Listener Mode (receiver)**::

    srt://0.0.0.0:9000?mode=listener&latency=200

    💡 Memory: "Listener = Waits for calls" (like answering phone)

**📞 Caller Mode (sender)**::

    srt://192.168.1.100:9000?mode=caller&latency=200&passphrase=mysecret

    💡 Memory: "Caller = Makes the call" (dialing a phone)

**🤝 Rendezvous Mode (both sides)**::

    srt://10.0.1.50:9000?mode=rendezvous&latency=150

    💡 Memory: "Rendezvous = Secret meeting spot" (both arrive independently!)

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎛️ IMPORTANT PARAMETERS - Tuning Your SRT Stream                           │
└─────────────────────────────────────────────────────────────────────────────┘

🔹 **latency**: Buffer time in milliseconds (default 120ms)
   └─ 💡 Higher latency = More time to recover lost packets
   └─ Sweet spot: 200-500ms for internet, 50-120ms for LAN

🔹 **maxbw**: Maximum bandwidth limit
   └─ 💡 Prevents SRT from hogging your entire connection

🔹 **pbkeylen**: Encryption key length (16, 24, 32 bytes)
   └─ 💡 Remember: 16=128-bit, 24=192-bit, 32=256-bit AES

🔹 **passphrase**: Pre-shared encryption key
   └─ 💡 Like your Wi-Fi password - keep it secret, keep it safe!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏆 ADVANTAGES - Why SRT Beats Traditional Methods                          │
└─────────────────────────────────────────────────────────────────────────────┘

✅ **No dedicated circuits required** (works over internet)
   └─ 🚫 Goodbye expensive MPLS/fiber leases!

✅ **Recovers from 10-15% packet loss gracefully**
   └─ 💡 Even sketchy hotel Wi-Fi can work!

✅ **Lower cost than satellite or fiber**
   └─ 💰 Save thousands per month on contribution links

✅ **Open standard** (no licensing fees)
   └─ 🆓 Free and open-source forever!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔴 TROUBLESHOOTING - Common SRT Issues & Fixes                             │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: ❌ Connection fails immediately
└─ 🔍 **Check**: Firewall blocking UDP port
   └─ **Solution**: Open UDP port on both ends, try rendezvous mode

**Problem**: ❌ Video stuttering/freezing
└─ 🔍 **Check**: Latency too low for network conditions
   └─ **Solution**: Increase latency parameter (try 500ms+)

**Problem**: ❌ High CPU usage
└─ 🔍 **Check**: Encryption overhead on weak hardware
   └─ **Solution**: Use AES-128 instead of 256, or disable encryption

**Problem**: ❌ "Passphrase mismatch" error
└─ 🔍 **Check**: Sender/receiver passphrase don't match
   └─ **Solution**: Verify exact same passphrase on both sides

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE - Visual Story to Remember SRT                            │
└─────────────────────────────────────────────────────────────────────────────┘

Imagine a **🚚 Armored Delivery Truck on the Highway**:

1. **🔒 Armored truck** = Encryption (AES-256, impenetrable!)
2. **📦 Packages with bubble wrap** = FEC (preemptive protection)
3. **📞 Truck radio** = ARQ (calls back: "Package 47 missing!")
4. **🚗 Cruise control** = Bandwidth adaptation (smart speed)
5. **🗺️ GPS rerouting** = NAT traversal (finds alternate routes)
6. **⏱️ Delivery window** = Latency buffer (time to handle issues)

**Story**: Your video is precious cargo in an armored truck. If a package bounces out (packet loss), the driver radios back for a replacement (ARQ). The bubble wrap protects fragile items (FEC). The truck adapts speed to traffic (congestion control). Even if roads are blocked, GPS finds a way through (firewall traversal)!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 PRO TIPS - Expert SRT Secrets                                           │
└─────────────────────────────────────────────────────────────────────────────┘

🔸 **Start with high latency (500ms), then tune down** - Better safe than sorry!
🔸 **Use rendezvous mode for NAT scenarios** - Both sides behind firewalls? No problem!
🔸 **Monitor SRT stats** (packet loss, RTT, bandwidth) - Knowledge is power!
🔸 **Combine with RIST for multi-source failover** - Ultimate reliability!
🔸 **Test on bad networks first** - If it works on hotel Wi-Fi, it'll work anywhere!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎯 QUICK REFERENCE - SRT Cheat Sheet                                       │
└─────────────────────────────────────────────────────────────────────────────┘

**Common Latency Values**:
  - LAN: 50-120ms 🏠
  - Regional Internet: 200-500ms 🌐
  - Transcontinental: 500-1000ms 🌍
  - Satellite/Mobile: 1000-2000ms 🛰️

**Port Recommendations**:
  - Default: 9000 (but any UDP port works)
  - Production: Use non-standard ports (security through obscurity)

**When to Use SRT**:
  ✅ Live contribution over public internet
  ✅ Remote production workflows
  ✅ Cloud-based encoding
  ✅ Backup connectivity
  ❌ Local studio (use ST 2110 instead - no compression needed!)
