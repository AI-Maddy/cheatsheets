**Yocto / BitBake Recipe (.bb / .bbappend) Cheat Sheet**  
(oriented toward modern Yocto releases — Mickledore 4.2 / Scarthgap 5.0 / Nanbield 5.1 / upcoming 6.0 as of early 2026)

📌 1. Minimal Recipe Skeleton (.bb)

.. code-block:: bitbake

================================================================================
mypkg_1.2.3.bb
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



SUMMARY = "Short one-line description"
DESCRIPTION = "Longer description (optional)"
AUTHOR = "Your Name <you@example.com>"
HOMEPAGE = "https://example.com/mypkg"
BUGTRACKER = "https://github.com/vendor/mypkg/issues"

LICENSE = "MIT | Apache-2.0 | GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://LICENSE;md5=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

================================================================================
SRC_URI can point to tarball, git, local files, etc.
================================================================================

SRC_URI = "\
    git://github.com/vendor/mypkg.git;protocol=https;branch=main \
    file://0001-fix-build.patch \
    file://mypkg.service \
"

================================================================================
For git SRC_URI — mandatory
================================================================================

SRCREV = "abcdef1234567890..."          # or "${AUTOREV}" for HEAD
PV = "1.2.3+git${SRCPV}"

S = "${WORKDIR}/git"                    # default for git sources

================================================================================
⚙️ Optional: inherit helpers
================================================================================

inherit autotools pkgconfig systemd meson cmake update-rc.d

================================================================================
For systemd units
================================================================================

SYSTEMD_SERVICE:${PN} = "mypkg.service"
SYSTEMD_AUTO_ENABLE = "enable"

================================================================================
Packaging (what files go where)
================================================================================

FILES:${PN} += "\
    ${bindir}/mypkg \
    ${systemd_system_unitdir}/mypkg.service \
"
FILES:${PN}-dev += "${includedir}/mypkg/*.h"

================================================================================
Runtime dependencies
================================================================================

DEPENDS = "openssl zlib libcurl"        # build-time
RDEPENDS:${PN} = "bash coreutils"       # runtime

================================================================================
⚙️ Optional: split into sub-packages
================================================================================

PACKAGES =+ "${PN}-tools ${PN}-examples"
FILES:${PN}-tools = "${bindir}/mypkg-tool*"
RDEPENDS:${PN}-tools = "${PN}"

================================================================================
Build steps overrides (only when needed)
================================================================================

do_configure:prepend() {
    # sed, cp, etc before configure
}

do_compile:append() {
    # extra build steps
}

do_install:append() {
    install -d ${D}${sysconfdir}/init.d
    install -m 0755 ${WORKDIR}/initscript ${D}${sysconfdir}/init.d/mypkg
}

⭐ 📚 2. Most Important Variables Quick Reference

Category              | Variable                  | Typical value / example
----------------------|---------------------------|---------------------------
**Identity**          | ``SUMMARY``                 | One line
``DESCRIPTION``         | Multi-line (optional)
``LICENSE``             | ``MIT``, ``GPL-2.0-or-later``, ``BSD-3-Clause``, etc.
``LIC_FILES_CHKSUM``    | ``file://COPYING;md5=...``
**Source**            | ``SRC_URI``                 | git://… or https://…tar.gz
``SRCREV``              | commit hash or tag
``PV``                  | version (auto-derived from recipe name or set manually)
``S``                   | source dir (usually ``${WORKDIR}/git``)
**Build**             | ``inherit``                 | ``autotools``, ``meson``, ``cmake``, ``cargo``, ``qmake``, ``update-rc.d``, ``systemd``, ``pkgconfig``
``DEPENDS``             | build-time deps
``EXTRA_OECONF``        | ``./configure`` flags
``EXTRA_OEMESON``       | meson setup flags
``EXTRA_OECMAKE``       | cmake flags
**Install / Packaging** | ``do_install()``          | ``install -d``, ``install -m``
``FILES:${PN}``         | files → main package
``FILES:${PN}-dev``     | headers → -dev
``PACKAGES``            | additional sub-packages
``RDEPENDS:${PN}``      | runtime depends
``RRECOMMENDS:${PN}``   | optional recommends
**Systemd**           | ``SYSTEMD_SERVICE:${PN}``   | ``foo.service bar.socket``
``SYSTEMD_AUTO_ENABLE`` | ``enable`` / ``disable``
**Init scripts**      | ``INITSCRIPT_NAME``         | for update-rc.d
``INITSCRIPT_PARAMS``   | ``"defaults 70"``

🏗️ 3. Common .bbappend Patterns (in your layer)

.. code-block:: bitbake

================================================================================
mypkg_%.bbappend
================================================================================

================================================================================
Add patch / config / extra file
================================================================================

FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
SRC_URI:append = " file://0001-my-company-fix.patch"
SRC_URI:append = " file://myconfig.conf"

================================================================================
Machine / distro specific
================================================================================

SRC_URI:append:raspberrypi5 = " file://rpi5-tuning.patch"
SRC_URI:append:class-target = " file://target-only.patch"

================================================================================
Change configure flags
================================================================================

EXTRA_OECONF:append = " --enable-featureX"
EXTRA_OEMESON:append = " -Dfeature-y=enabled"

================================================================================
Add runtime dependency
================================================================================

RDEPENDS:${PN}:append = " packagegroup-core-base"

================================================================================
Override install step
================================================================================

do_install:append() {
    rm -f ${D}${bindir}/debug-tool      # remove unwanted binary
}

================================================================================
Add new subpackage
================================================================================

PACKAGES += "${PN}-firmware"
FILES:${PN}-firmware = "${nonarch_base_libdir}/firmware/mypkg/*"

🐛 4. Quick Recipe Creation / Debugging Commands

Command                                   | Purpose
------------------------------------------|-----------------------------------------------
``devtool modify mypkg``                    | Edit sources in workspace (recommended)
``devtool build mypkg``                     | Build modified recipe
``devtool finish mypkg meta-mylayer``       | Commit patches → .bbappend
``bitbake mypkg -c devshell``               | Shell with env (CC, CFLAGS, etc) set
``bitbake mypkg -e | grep ^SRC_URI=``       | See final SRC_URI
``bitbake mypkg -e | grep ^FILESEXTRAPATHS`` | Check patch search path
``bitbake -c cleanall mypkg``               | Full clean
``bitbake mypkg -c fetchall``               | Download sources only
``bitbake-layers show-appends mypkg``       | Which .bbappends are active
``bitbake -g mypkg``                        | Generate dependency graphs

💡 5. Modern 🟢 🟢 Best Practices (2025–2026)

- Always use ``devtool`` for new packages or modifications — fastest workflow
- Prefer ``inherit meson`` or ``cmake`` over autotools when possible
- Use ``ref-classes`` helpers: ``update-alternatives``, ``binconfig``, ``gettext``, ``perlnative``
- Keep ``LIC_FILES_CHKSUM`` accurate (use ``md5sum`` or ``sha256sum``)
- 🔴 🔴 Avoid ``do_install:prepend/append`` when you can use ``install`` in recipe
- For git sources: prefer tag-based ``SRCREV`` over ``${AUTOREV}``
- Use ``:prepend`` / ``:append`` / ``:remove`` syntax for overrides (modern style)
- Enable ``INSANE_SKIP:${PN} += "already-stripped"`` only when really needed
- Test packaging with ``bitbake -c populate_sdk my-image``

📌 6. One-liners & Snippets

.. code-block:: bitbake

================================================================================
Add local patch directory
================================================================================

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

================================================================================
⚙️ Conditional append
================================================================================

SRC_URI:append:class-native = " file://native-fix.patch"

================================================================================
🐛 Disable stripping (debugging)
================================================================================

INSANE_SKIP:${PN} += "already-stripped"

================================================================================
⚙️ Runtime recommendation (not hard dependency)
================================================================================

RRECOMMENDS:${PN} += "kernel-module-xyz"

🟢 🟢 Good luck writing Yocto recipes!  
Most new recipes in 2026 follow: ``SRC_URI`` (git preferred) → ``inherit meson/cmake/autotools`` → ``do_install()`` → ``FILES:${PN}``.  
Start with ``devtool add`` / ``devtool modify`` — they generate 80% of the boilerplate for you.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
