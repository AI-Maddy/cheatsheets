**cheatsheet for USB in Linux** (kernel & userspace perspective, valid for kernels 6.1–6.14 / early 2026).

Covers USB host, gadget (device mode), common classes (audio, HID, mass storage, CDC, etc.), debugging, and embedded usage.

### 1. USB Basics – Speed & Versions (2026 Reality)

| USB Version       | Marketing Name       | Max Speed (theoretical) | Typical Real-World | Common Connectors (2026)       | Typical Use in Embedded |
|-------------------|----------------------|--------------------------|--------------------|--------------------------------|--------------------------|
| USB 2.0           | Hi-Speed             | 480 Mbit/s              | ~280–400 Mbit/s    | USB-A, micro-B, Type-C         | Legacy, low-cost devices |
| USB 3.2 Gen 1     | SuperSpeed USB 5 Gbps| 5 Gbit/s                | ~3.5–4.5 Gbit/s    | Type-C (most), Type-A (legacy) | Mass storage, cameras    |
| USB 3.2 Gen 2     | SuperSpeed USB 10 Gbps| 10 Gbit/s              | ~7–9 Gbit/s        | Type-C                         | High-speed storage, docks|
| USB 3.2 Gen 2×2   | SuperSpeed USB 20 Gbps| 20 Gbit/s              | ~15–18 Gbit/s      | Type-C (rare)                  | Pro audio interfaces     |
| USB4 (v1/v2)      | USB4 20/40/80 Gbps   | 20–80 Gbit/s            | 15–70 Gbit/s       | Type-C (Thunderbolt compat)    | High-end laptops, docks  |
| USB PD (Power Delivery) | —                 | Up to 240 W (EPR 2025+) | 15–100 W common    | Type-C                         | Charging + data          |

### 2. Linux USB Subsystems & Layers

| Subsystem / Driver        | Location                          | Purpose / Typical Devices                          | Key Files / Commands                     |
|---------------------------|-----------------------------------|----------------------------------------------------|------------------------------------------|
| **USB Core**              | `drivers/usb/core/`               | Hub, device enumeration, URB management            | `/sys/bus/usb/devices/`                  |
| **USB Host**              | `drivers/usb/host/`               | xHCI (most modern), EHCI, OHCI, DWC3 (embedded)    | `xhci-hcd`, `dwc3`                       |
| **USB Gadget**            | `drivers/usb/gadget/`             | Device mode (USB peripheral)                       | `g_ether`, `g_mass_storage`, `g_webcam`  |
| **USB Audio Class**       | `sound/usb/`                      | USB sound cards, headsets, microphones             | `snd-usb-audio`                          |
| **USB HID**               | `drivers/hid/usbhid/`             | Keyboards, mice, gamepads                          | `usbhid`                                 |
| **USB Mass Storage**      | `drivers/usb/storage/`            | USB sticks, card readers                           | `usb-storage`                            |
| **CDC (ACM / ECM / NCM)** | `drivers/usb/class/`              | Serial (CDC ACM), Ethernet (ECM/NCM/RNDIS)         | `cdc-acm`, `cdc_ether`                   |
| **USB Video Class (UVC)** | `drivers/media/usb/uvc/`          | USB webcams, endoscopes                            | `uvcvideo`                               |

### 3. Key USB Device Nodes & Sysfs Locations

| Node / Path                              | Meaning / Typical Use                              | Common Commands / Tools                     |
|------------------------------------------|----------------------------------------------------|---------------------------------------------|
| `/dev/bus/usb/001/002`                   | Raw USB device node (bus 001, device 002)          | `lsusb -v -d xxxx:yyyy`                     |
| `/dev/snd/pcmC1D0p`                      | USB audio playback (card 1, device 0)              | `aplay -D hw:1,0`                           |
| `/dev/video0`                            | UVC webcam                                         | `v4l2-ctl --list-devices`                   |
| `/dev/ttyACM0`                           | CDC ACM serial (Arduino, modem)                    | `minicom -D /dev/ttyACM0`                   |
| `/sys/bus/usb/devices/`                  | All connected USB devices (tree view)              | `lsusb -t` (tree)                           |
| `/sys/bus/usb/drivers/`                  | Bound drivers per device                           | `echo -n '1-1' > unbind` (unbind driver)    |

### 4. Most Useful lsusb & usb-devices Output Flags

```bash
# Basic list
lsusb

# Tree view (shows hierarchy)
lsusb -t

# Verbose (descriptors, endpoints)
lsusb -v -d 046d:c077   # Logitech webcam example

# By vendor:product
lsusb | grep 8087       # Intel Bluetooth example

# Speed & class
usb-devices | grep -E "Speed|Class"
```

### 5. Common USB Classes & Linux Driver Modules

| USB Class / Subclass | Decimal (bInterfaceClass) | Linux Module / Driver          | Typical Devices                          |
|----------------------|----------------------------|--------------------------------|------------------------------------------|
| Audio                | 0x01                       | snd-usb-audio                  | USB DACs, headsets, microphones          |
| Communications (CDC) | 0x02                       | cdc-acm, cdc_ether, rndis_host | Serial adapters, USB Ethernet            |
| HID                  | 0x03                       | usbhid                         | Keyboards, mice, touchscreens            |
| Mass Storage         | 0x08                       | usb-storage                    | USB sticks, card readers                 |
| Video (UVC)          | 0x0E                       | uvcvideo                       | Webcams, endoscopes                      |
| Vendor Specific      | 0xFF                       | Custom / vendor driver         | Many (Qualcomm, FTDI, etc.)              |

### 6. USB Gadget (Device Mode) – Quick Setup (Embedded)

**Most common gadget drivers**  
- `g_mass_storage` — emulate USB stick  
- `g_ether` — USB Ethernet (RNDIS/ECM/NCM)  
- `g_serial` — virtual serial port  
- `g_webcam` — UVC gadget (test webcam)  
- `g_audio` — USB sound card (experimental)

**Enable gadget on embedded board (e.g. Raspberry Pi, i.MX, Rockchip)**  
```bash
modprobe libcomposite
mkdir -p /sys/kernel/config/usb_gadget/g1
cd /sys/kernel/config/usb_gadget/g1

echo 0x1d6b > idVendor   # Linux Foundation
echo 0x0104 > idProduct  # Multifunction Composite Gadget
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

mkdir strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "MyCompany" > strings/0x409/manufacturer
echo "USB Ethernet Gadget" > strings/0x409/product

mkdir configs/c.1
mkdir functions/ecm.usb0
ln -s functions/ecm.usb0 configs/c.1/
echo "1" > os_desc/use
echo "0x1" > os_desc/b_vendor_code
echo "MSFT100" > os_desc/qw_sign

mkdir configs/c.1/strings/0x409
echo "Config 1" > configs/c.1/strings/0x409/configuration

echo "ci_hdrc.0" > UDC   # or dwc2, dwc3, etc.
```

### 7. Debugging & Diagnostic Commands

```bash
# Full USB tree + speeds
lsusb -t

# Watch enumeration live
dmesg -w | grep usb

# USB power / suspend debug
cat /sys/bus/usb/devices/1-1/power/level   # auto / on / suspend

# Force re-enumeration
echo 0 > /sys/bus/usb/devices/1-1/authorized
echo 1 > /sys/bus/usb/devices/1-1/authorized

# USB quirks (fix broken devices)
echo "046d:c077:i" > /sys/module/usbhid/parameters/ignore

# Monitor URB traffic (very verbose)
echo 'module usbcore +p' > /sys/kernel/debug/dynamic_debug/control
```

### 8. Embedded / Low-Level Tips (2026)

- **USB Device Tree bindings** — use `usb@...` + `dr_mode = "host";` / `"peripheral";` / `"otg"`
- **DWC3 / DWC2** — most common embedded USB controllers (Synopsys)
- **USB 3.x** — requires good PCB layout (impedance 90 Ω diff pairs)
- **USB PD** — use `tcpm` / `tcpci` + `typec` framework (Type-C)
- **Low-latency audio** — USB Audio Class 2 + small periods (64–256 frames)
- **Gadget multi-function** — composite gadget (ACM + ECM + mass storage)
- **Power budget** — USB 2.0 = 500 mA, USB 3.0 = 900 mA, PD = up to 100 W+

Good luck with your USB bring-up or gadget development in Linux!