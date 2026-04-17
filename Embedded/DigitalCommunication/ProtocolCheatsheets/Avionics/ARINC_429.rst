ARINC 429
=========

**Domain:** Avionics

**Description:**
The classic unidirectional, point-to-point data bus standard (most common in commercial/transport aircraft for sensor data like altitude, speed, heading).

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">✈️🔗 ARINC 429</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Avionics</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"A Reliable INterface for Cockpits"</span><br>
	<b>Icon:</b> ✈️🔗<br>
	</div>

**Key Features:**

.. raw:: html

	 <div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	 <b>Quick Visual:</b> <span style="font-size:1.5em;">✈️ &rarr; 🔗 &rarr; 📊</span><br>
	 <i>Plane sends data down a dedicated wire—no traffic jams!</i>
	 </div>

.. raw:: html

	 <div style="background-color:#e8f5e9; border-radius:10px; padding:14px; margin-top:18px;">
	 <b>🛠️ Practical Example:</b><br>
	 <pre style="background:#f5f5f5; border-radius:6px; padding:8px;">Sensor (Altitude) ──▶ ARINC 429 TX ──▶ [Twisted Pair] ──▶ ARINC 429 RX (Flight Computer)
	 </pre>
	 <i>Altitude sensor sends 32-bit data words to the flight computer, no handshake needed.</i>
	 </div>

**Troubleshooting Tips:**
- Check for correct voltage levels (±10V typical)
- Inspect for broken or shorted twisted pair wiring
- Use an oscilloscope to verify 32-bit word timing
- Parity errors? Check for noise or grounding issues

**Security Considerations:**
- No built-in encryption or authentication
- Physical access required for attacks (tampering, spoofing)
- Use physical security and cable shielding for protection

**Comparison Table:**

.. list-table:: ARINC 429 vs. ARINC 664 vs. MIL-STD-1553
	 :header-rows: 1
	 :widths: 20 20 20 20

	 * - Feature
		 - ARINC 429
		 - ARINC 664
		 - MIL-STD-1553
	 * - Directionality
		 - Simplex
		 - Full-duplex
		 - Bidirectional
	 * - Data Rate
		 - 12.5/100 kbps
		 - 100 Mbps/1 Gbps
		 - 1 Mbps
	 * - Topology
		 - Point-to-point
		 - Switched star
		 - Linear bus
	 * - Use Case
		 - Sensor data
		 - High-bandwidth
		 - Command/response

**Popular Tools:**
- AIM ARINC 429 Analyzer
- Excalibur Systems 429 Bus Monitor
- Ballard Technology ARINC 429 USB Adapter

.. raw:: html

	 <div style="background-color:#e1bee7; border-radius:10px; padding:12px; margin-top:18px;">
	 <b>🧠 Memorization Mnemonic:</b> <span style="color:#6a1b9a;">"ARINC 429 is the airplane's one-way street—simple, safe, and always on time!"</span>
	 </div>
- Self-clocking, self-synchronizing
- 32-bit word format (label, data, SSM, parity)
- Parity error checking

**Physical/Electrical Layer:**
- Differential signaling (twisted pair)
- Voltage: ±10V nominal
- Data rate: 12.5 kbps (low speed), 100 kbps (high speed)
- Cable length: up to 150 feet (45 meters) typical

**Topology:**
- Bus/Star (one-way)

**Use Cases:**
- Avionics sensor data (altitude, speed, heading, etc.)
- Communication between LRUs (Line Replaceable Units)

**Pros:**
- Simple, robust, highly reliable
- Widely adopted in commercial aviation

**Cons:**
- Low bandwidth by modern standards
- Unidirectional (no handshaking/acknowledgment)

**Standard:**
- ARINC Specification 429

**Typical Applications:**
- Commercial and transport aircraft avionics
- Legacy and retrofit systems
