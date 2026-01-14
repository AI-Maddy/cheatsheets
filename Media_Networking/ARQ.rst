═══════════════════════════════════════════════════════════════════════════════
🔄 ARQ - Automatic Repeat reQuest 📞
═══════════════════════════════════════════════════════════════════════════════

💡 **Memory Aid**: **A**sk **R**etransmit **Q**uickly = "Can you repeat that?" 🔁
    Think: "ARQ = Always Requesting (when packets are) ❌ Missing"

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔵 OVERVIEW - The "Repeat After Me" Protocol                               │
└─────────────────────────────────────────────────────────────────────────────┘

ARQ is an **error correction technique** where the receiver detects missing or corrupted packets and requests retransmission from the sender. Used in protocols like SRT, Zixi, and TCP.

🎯 **Think of it as**: A phone conversation - "Sorry, I didn't catch that. Can you say it again?" ☎️

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⭐ KEY FEATURES - Smart Retransmission System                               │
└─────────────────────────────────────────────────────────────────────────────┘

🎯 **Selective Retransmission**: Only missing packets are resent
   └─ 💡 Memory: "Cherry-picking" - Only grab what you need!

✅ **Acknowledgments (ACKs)**: Receiver confirms receipt
   └─ 💡 Like email read receipts - "Got it, thanks!"

❌ **Negative Acknowledgments (NAKs)**: Receiver requests specific packets
   └─ 💡 "Hey, I'm missing packet #47!" - Direct request

⏱️ **Latency Trade-off**: Adds delay for reliability
   └─ 💡 Speed vs Accuracy - Can't have both perfection AND instant!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎭 ARQ TYPES - Three Flavors of Retransmission                             │
└─────────────────────────────────────────────────────────────────────────────┘

1. 🐌 **Stop-and-Wait ARQ**
   - Sender waits for ACK before sending next packet
   - Simple but slow (not used in video)
   - 💡 Memory: "Wait for applause before next line" (theatrical!)

2. ⏪ **Go-Back-N ARQ**
   - Receiver discards all packets after error
   - Retransmits from error point forward
   - Wasteful for high packet loss
   - 💡 Memory: "Rewind the whole tape" (wasteful!)

3. ⚡ **Selective Repeat ARQ** (Used in SRT/Zixi) ⭐
   - Only retransmits missing packets
   - Most efficient for video
   - 💡 Memory: "Surgical strike" - Target only what's broken!

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🥊 ARQ vs FEC - The Battle of Error Correction                             │
└─────────────────────────────────────────────────────────────────────────────┘

+--------------------+----------------------+----------------------+
| Feature            | 🔄 ARQ               | 🛡️ FEC               |
+====================+======================+======================+
| Latency            | ⏱️ Higher (RTT delay) | ⚡ Lower (proactive) |
| Efficiency         | 🎯 Precise recovery   | 📦 Some overhead     |
| Network Overhead   | 💰 Low (only losses)  | 💸 Always adds data  |
| Best For           | 🌐 Stable RTT         | 🌪️ Unpredictable     |
| Bidirectional?     | ✅ Yes (needs feedback)| ❌ No (one-way OK)   |
+--------------------+----------------------+----------------------+

💡 **Memory Rule**: "ARQ = Reactive (fix after), FEC = Proactive (fix before)"

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📡 EXAMPLE: SRT ARQ FLOW - See It In Action!                               │
└─────────────────────────────────────────────────────────────────────────────┘

::

    Sender                          Receiver
      |                                |
      |-------- 📦 Packets 1-10 ----->|  (All sent!)
      |                                |
      |<------- ✅ ACK (1-7, 9-10) ----|  (❌ Packet 8 missing!)
      |                                |
      |-------- 🔄 Retransmit 8 ----->|  (Resend only #8)
      |                                |
      |<------- ✅ ACK (1-10) ---------|  (Perfect! All received)

💡 **Memory Story**: "Lost package #8? Send ONLY #8 again - don't resend 1-7!"

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎬 COMMON USE CASES - Where ARQ Shines                                     │
└─────────────────────────────────────────────────────────────────────────────┘

1. 🔐 **SRT protocol** (primary recovery mechanism)
   └─ Live sports contribution over internet

2. 📡 **Zixi reliable transport**
   └─ Broadcast-grade contribution feeds

3. 📁 **File transfer protocols** (FTP, HTTP)
   └─ Downloads that must be 100% perfect

4. 🌐 **TCP retransmission**
   └─ Web browsing, email, everything reliable!

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚠️ IMPORTANT NOTES - Critical ARQ Facts                                    │
└─────────────────────────────────────────────────────────────────────────────┘

📞 **Requires bidirectional communication** (back-channel)
   └─ Can't work if receiver can't talk back!

📡 **Not suitable for multicast** (no feedback channel)
   └─ How can 1000 receivers all send ACKs?

⏱️ **Latency increases with RTT** (round-trip time)
   └─ Satellite link (500ms RTT) = painful ARQ!

🤝 **Often combined with FEC** for hybrid approach
   └─ Best of both worlds: FEC handles common losses, ARQ fixes rare ones

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE - Visual Story for ARQ                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Imagine a **📚 Teacher Calling Roll**:

1. **📢 Teacher calls names** = Sender transmits packets 1-10
2. **✋ Students raise hands** = ACKs ("I'm here!")
3. **❓ "Where's Johnny?"** = Missing packet #8 detected
4. **📞 Call Johnny's phone** = NAK request for packet #8
5. **🏃 Johnny runs to class** = Retransmission of packet #8
6. **✅ Full attendance!** = All packets received

**Story**: The teacher (sender) calls roll (sends packets). Most students answer (ACK), but Johnny is missing (lost packet). Teacher notices the gap and calls Johnny's phone (NAK). Johnny rushes to class (retransmit). Now everyone is present! The key: Only Johnny had to come back, not the whole class.

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔴 TROUBLESHOOTING - ARQ Issues & Solutions                                │
└─────────────────────────────────────────────────────────────────────────────┘

**Problem**: ❌ High latency on ARQ streams
└─ 🔍 **Check**: RTT (round-trip time) too high
   └─ **Solution**: Add FEC, reduce RTT, or increase buffer

**Problem**: ❌ ARQ requests flood the network
└─ 🔍 **Check**: Packet loss > 10%
   └─ **Solution**: ARQ can't keep up - add FEC or fix network!

**Problem**: ❌ Retransmissions arrive too late
└─ 🔍 **Check**: Buffer/latency too small
   └─ **Solution**: Increase latency window in SRT config

**Problem**: ❌ ARQ doesn't work at all
└─ 🔍 **Check**: Firewall blocking return path
   └─ **Solution**: Ensure bidirectional UDP connectivity

┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 PRO TIPS - Master ARQ                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

🔹 **Combine ARQ + FEC** for ultimate reliability (hybrid approach)
🔹 **Monitor retransmission rate** - High rate = network issues!
🔹 **Set proper latency buffers** - Too small = ARQ can't catch up
🔹 **ARQ useless for multicast** - Use FEC-only for one-to-many
🔹 **Watch your RTT** - High RTT (>100ms) makes ARQ sluggish

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎯 QUICK REFERENCE - ARQ Cheat Sheet                                       │
└─────────────────────────────────────────────────────────────────────────────┘

**ARQ Perfect For**:
  ✅ Unicast video streaming (SRT, Zixi)
  ✅ Stable internet connections
  ✅ When 100% reliability needed
  ✅ Low to moderate packet loss (<10%)

**ARQ NOT Good For**:
  ❌ Multicast/broadcast
  ❌ Very high packet loss (>15%)
  ❌ Extremely low latency requirements (<50ms)
  ❌ Satellite links (500+ ms RTT)

**Typical ARQ Overhead**:
  - Low loss (<1%): <5% overhead
  - Moderate (1-5%): 5-15% overhead
  - High (>5%): 15-30%+ overhead
