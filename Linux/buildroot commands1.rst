**Buildroot Commands Cheat Sheet – Focus on Fetch / Patch / Configure / Build / Install Phases**  
(oriented toward package-level development and debugging in 2025–2026 releases)

⚙️ 1. Main Package Build Phases (Order of Execution)

Phase          | What happens (generic infrastructure)                  | Stamp file created                  | Typical override variable
---------------|--------------------------------------------------------|-------------------------------------|---------------------------
**fetch**      | Download tarball / git clone / local copy              | ``.stamp_downloaded``                 | ``<pkg>_SITE``, ``<pkg>_SOURCE``
**extract**    | Unpack tarball / rsync local dir                       | ``.stamp_extracted``                  | ``<pkg>_EXTRACT_CMDS``
**rsync**      | (local/OVERRIDE_SRCDIR only) sync source → build dir   | ``.stamp_rsynced``                    | ``<pkg>_POST_RSYNC_HOOKS``
**patch**      | Apply .patch files + global patches + downloaded patches | ``.stamp_patched``                 | ``<pkg>_PATCH``, patches dir
**configure**  | Run ./configure / cmake / meson setup / …              | ``.stamp_configured``                 | ``<pkg>_CONFIGURE_CMDS``
**build**      | Run make / ninja / cargo build / …                     | ``.stamp_built``                      | ``<pkg>_BUILD_CMDS``
**install**    | Install to staging (``output/staging``) + target (``output/target``) | ``.stamp_installed`` / ``.stamp_target_installed`` | ``<pkg>_INSTALL_TARGET_CMDS``, ``<pkg>_INSTALL_STAGING_CMDS``

**Host packages** follow almost the same flow but install to ``output/host/``.

🐛 2. Package-level Make Targets (most useful for debugging)

Target                              | What it (re)does                                                                 | Typical use case
------------------------------------|----------------------------------------------------------------------------------|----------------------
``make <pkg>``                        | Fetch → extract → patch → configure → build → install (target + staging if needed) | Build/rebuild one package + deps
``make <pkg>-fetch``                  | Only download sources (or copy local)                                            | Test download / offline prep
``make <pkg>-source``                 | Alias for ``<pkg>-fetch``                                                          | —
``make <pkg>-extract``                | Extract + rsync (if local)                                                       | Check unpack result
``make <pkg>-patch``                  | Apply all patches (including PRE/POST hooks)                                     | Debug patch application
``make <pkg>-configure``              | Run configure step only                                                          | Test configure flags / errors
``make <pkg>-build``                  | Run build step only                                                              | Fast rebuild after source edit
``make <pkg>-install``                | Run install step (target + staging if enabled)                                   | Test install rules
``make <pkg>-install-staging``        | Install only to staging/sysroot                                                  | For libraries/headers
``make <pkg>-install-target``         | Install only to target rootfs                                                    | For final binaries
``make <pkg>-reconfigure``            | Force re-run configure step (keeps build dir)                                    | Change config flags quickly
``make <pkg>-rebuild``                | Re-run build + install (after source/patch change)                               | Fast iteration
``make <pkg>-reinstall``              | Re-run install step only                                                         | Fix install bugs
``make <pkg>-clean``                  | Remove build + install artifacts (keep download)                                 | Clean before retry
``make <pkg>-dirclean``               | Remove entire package build directory → full re-fetch/extract/patch              | Nuclear reset for one pkg

Replace ``<pkg>`` with real name, e.g. ``busybox``, ``linux``, ``dropbear``, ``openssl``, ``libcurl``, or your custom ``myfoo``.

📌 3. Pre- and Post- Hooks (Most Common)

Hook variable                           | When executed                              | Typical use-case
----------------------------------------|--------------------------------------------|----------------------
``<pkg>_PRE_DOWNLOAD_HOOKS``              | Before fetch                               | Rare (custom download prep)
``<pkg>_POST_DOWNLOAD_HOOKS``             | After fetch, before extract                | Verify hash, unpack extra archives
``<pkg>_PRE_RSYNC_HOOKS``                 | Before rsync (local source only)           | Prepare local tree
``<pkg>_POST_RSYNC_HOOKS``                | After rsync (local/OVERRIDE_SRCDIR only)   | Fix permissions, remove .git, add files
``<pkg>_PRE_PATCH_HOOKS``                 | Before normal patching                     | Apply special patches first (e.g. kernel RT-patch before others)
``<pkg>_POST_PATCH_HOOKS``                | After all patches applied                  | Fixup sources, sed replacements, generate files
``<pkg>_PRE_CONFIGURE_HOOKS``             | Before configure                           | Set env vars, create config.cache
``<pkg>_POST_CONFIGURE_HOOKS``            | After configure                            | Patch Makefile, fix libtool
``<pkg>_PRE_BUILD_HOOKS``                 | Before build                               | Rare
``<pkg>_POST_BUILD_HOOKS``                | After build, before install                | Strip extra files, run tests
``<pkg>_PRE_INSTALL_HOOKS``               | Before install (both staging & target)     | Rare
``<pkg>_POST_INSTALL_STAGING_HOOKS``      | After staging install                      | Install extra headers / .pc files
``<pkg>_POST_INSTALL_TARGET_HOOKS``       | After target install                       | Create symlinks, install init scripts
``<pkg>_POST_INSTALL_HOOKS``              | After both staging & target install        | General cleanup

**How to define a hook** (in your ``.mk`` file):

.. code-block:: makefile

define MYFOO_POST_PATCH_FIXUP
    $(SED) 's/foo/bar/g' $(@D)/src/main.c
    touch $(@D)/stamp-extra-generated
endef
MYFOO_POST_PATCH_HOOKS += MYFOO_POST_PATCH_FIXUP

💻 4. Quick Debugging Workflow Examples

.. code-block:: bash

================================================================================
1. See what went wrong during patching
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



make myfoo-patch                # stops after patch step
vi output/build/myfoo-1.2.3/.stamp_patched   # check if stamp exists

================================================================================
⚡ 2. Edit source → fast rebuild
================================================================================

vi output/build/myfoo-*/src/*.c
make myfoo-rebuild

================================================================================
3. Force full re-patch (useful after changing patches)
================================================================================

make myfoo-dirclean && make myfoo-patch

================================================================================
🟢 ✅ 🟢 🟢 ✅ 4. Test only install step
================================================================================

make myfoo-reinstall

================================================================================
5. Check applied patches
================================================================================

ls output/build/myfoo-*/.applied_patches_list   # or look in build dir

📚 5. Quick Reference Table – Most Frequent Commands

Priority | Command                        | Phase / Purpose
---------|--------------------------------|--------------------------------------
1        | ``make <pkg>``                   | Full fetch → install
2        | ``make <pkg>-dirclean``          | Reset everything for this pkg
3        | ``make <pkg>-patch``             | Debug patch application
4        | ``make <pkg>-configure``         | Debug ./configure / cmake errors
5        | ``make <pkg>-build``             | Fast build iteration
6        | ``make <pkg>-post-patch-hook``   | (custom) test your POST_PATCH hook
7        | ``make <pkg>-reinstall``         | Fix install bugs quickly

Most daily package debugging is:  
``make <pkg>-dirclean && make <pkg>-patch && make <pkg>-configure && make <pkg>-build``

🟢 🟢 Good luck debugging your packages!  
See also: Buildroot manual → “Hooks available in the various build steps” and ``package/pkg-generic.mk`` for the exact stamp / hook logic.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
