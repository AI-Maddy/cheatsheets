**Buildroot Commands Cheat Sheet**  
(oriented toward daily usage in 2025–2026, tested on recent releases like 2025.02 / 2025.08 / 2025.11 LTS / 2026.02+)

### 1. Core Configuration & Defconfig Commands

Command                                      | What it does
---------------------------------------------|---------------------------------------------------------------
`make list-defconfigs`                       | Show all available board / qemu / vendor defconfigs
`make <board>_defconfig`                     | Apply board config (e.g. `make raspberrypi5_defconfig`)
`make qemu_aarch64_virt_defconfig`           | Quick test on QEMU aarch64
`make menuconfig` / `make nconfig`           | Open main Buildroot configuration (Kconfig style)
`make savedefconfig`                         | Save current .config as minimal defconfig → `defconfig`
`make defconfig BR2_DEFCONFIG=myfile`        | Load external defconfig file (not in configs/ folder)
`make olddefconfig`                          | Update .config with new defaults (after upgrading Buildroot)

### 2. Build & Clean Targets

Command                                      | Purpose / Speed
---------------------------------------------|-----------------------------------------------
`make`                                       | Full build (toolchain + kernel + rootfs + images)
`make -j$(nproc)`                            | Parallel build (almost always safe)
`make all`                                   | Same as plain `make`
`make world`                                 | Build everything (same as default target)
`make sdk`                                   | Build relocatable SDK (~ toolchain + sysroot)
`make source`                                | Download all sources (good for offline later)
`make clean`                                 | Remove output/ (except dl/ and .config)
`make distclean`                             | Nuclear option — remove everything
`make legal-info`                            | Generate license report (output/legal-info/)

### 3. Package-specific Targets (very frequent)

Command                                      | Effect
---------------------------------------------|-----------------------------------------------
`make busybox`                               | Build & install only busybox
`make linux`                                 | Build kernel only
`make uboot`                                 | Build bootloader only
`make dropbear`                              | Build only dropbear (SSH server)
`make <pkg>-clean`                           | Remove build & staging/install dirs of pkg
`make <pkg>-dirclean`                        | Remove entire build directory of pkg
`make <pkg>-reconfigure`                     | Re-run configure step of pkg
`make <pkg>-rebuild`                         | Force rebuild & reinstall of pkg
`make <pkg>-show-depends`                    | Show dependency tree of this package
`make show-depends`                          | Show full dependency graph (needs graphviz)

### 4. Kernel & Bootloader Fast Iteration

Command                                      | Typical use-case
---------------------------------------------|-----------------------------------------------
`make linux-menuconfig`                      | Edit kernel .config
`make linux-update-defconfig`                | Save current kernel config → fragments
`make linux-rebuild`                         | Rebuild kernel (fast if only .config changed)
`make linux-reconfig`                        | Re-run kernel configure step
`make uboot-menuconfig`                      | Edit U-Boot config
`make uboot-rebuild`                         | Rebuild U-Boot

### 5. Debugging & Inspection Commands

Command                                      | What you get
---------------------------------------------|-------------------------------------------------
`make show-info`                             | JSON dump of enabled packages, versions, licenses
`make pkg-stats`                             | CVE status + package statistics (HTML output)
`make graph-depends`                         | PNG dependency graph (requires graphviz)
`make graph-build`                           | Build-time graph (very useful for optimization)
`make graph-size`                            | Size contribution per package (output/build-size/)
`make printvars VARS=BR2_`                   | Show all BR2_ variables matching pattern
`make printvars PKG=LINUX`                   | Show all variables for the linux package
`make -s show-info | jq .`               | Pretty-print package list (if jq installed)

### 6. Output & Image Manipulation Quick Commands

Directory / File                             | Typical content
---------------------------------------------|-----------------------------------------------
`output/images/`                             | Final sdcard.img, rootfs.tar, zImage, rootfs.ext4…
`output/target/`                             | Populated (stripped) root filesystem
`output/staging/`                            | Headers + libs (sysroot for cross-compiling apps)
`output/host/`                               | Host cross-tools (gcc, pkg-config wrapper…)
`output/sdk/`                                | Relocatable SDK (after `make sdk`)

Quick inspection:
```bash
ls -lh output/images/               # see image sizes
tar tvf output/images/rootfs.tar    # list content of tarball
find output/target/ -name "*init*"  # find init system files
```

### 7. One-liners / Power User Patterns

```bash
# Quick qemu test (most common fast path)
make qemu_x86_64_defconfig && make -j$(nproc) && output/images/start-qemu.sh

# Force rebuild rootfs only (very fast for userspace changes)
rm -rf output/target/ output/images/rootfs* && make

# Offline build preparation
make source && tar czf sources.tar.gz dl/ && # later on air-gapped machine:
tar xzf sources.tar.gz && make

# Show which packages depend on openssl
make -s show-depends | grep -i openssl

# Update all defconfigs after Buildroot upgrade
for f in configs/*_defconfig; do make ${f##*/} && make savedefconfig && mv defconfig $f; done
```

### Quick Reference Table – Most Used Commands

Priority | Command                            | When / Why
---------|------------------------------------|-----------------------------------------------
1        | `make menuconfig`                  | Almost every session starts here
2        | `make <board>_defconfig`           | Start from known-good board
3        | `make -j$(nproc)`                  | Build everything
4        | `make linux-rebuild`               | Kernel tweak iteration
5        | `make <pkg>-dirclean && make`      | Package is broken / force clean rebuild
6        | `make legal-info`                  | Preparing for release / compliance
7        | `make sdk`                         | Need to build apps outside Buildroot

Keep `make help | grep -iE 'clean|rebuild|config|graph|show'` handy — it lists many more niche targets.

Happy building!  
Most daily work is: load defconfig → menuconfig → make -j → test in qemu → repeat.