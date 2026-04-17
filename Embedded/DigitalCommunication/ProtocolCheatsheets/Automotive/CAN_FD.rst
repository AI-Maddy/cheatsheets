CAN FD
======

**Domain:** Automotive

**Description:**
Upgraded CAN (up to ~5-8 Mbps data phase, 64-byte payloads; widely adopted for faster control/ADAS).

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">🚗💨 CAN FD</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Automotive</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"CAN, but Faster Data!"</span><br>
	<b>Icon:</b> 🚗💨<br>
	</div>

**Key Features:**
- 💨 Higher data rates (up to 8 Mbps)
- 📦 Larger payloads (up to 64 bytes)
- 🔄 Backward compatible with classic CAN
- 🛡️ Improved error detection

**Physical/Electrical Layer:**
- 🔌 Differential signaling (twisted pair)
- ⚡ Data rates: arbitration phase (1 Mbps), data phase (up to 8 Mbps)

**Topology:**
- 🌐 Bus topology

**Frame Format (CAN FD):**

.. code-block:: text

    +-----+-----+-----+-----+-----+-----+-----+-----+
    | SOF | ID  | RTR | IDE | DLC | DATA | CRC | ACK |
    +-----+-----+-----+-----+-----+-----+-----+-----+
    |  1  | 11  |  1  |  1  |  4  | 0-64|  21 |  2  |
    +-----+-----+-----+-----+-----+-----+-----+-----+

- DLC: Data Length Code (0-64 bytes)
- CRC: 21 bits (improved)

**Example CAN FD Message:**

.. code-block:: text

    0x18DAF110   [64]  02 10 01 ... (up to 64 bytes)

**Troubleshooting Tips:**
- Ensure all nodes support CAN FD
- Check for proper bus termination
- Use CAN FD-capable analyzers

**Security Considerations:**
- No built-in encryption/authentication
- Slightly improved error detection
- Use secure gateways, monitor for anomalies

**Comparison Table:**

.. list-table:: CAN Family Comparison
   :header-rows: 1

   * - Feature
     - CAN
     - CAN FD
     - CAN XL
   * - Max Data Rate
     - 1 Mbps
     - 8 Mbps
     - 20 Mbps
   * - Max Payload
     - 8 bytes
     - 64 bytes
     - 2048 bytes
   * - Security
     - None
     - Improved
     - Enhanced
   * - Typical Use
     - Powertrain, body
     - ADAS, diagnostics
     - Zonal, high-speed

**Advanced Use Cases:**
- ADAS sensor fusion
- High-speed diagnostics
- OTA updates

**Open-Source Tools:**
- can-utils (Linux)
- SavvyCAN
- Wireshark (CAN FD support)
- SocketCAN (Linux kernel)

**Standard:**
- 📜 ISO 11898-1:2015 (CAN FD)

**Typical Applications:**
- 🚗 Modern vehicles, especially with ADAS

**Memorization Tip:**
<span style="color:#1976d2;">Think of CAN FD as "CAN with a turbo boost"—same bus, much faster data!</span>

.. raw:: html

	<div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	<b>Quick Visual:</b> <span style="font-size:1.5em;">🚗 &rarr; 💨 &rarr; 📦</span><br>
	<i>More data, faster, on the same CAN bus!</i>
	</div>
