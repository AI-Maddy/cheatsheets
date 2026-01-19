==========================
Linux PWM Drivers Guide
==========================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

PWM Provider (Driver)
---------------------

.. code-block:: c

   #include <linux/pwm.h>
   
   static int mypwm_apply(struct pwm_chip *chip, struct pwm_device *pwm,
                           const struct pwm_state *state) {
       struct mypwm_data *data = to_mypwm_data(chip);
       u64 period_ns = state->period;
       u64 duty_ns = state->duty_cycle;
       bool enabled = state->enabled;
       
       /* Configure hardware */
       mypwm_set_period(data, period_ns);
       mypwm_set_duty(data, duty_ns);
       
       if (enabled)
           mypwm_enable(data);
       else
           mypwm_disable(data);
       
       return 0;
   }
   
   static const struct pwm_ops mypwm_ops = {
       .apply = mypwm_apply,
       .owner = THIS_MODULE,
   };
   
   /* Register PWM chip */
   chip->ops = &mypwm_ops;
   chip->npwm = 4;  // Number of PWM channels
   ret = pwmchip_add(chip);

PWM Consumer (User)
-------------------

.. code-block:: c

   struct pwm_device *pwm;
   struct pwm_state state;
   
   /* Get PWM device */
   pwm = devm_pwm_get(&pdev->dev, NULL);
   if (IS_ERR(pwm))
       return PTR_ERR(pwm);
   
   /* Prepare state */
   pwm_init_state(pwm, &state);
   state.period = 1000000;      // 1ms = 1kHz
   state.duty_cycle = 500000;   // 50% duty cycle
   state.polarity = PWM_POLARITY_NORMAL;
   state.enabled = true;
   
   /* Apply configuration and enable */
   ret = pwm_apply_state(pwm, &state);

PWM Subsystem Overview
=======================

PWM Concepts
------------

**Period:** Total cycle time (nanoseconds)
**Duty Cycle:** High time within period (nanoseconds)
**Frequency:** 1,000,000,000 / period (Hz)
**Duty Cycle %:** (duty_cycle / period) * 100

.. code-block:: text

   Period = 1,000,000 ns (1ms)
   Frequency = 1 kHz
   Duty = 500,000 ns (50%)
   
   ____      ____      ____
   |  |______|  |______|  |______
   <-period->
   <duty>

PWM State
---------

.. code-block:: c

   struct pwm_state {
       u64 period;          // Period in nanoseconds
       u64 duty_cycle;      // Duty cycle in nanoseconds
       enum pwm_polarity polarity;  // PWM_POLARITY_NORMAL or _INVERSED
       bool enabled;        // Enabled state
   };

PWM Provider (Driver)
=====================

Basic PWM Driver
----------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/pwm.h>
   #include <linux/platform_device.h>
   #include <linux/io.h>
   #include <linux/clk.h>
   
   struct mypwm_data {
       struct pwm_chip chip;
       void __iomem *regs;
       struct clk *clk;
       unsigned long clk_rate;
   };
   
   #define to_mypwm_data(c) container_of(c, struct mypwm_data, chip)
   
   static int mypwm_apply(struct pwm_chip *chip, struct pwm_device *pwm,
                           const struct pwm_state *state) {
       struct mypwm_data *data = to_mypwm_data(chip);
       u64 period_cycles, duty_cycles;
       u32 prescaler, period_val, duty_val;
       
       /* Calculate cycles from nanoseconds */
       period_cycles = (u64)data->clk_rate * state->period;
       do_div(period_cycles, NSEC_PER_SEC);
       
       duty_cycles = (u64)data->clk_rate * state->duty_cycle;
       do_div(duty_cycles, NSEC_PER_SEC);
       
       /* Find suitable prescaler */
       prescaler = (period_cycles / 65536) + 1;
       period_val = period_cycles / prescaler;
       duty_val = duty_cycles / prescaler;
       
       if (period_val == 0 || period_val > 65535)
           return -EINVAL;
       
       /* Write to hardware registers */
       writel(prescaler - 1, data->regs + PWM_PRESCALER);
       writel(period_val, data->regs + PWM_PERIOD);
       writel(duty_val, data->regs + PWM_DUTY);
       
       /* Handle polarity */
       if (state->polarity == PWM_POLARITY_INVERSED)
           writel(readl(data->regs + PWM_CTRL) | PWM_POLARITY_BIT,
                   data->regs + PWM_CTRL);
       else
           writel(readl(data->regs + PWM_CTRL) & ~PWM_POLARITY_BIT,
                   data->regs + PWM_CTRL);
       
       /* Enable/disable */
       if (state->enabled)
           writel(readl(data->regs + PWM_CTRL) | PWM_ENABLE_BIT,
                   data->regs + PWM_CTRL);
       else
           writel(readl(data->regs + PWM_CTRL) & ~PWM_ENABLE_BIT,
                   data->regs + PWM_CTRL);
       
       return 0;
   }
   
   static void mypwm_get_state(struct pwm_chip *chip, struct pwm_device *pwm,
                                struct pwm_state *state) {
       struct mypwm_data *data = to_mypwm_data(chip);
       u32 prescaler, period_val, duty_val, ctrl;
       u64 period_ns, duty_ns;
       
       prescaler = readl(data->regs + PWM_PRESCALER) + 1;
       period_val = readl(data->regs + PWM_PERIOD);
       duty_val = readl(data->regs + PWM_DUTY);
       ctrl = readl(data->regs + PWM_CTRL);
       
       /* Convert to nanoseconds */
       period_ns = (u64)period_val * prescaler * NSEC_PER_SEC;
       do_div(period_ns, data->clk_rate);
       
       duty_ns = (u64)duty_val * prescaler * NSEC_PER_SEC;
       do_div(duty_ns, data->clk_rate);
       
       state->period = period_ns;
       state->duty_cycle = duty_ns;
       state->polarity = (ctrl & PWM_POLARITY_BIT) ?
                          PWM_POLARITY_INVERSED : PWM_POLARITY_NORMAL;
       state->enabled = !!(ctrl & PWM_ENABLE_BIT);
   }
   
   static const struct pwm_ops mypwm_ops = {
       .apply = mypwm_apply,
       .get_state = mypwm_get_state,
       .owner = THIS_MODULE,
   };
   
   static int mypwm_probe(struct platform_device *pdev) {
       struct mypwm_data *data;
       struct resource *res;
       int ret;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       /* Map registers */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       data->regs = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(data->regs))
           return PTR_ERR(data->regs);
       
       /* Get clock */
       data->clk = devm_clk_get(&pdev->dev, NULL);
       if (IS_ERR(data->clk))
           return PTR_ERR(data->clk);
       
       ret = clk_prepare_enable(data->clk);
       if (ret)
           return ret;
       
       data->clk_rate = clk_get_rate(data->clk);
       
       /* Setup PWM chip */
       data->chip.dev = &pdev->dev;
       data->chip.ops = &mypwm_ops;
       data->chip.npwm = 4;  // 4 PWM channels
       
       platform_set_drvdata(pdev, data);
       
       /* Register PWM chip */
       ret = pwmchip_add(&data->chip);
       if (ret) {
           dev_err(&pdev->dev, "Failed to add PWM chip: %d\n", ret);
           clk_disable_unprepare(data->clk);
           return ret;
       }
       
       dev_info(&pdev->dev, "PWM chip registered with %d channels\n",
                data->chip.npwm);
       
       return 0;
   }
   
   static int mypwm_remove(struct platform_device *pdev) {
       struct mypwm_data *data = platform_get_drvdata(pdev);
       
       pwmchip_remove(&data->chip);
       clk_disable_unprepare(data->clk);
       
       return 0;
   }
   
   static const struct of_device_id mypwm_of_match[] = {
       { .compatible = "vendor,pwm", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mypwm_of_match);
   
   static struct platform_driver mypwm_driver = {
       .driver = {
           .name = "mypwm",
           .of_match_table = mypwm_of_match,
       },
       .probe = mypwm_probe,
       .remove = mypwm_remove,
   };
   
   module_platform_driver(mypwm_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("PWM Driver");

PWM Consumer (User)
===================

Getting PWM Device
------------------

.. code-block:: c

   /* From device tree */
   struct pwm_device *pwm;
   pwm = devm_pwm_get(&pdev->dev, NULL);  // First PWM in DT
   pwm = devm_pwm_get(&pdev->dev, "backlight");  // Named PWM
   
   /* Or with explicit index */
   pwm = devm_pwm_get(&pdev->dev, "pwm");

Using PWM
---------

.. code-block:: c

   #include <linux/pwm.h>
   
   struct pwm_device *pwm;
   struct pwm_state state;
   int ret;
   
   /* Get PWM */
   pwm = devm_pwm_get(&pdev->dev, NULL);
   if (IS_ERR(pwm)) {
       dev_err(&pdev->dev, "Failed to get PWM: %ld\n", PTR_ERR(pwm));
       return PTR_ERR(pwm);
   }
   
   /* Initialize state with current settings */
   pwm_init_state(pwm, &state);
   
   /* Configure PWM */
   state.period = 1000000;      // 1ms (1 kHz)
   state.duty_cycle = 500000;   // 50% duty cycle
   state.polarity = PWM_POLARITY_NORMAL;
   state.enabled = true;
   
   /* Apply settings */
   ret = pwm_apply_state(pwm, &state);
   if (ret) {
       dev_err(&pdev->dev, "Failed to apply PWM state: %d\n", ret);
       return ret;
   }
   
   /* Later: disable PWM */
   state.enabled = false;
   pwm_apply_state(pwm, &state);

Adjusting Duty Cycle
---------------------

.. code-block:: c

   static int set_brightness(struct pwm_device *pwm, unsigned int percent) {
       struct pwm_state state;
       
       pwm_get_state(pwm, &state);
       
       /* Calculate duty cycle from percentage */
       state.duty_cycle = (state.period * percent) / 100;
       
       return pwm_apply_state(pwm, &state);
   }
   
   /* Example usage */
   set_brightness(pwm, 75);  // 75% brightness

Device Tree Integration
=======================

PWM Provider Node
-----------------

.. code-block:: dts

   pwm: pwm@40000000 {
       compatible = "vendor,pwm";
       reg = <0x40000000 0x1000>;
       clocks = <&clk_pwm>;
       #pwm-cells = <2>;  // <channel_number> <period_in_ns>
   };

PWM Consumer Node
-----------------

.. code-block:: dts

   backlight {
       compatible = "pwm-backlight";
       pwms = <&pwm 0 1000000>;  // Channel 0, 1ms period (1kHz)
       brightness-levels = <0 10 20 30 40 50 60 70 80 90 100>;
       default-brightness-level = <5>;
   };
   
   led {
       compatible = "pwm-leds";
       pwms = <&pwm 1 1000000>;  // Channel 1
   };

PWM Backlight Example
======================

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/pwm.h>
   #include <linux/backlight.h>
   #include <linux/of.h>
   
   struct pwm_bl_data {
       struct pwm_device *pwm;
       unsigned int max_brightness;
       unsigned int *levels;
       unsigned int nlevel;
   };
   
   static int pwm_bl_update_status(struct backlight_device *bl) {
       struct pwm_bl_data *pb = bl_get_data(bl);
       struct pwm_state state;
       unsigned int brightness = bl->props.brightness;
       unsigned int duty;
       
       if (bl->props.power != FB_BLANK_UNBLANK ||
           bl->props.fb_blank != FB_BLANK_UNBLANK ||
           bl->props.state & BL_CORE_FBBLANK)
           brightness = 0;
       
       if (brightness == 0) {
           pwm_get_state(pb->pwm, &state);
           state.enabled = false;
           pwm_apply_state(pb->pwm, &state);
           return 0;
       }
       
       /* Get duty cycle from brightness level */
       if (pb->levels)
           duty = pb->levels[brightness];
       else
           duty = brightness;
       
       pwm_get_state(pb->pwm, &state);
       state.duty_cycle = (state.period * duty) / pb->max_brightness;
       state.enabled = true;
       
       return pwm_apply_state(pb->pwm, &state);
   }
   
   static int pwm_bl_get_brightness(struct backlight_device *bl) {
       return bl->props.brightness;
   }
   
   static const struct backlight_ops pwm_bl_ops = {
       .update_status = pwm_bl_update_status,
       .get_brightness = pwm_bl_get_brightness,
   };
   
   static int pwm_bl_probe(struct platform_device *pdev) {
       struct pwm_bl_data *pb;
       struct backlight_device *bl;
       struct backlight_properties props;
       struct pwm_state state;
       int ret;
       
       pb = devm_kzalloc(&pdev->dev, sizeof(*pb), GFP_KERNEL);
       if (!pb)
           return -ENOMEM;
       
       /* Get PWM */
       pb->pwm = devm_pwm_get(&pdev->dev, NULL);
       if (IS_ERR(pb->pwm))
           return PTR_ERR(pb->pwm);
       
       /* Parse brightness levels from DT */
       pb->max_brightness = 100;  // Default
       
       /* Initialize PWM */
       pwm_init_state(pb->pwm, &state);
       state.period = 1000000;  // 1ms
       state.duty_cycle = 0;
       state.enabled = false;
       
       ret = pwm_apply_state(pb->pwm, &state);
       if (ret)
           return ret;
       
       /* Register backlight device */
       memset(&props, 0, sizeof(props));
       props.type = BACKLIGHT_RAW;
       props.max_brightness = pb->max_brightness;
       props.brightness = 0;
       props.power = FB_BLANK_POWERDOWN;
       
       bl = devm_backlight_device_register(&pdev->dev, "pwm-backlight",
                                            &pdev->dev, pb, &pwm_bl_ops,
                                            &props);
       if (IS_ERR(bl))
           return PTR_ERR(bl);
       
       platform_set_drvdata(pdev, bl);
       
       dev_info(&pdev->dev, "PWM backlight registered\n");
       return 0;
   }
   
   static const struct of_device_id pwm_bl_of_match[] = {
       { .compatible = "pwm-backlight", },
       { }
   };
   MODULE_DEVICE_TABLE(of, pwm_bl_of_match);
   
   static struct platform_driver pwm_bl_driver = {
       .driver = {
           .name = "pwm-backlight",
           .of_match_table = pwm_bl_of_match,
       },
       .probe = pwm_bl_probe,
   };
   
   module_platform_driver(pwm_bl_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("PWM Backlight Driver");

Best Practices
==============

1. **Use pwm_apply_state()** for atomic updates
2. **Implement get_state()** for proper state query
3. **Handle clock management** properly
4. **Validate period/duty** values
5. **Use devm_pwm_get()** for automatic cleanup
6. **Check hardware capabilities**
7. **Support polarity inversion**
8. **Document frequency limitations**
9. **Test edge cases** (0%, 100% duty)
10. **Use nanosecond precision**

Common Pitfalls
===============

1. **Integer overflow** in calculations
2. **Not using do_div()** for 64-bit division
3. **Incorrect prescaler** calculation
4. **Missing clock enable**
5. **Race conditions** in multi-channel chips
6. **Not validating** period/duty ranges

Debugging
=========

.. code-block:: bash

   # List PWM devices
   ls /sys/class/pwm/
   
   # Export PWM channel
   echo 0 > /sys/class/pwm/pwmchip0/export
   
   # Configure PWM
   echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period
   echo 500000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
   echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable
   
   # Read current state
   cat /sys/class/pwm/pwmchip0/pwm0/period
   cat /sys/class/pwm/pwmchip0/pwm0/duty_cycle

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Regmap_API.rst
- Linux_Device_Tree_Drivers.rst

References
==========

- Documentation/driver-api/pwm.rst
- Documentation/devicetree/bindings/pwm/
- include/linux/pwm.h
