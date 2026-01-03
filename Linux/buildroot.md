**Buildroot cheat sheet** 
(updated for 2025–2026 releases, e.g. 2025.11 LTS / 2026.02+).  
Buildroot remains a lightweight, fast tool for generating embedded Linux systems (toolchain + kernel + rootfs + bootloader).

### 1. Quick Start Workflow

```bash
# 1. Clone / update (use latest stable or git master)
git clone https://gitlab.com/buildroot.org/buildroot.git
cd buildroot
git checkout 2025.11   # or latest LTS / -b master

# 2. List available board defconfigs
make list-defconfigs | grep raspberry   # example filter

# 3. Load a board config (copies → .config)
make raspberrypi5_defconfig             # or qemu_aarch64_virt_defconfig etc.

# 4. Customize (most important step!)
make menuconfig                         # or nconfig / xconfig / gconfig

# 5. Build (downloads + toolchain + packages + images)
make -j$(nproc)                         # safe even without per-package dirs

# 6. Output is here
ls output/images/                       # kernel, rootfs.*, sdcard.img, etc.
```

### 2. Most Useful `make` Targets (cheat sheet core)

Target                              | Purpose
------------------------------------|------------------------------------------------------
`make menuconfig` / `nconfig`       | Main configuration (Kconfig style)
`make savedefconfig`                | Save minimal config → `configs/your_board_defconfig`
`make defconfig`                    | Apply a defconfig (e.g. `make qemu_arm_versatile_defconfig`)
`make`                              | Full build
`make sdk`                          | Build relocatable SDK (great for app dev)
`make legal-info`                   | Generate license/copyright report (mandatory for products)
`make show-info`                    | JSON dump of enabled packages + licenses
`make pkg-stats`                    | CVE / package stats (HTML + JSON)
`make clean`                        | Remove almost everything (keep dl/ & configs)
`make distclean`                    | Nuclear: remove **everything**
`<pkg>`                             | Build only this package (e.g. `make busybox`)
`<pkg>-clean`                       | `make dropbear-clean`
`<pkg>-dirclean`                    | Remove build dir → force full rebuild of pkg
`<pkg>-reconfigure`                 | Re-run configure step
`<pkg>-rebuild`                     | Rebuild + reinstall
`linux-rebuild` / `uboot-rebuild`   | Fast kernel / u-boot rebuild
`linux-update-defconfig`            | Save current kernel .config → defconfig fragment

### 3. Configuration Sections (menuconfig main menu)

Section                          | Common Options / Tips
---------------------------------|--------------------------------------------------------------------------------
**Target options**               | Architecture, variant, endianness, CPU tuning
**Toolchain**                    | Internal (buildroot builds it) vs External (prebuilt, e.g. Bootlin / Linaro)
                                 | C library: glibc / musl / uClibc-ng (musl is very popular 2025+)
**System configuration**         | Root password, hostname, init system (busybox / systemd / none)
                                 | /dev management: devtmpfs + eudev / busybox mdev
**Kernel**                       | Version, custom config / defconfig / fragments
**Bootloaders**                  | U-Boot, barebox, grub, none
**Target packages**              | → BusyBox (coreutils), → Networking, → Filesystem utilities, → Libraries…
**Filesystem images**            | ext4 / squashfs / initramfs / tar / iso9660 / sdcard.img
**Boot from network / initramfs**| Useful for quick testing (BR2_TARGET_ROOTFS_INITRAMFS)

### 4. Output Directory Structure (after build)

Path                              | Content
----------------------------------|-----------------------------------------------
`output/images/`                  | Final artifacts: zImage, rootfs.tar, sdcard.img, ...
`output/target/`                  | Populated root filesystem (stripped)
`output/staging/`                 | Sysroot with headers & libs (for SDK / app cross-compile)
`output/host/`                    | Host tools (gcc, pkg-config wrapper, etc.)
`output/build/<pkg>-<ver>/`       | Package build directory
`output/dl/`                      | Downloaded sources (reuse between builds)
`output/sdk/`                     | Relocatable SDK when `make sdk`

### 5. Advanced / Common Patterns (2025–2026)

**Use external (prebuilt) toolchain**  
→ Toolchain → External toolchain → Bootlin toolchain (very reliable)

**Custom kernel config**  
```bash
make linux-menuconfig          # edit kernel .config
make linux-update-defconfig    # save minimal fragment
# Then in menuconfig: Kernel → Custom configuration file → use fragments
```

**Add post-build script** (overlay files, custom tweaks)  
→ System configuration → Root FS skeleton → Custom skeleton directories  
→ or → Root FS overlay directories (easiest)

**Per-package directories (parallel -jN safe)**  
Enable in menuconfig:  
→ Advanced → Per-package directories (newer kernels / safer rebuilds)

**Offline build**  
```bash
make source        # download everything first
# Later (no net): make
```

**Rebuild only rootfs (fast iteration)**  
```bash
rm -rf output/target/ output/images/rootfs*
make
```

### 6. Quick Debugging & Inspection

Command                                      | What it does
---------------------------------------------|--------------------------------------
`make show-info \| jq .`                     | Pretty JSON of packages
`make graph-depends`                         | dependency graph (needs graphviz)
`make graph-build`                           | build time graph
`output/host/usr/bin/<arch>-pkg-config --list-all` | See available libs
`./output/images/rootfs.tar`                 | Inspect content (tar -tvf)
`make legal-info` → `output/legal-info/`     | Licenses + hashes + sources

### 7. Modern Tips (2025–2026)

- Prefer **musl** libc for small & secure images (very mature now)
- Use **2025.02 / 2025.11 LTS** releases for production
- External Bootlin toolchains are excellent and frequently updated
- For fast iteration → enable `BR2_CCACHE` + SSD + per-package dirs + `-j$(nproc)`
- Add your own packages via `package/yourpkg/` (simple .mk + Config.in)
- Use `BR2_GLOBAL_PATCH_DIR` for custom patches on any package
- Initramfs + qemu is fastest way to test: `make qemu_aarch64_virt_defconfig && make`

Good luck with your embedded Linux images!  
Start with `make qemu_x86_64_defconfig && make` — you get a bootable system in <10 min on a decent machine.  
Official manual: https://buildroot.org/downloads/manual/manual.html (or `make manual-pdf`).