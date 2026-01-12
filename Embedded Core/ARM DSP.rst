🎵 **ARM DSP Cheatsheet (2026)**
================================

**2026 Guide**: 🚀 Comprehensive coverage of ARM CMSIS-DSP library, Cortex-M DSP hardware instructions (SIMD/NEON), and optimization strategies for embedded signal processing on ARM processors. Perfect for audio, sensor processing, ML inference! 🧠

.. contents:: Table of Contents
   :depth: 3

---

⭐ **Keywords Overview**: SIMD, NEON, Helium (MVE), fixed-point arithmetic, q-format, MAC operations, FFT/IFFT, FIR/IIR filtering, window functions, spectral analysis, parallel processing, instruction-level parallelism, cycle optimization.

---

⚙️ **Core Data Types & Fixed-Point Arithmetic**
================================================

⚙️ CMSIS-DSP Fixed-Point Representation
------------------------------------

ARM uses **Q-format** (Q n.m) for fixed-point representation: the integer portion and fractional portion split.

+----------------+--------+------------------+----------------------------+---------------------+
| Type           | Bits   | Q-Format         | Range                      | Precision           |
+================+========+==================+============================+=====================+
| q7_t           | 8-bit  | Q0.7             | -1.0 to +0.992             | 1/128 ≈ 0.0078125   |
+----------------+--------+------------------+----------------------------+---------------------+
| q15_t          | 16-bit | Q0.15            | -1.0 to +0.9999695         | 1/32768 ≈ 0.000031  |
+----------------+--------+------------------+----------------------------+---------------------+
| q31_t          | 32-bit | Q0.31            | -1.0 to +0.99999999        | 1/2^31 ≈ 4.66e-10   |
+----------------+--------+------------------+----------------------------+---------------------+
| f16_t          | 16-bit | IEEE 754         | ±6.1e-5 to ±6.55e4         | ~3.3 significant    |
+----------------+--------+------------------+----------------------------+---------------------+
| f32_t (float)  | 32-bit | IEEE 754         | ±1.18e-38 to ±3.4e38       | ~7 significant      |
+----------------+--------+------------------+----------------------------+---------------------+
| f64_t (double) | 64-bit | IEEE 754         | ±2.23e-308 to ±1.8e308     | ~15 significant     |
+----------------+--------+------------------+----------------------------+---------------------+

⭐ **Keywords**: Fixed-point saturation, rounding modes, overflow handling, scale factor selection, dynamic range preservation.

Fixed-Point 🟢 🟢 Best Practices
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Saturation**: Prevent overflow via `arm_scale_q15()` with saturation enabled
- **Rounding**: Use `__SSAT()` (signed saturate) for precision loss mitigation
- **Scale Factor**: Choose appropriate Q-format based on signal range (e.g., audio → Q0.15; sensor data → Q4.11)
- **Accumulator Width**: Use 64-bit (`q63_t`) accumulators to prevent intermediate overflow

---

🔧 **Cortex-M DSP Hardware Instructions** (The Real Performance!)
================================================================

📊 **Processor Support Matrix** (Who has what?)
-----------------------------------------------

+-------------------+--------+--------+--------+--------+--------+--------+--------+
| Instruction Set   | M0     | M3     | M4     | M7     | M33    | M55    | M85    |
+===================+========+========+========+========+========+========+========+
| 32-bit SIMD       | —      | —      | ✓      | ✓      | ✓      | ✓      | ✓      |
+-------------------+--------+--------+--------+--------+--------+--------+--------+
| Single MAC        | —      | —      | ✓      | ✓      | ✓      | ✓      | ✓      |
+-------------------+--------+--------+--------+--------+--------+--------+--------+
| Dual MAC (SMLAD)  | —      | —      | ✓      | ✓      | ✓      | ✓      | ✓      |
+-------------------+--------+--------+--------+--------+--------+--------+--------+
| NEON              | —      | —      | —      | —      | —      | Limited| Opt.   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+
| Helium (MVE)      | —      | —      | —      | —      | —      | ✓      | ✓      |
+-------------------+--------+--------+--------+--------+--------+--------+--------+

⭐ **Keywords**: Cortex-M4F, Cortex-M7, Cortex-M33F, Cortex-M55, Cortex-M85, floating-point unit (FPU), DSP extensions.

⚡ **SIMD Instructions** (Single Instruction Multiple Data) - Parallel Magic!
--------------------------------------------------------------------------

**16-bit Parallel Operations**

- **SADD16**: Two 16-bit signed additions in parallel
  - `result[31:16] = Rn[31:16] + Rm[31:16]`; `result[15:0] = Rn[15:0] + Rm[15:0]`
⚙️   - **Use Case**: Vector addition, element-wise operations on 16-bit data
  
- **SSUB16**: Two 16-bit signed subtractions in parallel
⚙️   - **Use Case**: Difference computation, delta encoding
  
- **SASX** / **SASXS**: Add/Subtract eXchange (asymmetric operations)
  - Top half adds, bottom half subtracts (with optional saturation)
  - **Use Case**: Hilbert transform preprocessing, IQ signal processing

**8-bit Parallel Operations**

- **SADD8**: Four 8-bit signed additions
- **SSUB8**: Four 8-bit signed subtractions
⭐ - **Keywords**: Byte-level parallelism, SIMD lane utilization

⚡ **MAC** (Multiply-Accumulate) Instructions - The Heartbeat of DSP!
------------------------------------------------------------------

**Single MAC (32-bit result)**

- **MUL**: Simple 32x32 → 32-bit multiply
- **MLA**: Multiply-Accumulate: `Rd = Rm × Rs + Rn`
- **Latency**: 1 cycle (M4/M7 optimized pipelines)

**Dual MAC (two 16-bit multiplications in parallel)**

- **SMLAD**: Signed Multiply-Accumulate Dual 16-bit
  - `Rd = (Rm[31:16] × Rs[31:16]) + (Rm[15:0] × Rs[15:0]) + Ra`
  - **Use Case**: Complex number multiplication, 2-tap FIR filters
  - **Throughput**: 2 multiplications per cycle

- **SMLADX**: Dual MAC with cross-multiplication
  - `Rd = (Rm[31:16] × Rs[15:0]) + (Rm[15:0] × Rs[31:16]) + Ra`
  - **Use Case**: Complex conjugate multiply, decorrelation filters

**Wide MAC (32x32 → 64-bit result)**

- **SMLAL**: Signed Multiply-Accumulate Long
  - `RdHi:RdLo = Rm × Rs + RdHi:RdLo` (64-bit accumulation)
  - **Use Case**: Preventing overflow in energy calculations, long-term integration
  - **Latency**: 2-3 cycles

- **SMMLA**: Signed Most Significant Word Multiply-Accumulate
  - Returns high 32 bits of 64-bit result with rounding
  - **Use Case**: Scaling without explicit right-shift

⭐ **Keywords**: Instruction pipelining, latency hiding, dual-issue, instruction-level parallelism (ILP), MAC throughput.

---

📚 **CMSIS-DSP Library Functions** (The Toolkit!)
================================================

**Include Header**: `#include "arm_math.h"`

**Initialization**: `arm_math_status` enums for validation

⚙️ **Basic Vector Operations** (The Building Blocks)
--------------------------------------------------

.. code-block:: c

    // Vector Element-wise Addition
    void arm_add_f32(const float32_t *pSrcA, const float32_t *pSrcB, 
                     float32_t *pDst, uint32_t blockSize);
    void arm_add_q15(const q15_t *pSrcA, const q15_t *pSrcB, 
                     q15_t *pDst, uint32_t blockSize);

    // Vector Dot Product (Inner Product)
    // result = Σ(pSrcA[n] × pSrcB[n])
    void arm_dot_prod_f32(const float32_t *pSrcA, const float32_t *pSrcB, 
                          uint32_t blockSize, float32_t *result);
    void arm_dot_prod_q15(const q15_t *pSrcA, const q15_t *pSrcB, 
                          uint32_t blockSize, q63_t *result);
    
    // Vector Scaling: pDst[n] = pSrc[n] × scale
    void arm_scale_f32(const float32_t *pSrc, float32_t scale, 
                       float32_t *pDst, uint32_t blockSize);
    void arm_scale_q15(const q15_t *pSrc, q15_t scale, 
                       int8_t shift, q15_t *pDst, uint32_t blockSize);

    // Vector Multiplication (element-wise): pDst[n] = pSrcA[n] × pSrcB[n]
    void arm_mult_f32(const float32_t *pSrcA, const float32_t *pSrcB, 
                      float32_t *pDst, uint32_t blockSize);

⭐ **Keywords**: Vectorization, data parallelism, block-based processing, streaming operations.

🎯 **Linear Filtering (FIR)** - Finite Impulse Response
------------------------------------------------------

.. code-block:: c

    // FIR Filter Structure
    typedef struct {
        uint16_t numTaps;      // Number of filter coefficients
        float32_t *pState;     // Internal state buffer (ringbuffer)
        const float32_t *pCoeffs;  // Filter coefficients
    } arm_fir_instance_f32;

    // Initialize FIR filter instance
    arm_status arm_fir_init_f32(arm_fir_instance_f32 *S, 
                                uint16_t numTaps,
                                const float32_t *pCoeffs,
                                float32_t *pState,
                                uint32_t blockSize);

    // Process FIR filter: y[n] = Σ(b[k] × x[n-k])
    void arm_fir_f32(const arm_fir_instance_f32 *S, 
                     const float32_t *pSrc, float32_t *pDst, 
                     uint32_t blockSize);

**State Buffer Requirement**: `blockSize + numTaps - 1` samples

⭐ **Keywords**: Impulse response, convolution, tap coefficients, delay-line, ringbuffer, linear-phase filtering.

🔁 **IIR Filtering** (Cascaded Biquad) - Infinite Impulse Response
------------------------------------------------------------------

.. code-block:: c

    // Biquad Stage Structure: y[n] = a0×x[n] + a1×x[n-1] + a2×x[n-2] 
    //                               - b1×y[n-1] - b2×y[n-2]
    typedef struct {
        uint32_t numStages;    // Number of biquad stages
        q31_t *pState;         // State buffer (4 elements per stage)
        q31_t *pCoeffs;        // Filter coefficients (5 per stage)
    } arm_biquad_casc_df2T_instance_q31;

    // Cascaded Biquad DF2-T (Direct Form 2, Transposed)
    void arm_biquad_cascade_df2T_q31(
        const arm_biquad_casc_df2T_instance_q31 *S,
        q31_t *pSrc, q31_t *pDst, uint32_t blockSize);

⭐ **Keywords**: Feedback, poles/zeros, stability (|poles| < 1), cascade design, DF2-T topology (superior numerical stability), peaking filter, shelf filter.

🔋 **Fast Fourier Transform (FFT)** - Frequency Domain Magic!
----------------------------------------------------------

.. code-block:: c

    // Complex FFT Structure
    typedef struct {
        uint16_t fftLen;       // FFT size (power of 2: 16, 32, 64, ...)
        const float32_t *pTwiddle;  // Pre-computed twiddle factors
        const uint16_t *pBitRevTable;  // Bit-reversal lookup
    } arm_cfft_instance_f32;

    // Initialize and compute Complex FFT
    arm_status arm_cfft_init_f32(arm_cfft_instance_f32 *S, uint16_t fftLen);
    
    void arm_cfft_f32(const arm_cfft_instance_f32 *S, 
                      float32_t *p_cfft_in, uint8_t ifftFlag, 
                      uint8_t bitReverseFlag);

    // Magnitude Computation: mag[k] = √(Real²[k] + Imag²[k])
    void arm_cmplx_mag_f32(const float32_t *pSrc, float32_t *pDst, 
                           uint32_t numSamples);

    // Power Spectrum (for energy): power[k] = mag[k]²
    void arm_cmplx_mag_squared_f32(const float32_t *pSrc, float32_t *pDst, 
                                   uint32_t numSamples);

**Memory Requirements**: 
- Twiddle factors: ~2 × fftLen × 4 bytes (float32)
- Bit-reversal table: fftLen × 2 bytes

⭐ **Keywords**: Radix-2 Cooley-Tukey algorithm, frequency domain, spectral analysis, power spectral density (PSD), zero-padding, windowing.

🪟 **Window Functions** (Reduce Spectral Leakage!)
-------------------------------------------------

Windowing reduces spectral leakage before FFT:

.. code-block:: c

    // Hann Window: w[n] = 0.5 - 0.5×cos(2π×n/(N-1))
    void arm_hann_f32(float32_t *pDst, uint32_t blockSize);
    
    // Hamming Window: w[n] = 0.54 - 0.46×cos(2π×n/(N-1))
    void arm_hamming_f32(float32_t *pDst, uint32_t blockSize);
    
    // Blackman Window: Excellent sidelobe suppression
    void arm_blackman_f32(float32_t *pDst, uint32_t blockSize);

⭐ **Keywords**: Spectral leakage, main-lobe width, sidelobe attenuation, scalloping loss, window overlap (COLA).

📊 **Statistics & Analysis** (Know Your Data!)
---------------------------------------------

.. code-block:: c

    // Vector Mean
    void arm_mean_f32(const float32_t *pSrc, uint32_t blockSize, 
                      float32_t *pResult);

    // Vector RMS (Root Mean Square)
    void arm_rms_f32(const float32_t *pSrc, uint32_t blockSize, 
                     float32_t *pResult);

    // Vector Standard Deviation
    void arm_std_f32(const float32_t *pSrc, uint32_t blockSize, 
                     float32_t *pResult);

    // Vector Power (Energy): Σ(x[n]²)
    void arm_power_f32(const float32_t *pSrc, uint32_t blockSize, 
                       float32_t *pResult);

    // Min/Max Detection
    void arm_max_f32(const float32_t *pSrc, uint32_t blockSize, 
                     float32_t *pResult, uint32_t *pIndex);
    void arm_min_f32(const float32_t *pSrc, uint32_t blockSize, 
                     float32_t *pResult, uint32_t *pIndex);

⭐ **Keywords**: Variance, energy estimation, peak detection, signal-to-noise ratio (SNR), crest factor.

🔢 **Matrix Operations** (Linear Algebra on Embedded!)
-----------------------------------------------------

.. code-block:: c

    // Matrix Multiplication: C = A × B (M×N) × (N×P) = (M×P)
    void arm_mat_mult_f32(const arm_matrix_instance_f32 *pSrcA,
                          const arm_matrix_instance_f32 *pSrcB,
                          arm_matrix_instance_f32 *pDst);

    // Matrix Transpose
    void arm_mat_trans_f32(const arm_matrix_instance_f32 *pSrc,
                           arm_matrix_instance_f32 *pDst);

    // Matrix Inverse (via Cholesky or LU decomposition)
    void arm_mat_inverse_f32(const arm_matrix_instance_f32 *pSrc,
                             arm_matrix_instance_f32 *pDst);

⭐ **Keywords**: Linear algebra, LU decomposition, Cholesky factorization, rank estimation, condition number.

---

⚡ **Optimization Techniques** (Make It FAST!)
============================================

💻 **Compiler & Preprocessor Optimizations** (Unlock Performance!)
-----------------------------------------------------------------

Enable these macros in project defines or before including `arm_math.h`:

.. code-block:: c

    #define ARM_MATH_LOOPUNROLL    // Manual loop unrolling (4×)
    #define ARM_MATH_NEON          // NEON SIMD (Cortex-A series only)
    #define ARM_MATH_HELIUM        // M-Profile Vector Extension (M55/M85)
    #define ARM_MATH_ROUNDING      // Enable rounding in fixed-point ops
    #define ARM_MATH_LOOPUNROLL_LEVEL 4  // Unroll factor (2-4)

**Impact**:
- `ARM_MATH_LOOPUNROLL`: 15-30% speedup on loops
- `ARM_MATH_HELIUM`: 2-8× speedup on M55/M85 (vector-length agnostic)

⭐ **Keywords**: Loop unrolling, compiler optimization flags, pragma directives, inline assembly, intrinsics.

🚀 **Hardware Optimization Strategies** (CPU-Level Tricks!)
---------------------------------------------------------

**1. Maximize MAC Throughput**

- Use **SMLAD** for dual 16-bit multiplications
- Arrange data for 16-bit alignment when possible
- Example (complex multiply): Use `arm_cmplx_mult_f32()` instead of scalar loop

**2. Minimize Memory Bandwidth**

- Use smaller data types (q15_t vs f32_t halves bandwidth)
- Exploit instruction caches: FIR tap coefficients in ITCM/CCM
- Cascade filters rather than one large filter (better cache locality)

**3. Leverage SIMD Instructions**

- Process 2-4 elements per cycle with SADD16, SSUB16
- Intrinsics: `__SADD16()`, `__SMLAD()` (in `arm_math.h`)

**4. Parallel Processing (Helium on M55/M85)**

- Vector operations execute on full vector width (128-bit)
- Functions like `arm_add_f32()` auto-vectorize with `ARM_MATH_HELIUM`
- Automatic register packing for 2-4 parallel lanes

⭐ **Keywords**: Memory access patterns, instruction cache (I-cache), data cache (D-cache), tightly-coupled memory (TCM), cache line optimization, false sharing.

⏱️ **Real-Time Performance Considerations** (Timing Budgets!)
------------------------------------------------------------

+------------------------------+----------+-----------+-------------+
| Task                         | Cortex-M4| Cortex-M7 | Cortex-M55  |
+==============================+==========+===========+=============+
| 256-point FFT (f32)          | ~3.2 ms  | ~1.8 ms   | ~0.4 ms     |
+------------------------------+----------+-----------+-------------+
| FIR (256 taps, 1 kHz)        | ~0.25 ms | ~0.12 ms  | ~0.03 ms    |
+------------------------------+----------+-----------+-------------+
| Matrix 64×64 multiply (f32)  | ~2.1 ms  | ~0.9 ms   | ~0.15 ms    |
+------------------------------+----------+-----------+-------------+

**Estimation Formula**: 
Cycle Count ≈ (Operations × Processor Cycles/Op) / Clock Frequency (MHz)

⭐ **Keywords**: Latency budgeting, deterministic timing, interrupt latency, worst-case execution time (WCET), profiling.

---

🎯 **NEON SIMD** (Cortex-A & Limited M-Profile) - Parallel Vectors!
==================================================================

**Availability**: Cortex-A series (ARMv7-A), optional on M55/M85

🏗️ **NEON Register Architecture** (128-bit Parallelism!)
------------------------------------------------------

- **D-registers**: 64-bit (16 registers D0-D15)
- **Q-registers**: 128-bit (8 registers Q0-Q7, alias D-regs)
- **Lanes**: Partitionable into multiple data types (8×8-bit, 4×16-bit, 2×32-bit, 1×64-bit)

**Typical NEON Operations**:

.. code-block:: c

    // Vector Addition (4 × 32-bit floats in parallel)
    float32x4_t a = vld1q_f32(pSrc1);  // Load 4 floats
    float32x4_t b = vld1q_f32(pSrc2);
    float32x4_t c = vaddq_f32(a, b);   // 4 parallel adds
    vst1q_f32(pDst, c);                // Store result

⭐ **Keywords**: Intrinsic functions, NEON intrinsics, lane operations, permutation, quad-precision (128-bit).

---

⚙️ Helium Vector Extension (M-Profile Vector Extension - MVE)
==========================================================

**Available**: Cortex-M55, Cortex-M85 (ARMv8.1-M)

⭐ **Key Advantages Over Traditional NEON**:

- **VLO (Variable-Length)**: Automatic adaptation to vector length (up to 128-bit)
- **Predication**: Per-lane masking for efficient data-dependent code
- **Performance**: Up to 2× faster than NEON on equivalent operations
- **Automatic Vectorization**: CMSIS-DSP functions auto-vectorize with `ARM_MATH_HELIUM`

💻 Helium Example (Auto-Vectorized by CMSIS-DSP)
-----------------------------------------------

.. code-block:: c

    // CMSIS-DSP handles Helium vectorization transparently
    #define ARM_MATH_HELIUM
    #include "arm_math.h"

    float32_t srcA[256], srcB[256], dst[256];
    arm_add_f32(srcA, srcB, dst, 256);  // Auto-vectorized: 4 floats/cycle

⭐ **Keywords**: MVE intrinsics, `__mve_pred_only_`, predicated operations, gather/scatter, transposition.

---

📡 Common Patterns & Applications
==============================

⚙️ Audio Processing Pipeline
--------------------------

.. code-block:: c

    // 1. Input: Acquire samples (I2S/SAI interface)
    // 2. Pre-emphasis (FIR high-pass): y[n] = x[n] - 0.97×x[n-1]
⚙️     arm_fir_f32(&fir_pre, pInputBuffer, pBufferTemp, blockSize);
    
    // 3. Window (Hann): Reduce spectral leakage
    arm_mult_f32(pBufferTemp, pWindow, pBufferTemp, blockSize);
    
    // 4. FFT: Transform to frequency domain
    arm_cfft_f32(&fftInstance, pBufferTemp, 0, 1);
    
    // 5. Magnitude spectrum & energy
    arm_cmplx_mag_f32(pBufferTemp, pSpectrum, fftSize/2);
    arm_power_f32(pSpectrum, fftSize/2, &pEnergy);

⭐ **Keywords**: Pre-processing, framing, STFT (Short-Time Fourier Transform), mel-scale spectrogram.

Control System (PID with Fixed-Point)
--------------------------------------

.. code-block:: c

    // Scaled error (Q15)
🔴     q15_t error = (q15_t)((setpoint - measurement) >> 8);
    
    // Proportional term
🔴     q31_t p_term = (q31_t)error * kp;  // Implicit scaling
    
    // Integral accumulation (with anti-windup)
    if (integral < MAX_INTEGRAL) {
        integral += (q31_t)error * ki;  // Q31 accumulator
    }
    
    // Output (scaled back to 16-bit)
    q15_t output = (q15_t)((p_term + integral) >> 16);

⭐ **Keywords**: Anti-windup, integrator saturation, PI loop, servo control, realtime constraints.

---

🐛 Debugging & Profiling
=======================

Common Pitfalls
---------------

1. **Fixed-Point Overflow**: Insufficient scale factor → clipping
   - *Solution*: Monitor peak values; use `arm_scale_q15()` with saturation

2. **Spectral Leakage**: Insufficient windowing → spectral smearing
   - *Solution*: Apply Hann or Hamming window before FFT

3. **Filter Instability**: IIR poles outside unit circle → divergence
   - *Solution*: Validate pole locations; use biquad cascade (DF2-T)

4. **Memory Fragmentation**: Large state buffers (FIR) → stack overflow
   - *Solution*: Allocate state buffers in CCM or static memory

🐛 Profiling Tools
----------------

- **Cortex-M Cycle Counter (CYCCNT)**: Measure CPU cycles
  
  .. code-block:: c

      CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
      DWT->CTRL |= DWT_CTRL_CYCCNTEN_Msk;
      uint32_t start = DWT->CYCCNT;
      // ... code to profile
      uint32_t elapsed = DWT->CYCCNT - start;

- **Compiler Flags**: `-O3 -march=armv7e-m -mfpu=fpv4-sp-d16`
- **Disassembly Analysis**: Verify SMLAD/SIMD instruction usage

⭐ **Keywords**: Performance counters, wall-clock time, instruction distribution, cache misses, profiler overhead.

---

📚 Reference: Data Type Conversion Quick Reference
===============================================

.. code-block:: c

    // Float → Q15 (scale by 2^15)
    q15_t q = (q15_t)(float_val * 32768.0f);
    
    // Q15 → Float (scale by 2^-15)
    float val = (float)q / 32768.0f;
    
    // Q15 → Q31 (shift left by 16)
    q31_t q31 = (q31_t)q15 << 16;
    
    // Saturated Right-Shift (Q31 → Q15)
    q15_t q15 = __SSAT((q31_val + (1 << 15)) >> 16, 16);

---

📚 ⭐ 📚 Essential References
====================

- **CMSIS-DSP v1.14+ Documentation**: https://www.keil.com/pack/doc/CMSIS/DSP/html/
- **ARM Cortex-M4/M7 Generic User Guide**: https://developer.arm.com/
- **CMSIS-DSP GitHub**: https://github.com/ARM-software/CMSIS-DSP
- **Cortex-M55/M85 Architecture Reference**: ARMv8.1-M specification
- **Fixed-Point Arithmetic Guide**: https://en.wikipedia.org/wiki/Q_(number_format)

---

**Last Updated**: January 2026 | **Compatibility**: ARM Cortex-M0-M85, CMSIS-DSP v1.14+

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

✨ **TL;DR Cheatsheet** (The 30-Second Version!)
================================================

✅ **Fixed-Point**: Q-format encoding; Q15 = [-1, +0.9999], 1 LSB ≈ 0.00003
✅ **SIMD**: SADD16, SSUB16 (2 ops/cycle); SMLAD (2 MACs/cycle)
✅ **MAC**: MLA, SMLAD, SMMLA, SMLAL (64-bit)
✅ **FIR**: Convolution, linear-phase, state buffer = blockSize + numTaps - 1
✅ **IIR**: Feedback loop, cascade biquads (DF2-T), poles must be |p| < 1
✅ **FFT**: Radix-2, twiddle factors, bit-reversal permutation
✅ **Windows**: Hann/Hamming (spectral leakage), Blackman (best sidelobe)
✅ **Optimize**: Loop unroll, MAC throughput, memory bandwidth, SIMD width
✅ **Helium**: M55/M85 MVE, 2× NEON speed, auto-vectorizes CMSIS-DSP
✅ **Profile**: Use CYCCNT, disassembly, -O3 optimization

---

🚀 **Common Gotchas** (Don't Get Bitten!)
========================================

| Issue                      | Root Cause                | Fix                         |
|----------------------------|-------------------------|-----------------------------|
| Overflow in fixed-point    | Scale factor too small  | Use `arm_scale_q15(...)`   |
| Spectral leakage in FFT    | No windowing            | Apply Hann/Hamming window  |
| IIR filter blows up        | Poles outside unit circle| Design with |poles| < 1    |
| Slow FIR performance       | Cache misses             | Use coefficients in ITCM   |
| Helium not activating      | Missing `#define`       | Add `#define ARM_MATH_HELIUM`|

---

**Last updated:** 2026-01-12 | **CMSIS-DSP v1.14+**

