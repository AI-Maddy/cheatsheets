**Yocto / BitBake Execution Cheat Sheet**  
(focused on the most common commands you actually type every day — Scarthgap/Nanbield era, 2025–2026)

### 1. Environment Setup (you do this every new terminal)

```bash
# Most common (Poky reference distro)
source oe-init-build-env [build-dir]          # default: build/

# Alternative names people use
source poky/oe-init-build-env
. oe-init-build-env
```

After this command you are inside the `build/` directory and the environment is sourced.

### 2. Most Frequently Used BitBake Commands

Command                                    | What you actually use it for                              | Frequency
-------------------------------------------|------------------------------------------------------------|---------
`bitbake <image>`                          | Build your final image (most common command)               | ★★★★★
`bitbake core-image-minimal`               | Quick test image                                           | ★★★★
`bitbake core-image-base`                  | Slightly more useful base image                            | ★★★★
`bitbake <recipe> -c devshell`             | Get a shell inside the work directory with env set up      | ★★★★★ (debugging king)
`bitbake <recipe> -c compile -f`           | Force recompile step (after editing source)                | ★★★★
`bitbake <recipe> -c cleanall`             | Nuclear clean — remove work/, sstate, downloads if needed  | ★★★
`bitbake <recipe> -c cleansstate`          | Remove sstate cache entries (lighter than cleanall)        | ★★★
`bitbake -c menuconfig virtual/kernel`     | Run kernel menuconfig                                      | ★★★
`bitbake -c menuconfig busybox`            | Configure busybox                                          | ★★
`bitbake -g <image>`                       | Generate dependency graphs (.dot files)                    | ★★
`bitbake -g -u depexp <image>`             | Open dependency explorer GUI                               | ★★ (when you have X11)
`bitbake -c populate_sdk <image>`          | Build full SDK installer                                   | ★★
`bitbake -c populate_sdk_ext <image>`      | Build extensible SDK (eSDK)                                | ★★ (app dev teams)

### 3. Quick Iteration & Debugging Patterns

```bash
# 1. Most common debug loop for recipe development
bitbake my-recipe -c devshell
# → inside devshell:
# edit sources, then
bitbake my-recipe -c compile -f   # or just exit and run from outside
bitbake my-recipe -c install -f
bitbake my-recipe                 # full build to test packaging

# 2. Force rebuild one step
bitbake busybox -c compile -f

# 3. See what changed / why rebuild happened
bitbake-diffsigs sstate/.../sigdata.*   # compare old vs new signature

# 4. Show final value of any variable
bitbake -e busybox | grep ^SRC_URI=
bitbake -e busybox | grep ^FILESEXTRAPATHS
bitbake -e core-image-minimal | grep ^IMAGE_INSTALL=

# 5. See which bbappends are active
bitbake-layers show-appends busybox
bitbake-layers show-appends linux-yocto

# 6. Quick layer inspection
bitbake-layers show-layers
bitbake-layers show-recipes -l meta-mylayer
```

### 4. devtool — The fastest way to develop / patch recipes (strongly recommended)

```bash
devtool modify busybox                      # create workspace copy + git repo
# → edit sources in sources/busybox/
devtool build busybox
devtool deploy-target busybox root@192.168.1.44
devtool finish busybox meta-mylayer         # commit patches → bbappend in your layer
devtool reset busybox                       # remove from workspace

devtool add mynewapp https://github.com/...
devtool upgrade openssl                     # attempt version bump
```

### 5. Build Control & Performance Flags (add to local.conf or command line)

```bash
# In local.conf or as BITBAKE variable
BB_NUMBER_THREADS = "16"           # ≈ number of CPU cores
PARALLEL_MAKE = "-j 16"

# One-liners when you are low on RAM / want to limit parallelism
bitbake world -j 4
BITBAKE_NO_NETWORK=1 bitbake core-image-minimal   # offline mode (after sources downloaded)

# Show tasks / progress more clearly
bitbake -v core-image-minimal
```

### 6. One-liners people actually type daily (2026)

```bash
# Quick test build
source oe-init-build-env && bitbake core-image-minimal && runqemu

# Debug kernel
bitbake virtual/kernel -c menuconfig
bitbake virtual/kernel -c compile -f

# Add package to image quickly
echo 'IMAGE_INSTALL:append = " strace dropbear"' >> conf/local.conf
bitbake core-image-minimal

# See dependency chain of a package
bitbake -g -u depexp busybox

# Clean + rebuild single recipe
bitbake mypkg -c cleanall && bitbake mypkg

# Build SDK for app developers
bitbake core-image-minimal -c populate_sdk
```

### 7. Quick Status / Help Commands

```bash
bitbake-layers show-layers
bitbake --help
bitbake -h                               # shorter
bitbake-layers --help
bitbake -e | grep ^DISTRO               # check current distro / machine etc.
```

**Golden Rule 2026**:  
When something breaks → first thing is almost always  
`bitbake <recipe> -c devshell`  
then edit → `bitbake <recipe> -c compile -f` from inside or outside.

Keep these 5–6 commands in your muscle memory:

- `bitbake <image>`
- `bitbake <recipe> -c devshell`
- `bitbake -c compile -f`
- `devtool modify / build / finish`
- `bitbake-layers show-appends`
- `bitbake -e | grep ^…`

Good luck with your builds!