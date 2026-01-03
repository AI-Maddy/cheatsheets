**practical Linux framebuffer cheat sheet** (fbdev, /dev/fb* devices) focused on the most useful commands and techniques in 2025–2026 (still relevant on embedded systems, minimal installs, recovery, kiosk setups, and some servers).

### Quick Quick-Reference Table

| Purpose                        | Command / Example                                            | Needs root? | Notes / Common use case                              |
|-------------------------------|------------------------------------------------------------------|-------------|------------------------------------------------------|
| Show current resolution & mode | `fbset` or `fbset -s`                                            | Usually no  | Most important command                               |
| Show detailed fb info          | `fbset -i`                                                       | No          | Driver name, geometry, timings, accel, etc.          |
| List available modes           | `cat /sys/class/graphics/fb0/modes`                              | No          | On modern kernels (KMS-based)                        |
| Change resolution (simple)     | `fbset 1280x720`                                                 | Yes         | Works if mode exists                                 |
| Change depth (e.g. 16→32 bit)  | `fbset -depth 32`                                                | Yes         | Rarely needed today                                  |
| Set custom mode (one-liner)    | `fbset "1920x1080-60" -xres 1920 -yres 1080 -vxres 1920 -vyres 1080 -depth 32` | Yes | Useful on embedded/legacy hardware                   |
| Show mode in Xorg format       | `fbset -x`                                                       | No          | Copy-paste friendly for Xorg.conf                    |
| Clear screen (black)           | `dd if=/dev/zero of=/dev/fb0 bs=1M`                              | Yes         | Fast & brutal                                        |
| Random pixel noise (test)      | `cat /dev/urandom > /dev/fb0` <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop | Yes | Classic framebuffer is alive test                    |
| Draw single pixel (red, 32bpp) | `printf '\x00\x00\xff\xff' | dd of=/dev/fb0 bs=4 seek=$((y*bytes_per_line + x*4))` | Yes | y×stride + x×bytespp offset                          |
| Show framebuffer device info   | `cat /sys/class/graphics/fb0/name`                               | No          | Usually simplefb / radeondrmfb / efifb / vesafb etc. |
| Which console → fb mapping     | `con2fbmap` or `con2fbmap 1`                                     | Yes         | Useful with multiple fb devices                      |
| Map console 1 → fb1            | `con2fbmap 1 1`                                                  | Yes         | Embedded / multi-monitor setups                      |

### Most Commonly Used Tools That Draw to Framebuffer

| Tool       | Purpose                               | Install (Debian/Ubuntu)     | Example                                      | Still maintained 2025? |
|------------|----------------------------------------|------------------------------|----------------------------------------------|------------------------|
| `fbi`      | Fast framebuffer image viewer          | `apt install fbi`            | `fbi -T 1 photo.jpg`                         | Yes (low activity)     |
| `fim`      | fbi improved (better keys, zoom, etc.) | `apt install fim`            | `fim --help`                                 | Yes                    |
| `fbv`      | Very simple image viewer               | `apt install fbv`            | `fbv -ciuker image.png`                      | No (but still works)   |
| `fbterm`   | Fast framebuffer terminal (256 colors, fontconfig) | `apt install fbterm` | `fbterm`                                     | Yes (forks exist)      |
| `yaft`     | Modern UTF-8 framebuffer terminal      | Compile or find package      | `yaft`                                       | Yes (active)           |

### Quick How-To Snippets

**1. Test if framebuffer works at all**

```bash
sudo dd if=/dev/urandom of=/dev/fb0 bs=4M count=1 status=progress
# Press Ctrl+C quickly to stop the mess
```

**2. Show nice image from console (no X)**

```bash
sudo apt install fbi
sudo fbi --noverbose --autozoom --once beautiful-sunset.jpg
```

**3. Run better-looking console (fbterm)**

```bash
# Optional: background image first
fbv -ciuker wallpaper.jpg <<< q
export FBTERM_BACKGROUND_IMAGE=1

fbterm --font-size=16
# or with better font
fbterm -f "DejaVu Sans Mono:size=15"
```

**4. One-liner pixel test (blue-ish pixel near top-left – 32 bpp)**

```bash
# x=100, y=50, assuming 1920×1080 stride ≈ 7680 bytes
printf '\x80\xff\x40\xff' | sudo dd of=/dev/fb0 bs=4 seek=$((50*7680 + 100*4))
```

**5. Restore console after messing up (most cases)**

```bash
sudo chvt 1    # switch to console 1
# or just reboot if really broken
```

### Quick Tips – 2025 Reality Check

- On modern desktops → **framebuffer is usually emulated via simpledrm / efifb / vesafb**  
  (real hw fbdev mostly dead except embedded & some servers)
- Inside Xorg/Wayland → writing to /dev/fb* usually has **no effect** (compositor owns the display)
- Best remaining use-cases in 2025–2026:  
  • Embedded devices / IoT screens  
  • Recovery / minimal installs  
  • Kiosk / signage systems  
  • Retro/minimalist terminals (yaft, fbterm)

Stay safe — **never** write to /dev/fb* without knowing the current mode & pixel format (use `fbset -i` first).

Happy frame-buffering! 🖼️