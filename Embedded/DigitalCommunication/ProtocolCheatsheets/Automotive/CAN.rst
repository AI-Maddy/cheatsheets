CAN
===

**Domain:** Automotive/Avionics

**Description:**
Classic automotive/industrial bus (1 Mbps). Used in some military/ground-support aerospace contexts as MIL-CAN.

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">🚗🚌 CAN (Controller Area Network)</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Automotive/Avionics</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"Car Area Network"</span><br>
	<b>Icon:</b> 🚗🚌<br>
	</div>

**Key Features:**
- 🚌 Multi-master, message-based protocol
- 🔄 Robust error detection and handling
- 🛡️ Real-time, deterministic communication
- 🔌 Supports up to 1 Mbps (classic CAN)

**Physical/Electrical Layer:**
- 🔌 Differential signaling (twisted pair)
- ⚡ Data rates: up to 1 Mbps

**Topology:**
- 🌐 Bus topology

**Frame Format (Classical CAN):**

.. code-block:: text

    +-----+-----+-----+-----+-----+-----+-----+-----+
    | SOF | ID  | RTR | IDE | DLC | DATA | CRC | ACK |
    +-----+-----+-----+-----+-----+-----+-----+-----+
    |  1  | 11  |  1  |  1  |  4  | 0-8 |  15 |  2  |
    +-----+-----+-----+-----+-----+-----+-----+-----+

- SOF: Start of Frame
- ID: Identifier (message priority)
- RTR: Remote Transmission Request
- IDE: Identifier Extension
- DLC: Data Length Code
- DATA: 0-8 bytes
- CRC: Cyclic Redundancy Check
- ACK: Acknowledge

**Example CAN Message:**

.. code-block:: text

    0x18DAF110   [8]  02 10 01 00 00 00 00 00
    (ID: 0x18DAF110, 8 bytes, data: 02 10 01 ...)

**Troubleshooting Tips:**
- Check for proper termination (120Ω at each end)
- Use an oscilloscope or CAN analyzer for bus errors
- Look for dominant/recessive bit errors
- Monitor error counters in CAN controller

**Security Considerations:**
- No built-in encryption or authentication
- Susceptible to spoofing, DoS, fuzzing attacks
- Use network segmentation, gateways, and intrusion detection

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
- Zonal architectures in modern vehicles
- Over-the-air (OTA) updates
- Integration with Ethernet gateways

**Open-Source Tools:**
- can-utils (Linux)
- SavvyCAN
- Wireshark (CAN dissector)
- SocketCAN (Linux kernel)

**Standard:**
- 📜 ISO 11898

**Typical Applications:**
- 🚗 All modern vehicles, industrial automation

**Memorization Tip:**
<span style="color:#1976d2;">Think of CAN as the "car's nervous system"—simple, reliable, and everywhere!</span>

.. raw:: html

	<div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	<b>Quick Visual:</b> <span style="font-size:1.5em;">🚗 &rarr; 🚌 &rarr; 🛡️</span><br>
	<i>All your car's parts talk on the CAN bus!</i>
	</div>
