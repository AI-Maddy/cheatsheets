**Yocto Layer Creation Guide / Cheat Sheet**  
(oriented toward modern Yocto releases: Scarthgap 5.0, Nanbield 5.1, upcoming 6.0 – as of 2026)

📌 1. Why Create a Custom Layer?

Common reasons:
- Add your own applications/recipes
- BSP customizations (kernel, u-boot, device tree, firmware)
- Machine configuration overrides
- Distro policy / configuration fragments
- Company branding / packaging rules
- Meta layers for third-party software (opencv, qt, docker, etc.)

⚙️ 2. Recommended Layer Naming Convention (2025–2026)

Prefix     | Purpose                          | Example
-----------|----------------------------------|-----------------------------
``meta-``    | Most common                      | ``meta-mylayer``, ``meta-company``
``meta-bsp-``| Board Support Package            | ``meta-raspberrypi``, ``meta-ti``
``meta-oe-`` | OpenEmbedded style extensions    | ``meta-python``, ``meta-multimedia``
``meta-`` + product/company | Proprietary / product-specific | ``meta-acme-prod``

⚙️ 3. Quick Creation (Most Common Way – Recommended)

.. code-block:: bash

================================================================================
1. Go to your sources directory (outside poky/)
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



cd ..   # so you're next to poky/

================================================================================
2. Create the layer skeleton
================================================================================

bitbake-layers create-layer meta-mylayer

================================================================================
This creates:
================================================================================

================================================================================
meta-mylayer/
================================================================================

================================================================================
├── conf/
================================================================================

================================================================================
│   └── layer.conf
================================================================================

================================================================================
💻 ├── recipes-example/
================================================================================

================================================================================
💻 │   └── example/
================================================================================

================================================================================
💻 │       ├── example.bb
================================================================================

================================================================================
│       └── files/
================================================================================

================================================================================
└── COPYING.MIT
================================================================================

⭐ 📌 4. Edit ``conf/layer.conf`` (Important!)

⭐ Most important lines to customize:

.. code-block:: bitbake

================================================================================
We have a conf and classes directory, add to BBPATH
================================================================================

BBPATH .= ":${LAYERDIR}"

================================================================================
We have recipes-* directories, add to BBFILES
================================================================================

BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
            ${LAYERDIR}/recipes-*/*/*.bbappend"

BBFILE_COLLECTIONS += "mylayer"
BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
BBFILE_PRIORITY_mylayer = "10"           # higher = wins over lower priority

================================================================================
⚙️ Optional – useful when you have machine-specific overrides
================================================================================

LAYERDEPENDS_mylayer = "core"

================================================================================
⚙️ Optional – if your layer provides BSP/machine support
================================================================================

================================================================================
BBFILES += "${LAYERDIR}/conf/machine/*.conf"
================================================================================

================================================================================
BBFILES += "${LAYERDIR}/conf/machine/include/*.inc"
================================================================================

📌 5. Add the Layer to Your Build

Two ways (pick one):

**Way A – Recommended (persistent)**

.. code-block:: bash

bitbake-layers add-layer ../meta-mylayer

→ Adds line to ``build/conf/bblayers.conf``

**Way B – One-time / testing**

.. code-block:: bash

================================================================================
Just edit build/conf/bblayers.conf manually and add:
================================================================================

BBLAYERS += "${TOPDIR}/../../meta-mylayer"

Verify:

.. code-block:: bash

bitbake-layers show-layers

📌 6. Typical Directory Structure You Will Create

.. code-block:: text

meta-mylayer/
├── conf/
│   ├── layer.conf
│   ├── distro/
│   │   └── mydistro.conf          (optional)
│   └── machine/
│       └── myboard.conf           (optional)
├── recipes-bsp/
│   ├── linux/
│   │   └── linux-yocto_%.bbappend
│   └── images/
│       └── my-image.bb
├── recipes-core/
│   └── images/
│       └── core-image-myminimal.bbappend
├── recipes-example/
│   └── myapp/
│       ├── myapp_1.0.bb
│       └── files/
│           ├── myapp.service
│           └── 0001-fix-build.patch
├── recipes-kernel/
│   └── kernel-fragments/
│       └── myfeatures.cfg
└── recipes-support/
    └── mylib/
        └── mylib_git.bb

🏗️ 7. Most Common Layer Contents & Creation Patterns

Task                               | Command / Pattern
-----------------------------------|-------------------------------------------------
New application recipe             | ``devtool add myapp https://github.com/…`` or manual .bb
Modify existing recipe             | ``devtool modify busybox`` → edit → ``devtool finish busybox meta-mylayer``
Kernel config fragment             | Create ``recipes-kernel/linux/linux-yocto/tune.cfg`` + ``.bbappend``
Machine config                     | ``conf/machine/myboard.conf`` + ``MACHINEOVERRIDES``
Distro policy                      | ``conf/distro/mydistro.conf`` + ``DISTRO = "mydistro"``
Systemd service + recipe           | ``inherit systemd``, ``SYSTEMD_SERVICE:${PN} = "my.service"``
Append to image                    | ``recipes-core/images/core-image-base.bbappend`` → ``IMAGE_INSTALL:append = " mypkg"``
Append to kernel                   | ``recipes-kernel/linux/linux-yocto_%.bbappend`` → ``SRC_URI += "file://my.patch"``

🐛 8. Quick Validation & Debugging Commands

.. code-block:: bash

================================================================================
See what your layer provides / overrides
================================================================================

bitbake-layers show-recipes -l meta-mylayer
bitbake-layers show-appends

================================================================================
Check if a recipe is affected by your bbappend
================================================================================

bitbake-layers show-appends busybox

================================================================================
See final variable value
================================================================================

bitbake -e busybox | grep ^SRC_URI=

================================================================================
🟢 ✅ 🟢 🟢 ✅ Test build of your new recipe
================================================================================

bitbake myapp

================================================================================
🟢 ✅ 🟢 🟢 ✅ Test image with your additions
================================================================================

bitbake core-image-minimal

💡 9. Modern 🟢 🟢 Best Practices (2026)

- Always use **devtool** for new recipes and modifications (fastest & cleanest)
- Prefer **git sources** with fixed ``SRCREV`` over tarballs when possible
- Use **.bbappend** instead of copying whole .bb files
- Keep layer priority reasonable (6–12 range)
- Use **FILESEXTRAPATHS:prepend** correctly in .bbappends
- Add **LAYERDEPENDS** if your layer depends on meta-openembedded / meta-python etc.
- Version your layer (add ``LAYERVERSION_mylayer = "1"`` in layer.conf)
- Include **COPYING.MIT** or appropriate license file
- Use **kas** / **repo** manifests for multi-layer projects

🟢 🟢 ✅ 10. One-liner Creation + Add + Test

.. code-block:: bash

bitbake-layers create-layer ../meta-testlayer
bitbake-layers add-layer ../meta-testlayer
bitbake-layers create-recipe ../meta-testlayer recipes-example/hello hello_1.0.bb
bitbake hello

You now have a working custom layer!

🟢 🟢 Good luck with your Yocto layers!  
Most new layers in 2026 start with ``bitbake-layers create-layer``, then ``devtool add/modify``, and grow from there. Keep it minimal at first — add complexity only when needed.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
