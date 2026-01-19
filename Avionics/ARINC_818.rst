===================================================================
ARINC 818 — Avionics Digital Video Bus
===================================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC 818** defines a high-bandwidth digital video interface for avionics based on **Fibre Channel (FC-AE-ASM)**.

**Key Characteristics:**
- **Base Technology:** Fibre Channel - Avionics Environment (FC-AE-ASM)
- **Speed:** 1.0625, 2.125, 4.25, 8.5 Gbps (multi-rate)
- **Topology:** Point-to-point or switched fabric
- **Video Formats:** SMPTE 274M (HD), SMPTE 296M (720p), custom formats
- **Applications:** FLIR cameras, EVS (Enhanced Vision), synthetic vision, reconnaissance
- **Advantages:** High bandwidth, fiber optic (EMI immunity, lightweight)

**Typical Systems:**
- **F-35 EO-DAS:** 6× infrared cameras, 360° situational awareness
- **Enhanced Vision Systems (EVS):** FLIR thermal imaging for low-visibility landing
- **Helmet-Mounted Displays (HMD):** High-resolution video to pilot's visor
- **Unmanned Aircraft:** Real-time ISR video downlink
- **Reconnaissance Pods:** Multi-spectral imaging

**ARINC 818 vs Alternatives:**

.. code-block:: text

   Feature            ARINC 818      Camera Link    Analog Video
   ────────────────── ──────────────────────────────────────────
   Bandwidth          Up to 8.5 Gbps 680 Mbps       ~6 Mbps
   Cable              Fiber optic    Copper MDR26   Coax
   Distance           10+ km         10 m           100 m
   EMI Immunity       Excellent      Poor           Moderate
   Weight             Low            High           Moderate
   Certification      DO-178C/254    Industrial     Legacy
   Latency            <1 ms          ~100 μs        >16 ms
   Cost               High           Moderate       Low

================================================================================
1. Overview & Background
================================================================================

**1.1 Why Digital Video in Avionics?**
----------------------------------------

**Legacy Analog Video Problems:**
- Low resolution (NTSC: 480i, PAL: 576i)
- Susceptible to EMI/noise
- Heavy coax cabling
- Difficult to process/compress
- No metadata (requires separate data bus)

**Digital Video Advantages:**
- **High Definition:** 1080p/4K support
- **Lossless transmission:** No generational loss
- **Metadata integration:** Embed telemetry, GPS, sensor data
- **Fiber optic:** EMI-immune, lightweight, long distance
- **Processing:** Direct input to image processing (target tracking, sensor fusion)

**ARINC 818 Introduction (2007):**
- Based on Fibre Channel - Avionics Environment (FC-AE-ASM)
- Standardizes video formats, control protocol, metadata
- Enables multi-vendor interoperability (camera ↔ display)

**1.2 Market Adoption**
------------------------

**Military Aircraft:**
- **F-35 Lightning II:** EO-DAS (Distributed Aperture System), EOTS (Electro-Optical Targeting System)
- **F-22 Raptor:** Sensor fusion displays
- **Boeing P-8 Poseidon:** Multi-spectral maritime reconnaissance
- **MQ-9 Reaper UAV:** ISR video downlink

**Commercial Aircraft:**
- **Enhanced Vision Systems (EVS):** Gulfstream G650, Bombardier Global 7500
- **External Cameras:** Airbus A350 tail camera, Boeing 787 wing cameras
- **Maintenance Cameras:** Engine borescopes, landing gear inspection

================================================================================
2. Fibre Channel Fundamentals
================================================================================

**2.1 FC-AE-ASM Architecture**
-------------------------------

**Fibre Channel Avionics Environment - Avionics Streaming Management (FC-AE-ASM):**

.. code-block:: text

   Layer Model:
   
   ┌──────────────────────────────────────┐
   │  Application (ARINC 818 Commands)    │  ← Video control, metadata
   ├──────────────────────────────────────┤
   │  FC-4 (Upper Layer Protocol)         │  ← Mapping layer
   ├──────────────────────────────────────┤
   │  FC-2 (Framing/Flow Control)         │  ← Ordered sets, frames
   ├──────────────────────────────────────┤
   │  FC-1 (Encode/Decode - 8b/10b)       │  ← Line coding
   ├──────────────────────────────────────┤
   │  FC-0 (Physical - Fiber/Copper)      │  ← 1/2/4/8 Gbps serializer
   └──────────────────────────────────────┘

**FC-AE-ASM vs Standard Fibre Channel:**
- **Deterministic:** Avionics requires guaranteed latency
- **Streaming:** Optimized for video (not storage like FC-SAN)
- **Simplified:** Reduced protocol overhead for real-time

**2.2 Physical Layer (FC-0)**
------------------------------

**Supported Speeds:**

.. code-block:: text

   Rate    Line Rate   Encoded Rate  Payload Rate
   ──────  ──────────  ────────────  ────────────
   1GFC    1.0625 Gbps  850 Mbps     ~100 MB/s
   2GFC    2.125 Gbps  1700 Mbps     ~200 MB/s
   4GFC    4.25 Gbps   3400 Mbps     ~400 MB/s
   8GFC    8.5 Gbps    6800 Mbps     ~800 MB/s
   
   Note: 8b/10b encoding adds 25% overhead

**Fiber Optic Transceivers:**
- **Multimode Fiber (MMF):** 62.5/50 μm, OM1/OM2/OM3
  - Distance: 500 m @ 1 GFC, 150 m @ 4 GFC
  - Wavelength: 850 nm (VCSEL laser)
- **Single-Mode Fiber (SMF):** 9 μm
  - Distance: 10+ km @ 1 GFC
  - Wavelength: 1310 nm / 1550 nm

**Connectors:**
- **MIL-DTL-38999 Series III:** Ruggedized for avionics
- **ARINC 801 Fiber Optic Connectors:** Quad Small Form-factor Pluggable (QSFP)

**2.3 Encoding (FC-1): 8b/10b**
--------------------------------

**8b/10b Line Coding:**
- Converts 8-bit data → 10-bit symbols
- Ensures DC balance (equal 1s and 0s)
- Embedded clock recovery (no separate clock line)

**Special Characters (K-codes):**

.. code-block:: text

   K28.5: Comma (frame synchronization)
   K28.2: Start of Frame (SOF)
   K28.3: End of Frame (EOF)
   K28.1: Idle (link idle state)

**Example 8b/10b Encoding:**

.. code-block:: text

   Data (8-bit):  0xD2 (11010010)
   Symbol (10-bit): 0b0101010110 (chosen for DC balance)
   
   Running Disparity (RD):
   - Track cumulative 1s - 0s
   - Alternate between RD+ and RD- symbols
   - Maintains long-term DC balance

================================================================================
3. ARINC 818 Protocol
================================================================================

**3.1 Frame Structure**
------------------------

**ARINC 818 Video Frame:**

.. code-block:: text

   ┌────────────────────────────────────────────────────┐
   │                   FC Frame Header                   │  24 bytes
   ├─────────────────────┬──────────────────────────────┤
   │   ARINC 818 Header  │      Video Payload           │
   │      (32 bytes)     │  (up to 2112 bytes)          │
   ├─────────────────────┴──────────────────────────────┤
   │                   FC Frame CRC                      │  4 bytes
   └────────────────────────────────────────────────────┘
   
   Total: 24 + 32 + payload + 4 = 60 + payload bytes

**ARINC 818 Header Fields:**

.. code-block:: c

   typedef struct {
       uint32_t sequence_number;     // Frame counter
       uint32_t timestamp;            // 1 μs resolution
       uint16_t image_width;          // Pixels per line
       uint16_t image_height;         // Lines per image
       uint16_t pixel_format;         // Encoding (RGB, YUV, etc.)
       uint16_t bits_per_pixel;       // 8, 10, 12, 16
       uint8_t  frame_type;           // Progressive/Interlaced
       uint8_t  reserved[7];
   } ARINC818_Header;

**Pixel Formats:**

.. code-block:: text

   Code  Format       Description
   ────  ───────────  ────────────────────────────────────
   0x01  Mono8        8-bit grayscale
   0x02  Mono10       10-bit grayscale (packed)
   0x03  Mono12       12-bit grayscale
   0x10  RGB8         24-bit RGB (8-8-8)
   0x11  RGB10        30-bit RGB (10-10-10)
   0x20  YUV422       YCbCr 4:2:2 (8-bit)
   0x21  YUV444       YCbCr 4:4:4 (8-bit)
   0x30  Bayer8       8-bit Bayer pattern (raw sensor)

**3.2 Video Streaming Protocol**
----------------------------------

**Image Transmission:**

.. code-block:: text

   Camera (Talker):
   
   1. Start of Image (SOI) command
   2. Send image lines:
      For each line:
        - ARINC 818 header (line metadata)
        - Pixel data (width × bytes_per_pixel)
   3. End of Image (EOI) command
   
   Display (Listener):
   
   1. Receive SOI → allocate framebuffer
   2. Receive lines → write to buffer
   3. Receive EOI → display complete frame

**Latency Calculation:**

.. code-block:: text

   Example: 1920×1080 @ 60 Hz, RGB8, 4 GFC
   
   Frame size = 1920 × 1080 × 3 bytes = 6.2 MB
   Frame time = 1/60 = 16.67 ms
   
   Transmission time = 6.2 MB / 400 MB/s = 15.5 ms
   Overhead (headers, gaps) ≈ 5%
   
   Total latency ≈ 16.3 ms (meets 60 Hz requirement)
   
   For 4GFC, achievable frame rates:
   - 1080p RGB8: ~60 Hz
   - 720p RGB8: ~120 Hz
   - 1080p Mono8: ~180 Hz (thermal imaging)

**3.3 Command & Control Protocol**
------------------------------------

**ARINC 818 Commands (FC-4 Layer):**

.. code-block:: c

   // Command packet structure
   typedef struct {
       uint8_t command_code;
       uint8_t node_address;      // Target camera/display
       uint16_t parameter_id;     // What to control
       uint32_t parameter_value;  // New value
   } ARINC818_Command;
   
   // Common commands
   #define CMD_SET_GAIN           0x10  // Camera gain (0-255)
   #define CMD_SET_EXPOSURE       0x11  // Exposure time (μs)
   #define CMD_SET_FRAMERATE      0x12  // Frames per second
   #define CMD_SET_ROI            0x20  // Region of Interest
   #define CMD_START_STREAM       0x30  // Begin video
   #define CMD_STOP_STREAM        0x31  // Stop video
   #define CMD_GET_STATUS         0x40  // Camera status query
   #define CMD_SET_FOCUS          0x50  // Lens focus position

**Example: Adjust Camera Gain**

.. code-block:: c

   void set_camera_gain(uint8_t node_id, uint8_t gain_value) {
       ARINC818_Command cmd;
       
       cmd.command_code = CMD_SET_GAIN;
       cmd.node_address = node_id;
       cmd.parameter_id = 0;  // Default gain parameter
       cmd.parameter_value = gain_value;  // 0-255
       
       fc_send_command(&cmd, sizeof(cmd));
   }

================================================================================
4. ARINC 818 Implementation Example
================================================================================

**4.1 Camera (Talker) Implementation**
----------------------------------------

.. code-block:: c

   #include <stdint.h>
   #include "fc_driver.h"    // Fibre Channel driver
   #include "arinc818.h"
   
   #define IMAGE_WIDTH  1920
   #define IMAGE_HEIGHT 1080
   #define BYTES_PER_PIXEL 3  // RGB8
   
   // Camera state
   typedef struct {
       uint8_t *framebuffer;      // Raw camera data
       uint32_t sequence_number;
       uint8_t streaming;
   } Camera_State;
   
   Camera_State camera;
   
   // Initialize camera
   void camera_init(void) {
       camera.framebuffer = malloc(IMAGE_WIDTH * IMAGE_HEIGHT * BYTES_PER_PIXEL);
       camera.sequence_number = 0;
       camera.streaming = 0;
       
       fc_init(FC_SPEED_4GFC);  // 4.25 Gbps
   }
   
   // Send one line of image
   void send_image_line(uint16_t line_number) {
       ARINC818_Header header;
       uint8_t *line_data;
       
       // Build header
       header.sequence_number = camera.sequence_number;
       header.timestamp = get_microsecond_timer();
       header.image_width = IMAGE_WIDTH;
       header.image_height = IMAGE_HEIGHT;
       header.pixel_format = PIXEL_FORMAT_RGB8;
       header.bits_per_pixel = 24;
       header.frame_type = FRAME_PROGRESSIVE;
       
       // Get line data from framebuffer
       line_data = camera.framebuffer + (line_number * IMAGE_WIDTH * BYTES_PER_PIXEL);
       
       // Send FC frame (header + line data)
       fc_send_frame(&header, sizeof(header), line_data, IMAGE_WIDTH * BYTES_PER_PIXEL);
   }
   
   // Transmit complete frame
   void transmit_frame(void) {
       if (!camera.streaming) return;
       
       // Start of Image
       fc_send_command(CMD_START_OF_IMAGE, camera.sequence_number);
       
       // Send all lines
       for (uint16_t line = 0; line < IMAGE_HEIGHT; line++) {
           send_image_line(line);
       }
       
       // End of Image
       fc_send_command(CMD_END_OF_IMAGE, camera.sequence_number);
       
       camera.sequence_number++;
   }
   
   // 60 Hz timer interrupt
   void TIMER_60HZ_IRQHandler(void) {
       capture_camera_image(camera.framebuffer);  // From sensor
       transmit_frame();
   }

**4.2 Display (Listener) Implementation**
-------------------------------------------

.. code-block:: c

   // Display state
   typedef struct {
       uint8_t *framebuffer;      // Display buffer
       uint32_t last_sequence;
       uint16_t current_line;
   } Display_State;
   
   Display_State display;
   
   // Initialize display
   void display_init(void) {
       display.framebuffer = malloc(IMAGE_WIDTH * IMAGE_HEIGHT * BYTES_PER_PIXEL);
       display.last_sequence = 0;
       display.current_line = 0;
       
       fc_init_listener(FC_SPEED_4GFC);
       fc_register_callback(fc_receive_callback);
   }
   
   // Fibre Channel receive callback
   void fc_receive_callback(FC_Frame *frame) {
       ARINC818_Header *header = (ARINC818_Header *)frame->payload;
       uint8_t *pixel_data = frame->payload + sizeof(ARINC818_Header);
       
       // Check for sequence number jump (dropped frames)
       if (header->sequence_number != display.last_sequence + 1) {
           printf("WARNING: Dropped frame (expected %u, got %u)\n",
                  display.last_sequence + 1, header->sequence_number);
       }
       
       // Check if Start of Image
       if (frame->command == CMD_START_OF_IMAGE) {
           display.current_line = 0;
           display.last_sequence = header->sequence_number;
           return;
       }
       
       // Copy line to framebuffer
       uint32_t offset = display.current_line * IMAGE_WIDTH * BYTES_PER_PIXEL;
       memcpy(display.framebuffer + offset, pixel_data, IMAGE_WIDTH * BYTES_PER_PIXEL);
       display.current_line++;
       
       // Check if End of Image
       if (frame->command == CMD_END_OF_IMAGE) {
           // Display complete frame
           render_framebuffer_to_screen(display.framebuffer);
       }
   }

**4.3 Python Simulation (ARINC 818 Parser)**
----------------------------------------------

.. code-block:: python

   import struct
   import numpy as np
   from PIL import Image
   
   class ARINC818Parser:
       # Pixel formats
       PIXEL_FORMAT_MONO8 = 0x01
       PIXEL_FORMAT_RGB8 = 0x10
       PIXEL_FORMAT_YUV422 = 0x20
       
       def __init__(self):
           self.sequence = 0
           self.framebuffer = None
       
       def parse_header(self, data):
           """Parse ARINC 818 header (32 bytes)"""
           header = struct.unpack('>IIHHHHHB7x', data[:32])
           return {
               'sequence': header[0],
               'timestamp': header[1],
               'width': header[2],
               'height': header[3],
               'pixel_format': header[4],
               'bits_per_pixel': header[5],
               'frame_type': header[6]
           }
       
       def decode_rgb8_line(self, line_data, width):
           """Decode RGB8 line to numpy array"""
           pixels = np.frombuffer(line_data, dtype=np.uint8)
           return pixels.reshape((width, 3))
       
       def receive_frame(self, fc_frames):
           """Receive sequence of FC frames comprising one image"""
           lines = []
           
           for frame in fc_frames:
               header = self.parse_header(frame[:32])
               pixel_data = frame[32:]
               
               if header['pixel_format'] == self.PIXEL_FORMAT_RGB8:
                   line = self.decode_rgb8_line(pixel_data, header['width'])
                   lines.append(line)
           
           # Stack lines into image
           image_array = np.vstack(lines)
           return Image.fromarray(image_array, 'RGB')
       
       def save_image(self, fc_frames, filename):
           """Save received ARINC 818 image"""
           img = self.receive_frame(fc_frames)
           img.save(filename)
           print(f"Saved {filename}: {img.size[0]}×{img.size[1]}")
   
   # Example usage
   parser = ARINC818Parser()
   
   # Simulate receiving FC frames (from camera)
   fc_frames = load_fc_capture("flir_video.bin")
   parser.save_image(fc_frames, "thermal_image.png")

================================================================================
5. Enhanced Vision Systems (EVS)
================================================================================

**5.1 FLIR Thermal Imaging**
------------------------------

**Forward-Looking Infrared (FLIR) Cameras:**
- Detect 8-14 μm infrared (thermal radiation)
- See through fog, haze, darkness
- Display on Head-Up Display (HUD) or Head-Down Display (HDD)

**EVS Architecture:**

.. code-block:: text

   ┌─────────────┐         ARINC 818         ┌──────────────┐
   │ FLIR Camera ├──────────────────────────►│ EVS Computer │
   │  (Nose)     │      4 GFC, Fiber         │              │
   └─────────────┘                           └──────┬───────┘
                                                    │ ARINC 818
                                                    ▼
                                             ┌──────────────┐
                                             │  HUD/HDD     │
                                             │  (Overlay)   │
                                             └──────────────┘
   
   EVS Computer:
   - Image enhancement (gain, contrast)
   - Overlay symbology (runway outline, ILS guidance)
   - Sensor fusion (combine visual + IR)

**FAR 91.175 EVS Requirements (2004):**
- Allows lower approach minimums with certified EVS
- Must display FLIR image on HUD
- Pilot must identify visual references (runway, lights)

**Gulfstream G650 EVS:**
- **Camera:** Elbit SkyLens FLIR (640×480, 60 Hz)
- **Interface:** ARINC 818 @ 2 GFC
- **Display:** Collins Aerospace HUD (1280×1024 overlay)
- **Benefit:** Land in 1000 RVR (Runway Visual Range) vs 2400 RVR standard

**5.2 Image Processing Pipeline**
-----------------------------------

.. code-block:: text

   FLIR Sensor → ARINC 818 → Image Processor → Enhanced Display
   
   Image Processing Steps:
   
   1. Noise Reduction:
      - Temporal filtering (average N frames)
      - Spatial filtering (Gaussian blur)
   
   2. Histogram Equalization:
      - Expand contrast (hot spots = white, cold = black)
      - Adaptive (local contrast enhancement)
   
   3. Edge Enhancement:
      - Sobel filter to detect runway edges
      - Highlight obstacles (trees, buildings)
   
   4. Symbology Overlay:
      - ILS localizer/glideslope
      - Runway outline (synthetic)
      - Flight path vector
   
   5. Color Mapping (optional):
      - White-hot (hot = white)
      - Black-hot (hot = black)
      - Rainbow (pseudocolor)

**Python Image Enhancement Example:**

.. code-block:: python

   import cv2
   import numpy as np
   
   def enhance_flir_image(raw_image):
       """EVS image processing pipeline"""
       
       # 1. Noise reduction (Gaussian blur)
       denoised = cv2.GaussianBlur(raw_image, (5, 5), 0)
       
       # 2. Histogram equalization (improve contrast)
       equalized = cv2.equalizeHist(denoised)
       
       # 3. Edge enhancement (Sobel filter)
       sobelx = cv2.Sobel(equalized, cv2.CV_64F, 1, 0, ksize=3)
       sobely = cv2.Sobel(equalized, cv2.CV_64F, 0, 1, ksize=3)
       edges = np.sqrt(sobelx**2 + sobely**2)
       
       # 4. Combine enhanced image + edges
       enhanced = cv2.addWeighted(equalized, 0.8, edges.astype(np.uint8), 0.2, 0)
       
       return enhanced
   
   # Example: Process FLIR frame
   flir_frame = receive_arinc818_frame()  # From camera
   enhanced = enhance_flir_image(flir_frame)
   display_on_hud(enhanced)

================================================================================
6. Helmet-Mounted Displays (HMD)
================================================================================

**6.1 F-35 Helmet-Mounted Display System (HMDS)**
---------------------------------------------------

**Architecture:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────┐
   │         EO-DAS (6× IR Cameras) - 360° Coverage       │
   ├──────┬──────┬──────┬──────┬──────┬──────────────────┤
        │      │      │      │      │      │
        │ ARINC 818 (8 GFC, Fiber Optic)
        ▼      ▼      ▼      ▼      ▼      ▼
   ┌────────────────────────────────────────────────────┐
   │         Avionics Computer (Sensor Fusion)          │
   └────────────────────┬───────────────────────────────┘
                        │ ARINC 818 (4 GFC)
                        ▼
                 ┌──────────────┐
                 │  HMDS (Pilot)│  1280×1024 per eye (stereo)
                 └──────────────┘

**EO-DAS Cameras:**
- 6× infrared cameras (top, bottom, left, right, front-left, front-right)
- 640×480 @ 60 Hz each
- Combined data rate: 6 × (640×480×1 byte×60 Hz) = 110 MB/s

**Sensor Fusion:**
- Stitch 6 camera views into spherical panorama
- Track pilot head position/orientation
- Render view corresponding to helmet pointing direction
- Overlay symbology (HUD, targeting reticle, waypoints)

**HMDS Latency Requirement:**
- **Total latency:** <20 ms (camera capture → display update)
- **Motion-to-photon:** <16 ms (prevents motion sickness)
- ARINC 818 enables <1 ms video transmission latency

**6.2 Latency Budget**
-----------------------

.. code-block:: text

   Component                     Latency
   ───────────────────────────── ─────────
   Camera capture                2 ms (60 Hz exposure)
   ARINC 818 transmission        0.8 ms (4 GFC, 1 MB image)
   Sensor fusion processing      5 ms (GPU warping/stitching)
   Symbology rendering           3 ms (OpenGL overlay)
   Display refresh               2 ms (60 Hz panel)
   ─────────────────────────────────────
   Total                         12.8 ms ✓ (meets <16 ms requirement)

================================================================================
7. ARINC 818 vs Alternatives
================================================================================

**7.1 Comparison Table**
-------------------------

.. code-block:: text

   Feature           ARINC 818     Camera Link   CoaXPress   SDI (HD-SDI)
   ───────────────── ────────────  ────────────  ──────────  ─────────────
   Bandwidth         8.5 Gbps      680 Mbps      6.25 Gbps   1.485 Gbps
   Cable             Fiber optic   Copper MDR26  Coax        Coax
   Max Distance      10+ km        10 m          100 m       100 m
   Connector         MIL-38999     MDR26         BNC         BNC
   EMI Immunity      Excellent     Poor          Moderate    Moderate
   Weight (100m)     2 kg          15 kg         8 kg        6 kg
   Power over Cable  No            Yes (PoCL)    Yes (PoC)   No
   Certification     DO-178C/254   Industrial    Industrial  Broadcast
   Cost (camera)     High ($$$)    Moderate ($$) Moderate    Low ($)
   Latency           <1 ms         ~100 μs       ~50 μs      >16 ms
   Metadata          ARINC 818     GenICam       CXP protocol SMPTE 2110

**When to Use ARINC 818:**
- Long cable runs (>10 m), especially in large aircraft
- EMI-sensitive environments (near radar, jamming)
- High bandwidth (1080p @ 60 Hz or 4K)
- Certification required (military/commercial avionics)
- Integration with FC-AE network

**When to Use Alternatives:**
- **Camera Link:** Short distances, industrial cameras (non-certified)
- **CoaXPress:** High frame rate (300+ fps), machine vision
- **HD-SDI:** Broadcast-quality video, legacy systems

================================================================================
8. Certification & DO-178C/254 Compliance
================================================================================

**8.1 Software Certification (DO-178C)**
-----------------------------------------

**ARINC 818 Software Components:**
- **Fibre Channel Driver:** DAL A/B (critical)
- **Video Encoder/Decoder:** DAL B/C
- **Image Processing:** DAL C/D (depends on function)

**Verification Requirements:**

.. code-block:: text

   DAL B (Failure prevents continued safe flight):
   
   - Requirements: 100% coverage
   - Source code: 100% coverage (MC/DC)
   - Object code: Structural coverage analysis
   - Testing: Normal + abnormal cases
   
   Critical Functions:
   - Frame synchronization (prevent garbled image)
   - Error detection/recovery (CRC validation)
   - Latency guarantee (<16 ms for HMD)

**8.2 Hardware Certification (DO-254)**
-----------------------------------------

**ARINC 818 Hardware (FPGA/ASIC):**
- **Fibre Channel PHY:** 8b/10b encoder/decoder
- **Video Formatter:** Pixel packetization
- **DMA Controller:** Memory bandwidth management

**DO-254 Design Assurance (DAL B):**

.. code-block:: text

   Requirement                    DAL B
   ────────────────────────────── ─────────────────────────
   Requirements capture           Mandatory
   HDL coding standards           Mandatory (DO-254 Annex A)
   Functional verification        100% coverage
   Timing analysis                Static timing analysis
   Fault injection testing        Mandatory
   Environmental testing          DO-160G (temp, vibration)

**Critical Design Considerations:**
- **Single Event Upset (SEU):** FPGA configuration memory protection (scrubbing)
- **Timing closure:** Meet 8.5 Gbps serializer/deserializer (SerDes) specs
- **Power supply filtering:** Prevent EMI from SerDes switching noise

================================================================================
9. Exam Preparation — 5 Questions
================================================================================

**Question 1: Bandwidth Calculation (12 points)**

Calculate required ARINC 818 link speed for:
- **Image:** 1920×1080 pixels
- **Pixel format:** RGB10 (10-bit per channel, 30 bits per pixel)
- **Frame rate:** 60 Hz
- **Protocol overhead:** 15%

a) Calculate raw data rate (4 pts)
b) Include overhead (3 pts)
c) Choose minimum FC speed (2 pts)
d) What is utilization at that speed? (3 pts)

**Answer:**

a) **Raw Data Rate:**
   - Pixels per frame: 1920 × 1080 = 2,073,600
   - Bits per pixel: 30 (10R + 10G + 10B)
   - Bits per frame: 2,073,600 × 30 = 62,208,000 bits
   - Frames per second: 60
   - **Raw data rate:** 62,208,000 × 60 = **3.73 Gbps**

b) **With Overhead:**
   - Protocol overhead: 15% (headers, gaps, FC framing)
   - Effective rate: 3.73 Gbps / 0.85 = **4.39 Gbps**

c) **Minimum FC Speed:**
   - Available: 1.0625, 2.125, **4.25**, 8.5 Gbps
   - **4 GFC (4.25 Gbps) is insufficient** (4.39 > 4.25)
   - **Must use 8 GFC (8.5 Gbps)**

d) **Utilization:**
   - Utilization = 4.39 Gbps / 8.5 Gbps = **51.6%**
   - Good design margin (48.4% headroom)

---

**Question 2: Latency Analysis (10 points)**

For F-35 HMDS, analyze total latency:
- Camera capture: 60 Hz (rolling shutter, 10 ms exposure)
- ARINC 818 transmission: 1 MB image @ 4 GFC
- Sensor fusion: 6 cameras, GPU processing 120 fps
- Display: 60 Hz LCD

a) Calculate transmission time (4 pts)
b) Estimate sensor fusion latency (3 pts)
c) Total worst-case latency? (3 pts)

**Answer:**

a) **Transmission Time:**
   - Image size: 1 MB = 8 Mb
   - 4 GFC payload rate: 3.4 Gbps (after 8b/10b overhead)
   - Transmission: 8 Mb / 3.4 Gbps = **2.35 ms**

b) **Sensor Fusion Latency:**
   - GPU processing: 120 fps → 8.33 ms per frame budget
   - Stitch 6 cameras: ~5 ms (parallel processing)
   - Render symbology: ~2 ms
   - **Total sensor fusion: ~7 ms**

c) **Worst-Case Total Latency:**

.. code-block:: text

   Component               Latency
   ─────────────────────── ───────
   Camera exposure         10 ms (rolling shutter)
   ARINC 818 transmit      2.35 ms
   Sensor fusion           7 ms
   Display refresh         16.67 ms (60 Hz worst-case)
   ───────────────────────────────
   Total                   36 ms
   
   **Exceeds 20 ms requirement!**
   
   Optimization needed:
   - Use global shutter camera (2 ms exposure)
   - Reduce fusion latency (5 ms target)
   - 120 Hz display (8.33 ms refresh)
   
   Optimized total: 2 + 2.35 + 5 + 8.33 = 17.68 ms ✓

---

**Question 3: Error Detection (8 points)**

ARINC 818 uses Fibre Channel CRC for error detection.

a) What is FC frame CRC polynomial and length? (2 pts)
b) If bit error rate = 10⁻¹², what is frame error rate for 2000-byte frames? (4 pts)
c) How does system handle corrupted frames? (2 pts)

**Answer:**

a) **FC CRC:**
   - **Polynomial:** CRC-32 (x³²+x²⁶+x²³+...+x+1)
   - **Length:** 32 bits (4 bytes)
   - Appended to end of each FC frame

b) **Frame Error Rate:**
   - Frame size: 2000 bytes = 16,000 bits
   - Bit error rate (BER): 10⁻¹²
   - **Frame error probability:**
     
     P(error) ≈ 16,000 × 10⁻¹² = 1.6 × 10⁻⁸
   
   - At 60 Hz: 60 × 1.6 × 10⁻⁸ = **9.6 × 10⁻⁷ errors/second**
   - **~1 error per 12 days** (very reliable)

c) **Error Handling:**
   - **Discard frame:** CRC mismatch → drop frame
   - **Retransmission:** Camera resends frame (if time permits)
   - **Interpolation:** Display uses previous frame (temporal interpolation)
   - **Status flag:** Set "video degraded" warning to pilot

---

**Question 4: Fiber Optic Design (10 points)**

Design fiber optic link for reconnaissance pod:
- **Distance:** 25 meters (pod to cockpit)
- **Environment:** -55°C to +85°C, vibration 10G
- **Data rate:** 4 GFC
- **Connector:** MIL-DTL-38999

a) Choose fiber type (SMF vs MMF) and justify (4 pts)
b) Calculate link budget (3 pts)
c) What environmental testing required? (3 pts)

**Answer:**

a) **Fiber Type:**
   - **Multimode Fiber (MMF) 50 μm OM3**
   - **Justification:**
     - Distance: 25 m well within MMF range (500 m @ 1 GFC, 150 m @ 4 GFC) ✓
     - Lower cost than SMF ($50 vs $200 per connector)
     - Easier alignment (50 μm vs 9 μm core)
     - VCSEL laser cheaper than SMF laser
   - **Wavelength:** 850 nm (standard for MMF)

b) **Link Budget:**

.. code-block:: text

   Component                      Value
   ────────────────────────────── ──────────
   Transmitter power (VCSEL)      -4 dBm
   Connector loss (2×)            -1.5 dB
   Fiber attenuation (25m @ 3 dB/km) -0.075 dB
   Bend loss (conservative)       -1 dB
   Margin (temperature, aging)    -3 dB
   ──────────────────────────────────────
   Total loss                     -5.575 dB
   
   Receiver sensitivity (4 GFC):  -15 dBm
   Received power:                -4 - 5.575 = -9.575 dBm
   Link margin:                   -9.575 - (-15) = 5.4 dB ✓
   
   **Adequate margin** (typical requirement: >3 dB)

c) **Environmental Testing (DO-160G):**
   - **Temperature:** -55°C to +85°C operational (Section 4)
   - **Vibration:** 10G operational, 15G crash (Section 8)
   - **Humidity:** 95% RH (Section 6)
   - **Salt fog:** 5% NaCl (Section 6)
   - **Fluid resistance:** Hydraulic fluid, fuel, cleaning agents (Section 13)
   - **EMI/EMC:** Radiated emissions/susceptibility (Section 21)
   
   **Fiber-specific:**
   - Connector retention force (pull test: 20 lbf minimum)
   - Fiber bend radius (>10× fiber diameter = 1.25 mm)
   - Optical power stability over temperature

---

**Question 5: System Design (10 points)**

Design ARINC 818 video distribution for aircraft with:
- 1× FLIR camera (nose)
- 2× displays (pilot PFD, copilot PFD)
- 1× video recorder (for post-flight review)

a) Draw topology (point-to-point vs switched fabric) (4 pts)
b) Calculate aggregate bandwidth (3 pts)
c) How to handle display failure? (3 pts)

**Answer:**

a) **Topology:**

**Option 1: Point-to-Point (Simpler, Lower Cost)**

.. code-block:: text

   ┌──────────┐
   │   FLIR   │
   │  Camera  │
   └────┬─────┘
        │ ARINC 818 (2 GFC)
        ▼
   ┌──────────────┐    ARINC 818    ┌──────────────┐
   │   Video      ├───────────────►│  Pilot PFD   │
   │  Splitter    │    (2 GFC)      └──────────────┘
   │   (FPGA)     ├───────────────►┌──────────────┐
   └──────────────┘    (2 GFC)     │ Copilot PFD  │
        │                          └──────────────┘
        │ ARINC 818 (2 GFC)
        ▼
   ┌──────────────┐
   │   Recorder   │
   └──────────────┘

**Option 2: Switched Fabric (More Scalable)**

.. code-block:: text

   ┌──────────┐      ┌───────────────┐      ┌──────────────┐
   │   FLIR   ├─────►│               ├─────►│  Pilot PFD   │
   └──────────┘      │  FC Switch    ├─────►│ Copilot PFD  │
                     │  (3 in, 3 out)├─────►│   Recorder   │
                     └───────────────┘      └──────────────┘

**Recommendation:** Point-to-point for 3 outputs (simpler, lower latency)

b) **Aggregate Bandwidth:**
   - FLIR camera: 640×480×1 byte×60 Hz = 18.4 MB/s = 147 Mbps
   - 3× outputs: 147 Mbps (same data, multicast)
   - **Link speed:** 2 GFC (2.125 Gbps) sufficient (7% utilization)

c) **Display Failure Handling:**
   - **Built-In Test (BIT):** Each display sends heartbeat to camera
   - **Missing heartbeat:** Camera flags failed display
   - **Pilot action:** Switch to backup display (standby instruments)
   - **Recorder:** Continue recording even if displays fail (accident investigation)
   - **Redundancy:** Critical aircraft may have 2× FLIR cameras (nose + tail)

================================================================================
10. Completion Checklist
================================================================================

□ Understand Fibre Channel architecture (FC-0 to FC-4 layers)
□ Know 8b/10b encoding (DC balance, K-codes)
□ Decode ARINC 818 header (sequence, timestamp, pixel format)
□ Calculate video bandwidth (resolution × fps × bpp)
□ Implement camera (talker) in C
□ Implement display (listener) in C
□ Design fiber optic link budget
□ Understand EVS FLIR image processing
□ Calculate latency for HMD applications
□ Compare ARINC 818 vs Camera Link/CoaXPress
□ Apply DO-178C/254 certification requirements
□ Design video distribution topology (point-to-point vs switched)

================================================================================
11. Key Takeaways
================================================================================

1. **ARINC 818 = FC-AE-ASM for Video:** Fibre Channel adapted for avionics streaming

2. **High Bandwidth:** Up to 8.5 Gbps supports 4K video, multi-camera systems

3. **Fiber Optic Benefits:** EMI-immune, lightweight, long distance (10+ km)

4. **8b/10b Encoding:** Embedded clock, DC balance, special K-codes for framing

5. **Low Latency:** <1 ms transmission enables HMD (<16 ms motion-to-photon)

6. **EVS Applications:** FLIR thermal imaging for low-visibility landing (FAR 91.175)

7. **F-35 EO-DAS:** 6× cameras, sensor fusion, 360° situational awareness via HMDS

8. **DO-178C/254 Certified:** DAL A/B software, DO-160G environmental testing

9. **Pixel Formats:** Mono8/10/12, RGB8/10, YUV422/444, Bayer (raw sensor)

10. **Point-to-Point or Switched:** Choose topology based on number of sources/sinks

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 818 — Avionics Digital Video Bus
- FC-AE-ASM (Fibre Channel - Avionics Environment - Avionics Streaming Management)
- SMPTE 274M (1080p HD Video Format)
- SMPTE 296M (720p HD Video Format)

**Avionics Systems:**
- F-35 HMDS (Helmet-Mounted Display System)
- Gulfstream G650 EVS (Enhanced Vision System)
- Elbit Systems SkyLens FLIR

**Fibre Channel:**
- ANSI X3.230 (Fibre Channel Physical Layer)
- FC-PI-5 (Fibre Channel Physical Interface)

**Certification:**
- RTCA DO-178C (Software Considerations)
- RTCA DO-254 (Hardware Considerations)
- RTCA DO-160G (Environmental Testing)
- FAR 91.175 (EVS Operations)

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Standards:** ARINC 818, FC-AE-ASM, DO-178C/254, DO-160G

================================================================================
