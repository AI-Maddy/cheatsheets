ARINC 825 / CAN in avionics
===========================

**Domain:** Avionics

**Description:**
Adapted CAN for aerospace applications.

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">✈️🚌 ARINC 825 / CAN in Avionics</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Avionics</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"CAN for the Clouds"</span><br>
	<b>Icon:</b> ✈️🚌<br>
	</div>

**Key Features:**
- 🚌 Based on CAN (Controller Area Network)
- ✈️ Adapted for aerospace reliability and redundancy
- 🔄 Supports deterministic, real-time communication
- 🛡️ Enhanced error detection and fault tolerance

**Physical/Electrical Layer:**
- 🔌 Differential signaling (twisted pair)
- ⚡ Data rates: up to 1 Mbps (CAN), higher for CAN FD

**Topology:**
- 🌐 Bus topology

**Use Cases:**
- ✈️ Avionics subsystems (sensors, actuators, displays)
- 🛫 Redundant and safety-critical communication

**Pros:**
- 🛡️ Robust, proven CAN technology
- 🔁 Supports redundancy and error handling

**Cons:**
- 🐢 Limited bandwidth compared to Ethernet
- 🏗️ Not as widely adopted as ARINC 429/664

**Standard:**
- 📜 ARINC Specification 825

**Typical Applications:**
- ✈️ Modern and retrofit avionics systems

**Memorization Tip:**
<span style="color:#1976d2;">Think of ARINC 825 as "CAN with wings"—the trusted bus for aircraft electronics!</span>

.. raw:: html

	<div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	<b>Quick Visual:</b> <span style="font-size:1.5em;">✈️ &rarr; 🚌 &rarr; 🛡️</span><br>
	<i>Aircraft systems talk safely on a CAN-based bus!</i>
	</div>

.. raw:: html

	 <div style="background-color:#e8f5e9; border-radius:10px; padding:14px; margin-top:18px;">
	 <b>🛠️ Practical Example:</b><br>
	 <pre style="background:#f5f5f5; border-radius:6px; padding:8px;">Sensor (Landing Gear) ──▶ CAN Node ──▶ [Twisted Pair] ──▶ CAN Node (Flight Computer)
	 </pre>
	 <i>Landing gear sensor transmits status to the flight computer using ARINC 825 CAN protocol.</i>
	 </div>

**Troubleshooting Tips:**
- Check for correct bus termination (120Ω at each end)
- Inspect for wiring faults or shorts
- Use CAN analyzers to monitor message traffic and error frames
- Confirm node IDs and bit timing settings

**Security Considerations:**
- No built-in encryption; use secure physical access
- Monitor for unauthorized devices or spoofed messages
- Employ redundancy and error detection for safety

**Comparison Table:**

.. list-table:: ARINC 429 vs. ARINC 825 vs. ARINC 664
	 :header-rows: 1
	 :widths: 20 20 20 20

	 * - Feature
		 - ARINC 429
		 - ARINC 825
		 - ARINC 664
	 * - Data Rate
		 - 12.5/100 kbps
		 - 1 Mbps (CAN)
		 - 100 Mbps/1 Gbps
	 * - Use Case
		 - Sensor data
		 - Subsystem comms
		 - High-bandwidth networking
	 * - Topology
		 - Point-to-point
		 - Bus
		 - Switched star

**Popular Tools:**
- Vector CANalyzer/ARINC 825 Option
- Kvaser CAN Bus Tools
- AIM ARINC 825 Analyzer

.. raw:: html

	 <div style="background-color:#e1bee7; border-radius:10px; padding:12px; margin-top:18px;">
	 <b>🧠 Memorization Mnemonic:</b> <span style="color:#6a1b9a;">"ARINC 825 is CAN with wings—the trusted bus for aircraft electronics!"</span>
	 </div>
