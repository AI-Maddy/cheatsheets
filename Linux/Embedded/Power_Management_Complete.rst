=====================================
Embedded Linux Power Management - Complete Guide
=====================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Reference: Thermal Imaging Camera (DaVinci DM365), Smart Home Hub (i.MX 93), E-Bike Infotainment

.. contents:: Table of Contents
   :depth: 4
   :local:

====================
1. Overview
====================

Comprehensive power management for battery-powered and low-power embedded Linux systems, 
covering CPU power states, peripheral power control, and system-wide power optimization.

**Project Context**:

- **Thermal Imaging Camera** (DaVinci DM365): Target <8mW standby, <2s resume
- **Smart Home Hub** (i.MX 93): Battery backup mode, <50mW idle
- **E-Bike Infotainment**: Automotive power modes, ignition-aware power management
- **AFIRS SDU**: Aircraft power constraints, low-power during ground operations

**Power Consumption Targets**:

.. code-block:: text

    System State      DaVinci    i.MX 93    E-Bike     Atom
    ─────────────────────────────────────────────────────────
    Active            850mW      2.1W       3.5W       15W
    Idle              180mW      420mW      680mW      8W
    Suspend (S3)      45mW       85mW       150mW      2W
    Deep Sleep        7.5mW      18mW       35mW       N/A
    Hibernation       <1mW       <2mW       <5mW       <1W

====================
2. Linux Power Management Framework
====================

2.1 Power Management States
----------------------------

**System Sleep States** (ACPI):

.. code-block:: text

    S0 (Working): Full operation
    S1 (Standby): CPU stopped, RAM powered
    S2 (Standby): CPU powered off, dirty cache flushed
    S3 (Suspend-to-RAM): RAM in self-refresh, context saved
    S4 (Hibernate): Suspend-to-disk, system powered off
    S5 (Soft Off): Shutdown, power supply on

**CPU States** (C-states):

.. code-block:: text

    C0: Active execution
    C1: Halt (clock gating)
    C2: Stop-Grant (PLL running)
    C3: Deep Sleep (PLL stopped)
    C4+: Deeper sleep states (SoC-specific)

**Device States** (D-states):

.. code-block:: text

    D0: Fully operational
    D1: Light sleep
    D2: Deeper sleep
    D3hot: Device powered but not operational
    D3cold: Device power removed

2.2 Kernel Power Management APIs
---------------------------------

2.2.1 Runtime PM
~~~~~~~~~~~~~~~~

**Driver Implementation**:

.. code-block:: c

    #include <linux/pm_runtime.h>
    
    static int my_device_probe(struct platform_device *pdev)
    {
        struct device *dev = &pdev->dev;
        
        /* Enable runtime PM */
        pm_runtime_enable(dev);
        
        /* Set autosuspend delay (2 seconds) */
        pm_runtime_set_autosuspend_delay(dev, 2000);
        pm_runtime_use_autosuspend(dev);
        
        /* Mark as active initially */
        pm_runtime_get_sync(dev);
        
        /* ... device initialization ... */
        
        /* Release and allow suspend */
        pm_runtime_put_autosuspend(dev);
        
        return 0;
    }
    
    static int my_device_remove(struct platform_device *pdev)
    {
        struct device *dev = &pdev->dev;
        
        pm_runtime_disable(dev);
        
        return 0;
    }
    
    /* Runtime PM callbacks */
    static int my_device_runtime_suspend(struct device *dev)
    {
        struct my_device *priv = dev_get_drvdata(dev);
        
        dev_dbg(dev, "Runtime suspend\n");
        
        /* Disable clocks */
        clk_disable_unprepare(priv->clk);
        
        /* Power off regulators */
        regulator_disable(priv->regulator);
        
        return 0;
    }
    
    static int my_device_runtime_resume(struct device *dev)
    {
        struct my_device *priv = dev_get_drvdata(dev);
        int ret;
        
        dev_dbg(dev, "Runtime resume\n");
        
        /* Power on regulators */
        ret = regulator_enable(priv->regulator);
        if (ret)
            return ret;
        
        /* Enable clocks */
        ret = clk_prepare_enable(priv->clk);
        if (ret) {
            regulator_disable(priv->regulator);
            return ret;
        }
        
        /* Restore device state */
        my_device_restore_state(priv);
        
        return 0;
    }
    
    static const struct dev_pm_ops my_device_pm_ops = {
        SET_RUNTIME_PM_OPS(my_device_runtime_suspend,
                          my_device_runtime_resume,
                          NULL)
        SET_SYSTEM_SLEEP_PM_OPS(my_device_suspend, my_device_resume)
    };

**Usage in Driver**:

.. code-block:: c

    static ssize_t my_device_read(struct file *file, char __user *buf,
                                   size_t count, loff_t *ppos)
    {
        struct my_device *priv = file->private_data;
        struct device *dev = priv->dev;
        int ret;
        
        /* Ensure device is powered */
        ret = pm_runtime_get_sync(dev);
        if (ret < 0) {
            pm_runtime_put_noidle(dev);
            return ret;
        }
        
        /* ... perform read operation ... */
        
        /* Release device, allow suspend */
        pm_runtime_mark_last_busy(dev);
        pm_runtime_put_autosuspend(dev);
        
        return count;
    }

2.2.2 System Sleep PM
~~~~~~~~~~~~~~~~~~~~~

**Suspend/Resume Callbacks**:

.. code-block:: c

    static int my_device_suspend(struct device *dev)
    {
        struct my_device *priv = dev_get_drvdata(dev);
        
        dev_info(dev, "Entering suspend\n");
        
        /* Stop active operations */
        cancel_delayed_work_sync(&priv->work);
        
        /* Save device state */
        my_device_save_state(priv);
        
        /* Power down hardware */
        my_device_power_off(priv);
        
        return 0;
    }
    
    static int my_device_resume(struct device *dev)
    {
        struct my_device *priv = dev_get_drvdata(dev);
        
        dev_info(dev, "Resuming from suspend\n");
        
        /* Power on hardware */
        my_device_power_on(priv);
        
        /* Restore device state */
        my_device_restore_state(priv);
        
        /* Resume operations */
        schedule_delayed_work(&priv->work, msecs_to_jiffies(100));
        
        return 0;
    }

2.3 PM QoS (Quality of Service)
--------------------------------

**Request PM Constraints**:

.. code-block:: c

    #include <linux/pm_qos.h>
    
    /* Constrain CPU latency (µs) */
    struct pm_qos_request cpu_latency_req;
    
    void request_low_latency(void)
    {
        /* Request max 100µs wakeup latency */
        pm_qos_add_request(&cpu_latency_req, PM_QOS_CPU_LATENCY, 100);
    }
    
    void release_low_latency(void)
    {
        pm_qos_remove_request(&cpu_latency_req);
    }

====================
3. TI DaVinci Power Management
====================

3.1 DM365 Power Domains
------------------------

**Power Domains**:

.. code-block:: text

    - ALWON: Always-on (RTC, GPIO wakeup)
    - DSP: Video/Image coprocessor
    - VENC: Video encoder
    - VPSS: Video processing subsystem
    - USB: USB OTG controller
    - EMAC: Ethernet controller

**Clock Domains**:

.. code-block:: c

    /* drivers/clk/davinci/dm365-clk.c */
    
    static struct clk_lookup dm365_clks[] = {
        CLK(NULL, "ref", &ref_clk),
        CLK(NULL, "pll1", &pll1_clk),
        CLK(NULL, "pll2", &pll2_clk),
        CLK(NULL, "cpu", &cpu_clk),
        CLK(NULL, "arm", &arm_clk),
        CLK("vpss", "master", &vpss_master_clk),
        CLK("vpss", "slave", &vpss_slave_clk),
        CLK("davinci_emac", NULL, &emac_clk),
        CLK("i2c_davinci.1", NULL, &i2c_clk),
        CLK("dm365-mmc.0", NULL, &mmcsd0_clk),
        CLK("spi_davinci.0", NULL, &spi0_clk),
        // ...
    };

3.2 Hibernation Implementation (DaVinci)
-----------------------------------------

**Hibernation Flow**:

.. code-block:: text

    1. Save system state to NAND flash
    2. Configure wakeup sources (RTC, GPIO)
    3. Power off DSP, VPSS, peripherals
    4. Enter deep sleep (ARM in WFI, DDR self-refresh)
    5. Wakeup event → boot from NAND
    6. Restore system state

**Save/Restore State** (``arch/arm/mach-davinci/pm.c``):

.. code-block:: c

    struct davinci_pm_state {
        u32 pinmux[20];
        u32 ddr_sr;
        u32 psc_states[PSC_MAX_DOMAINS];
        u32 vtpio_ctrl;
        u32 plls[2];
    };
    
    static struct davinci_pm_state pm_state;
    
    static int davinci_pm_enter_sleep(suspend_state_t state)
    {
        int ret;
        
        /* Save system state */
        davinci_save_pinmux(pm_state.pinmux);
        davinci_save_psc_state(pm_state.psc_states);
        
        /* Disable unnecessary clocks */
        davinci_disable_clocks();
        
        /* Put DDR into self-refresh */
        davinci_ddr_self_refresh_enter();
        
        /* Enter WFI (Wait For Interrupt) */
        cpu_do_idle();
        
        /* Wakeup - restore state */
        davinci_ddr_self_refresh_exit();
        davinci_enable_clocks();
        davinci_restore_psc_state(pm_state.psc_states);
        davinci_restore_pinmux(pm_state.pinmux);
        
        return 0;
    }

**RTC Wakeup Configuration**:

.. code-block:: c

    #include <linux/rtc.h>
    
    static int setup_rtc_wakeup(unsigned int seconds)
    {
        struct rtc_device *rtc;
        struct rtc_wkalrm alarm;
        struct rtc_time tm;
        unsigned long now, alarm_time;
        
        rtc = rtc_class_open("rtc0");
        if (!rtc)
            return -ENODEV;
        
        /* Get current time */
        rtc_read_time(rtc, &tm);
        rtc_tm_to_time(&tm, &now);
        
        /* Set alarm */
        alarm_time = now + seconds;
        rtc_time_to_tm(alarm_time, &alarm.time);
        alarm.enabled = 1;
        
        rtc_set_alarm(rtc, &alarm);
        rtc_class_close(rtc);
        
        return 0;
    }

**Hibernate Trigger** (userspace):

.. code-block:: bash

    #!/bin/bash
    # hibernate_davinci.sh
    
    # Sync filesystems
    sync
    
    # Set RTC wakeup (60 seconds)
    echo "+60" > /sys/class/rtc/rtc0/wakealarm
    
    # Stop non-essential services
    systemctl stop networking
    systemctl stop bluetooth
    
    # Enter hibernation
    echo mem > /sys/power/state

**Project Measurements** (Thermal Imaging Camera):

.. code-block:: text

    State            Current    Time
    ───────────────────────────────────
    Active capture   285mA      Continuous
    Idle             60mA       Between captures
    Deep sleep       2.5mA      Waiting for trigger
    Hibernation      <0.3mA     Extended standby
    
    Battery Life (3000mAh):
    - Continuous: ~10.5 hours
    - 1 capture/min with deep sleep: ~48 hours
    - 1 capture/hour with hibernation: ~15 days
    
    Resume Time from Hibernation:
    - Boot ROM → U-Boot: 850ms
    - U-Boot → Kernel: 720ms
    - Kernel → App ready: 380ms
    - Total: 1.95 seconds

3.3 DSP Power Management
-------------------------

**DSP Sleep Control**:

.. code-block:: c

    /* Power on DSP */
    static int davinci_dsp_power_on(struct davinci_dsp *dsp)
    {
        /* Enable PSC module */
        davinci_psc_config(DAVINCI_LPSC_GEM, 1, PSC_ENABLE);
        
        /* Enable DSP clocks */
        clk_prepare_enable(dsp->dsp_clk);
        
        /* Take DSP out of reset */
        writel(0, dsp->base + DSP_RESET);
        
        return 0;
    }
    
    /* Power off DSP */
    static int davinci_dsp_power_off(struct davinci_dsp *dsp)
    {
        /* Put DSP in reset */
        writel(1, dsp->base + DSP_RESET);
        
        /* Disable clocks */
        clk_disable_unprepare(dsp->dsp_clk);
        
        /* Disable PSC module */
        davinci_psc_config(DAVINCI_LPSC_GEM, 1, PSC_SWRSTDISABLE);
        
        return 0;
    }

**Video Codec Power Management**:

.. code-block:: c

    /* Enable codec only when needed */
    int video_codec_start(struct video_codec *codec)
    {
        pm_runtime_get_sync(codec->dev);
        
        /* DSP powers on via runtime PM */
        codec->active = true;
        
        return 0;
    }
    
    void video_codec_stop(struct video_codec *codec)
    {
        codec->active = false;
        
        /* Auto-suspend after 2 seconds */
        pm_runtime_mark_last_busy(codec->dev);
        pm_runtime_put_autosuspend(codec->dev);
    }

====================
4. NXP i.MX Power Management
====================

4.1 i.MX 93 Power Architecture
-------------------------------

**Power Domains**:

.. code-block:: text

    Cortex-A55 (2 cores):
    - RUN: Full speed (1.7 GHz)
    - WAIT: Clock gated, cache retained
    - STOP: Power gated, context lost
    
    Cortex-M33:
    - Active: 250 MHz
    - Sleep: WFI, clock gated
    - Deep Sleep: Power gated
    
    System Power Modes:
    - RUN: All domains active
    - WAIT: CPU clock gated
    - STOP: CPU powered off, DDR self-refresh
    - SUSPEND: System powered off except SNVS (RTC, GPIO)

**GPC (General Power Controller)**:

.. code-block:: c

    /* arch/arm64/boot/dts/freescale/imx93.dtsi */
    
    gpc: gpc@44470000 {
        compatible = "fsl,imx93-gpc";
        reg = <0x44470000 0x10000>;
        interrupts = <GIC_SPI 587 IRQ_TYPE_LEVEL_HIGH>;
        
        pgc {
            #address-cells = <1>;
            #size-cells = <0>;
            
            pgc_a55: power-domain@0 {
                #power-domain-cells = <0>;
                reg = <0>;
                clocks = <&clk IMX93_CLK_A55_SEL>;
            };
            
            pgc_m33: power-domain@1 {
                #power-domain-cells = <0>;
                reg = <1>;
                clocks = <&clk IMX93_CLK_M33>;
            };
            
            pgc_usb: power-domain@2 {
                #power-domain-cells = <0>;
                reg = <2>;
            };
            
            pgc_gpu: power-domain@3 {
                #power-domain-cells = <0>;
                reg = <3>;
                clocks = <&clk IMX93_CLK_GPU>;
            };
        };
    };

4.2 CPU Frequency Scaling (CPUFreq)
------------------------------------

**Operating Performance Points (OPP)**:

.. code-block:: dts

    cpu0: cpu@0 {
        compatible = "arm,cortex-a55";
        device_type = "cpu";
        reg = <0x0>;
        enable-method = "psci";
        clocks = <&clk IMX93_CLK_A55_SEL>;
        operating-points-v2 = <&a55_opp_table>;
    };
    
    a55_opp_table: opp-table {
        compatible = "operating-points-v2";
        opp-shared;
        
        opp-900000000 {
            opp-hz = /bits/ 64 <900000000>;
            opp-microvolt = <850000>;
            clock-latency-ns = <150000>;
        };
        
        opp-1200000000 {
            opp-hz = /bits/ 64 <1200000000>;
            opp-microvolt = <950000>;
            clock-latency-ns = <150000>;
        };
        
        opp-1400000000 {
            opp-hz = /bits/ 64 <1400000000>;
            opp-microvolt = <1000000>;
            clock-latency-ns = <150000>;
        };
        
        opp-1700000000 {
            opp-hz = /bits/ 64 <1700000000>;
            opp-microvolt = <1100000>;
            clock-latency-ns = <150000>;
        };
    };

**CPUFreq Governor Configuration**:

.. code-block:: bash

    # Available governors
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
    # conservative ondemand userspace powersave performance schedutil
    
    # Set governor
    echo schedutil > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    
    # View current frequency
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
    
    # Set min/max frequency
    echo 900000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq
    echo 1400000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq

**Custom Governor (ondemand tuning)**:

.. code-block:: bash

    # Ondemand governor parameters
    cd /sys/devices/system/cpu/cpufreq/ondemand
    
    # Increase sampling rate (check every 50ms instead of 10ms)
    echo 50000 > sampling_rate
    
    # Threshold to increase frequency (80% CPU usage)
    echo 80 > up_threshold
    
    # Powersave bias (prefer lower frequencies)
    echo 100 > powersave_bias

**Project Configuration** (Smart Home Hub):

.. code-block:: bash

    # Use schedutil for responsive power management
    echo schedutil > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    
    # Limit max frequency during battery backup
    if [ "$(cat /sys/class/power_supply/battery/status)" = "Discharging" ]; then
        echo 1200000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
    else
        echo 1700000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
    fi

4.3 Suspend to RAM (i.MX 93)
-----------------------------

**Device Tree Wakeup Sources**:

.. code-block:: dts

    gpio1: gpio@47400000 {
        compatible = "fsl,imx93-gpio", "fsl,imx7d-gpio";
        reg = <0x47400000 0x10000>;
        interrupts = <GIC_SPI 10 IRQ_TYPE_LEVEL_HIGH>;
        gpio-controller;
        #gpio-cells = <2>;
        interrupt-controller;
        #interrupt-cells = <2>;
        wakeup-source;  /* Enable GPIO as wakeup source */
    };
    
    rtc: rtc@44440000 {
        compatible = "fsl,imx93-snvs-rtc";
        reg = <0x44440000 0x10000>;
        interrupts = <GIC_SPI 53 IRQ_TYPE_LEVEL_HIGH>;
        clocks = <&clk IMX93_CLK_SNVS>;
        wakeup-source;  /* Enable RTC alarm as wakeup */
    };

**Suspend Script**:

.. code-block:: bash

    #!/bin/bash
    # suspend_imx93.sh
    
    # Enable wakeup sources
    echo enabled > /sys/devices/platform/soc@0/44000000.bus/44440000.rtc/power/wakeup
    echo enabled > /sys/devices/platform/soc@0/44000000.bus/443f0000.snvs/power/wakeup
    
    # Set RTC wakeup alarm (60 seconds)
    rtcwake -m mem -s 60

**Suspend Handler** (kernel):

.. code-block:: c

    /* arch/arm64/mach-imx/pm-imx93.c */
    
    static int imx93_suspend_enter(suspend_state_t state)
    {
        switch (state) {
        case PM_SUSPEND_MEM:
            /* Save GPC state */
            imx93_gpc_save();
            
            /* Configure DDR self-refresh */
            imx_ddrc_enter_self_refresh();
            
            /* Enter suspend */
            cpu_suspend(0, imx93_suspend_finish);
            
            /* Resume */
            imx_ddrc_exit_self_refresh();
            imx93_gpc_restore();
            break;
            
        default:
            return -EINVAL;
        }
        
        return 0;
    }

**Power Measurements** (Smart Home Hub):

.. code-block:: text

    State               Power      Wakeup Latency
    ──────────────────────────────────────────────
    Active (1.7GHz)     2100mW     -
    Idle (WFI)          420mW      <1µs
    WAIT mode           180mW      ~10µs
    STOP mode           85mW       ~50ms
    Suspend (mem)       18mW       ~350ms
    
    Battery Backup (2500mAh @ 3.7V):
    - Suspend: ~510 hours (21 days)
    - STOP: ~108 hours (4.5 days)
    - Idle: ~22 hours

====================
5. Intel Atom Power Management
====================

5.1 ACPI States
---------------

**P-States (Performance)**:

.. code-block:: bash

    # View available frequencies
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
    # 800000 1000000 1200000 1600000 1900000 2400000
    
    # Intel P-State driver
    cat /sys/devices/system/cpu/intel_pstate/status
    # active
    
    # Set performance mode
    echo performance > /sys/devices/system/cpu/intel_pstate/no_turbo
    
    # Set power-saving mode
    echo powersave > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

**C-States (Idle)**:

.. code-block:: bash

    # View available C-states
    ls /sys/devices/system/cpu/cpu0/cpuidle/
    # state0  state1  state2  state3  state4
    
    # View C-state info
    cat /sys/devices/system/cpu/cpu0/cpuidle/state2/name
    # C3
    
    cat /sys/devices/system/cpu/cpu0/cpuidle/state2/latency
    # 96 (µs)
    
    cat /sys/devices/system/cpu/cpu0/cpuidle/state2/power
    # 100 (mW)
    
    # Disable deep C-states (for latency-sensitive apps)
    echo 1 > /sys/devices/system/cpu/cpu0/cpuidle/state3/disable
    echo 1 > /sys/devices/system/cpu/cpu0/cpuidle/state4/disable

**Kernel Parameters**:

.. code-block:: bash

    # Limit C-states (GRUB configuration)
    GRUB_CMDLINE_LINUX="intel_idle.max_cstate=2 processor.max_cstate=2"
    
    # Disable turbo boost
    echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo

5.2 S3 Suspend (Avionics Platform)
-----------------------------------

**Suspend Configuration**:

.. code-block:: bash

    # Check supported sleep states
    cat /sys/power/state
    # freeze mem disk
    
    # Check current mem_sleep mode
    cat /sys/power/mem_sleep
    # s2idle [deep]
    
    # Set to S3 (deep)
    echo deep > /sys/power/mem_sleep
    
    # Suspend to RAM
    systemctl suspend

**Wake-on-LAN Configuration**:

.. code-block:: bash

    # Enable WOL on network interface
    ethtool -s eth0 wol g
    
    # Verify WOL setting
    ethtool eth0 | grep Wake-on
    # Supports Wake-on: pumbg
    # Wake-on: g
    
    # Suspend with WOL enabled
    rtcwake -m mem -s 3600  # or magic packet wakes up

**Project Use Case** (Avionics Platform):

.. code-block:: text

    Ground Operations Power Management:
    - Aircraft parked: System enters S3 suspend
    - Power: 2W (vs. 15W active)
    - Wakeup sources:
      * Ethernet (ground crew connection)
      * GPIO (maintenance panel button)
      * RTC (scheduled checks every 4 hours)
    - Resume time: ~2.8 seconds
    
    Result: 87% power reduction during 12-hour ground operations
    Extended aircraft battery life from 14 hours to 36 hours

5.3 PCIe ASPM (Active State Power Management)
----------------------------------------------

**Enable ASPM**:

.. code-block:: bash

    # View ASPM status
    lspci -vv | grep ASPM
    # LnkCap: ASPM L0s L1
    # LnkCtl: ASPM L1 Enabled
    
    # Enable ASPM in kernel
    # Kernel parameter:
    pcie_aspm=force
    
    # Runtime ASPM control
    echo powersave > /sys/module/pcie_aspm/parameters/policy
    # Policies: default performance powersave powersupersave

**PCIe Device Power Control**:

.. code-block:: c

    /* Driver runtime PM for PCIe device */
    static int pcie_device_runtime_suspend(struct device *dev)
    {
        struct pci_dev *pdev = to_pci_dev(dev);
        
        /* Transition to D3hot */
        pci_save_state(pdev);
        pci_set_power_state(pdev, PCI_D3hot);
        
        return 0;
    }
    
    static int pcie_device_runtime_resume(struct device *dev)
    {
        struct pci_dev *pdev = to_pci_dev(dev);
        
        /* Transition to D0 */
        pci_set_power_state(pdev, PCI_D0);
        pci_restore_state(pdev);
        
        return 0;
    }

====================
6. Device-Specific Power Management
====================

6.1 Display Power Management
-----------------------------

**DRM/KMS DPMS (Display Power Management Signaling)**:

.. code-block:: c

    #include <xf86drm.h>
    #include <xf86drmMode.h>
    
    void set_display_power(int fd, uint32_t connector_id, int mode)
    {
        drmModeObjectProperties *props;
        drmModePropertyRes *prop;
        int i;
        
        props = drmModeObjectGetProperties(fd, connector_id, 
                                          DRM_MODE_OBJECT_CONNECTOR);
        
        for (i = 0; i < props->count_props; i++) {
            prop = drmModeGetProperty(fd, props->props[i]);
            if (strcmp(prop->name, "DPMS") == 0) {
                /* mode: DRM_MODE_DPMS_ON, _STANDBY, _SUSPEND, _OFF */
                drmModeObjectSetProperty(fd, connector_id,
                                        DRM_MODE_OBJECT_CONNECTOR,
                                        prop->prop_id, mode);
            }
            drmModeFreeProperty(prop);
        }
        
        drmModeFreeObjectProperties(props);
    }

**Backlight Control**:

.. code-block:: bash

    # Find backlight device
    ls /sys/class/backlight/
    # pwm-backlight
    
    # Get brightness range
    cat /sys/class/backlight/pwm-backlight/max_brightness
    # 255
    
    # Set brightness (0-255)
    echo 128 > /sys/class/backlight/pwm-backlight/brightness
    
    # Adaptive brightness based on ambient light
    AMBIENT=$(cat /sys/bus/iio/devices/iio:device0/in_illuminance_raw)
    BRIGHTNESS=$((AMBIENT / 40 + 50))  # Scale to 50-255
    echo $BRIGHTNESS > /sys/class/backlight/pwm-backlight/brightness

**Screen Blanking**:

.. code-block:: bash

    # Disable console blanking
    echo 0 > /sys/module/kernel/parameters/consoleblank
    
    # Or at boot (kernel parameter)
    consoleblank=0
    
    # X11 screen blanking
    xset s off          # Disable screensaver
    xset -dpms          # Disable DPMS
    xset dpms 300 600 900  # Standby, suspend, off timeouts (seconds)

6.2 Network Power Management
-----------------------------

**Wake-on-LAN**:

.. code-block:: c

    #include <linux/ethtool.h>
    #include <linux/sockios.h>
    
    int enable_wol(const char *ifname)
    {
        int sock;
        struct ifreq ifr;
        struct ethtool_wolinfo wol;
        
        sock = socket(AF_INET, SOCK_DGRAM, 0);
        
        memset(&ifr, 0, sizeof(ifr));
        strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
        
        wol.cmd = ETHTOOL_GWOL;
        ifr.ifr_data = (caddr_t)&wol;
        ioctl(sock, SIOCETHTOOL, &ifr);
        
        /* Enable WOL on magic packet */
        wol.cmd = ETHTOOL_SWOL;
        wol.wolopts = WAKE_MAGIC;
        ioctl(sock, SIOCETHTOOL, &ifr);
        
        close(sock);
        return 0;
    }

**Wireless Power Save**:

.. code-block:: bash

    # Enable WiFi power management
    iw dev wlan0 set power_save on
    
    # Check power save status
    iw dev wlan0 get power_save
    # Power save: on
    
    # Driver-specific power settings (iwlwifi)
    echo 1 > /sys/module/iwlwifi/parameters/power_save
    echo 5 > /sys/module/iwlwifi/parameters/power_level  # 1-5, higher = more aggressive

**Bluetooth Power Management**:

.. code-block:: bash

    # Enable Bluetooth autosuspend
    echo auto > /sys/bus/usb/devices/1-1.4/power/control
    
    # Set autosuspend delay (2 seconds)
    echo 2000 > /sys/bus/usb/devices/1-1.4/power/autosuspend_delay_ms
    
    # Disable Bluetooth when not in use
    rfkill block bluetooth
    rfkill unblock bluetooth

6.3 Storage Power Management
-----------------------------

**HDD Spindown**:

.. code-block:: bash

    # Install hdparm
    apt-get install hdparm
    
    # Set spindown timeout (5 minutes = 60 * 5 / 5 = 60)
    hdparm -S 60 /dev/sda
    
    # Set advanced power management (1=min power, 255=max performance)
    hdparm -B 128 /dev/sda
    
    # Check current settings
    hdparm -I /dev/sda | grep -i power

**eMMC/SD Power Management**:

.. code-block:: bash

    # Enable runtime PM for MMC
    echo auto > /sys/block/mmcblk0/device/power/control
    
    # Set autosuspend delay
    echo 3000 > /sys/block/mmcblk0/device/power/autosuspend_delay_ms

6.4 USB Power Management
-------------------------

**USB Autosuspend**:

.. code-block:: bash

    # Enable autosuspend globally
    echo auto > /sys/bus/usb/devices/*/power/control
    
    # Set autosuspend delay (2 seconds)
    for dev in /sys/bus/usb/devices/*/power/autosuspend_delay_ms; do
        echo 2000 > $dev
    done
    
    # Disable autosuspend for specific device (e.g., USB webcam)
    echo on > /sys/bus/usb/devices/1-1.2/power/control

**Driver Implementation**:

.. code-block:: c

    static int usb_device_probe(struct usb_interface *intf,
                                const struct usb_device_id *id)
    {
        struct usb_device *udev = interface_to_usbdev(intf);
        
        /* Enable autosuspend */
        usb_enable_autosuspend(udev);
        
        /* Set autosuspend delay (2 seconds) */
        pm_runtime_set_autosuspend_delay(&udev->dev, 2000);
        
        return 0;
    }

====================
7. System-Wide Power Optimization
====================

7.1 PowerTOP Analysis
---------------------

.. code-block:: bash

    # Install PowerTOP
    apt-get install powertop
    
    # Run interactive analysis
    powertop
    
    # Generate HTML report
    powertop --html=powertop-report.html
    
    # Apply all power-saving suggestions
    powertop --auto-tune
    
    # Calibrate (takes ~15 minutes)
    powertop --calibrate

**PowerTOP Tuning Script**:

.. code-block:: bash

    #!/bin/bash
    # power_optimize.sh
    
    # Enable all runtime PM
    for dev in /sys/bus/*/devices/*/power/control; do
        echo auto > $dev 2>/dev/null
    done
    
    # Enable USB autosuspend
    for dev in /sys/bus/usb/devices/*/power/control; do
        echo auto > $dev 2>/dev/null
    done
    
    # Enable SATA link power management
    for dev in /sys/class/scsi_host/*/link_power_management_policy; do
        echo med_power_with_dipm > $dev 2>/dev/null
    done
    
    # Enable audio codec power save
    echo 1 > /sys/module/snd_hda_intel/parameters/power_save 2>/dev/null
    
    # Enable NMI watchdog
    echo 0 > /proc/sys/kernel/nmi_watchdog
    
    # VM writeback timeout
    echo 1500 > /proc/sys/vm/dirty_writeback_centisecs

7.2 Thermal Management
-----------------------

**Thermal Zones**:

.. code-block:: bash

    # List thermal zones
    ls /sys/class/thermal/
    # cooling_device0  thermal_zone0  thermal_zone1
    
    # View thermal zone info
    cat /sys/class/thermal/thermal_zone0/type
    # cpu-thermal
    
    cat /sys/class/thermal/thermal_zone0/temp
    # 45000 (45°C in millidegrees)
    
    # View trip points
    cat /sys/class/thermal/thermal_zone0/trip_point_0_type
    # passive
    cat /sys/class/thermal/thermal_zone0/trip_point_0_temp
    # 85000 (85°C)

**Device Tree Thermal Configuration**:

.. code-block:: dts

    thermal-zones {
        cpu-thermal {
            polling-delay-passive = <250>;  /* ms */
            polling-delay = <1000>;
            thermal-sensors = <&tmu 0>;
            
            trips {
                cpu_alert: cpu-alert {
                    temperature = <85000>;  /* 85°C */
                    hysteresis = <5000>;
                    type = "passive";
                };
                
                cpu_crit: cpu-crit {
                    temperature = <95000>;  /* 95°C */
                    hysteresis = <5000>;
                    type = "critical";
                };
            };
            
            cooling-maps {
                map0 {
                    trip = <&cpu_alert>;
                    cooling-device = <&cpu0 THERMAL_NO_LIMIT THERMAL_NO_LIMIT>;
                };
            };
        };
    };

**Thermal Governor**:

.. code-block:: bash

    # View available governors
    cat /sys/class/thermal/thermal_zone0/available_policies
    # step_wise fair_share user_space power_allocator
    
    # Set governor
    echo power_allocator > /sys/class/thermal/thermal_zone0/policy

7.3 Battery Management
-----------------------

**Battery Monitoring**:

.. code-block:: bash

    # View battery status
    cat /sys/class/power_supply/battery/status
    # Discharging
    
    cat /sys/class/power_supply/battery/capacity
    # 73 (percent)
    
    cat /sys/class/power_supply/battery/voltage_now
    # 3856000 (µV)
    
    cat /sys/class/power_supply/battery/current_now
    # 234000 (µA)
    
    # Calculate power
    # P = V * I = 3.856V * 0.234A = 0.902W

**Low Battery Handler**:

.. code-block:: python

    #!/usr/bin/env python3
    import time
    
    BATTERY_PATH = "/sys/class/power_supply/battery"
    LOW_THRESHOLD = 15  # percent
    CRITICAL_THRESHOLD = 5
    
    def get_battery_capacity():
        with open(f"{BATTERY_PATH}/capacity", 'r') as f:
            return int(f.read().strip())
    
    def is_discharging():
        with open(f"{BATTERY_PATH}/status", 'r') as f:
            return "Discharging" in f.read()
    
    def enter_power_save_mode():
        # Reduce CPU frequency
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq", 'w') as f:
            f.write("900000")
        
        # Reduce display brightness
        with open("/sys/class/backlight/pwm-backlight/brightness", 'w') as f:
            f.write("50")
        
        # Disable non-essential services
        os.system("systemctl stop bluetooth")
        os.system("systemctl stop avahi-daemon")
    
    def critical_shutdown():
        os.system("systemctl poweroff")
    
    while True:
        if is_discharging():
            capacity = get_battery_capacity()
            
            if capacity <= CRITICAL_THRESHOLD:
                print("Critical battery! Shutting down...")
                critical_shutdown()
            elif capacity <= LOW_THRESHOLD:
                print("Low battery! Entering power save mode...")
                enter_power_save_mode()
        
        time.sleep(30)

**Fuel Gauge Driver** (for accurate battery monitoring):

.. code-block:: c

    /* drivers/power/supply/bq27xxx_battery.c example */
    
    static int bq27xxx_battery_read_soc(struct bq27xxx_device_info *di)
    {
        int soc;
        
        soc = bq27xxx_read(di, BQ27XXX_REG_SOC, false);
        if (soc < 0)
            return soc;
        
        return soc;  /* State of charge (0-100%) */
    }
    
    static int bq27xxx_battery_voltage(struct bq27xxx_device_info *di)
    {
        int volt;
        
        volt = bq27xxx_read(di, BQ27XXX_REG_VOLT, false);
        if (volt < 0)
            return volt;
        
        return volt * 1000;  /* Convert to µV */
    }

====================
8. Power Profiling
====================

8.1 Current Measurement Hardware
---------------------------------

**INA226 Current Sensor**:

.. code-block:: c

    /* TI INA226 I2C current/voltage monitor */
    
    #define INA226_ADDR 0x40
    #define INA226_SHUNT_VOLTAGE 0x01
    #define INA226_BUS_VOLTAGE 0x02
    #define INA226_POWER 0x03
    #define INA226_CURRENT 0x04
    
    int ina226_read_current(int i2c_fd, float *current_ma)
    {
        uint16_t raw;
        
        /* Read current register (2 bytes) */
        i2c_smbus_read_word_data(i2c_fd, INA226_CURRENT);
        
        /* Convert to mA (LSB = 1.25mA) */
        *current_ma = (int16_t)raw * 1.25;
        
        return 0;
    }

**Measurement Setup** (Project):

.. code-block:: text

    Power Supply → INA226 → Device Under Test
                      ↓
                   I2C to Host
                   
    Shunt Resistor: 0.01Ω (10mΩ)
    Max Current: 3.2A
    Resolution: 1.25mA
    Sampling Rate: 1kHz

8.2 Software Power Profiling
-----------------------------

**perf Power Events**:

.. code-block:: bash

    # Record power events
    perf stat -e power/energy-cores/,power/energy-pkg/ ./my_app
    
    # Output:
    # 1.234 Joules power/energy-cores/
    # 2.567 Joules power/energy-pkg/

**Ftrace Power Events**:

.. code-block:: bash

    # Enable power events
    echo 1 > /sys/kernel/debug/tracing/events/power/enable
    
    # Trace CPU frequency changes
    echo 1 > /sys/kernel/debug/tracing/events/power/cpu_frequency/enable
    
    # View trace
    cat /sys/kernel/debug/tracing/trace
    
    # Output:
    # cpufreq_interactive-129   [001] .... 12.345: cpu_frequency: state=1200000 cpu_id=0
    # cpufreq_interactive-129   [001] .... 15.678: cpu_frequency: state=1700000 cpu_id=0

====================
9. Automotive Power Management (E-Bike)
====================

9.1 Ignition-Aware Power Control
---------------------------------

**Ignition State Detection**:

.. code-block:: c

    /* GPIO-based ignition detection */
    
    #include <linux/gpio.h>
    #include <linux/interrupt.h>
    
    #define IGN_GPIO 23  /* GPIO for ignition signal */
    
    static irqreturn_t ignition_irq_handler(int irq, void *dev_id)
    {
        struct power_manager *pm = dev_id;
        int ign_state;
        
        ign_state = gpio_get_value(IGN_GPIO);
        
        if (ign_state) {
            /* Ignition ON */
            pr_info("Ignition ON - entering active mode\n");
            pm->state = PM_STATE_ACTIVE;
            queue_work(pm->wq, &pm->power_on_work);
        } else {
            /* Ignition OFF */
            pr_info("Ignition OFF - entering standby mode\n");
            pm->state = PM_STATE_STANDBY;
            queue_delayed_work(pm->wq, &pm->power_off_work,
                             msecs_to_jiffies(30000));  /* 30s delay */
        }
        
        return IRQ_HANDLED;
    }
    
    static int power_manager_probe(struct platform_device *pdev)
    {
        struct power_manager *pm;
        int ret, irq;
        
        pm = devm_kzalloc(&pdev->dev, sizeof(*pm), GFP_KERNEL);
        
        /* Configure GPIO */
        ret = gpio_request(IGN_GPIO, "ignition");
        gpio_direction_input(IGN_GPIO);
        
        /* Request IRQ for both edges */
        irq = gpio_to_irq(IGN_GPIO);
        ret = request_irq(irq, ignition_irq_handler,
                         IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                         "ignition", pm);
        
        return 0;
    }

**Power State Machine**:

.. code-block:: text

    ┌─────────────┐
    │   OFF       │
    └──────┬──────┘
           │ Ignition ON
           ▼
    ┌─────────────┐
    │   ACTIVE    │◄──── User activity
    └──────┬──────┘
           │ No activity (5 min)
           ▼
    ┌─────────────┐
    │   IDLE      │
    └──────┬──────┘
           │ Ignition OFF + delay (30s)
           ▼
    ┌─────────────┐
    │   STANDBY   │
    └──────┬──────┘
           │ No wakeup (8 hours)
           ▼
    ┌─────────────┐
    │   OFF       │
    └─────────────┘

9.2 Watchdog-Based Shutdown
----------------------------

**Delayed Shutdown Service**:

.. code-block:: bash

    # /etc/systemd/system/auto-shutdown.service
    
    [Unit]
    Description=Auto-shutdown after ignition off
    
    [Service]
    Type=oneshot
    ExecStart=/usr/bin/auto-shutdown.sh
    RemainAfterExit=yes
    ExecStop=/bin/true
    
    [Install]
    WantedBy=multi-user.target

.. code-block:: bash

    #!/bin/bash
    # /usr/bin/auto-shutdown.sh
    
    IGN_GPIO_PATH="/sys/class/gpio/gpio23"
    SHUTDOWN_DELAY=30  # seconds
    
    while true; do
        IGN_STATE=$(cat $IGN_GPIO_PATH/value)
        
        if [ "$IGN_STATE" = "0" ]; then
            echo "Ignition OFF detected"
            sleep $SHUTDOWN_DELAY
            
            # Check again after delay
            IGN_STATE=$(cat $IGN_GPIO_PATH/value)
            if [ "$IGN_STATE" = "0" ]; then
                echo "Shutting down..."
                systemctl poweroff
            fi
        fi
        
        sleep 5
    done

====================
10. Project Power Results Summary
====================

**Thermal Imaging Camera (DaVinci DM365)**:

.. code-block:: text

    Configuration:
    - 300 MHz ARM9 + DSP
    - 128MB DDR2
    - 16-bit thermal sensor
    - NAND flash storage
    
    Power States:
    - Active capture: 285mA @ 3.3V = 941mW
    - Idle (DSP off): 60mA @ 3.3V = 198mW
    - Deep sleep: 2.5mA @ 3.3V = 8.25mW
    - Hibernation: <0.3mA @ 3.3V = <1mW
    
    Battery Life (3000mAh):
    - Continuous: 10.5 hours
    - 1 capture/min: 48 hours
    - 1 capture/hour: 15 days
    
    Optimizations Implemented:
    ✓ DSP clock gating when not encoding
    ✓ DDR self-refresh in deep sleep
    ✓ Peripheral power domain control
    ✓ RTC-based hibernation

**Smart Home Hub (i.MX 93)**:

.. code-block:: text

    Configuration:
    - Dual Cortex-A55 @ 1.7GHz
    - Cortex-M33 @ 250MHz
    - 2GB LPDDR4
    - Wi-Fi, Zigbee, Matter
    
    Power States:
    - Active: 2.1W
    - Idle (WFI): 420mW
    - Suspend: 18mW
    
    Battery Backup (2500mAh @ 3.7V):
    - Suspend: 21 days
    - 1 wakeup/hour: 18 days
    
    Optimizations:
    ✓ CPUfreq schedutil governor
    ✓ Runtime PM for all peripherals
    ✓ Wi-Fi power save (PSP mode)
    ✓ Cortex-M33 handles low-power tasks

**E-Bike Infotainment**:

.. code-block:: text

    Configuration:
    - Quad-core Cortex-A53 @ 1.5GHz
    - CAN bus connectivity
    - 7" touchscreen display
    
    Power States:
    - Active (display on): 3.5W
    - Idle (display dim): 680mW
    - Standby (ignition off): 35mW
    
    Ignition-Based Power Management:
    - ON: Full active mode
    - OFF + 30s: Enter standby
    - OFF + 8hr: Power off
    
    Result: <0.3% battery drain per day when parked

====================
11. References
====================

**Linux Power Management**:

- Documentation/power/ in kernel source
- https://www.kernel.org/doc/html/latest/power/

**TI DaVinci**:

- SPRUFL8B: DM36x Power Management User's Guide
- SPRUFG5: DM36x ARM Subsystem Reference Guide

**NXP i.MX**:

- IMX93RM: i.MX 93 Reference Manual (Chapter 14: Power Management)
- AN5383: i.MX Linux Power Management and Optimization

**Intel**:

- Intel® 64 and IA-32 Architectures Software Developer's Manual (Vol 3, Ch 14: Power Management)

**Tools**:

- PowerTOP: https://github.com/fenrus75/powertop
- TLP: https://linrunner.de/tlp/

---

**Revision History**:

========  ==========  ====================================
Version   Date        Changes
========  ==========  ====================================
1.0       2026-01-22  Initial comprehensive power guide
========  ==========  ====================================
