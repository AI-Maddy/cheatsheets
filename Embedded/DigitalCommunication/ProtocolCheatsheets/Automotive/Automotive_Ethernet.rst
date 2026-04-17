Automotive Ethernet
==================

**Domain:** Automotive

**Description:**
High-bandwidth, real-time Ethernet (100BASE-T1, 1000BASE-T1, Multi-Gig up to 10 Gbps+; for cameras, ADAS, infotainment, zonal architectures; TSN profiles like IEEE 802.1DG for real-time).

.. raw:: html

	<div style="background-color:#e3f2fd; border-radius:10px; padding:16px; margin-bottom:16px;">
	<h2 style="color:#1565c0;">🚗🌐 Automotive Ethernet</h2>
	<b>Domain:</b> <span style="color:#1976d2;">Automotive</span><br>
	<b>Mnemonic:</b> <span style="color:#388e3c;">"Ethernet for Engines"</span><br>
	<b>Icon:</b> 🚗🌐<br>
	</div>

**Key Features:**
- 🌐 High-bandwidth, real-time Ethernet
- 🚦 Supports TSN (Time-Sensitive Networking)
- 🔄 Enables zonal architectures and ADAS
- 🛡️ Supports redundancy and security

**Physical/Electrical Layer:**
- 🔌 100BASE-T1, 1000BASE-T1, Multi-Gig (up to 10 Gbps+)
- 🧲 Twisted pair cabling, automotive-grade connectors

**Topology:**
- 🌟 Star or daisy-chain (switched)

**Ethernet Frame Format:**

.. code-block:: text

    +--------+--------+--------+--------+--------+--------+--------+
    | Preamble | Dest MAC | Src MAC | Type | Payload | CRC |
    +--------+--------+--------+--------+--------+--------+--------+
    |   7B   |   6B   |   6B   |  2B   | 46-1500B|  4B   |
    +--------+--------+--------+--------+--------+--------+--------+

- MAC: Media Access Control address
- Type: EtherType (e.g., 0x0800 for IPv4)
- CRC: Frame Check Sequence

**Example Ethernet Message:**

.. code-block:: text

    01:23:45:67:89:ab > 12:34:56:78:9a:bc, ethertype IPv4 (0x0800), length 100
    Data: 45 00 ...

**Troubleshooting Tips:**
- Check for correct cabling and connectors
- Use automotive Ethernet analyzers (e.g., Intrepid, Vector)
- Monitor for dropped packets, EMI issues
- Validate TSN configuration for real-time

**Security Considerations:**
- Use VLANs, MACsec, and firewalls
- Segment critical networks (e.g., ADAS vs infotainment)
- Monitor for ARP spoofing, DoS attacks

**Comparison Table:**

.. list-table:: Automotive Network Comparison
   :header-rows: 1

   * - Feature
     - CAN
     - CAN FD
     - CAN XL
     - Automotive Ethernet
   * - Max Data Rate
     - 1 Mbps
     - 8 Mbps
     - 20 Mbps
     - 10 Gbps+
   * - Max Payload
     - 8 bytes
     - 64 bytes
     - 2048 bytes
     - 1500 bytes
   * - Real-Time
     - Yes
     - Yes
     - Yes
     - Yes (TSN)
   * - Typical Use
     - Powertrain
     - ADAS
     - Zonal
     - Cameras, backbone

**Advanced Use Cases:**
- Zonal architectures
- High-speed sensor fusion
- Over-the-air (OTA) updates
- In-vehicle infotainment

**Open-Source Tools:**
- Wireshark (Ethernet dissector)
- Scapy (packet crafting)
- Linux ethtool, iproute2

**Standard:**
- 📜 IEEE 802.3, TSN (802.1DG)

**Typical Applications:**
- 🚗 Modern vehicles, electric vehicles, autonomous cars

**Memorization Tip:**
<span style="color:#1976d2;">Think of Automotive Ethernet as the "data highway" for your car—fast, reliable, and ready for the future!</span>

.. raw:: html

	<div style="background-color:#fffde7; border-radius:10px; padding:12px; margin-top:16px;">
	<b>Quick Visual:</b> <span style="font-size:1.5em;">🚗 &rarr; 🌐 &rarr; 🚦</span><br>
	<i>Your car's data zips around on Ethernet lanes!</i>
	</div>
