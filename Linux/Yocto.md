Here is a concise **Yocto Project Cheat Sheet** (valid for recent branches as of early 2026 — Dunfell 3.1.x LTS, Kirkstone 4.0.x LTS, Mickledore 4.2.x / Scarthgap 5.0.x / Nanbield 5.1.x / upcoming 6.0.x).  
Yocto = Poky reference distro + OpenEmbedded Core + BitBake.

### 1. Quick Start – One-time Setup

```bash
# Clone Poky (reference distro)
git clone -b nanbield git://git.yoctoproject.org/poky
cd poky

# Initialize build environment (creates build/ if missing)
source oe-init-build-env [build-dir]   # usually just source oe-init-build-env

# Optional: add more layers (e.g. meta-openembedded, meta-yourboard)
git clone -b nanbield git://git.openembedded.org/meta-openembedded
bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-openembedded/meta-python
# ... add BSP layers, meta-custom, etc.
```

### 2. Core Configuration Files (in build/conf/)

File                | Purpose / Most common edits
--------------------|------------------------------------------------------
`local.conf`        | MACHINE, DISTRO, IMAGE_FEATURES, DL_DIR, SSTATE_DIR, parallel build settings
`bblayers.conf`     | List of active layers (BBLAYERS += "...")
`site.conf`         | (optional) global mirror / proxy / sstate settings
`buildhistory.conf` | Enable buildhistory (track size / package changes)

Common `local.conf` snippets (2025–2026 style):

```bash
MACHINE ?= "qemuarm64"                  # or raspberrypi5, imx8mp, etc.
DISTRO ?= "poky"                        # or poky-minimal, poky-musl
BB_NUMBER_THREADS = "16"                # ≈ cores
PARALLEL_MAKE = "-j 16"
DL_DIR ?= "${TOPDIR}/../downloads"
SSTATE_DIR ?= "${TOPDIR}/../sstate-cache"
IMAGE_FSTYPES += "tar.bz2 wic.xz"       # common outputs
IMAGE_FEATURES += "ssh-server-dropbear tools-sdk"
# For smaller images
# DISTRO_FEATURES:remove = "x11 wayland opengl"
# IMAGE_FEATURES:remove = "package-management"
```

### 3. Most Useful `bitbake` Commands

Command                                      | What it does
---------------------------------------------|---------------------------------------------------------------
`bitbake <recipe>`                           | Build recipe / package / image (e.g. `core-image-minimal`)
`bitbake <image> -c populate_sdk`            | Build SDK installer (eSDK or full SDK)
`bitbake -c devshell <recipe>`               | Open shell in work dir with env set up (very useful!)
`bitbake -c menuconfig virtual/kernel`       | Kernel config (linux-yocto or custom)
`bitbake -c menuconfig busybox`              | BusyBox config
`bitbake -c cleanall <recipe>`               | Nuclear clean (rm work/ + sstate)
`bitbake -c cleansstate <recipe>`            | Remove sstate cache entries
`bitbake -c fetchall <image>`                | Download everything needed for image
`bitbake-layers show-layers`                 | List active layers
`bitbake-layers show-recipes`                | List all available recipes
`bitbake-layers show-recipes -l <layer>`     | Recipes provided by one layer
`bitbake-layers show-appends`                | Which .bbappend files are applied to which recipes
`bitbake-layers show-overrides`              | Active OVERRIDES (MACHINE, DISTRO, ...)
`bitbake -g <image> -u depexp`               | Dependency explorer GUI
`bitbake -g <image>`                         | Generate pn-depends.dot / task-depends.dot (graphviz)

### 4. devtool – Workflow for Recipe / App Development (Highly Recommended)

Command                                      | Typical use-case
---------------------------------------------|-----------------------------------------------
`devtool modify <recipe>`                    | Create workspace copy + git repo for patching
`devtool modify -x new-recipe git://...`     | Import external source as new recipe
`devtool build <recipe>`                     | Build modified recipe
`devtool deploy-target <recipe> root@target-ip` | Copy built package to running target
`devtool finish <recipe> <your-layer>`       | Commit patches → .bbappend + move to layer
`devtool reset <recipe>`                     | Remove from workspace
`devtool upgrade <recipe>`                   | Attempt version upgrade + create patches
`devtool status`                             | Show workspace status

### 5. Layer & Recipe Creation Quick Commands

```bash
# Create new layer
bitbake-layers create-layer ../meta-mylayer

# Create skeleton recipe
bitbake-layers create-recipe ../meta-mylayer recipes-example/mypkg mypkg_1.0.bb

# Add your new layer
bitbake-layers add-layer ../meta-mylayer
```

**Recipe minimal skeleton** (mypkg_1.0.bb)

```bitbake
SUMMARY = "My example package"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://main.c"

S = "${WORKDIR}"

do_compile() {
    ${CC} ${CFLAGS} ${LDFLAGS} main.c -o mypkg
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 mypkg ${D}${bindir}
}
```

### 6. Common Variables & Snippets (copy-paste friendly)

```bitbake
# Append / prepend
SRC_URI:append = " file://my-patch.patch"
FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

# Override SRC_URI for machine
SRC_URI:append:raspberrypi5 = " file://rpi5-specific.cfg"

# Kernel fragment
SRC_URI += "file://myfeature.cfg"
KERNEL_FEATURES:append = " features/myfeature.scc"

# Add package to image
IMAGE_INSTALL:append = " packagegroup-core-full-cmdline strace"

# Disable systemd / use sysvinit
DISTRO_FEATURES:remove = " systemd"
VIRTUAL-RUNTIME_init_manager = "sysvinit"
```

### 7. Debugging & Inspection Quick Hits

Command / Tip                               | Use-case
--------------------------------------------|---------
`bitbake -e <recipe> | grep ^SRC_URI`     | See final SRC_URI after all appends
`bitbake -e <recipe> | grep ^FILESEXTRAPATHS` | Check patch search paths
`bitbake -D`                                 | Debug output (very verbose)
`bitbake-diffsigs sstate/.../*.sigdata.*`    | Compare sstate signatures (why rebuild?)
`oe-layerindex`                              | Web search for layers/recipes (oe-index)
`buildhistory-collect-srcrevs`               | Track git revisions used in buildhistory
`oe-pkgdata-util`                            | Query built packages (runtime depends, files, …)

### 8. Modern Tips (2025–2026)

- Prefer **devtool** for new code / modifications — much faster iteration
- Use **eSDK** (`bitbake -c populate_sdk`) for app developers
- Enable **buildhistory** + **oeqa** selftests for CI/CD
- Use **kas** / **repo** for multi-layer / multi-manifest projects
- Switch to **musl** (`DISTRO_FEATURES += "musl"`) for smaller & more secure images
- Current stable: Scarthgap (5.0) or Nanbield (5.1); check LTS status on yoctoproject.org
- Official quick start: https://docs.yoctoproject.org/brief-yoctoprojectqs/

Start with:  
`source oe-init-build-env` → edit `local.conf` (MACHINE=qemuarm64) → `bitbake core-image-minimal` → `runqemu`

Good luck building your embedded Linux! Most daily commands are `bitbake`, `devtool modify/build/finish`, and `bitbake-layers`.