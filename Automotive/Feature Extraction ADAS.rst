
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


Here is a practical, ADAS-focused **cheatsheet for JPEG, MPEG video codecs + common feature extraction methods**  
(oriented toward embedded automotive perception engineers — 2025/2026 reality)

```text
╔════════════════════════════════════════════════════════════════════════════╗
║         JPEG / MPEG / Feature Extraction Cheatsheet ─ ADAS Edition         ║
╚════════════════════════════════════════════════════════════════════════════╝

                            ADAS Camera Pipeline Context
                 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
Raw Bayer ───►  Debayer/DPC  ───►  JPEG/MJPEG   ───►  Feature Extraction  ───► Detection/Tracking
                 (ISP)               (compression)          (classical / DL)
                                           └───────────────┘
                                 or H.264/H.265 (MPEG) for recording/streaming

════════════════════════════════════════════════════════════════════════════════
⭐ 1. JPEG (Still Image Compression) – Most Important in ADAS Cameras 2025–2026
════════════════════════════════════════════════════════════════════════════════

⭐ Key JPEG modes used in ADAS cameras:

Mode                  Chroma subsampling   Quality range   Typical bitrate   Use-case in ADAS
────────────────────  ───────────────────  ──────────────  ─────────────────  ────────────────────────────────
JPEG Baseline         4:2:0                70–92%          120–400 kB/frame   Main front/surround view stills
JPEG 4:2:2            4:2:2                75–90%          180–600 kB/frame   Better chroma → traffic signs, colors
MJPEG (Motion JPEG)   4:2:0 or 4:2:2       75–90%          5–25 Mbps         Live view debug / low-latency stream
JPEG-XL (emerging)    adaptive             60–85%          40–60% smaller    Future replacement (2026+ adoption slow)

⭐ Important quality sweet-spots in ADAS (empirical 2024–2026):

Target                     Recommended Q   Approx. size (2MP)   Remarks
─────────────────────────  ──────────────  ───────────────────  ────────────────────────────────────────
Front camera (object det)      82–88           180–280 kB         Balance between size & text readability
Surround view (fisheye)        78–84           220–350 kB         Strong compression artifacts hurt stitching
Traffic sign / LPR             88–92           300–450 kB         Higher quality → better OCR/character recognition
Night/low-light                85–90           250–400 kB         Noise makes compression artifacts more visible

════════════════════════════════════════════════════════════════════════════════
2. MPEG Video Codecs in ADAS (Recording / Streaming / V2X)
════════════════════════════════════════════════════════════════════════════════

Codec            Typical Resolution   Bitrate range (ADAS)   GOP size   Latency   Main ADAS Use-case                     Status 2026
───────────────  ───────────────────  ─────────────────────  ─────────  ────────  ────────────────────────────────────────  ───────────────
H.264/AVC        1080p / 2K           4–12 Mbps              30–120     50–150ms  Almost every DVR / CMS / telematics       Dominant
H.265/HEVC       1080p / 4K           2–8 Mbps               60–150     80–200ms  High-end DVR, better quality@low bitrate  Very common
AV1              4K                   1.5–6 Mbps             60–240     100–300ms Emerging for cloud upload / V2X           Slow adoption
H.266/VVC        4K/8K                1–4 Mbps               90–300     high      Future (2027+) – almost no automotive yet Very early

ADAS sweet-spots 2025–2026:

⭐ Use-case                        Codec     Resolution   Bitrate     GOP   Keyframe interval   Remarks
──────────────────────────────  ────────  ───────────  ──────────  ─────  ──────────────────  ────────────────────────────────────────
⭐ Cabin DMS / driver monitoring   H.264     720p–1080p   2–5 Mbps    30–60  1–2 sec             Latency critical
Surround / AVM recording        H.265     1080p        6–10 Mbps   60–90  2–4 sec             Storage is expensive → HEVC wins
Event / accident clip (upload)  H.264     1080p        8–15 Mbps   15–30  0.5–1 sec           Fast seek + 🟢 🟢 good quality
V2X camera sharing (live)      H.264     720p         1.5–4 Mbps  15–30  <100ms              Ultra low latency priority

════════════════════════════════════════════════════════════════════════════════
3. Classical Feature Extraction Methods Still Alive in ADAS (2025–2026)
════════════════════════════════════════════════════════════════════════════════

Method              Speed (embedded)   Robustness   Main ADAS Use-case                          Still Used?   Typical Lib
──────────────────  ────────────────   ───────────  ──────────────────────────────────────────  ─────────────  ───────────────
Harris / Shi-Tomasi Very fast          Medium       Corner detection for visual odometry         Yes            OpenCV
FAST / AGAST        Extremely fast     Medium       Feature points for SLAM / mono VO            Yes            OpenCV / libviso2
ORB                 Fast               🟢 🟢 Good         Rotation + scale robust, binary descriptor   Yes (very much) OpenCV
BRISK               Fast               🟢 🟢 Good         Alternative to ORB, scale+rotation           Yes            OpenCV
SIFT (patent-free)  Slow               Excellent    Reference / ground truth, few fps cases      Rarely         OpenCV contrib
SURF                Medium             Very 🟢 🟢 good    When ORB fails (older codebases)             Rarely         OpenCV contrib
AKAZE               Medium             Very 🟢 🟢 good    Nonlinear scale-space, 🟢 🟢 good in low-texture   Sometimes      OpenCV
SuperPoint          Medium–Fast (GPU)  Excellent    Learned detector + descriptor                Increasing     PyTorch / ONNX
⭐ R2D2 / Key.Net      Fast (GPU)         Excellent    Modern learned keypoints + descriptors       Rising         Research → prod slowly

════════════════════════════════════════════════════════════════════════════════
4. Quick Decision Tree – What to Use in 2026 ADAS Project?
════════════════════════════════════════════════════════════════════════════════

⭐ Need keypoints / features?

├── Classical method required (certification, deterministic, no GPU)?
│   ├── Need fastest possible detector?          → FAST / AGAST
│   ├── Need binary + rotation+scale robust?     → ORB (default choice 2024–2026)
│   └── Need 🟢 🟢 best classical quality?             → AKAZE or BRISK
│
└── Can use learned methods (most new projects)?
    ├── Have GPU / NPU / 🟢 🟢 good DSP?               → SuperPoint + SuperGlue / LightGlue
    └── CPU only, strict real-time?              → ORB or FAST + handcrafted matcher
        └─→ still very hard to beat ORB in ~10–15 ms budget on Cortex-A7x

════════════════════════════════════════════════════════════════════════════════
5. One-liners / Snippets you copy-paste all the time (OpenCV 4.10+)
════════════════════════════════════════════════════════════════════════════════

# ORB – the evergreen
orb = cv2.ORB_create(nfeatures=1500, scaleFactor=1.2, nlevels=8)
kp, des = orb.detectAndCompute(gray, None)

# FAST + ORB descriptor
fast = cv2.FastFeatureDetector_create(threshold=20)
orb = cv2.ORB_create()
kp_fast = fast.detect(gray, None)
kp, des = orb.compute(gray, kp_fast)

# SuperPoint inference (ONNX style – very common pattern)
import onnxruntime as ort
sess = ort.InferenceSession("superpoint.onnx")
outs = sess.run(None, {"input": img_tensor_np})
points, descriptors = outs[0], outs[1]

# Simple quality check after compression
def jpeg_quality_score(img_orig, img_comp):
    return 100 - cv2.PSNR(img_orig, img_comp)   # rough rule-of-thumb

Happy ADAS perception coding! 📸🚗
```

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
