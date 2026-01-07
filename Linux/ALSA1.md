**cheatsheet for ALSA kernel programming & porting** (Linux kernel 6.1–6.14 era, early 2026 perspective).  
Focuses on the most common tasks when porting or writing new ALSA drivers — especially for embedded/SoC platforms (ASoC = ALSA System on Chip).

### 1. ALSA Driver Types & When to Use Each

| Driver Type              | Typical Use Case                                   | Main Kernel Location                  | Key Structures / Files                     |
|--------------------------|----------------------------------------------------|---------------------------------------|--------------------------------------------|
| **Simple PCM (non-ASoC)**| Legacy PCI/USB sound cards, very simple I²S        | `sound/core/pcm*`                     | `snd_pcm_ops`, `snd_pcm_substream`         |
| **ASoC (most embedded)** | SoC + codec + platform glue (i.MX, Rockchip, Qualcomm, TI, NXP) | `sound/soc/`                          | `snd_soc_dai`, `snd_soc_dai_driver`, `snd_soc_codec`, `snd_soc_component` |
| **Topology (SoF/Intel/AMD)** | DSP firmware + topology (Intel SOF, AMD ACP, Qualcomm) | `sound/soc/sof/`, `sound/soc/codecs/` | topology files (.bin), `snd_soc_tplg_*`    |
| **USB Audio**            | USB sound cards, class-compliant devices           | `sound/usb/`                          | `snd_usb_audio`, `usb_audio` quirks        |
| **HD-Audio**             | Intel HDA (laptops, desktops)                      | `sound/pci/hda/`                      | `snd_hda_codec`, `hda_codec_driver`        |

**Rule of thumb 2026**:  
Almost all new embedded audio drivers → **ASoC** (Machine + Platform + Codec + DAI link)

### 2. ASoC Driver Structure – Most Common Pattern

```
Machine driver (board-specific glue)
  ↓
Platform driver (SoC I²S/SAI/PDM controller)
  ↓
Codec driver (external codec: WM8960, CS42L42, ES8316, ALC5682…)
  ↓
DAI links (connect CPU DAI ↔ codec DAI)
  ↓
Card registration (snd_soc_card)
```

### 3. Key ASoC Structures & Their Roles

| Structure                        | Location                              | Purpose / Most Important Fields                              |
|----------------------------------|---------------------------------------|--------------------------------------------------------------|
| `snd_soc_dai_driver`             | `include/sound/soc-dai.h`             | CPU / codec DAI capabilities: `.playback`, `.capture`, `.ops` |
| `snd_soc_dai`                    | `include/sound/soc-dai.h`             | Runtime instance of DAI (linked to substream)                |
| `snd_soc_component_driver`       | `include/sound/soc-component.h`       | Generic component (codec/platform)                           |
| `snd_soc_codec_driver`           | `include/sound/soc-codec.h`           | Codec-specific: controls, biases, DAPM routes                |
| `snd_soc_platform_driver`        | `include/sound/soc-dapm.h`            | SoC-specific: PCM ops, DAI link                              |
| `snd_soc_card`                   | `include/sound/soc.h`                 | Top-level card: `.dai_link`, `.components`, `.name`          |
| `snd_soc_dai_link`               | `include/sound/soc.h`                 | Connects CPU DAI ↔ codec DAI: `.name`, `.codecs`, `.cpus`    |
| `snd_soc_pcm_runtime`            | runtime                               | Runtime link between card + substream                        |

### 4. Minimal ASoC Machine Driver Example Skeleton

```c
/* board.c – machine driver */

#include <sound/soc.h>

static int board_hw_params(struct snd_pcm_substream *substream,
                           struct snd_pcm_hw_params *params) {
    /* optional: set clock, format constraints */
    return 0;
}

static const struct snd_soc_ops board_ops = {
    .hw_params = board_hw_params,
};

static struct snd_soc_dai_link board_dai_link[] = {
    {
        .name = "Primary",
        .stream_name = "Playback + Capture",
        .cpus = { .name = "sai1" },           /* CPU DAI name */
        .codecs = { .name = "cs42l42.0-004a" }, /* codec I²C addr */
        .platforms = { .name = "sai1" },
        .dai_fmt = SND_SOC_DAIFMT_I2S | SND_SOC_DAIFMT_NB_NF | SND_SOC_DAIFMT_CBS_CFS,
        .ops = &board_ops,
        .ignore_pmdown_time = 1,  /* common for low-power codecs */
    },
};

static struct snd_soc_card board_card = {
    .name = "MyBoardAudio",
    .dai_link = board_dai_link,
    .num_links = ARRAY_SIZE(board_dai_link),
};

static int board_probe(struct platform_device *pdev) {
    board_card.dev = &pdev->dev;
    return devm_snd_soc_register_card(&pdev->dev, &board_card);
}

static const struct of_device_id board_dt_ids[] = {
    { .compatible = "myvendor,myboard-audio" },
    { }
};
MODULE_DEVICE_TABLE(of, board_dt_ids);

static struct platform_driver board_driver = {
    .driver = {
        .name = "myboard-audio",
        .of_match_table = board_dt_ids,
    },
    .probe = board_probe,
};
module_platform_driver(board_driver);
```

### 5. Most Important ASoC / ALSA Kernel APIs

| API / Function                              | Purpose / When to call                                   | Common Flags / Params |
|---------------------------------------------|----------------------------------------------------------|-----------------------|
| `snd_soc_register_card()`                   | Register complete card (machine driver)                  | `devm_` variant preferred |
| `snd_soc_dai_driver` → `.ops`               | CPU DAI operations (set_sysclk, set_fmt, hw_params)      | `.trigger`, `.hw_params` |
| `snd_soc_add_dai_controls()`                | Add custom kcontrols to codec/DAI                        | `snd_kcontrol_new` array |
| `snd_soc_dapm_add_routes()`                 | Define DAPM audio path routing                           | Widget → widget connections |
| `snd_pcm_set_ops()`                         | Set PCM ops for non-ASoC simple drivers                  | `snd_pcm_ops` struct |
| `snd_pcm_set_managed_buffer()`              | Allocate DMA buffer (most drivers)                       | `SNDRV_DMA_TYPE_DEV` |
| `snd_pcm_lib_ioctl()`                       | Default PCM ioctl handler                                | Call in custom ioctl |
| `snd_soc_component_read/write()`            | Codec register access (I²C/SPI)                          | `regmap` preferred |

### 6. Porting / Bring-up Checklist

1. **Device Tree** – define codec node, CPU DAI (SAI/I²S), sound card node, dai-link
2. **Clock / MCLK** – provide correct parent clock, set rate (12.288 MHz / 11.2896 MHz typical)
3. **DAI format** – I²S / Left-justified / Right-justified, master/slave, BCLK ratio
4. **PDM mics** – use `snd_soc_dai_driver` with `.pdl` ops, configure decimation
5. **DPCM / DAPM** – define correct routes (AIF → DAC → Speaker, Mic → AIF)
6. **Power management** – implement `.pmdown_time`, `.set_bias_level`
7. **Topology (SoF/Intel/Qualcomm)** – generate .bin topology file + `snd-sof-topology`
8. **Test** – `speaker-test -c2 -r48000 -Dhw:0,0`, `arecord`, `alsamixer`

### 7. Debugging & Trace Commands

```bash
# Show registered cards & PCMs
cat /proc/asound/cards
aplay -l

# DAPM widget status (very useful!)
cat /sys/kernel/debug/asound/card0/codec#0/dapm_widget

# ASoC debug log
echo 1 > /sys/kernel/debug/asound/card0/pcm0p/sub0/status

# Enable dynamic debug for ASoC
echo "file soc-core.c +p" > /sys/kernel/debug/dynamic_debug/control
dmesg -w | grep soc

# ASoC topology debug
modprobe snd-sof-topology debug=1
```

### 8. Quick Rules of Thumb (Embedded Audio 2026)

- **ASoC is mandatory** for any SoC + codec combination
- **Use regmap** for codec register access (I²C/SPI)
- **DAPM routes** are critical — wrong route = no sound
- **Latency** — keep period size 64–256 frames, buffer 2–4 periods
- **PDM** — decimate in hardware or use optimized PDM library
- **LE Audio** — LC3 codec needs ~10 ms buffer + jitter management
- **Power** — codec bias off when idle, runtime PM on platform

Good luck with your ALSA porting or ASoC driver development!