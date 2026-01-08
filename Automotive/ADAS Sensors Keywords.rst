=====================================
ADAS Sensors & ISP Keywords Reference
=====================================

**2026 Guide**: Comprehensive keyword dictionary for Advanced Driver Assistance Systems (ADAS) sensors, sensor fusion, image signal processing (ISP), and automotive perception technologies.

.. contents:: Table of Contents
   :depth: 2

---

ADAS Sensor Fundamentals
========================

Core Sensor Types
~~~~~~~~~~~~~~~~~

**Camera / Vision Sensor**
  Optical sensor using CMOS/CCD imaging array capturing visible light (380-750 nm) for high-resolution object classification, lane detection, traffic sign recognition, and semantic segmentation. Typical resolution: 1080p-8K, frame rate: 30-120 fps. Strength: semantic understanding. Weakness: poor in fog/rain/snow.

**Radar (Radio Detection and Ranging)**
  Millimeter-wave (77-79 GHz) electromagnetic sensor measuring range via FMCW (Frequency-Modulated Continuous Wave) and velocity via Doppler shift. Update rate: 10-50 Hz. Strength: weather-robust, direct velocity measurement. Weakness: low angular resolution, poor object classification.

**LiDAR (Light Detection and Ranging)**
  Laser-based sensor (905 nm or 1550 nm) creating 3D point clouds via time-of-flight measurement. Point density: 10k-300k points/scan. Strength: high spatial resolution (cm-level), excellent low-light. Weakness: expensive (declining), degrades in heavy rain/snow.

**Ultrasonic / Sonar Sensor**
  Acoustic pulse sensor (40 kHz typical) measuring distance via sound wave propagation. Range: 0.2-5 m. Strength: very low cost (~$10-30), weather-independent. Weakness: very limited range, field of view restricted.

**Infrared / Thermal Camera**
  Long-Wave Infrared (LWIR, 8-14 μm) or Near-Infrared (NIR, 0.7-1.0 μm) sensor detecting heat signatures. Sensitivity: ~50 mK NETD. Strength: night vision, pedestrian detection by body heat. Weakness: lower resolution than visible cameras, requires external IR illumination (NIR).

**GPS / GNSS (Global Navigation Satellite System)**
  Satellite-based absolute positioning (accuracy: 1-5 m standard, <10 cm with RTK). Strength: global coverage, absolute position. Weakness: vulnerable to jamming/spoofing, GPS-denied areas (tunnels, urban canyons).

**IMU (Inertial Measurement Unit)**
  Combined accelerometers (3-axis) + gyroscopes (3-axis) + magnetometer measuring vehicle motion. Strength: dead-reckoning in GPS-denied areas, high-frequency motion data. Weakness: drift over time without GPS correction.

Sensor Fusion & Perception
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Sensor Fusion**
  Integration of data from multiple sensors (camera + radar + LiDAR + ultrasonic) using statistical methods (Kalman filtering, Bayesian fusion) to create unified object representations with improved accuracy, redundancy, and robustness. Three approaches: early (low-level raw data fusion), late (decision-level fusion), intermediate (feature-level fusion).

**Multi-Modal Fusion**
  Combining heterogeneous sensor modalities (vision + mmWave + acoustic) for complementary information: camera provides semantic classes, radar provides velocity, LiDAR provides 3D shape.

**Kalman Filter / Extended Kalman Filter (EKF)**
  Recursive Bayesian estimation algorithm tracking object state (position, velocity) by predicting next state and correcting with sensor measurements. Update rate: 10-50 Hz. Computational load: ~1-5 GFLOPS per object.

**Hungarian Algorithm**
  Graph matching algorithm solving data association problem (matching current detections to previous tracked objects) in O(n³) time. Minimizes total assignment cost across multiple objects.

**Mahalanobis Distance**
  Normalized statistical distance metric accounting for measurement uncertainty, used in data association to match detections to tracks. Formula: D² = (z - ẑ)ᵀ × S⁻¹ × (z - ẑ), where S is innovation covariance.

**Object Tracking / Multi-Object Tracking (MOT)**
  Temporal association of detections across consecutive frames maintaining consistent object IDs. Metrics: MOTA (Multiple Object Tracking Accuracy), IDF1 (ID F1 Score).

**Detection Bounding Box**
  2D (x, y, width, height) or 3D (x, y, z, length, width, height, rotation) axis-aligned rectangle localizing object. Confidence score: 0-1 indicating detection confidence.

**Point Cloud**
  3D data representation as collection of points with (x, y, z) coordinates. LiDAR point clouds typically 10k-300k points per frame. Format: LAS/LAZ or proprietary binary.

**SLAM (Simultaneous Localization and Mapping)**
  Real-time technique building spatial map of environment while localizing vehicle position. Uses camera + IMU or LiDAR + IMU. Enables HD map building for autonomous vehicles.

Object Detection & Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Object Detection**
  Identifying and localizing objects (vehicles, pedestrians, cyclists, road signs) in sensor data. Output: bounding box + class label + confidence. Networks: YOLO, Faster R-CNN, EfficientDet, Mask R-CNN.

**Semantic Segmentation**
  Pixel-wise classification assigning each image pixel to class (road, lane, sidewalk, sky, etc.). Networks: SegNet, DeepLabv3+, U-Net. Used for road/lane detection in ADAS.

**Instance Segmentation**
  Combining object detection + semantic segmentation distinguishing individual object instances. Networks: Mask R-CNN, YOLACT. Enables separate tracking of overlapping objects.

**3D Object Detection**
  Detecting objects in 3D space from LiDAR point clouds or stereo camera depth. Output: 3D bounding box (x, y, z, l, w, h, rotation). Networks: PointNet++, VoxelNet, PV-RCNN.

**Lane Detection**
  Identifying road lane markings and boundaries. Approaches: edge detection (Canny, Sobel), semantic segmentation, curve fitting (polynomial or spline). Used for LKA (Lane Keep Assist).

**Traffic Sign Recognition (TSR)**
  Classifying traffic signs (stop, yield, speed limits, etc.) from camera images. Resolution requirement: high (sign must be ~20-30 pixels). Network: ResNet, EfficientNet.

**Pedestrian Detection**
  Identifying human figures in camera or thermal images. Challenges: pose variation, occlusion, small size at distance. Networks: SSD, RetinaNet, specialized pedestrian detectors.

**Vehicle Classification**
  Categorizing detected vehicles into classes (car, truck, bus, motorcycle). Helps ADAS differentiate behavior (truck = longer braking distance, motorcycle = smaller size).

Sensor Specifications & Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Field of View (FOV)**
  Angular range sensor captures. Camera: 30-180°+, Radar: 50-90°, LiDAR: 120-360° (mechanical) or 120° × 25° (solid-state). Horizontal FOV critical for multi-vehicle detection.

**Range / Maximum Range**
  Maximum distance sensor reliably detects objects. Camera: 50-250 m (depends on object size), Radar LR: 150-250+ m, LiDAR: 100-200 m, Ultrasonic: 5-7 m.

**Range Resolution**
  Minimum distance difference to distinguish two objects. Radar: ~0.1-0.2 m, LiDAR: ~0.01-0.05 m (point spacing), Camera: N/A (depth from disparity or monocular estimation).

**Angular Resolution / Azimuth Resolution**
  Minimum angle separation to distinguish two objects side-by-side. Camera: ~0.1° (depends on resolution + FOV), Radar: 5-30° (depends on antenna array), LiDAR: ~0.1-0.5°.

**Update Rate / Frame Rate**
  Frequency of sensor data capture. Camera: 30-120 fps typical, Radar: 10-50 Hz, LiDAR mechanical: 10 Hz, LiDAR solid-state: 20-50 Hz.

**Latency**
  Time delay from sensor capture to data availability for processing. Camera: ~5-10 ms, Radar: ~20-50 ms, LiDAR mechanical: ~30-100 ms (due to rotation), LiDAR solid-state: ~10-20 ms.

**Accuracy (Positional)**
  Error in detected object position/bounding box. Camera: ±50 pixels typical (depends on distance), Radar: ±0.2-0.5 m, LiDAR: ±0.1 m.

**Velocity Accuracy**
  Error in measured velocity. Radar: ±0.2-0.5 m/s, LiDAR: ~0.1-0.2 m/s (temporal differentiation), Camera: N/A (requires separate depth/tracking).

**Signal-to-Noise Ratio (SNR)**
  Ratio of signal power to noise power. Higher SNR = better detection reliability. Radar SNR: typically 5-20 dB for target detection.

**Receiver Operating Characteristic (ROC)**
  Plot of true positive rate (TPR) vs false positive rate (FPR) for detector. Metric: Area under ROC curve (AUC), 1.0 = perfect.

**Mean Average Precision (mAP)**
  Standard metric for object detection evaluation averaged over IoU thresholds and object classes. Threshold typically IoU > 0.5 (loose) or > 0.75 (strict).

---

Image Signal Processing (ISP) Pipeline
=======================================

Core ISP Concepts
~~~~~~~~~~~~~~~~~

**ISP (Image Signal Processor)**
  Dedicated hardware block or software module converting raw CMOS/CCD sensor data (Bayer pattern) into standard image format (RGB/YUV) suitable for human viewing or machine vision. Typical latency: 10-50 ms. Computational load: 0.5-5 TFLOPS depending on resolution/algorithms.

**Raw Data / Bayer Pattern**
  Unprocessed sensor output where each pixel captures only one color (red, green, or blue) via color filter array. Standard patterns: RGGB, GRBG, GBRG, BGGR. Requires demosaicing to produce full RGB image.

**Demosaicing / Debayering / CFA Interpolation**
  Interpolating missing color values from neighboring pixels to reconstruct full RGB image from Bayer CFA. Algorithms: nearest neighbor (poor quality), bilinear (moderate), edge-directed (EDAC, good quality), high-quality (12+ sample kernels).

**Sensor Black Level / Pedestal**
  Fixed dark offset from sensor dark current and circuitry (~50-100 mV typical). Removed via black level correction to properly center image data and improve dynamic range.

**Pixel Binning**
  Combining signals from multiple adjacent pixels before readout, reducing resolution but improving light sensitivity. 2×2 binning: resolution halved, ~4× signal improvement.

**Rolling Shutter vs Global Shutter**
  **Rolling Shutter**: Rows read sequentially (1-50 ms readout time), causes temporal distortion in fast motion. **Global Shutter**: All pixels captured simultaneously, eliminates distortion. Automotive ADAS prefers global shutter for reliability.

ISP Processing Stages
~~~~~~~~~~~~~~~~~~~~~

**Auto Exposure Control (AEC)**
  Dynamically adjusting integration time (shutter speed) and/or analog/digital gain to maintain target image brightness. Algorithms: histogram-based, metering patterns (average, center-weighted, spot, matrix). Response time: ~100-300 ms typical.

**Auto White Balance (AWB)**
  Correcting color cast from different light sources (tungsten, daylight, fluorescent) by scaling R/G/B channel gains. Algorithms: gray-world assumption, histogram-based, machine learning. Target: white objects appear neutral.

**Color Filter Array (CFA) / Color Mosaic**
  Arrangement of red, green, blue filters overlaying sensor pixels. Common pattern RGGB: Bayer array with 1R:2G:1B ratio (human eye more sensitive to green). Requires proper demosaicing.

**Noise Reduction / Denoising**
  Removing sensor noise (shot noise, thermal noise, read noise) while preserving image details. Spatial filtering: bilateral filter, Gaussian blur, morphological operations. Temporal filtering: frame averaging, motion-compensated denoising. Trade-off: noise reduction vs blur/ghosting.

**HDR (High Dynamic Range) / Tone Mapping**
  Merging multiple exposures or compressing dynamic range to handle scenes with both bright (headlights, sun) and dark (road, shadows) regions. Algorithms: weighted averaging, gradient domain methods, bilateral filtering. Computational overhead: ~10-15% vs single exposure.

**Gamma Correction**
  Non-linear brightness adjustment mapping linear sensor data to perceptual brightness. sRGB gamma = 2.2 (typical). Formula: V_out = V_in^(1/gamma). Improves low-light visibility without clipping.

**Lens Distortion Correction**
  Removing barrel (pincushion distortion from wide-angle lenses via radial distortion model: r_distorted = r_undistorted × (1 + k1×r² + k2×r⁴). Requires calibration to estimate k1, k2 coefficients. Essential for accurate lane detection, object localization.

**Lens Shading / Vignetting Correction**
  Compensating for uneven illumination across image from lens optical properties. Correction: multiply pixel by position-dependent gain map (pre-computed from flat-field calibration). Typical gain variation: ±20-30% from center to edges.

**Color Correction / Color Correction Matrix (CCM)**
  3×3 matrix transformation converting from sensor color space to standard output space (sRGB, Adobe RGB, etc.). Accounts for camera spectral sensitivity vs standard observer response. Matrix calibrated against color reference (Macbeth ColorChecker).

**Bad Pixel Correction / Defective Pixel Removal**
  Identifying and interpolating stuck pixels, hot pixels (sensor defects) or dead pixels (permanently low output). Methods: spatial interpolation from neighbors, temporal averaging across frames. Typical defect rate: <100 bad pixels per megapixel.

**Sharpening / Edge Enhancement**
  Boosting contrast at edges to improve apparent sharpness. Algorithms: unsharp mask (output = input + strength × (input - blurred)), Sobel/Laplacian-based sharpening. Trade-off: increased noise, ringing artifacts at high strength.

**Histogram Equalization / Contrast Stretching**
  Expanding tonal range by redistributing histogram to fill full dynamic range. Improves visibility in low-contrast images. Algorithms: global histogram equalization, CLAHE (Contrast Limited Adaptive Histogram Equalization, local processing).

**Saturation / Color Enhancement**
  Adjusting color intensity (saturation) of image for perceptual enhancement. Typical adjustment: 0.8-1.2× saturation (0 = grayscale, 1 = normal, >1 = oversaturated).

**Chroma Subsampling**
  Reducing color information resolution while preserving luminance (exploits human vision sensitivity). Formats: 4:4:4 (full), 4:2:2 (horizontal reduce 2×), 4:2:0 (both horizontal + vertical reduce 2×). Bandwidth reduction: 4:2:0 = 50% vs 4:4:4.

**Lens Optical Aberration Correction**
  Correcting chromatic aberration (misalignment of R/G/B channels from lens), spherical aberration (focus variation across FOV). Methods: per-channel spatial registration, polynomial correction models.

Advanced ISP Features
~~~~~~~~~~~~~~~~~~~~~

**Machine Vision ISP**
  ISP pipeline optimized for object detection (AI) rather than human viewing. Characteristics: minimal post-processing, raw-like output (high contrast), aggressive noise reduction. Bypass gamma correction, preserve linear light.

**Multi-ISP / Parallel ISP**
  Processing multiple camera streams simultaneously (8-12 cameras in typical Level 2+ ADAS). Requires multi-channel hardware or time-division multiplexing. Per-camera ISP instance: ~500 MB-2 GB DRAM.

**ISP Tuning / Parameterization**
  Optimizing ISP parameters (AEC target, AWB gains, noise reduction strength, sharpening amount) to maximize downstream perception accuracy. Method: iterate on test dataset, measure detection mAP/recall.

**Stereo ISP**
  Coordinated ISP processing for stereo camera pairs ensuring consistency across cameras (matched white balance, exposure, gamma). Critical for stereo matching accuracy (epipolar geometry).

**Raw Image Recording**
  Storing unprocessed sensor data (Bayer pattern) for offline ISP development/tuning. Enables flexibility in algorithm changes without re-recording. Storage: ~50-100 MB/s per camera @ 30 fps.

**ISP Latency Budget**
  Time constraint for ISP processing within overall ADAS system latency budget (~130-260 ms total for Level 2). ISP typically 5-20 ms, leaving 110-255 ms for object detection, fusion, decision-making.

Depth Estimation Methods
~~~~~~~~~~~~~~~~~~~~~~~~

**Stereo Vision / Stereo Matching**
  Computing disparity map from stereo camera pair by finding corresponding pixels in left/right images. Depth = (baseline × focal_length) / disparity. Accuracy: ~5-10% of distance. Latency: 10-50 ms depending on resolution.

**Epipolar Geometry**
  Geometric relationship constraining matching of stereo pairs. Epipolar line: line in right image where corresponding left pixel must lie (eliminates 2D search space to 1D). Essential for stereo efficiency.

**Disparity Map**
  Dense depth map from stereo matching where each pixel has estimated disparity (in pixels). Typical resolution: 1280×720 (half HD). Post-processing: median filter, LR consistency check for outlier removal.

**Monocular Depth Estimation**
  Estimating depth from single camera using self-supervised deep learning (MiDaS, ZoeDepth, MonoDepth2). Advantages: cheaper (single camera), no calibration. Disadvantages: relative depth, less accurate than stereo.

**Structure from Motion (SfM)**
  Reconstructing 3D scene from video sequence by tracking feature motion across frames. Enables depth estimation from monocular video. Used in SLAM for mapping.

**Optical Flow**
  Estimating pixel-wise motion between consecutive frames. Used for: motion estimation (video stabilization), depth from motion, temporal filtering. Algorithms: Lucas-Kanade, FlowNet (deep learning).

---

Sensor Technologies & Hardware
=======================================

Radar Technology
~~~~~~~~~~~~~~~~

**FMCW (Frequency-Modulated Continuous Wave)**
  Radar modulation sweeping transmit frequency over bandwidth during chirp duration (10-100 μs). Beat frequency between transmitted and received signals encodes target range. Standard in automotive 77 GHz.

**Doppler Shift**
  Change in signal frequency from moving target: Δf = 2 × f_tx × v / c. Radar extracts velocity from beat frequency change between chirps. Accuracy: ~0.05 m/s per Hz.

**Beamforming / Phased Array**
  Controlling antenna array phase/amplitude to electronically steer radar beam without mechanical rotation. Enables multiple simultaneous beams. Typical array: 3 TX + 4 RX antennas.

**Monopulse Radar**
  Extracting angle-of-arrival from amplitude/phase difference between antenna elements in single pulse. Faster than sequential scanning.

**Constant False Alarm Rate (CFAR)**
  Adaptive thresholding maintaining constant false alarm rate despite clutter/noise variations. Algorithm: cell averaging CFAR, sliding window over range-Doppler map.

**RCS (Radar Cross Section)**
  Measure of object reflectivity (m² units). Larger RCS = easier detection. Example: car ~20 m², motorcycle ~2 m², pedestrian ~0.5 m². Range ~ sqrt(RCS), so small RCS objects need closer range.

**77 GHz vs 79 GHz**
  Standard automotive frequencies (W-band). 77 GHz global allocation (some interference concerns). 79 GHz emerging for better coexistence. 24 GHz legacy (phasing out).

**Antenna Gain**
  Measure of directivity (dB). Higher gain = narrower beam = better angular resolution but smaller coverage area. Typical automotive: 18-25 dBi.

LiDAR Technology
~~~~~~~~~~~~~~~~

**Time-of-Flight (ToF) / Time-of-Flight Measurement**
  Distance = (speed_of_light × round_trip_time) / 2. Light speed = 3×10⁸ m/s. Example: 100 m range requires 667 ns round-trip time. Accuracy: ~0.01-0.1 m depending on timing resolution.

**Mechanical Scanning LiDAR**
  Velodyne HDL-64E style: rotating laser + mirror assembly capturing 64 channels (vertical angle stacking). Rotation rate: 5-20 Hz. Advantages: 360° coverage, mature. Disadvantages: moving parts, latency from rotation.

**Solid-State LiDAR**
  No moving parts: uses MEMS (microelectromechanical) mirror or phased array steering. Advantages: compact, reliable, faster update (20-50 Hz). Disadvantages: smaller FOV (120° × 25° vs 360° × 50°), immature supply.

**Flash LiDAR**
  Entire scene illuminated simultaneously in single laser pulse. No scanning delay. Disadvantages: high cost (~$20k+), limited FOV, low point density for ADAS.

**Laser Wavelength**
  905 nm (most common, NIR): high power available, mature components. 1550 nm (SWIR): eye-safe, better fog penetration, emerging 2025-2026. 532 nm (green): high sensitivity, niche/research.

**Pulse Repetition Rate (PRF)**
  Frequency of laser pulses. Higher PRF = faster updates but range ambiguity. Typical automotive: 100 kHz - 1 MHz.

**Laser Safety / IEC 60825-1**
  Classification system: Class 1 (<0.39 mW, safe), 1M (pulsed variant), 3R (5 mW, caution), 3B (500 mW, restricted), Class 4 (high power, dangerous). Automotive typically Class 1M or 3B.

**Beam Divergence**
  Angular width of laser beam. Smaller = tighter focus = smaller spot size at distance. Typical: 0.1-0.3° (10m range = 17-50 cm spot diameter).

**Voxelization**
  Converting continuous point cloud to 3D grid (voxels). Resolution: 0.1-0.5 m typical. Reduces memory (10k points → 1M voxel grid) but discretizes space.

**Ground Plane Extraction**
  Identifying road surface (ground) points from point cloud using RANSAC or height-based filtering. Removes road from clutter for cleaner obstacle detection.

Camera Technology
~~~~~~~~~~~~~~~~~

**CMOS Sensor**
  Complementary metal-oxide-semiconductor active pixel sensor. Advantages: low power, fast readout, integrated circuitry. Disadvantages: higher noise, less quantum efficiency than CCD.

**CCD Sensor**
  Charge-coupled device: shift register reads accumulated charge. Advantages: high quantum efficiency, low noise. Disadvantages: higher power, slower readout.

**Quantum Efficiency (QE)**
  Percentage of photons converted to electrons. Typical: 60-80% for automotive CMOS. Higher QE = better low-light sensitivity.

**Dark Current**
  Leakage current from thermal excitation (electrons without incident photons). Temperature dependent (~doubles every 6-8°C). Creates black level offset. Mitigated: cooling, dark frame subtraction.

**Read Noise**
  Noise from readout electronics independent of light. Typical: 5-10 electrons RMS. Dominates in dark areas. Improves with newer sensor generations.

**Shot Noise / Photon Noise**
  Statistical noise from discrete photon arrivals (Poisson distribution). Magnitude: sqrt(N) where N = number of photons. Dominates in bright areas.

**Full Well Capacity**
  Maximum charge a pixel can hold before saturation. Typical: 30k-100k electrons. Defines dynamic range (FWC / read_noise).

**Pixel Size**
  Physical dimension of individual pixel. Smaller pixel: higher resolution at same die size, worse light-gathering (higher noise). Typical automotive: 2-3 μm.

**Global Shutter** (see above)

**Rolling Shutter** (see above)

Ultrasonic Technology
~~~~~~~~~~~~~~~~~~~~~

**Piezoelectric Transducer**
  Crystal material vibrating at specific frequency when driven by AC voltage. 40 kHz resonance for automotive parking sensors. Efficient mechanical oscillation, low cost.

**Acoustic Impedance**
  Property resisting wave motion (Z = density × sound_velocity). Impedance mismatch at boundaries causes reflections (echo). Air-to-plastic: large mismatch, good reflection.

**Speed of Sound**
  ~343 m/s at 20°C sea level. Varies with temperature (±0.6 m/s per °C). Requires compensation in measurement: distance = speed × time / 2.

**Ring-Down Effect**
  Transducer continues oscillating after transmit pulse ends, blinding receiver to echoes from very close objects. Typical ring-down: 1-2 ms. Defines minimum range (~20-30 cm).

**Envelope Detection**
  Extracting amplitude envelope of RF signal using rectification + low-pass filter. Outputs DC signal proportional to received acoustic amplitude.

**Threshold Crossing Detection**
  Detecting when received signal crosses amplitude threshold to determine time-of-arrival. Simple method, sensitive to threshold setting (false positives/negatives).

**Time-Division Multiplexing (TDM)**
  Sequencing transmissions from multiple ultrasonic sensors to avoid crosstalk (each sensor transmits at different time). Typical: 8 sensors × ~10 Hz = multiplexed at ~80 kHz.

**Temperature Compensation**
  Adjusting distance calculation for speed of sound variation with temperature. Formula: distance = (speed × (1 + 0.002 × (T - 20))) × time / 2.

Thermal/Infrared Technology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Microbolometer**
  Uncooled infrared detector: thin resistive element (amorphous Si or vanadium oxide) with temperature-dependent resistance. Detects heat via resistance change. Advantages: uncooled, compact. Disadvantages: lower sensitivity, drift with temperature.

**NETD (Noise Equivalent Temperature Difference)**
  Sensitivity metric: temperature difference producing signal equal to noise floor. Typical automotive: ~50 mK (can detect 0.05°C temperature difference). Lower NETD = more sensitive.

**Non-Uniformity Correction (NUC)**
  Compensating for pixel-to-pixel sensitivity variations in bolometer array via offset + gain calibration. Periodic NUC (every ~30 sec) corrects calibration drift.

**Bolometer Drift**
  Gradual change in sensor sensitivity over time from material aging, temperature cycling. Requires periodic recalibration. Causes baseline shift in thermal image.

**Blackbody Radiation**
  All objects emit IR radiation according to temperature. Stefan-Boltzmann law: radiance ∝ T⁴. Human (~310K) peaks at ~10 μm (LWIR range).

**Emissivity**
  Fraction of theoretical blackbody radiation emitted. Metal: low emissivity (~0.1), skin: high (~0.98). Affects temperature measurement accuracy.

**Staring Array / Uncooled FPA (Focal Plane Array)**
  Grid of microbolometer pixels (64×48 to 320×256 typical). "Uncooled" = no cryogenic cooling needed (unlike older cooled IR). Update rate: 9-60 Hz.

---

ADAS Standards & Compliance
=============================

Safety Standards
~~~~~~~~~~~~~~~~

**ISO 26262 (Functional Safety for Automotive)**
  Specifies safety lifecycle, processes, and ASIL (Automotive Safety Integrity Level) definitions (A=lowest to D=highest). Requirement: ADAS must achieve target ASIL via redundancy, diagnostics, failsafes. Affects sensor selection, architecture.

**SAE J3016 (Driving Automation Levels)**
  Defines automation levels 0-5:
  - Level 0: No automation
  - Level 1: Driver assistance (ACC, LKA)
  - Level 2: Partial automation (both steering + ACC)
  - Level 3: Conditional automation (vehicle handles most, driver on standby)
  - Level 4-5: High/Full automation (no driver needed)

**SAE J3061 (Cybersecurity Guidebook)**
  Guidelines for protecting vehicles from cyber attacks. Sensor spoofing (radar jamming, GPS spoofing, LiDAR blinding) emerging threat. Recommends sensor authentication, redundancy.

**ASIL (Automotive Safety Integrity Level)**
  Risk classification (A-D, D highest) based on severity × probability. ASIL D systems require higher test coverage, validation rigor.

**SOTIF (Safety of the Intended Functionality)**
  ISO 26262:2018 Addition: addresses risks from sensor errors, algorithmic limitations (not just component failures). E.g., camera fails in fog = functional failure requiring detection/mitigation.

Performance & Test Standards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**mAP (Mean Average Precision)**
  Standard object detection evaluation metric. Averaged over IoU thresholds and classes. Typical benchmark: COCO (Common Objects in Context) dataset.

**Confusion Matrix / Precision / Recall**
  - **True Positive (TP)**: correct detection. **False Positive (FP)**: incorrect detection. **False Negative (FN)**: missed detection.
  - **Precision** = TP / (TP + FP): fraction of detections correct.
  - **Recall** = TP / (TP + FN): fraction of ground truth detected.

**F1 Score**
  Harmonic mean of precision + recall. F1 = 2 × (precision × recall) / (precision + recall). Balanced metric for imbalanced datasets.

**IoU (Intersection over Union)**
  Bounding box overlap metric: IoU = intersection / union. Typical threshold: IoU > 0.5 for detection match. Stricter threshold (>0.75) for higher quality.

**NHTSA Safety Standards**
  US regulations covering ADAS braking distance, reaction time. Example: AEB must achieve 80% reduction of crash speed for typical scenarios.

**Euro NCAP Testing**
  European safety ratings testing AEB, LKA on test tracks with real-world scenarios (pedestrians, vehicles, obstacles).

---

Integration & System Concepts
=============================

Sensor Architecture
~~~~~~~~~~~~~~~~~~~

**Distributed Architecture**
  Each sensor has local ECU (microcontroller) processing raw data, sending high-level detections over vehicle bus (CAN, FlexRay, Ethernet). Advantages: modularity, real-time per-sensor processing. Disadvantages: bus bandwidth limits, latency from serialization.

**Centralized Architecture**
  All raw sensor data → Central ECU (high-performance SoC) performing all processing. Advantages: better fusion, optimization. Disadvantages: single point of failure, extreme compute/power demands.

**Hybrid Architecture**
  Sensors perform initial filtering/compression locally, detailed processing centrally. Balance of distributed modularity + centralized optimization.

**Bus / Communication Protocol**
  CAN (1 Mbps, traditional), FlexRay (10 Mbps, redundant), Ethernet (100 Mbps-1 Gbps, modern). Vehicle synchronization: all sensors timestamped to master clock ±50 ms tolerance.

Compute Platforms
~~~~~~~~~~~~~~~~~

**NVIDIA Orin**
  200 TFLOPS, Arm-based, power-efficient. Used in various ADAS platforms.

**Tesla FSD Computer**
  144 TFLOPS, custom hardware, optimized for full self-driving inference. Dual boards (redundancy).

**Qualcomm Snapdragon Ride**
  Multi-core ARM + GPU + neural accelerator. Automotive-grade thermal/power management.

**Mobileye SuperVision SoC**
  Integrated perception + decision stack in single SoC. Road-centric mapping focus.

**TI Jacinto**
  TI automotive deep learning accelerator (TIDL). Supports multiple frameworks (TensorFlow, PyTorch).

**Hardware Acceleration Units**
  Dedicated neural network accelerators (NPU, TPU, etc.) speeding up inference 10-100×. Essential for real-time processing.

---

Performance Metrics & Benchmarking
===================================

Latency Breakdown (System-Level)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Sensor Capture**: 5-10 ms (frame readout time)
**Sensor → ECU Transfer**: 10-20 ms (CAN/Ethernet transmission)
**ISP Processing**: 5-20 ms (demosaicing, color correction, etc.)
**Object Detection**: 50-100 ms (neural network inference)
**Tracking/Fusion**: 10-20 ms (Kalman filter, data association)
**Decision Logic**: 5-10 ms (ADAS rules evaluation)
**Vehicle Actuation**: 50-100 ms (brake/steering response)
**Total**: ~130-260 ms (acceptable for Level 2), Target <100 ms for Level 3+

**Real-Time Processing Requirements**
  30 fps = 33 ms per frame budget. 60 fps = 16.7 ms. All processing must complete within frame period.

Computational Load Estimation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Measurement Units**:
- **FLOPS**: Floating-point operations per second. 1 TFLOPS = 10¹² FLOPS.
- **GFLOPS**: 10⁹ FLOPS (billions operations/sec).

**Per-Sensor Load**:
- Camera object detection (1080p): 2-5 TFLOPS
- Camera lane detection: 0.1-0.5 TFLOPS
- Radar signal processing: 1-3 TFLOPS
- LiDAR point cloud + 3D NN: 10-50 TFLOPS
- Fusion/tracking: 5-10 TFLOPS

**System Total** (Mid-Range Level 2):
- 8 cameras: 5-10 TFLOPS
- 6 radars: 3-5 TFLOPS
- Fusion: 5-10 TFLOPS
- **Total: 15-30 TFLOPS**

Power Budget
~~~~~~~~~~~~

**Typical Mid-Range ADAS**: 30-50 W total (sensors + compute)
- Cameras: 10-15 W
- Radars: 5-10 W
- LiDAR (optional): 10-15 W
- Compute SoC: 20-30 W

**Premium Level 3**: 50-100+ W (more cameras, LiDAR, high-end SoC)

Accuracy Metrics
~~~~~~~~~~~~~~~~

**Detection Accuracy**: mAP @ IoU 0.5 / IoU 0.75, typically 80-95% for ADAS benchmark datasets.
**Tracking Accuracy**: MOTA (Multiple Object Tracking Accuracy), IDF1 (ID F1 Score).
**Depth Accuracy**: RMSE (Root Mean Squared Error) in meters, typical 5-10% of range.
**Latency**: Total system latency <150 ms Level 2, <100 ms Level 3.

---

**Last Updated**: January 2026
**Compatibility**: ADAS Level 0-3, ISO 26262 / SAE J3016 standards
**Scope**: Sensors, ISP, fusion, standards, performance metrics

