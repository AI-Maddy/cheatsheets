**cheatsheet for USB in embedded Linux devices** — focused on **porting**, **kernel programming**, **driver development**, and **typical bring-up** patterns (kernels 6.1–6.14 / early 2026 perspective).

Covers both **USB host** and **USB gadget/device** mode — very common in embedded products (gateways, industrial HMI, automotive ECUs, audio interfaces, medical devices, IoT hubs, etc.).

📌 1. USB Controller Drivers – Most Common in Embedded (2026)

| Controller IP / SoC Family       | Linux Driver Module       | Device Tree compatible string example                  | Mode Support (Host / Device / OTG) | Typical Platforms |
|----------------------------------|---------------------------|--------------------------------------------------------|-------------------------------------|-------------------|
| Synopsys DesignWare USB3 (DWC3)  | ``dwc3``                    | ``snps,dwc3``                                            | Host + Device + OTG                 | Almost all modern ARM SoCs (Qualcomm, NXP i.MX8, Rockchip, TI Jacinto, MediaTek) |
| Synopsys DesignWare USB2 (DWC2)  | ``dwc2``                    | ``snps,dwc2``                                            | Host + Device + OTG                 | Older/cheap SoCs, Raspberry Pi 3/4/Zero |
| NXP / Freescale USB              | ``fsl-usb2`` / ``imx-usb``    | ``fsl,usb2``, ``fsl,imx-usb``                              | Host + Device                       | i.MX6/7/8 series |
| ChipIdea / NXP USB               | ``ci_hdrc``                 | ``chipidea,usb2``                                        | Host + Device + OTG                 | Many i.MX, Layerscape |
| Atmel / Microchip USB            | ``atmel-usb`` / ``at91-udc``  | ``atmel,at91rm9200-udc``                                 | Device mostly                       | SAM9, SAMA5 |
| Allwinner / Pine64 USB           | ``musb`` / ``sunxi`` variants | ``allwinner,sun4i-a10-musb``                             | OTG                                 | Allwinner SoCs |
| Raspberry Pi (BCM283x/2711)      | ``dwc2`` + ``dwc-otg``        | ``brcm,bcm2835-usb``                                     | OTG                                 | Pi 1–5 |

**Rule 2026**:  
**DWC3 is the dominant USB controller** in almost all new embedded Linux designs (Qualcomm, NXP, Rockchip, Amlogic, MediaTek, etc.)

🔧 2. Device Tree – Typical USB Node Patterns

#### Host-only (most common in gateways / industrial)

.. code-block:: dts

&usb {
    dr_mode = "host";
    status = "okay";
};

#### OTG / Dual-role (very common – switch host/device at runtime)

.. code-block:: dts

&usb {
    dr_mode = "otg";
    status = "okay";

    usb-role-switch;
    role-switch-default-mode = "host";   // or "peripheral"

    /* Optional: Type-C connector with PD */
    usb_con: connector {
        compatible = "usb-c-connector";
        data-role = "dual";
        power-role = "dual";
        try-power-role = "sink";
    };
};

#### Gadget / Device-only (e.g. USB audio class device, RNDIS Ethernet gadget)

.. code-block:: dts

&usb {
    dr_mode = "peripheral";
    status = "okay";
};

🐧 3. Kernel Configuration – Must-Have Options (embedded USB)

.. code-block:: text

================================================================================
USB Core & Host
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



CONFIG_USB=y
CONFIG_USB_XHCI_HCD=y               # USB 3.x (most modern SoCs)
CONFIG_USB_EHCI_HCD=y               # USB 2.0 fallback
CONFIG_USB_OHCI_HCD=y               # older USB 1.1/2.0
CONFIG_USB_DWC3=y                   # Synopsys DWC3 (most common)
CONFIG_USB_DWC3_HOST=y
CONFIG_USB_DWC3_GADGET=y
CONFIG_USB_DWC3_DUAL_ROLE=y         # OTG support

================================================================================
🔧 USB Gadget / Device mode
================================================================================

CONFIG_USB_GADGET=y
CONFIG_USB_GADGETFS=y               # raw gadgetfs (low-level)
CONFIG_USB_CONFIGFS=y               # configfs (modern, recommended)
CONFIG_USB_CONFIGFS_F_FS=y          # file storage
CONFIG_USB_CONFIGFS_F_MASS_STORAGE=y
CONFIG_USB_CONFIGFS_F_SERIAL=y
CONFIG_USB_CONFIGFS_F_RNDIS=y       # network gadget
CONFIG_USB_CONFIGFS_F_ECM=y
CONFIG_USB_CONFIGFS_F_AUDIO=y       # USB audio gadget

================================================================================
USB classes
================================================================================

CONFIG_USB_ACM=y                    # CDC ACM (serial)
CONFIG_USB_SERIAL=y
CONFIG_USB_USB_SERIAL=y
CONFIG_USB_AUDIO=y                  # USB sound card
CONFIG_USB_VIDEO_CLASS=y            # UVC gadget / webcam

📌 4. USB Gadget – Most Common Use Cases & Setup (Embedded)

| Use Case                     | Gadget Driver / Configfs Function | Typical Device Tree / Config | Linux Host Side Appearance |
|------------------------------|------------------------------------|-------------------------------|-----------------------------|
| **USB Ethernet (RNDIS/ECM)** | ``g_ether`` / ``ecm`` / ``rndis``        | ``functions/ecm.usb0``          | USB network adapter (RNDIS or CDC-ECM) |
| **Mass Storage**             | ``g_mass_storage``                   | ``functions/mass_storage.usb0`` | USB flash drive             |
| **Serial (CDC ACM)**         | ``g_serial`` / ``acm``                 | ``functions/acm.usb0``          | /dev/ttyACM0                |
| **USB Audio Class**          | ``g_audio``                          | ``functions/audio.usb0``        | USB sound card              |
| **Composite (multi-function)** | configfs + multiple functions    | ``functions/acm + ecm + mass_storage`` | Multiple devices in one USB port |

**Modern configfs gadget setup example** (most recommended 2026)

.. code-block:: bash

================================================================================
Create gadget
================================================================================

mkdir -p /config/usb_gadget/g1
cd /config/usb_gadget/g1

================================================================================
IDs & strings
================================================================================

echo 0x1d6b > idVendor   # Linux Foundation
echo 0x0104 > idProduct
mkdir strings/0x409
echo "1234567890" > strings/0x409/serialnumber

================================================================================
⚙️ Configuration
================================================================================

mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo "RNDIS + ACM" > configs/c.1/strings/0x409/configuration

================================================================================
📚 Add functions
================================================================================

mkdir functions/rndis.usb0
ln -s functions/rndis.usb0 configs/c.1/
mkdir functions/acm.usb0
ln -s functions/acm.usb0 configs/c.1/

================================================================================
💻 Bind to controller (dwc3 example)
================================================================================

echo "dwc3@...auto" > UDC

🐛 5. Debugging & Bring-up Commands (Embedded USB)

.. code-block:: bash

================================================================================
See USB controller status
================================================================================

dmesg | grep -i usb
lsmod | grep -E 'dwc|musb|ci_hdrc|xhci'

================================================================================
🔧 List connected devices (host mode)
================================================================================

lsusb -t

================================================================================
Raw USB traffic (very useful!)
================================================================================

usbmon (module usbmon)
tcpdump -i usbmon1 -w usb.pcap   # Wireshark compatible

================================================================================
🔧 Force re-probe / reset device
================================================================================

echo 1-1 > /sys/bus/usb/drivers/usb/unbind
echo 1-1 > /sys/bus/usb/drivers/usb/bind

================================================================================
Check gadget state
================================================================================

cat /sys/kernel/config/usb_gadget/g1/UDC
cat /sys/class/udc/dwc3/state

================================================================================
USB role switch (OTG)
================================================================================

echo peripheral > /sys/devices/platform/soc/.../usb-role-switch/role

💾 6. Common Porting / Kernel Programming Gotchas

- **dr_mode** in DT must match hardware capability
- **DWC3** needs correct PHY binding (``usb-phy``, ``usb2-phy``, ``usb3-phy``)
- **VBUS sense** — use GPIO or Type-C connector driver (``typec``)
- **USB role switch** — use ``usb-role-switch`` property + ``typec`` framework
- **High-speed / SuperSpeed** — impedance matching 90 Ω ±15 %, short traces
- **Power delivery (PD)** — ``tcpm`` / ``tcpci`` + ``typec`` stack required
- **Low-latency audio** — use small buffer sizes (64–256 frames), RT priority
- **Gadget multi-function** — configfs is the modern way (g_multi is deprecated)

This cheatsheet covers ~90% of USB bring-up and kernel-level work in embedded Linux devices.

🟢 🟢 Good luck with your USB host/gadget porting!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
