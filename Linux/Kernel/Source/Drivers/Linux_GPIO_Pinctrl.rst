==============================
Linux GPIO and Pinctrl Guide
==============================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

GPIO Consumer API (Descriptor-Based)
-------------------------------------

.. code-block:: c

   #include <linux/gpio/consumer.h>
   
   /* Get GPIO from device tree */
   struct gpio_desc *gpio;
   gpio = devm_gpiod_get(&pdev->dev, "reset", GPIOD_OUT_LOW);
   if (IS_ERR(gpio))
       return PTR_ERR(gpio);
   
   /* Set value */
   gpiod_set_value(gpio, 1);  // Fast, atomic
   gpiod_set_value_cansleep(gpio, 1);  // May sleep (I2C GPIO expanders)
   
   /* Get value */
   int val = gpiod_get_value(gpio);
   
   /* Get multiple GPIOs */
   struct gpio_desc *reset_gpio, *power_gpio;
   reset_gpio = devm_gpiod_get_index(&pdev->dev, "control", 0, GPIOD_OUT_LOW);
   power_gpio = devm_gpiod_get_index(&pdev->dev, "control", 1, GPIOD_OUT_HIGH);
   
   /* GPIO IRQ */
   int irq = gpiod_to_irq(gpio);
   devm_request_irq(&pdev->dev, irq, handler, IRQF_TRIGGER_RISING, "mydev", data);

Device Tree GPIO Bindings
--------------------------

.. code-block:: dts

   mydevice {
       compatible = "vendor,device";
       reset-gpios = <&gpio1 5 GPIO_ACTIVE_LOW>;
       power-gpios = <&gpio2 10 GPIO_ACTIVE_HIGH>;
       control-gpios = <&gpio1 6 GPIO_ACTIVE_HIGH>,
                       <&gpio1 7 GPIO_ACTIVE_HIGH>;
   };

GPIO Fundamentals
=================

GPIO Descriptor API
-------------------

The modern GPIO API uses descriptors (struct gpio_desc *) instead of integer GPIO numbers.

**Advantages:**

- Type-safe
- Device tree integration
- Automatic active-low handling
- Better error handling

Getting GPIOs
-------------

.. code-block:: c

   #include <linux/gpio/consumer.h>
   
   /* Single GPIO by name */
   struct gpio_desc *gpio;
   gpio = devm_gpiod_get(&dev, "reset", GPIOD_OUT_LOW);
   
   /* Flags: */
   // GPIOD_IN - Input
   // GPIOD_OUT_LOW - Output, initially low
   // GPIOD_OUT_HIGH - Output, initially high
   // GPIOD_OUT_LOW_OPEN_DRAIN - Open drain, initially low
   // GPIOD_OUT_HIGH_OPEN_DRAIN - Open drain, initially high
   
   /* Optional GPIO (doesn't fail if missing) */
   gpio = devm_gpiod_get_optional(&dev, "enable", GPIOD_OUT_HIGH);
   if (IS_ERR(gpio))
       return PTR_ERR(gpio);
   if (!gpio)
       dev_info(&dev, "Optional GPIO not present\n");
   
   /* GPIO by index (for multiple GPIOs) */
   struct gpio_desc *gpio0, *gpio1;
   gpio0 = devm_gpiod_get_index(&dev, "control", 0, GPIOD_OUT_LOW);
   gpio1 = devm_gpiod_get_index(&dev, "control", 1, GPIOD_OUT_LOW);
   
   /* GPIO array */
   struct gpio_descs *gpios;
   gpios = devm_gpiod_get_array(&dev, "data", GPIOD_OUT_LOW);
   if (!IS_ERR(gpios)) {
       dev_info(&dev, "Got %d GPIOs\n", gpios->ndescs);
   }

Setting/Getting GPIO Values
----------------------------

.. code-block:: c

   /* Set GPIO value (atomic context OK) */
   gpiod_set_value(gpio, 1);  // High
   gpiod_set_value(gpio, 0);  // Low
   
   /* Set GPIO value (may sleep - for I2C/SPI GPIO expanders) */
   gpiod_set_value_cansleep(gpio, 1);
   
   /* Get GPIO value */
   int value = gpiod_get_value(gpio);
   
   /* Direction control */
   gpiod_direction_input(gpio);
   gpiod_direction_output(gpio, 1);  // Set as output with initial value
   
   /* Get direction */
   int dir = gpiod_get_direction(gpio);  // 0=out, 1=in
   
   /* Toggle */
   gpiod_set_value(gpio, !gpiod_get_value(gpio));

GPIO Arrays
-----------

.. code-block:: c

   struct gpio_descs *data_lines;
   unsigned long values_bitmap;
   int i;
   
   data_lines = devm_gpiod_get_array(&pdev->dev, "data", GPIOD_OUT_LOW);
   if (IS_ERR(data_lines))
       return PTR_ERR(data_lines);
   
   /* Set array values (efficient for same controller) */
   unsigned long values[] = { 0xAA };  // Bitmap
   gpiod_set_array_value(data_lines->ndescs, data_lines->desc,
                          NULL, values);
   
   /* Get array values */
   gpiod_get_array_value(data_lines->ndescs, data_lines->desc,
                          NULL, &values_bitmap);
   
   /* Individual access */
   for (i = 0; i < data_lines->ndescs; i++)
       gpiod_set_value(data_lines->desc[i], (data >> i) & 1);

GPIO Interrupts
===============

GPIO to IRQ Conversion
----------------------

.. code-block:: c

   #include <linux/interrupt.h>
   
   static irqreturn_t mydev_irq_handler(int irq, void *data) {
       struct mydev_data *mydata = data;
       
       /* Read GPIO state */
       int gpio_state = gpiod_get_value(mydata->gpio);
       
       dev_info(mydata->dev, "IRQ triggered, GPIO=%d\n", gpio_state);
       
       return IRQ_HANDLED;
   }
   
   static int mydev_setup_irq(struct platform_device *pdev,
                               struct mydev_data *data) {
       int irq, ret;
       
       /* Get IRQ number from GPIO */
       irq = gpiod_to_irq(data->gpio);
       if (irq < 0) {
           dev_err(&pdev->dev, "Cannot get IRQ: %d\n", irq);
           return irq;
       }
       
       /* Request IRQ */
       ret = devm_request_irq(&pdev->dev, irq, mydev_irq_handler,
                               IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                               "mydevice", data);
       if (ret) {
           dev_err(&pdev->dev, "Failed to request IRQ: %d\n", ret);
           return ret;
       }
       
       data->irq = irq;
       return 0;
   }

Edge and Level Triggers
-----------------------

.. code-block:: c

   /* Edge triggers */
   devm_request_irq(&dev, irq, handler, IRQF_TRIGGER_RISING, name, data);
   devm_request_irq(&dev, irq, handler, IRQF_TRIGGER_FALLING, name, data);
   devm_request_irq(&dev, irq, handler,
                     IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                     name, data);
   
   /* Level triggers */
   devm_request_irq(&dev, irq, handler, IRQF_TRIGGER_HIGH, name, data);
   devm_request_irq(&dev, irq, handler, IRQF_TRIGGER_LOW, name, data);

Pinctrl Subsystem
=================

Introduction
------------

The pinctrl subsystem manages pin multiplexing and configuration.

**Functions:**

- Pin multiplexing (selecting function)
- Pin configuration (pull-up/down, drive strength, etc.)
- Pin groups management

Device Tree Pinctrl
-------------------

.. code-block:: dts

   /* Define pinctrl states in SoC dtsi */
   &iomuxc {
       mydevice_pins: mydevice {
           fsl,pins = <
               MX6QDL_PAD_GPIO_5__GPIO1_IO05    0x1b0b0  /* Reset */
               MX6QDL_PAD_GPIO_6__GPIO1_IO06    0x1b0b0  /* Enable */
               MX6QDL_PAD_GPIO_7__UART1_TX_DATA 0x1b0b0
               MX6QDL_PAD_GPIO_8__UART1_RX_DATA 0x1b0b0
           >;
       };
       
       mydevice_sleep: mydevice_sleep {
           fsl,pins = <
               MX6QDL_PAD_GPIO_5__GPIO1_IO05    0x10000  /* Low power */
           >;
       };
   };
   
   /* Reference in device node */
   mydevice {
       compatible = "vendor,device";
       pinctrl-names = "default", "sleep";
       pinctrl-0 = <&mydevice_pins>;
       pinctrl-1 = <&mydevice_sleep>;
   };

Using Pinctrl in Drivers
-------------------------

.. code-block:: c

   #include <linux/pinctrl/consumer.h>
   
   struct mydev_data {
       struct pinctrl *pinctrl;
       struct pinctrl_state *pins_default;
       struct pinctrl_state *pins_sleep;
   };
   
   static int mydev_init_pinctrl(struct device *dev,
                                  struct mydev_data *data) {
       int ret;
       
       /* Get pinctrl handle (automatic with devm_) */
       data->pinctrl = devm_pinctrl_get(dev);
       if (IS_ERR(data->pinctrl)) {
           if (PTR_ERR(data->pinctrl) == -EPROBE_DEFER)
               return -EPROBE_DEFER;
           /* Pinctrl is optional for some devices */
           dev_info(dev, "No pinctrl available\n");
           data->pinctrl = NULL;
           return 0;
       }
       
       /* Get default state */
       data->pins_default = pinctrl_lookup_state(data->pinctrl, "default");
       if (IS_ERR(data->pins_default)) {
           dev_err(dev, "Cannot find default pinctrl state\n");
           return PTR_ERR(data->pins_default);
       }
       
       /* Get sleep state (optional) */
       data->pins_sleep = pinctrl_lookup_state(data->pinctrl, "sleep");
       if (IS_ERR(data->pins_sleep))
           data->pins_sleep = NULL;
       
       /* Apply default state */
       ret = pinctrl_select_state(data->pinctrl, data->pins_default);
       if (ret) {
           dev_err(dev, "Cannot select default pinctrl state\n");
           return ret;
       }
       
       return 0;
   }
   
   /* In suspend function */
   static int mydev_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       if (data->pinctrl && data->pins_sleep)
           pinctrl_select_state(data->pinctrl, data->pins_sleep);
       
       return 0;
   }
   
   /* In resume function */
   static int mydev_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       if (data->pinctrl && data->pins_default)
           pinctrl_select_state(data->pinctrl, data->pins_default);
       
       return 0;
   }

Complete Driver Example
========================

GPIO-Based LED Driver
---------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/gpio/consumer.h>
   #include <linux/of.h>
   #include <linux/leds.h>
   
   struct gpio_led_data {
       struct led_classdev cdev;
       struct gpio_desc *gpio;
       bool active_low;
   };
   
   static void gpio_led_set(struct led_classdev *cdev,
                             enum led_brightness value) {
       struct gpio_led_data *led = container_of(cdev,
                                                  struct gpio_led_data, cdev);
       
       gpiod_set_value_cansleep(led->gpio, value != LED_OFF);
   }
   
   static enum led_brightness gpio_led_get(struct led_classdev *cdev) {
       struct gpio_led_data *led = container_of(cdev,
                                                  struct gpio_led_data, cdev);
       
       return gpiod_get_value_cansleep(led->gpio) ? LED_FULL : LED_OFF;
   }
   
   static int gpio_led_probe(struct platform_device *pdev) {
       struct gpio_led_data *led;
       struct device_node *np = pdev->dev.of_node;
       const char *name;
       int ret;
       
       led = devm_kzalloc(&pdev->dev, sizeof(*led), GFP_KERNEL);
       if (!led)
           return -ENOMEM;
       
       /* Get GPIO */
       led->gpio = devm_gpiod_get(&pdev->dev, "led", GPIOD_OUT_LOW);
       if (IS_ERR(led->gpio)) {
           dev_err(&pdev->dev, "Failed to get GPIO\n");
           return PTR_ERR(led->gpio);
       }
       
       /* Get LED name from DT */
       ret = of_property_read_string(np, "label", &name);
       if (ret < 0)
           name = np->name;
       
       led->cdev.name = name;
       led->cdev.brightness_set = gpio_led_set;
       led->cdev.brightness_get = gpio_led_get;
       led->cdev.max_brightness = LED_FULL;
       
       /* Get default state */
       if (of_property_read_bool(np, "default-on"))
           led->cdev.brightness = LED_FULL;
       else
           led->cdev.brightness = LED_OFF;
       
       gpiod_set_value_cansleep(led->gpio, led->cdev.brightness);
       
       ret = devm_led_classdev_register(&pdev->dev, &led->cdev);
       if (ret) {
           dev_err(&pdev->dev, "Failed to register LED\n");
           return ret;
       }
       
       platform_set_drvdata(pdev, led);
       dev_info(&pdev->dev, "GPIO LED '%s' registered\n", name);
       
       return 0;
   }
   
   static const struct of_device_id gpio_led_of_match[] = {
       { .compatible = "gpio-led", },
       { }
   };
   MODULE_DEVICE_TABLE(of, gpio_led_of_match);
   
   static struct platform_driver gpio_led_driver = {
       .driver = {
           .name = "gpio-led",
           .of_match_table = gpio_led_of_match,
       },
       .probe = gpio_led_probe,
   };
   
   module_platform_driver(gpio_led_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("GPIO LED Driver");

GPIO Button Driver with IRQ
----------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/gpio/consumer.h>
   #include <linux/interrupt.h>
   #include <linux/input.h>
   #include <linux/of.h>
   
   struct gpio_button_data {
       struct input_dev *input;
       struct gpio_desc *gpio;
       int irq;
       unsigned int code;
       struct delayed_work work;
   };
   
   static void gpio_button_work(struct work_struct *work) {
       struct gpio_button_data *button = container_of(work,
                                                        struct gpio_button_data,
                                                        work.work);
       int state;
       
       state = gpiod_get_value_cansleep(button->gpio);
       
       input_event(button->input, EV_KEY, button->code, state);
       input_sync(button->input);
       
       dev_dbg(button->input->dev.parent,
               "Button state: %d\n", state);
   }
   
   static irqreturn_t gpio_button_irq(int irq, void *data) {
       struct gpio_button_data *button = data;
       
       /* Debounce: schedule work after 10ms */
       schedule_delayed_work(&button->work, msecs_to_jiffies(10));
       
       return IRQ_HANDLED;
   }
   
   static int gpio_button_probe(struct platform_device *pdev) {
       struct gpio_button_data *button;
       struct device_node *np = pdev->dev.of_node;
       int ret;
       
       button = devm_kzalloc(&pdev->dev, sizeof(*button), GFP_KERNEL);
       if (!button)
           return -ENOMEM;
       
       /* Get GPIO */
       button->gpio = devm_gpiod_get(&pdev->dev, "button", GPIOD_IN);
       if (IS_ERR(button->gpio)) {
           dev_err(&pdev->dev, "Failed to get GPIO\n");
           return PTR_ERR(button->gpio);
       }
       
       /* Get button code */
       ret = of_property_read_u32(np, "linux,code", &button->code);
       if (ret < 0) {
           dev_err(&pdev->dev, "Missing linux,code property\n");
           return ret;
       }
       
       /* Setup input device */
       button->input = devm_input_allocate_device(&pdev->dev);
       if (!button->input)
           return -ENOMEM;
       
       button->input->name = "GPIO Button";
       button->input->phys = "gpio-button/input0";
       button->input->id.bustype = BUS_HOST;
       
       input_set_capability(button->input, EV_KEY, button->code);
       
       ret = input_register_device(button->input);
       if (ret) {
           dev_err(&pdev->dev, "Failed to register input device\n");
           return ret;
       }
       
       /* Setup IRQ */
       button->irq = gpiod_to_irq(button->gpio);
       if (button->irq < 0) {
           dev_err(&pdev->dev, "Failed to get IRQ\n");
           return button->irq;
       }
       
       INIT_DELAYED_WORK(&button->work, gpio_button_work);
       
       ret = devm_request_irq(&pdev->dev, button->irq,
                               gpio_button_irq,
                               IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                               "gpio-button", button);
       if (ret) {
           dev_err(&pdev->dev, "Failed to request IRQ\n");
           return ret;
       }
       
       platform_set_drvdata(pdev, button);
       dev_info(&pdev->dev, "GPIO button registered (code=%u)\n",
                button->code);
       
       return 0;
   }
   
   static int gpio_button_remove(struct platform_device *pdev) {
       struct gpio_button_data *button = platform_get_drvdata(pdev);
       
       cancel_delayed_work_sync(&button->work);
       return 0;
   }
   
   static const struct of_device_id gpio_button_of_match[] = {
       { .compatible = "gpio-button", },
       { }
   };
   MODULE_DEVICE_TABLE(of, gpio_button_of_match);
   
   static struct platform_driver gpio_button_driver = {
       .driver = {
           .name = "gpio-button",
           .of_match_table = gpio_button_of_match,
       },
       .probe = gpio_button_probe,
       .remove = gpio_button_remove,
   };
   
   module_platform_driver(gpio_button_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("GPIO Button Driver");

Legacy GPIO API (Integer-Based)
================================

.. note:: This API is deprecated. Use descriptor-based API for new code.

.. code-block:: c

   #include <linux/gpio.h>
   
   /* Request GPIO */
   int gpio_num = 25;
   int ret = gpio_request(gpio_num, "my-gpio");
   if (ret < 0)
       return ret;
   
   /* Set direction */
   gpio_direction_output(gpio_num, 1);  // Output, initial high
   gpio_direction_input(gpio_num);       // Input
   
   /* Set/Get value */
   gpio_set_value(gpio_num, 1);
   int val = gpio_get_value(gpio_num);
   
   /* Free GPIO */
   gpio_free(gpio_num);

Best Practices
==============

1. **Use descriptor-based API** for new drivers
2. **Use devm_* functions** for automatic cleanup
3. **Handle optional GPIOs** gracefully
4. **Use _cansleep variants** when context allows sleeping
5. **Implement proper debouncing** for buttons
6. **Check GPIO validity** before use
7. **Document GPIO requirements** in device tree bindings
8. **Use pinctrl** for pin configuration
9. **Handle active-low** in device tree
10. **Test error paths**

Common Pitfalls
===============

1. **Using wrong API** (mixing legacy and descriptor)
2. **Not using _cansleep** with I2C/SPI GPIO expanders
3. **Forgetting to request GPIOs**
4. **Hardcoding GPIO numbers**
5. **Not handling -EPROBE_DEFER**
6. **Missing pull-up/down configuration**
7. **Incorrect active-low handling**

Debugging
=========

.. code-block:: bash

   # List all GPIOs
   cat /sys/kernel/debug/gpio
   
   # Export GPIO to userspace
   echo 25 > /sys/class/gpio/export
   echo out > /sys/class/gpio/gpio25/direction
   echo 1 > /sys/class/gpio/gpio25/value
   cat /sys/class/gpio/gpio25/value
   echo 25 > /sys/class/gpio/unexport
   
   # Check pinctrl state
   cat /sys/kernel/debug/pinctrl/*/pinmux-pins
   cat /sys/kernel/debug/pinctrl/*/pinconf-pins

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Interrupts.rst
- Linux_Device_Tree_Drivers.rst
- Linux_Input_Drivers.rst

References
==========

- Documentation/driver-api/gpio/
- Documentation/devicetree/bindings/gpio/
- Documentation/driver-api/pin-control.rst
- include/linux/gpio/consumer.h
