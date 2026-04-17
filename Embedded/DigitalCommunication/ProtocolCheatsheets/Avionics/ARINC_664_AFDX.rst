ARINC 664 / AFDX
================

**Domain:** Avionics

**Description:**
Ethernet-based, deterministic network (used in modern airliners like Airbus A380, Boeing 787 for high-bandwidth data).

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">✈️🌐 ARINC 664 / AFDX</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Avionics</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"Avionics Full-Duplex Data eXpress"</span><br>
	<b>Icon:</b> ✈️🌐<br>
	</div>

**Key Features:**
- 🌐 Based on Ethernet (IEEE 802.3)
- 🔄 Full-duplex, switched network
- 🛣️ Virtual links (VLs) for deterministic delivery
- 📊 Bandwidth allocation and traffic shaping
- 🛡️ Redundancy for fault tolerance

**Physical/Electrical Layer:**
- 🔌 Standard Ethernet cabling (twisted pair, fiber)
- 🚀 Data rates: 100 Mbps, 1 Gbps

**Topology:**
- 🌟 Switched star topology

**Use Cases:**
- 🎥 High-bandwidth avionics data (video, sensor fusion)
- 🔄 Replacing legacy point-to-point buses

**Pros:**
- 🚀 High bandwidth, scalable
- 🛡️ Deterministic and reliable
- 🔁 Supports redundancy

**Cons:**
- 🏗️ More complex than legacy buses
- ⚠️ Requires careful network design

**Standard:**
- 📜 ARINC 664 Part 7 (AFDX)

**Typical Applications:**

.. raw:: html

	 <div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	 <b>Quick Visual:</b> <span style="font-size:1.5em;">✈️ &rarr; 🌐 &rarr; 🛣️</span><br>
	 <i>Plane's data rides on a dedicated, high-speed network highway!</i>
	 </div>

.. raw:: html

	 <div style="background-color:#e8f5e9; border-radius:10px; padding:14px; margin-top:18px;">
	 <b>🛠️ Practical Example:</b><br>
	 <pre style="background:#f5f5f5; border-radius:6px; padding:8px;">Flight Management System ──▶ AFDX End System ──▶ [Ethernet Switch] ──▶ AFDX End System (Display Unit)
	 </pre>
	 <i>Flight data is sent deterministically over virtual links to cockpit displays and other subsystems.</i>
	 </div>

**Troubleshooting Tips:**
- Check switch configuration for correct virtual link mapping
- Monitor bandwidth allocation and traffic shaping settings
- Use network analyzers to verify deterministic delivery
- Redundancy issues? Inspect cabling and switch failover

**Security Considerations:**
- No built-in encryption (add network-level security)
- VLANs and firewalls recommended for isolation
- Monitor for spoofing or denial-of-service attempts

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
- AFDX End System Simulators (e.g., TechSAT, AIM)
- Wireshark with AFDX plugins
- Airbus/Boeing AFDX test benches

.. raw:: html

	 <div style="background-color:#e1bee7; border-radius:10px; padding:12px; margin-top:18px;">
	 <b>🧠 Memorization Mnemonic:</b> <span style="color:#6a1b9a;">"AFDX is the Ethernet superhighway for planes—fast, organized, and always with a backup lane!"</span>
	 </div>
