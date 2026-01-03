**cheatsheet for DSI** (Display Serial Interface) in the context of Linux kernel and embedded systems (modern MIPI DSI, as of 2026 – kernels ~6.12+).

### 1. DSI Basics

- **Standard** — MIPI Alliance DSI (Display Serial Interface) v1.3 (2015) + later amendments  
  Most common in mobile/embedded: smartphones, tablets, automotive displays, laptops, Raspberry Pi, etc.
- **Physical Layer** — MIPI D-PHY (most common) or C-PHY (newer, higher bandwidth, lower power)
- **Topology** — Point-to-point (host → one display panel)
- **Data Lanes** — 1–4 lanes (data) + 1 clock lane (D-PHY); C-PHY uses 3-phase signaling
- **Modes**  
  - **Command Mode** (most common for small/medium panels): Host sends commands + pixel data  
  - **Video Mode** (burst / non-burst): Continuous streaming like HDMI (for large/high-refresh panels)

### 2. DSI vs Other Display Interfaces

| Interface   | Lanes       | Max Bandwidth (2026 typical) | Power / Pins | Typical Use Cases              |
|-------------|-------------|-------------------------------|--------------|--------------------------------|
| MIPI DSI    | 1–4 (D-PHY) | ~2–6 Gbps (4 lanes Gen1/2)   | Low          | Phones, tablets, wearables     |
| MIPI CSI-2  | 1–4         | Similar                       | Low          | Cameras (not displays)         |
| eDP         | 1–8 lanes   | Higher (up to 20+ Gbps)       | Medium       | Laptops, Chromebooks           |
| MIPI C-PHY  | 3-phase     | Up to ~12–17 Gbps equiv       | Lower        | Newer flagship phones (2024+)  |
| Parallel RGB| 18/24-bit   | Low (~100–300 MB/s)           | High pin count | Cheap LCDs, legacy             |

### 3. DSI Packet Types

| Packet Type          | Direction | Payload? | Use Case / Notes |
|----------------------|-----------|----------|------------------|
| **Short Write**      | Host → Panel | No       | Most commands (DCS) |
| **Long Write**       | Host → Panel | Yes      | Frame buffer data, large register writes |
| **Short Read**       | Host → Panel | No       | Read status/register |
| **Long Read**        | Host → Panel | Yes      | Read large data (rare) |
| **Acknowledge Error** | Panel → Host | No       | Error reporting (ECC/CRC fail) |
| **End of Transmission** | —       | —        | Marks end of burst |

**DCS** (Display Command Set) — subset of MIPI DCS commands (0x00–0xFF), e.g.:
- 0x11 = Sleep Out
- 0x29 = Display On
- 0x2C = Memory Write (start pixel data)
- 0x3C = Memory Continue Write

### 4. Linux Kernel DSI Subsystem (drm/panel + drm/bridge)

| Component                  | Location / File                          | Purpose |
|----------------------------|------------------------------------------|---------|
| `struct mipi_dsi_host`     | `include/drm/drm_mipi_dsi.h`             | DSI host controller (SoC side) |
| `struct mipi_dsi_device`   | same                                     | Per-panel DSI device |
| `struct drm_panel`         | `include/drm/drm_panel.h`                | Generic panel abstraction |
| `struct mipi_dsi_driver`   | `include/drm/drm_mipi_dsi.h`             | Register panel driver |
| `drm_of_find_panel_or_bridge` | `drivers/gpu/drm/drm_of.c`            | DT lookup helper |
| `mipi_dsi_dcs_write()` / `read()` | helpers                             | Send DCS commands |

### 5. Typical Device Tree Structure

```dts
& DSI_host_node {                   // e.g. &dsi@... or &mipi_dsi
    status = "okay";

    ports {
        #address-cells = <1>;
        #size-cells = <0>;

        port@1 {                        // usually out port
            reg = <1>;
            dsi_out: endpoint {
                remote-endpoint = <&panel_in>;
                data-lanes = <1 2>;     // or <1 2 3 4>
            };
        };
    };
};

panel: panel@0 {
    compatible = "vendor,model", "panel-dsi-simple";
    reg = <0>;                      // DSI virtual channel (usually 0)
    reset-gpios = <&gpio 10 GPIO_ACTIVE_LOW>;
    vdd-supply = <&reg_lcd_vdd>;
    status = "okay";

    port {
        panel_in: endpoint {
            remote-endpoint = <&dsi_out>;
        };
    };
};
```

### 6. Common Panel Compatible Strings (2025–2026)

- `himax,hx8394`
- `novatek,nt35510`, `nt35595`, `nt36672a`
- `ilitek,ili9881c`, `ili7807`
- `visionox,rm67191` (OLED)
- `samsung,s6e3ha3`, `s6e3hf4` (AMOLED)
- `panel-dsi-simple` — fallback for dumb panels (only DCS init sequence)

### 7. Key Kernel APIs for Panel Drivers

```c
static int panel_prepare(struct drm_panel *panel) {
    /* Power on, reset sequence, send DCS init commands */
    mipi_dsi_dcs_set_display_on(dsi);
    return 0;
}

static int panel_enable(struct drm_panel *panel) {
    /* Final Display On, backlight enable */
    return 0;
}

static const struct drm_panel_funcs panel_funcs = {
    .prepare = panel_prepare,
    .enable  = panel_enable,
    .disable = panel_disable,
    .unprepare = panel_unprepare,
    .get_modes = panel_get_modes,
};

static int panel_probe(struct mipi_dsi_device *dsi) {
    struct panel_drv *drv = ...;
    mipi_dsi_set_drvdata(dsi, drv);
    drv->panel.funcs = &panel_funcs;
    return drm_panel_add(&drv->panel);
}
```

### 8. Debugging Tools & Tips

```bash
# List DSI devices & modes
cat /sys/class/drm/card*/card*/modes
dmesg | grep -i dsi

# Media controller graph (if using bridge)
media-ctl -p -d /dev/media0

# Force panel modes / timings
modetest -M drm -s <connector_id>@<mode_id>

# DSI packet tracing (if enabled)
echo 1 > /sys/kernel/debug/dri/0/i915_dsi_trace  # Intel
# or vendor-specific debugfs

# Common errors
- "no valid mode" → wrong timing in panel driver or DT
- "DCS NAK" → wrong command sequence or panel not powered
- "short read" → panel does not support readback
```

### 9. Modern Trends (2026)

- **C-PHY** adoption increasing (Qualcomm, MediaTek flagship SoCs)
- **Command Mode** still dominates for power efficiency
- **DSC** (Display Stream Compression) almost always enabled for 4K/120 Hz+
- **Panel Self-Refresh (PSR/PSR2/PSR-SU)** — widely used on laptops/phones
- **libcamera-style** userspace control for advanced panels (rare)

This cheatsheet covers the essentials for writing DSI panel drivers, debugging bring-up, or integrating displays on Linux embedded systems.

Good luck with your DSI panel integration!