**cheatsheet for ALSA (Advanced Linux Sound Architecture)** in Linux — focused on the most useful parts for developers, embedded audio, userspace applications, and kernel-level work (valid for kernels 6.1–6.14 / early 2026).

### 1. ALSA Layers – Quick Overview

| Layer                     | What it is                                   | Main users / tools                           | Typical path / device nodes          |
|---------------------------|----------------------------------------------|----------------------------------------------|--------------------------------------|
| **Kernel driver**         | Hardware-specific ALSA driver                | Kernel modules (snd-hda-intel, snd-soc-…)    | /dev/snd/*                           |
| **ALSA kernel API**       | snd_pcm_*, snd_ctl_*, snd_timer_*            | Kernel modules, ASoC drivers                 | include/sound/*                      |
| **ALSA lib (libasound)**  | Userspace library (highest level)            | Most applications (aplay, speaker-test, PulseAudio) | libasound.so                         |
| **ALSA pcm plugin**       | Software processing chain (asym, dmix, dsnoop, rate, …) | .asoundrc / alsa.conf                        | ~/.asoundrc, /etc/alsa/conf.d        |
| **ALSA sequencer**        | MIDI routing & software synth                | MIDI apps, fluidsynth, qsynth                | /dev/snd/seq                         |
| **TinyALSA**              | Minimal C library (no plugins)               | Embedded / Android / low-overhead apps       | tinyalsa library                     |

### 2. Most Important Device Nodes

| Node                          | Meaning / Typical Use                              | Access mode          | Common commands/tools                  |
|-------------------------------|----------------------------------------------------|----------------------|----------------------------------------|
| /dev/snd/controlC0            | Mixer controls (volume, mute, input select)        | Read/write           | amixer, alsamixer, alsactl             |
| /dev/snd/pcmC0D0p             | Playback (C=card, D=device, p=playback)            | Read/write           | aplay, speaker-test                    |
| /dev/snd/pcmC0D0c             | Capture (recording)                                | Read/write           | arecord                                |
| /dev/snd/seq                  | ALSA sequencer (MIDI)                              | Read/write           | aseqdump, aplaymidi                    |
| /dev/snd/timer                | Timer device (used internally)                     | —                    | —                                      |

### 3. Key Command-Line Tools (ALSA Utils)

| Tool               | Purpose / Most Useful Commands                                                                 | Example (most common)                              |
|--------------------|------------------------------------------------------------------------------------------------|----------------------------------------------------|
| **alsamixer**      | Interactive mixer (F4=capture, F5=all, M=mute, arrow keys)                                     | `alsamixer -c 0`                                   |
| **amixer**         | Command-line mixer control                                                                     | `amixer sset Master 80%` <br> `amixer sset Capture nocap` |
| **aplay**          | Play WAV files                                                                                 | `aplay -D hw:0,0 test.wav`                         |
| **arecord**        | Record WAV files                                                                               | `arecord -D hw:0,0 -f cd -d 10 test.wav`           |
| **speaker-test**   | Generate test tones (very useful for debug)                                                    | `speaker-test -c 2 -t wav -D hw:0,0`               |
| **alsactl**        | Save/restore mixer settings                                                                    | `alsactl store` / `alsactl restore`                |
| **alsaloop**       | Create loopback between capture & playback                                                     | `alsaloop -C hw:0,0 -P hw:0,0`                     |
| **alsatplg**       | Compile topology files (for ASoC / topology driver)                                            | Used in kernel build                               |

### 4. Important ALSA Configuration (.asoundrc / alsa.conf)

```text
# ~/.asoundrc example – create a "default" alias with dmix + dsnoop

pcm.!default {
    type asym
    playback.pcm "dmix"
    capture.pcm "dsnoop"
}

pcm.dmix {
    type dmix
    ipc_key 12345
    slave {
        pcm "hw:0,0"
        rate 48000
        channels 2
        period_size 1024
        buffer_size 4096
    }
}

pcm.dsnoop {
    type dsnoop
    ipc_key 54321
    slave {
        pcm "hw:0,0"
        rate 48000
        channels 2
    }
}
```

**Common plugins**:
- `dmix` — software mixing (multiple apps → one hardware playback)
- `dsnoop` — software demux (one hardware capture → multiple apps)
- `asym` — combine playback + capture
- `rate` — sample rate conversion
- `plughw` — automatic format/rate conversion (hw without plugin)
- `null` — discard audio (debug)
- `file` — write to WAV file
- `loopback` — create virtual loopback device

### 5. ALSA API Quick Reference (libasound / C)

```c
// Open PCM device
snd_pcm_t *pcm;
snd_pcm_open(&pcm, "default", SND_PCM_STREAM_PLAYBACK, 0);

// Set hardware parameters
snd_pcm_hw_params_t *hwparams;
snd_pcm_hw_params_alloca(&hwparams);
snd_pcm_hw_params_any(pcm, hwparams);
snd_pcm_hw_params_set_access(pcm, hwparams, SND_PCM_ACCESS_MMAP_INTERLEAVED);
snd_pcm_hw_params_set_format(pcm, hwparams, SND_PCM_FORMAT_S16_LE);
snd_pcm_hw_params_set_rate_near(pcm, hwparams, &rate, 0);
snd_pcm_hw_params_set_channels(pcm, hwparams, 2);
snd_pcm_hw_params_set_periods_near(pcm, hwparams, &periods, 0);
snd_pcm_hw_params(pcm, hwparams);

// Write interleaved data
snd_pcm_writei(pcm, buffer, frames);

// Error recovery
snd_pcm_recover(pcm, err, 1);   // very important!
```

**Key return values**:
- `snd_pcm_writei()` / `snd_pcm_readi()` → positive = frames written/read, negative = error
- `-EPIPE` → underrun (playback) / overrun (capture)
- `-ESTRPIPE` → suspend (power management)
- `-EIO` → hardware error

### 6. Debugging & Diagnostic Commands

```bash
# List all cards & PCM devices
aplay -l
arecord -l
cat /proc/asound/cards

# Show current mixer settings
amixer contents
amixer -c 0 contents

# Check ALSA version & drivers
cat /proc/asound/version
lsmod | grep snd

# Real-time latency measurement
cyclictest -m -Sp90 -i200 -D -t -n -l1000000   # background while playing audio

# Force reload ALSA state
alsactl restore
alsactl init

# Dump hardware topology (ASoC systems)
aplay -v --dump-hw-params /dev/null
```

### 7. Embedded / Low-Level Tips (2026)

- **Use tinyalsa** on constrained systems — no plugin overhead, tiny footprint
- **Avoid dmix/dsnoop** on embedded — use direct hw:0,0 or ASoC multi-client
- **PDM microphones** — use hardware PDM-to-PCM (i.MX SAI, Qualcomm SLIMbus, etc.)
- **Low-latency** → period size 64–256 frames, buffer 2–4 periods, RT priority
- **Power saving** → disable unused codecs, use runtime PM, clock gating
- **ASoC topology** — use topology files + `snd-sof-topology` for Intel/AMD/Qualcomm DSPs
- **Bluetooth LE Audio** — LC3 codec latency ~10 ms → plan jitter buffer

### Quick Mnemonics

- **plughw** = hardware + automatic conversion (safe but adds latency)
- **hw** = direct hardware access (lowest latency, strict format)
- **dmix** = software mixing (multiple playback apps)
- **dsnoop** = software capture sharing (multiple recording apps)
- **asym** = combine playback + capture in one logical device

This cheatsheet covers 95% of what you need for ALSA development, debugging, and embedded audio bring-up.

Good luck with your Linux audio project!