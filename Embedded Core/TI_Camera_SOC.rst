================================================================================
� **TI Camera SoC Cheatsheet** — Jacinto 7 & AM6xA (ADAS / Vision)!
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

This cheatsheet gives a compact, emoji-rich overview to help you pick, remember, and prototype with TI SoCs for camera and ADAS designs.

📚 **Legend & Quick Icons** (Quick Reference!)
===============================================

🔹 **SoC families:** Jacinto™ 7 (TDA4x-Q1 family), Sitara™ AM6xA
🔋 **Power hints:** ⚡ low / ⚡⚡ mid / ⚡⚡⚡ high
🟢 **Status:** 🟢 Production | 🟡 Sampling/Eval | 🔴 EOL/Legacy
⭐ **Memory aid:** Star the ones you use often to remember their strengths


1️⃣ **Top TI SoCs at a Glance** (Quick Comparison!)
===================================================

.. list-table:: Key TI SoCs for Camera/ADAS (2026)
   :header-rows: 1

   * - SoC (short)
     - TOPS
     - CPU
     - Cameras
     - Typical use
     - Accelerators / Notes
     - Power
     - Status
   * - **AM62A3/7-Q1**
     - 1–2 TOPS
     - 1–4× A53
     - 1–2 cams
     - DMS, dashcam, entry ADAS
     - RGB-IR ISP, basic DSP
     - ⚡ (very low)
     - 🟢 Production
   * - **AM67A**
     - ~4 TOPS
     - Quad A53
     - up to 4 cams
     - Machine vision, entry surround
     - Vision pre-proc, MMA
     - ⚡
     - 🟢 Production
   * - **TDA4AL / TDA4VL-Q1**
     - 4 TOPS
     - Dual A72
     - 4–8 cams
     - Front camera, analytics
     - C7x DSP, MMA, DMPAC
     - ⚡⚡
     - 🟢 Production (auto)
   * - **TDA4VM / TDA4VE-Q1**
     - 8 TOPS
     - Dual A72
     - 8+ cams
     - Mid ADAS, surround, fusion
     - C7x + GPU + MMA + DMPAC
     - ⚡⚡
     - 🟢 Widely used
   * - **TDA4VH**
     - 8–16 TOPS
     - Dual/Quad A72
     - 8–12+ cams
     - High-end ADAS, sensor fusion
     - Enhanced vision accelerators
     - ⚡⚡⚡
     - 🟢 Production
   * - **AM68A / AM69A**
     - 8 / 32 TOPS
     - Dual A72 / Octa A72
     - 1–12 cams
     - Industrial/AI-box, high-res analytics
     - Multiple MMAv2, video engines
     - ⚡⚡–⚡⚡⚡
     - 🟢 Production
   * - **TDA5 family**
     - 10 → 1200 TOPS
     - Scalable/chiplet
     - Many cams (central compute)
     - Next-gen domain compute / L3
     - Proprietary NPU (very efficient)
     - ⚡⚡⚡ (very efficient)
     - 🟡 Sampling (end-2026)


================================================================================
2️⃣ Quick Selection Guide — Pick fast (mnemonic: E-M-H-C)
================================================================================

- Entry (E): DMS / single-front / dashcam → **AM62A7 / AM62A3** 🟢⚡ (low power, low cost)
- Mid (M): 4–8 cams / surround → **TDA4VM / TDA4VL** 🟢⚡⚡ (workhorse, best ecosystem)
- High (H): 8+ cams / L2+ → **TDA4VH / AM69A** 🟢⚡⚡⚡ (higher bandwidth)
- Central (C): Domain / L3 central compute → **TDA5** family 🟡⚡⚡⚡ (wait for sampling)

Memory tip: Remember "E-M-H-C" → Entry, Mid, High, Central maps to AM62 → TDA4VM → TDA4VH/AM69 → TDA5


================================================================================
3️⃣ Key Hardware Features (visual cheat)
================================================================================

- MMA (Matrix Multiply Accelerator): 🔢 Deep learning inner loop (8 TOPS per MMA instance)
- C7x DSP: 🔧 Vision DSP for pre/post processing and sensor fusion
- DMPAC / VISS: 🎯 Depth, motion, ISP pipelines
- Safety island (R5F): 🛡️ ASIL capable control & safety monitor
- High-speed IO: 📷 CSI-2 RX lanes, FPD-Link, Ethernet TSN, PCIe


================================================================================
4️⃣ Recommended Devkits & Quick Start Tips
================================================================================

- Evaluation kit: **SK-TDA4VM** — best supported, many demos (surround, front, AI)
- Entry eval: **AM62x EVM** — good for DMS and low-cost cameras
- Tools: **Processor SDK Linux**, **TIDL**, **Edge AI Studio**, **Vision Apps** demos

Quick SDK tips:

.. code-block:: bash

   # Download & untar TI Processor SDK (example - replace URL)
   wget <processor-sdk-url>
   tar xzf processor-sdk.tar.gz

   # Build a minimal Yocto image (high level)
   source ./environment-setup
   bitbake core-image-minimal

Pro tip: Use TI's prebuilt SD card images to validate camera pipelines quickly.


================================================================================
5️⃣ Design Considerations & Power Budgeting
================================================================================

- Bandwidth: Camera count × resolution × fps → key for memory and CSI lanes
- Thermal: TDA4VM class often needs passive heatsink; TDA4VH/AM69A often need active cooling for sustained full-load
- Power estimate (very rough):

.. code-block:: text

   - AM62x: ~2–6 W (idle→load)
   - TDA4VM: ~5–15 W (typical), spikes up to ~20 W for heavy AI
   - TDA4VH / AM69A: 10–25 W depending on mode


================================================================================
6️⃣ Common Camera/SoC Pairings & Why (mnemonic icons)
================================================================================

- Front & DMS → AM62A7-Q1 (cheap + RGB-IR ISP) 📸🟢
- 4× cameras surround → TDA4VM-Q1 (best SW + DSP) 🔁⭐
- 8+ cameras / sensor fusion → TDA4VH / AM69A (bandwidth & MMA) 🔗⚡⚡
- Central compute (fusion of ADAS + IVI) → TDA5 (future-proof) 🚀🟡


================================================================================
7️⃣ Quick Debug & Bring-up Checklist
================================================================================

- Hardware:
  - Check CSI lanes mapping and clocking
  - Validate lens/ISIF formats and lane polarity
  - Confirm power sequencing (rail ramps)

- Software:
  - Boot SD card image on EVM
  - Run camera pipeline demo (Vision Apps)
  - Run `media-ctl` to check v4l2 pipeline

Commands to sanity-check camera pipeline:

.. code-block:: bash

   # List video devices
   v4l2-ctl --list-devices

   # Show formats on a media pad
   media-ctl -p -d /dev/media0

   # Run a simple gst-launch preview (example)
   gst-launch-1.0 v4l2src device=/dev/video0 ! autovideosink


================================================================================
8️⃣ Quick Mnemonics & Memory Aids (colorful!)
================================================================================

- Emoji map:
  - 🛰️ SoC family = Jacinto/AM6xA
  - 🔢 MMA = deep learning accelerator
  - 🔧 C7x = vision DSP
  - 🛡️ safety island = R5F
  - 📷 camera = CSI lanes

- Remember: "MMA + C7x + ISP = Vision Pipeline" → 🔢 + 🔧 + 🎯
- Short checklist: "C-BATS" → Cameras, Bandwidth, Alignment, Thermal, Safety


================================================================================
9️⃣ Useful Links & Next Steps (local notes)
================================================================================

- Start: SK-TDA4VM kit + Processor SDK Linux image
- Prototype: Try 1 camera → 4 cameras → scale to 8 to validate CSI and thermal
- Production: Check automotive variants (Q1) for ASIL/temperature and longevity


================================================================================
🔚 Bottom Line — One-line cheat
================================================================================

TDA4VM = workhorse for most camera ADAS in 2023–2026; AM62x = cheap DMS; TDA4VH/AM69A = scale up; TDA5 = central compute future. Remember E‑M‑H‑C.

🚗📸 Good luck — ping me if you want a compact one-page printable flashcard!

✨ **TI Camera SoC TL;DR** (30-Second Guide!)
==============================================

✅ **Entry ADAS**: AM62A3/7 (1-2 TOPS, $30–50 budget)
✅ **Mid-Range**: TDA4AL/VL (4 TOPS, good ISP, $80–120)
✅ **High-End**: TDA4VM/VE (8 TOPS, dual C7x DSP, full ADAS)
✅ **Production**: Jacinto 7 line → automotive-qualified (ASIL-B/D)
✅ **Surround View**: TDA4VE + 4–8 cameras + ISP + VISS
✅ **ISP Pipeline**: Bayer demosaicing, tone mapping, distortion correction
✅ **MIPI CSI-2**: Up to 8 lanes per sensor (dual sensor support)
✅ **Software**: TDA4x includes ISP firmware + RTOS support
✅ **Power**: 5–20W typical for full sensor pipeline
✅ **FPGA Options**: Select models include optional FPGA co-processors

---

🏆 **Why Choose TI?**
===================

✅ Integrated ISP (image signal processor) on-die
✅ Strong DSP + MMA for edge AI inference
✅ Production automotive qualification (ASIL)
✅ Rich camera ecosystem (OmniVision, Sony, Samsung)
✅ Good documentation and developer support
✅ Thermal and reliability track record in automotive

---

**Last updated:** 2026-01-12 | **TI Embedded Vision Architecture**

