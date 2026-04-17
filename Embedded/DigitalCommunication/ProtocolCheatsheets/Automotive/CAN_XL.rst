CAN XL
======

**Domain:** Automotive

**Description:**
Latest evolution of CAN (up to 20 Mbps, 2048-byte payloads, enhanced security/QoS; bridging to Ethernet while keeping CAN advantages; gaining traction in 2025–2026 designs).

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">🚗⚡ CAN XL</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Automotive</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"CAN eXtra Large!"</span><br>
	<b>Icon:</b> 🚗⚡<br>
	</div>

**Key Features:**
- ⚡ Up to 20 Mbps data rate
- 📦 Payloads up to 2048 bytes
- 🔒 Enhanced security and QoS
- 🔄 Bridges CAN and Ethernet domains

**Physical/Electrical Layer:**
- 🔌 Differential signaling (twisted pair)
- ⚡ Data rates: up to 20 Mbps

**Topology:**
- 🌐 Bus topology

**Frame Format (CAN XL):**

.. code-block:: text

    +-----+-----+-----+-----+-----+-----+-----+-----+
    | SOF | ID  | XL  | DLC | DATA | CRC | ACK | SEC |
    +-----+-----+-----+-----+-----+-----+-----+-----+
    |  1  | 29  |  1  |  8  |0-2048|  32 |  2  |var.|
    +-----+-----+-----+-----+-----+-----+-----+-----+

- XL: CAN XL control bits
- SEC: Security field (optional)

**Example CAN XL Message:**

.. code-block:: text

    0x18DAF110   [2048]  ... (up to 2048 bytes)

**Troubleshooting Tips:**
- Ensure all nodes are CAN XL capable
- Check for proper bus design and length
- Use CAN XL analyzers for debugging

**Security Considerations:**
- Enhanced security fields (optional)
- Still recommend network segmentation
- Monitor for protocol downgrades

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
- Zonal architectures
- High-speed sensor fusion
- Secure OTA updates

**Open-Source Tools:**
- can-utils (Linux, experimental XL support)
- Vector CANoe (commercial)
- Wireshark (future XL support)

**Standard:**
- 📜 ISO 11898-1:2024 (CAN XL)

**Typical Applications:**
- 🚗 Next-gen vehicles, software-defined cars

**Memorization Tip:**
<span style="color:#1976d2;">Think of CAN XL as "CAN eXtra Large"—bigger, faster, and ready for the future of cars!</span>

.. raw:: html

	<div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	<b>Quick Visual:</b> <span style="font-size:1.5em;">🚗 &rarr; ⚡ &rarr; 📦</span><br>
	<i>CAN bus, but supercharged for tomorrow's vehicles!</i>
	</div>
