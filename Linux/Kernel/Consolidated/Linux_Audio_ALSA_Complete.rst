================================================================================
Linux Audio & ALSA Subsystem - Comprehensive Reference
================================================================================

**Advanced Linux Sound Architecture (ALSA), ASoC, Audio Drivers**

**Last Updated:** January 2026

**Author:** Comprehensive consolidation from kernel sources

================================================================================

TL;DR - Quick Reference
================================================================================

**ALSA Architecture (2026)**

::

    User Space: Applications → libasound (ALSA lib) → /dev/snd/*
                               ↓
    Kernel:     ALSA Core → PCM/Control/Mixer → Hardware Driver
                           ↓
    Hardware:   I2S/SAI/PDM Controller → Codec → Speaker/Mic

**Key Device Nodes**

::

    /dev/snd/controlC0    - Mixer controls (volume, mute)
    /dev/snd/pcmC0D0p     - Playback (C=card, D=device, p=playback)
    /dev/snd/pcmC0D0c     - Capture (recording)
    /dev/snd/seq          - MIDI sequencer
    /dev/snd/timer        - Timer device

**Essential Command-Line Tools**

.. code-block:: bash

    # List audio devices
    aplay -l
    arecord -l
    cat /proc/asound/cards
    
    # Interactive mixer
    alsamixer
    
    # Set volume
    amixer sset Master 80%
    amixer sset Capture cap
    
    # Play test tone
    speaker-test -c 2 -t wav
    
    # Play WAV file
    aplay -D hw:0,0 test.wav
    
    # Record audio
    arecord -D hw:0,0 -f cd -d 10 output.wav
    
    # Save/restore mixer settings
    alsactl store
    alsactl restore

**ALSA Layers**

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Layer
     - Components
     - Purpose
   * - **User Space**
     - Applications, libasound, plugins
     - Audio playback/capture
   * - **ALSA Core**
     - PCM, Control, Mixer, Sequencer
     - Framework and routing
   * - **ASoC**
     - Machine, Platform, Codec drivers
     - SoC audio (embedded systems)
   * - **Hardware**
     - I2S/SAI/PDM, Codec chip, Amplifier
     - Physical audio hardware

**ASoC Driver Structure (Embedded/SoC)**

::

    Machine Driver (board-specific glue)
           ↓
    snd_soc_card → DAI links
           ↓
    CPU DAI (SoC I2S/SAI/PDM controller)
           ↔
    Codec DAI (external codec: WM8960, CS42L42, etc.)
           ↓
    Card Registration

**Common Audio Formats**

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Format
     - Description
     - Typical Use
   * - **S16_LE**
     - 16-bit signed little-endian
     - Standard PCM audio
   * - **S24_LE**
     - 24-bit signed
     - High-quality audio
   * - **S32_LE**
     - 32-bit signed
     - Professional audio
   * - **FLOAT_LE**
     - 32-bit float
     - Audio processing
   * - **MU_LAW**
     - µ-law compressed
     - Telephony
   * - **A_LAW**
     - A-law compressed
     - Telephony

**Sample Rates**

::

    8000 Hz    - Telephony
    16000 Hz   - Wideband telephony
    44100 Hz   - CD audio
    48000 Hz   - Professional audio (most common)
    96000 Hz   - High-resolution audio
    192000 Hz  - Ultra high-resolution

**Quick PCM API Example (User Space)**

.. code-block:: c

    #include <alsa/asoundlib.h>
    
    snd_pcm_t *pcm;
    snd_pcm_hw_params_t *params;
    
    // Open PCM device
    snd_pcm_open(&pcm, "default", SND_PCM_STREAM_PLAYBACK, 0);
    
    // Configure hardware parameters
    snd_pcm_hw_params_alloca(&params);
    snd_pcm_hw_params_any(pcm, params);
    snd_pcm_hw_params_set_access(pcm, params, SND_PCM_ACCESS_RW_INTERLEAVED);
    snd_pcm_hw_params_set_format(pcm, params, SND_PCM_FORMAT_S16_LE);
    snd_pcm_hw_params_set_channels(pcm, params, 2);
    snd_pcm_hw_params_set_rate(pcm, params, 48000, 0);
    snd_pcm_hw_params(pcm, params);
    
    // Write audio data
    snd_pcm_writei(pcm, buffer, frames);
    
    // Close
    snd_pcm_close(pcm);

**DAI Format Flags (ASoC)**

::

    SND_SOC_DAIFMT_I2S           - I2S format
    SND_SOC_DAIFMT_LEFT_J        - Left-justified
    SND_SOC_DAIFMT_RIGHT_J       - Right-justified
    SND_SOC_DAIFMT_DSP_A/B       - PCM/DSP modes
    
    SND_SOC_DAIFMT_NB_NF         - Normal bit clock, normal frame
    SND_SOC_DAIFMT_NB_IF         - Normal bit, inverted frame
    SND_SOC_DAIFMT_IB_NF         - Inverted bit, normal frame
    
    SND_SOC_DAIFMT_CBS_CFS       - Codec is slave (SoC is master)
    SND_SOC_DAIFMT_CBM_CFM       - Codec is master
    SND_SOC_DAIFMT_CBS_CFM       - Codec provides BCLK, SoC provides frame

**ALSA Configuration Plugins**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Plugin
     - Purpose
   * - **dmix**
     - Software mixing (multiple apps → one hardware playback)
   * - **dsnoop**
     - Software demux (one capture → multiple apps)
   * - **asym**
     - Combine playback + capture
   * - **plug**
     - Automatic format/rate conversion
   * - **rate**
     - Sample rate converter
   * - **loopback**
     - Virtual loopback device

**Key Kernel Structures**

.. code-block:: c

    struct snd_pcm              // PCM stream
    struct snd_pcm_substream    // Playback or capture substream
    struct snd_pcm_ops          // PCM operations
    struct snd_pcm_hw_params    // Hardware parameters
    
    // ASoC specific
    struct snd_soc_card         // Sound card
    struct snd_soc_dai          // Digital Audio Interface
    struct snd_soc_dai_driver   // DAI driver
    struct snd_soc_dai_link     // Connection between CPU and codec DAIs
    struct snd_soc_component    // Generic component (codec/platform)

================================================================================

1. ALSA Core Architecture
================================================================================

1.1 ALSA Subsystem Components
------------------------------

**ALSA consists of multiple subsystems:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │         User Space Applications         │
    │  (aplay, PulseAudio, JACK, PipeWire)   │
    └──────────────┬──────────────────────────┘
                   ↓
    ┌─────────────────────────────────────────┐
    │        libasound (ALSA library)         │
    │   Provides high-level PCM/Mixer API     │
    └──────────────┬──────────────────────────┘
                   ↓ (ioctl, mmap)
    ┌─────────────────────────────────────────┐
    │           /dev/snd/* devices            │
    │  pcmCxDxp, pcmCxDxc, controlCx, seq    │
    └──────────────┬──────────────────────────┘
                   ↓
    ┌─────────────────────────────────────────┐
    │           ALSA Core Kernel              │
    │  ├─ PCM (sound/core/pcm.c)             │
    │  ├─ Control (sound/core/control.c)     │
    │  ├─ Mixer (sound/core/mixer.c)         │
    │  ├─ Sequencer (sound/core/seq/)        │
    │  └─ Timer (sound/core/timer.c)         │
    └──────────────┬──────────────────────────┘
                   ↓
    ┌─────────────────────────────────────────┐
    │         Hardware Drivers Layer          │
    │  ├─ ASoC (SoC audio - sound/soc/)      │
    │  ├─ PCI (HDA - sound/pci/hda/)         │
    │  ├─ USB (sound/usb/)                   │
    │  └─ Firewire, Bluetooth, etc.          │
    └──────────────┬──────────────────────────┘
                   ↓
    ┌─────────────────────────────────────────┐
    │          Hardware (Codec, I2S)          │
    └─────────────────────────────────────────┘

1.2 PCM Subsystem
-----------------

**PCM (Pulse Code Modulation)** is the core audio data streaming interface.

**Key Concepts:**

- **Stream:** Playback or Capture
- **Substream:** Single audio stream instance
- **Period:** DMA transfer unit (e.g., 512 frames)
- **Buffer:** Ring buffer containing multiple periods (e.g., 4 periods)

**Buffer Layout:**

.. code-block:: text

    Ring Buffer (4096 frames total, 4 periods of 1024 frames each)
    
    ┌───────────┬───────────┬───────────┬───────────┐
    │ Period 0  │ Period 1  │ Period 2  │ Period 3  │
    │ 1024 frm  │ 1024 frm  │ 1024 frm  │ 1024 frm  │
    └───────────┴───────────┴───────────┴───────────┘
         ↑                                       ↑
      HW Pointer                            Appl Pointer
    
    - Application writes data
    - Hardware reads via DMA
    - Interrupt every period (for low latency)
    - Pointer wraps around (ring buffer)

**PCM States:**

.. code-block:: c

    SNDRV_PCM_STATE_OPEN       // Opened
    SNDRV_PCM_STATE_SETUP      // Parameters set
    SNDRV_PCM_STATE_PREPARED   // Ready to start
    SNDRV_PCM_STATE_RUNNING    // Streaming
    SNDRV_PCM_STATE_XRUN       // Underrun/overrun
    SNDRV_PCM_STATE_DRAINING   // Draining data
    SNDRV_PCM_STATE_PAUSED     // Paused
    SNDRV_PCM_STATE_SUSPENDED  // Suspended (PM)

1.3 Control and Mixer Interface
--------------------------------

**Controls** provide access to hardware settings (volume, mute, input selection).

**Control Types:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Type
     - Description
   * - **BOOLEAN**
     - On/Off switch (e.g., "Master Playback Switch")
   * - **INTEGER**
     - Numeric value (e.g., "Master Playback Volume" 0-100)
   * - **ENUMERATED**
     - Selection from list (e.g., "Input Source: Mic/Line/CD")
   * - **BYTES**
     - Raw byte array (e.g., EQ coefficients)
   * - **IEC958**
     - S/PDIF settings
   * - **INTEGER64**
     - 64-bit integer

**Example Control Access:**

.. code-block:: bash

    # List all controls
    amixer controls
    
    # Get control value
    amixer cget name='Master Playback Volume'
    
    # Set control value
    amixer cset name='Master Playback Volume' 80%
    
    # Set boolean
    amixer cset name='Master Playback Switch' on

================================================================================

2. ASoC (ALSA System on Chip) Framework
================================================================================

2.1 ASoC Architecture
---------------------

**ASoC** is designed for embedded SoC audio systems with separate CPU controller and codec.

**Three-Component Model:**

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │           Machine Driver (Board-Specific)        │
    │  - Connects CPU DAI to Codec DAI                │
    │  - Defines audio routes (DAPM)                  │
    │  - Sets clock configuration                     │
    │  - Creates snd_soc_card                         │
    └──────────────┬──────────────────┬───────────────┘
                   ↓                  ↓
         ┌─────────────────┐  ┌─────────────────┐
         │  Platform Driver │  │  Codec Driver   │
         │  (CPU DAI)       │  │  (Codec DAI)    │
         │                  │  │                 │
         │  - I2S/SAI/PDM   │  │  - WM8960       │
         │  - DMA setup     │  │  - CS42L42      │
         │  - Clock control │  │  - Register I/O │
         │  - PCM ops       │  │  - DAPM widgets │
         └─────────┬────────┘  └────────┬────────┘
                   ↓                    ↓
         ┌─────────────────────────────────────┐
         │          Hardware (I2S Bus)          │
         │   CPU I2S Controller ↔ Codec Chip   │
         └─────────────────────────────────────┘

2.2 ASoC Machine Driver
------------------------

**Purpose:** Board-specific glue that connects CPU DAI to Codec DAI.

**Minimal Machine Driver:**

.. code-block:: c

    #include <linux/module.h>
    #include <linux/of.h>
    #include <sound/soc.h>
    
    static int my_hw_params(struct snd_pcm_substream *substream,
                           struct snd_pcm_hw_params *params)
    {
        struct snd_soc_pcm_runtime *rtd = asoc_substream_to_rtd(substream);
        struct snd_soc_dai *codec_dai = asoc_rtd_to_codec(rtd, 0);
        struct snd_soc_dai *cpu_dai = asoc_rtd_to_cpu(rtd, 0);
        unsigned int mclk_freq;
        int ret;
        
        // Set codec system clock
        mclk_freq = 12288000;  // 12.288 MHz for 48kHz
        ret = snd_soc_dai_set_sysclk(codec_dai, 0, mclk_freq,
                                     SND_SOC_CLOCK_IN);
        if (ret)
            return ret;
        
        // Set CPU DAI clock dividers
        ret = snd_soc_dai_set_sysclk(cpu_dai, 0, mclk_freq,
                                     SND_SOC_CLOCK_OUT);
        if (ret)
            return ret;
        
        return 0;
    }
    
    static const struct snd_soc_ops my_ops = {
        .hw_params = my_hw_params,
    };
    
    SND_SOC_DAILINK_DEFS(primary,
        DAILINK_COMP_ARRAY(COMP_CPU("imx-sai.1")),
        DAILINK_COMP_ARRAY(COMP_CODEC("wm8960.0-001a", "wm8960-hifi")),
        DAILINK_COMP_ARRAY(COMP_PLATFORM("imx-sai.1")));
    
    static struct snd_soc_dai_link my_dai_link = {
        .name = "WM8960",
        .stream_name = "WM8960 HiFi",
        .dai_fmt = SND_SOC_DAIFMT_I2S |
                   SND_SOC_DAIFMT_NB_NF |
                   SND_SOC_DAIFMT_CBS_CFS,
        .ops = &my_ops,
        SND_SOC_DAILINK_REG(primary),
    };
    
    static struct snd_soc_card my_card = {
        .name = "My-Board-Audio",
        .owner = THIS_MODULE,
        .dai_link = &my_dai_link,
        .num_links = 1,
    };
    
    static int my_probe(struct platform_device *pdev)
    {
        struct device *dev = &pdev->dev;
        int ret;
        
        my_card.dev = dev;
        
        ret = devm_snd_soc_register_card(dev, &my_card);
        if (ret)
            dev_err(dev, "Failed to register card: %d\n", ret);
        
        return ret;
    }
    
    static const struct of_device_id my_dt_ids[] = {
        { .compatible = "vendor,my-audio", },
        { }
    };
    MODULE_DEVICE_TABLE(of, my_dt_ids);
    
    static struct platform_driver my_driver = {
        .driver = {
            .name = "my-audio",
            .of_match_table = my_dt_ids,
        },
        .probe = my_probe,
    };
    module_platform_driver(my_driver);
    
    MODULE_LICENSE("GPL");
    MODULE_DESCRIPTION("My Board ASoC Machine Driver");

2.3 ASoC Platform Driver (CPU DAI)
-----------------------------------

**Purpose:** Controls SoC audio controller (I2S/SAI/PDM).

**Platform Driver Example (I2S Controller):**

.. code-block:: c

    #include <sound/soc.h>
    #include <sound/pcm_params.h>
    #include <sound/dmaengine_pcm.h>
    
    #define I2S_TX_DATA     0x00
    #define I2S_RX_DATA     0x04
    #define I2S_CTRL        0x08
    #define I2S_CLOCK_CFG   0x0C
    
    struct my_i2s {
        void __iomem *base;
        struct clk *clk;
        struct snd_dmaengine_dai_dma_data dma_data_tx;
        struct snd_dmaengine_dai_dma_data dma_data_rx;
    };
    
    static int my_i2s_hw_params(struct snd_pcm_substream *substream,
                               struct snd_pcm_hw_params *params,
                               struct snd_soc_dai *dai)
    {
        struct my_i2s *i2s = snd_soc_dai_get_drvdata(dai);
        unsigned int channels = params_channels(params);
        unsigned int rate = params_rate(params);
        unsigned int width = params_width(params);
        u32 ctrl = 0;
        
        // Configure bit width
        switch (width) {
        case 16:
            ctrl |= (16 << CTRL_WIDTH_SHIFT);
            break;
        case 24:
            ctrl |= (24 << CTRL_WIDTH_SHIFT);
            break;
        default:
            return -EINVAL;
        }
        
        // Configure channels
        ctrl |= ((channels - 1) << CTRL_CHANNELS_SHIFT);
        
        writel(ctrl, i2s->base + I2S_CTRL);
        
        // Set clock divider for sample rate
        clk_set_rate(i2s->clk, rate * channels * width * 2);
        
        return 0;
    }
    
    static int my_i2s_set_fmt(struct snd_soc_dai *dai, unsigned int fmt)
    {
        struct my_i2s *i2s = snd_soc_dai_get_drvdata(dai);
        u32 ctrl = readl(i2s->base + I2S_CTRL);
        
        // Clock provider/consumer
        switch (fmt & SND_SOC_DAIFMT_CLOCK_PROVIDER_MASK) {
        case SND_SOC_DAIFMT_BP_FP:  // Codec is provider (master)
            ctrl &= ~CTRL_MASTER;
            break;
        case SND_SOC_DAIFMT_BC_FC:  // Codec is consumer (slave)
            ctrl |= CTRL_MASTER;
            break;
        default:
            return -EINVAL;
        }
        
        // Format
        switch (fmt & SND_SOC_DAIFMT_FORMAT_MASK) {
        case SND_SOC_DAIFMT_I2S:
            ctrl |= CTRL_FMT_I2S;
            break;
        case SND_SOC_DAIFMT_LEFT_J:
            ctrl |= CTRL_FMT_LEFT_J;
            break;
        default:
            return -EINVAL;
        }
        
        writel(ctrl, i2s->base + I2S_CTRL);
        return 0;
    }
    
    static int my_i2s_trigger(struct snd_pcm_substream *substream,
                             int cmd, struct snd_soc_dai *dai)
    {
        struct my_i2s *i2s = snd_soc_dai_get_drvdata(dai);
        u32 ctrl = readl(i2s->base + I2S_CTRL);
        
        switch (cmd) {
        case SNDRV_PCM_TRIGGER_START:
        case SNDRV_PCM_TRIGGER_RESUME:
        case SNDRV_PCM_TRIGGER_PAUSE_RELEASE:
            ctrl |= CTRL_ENABLE;
            break;
        case SNDRV_PCM_TRIGGER_STOP:
        case SNDRV_PCM_TRIGGER_SUSPEND:
        case SNDRV_PCM_TRIGGER_PAUSE_PUSH:
            ctrl &= ~CTRL_ENABLE;
            break;
        default:
            return -EINVAL;
        }
        
        writel(ctrl, i2s->base + I2S_CTRL);
        return 0;
    }
    
    static const struct snd_soc_dai_ops my_i2s_dai_ops = {
        .hw_params = my_i2s_hw_params,
        .set_fmt = my_i2s_set_fmt,
        .trigger = my_i2s_trigger,
    };
    
    static struct snd_soc_dai_driver my_i2s_dai = {
        .name = "my-i2s",
        .playback = {
            .channels_min = 2,
            .channels_max = 2,
            .rates = SNDRV_PCM_RATE_8000_192000,
            .formats = SNDRV_PCM_FMTBIT_S16_LE |
                      SNDRV_PCM_FMTBIT_S24_LE,
        },
        .capture = {
            .channels_min = 2,
            .channels_max = 2,
            .rates = SNDRV_PCM_RATE_8000_192000,
            .formats = SNDRV_PCM_FMTBIT_S16_LE |
                      SNDRV_PCM_FMTBIT_S24_LE,
        },
        .ops = &my_i2s_dai_ops,
    };
    
    static int my_i2s_probe(struct platform_device *pdev)
    {
        struct my_i2s *i2s;
        struct resource *res;
        int ret;
        
        i2s = devm_kzalloc(&pdev->dev, sizeof(*i2s), GFP_KERNEL);
        if (!i2s)
            return -ENOMEM;
        
        i2s->base = devm_platform_ioremap_resource(pdev, 0);
        if (IS_ERR(i2s->base))
            return PTR_ERR(i2s->base);
        
        i2s->clk = devm_clk_get(&pdev->dev, "i2s");
        if (IS_ERR(i2s->clk))
            return PTR_ERR(i2s->clk);
        
        clk_prepare_enable(i2s->clk);
        
        // Setup DMA data
        res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
        i2s->dma_data_tx.addr = res->start + I2S_TX_DATA;
        i2s->dma_data_tx.maxburst = 4;
        i2s->dma_data_rx.addr = res->start + I2S_RX_DATA;
        i2s->dma_data_rx.maxburst = 4;
        
        dev_set_drvdata(&pdev->dev, i2s);
        
        // Register DAI
        ret = devm_snd_soc_register_component(&pdev->dev,
                                              &snd_soc_component_driver_empty,
                                              &my_i2s_dai, 1);
        if (ret)
            return ret;
        
        // Register DMA engine PCM
        return devm_snd_dmaengine_pcm_register(&pdev->dev, NULL, 0);
    }
    
    static const struct of_device_id my_i2s_dt_ids[] = {
        { .compatible = "vendor,my-i2s", },
        { }
    };
    MODULE_DEVICE_TABLE(of, my_i2s_dt_ids);
    
    static struct platform_driver my_i2s_driver = {
        .driver = {
            .name = "my-i2s",
            .of_match_table = my_i2s_dt_ids,
        },
        .probe = my_i2s_probe,
    };
    module_platform_driver(my_i2s_driver);

================================================================================

3. Device Tree Configuration
================================================================================

**Complete Audio System DT Example:**

.. code-block:: dts

    / {
        sound {
            compatible = "vendor,my-audio";
            model = "My Board Audio";
            audio-cpu = <&sai1>;
            audio-codec = <&wm8960>;
        };
    };
    
    &i2c1 {
        wm8960: codec@1a {
            compatible = "wlf,wm8960";
            reg = <0x1a>;
            clocks = <&clk_codec_mclk>;
            clock-names = "mclk";
            wlf,shared-lrclk;
            #sound-dai-cells = <0>;
        };
    };
    
    &sai1 {
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_sai1>;
        assigned-clocks = <&clk_sai1>;
        assigned-clock-rates = <12288000>;
        fsl,sai-mclk-direction-output;
        status = "okay";
    };

================================================================================

4. Debugging and Monitoring
================================================================================

4.1 Essential Commands
-----------------------

.. code-block:: bash

    # List all sound cards
    cat /proc/asound/cards
    aplay -l
    
    # List PCM devices
    aplay -L
    
    # Show detailed card info
    cat /proc/asound/card0/pcm0p/info
    cat /proc/asound/card0/pcm0p/sub0/status
    
    # Test playback
    speaker-test -D hw:0,0 -c 2 -t wav
    
    # Test capture
    arecord -D hw:0,0 -f S16_LE -r 48000 -c 2 -d 5 test.wav
    
    # Check mixer controls
    amixer contents
    alsamixer
    
    # DAPM widget status (ASoC)
    cat /sys/kernel/debug/asound/card0/dapm_widget
    
    # Codec register dump
    cat /sys/kernel/debug/asound/card0/codec_reg
    
    # Enable ALSA debug
    echo 8 > /proc/sys/kernel/printk
    
    # Check DMA activity
    cat /proc/interrupts | grep dma
    
    # Monitor buffer status
    cat /sys/kernel/debug/asound/card0/pcm0p/sub0/hw_params

4.2 Common Issues
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Issue
     - Symptoms
     - Solution
   * - **No sound**
     - Playback works, no audio
     - Check mixer (amixer), unmute controls
   * - **Underrun (XRUN)**
     - Crackling, gaps in audio
     - Increase buffer/period size, RT priority
   * - **Format not supported**
     - aplay fails with error
     - Check supported formats (aplay -L)
   * - **Clock mismatch**
     - Wrong pitch, distortion
     - Verify MCLK frequency, check dividers
   * - **No capture**
     - arecord fails
     - Enable capture controls, check routing

================================================================================

5. Exam Question: Complete ASoC Driver
================================================================================

**Question (14 points):**

Implement a complete ASoC machine driver for a board with:
- i.MX8 SAI controller (CPU DAI)
- CS42L42 codec connected via I2C at address 0x48
- MCLK = 12.288 MHz from SoC
- I2S format, codec is slave (SoC is master)

**Part A (6 points):** Implement the machine driver with correct DAI link configuration.

**Part B (4 points):** Implement the hw_params callback to set system clocks correctly.

**Part C (4 points):** Create the device tree binding for this audio system.

**Answer:**

**Part A: Machine Driver**

.. code-block:: c

    #include <linux/module.h>
    #include <linux/of.h>
    #include <sound/soc.h>
    
    static int imx_cs42l42_hw_params(struct snd_pcm_substream *substream,
                                    struct snd_pcm_hw_params *params)
    {
        struct snd_soc_pcm_runtime *rtd = asoc_substream_to_rtd(substream);
        struct snd_soc_dai *codec_dai = asoc_rtd_to_codec(rtd, 0);
        struct snd_soc_dai *cpu_dai = asoc_rtd_to_cpu(rtd, 0);
        unsigned int sample_rate = params_rate(params);
        unsigned int mclk_freq;
        int ret;
        
        // Calculate MCLK frequency (256fs for most rates)
        if (sample_rate == 44100 || sample_rate == 88200)
            mclk_freq = 11289600;  // 44.1kHz * 256
        else
            mclk_freq = 12288000;  // 48kHz * 256
        
        // Set codec system clock (MCLK input)
        ret = snd_soc_dai_set_sysclk(codec_dai, 0, mclk_freq,
                                     SND_SOC_CLOCK_IN);
        if (ret) {
            pr_err("Failed to set codec MCLK: %d\n", ret);
            return ret;
        }
        
        // Set CPU DAI system clock (MCLK output)
        ret = snd_soc_dai_set_sysclk(cpu_dai, 0, mclk_freq,
                                     SND_SOC_CLOCK_OUT);
        if (ret) {
            pr_err("Failed to set CPU MCLK: %d\n", ret);
            return ret;
        }
        
        return 0;
    }
    
    static const struct snd_soc_ops imx_cs42l42_ops = {
        .hw_params = imx_cs42l42_hw_params,
    };
    
    SND_SOC_DAILINK_DEFS(hifi,
        DAILINK_COMP_ARRAY(COMP_CPU("30c20000.sai")),
        DAILINK_COMP_ARRAY(COMP_CODEC("cs42l42.1-0048", "cs42l42")),
        DAILINK_COMP_ARRAY(COMP_PLATFORM("30c20000.sai")));
    
    static struct snd_soc_dai_link imx_cs42l42_dai = {
        .name = "CS42L42",
        .stream_name = "CS42L42 HiFi",
        .dai_fmt = SND_SOC_DAIFMT_I2S |
                   SND_SOC_DAIFMT_NB_NF |
                   SND_SOC_DAIFMT_CBS_CFS,  // Codec is slave
        .ops = &imx_cs42l42_ops,
        SND_SOC_DAILINK_REG(hifi),
    };
    
    static struct snd_soc_card imx_cs42l42_card = {
        .name = "imx-cs42l42",
        .owner = THIS_MODULE,
        .dai_link = &imx_cs42l42_dai,
        .num_links = 1,
    };
    
    static int imx_cs42l42_probe(struct platform_device *pdev)
    {
        struct device *dev = &pdev->dev;
        int ret;
        
        imx_cs42l42_card.dev = dev;
        
        ret = devm_snd_soc_register_card(dev, &imx_cs42l42_card);
        if (ret)
            dev_err(dev, "Failed to register card: %d\n", ret);
        
        return ret;
    }
    
    static const struct of_device_id imx_cs42l42_dt_ids[] = {
        { .compatible = "fsl,imx-audio-cs42l42", },
        { }
    };
    MODULE_DEVICE_TABLE(of, imx_cs42l42_dt_ids);
    
    static struct platform_driver imx_cs42l42_driver = {
        .driver = {
            .name = "imx-cs42l42",
            .pm = &snd_soc_pm_ops,
            .of_match_table = imx_cs42l42_dt_ids,
        },
        .probe = imx_cs42l42_probe,
    };
    module_platform_driver(imx_cs42l42_driver);
    
    MODULE_AUTHOR("Your Name");
    MODULE_DESCRIPTION("i.MX CS42L42 ASoC Machine Driver");
    MODULE_LICENSE("GPL");

**Part B: Explanation of hw_params**

The hw_params callback is called when audio parameters are set. It must:

1. **Calculate MCLK frequency** based on sample rate:
   - 48kHz family (48k, 96k, 192k) → 12.288 MHz (48000 × 256)
   - 44.1kHz family (44.1k, 88.2k) → 11.2896 MHz (44100 × 256)

2. **Set codec system clock:**
   - ``snd_soc_dai_set_sysclk(codec_dai, ...)``
   - Direction: SND_SOC_CLOCK_IN (MCLK is input to codec)
   - Codec uses MCLK to generate bit clock and frame clock

3. **Set CPU DAI system clock:**
   - ``snd_soc_dai_set_sysclk(cpu_dai, ...)``
   - Direction: SND_SOC_CLOCK_OUT (SAI outputs MCLK)
   - SAI controller configures PLL/dividers

**Part C: Device Tree Binding**

.. code-block:: dts

    / {
        sound-cs42l42 {
            compatible = "fsl,imx-audio-cs42l42";
            model = "imx-cs42l42";
            audio-cpu = <&sai3>;
            audio-codec = <&cs42l42>;
        };
    };
    
    &i2c1 {
        clock-frequency = <100000>;
        
        cs42l42: codec@48 {
            compatible = "cirrus,cs42l42";
            reg = <0x48>;
            clocks = <&clk IMX8MM_CLK_SAI3_ROOT>;
            clock-names = "mclk";
            VA-supply = <&reg_3v3_audio>;
            VP-supply = <&reg_3v3_audio>;
            VCP-supply = <&reg_3v3_audio>;
            VD_FILT-supply = <&reg_3v3_audio>;
            VL-supply = <&reg_1v8_audio>;
            reset-gpios = <&gpio5 10 GPIO_ACTIVE_LOW>;
            interrupt-parent = <&gpio5>;
            interrupts = <11 IRQ_TYPE_LEVEL_LOW>;
            #sound-dai-cells = <0>;
        };
    };
    
    &sai3 {
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_sai3>;
        assigned-clocks = <&clk IMX8MM_CLK_SAI3>;
        assigned-clock-parents = <&clk IMX8MM_AUDIO_PLL1_OUT>;
        assigned-clock-rates = <12288000>;
        fsl,sai-mclk-direction-output;
        status = "okay";
    };
    
    &iomuxc {
        pinctrl_sai3: sai3grp {
            fsl,pins = <
                MX8MM_IOMUXC_SAI3_TXFS_SAI3_TX_SYNC     0xd6
                MX8MM_IOMUXC_SAI3_TXC_SAI3_TX_BCLK      0xd6
                MX8MM_IOMUXC_SAI3_TXD_SAI3_TX_DATA0     0xd6
                MX8MM_IOMUXC_SAI3_RXD_SAI3_RX_DATA0     0xd6
                MX8MM_IOMUXC_SAI3_MCLK_SAI3_MCLK        0xd6
            >;
        };
    };

**Key DT Components:**

1. **sound-cs42l42 node:** Machine driver binding, references SAI and codec
2. **cs42l42 node:** Codec I2C device at 0x48, power supplies, reset GPIO, interrupt
3. **sai3 node:** SAI controller, MCLK output enabled, clock tree configuration
4. **pinctrl:** Pin muxing for SAI signals (BCLK, LRCLK, DATA, MCLK)

================================================================================

6. Key Takeaways
================================================================================

**ALSA Best Practices (2026):**

1. **Use ASoC for All SoC Audio**
   - Machine + Platform + Codec separation
   - Reusable components
   - DAPM for power management

2. **DMA Engine PCM**
   - Use dmaengine_pcm_register for DMA
   - Automatic buffer management
   - Lower CPU overhead

3. **Device Tree Driven**
   - All hardware configuration in DT
   - Compatible strings for driver matching
   - Clock tree properly configured

4. **Error Recovery**
   - Handle underrun/overrun gracefully
   - Use snd_pcm_recover() in user space
   - Monitor buffer levels

5. **Low Latency**
   - Small period size (64-256 frames)
   - 2-4 periods per buffer
   - RT thread priority
   - DMA instead of interrupts per frame

6. **Power Management**
   - Implement runtime PM
   - Use DAPM for codec power
   - Clock gating when idle

**Common Pitfalls:**

::

    ✗ Wrong MCLK frequency (check sample rate × 256)
    ✗ Incorrect DAI format flags (check I2S vs DSP mode)
    ✗ Master/slave mismatch (CBS_CFS = codec slave)
    ✗ Missing clock tree setup in DT
    ✗ Unmuted mixers after probe
    ✗ Buffer size too small (causes underruns)
    ✗ DMA not enabled in controller

**Quick Command Reference:**

.. code-block:: bash

    # List devices
    aplay -l
    cat /proc/asound/cards
    
    # Test playback
    speaker-test -D hw:0,0 -c 2
    
    # Control mixer
    alsamixer
    amixer sset Master 80%
    
    # Debug
    cat /sys/kernel/debug/asound/card0/dapm_widget
    cat /proc/asound/card0/pcm0p/sub0/hw_params
    
    # Save/restore
    alsactl store
    alsactl restore

**Sample Rates & MCLK:**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Sample Rate
     - MCLK (256fs)
     - Typical Use
   * - 8 kHz
     - 2.048 MHz
     - Telephony
   * - 16 kHz
     - 4.096 MHz
     - Voice
   * - 44.1 kHz
     - 11.2896 MHz
     - CD audio
   * - 48 kHz
     - 12.288 MHz
     - Professional audio
   * - 96 kHz
     - 24.576 MHz
     - Hi-res audio

================================================================================

**Last Updated:** January 2026  
**Kernel Version:** 6.8+  
**Status:** Production Ready

================================================================================

