=====================================
ARM ISP (Image Signal Processor) Cheatsheet (2026)
=====================================

**2026 Guide**: Comprehensive coverage of ARM Image Signal Processing architectures, ISP pipelines, color processing, and optimization techniques for embedded vision on ARM platforms.

.. contents:: Table of Contents
   :depth: 3

---

⭐ **Keywords Overview**: ISP pipeline, Bayer demosaicing, white balance, color correction, gamma correction, noise reduction (NR), edge enhancement, lens distortion correction, tone mapping, auto-exposure (AE), auto-focus (AF), auto-white-balance (AWB), RAW processing, HDR, video stabilization.

---

📖 ARM ISP Architecture Overview
=============================

ISP Processing Stages (Typical Pipeline)
----------------------------------------

The ARM ISP follows a sequential processing pipeline from RAW sensor data to output RGB frames:

1. **RAW Input Stage**: Bayer pattern sensor data (CFA demosaicing)
2. **Black Level Correction**: Subtract dark frame offset
3. **Lens Shading Correction**: Correct vignetting and uneven illumination
4. **White Balance**: Scale color channels (gains for R, G, B)
5. **Demosaicing**: Interpolate missing color channels (CFA → RGB)
6. **Color Correction**: Transform to standard color space (sRGB, Adobe RGB)
7. **Gamma Correction**: Apply tone curve for perceptual uniformity
8. **Noise Reduction**: Spatial/temporal filtering
9. **Edge Enhancement**: Sharpening filters
10. **Tone Mapping**: Map HDR → LDR (if applicable)
11. **Video Output**: YUV 4:2:0 or RGB output

⭐ **Keywords**: Color Filter Array (CFA), RAW processing, linear RGB, sRGB gamma, color space conversion, ISP datapath.

---

📚 Core ISP Components & Functions
===============================

📡 Sensor Interface
----------------

**Supported Formats**:

+------------------+------------------+----------------------+---------------------------+
| Format           | Bits per Pixel   | Compression          | Applications              |
+==================+==================+======================+===========================+
| RAW Bayer RGGB   | 8/10/12/14 bits  | None                 | Standard cameras          |
+------------------+------------------+----------------------+---------------------------+
| RAW Bayer GRBG   | 8/10/12/14 bits  | None                 | Alternate arrangement     |
+------------------+------------------+----------------------+---------------------------+
| RAW Bayer GBRG   | 8/10/12/14 bits  | None                 | Alternate arrangement     |
+------------------+------------------+----------------------+---------------------------+
| RAW Bayer BGGR   | 8/10/12/14 bits  | None                 | Alternate arrangement     |
+------------------+------------------+----------------------+---------------------------+
| Mono (Y)         | 8/10/12/14 bits  | None                 | Grayscale sensors         |
+------------------+------------------+----------------------+---------------------------+
| MIPI CSI-2       | Variable         | DPCM/Lossless        | High-speed serial link    |
+------------------+------------------+----------------------+---------------------------+

⭐ **Keywords**: Bayer pattern, CFA (Color Filter Array), pixel format, data rate (Mbps), MIPI CSI-2, I3C interface.

⚙️ Black Level Correction (BLC)
-----------------------------

Removes dark offset from sensor output:

.. code-block:: c

    // Black level correction: output = (input - blackLevel) << shift
    uint16_t blc_value = 64;  // Typical dark frame offset
    uint8_t output = (input - blc_value) >> shift;  // Prevent underflow with saturation

**Purpose**: Correct fixed pattern noise, improve dynamic range
⭐ **Keywords**: Dark frame subtraction, pedestal removal, offset correction, linearization.

⚙️ Lens Shading Correction (LSC)
-----------------------------

Corrects uneven illumination (vignetting) across the image:

.. code-block:: c

    // Lens shading: output = input × lensShadingGain[x][y]
    // Gain map typically 8×8 or 16×16 grid with bilinear interpolation
    uint16_t lsc_gain = 256;  // Unity gain = 256 (0.5 to 2.0 typical range)
    uint16_t corrected = (input * lsc_gain) >> 8;

**Correction Method**: Pre-computed gain map (lookup table or polynomial)
**Storage**: ~1-4 KB for typical gain map
⭐ **Keywords**: Vignetting correction, illumination correction, gain map, spatial interpolation, LSC calibration.

White Balance (WB)
------------------

Adjusts color channel gains to achieve neutral colors under different lighting:

.. code-block:: c

    // White balance: scale R, G, B channels independently
    uint8_t r_gain = 256;  // Q8 format (1.0 = 256, range ~0.5-2.0)
    uint8_t g_gain = 256;
    uint8_t b_gain = 256;
    
    uint16_t r_out = (r_in * r_gain) >> 8;
    uint16_t b_out = (b_in * b_gain) >> 8;

**Common Modes**:
- **Auto White Balance (AWB)**: Algorithm detects light source and adjusts gains
  - Gray-world assumption: average of R, G, B channels should be equal
  - Histogram analysis to detect color temperature
  - Machine learning models for scene analysis

- **Manual Presets**: Daylight, cloudy, tungsten, fluorescent, custom

⭐ **Keywords**: Color temperature (Kelvin), white point, AWB algorithm, color constancy, Planckian locus, AWB convergence.

⚙️ Demosaicing (CFA Interpolation)
--------------------------------

Interpolates missing color channels from Bayer pattern to produce full RGB:

**Algorithm Comparison**:

+------------------------+--------+-------+----------+------------------------+
| Algorithm              | Quality| Speed | Artifacts| Complexity             |
+========================+========+=======+==========+========================+
| Nearest Neighbor       | Poor   | Fast  | Blocky   | 1 sample               |
+------------------------+--------+-------+----------+------------------------+
| Bilinear              | Fair   | Fast  | Blurred  | 4 samples              |
+------------------------+--------+-------+----------+------------------------+
| Edge-Directed (EDAC)  | 🟢 🟢 Good   | Medium| Low      | Edge detection + 4-8   |
+------------------------+--------+-------+----------+------------------------+
| High-Quality (HQ)     | Excellent| Slow | Minimal  | 12+ samples            |
+------------------------+--------+-------+----------+------------------------+

**Edge-Directed Algorithm (EDAC)** — Industry standard:

.. code-block:: c

    // Simplified EDAC: detect edge direction, interpolate along edge
    int vert_gradient = abs(top - bottom);
    int horiz_gradient = abs(left - right);
    
    if (vert_gradient < horiz_gradient) {
        // Vertical edge: interpolate vertically
        output = (top + bottom) >> 1;
    } else {
        // Horizontal edge: interpolate horizontally
        output = (left + right) >> 1;
    }

⭐ **Keywords**: Bayer interpolation, CFA demosaicing, edge-aware interpolation, color plane alignment, alias artifacts.

⚙️ Color Correction Matrix (CCM)
-----------------------------

Transforms from sensor color space to standard output color space (sRGB, Adobe RGB):

.. code-block:: c

    // 3×3 color correction matrix (fixed-point Q7)
    int16_t ccm[3][3] = {
        {128,  -10,  -20},  // R row
        { -15, 140,   -5},  // G row
        {  -5,  -20, 150}   // B row
    };
    
    // Apply CCM: output_color = CCM × input_color (Q14 accumulator)
    int32_t r_out = (ccm[0][0]*r + ccm[0][1]*g + ccm[0][2]*b) >> 7;
    int32_t g_out = (ccm[1][0]*r + ccm[1][1]*g + ccm[1][2]*b) >> 7;
    int32_t b_out = (ccm[2][0]*r + ccm[2][1]*g + ccm[2][2]*b) >> 7;

**Calibration**: Requires color reference chart (Macbeth ColorChecker or similar)
**Adaptive CCM**: Different matrices for different color temperatures
⭐ **Keywords**: Color space transformation, chrominance correction, color gamut, gamut mapping.

⚙️ Gamma Correction & Tone Mapping
--------------------------------

Applies perceptual tone curve for display-friendly output:

**Gamma Function**:

.. code-block:: c

    // Standard sRGB gamma: output = input^(1/2.2)
    // Implemented via lookup table (LUT) for efficiency
    uint16_t gamma_lut[256];  // 8-bit input → 16-bit output
    uint16_t output = gamma_lut[input];

**Common Curves**:
- **sRGB (2.2 gamma)**: Perceptual uniformity, web standard
- **Linear (1.0 gamma)**: No correction, for post-processing
- **Rec.709**: Video standard
- **Custom curves**: Scene-dependent tone mapping

**HDR Tone Mapping**:
- Compress high dynamic range to displayable range
- Preserve local contrast (shadow/highlight balance)
- Algorithms: Reinhard, gradient domain, bilateral filtering

⭐ **Keywords**: Gamma 2.2, sRGB gamma curve, tone mapping curve, EOTF (electro-optical transfer function), inverse OECF.

⚙️ Noise Reduction (NR)
--------------------

Reduces sensor noise (shot noise, read noise) while preserving detail:

**Spatial Filters**:

+----------------+----------+--------+------------+---------------------+
| Filter Type    | Strength | Speed  | Artifacts  | Use Case            |
+================+==========+========+============+=====================+
| Bilateral      | High     | Medium | Low        | Real-time, balanced |
+----------------+----------+--------+------------+---------------------+
| Non-Local (NLM)| Very High| Slow   | Very Low   | Post-processing     |
+----------------+----------+--------+------------+---------------------+
| Morphological  | Medium   | Fast   | Blocky     | Edge-preserving     |
+----------------+----------+--------+------------+---------------------+
| Gaussian       | Low      | Very   | Blurred    | Preprocessing       |
+----------------+----------+--------+------------+---------------------+

**Bilateral Filter** (common in ISP):

.. code-block:: c

    // Bilateral: weighted average based on spatial & intensity proximity
    output = 0;
    weight_sum = 0;
    for (dy = -r; dy <= r; dy++) {
        for (dx = -r; dx <= r; dx++) {
            spatial_dist = sqrt(dx*dx + dy*dy);
            intensity_dist = abs(pixel[y+dy][x+dx] - pixel[y][x]);
            
            weight = exp(-(spatial_dist*spatial_dist)/(2*sigma_s*sigma_s)) *
                    exp(-(intensity_dist*intensity_dist)/(2*sigma_r*sigma_r));
            
            output += weight * pixel[y+dy][x+dx];
            weight_sum += weight;
        }
    }
    output /= weight_sum;

**Temporal Filtering** (video streams):
- Frame averaging: Reduce flicker without ghosting
- Optical flow: Motion-compensated filtering for moving objects

⭐ **Keywords**: Gaussian blur, bilateral filtering, non-local means (NLM), denoise, denoiser strength, temporal coherence.

Edge Enhancement (Sharpening)
------------------------------

Enhances edge contrast for perceived sharpness:

**Unsharp Mask** (most common):

.. code-block:: c

    // Unsharp mask: output = input + strength × (input - blurred)
    uint8_t blurred = gaussian_blur(input);
    uint8_t edge = input - blurred;
    uint8_t sharpened = input + (strength * edge);  // with saturation

**Edge Detection Methods**:
- Sobel kernel: 3×3 gradient operator
- Laplacian: Second-order edge detection
- High-pass filter: Frequency domain sharpening

**Parameters**:
- **Strength**: 0-2.0 (0 = no sharpening, 1.0 = standard, 2.0+ = aggressive)
- **Radius**: Kernel size (1-3 pixels typical)
- **Threshold**: Minimum edge amplitude to sharpen

⭐ **Keywords**: Unsharp mask, Sobel filter, Laplacian, high-pass filter, edge detection kernel, sharpening artifact.

⚙️ Lens Distortion Correction
---------------------------

Corrects barrel/pincushion distortion from camera lens:

**Radial Distortion Model**:

.. code-block:: c

    // Radial distortion: r_distorted = r_undistorted × (1 + k1×r² + k2×r⁴)
    // Correction: iterate to find undistorted radius
    float r = sqrt(x*x + y*y);
    float r_dist = r * (1.0f + k1*r*r + k2*r*r*r*r);
    float scale = r_dist / r;
    
    float x_undist = x * scale;
    float y_undist = y * scale;

**Implementation**:
- Pre-computed look-up table (LUT) for real-time performance
- Bilinear interpolation for sub-pixel accuracy

**Calibration Parameters**:
- Focal length (f)
- Principal point (cx, cy)
- Distortion coefficients (k1, k2, k3, ...)

⭐ **Keywords**: Barrel distortion, pincushion distortion, radial distortion, tangential distortion, distortion coefficients, calibration.

---

Auto-Exposure (AE) & Auto-Focus (AF)
=====================================

🧮 Auto-Exposure (AE) Algorithm
-----------------------------

Automatically adjusts sensor gain and integration time for proper brightness:

**Metering Modes**:

+---------------+-------------------+------------------+-------------------+
| Mode          | Weight Distribution| 🟢 🟢 Best For         | Sensitivity       |
+===============+===================+==================+===================+
| Average       | Uniform           | Generic scenes   | Low               |
+---------------+-------------------+------------------+-------------------+
| Center-Weight | Center emphasis   | Portrait, center | Medium            |
+---------------+-------------------+------------------+-------------------+
| Spot          | Small region      | Backlit subjects | High (precise)    |
+---------------+-------------------+------------------+-------------------+
| Matrix        | Complex zones     | Intelligent      | Medium-High       |
+---------------+-------------------+------------------+-------------------+

**AE Algorithm Flow**:

.. code-block:: c

    // Simplified AE feedback loop
    uint32_t histogram[256];
💾     compute_histogram(frame, histogram);
    
    uint32_t mean_brightness = compute_weighted_mean(histogram, weights);
    uint32_t target_brightness = 128;  // 50% target
    
    // PID controller
    int32_t error = target_brightness - mean_brightness;
    exposure_time += kp * error + ki * integral_error;  // Adjust exposure
    sensor_gain += derivative_term;                      // Adjust gain

**Parameters**:
- **Target Brightness**: Typical 40-50% of range
- **Convergence Speed**: 30-100 ms for stable lock
- **Flicker 🔴 🔴 Avoidance**: Align exposure to power line frequency (50/60 Hz)

⭐ **Keywords**: Metering, exposure compensation, AE lock, flicker reduction, anti-flicker filter, histogram-based AE.

🧮 Auto-Focus (AF) Algorithm
--------------------------

Automatically adjusts lens focus for sharp images:

**AF Methods**:

1. **Contrast Autofocus (CAF)** — Software-based:
   - Measure edge sharpness across focus range
   - Find peak contrast position
   - Advantage: No dedicated hardware
   - Disadvantage: Slower, requires lens movement

.. code-block:: c

    // Contrast metric: Laplacian variance
    int32_t contrast = 0;
    for (int y = 1; y < height-1; y++) {
        for (int x = 1; x < width-1; x++) {
            int laplacian = -4*frame[y][x] + frame[y-1][x] + frame[y+1][x] 
                          + frame[y][x-1] + frame[y][x+1];
            contrast += abs(laplacian);
        }
    }

2. **Phase Detection Autofocus (PDAF)** — Hardware-based:
   - Uses dedicated AF sensors (phase detection pixels)
   - Fast, accurate focus
   - Requires PDAF pixel layout in sensor

3. **Laser Autofocus** — Time-of-flight:
   - Measures distance to subject
   - Very fast, works in low light

**Focus Score Metrics**:
- **Sharpness**: Laplacian variance, Tenengrad, NGLRT
- **Contrast**: Edge contrast measure
- **Frequency**: High-frequency content

⭐ **Keywords**: Phase-detection AF, contrast AF, focus scoring, depth map, PDAF pixel, laser AF, time-of-flight.

---

Color Processing Deep Dive
===========================

⚙️ Color Spaces & Conversions
---------------------------

**Common Color Spaces**:

+----------+-------------+-------+------------------+--------------------------+
| Space    | Components  | Bits  | Gamma            | Application              |
+==========+=============+=======+==================+==========================+
| RGB      | R, G, B     | 8/10  | sRGB (2.2)       | Display output           |
+----------+-------------+-------+------------------+--------------------------+
| YUV      | Y, U, V     | 8     | Implicit (709)   | Video compression        |
+----------+-------------+-------+------------------+--------------------------+
| YCbCr    | Y, Cb, Cr   | 8     | ITU-R BT.709     | JPEG, MPEG               |
+----------+-------------+-------+------------------+--------------------------+
| LAB      | L, a, b     | 16/24 | Perceptual       | Color correction         |
+----------+-------------+-------+------------------+--------------------------+
| HSV      | H, S, V     | 8     | N/A              | Color adjustment         |
+----------+-------------+-------+------------------+--------------------------+

**RGB → YUV Conversion** (BT.709):

.. code-block:: c

    // Linear RGB → YUV (ITU-R BT.709)
    Y  =  0.2126*R + 0.7152*G + 0.0722*B
    Cb = -0.1145*R - 0.3855*G + 0.5*B       // +128 offset for storage
💾     Cr =  0.5*R - 0.4542*G - 0.0458*B      // +128 offset for storage
    
    // Fixed-point Q7 implementation:
    Y  = (27*R + 92*G +  9*B) >> 7;
    Cb = (128 - 15*R - 49*G + 64*B) >> 7;
    Cr = (128 + 64*R - 58*G -  6*B) >> 7;

⭐ **Keywords**: Color space conversion, RGB to YUV, chroma subsampling (4:2:0, 4:2:2), color matrix.

Chroma Subsampling
-------------------

Reduces color information while preserving luminance (exploits human vision):

+----------+--+--+---+----------+----------+
| Format   | Y| Cb| Cr| H Reduce | V Reduce |
+==========+==+==+===+==========+==========+
| 4:4:4    | 1| 1| 1 | None     | None     |
+----------+--+--+---+----------+----------+
| 4:2:2    | 1|1/2|1/2| 2×       | None     |
+----------+--+--+---+----------+----------+
| 4:2:0    | 1|1/4|1/4| 2×       | 2×       |
+----------+--+--+---+----------+----------+

**Impact**:
- **4:4:4**: Full color quality, 1× bandwidth
- **4:2:2**: 🟢 🟢 Good for video, 0.5× bandwidth (JPEG, broadcast)
- **4:2:0**: Optimal compression, 0.5× bandwidth (YouTube, HEVC)

⭐ **Keywords**: Chroma subsampling, color downsampling, YUV 4:2:0, color bandwidth.

---

🎯 Advanced ISP Features
=====================

HDR Processing
---------------

Merges multiple exposures to create high dynamic range output:

**Algorithm**:

1. **Capture**: Short, normal, and long exposures
2. **Alignment**: Register frames using optical flow
3. **Fusion**: Combine exposures (weighted merge)
4. **Tone Mapping**: Compress to 8-bit output

.. code-block:: c

    // Simple HDR fusion: weighted average of exposures
    // Weight based on proximity to optimal exposure
    float weight_short  = exp(-(brightness_short - target)² / (2*sigma²));
    float weight_normal = exp(-(brightness_normal - target)² / (2*sigma²));
    float weight_long   = exp(-(brightness_long - target)² / (2*sigma²));
    
    output = (weight_short*short_exp + weight_normal*normal_exp + weight_long*long_exp) 
             / (weight_short + weight_normal + weight_long);

⭐ **Keywords**: Multi-exposure fusion, tone mapping, local contrast enhancement, ghost removal.

⚙️ Video Stabilization
--------------------

Reduces camera shake through optical or digital stabilization:

**Digital Video Stabilization (DVS)**:

.. code-block:: c

    // Frame-to-frame motion estimation (optical flow)
💾     motion_vector = estimate_optical_flow(previous_frame, current_frame);
    
    // Smooth motion over time (Kalman filter)
⚙️     smooth_motion = kalman_filter(motion_vector);
    
    // Compensate: shift current frame
    stabilized = warp(current_frame, smooth_motion);

**Metrics**:
- **Jitter**: High-frequency shake (reduce with temporal smoothing)
- **Drift**: Long-term motion bias (compensate with Kalman filtering)

⭐ **Keywords**: Optical flow, motion estimation, Kalman filter, digital stabilization, OIS (Optical Image Stabilization).

⚙️ Face Detection & Recognition
-----------------------------

Detects faces for AF/AE optimization and image enhancement:

**Integration with AE/AF**:
- Detect face regions
- Apply higher metering weight to face center
- Focus on eyes for portrait mode

⭐ **Keywords**: Face detection, eye detection, face recognition, histogram equalization for faces.

---

⚡ Performance & Optimization
===========================

⚡ ISP Pipeline Performance Benchmarks
-----------------------------------

+------------------------+-----------+-----------+----------+
| Operation              | Cortex-A53| Cortex-A72| M55/M85  |
+========================+===========+===========+==========+
| Demosaicing (1080p)    | ~25 ms    | ~8 ms     | ~15 ms   |
+------------------------+-----------+-----------+----------+
| Color correction       | ~5 ms     | ~1 ms     | ~2 ms    |
+------------------------+-----------+-----------+----------+
| Noise reduction        | ~40 ms    | ~12 ms    | ~20 ms   |
+------------------------+-----------+-----------+----------+
| Full ISP pipeline      | ~150 ms   | ~40 ms    | ~70 ms   |
+------------------------+-----------+-----------+----------+

**Real-time Constraints**:
- 30 fps @ 1080p: 33 ms per frame
- 60 fps @ 720p: 16.7 ms per frame
- 120 fps @ 480p: 8.3 ms per frame

⭐ **Keywords**: Throughput (Mpixels/s), latency budgeting, frame rate, pipeline bottleneck.

⚡ Optimization Techniques
-----------------------

**1. SIMD Vectorization**

.. code-block:: c

    // Scalar demosaicing (slow)
    for (int i = 0; i < n; i++) {
        output[i] = (input[i-1] + input[i+1]) >> 1;
    }
    
    // SIMD (ARM NEON): 4 pixels per cycle
    uint8x16_t left = vld1q_u8(input - 1);
    uint8x16_t right = vld1q_u8(input + 1);
    uint8x16_t avg = vhaddq_u8(left, right);  // Halving add

**2. Memory Access Patterns**
- Tile-based processing: Fit working set in L1 cache
- Row-major vs column-major: Choose cache-friendly layout
- Prefetching: Use DMA or software prefetch hints

**3. Fixed-Point Processing**
- Use Q8/Q15 instead of float32 where possible
- Reduces memory bandwidth, improves cache efficiency

**4. Parallel Processing**
- Tile parallelization: Split image into regions
- Line-based streaming: Process row-by-row with minimal memory

⭐ **Keywords**: Vectorization, cache optimization, tile-based processing, streaming, fixed-point acceleration.

---

Common ISP Libraries & Tools
=============================

ARM Compiler & Libraries
------------------------

- **CMSIS-DSP**: Vector/Matrix operations for ISP algorithms
- **OpenCV (ARM-optimized)**: Image processing (demosaicing, filtering, etc.)
- **TensorFlow Lite**: ML-based ISP (denoising, super-resolution)
- **LibYUV**: YUV/RGB conversion, color space handling

**Integration**:

.. code-block:: c

    #define ARM_MATH_NEON
    #include "arm_math.h"
    #include "opencv2/imgproc.hpp"
    
    // Fast bilateral filter using ARM NEON
    arm_neon_bilateral_filter(src, dst, diameter, sigma_s, sigma_r);

⭐ **Keywords**: CMSIS-DSP, OpenCV, LibYUV, TensorFlow Lite, NEON intrinsics.

🐛 Debugging & Profiling
---------------------

**Tools**:
- **Gstreamer**: Pipeline simulation and testing
- **Raw viewers**: Examine RAW frames for debugging
- **Histogram analysis**: Monitor exposure, color balance
- **Frame comparison**: Diff analysis between ISP versions

**Common Issues**:
1. **Color shift**: Incorrect white balance or CCM
2. **Posterization**: Insufficient color depth, gamma issues
3. **Artifacts**: Demosaicing errors, sharpening halos
4. **Flicker**: AE oscillation, frame-to-frame instability

⭐ **Keywords**: Gstreamer, RAW viewer, histogram, profiling, frame capture.

---

📚 Reference: Fixed-Point ISP Calculations
========================================

.. code-block:: c

    // Q8 arithmetic (typical for ISP)
    #define Q8(x) ((x) << 8)
    #define MUL_Q8(a, b) (((a) * (b)) >> 8)
    #define DIV_Q8(a, b) (((a) << 8) / (b))
    
    // Example: White balance gain (1.5× for R channel)
    uint8_t r_in = 128;
    int16_t r_gain = Q8(1.5);  // 1.5 in Q8
    uint16_t r_out = MUL_Q8(r_in, r_gain);  // = 192

---

📚 ⭐ 📚 Essential References
====================

- **MIPI Camera Serial Interface (CSI-2)**: https://mipi.org/
- **Bayer Filter Demosaicing**: https://en.wikipedia.org/wiki/Demosaicing
- **sRGB Color Space**: https://en.wikipedia.org/wiki/SRGB
- **Bilateral Filtering**: https://en.wikipedia.org/wiki/Bilateral_filter
- **ARM NEON Intrinsics**: https://developer.arm.com/architectures/instruction-sets/intrinsics/

---

**Last Updated**: January 2026 | **Compatibility**: ARM Cortex-A (all variants), Cortex-M55/M85, CMSIS-DSP v1.14+

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
