============================
Linux Input Drivers Guide
============================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Input Device
------------------

.. code-block:: c

   #include <linux/input.h>
   
   struct input_dev *input;
   
   /* Allocate input device */
   input = devm_input_allocate_device(&pdev->dev);
   if (!input)
       return -ENOMEM;
   
   /* Setup device info */
   input->name = "My Input Device";
   input->phys = "mydev/input0";
   input->id.bustype = BUS_HOST;
   input->id.vendor = 0x0001;
   input->id.product = 0x0001;
   input->id.version = 0x0100;
   
   /* Set capabilities */
   input_set_capability(input, EV_KEY, BTN_0);
   input_set_capability(input, EV_KEY, KEY_A);
   
   /* Register */
   ret = input_register_device(input);
   
   /* Report events */
   input_report_key(input, KEY_A, 1);  // Press
   input_sync(input);
   input_report_key(input, KEY_A, 0);  // Release
   input_sync(input);

Polling Input Device
--------------------

.. code-block:: c

   static void mydev_poll(struct input_dev *input) {
       struct mydev_data *data = input_get_drvdata(input);
       
       /* Read hardware */
       u32 val = readl(data->regs + DATA_REG);
       
       /* Report events */
       input_event(input, EV_KEY, BTN_0, (val & BIT(0)) ? 1 : 0);
       input_sync(input);
   }
   
   /* Setup polling */
   ret = input_setup_polling(input, mydev_poll);
   if (ret)
       return ret;
   
   input_set_poll_interval(input, 100);  // 100ms

Input Subsystem Overview
=========================

Event Types
-----------

.. code-block:: c

   EV_SYN        // Synchronization events
   EV_KEY        // Key/button events
   EV_REL        // Relative axes (mouse)
   EV_ABS        // Absolute axes (touchscreen, joystick)
   EV_MSC        // Miscellaneous events
   EV_SW         // Switch events
   EV_LED        // LED events
   EV_SND        // Sound events
   EV_REP        // Repeat events
   EV_FF         // Force feedback

Common Event Codes
------------------

.. code-block:: c

   /* Keys */
   KEY_A, KEY_B, KEY_1, KEY_ESC, KEY_ENTER
   BTN_0, BTN_1, BTN_LEFT, BTN_RIGHT, BTN_MIDDLE
   
   /* Relative axes */
   REL_X, REL_Y, REL_Z, REL_WHEEL
   
   /* Absolute axes */
   ABS_X, ABS_Y, ABS_Z
   ABS_PRESSURE, ABS_MT_POSITION_X, ABS_MT_POSITION_Y

Creating Input Devices
=======================

Basic Setup
-----------

.. code-block:: c

   #include <linux/input.h>
   #include <linux/module.h>
   #include <linux/platform_device.h>
   
   struct mydev_data {
       struct input_dev *input;
       struct device *dev;
   };
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       struct input_dev *input;
       int ret;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       /* Allocate input device */
       input = devm_input_allocate_device(&pdev->dev);
       if (!input)
           return -ENOMEM;
       
       data->input = input;
       data->dev = &pdev->dev;
       platform_set_drvdata(pdev, data);
       input_set_drvdata(input, data);
       
       /* Setup device information */
       input->name = "My Input Device";
       input->phys = "mydev/input0";
       input->id.bustype = BUS_HOST;
       input->id.vendor = 0x0001;
       input->id.product = 0x0001;
       input->id.version = 0x0100;
       input->dev.parent = &pdev->dev;
       
       /* Set event capabilities */
       __set_bit(EV_KEY, input->evbit);
       __set_bit(KEY_A, input->keybit);
       __set_bit(KEY_B, input->keybit);
       
       /* Or use helper */
       input_set_capability(input, EV_KEY, KEY_C);
       
       /* Register device */
       ret = input_register_device(input);
       if (ret) {
           dev_err(&pdev->dev, "Failed to register input device\n");
           return ret;
       }
       
       dev_info(&pdev->dev, "Input device registered\n");
       return 0;
   }

Setting Capabilities
--------------------

.. code-block:: c

   /* Keyboard */
   __set_bit(EV_KEY, input->evbit);
   __set_bit(KEY_A, input->keybit);
   __set_bit(KEY_B, input->keybit);
   
   /* Mouse (relative) */
   __set_bit(EV_REL, input->evbit);
   __set_bit(REL_X, input->relbit);
   __set_bit(REL_Y, input->relbit);
   __set_bit(REL_WHEEL, input->relbit);
   
   /* Buttons */
   __set_bit(EV_KEY, input->evbit);
   __set_bit(BTN_LEFT, input->keybit);
   __set_bit(BTN_RIGHT, input->keybit);
   __set_bit(BTN_MIDDLE, input->keybit);
   
   /* Touchscreen (absolute) */
   __set_bit(EV_ABS, input->evbit);
   __set_bit(EV_KEY, input->evbit);
   __set_bit(BTN_TOUCH, input->keybit);
   
   /* Set absolute axis parameters */
   input_set_abs_params(input, ABS_X, 0, 4095, 0, 0);
   input_set_abs_params(input, ABS_Y, 0, 4095, 0, 0);
   // min, max, fuzz, flat

Reporting Events
================

Key Events
----------

.. code-block:: c

   /* Key press */
   input_report_key(input, KEY_A, 1);
   input_sync(input);
   
   /* Key release */
   input_report_key(input, KEY_A, 0);
   input_sync(input);
   
   /* Generic event */
   input_event(input, EV_KEY, KEY_B, 1);  // Press
   input_sync(input);

Relative Events (Mouse)
-----------------------

.. code-block:: c

   /* Mouse movement */
   input_report_rel(input, REL_X, dx);
   input_report_rel(input, REL_Y, dy);
   input_sync(input);
   
   /* Wheel scroll */
   input_report_rel(input, REL_WHEEL, wheel_delta);
   input_sync(input);

Absolute Events (Touchscreen)
------------------------------

.. code-block:: c

   /* Single touch */
   input_report_abs(input, ABS_X, x);
   input_report_abs(input, ABS_Y, y);
   input_report_key(input, BTN_TOUCH, 1);
   input_sync(input);
   
   /* Touch release */
   input_report_key(input, BTN_TOUCH, 0);
   input_sync(input);

Synchronization
---------------

.. code-block:: c

   /* Always call input_sync() after reporting events */
   input_report_key(input, KEY_A, 1);
   input_report_key(input, KEY_B, 1);
   input_sync(input);  // Mark end of event packet

Polling Input Devices
=====================

Setup Polling
-------------

.. code-block:: c

   static void mydev_poll(struct input_dev *input) {
       struct mydev_data *data = input_get_drvdata(input);
       u8 state;
       
       /* Read hardware state */
       state = mydev_read_state(data);
       
       /* Report button states */
       input_report_key(input, BTN_0, state & BIT(0));
       input_report_key(input, BTN_1, state & BIT(1));
       input_sync(input);
   }
   
   static int mydev_open(struct input_dev *input) {
       struct mydev_data *data = input_get_drvdata(input);
       
       /* Enable hardware */
       return mydev_hw_enable(data);
   }
   
   static void mydev_close(struct input_dev *input) {
       struct mydev_data *data = input_get_drvdata(input);
       
       /* Disable hardware */
       mydev_hw_disable(data);
   }
   
   static int mydev_setup_input(struct mydev_data *data) {
       struct input_dev *input = data->input;
       int ret;
       
       /* Set open/close callbacks */
       input->open = mydev_open;
       input->close = mydev_close;
       
       /* Setup polling */
       ret = input_setup_polling(input, mydev_poll);
       if (ret)
           return ret;
       
       /* Set poll interval */
       input_set_poll_interval(input, 50);  // 50ms (20Hz)
       input_set_min_poll_interval(input, 10);
       input_set_max_poll_interval(input, 200);
       
       return 0;
   }

Complete Driver Examples
=========================

Button Driver with IRQ
----------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/input.h>
   #include <linux/gpio/consumer.h>
   #include <linux/interrupt.h>
   #include <linux/of.h>
   
   struct button_data {
       struct input_dev *input;
       struct gpio_desc *gpio;
       int irq;
       unsigned int code;
       struct delayed_work work;
   };
   
   static void button_work(struct work_struct *work) {
       struct button_data *button = container_of(work,
                                                   struct button_data,
                                                   work.work);
       int state;
       
       state = gpiod_get_value_cansleep(button->gpio);
       
       input_report_key(button->input, button->code, state);
       input_sync(button->input);
   }
   
   static irqreturn_t button_irq(int irq, void *data) {
       struct button_data *button = data;
       
       /* Debounce: schedule work after 10ms */
       mod_delayed_work(system_wq, &button->work,
                         msecs_to_jiffies(10));
       
       return IRQ_HANDLED;
   }
   
   static int button_probe(struct platform_device *pdev) {
       struct button_data *button;
       struct device_node *np = pdev->dev.of_node;
       int ret;
       
       button = devm_kzalloc(&pdev->dev, sizeof(*button), GFP_KERNEL);
       if (!button)
           return -ENOMEM;
       
       /* Get GPIO */
       button->gpio = devm_gpiod_get(&pdev->dev, "button", GPIOD_IN);
       if (IS_ERR(button->gpio))
           return PTR_ERR(button->gpio);
       
       /* Get button code */
       ret = of_property_read_u32(np, "linux,code", &button->code);
       if (ret < 0)
           return ret;
       
       /* Allocate input device */
       button->input = devm_input_allocate_device(&pdev->dev);
       if (!button->input)
           return -ENOMEM;
       
       button->input->name = "GPIO Button";
       button->input->phys = "gpio-button/input0";
       button->input->id.bustype = BUS_HOST;
       
       input_set_capability(button->input, EV_KEY, button->code);
       
       ret = input_register_device(button->input);
       if (ret)
           return ret;
       
       /* Setup IRQ */
       button->irq = gpiod_to_irq(button->gpio);
       if (button->irq < 0)
           return button->irq;
       
       INIT_DELAYED_WORK(&button->work, button_work);
       
       ret = devm_request_irq(&pdev->dev, button->irq, button_irq,
                               IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                               "button", button);
       if (ret)
           return ret;
       
       platform_set_drvdata(pdev, button);
       dev_info(&pdev->dev, "Button registered (code=%u)\n", button->code);
       
       return 0;
   }
   
   static int button_remove(struct platform_device *pdev) {
       struct button_data *button = platform_get_drvdata(pdev);
       cancel_delayed_work_sync(&button->work);
       return 0;
   }
   
   static const struct of_device_id button_of_match[] = {
       { .compatible = "gpio-keys", },
       { }
   };
   MODULE_DEVICE_TABLE(of, button_of_match);
   
   static struct platform_driver button_driver = {
       .driver = {
           .name = "gpio-button",
           .of_match_table = button_of_match,
       },
       .probe = button_probe,
       .remove = button_remove,
   };
   
   module_platform_driver(button_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("GPIO Button Input Driver");

Polling Keyboard Matrix
------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/input.h>
   #include <linux/platform_device.h>
   #include <linux/gpio/consumer.h>
   
   #define ROWS 4
   #define COLS 4
   
   struct matrix_kbd_data {
       struct input_dev *input;
       struct gpio_descs *row_gpios;
       struct gpio_descs *col_gpios;
       unsigned int keymap[ROWS][COLS];
       bool keystates[ROWS][COLS];
   };
   
   static const unsigned int default_keymap[ROWS][COLS] = {
       { KEY_1, KEY_2, KEY_3, KEY_A },
       { KEY_4, KEY_5, KEY_6, KEY_B },
       { KEY_7, KEY_8, KEY_9, KEY_C },
       { KEY_LEFTSHIFT, KEY_0, KEY_DOT, KEY_ENTER },
   };
   
   static void matrix_kbd_scan(struct input_dev *input) {
       struct matrix_kbd_data *kbd = input_get_drvdata(input);
       int row, col;
       bool state;
       
       for (col = 0; col < COLS; col++) {
           /* Activate column */
           gpiod_set_value(kbd->col_gpios->desc[col], 1);
           udelay(10);
           
           for (row = 0; row < ROWS; row++) {
               /* Read row */
               state = gpiod_get_value(kbd->row_gpios->desc[row]);
               
               if (state != kbd->keystates[row][col]) {
                   kbd->keystates[row][col] = state;
                   input_report_key(input,
                                     kbd->keymap[row][col],
                                     state);
               }
           }
           
           /* Deactivate column */
           gpiod_set_value(kbd->col_gpios->desc[col], 0);
       }
       
       input_sync(input);
   }
   
   static int matrix_kbd_probe(struct platform_device *pdev) {
       struct matrix_kbd_data *kbd;
       struct input_dev *input;
       int ret, row, col;
       
       kbd = devm_kzalloc(&pdev->dev, sizeof(*kbd), GFP_KERNEL);
       if (!kbd)
           return -ENOMEM;
       
       /* Get GPIOs */
       kbd->row_gpios = devm_gpiod_get_array(&pdev->dev, "row", GPIOD_IN);
       if (IS_ERR(kbd->row_gpios))
           return PTR_ERR(kbd->row_gpios);
       
       kbd->col_gpios = devm_gpiod_get_array(&pdev->dev, "col", GPIOD_OUT_LOW);
       if (IS_ERR(kbd->col_gpios))
           return PTR_ERR(kbd->col_gpios);
       
       /* Allocate input device */
       input = devm_input_allocate_device(&pdev->dev);
       if (!input)
           return -ENOMEM;
       
       kbd->input = input;
       input_set_drvdata(input, kbd);
       
       input->name = "Matrix Keyboard";
       input->phys = "matrix-kbd/input0";
       input->id.bustype = BUS_HOST;
       
       /* Setup keymap */
       memcpy(kbd->keymap, default_keymap, sizeof(kbd->keymap));
       
       /* Set capabilities */
       __set_bit(EV_KEY, input->evbit);
       for (row = 0; row < ROWS; row++) {
           for (col = 0; col < COLS; col++) {
               __set_bit(kbd->keymap[row][col], input->keybit);
           }
       }
       
       /* Setup polling */
       ret = input_setup_polling(input, matrix_kbd_scan);
       if (ret)
           return ret;
       
       input_set_poll_interval(input, 20);  // 20ms
       
       /* Register */
       ret = input_register_device(input);
       if (ret)
           return ret;
       
       platform_set_drvdata(pdev, kbd);
       dev_info(&pdev->dev, "Matrix keyboard registered\n");
       
       return 0;
   }
   
   static const struct of_device_id matrix_kbd_of_match[] = {
       { .compatible = "matrix-keyboard", },
       { }
   };
   MODULE_DEVICE_TABLE(of, matrix_kbd_of_match);
   
   static struct platform_driver matrix_kbd_driver = {
       .driver = {
           .name = "matrix-keyboard",
           .of_match_table = matrix_kbd_of_match,
       },
       .probe = matrix_kbd_probe,
   };
   
   module_platform_driver(matrix_kbd_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Matrix Keyboard Driver");

Touchscreen Driver
------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/i2c.h>
   #include <linux/input.h>
   #include <linux/input/touchscreen.h>
   #include <linux/interrupt.h>
   
   struct touch_data {
       struct i2c_client *client;
       struct input_dev *input;
       struct touchscreen_properties prop;
       int irq;
   };
   
   static irqreturn_t touch_irq(int irq, void *data) {
       struct touch_data *ts = data;
       u8 buf[4];
       u16 x, y;
       bool touch;
       
       /* Read touch data from device */
       i2c_master_recv(ts->client, buf, sizeof(buf));
       
       touch = buf[0] & 0x01;
       x = (buf[1] << 4) | (buf[2] & 0x0F);
       y = (buf[3] << 4) | ((buf[2] >> 4) & 0x0F);
       
       /* Apply touchscreen properties */
       touchscreen_report_pos(ts->input, &ts->prop, x, y, true);
       
       input_report_key(ts->input, BTN_TOUCH, touch);
       input_sync(ts->input);
       
       return IRQ_HANDLED;
   }
   
   static int touch_probe(struct i2c_client *client) {
       struct touch_data *ts;
       int ret;
       
       ts = devm_kzalloc(&client->dev, sizeof(*ts), GFP_KERNEL);
       if (!ts)
           return -ENOMEM;
       
       ts->client = client;
       i2c_set_clientdata(client, ts);
       
       /* Allocate input device */
       ts->input = devm_input_allocate_device(&client->dev);
       if (!ts->input)
           return -ENOMEM;
       
       ts->input->name = "Touchscreen";
       ts->input->phys = "i2c-touchscreen/input0";
       ts->input->id.bustype = BUS_I2C;
       
       input_set_abs_params(ts->input, ABS_X, 0, 4095, 0, 0);
       input_set_abs_params(ts->input, ABS_Y, 0, 4095, 0, 0);
       
       input_set_capability(ts->input, EV_KEY, BTN_TOUCH);
       
       /* Parse touchscreen properties from DT */
       touchscreen_parse_properties(ts->input, false, &ts->prop);
       
       ret = input_register_device(ts->input);
       if (ret)
           return ret;
       
       /* Request IRQ */
       ts->irq = client->irq;
       ret = devm_request_threaded_irq(&client->dev, ts->irq,
                                        NULL, touch_irq,
                                        IRQF_ONESHOT,
                                        "touchscreen", ts);
       if (ret)
           return ret;
       
       dev_info(&client->dev, "Touchscreen initialized\n");
       return 0;
   }
   
   static const struct of_device_id touch_of_match[] = {
       { .compatible = "vendor,touchscreen", },
       { }
   };
   MODULE_DEVICE_TABLE(of, touch_of_match);
   
   static const struct i2c_device_id touch_id[] = {
       { "touchscreen", 0 },
       { }
   };
   MODULE_DEVICE_TABLE(i2c, touch_id);
   
   static struct i2c_driver touch_driver = {
       .driver = {
           .name = "touchscreen",
           .of_match_table = touch_of_match,
       },
       .probe_new = touch_probe,
       .id_table = touch_id,
   };
   
   module_i2c_driver(touch_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Touchscreen Driver");

Best Practices
==============

1. **Always call input_sync()** after event reports
2. **Use devm_input_allocate_device()** for managed cleanup
3. **Set proper device information** (name, phys, bustype)
4. **Implement open/close** for power management
5. **Use polling for simple devices**
6. **Debounce button inputs**
7. **Report all state changes**
8. **Handle autorepeat** for keyboards
9. **Test with evtest utility**
10. **Document event types** in driver

Common Pitfalls
===============

1. **Forgetting input_sync()**
2. **Not setting capabilities** before registering
3. **Incorrect absolute axis parameters**
4. **Missing debouncing**
5. **Wrong event types**
6. **Memory leaks** with non-devm functions

Debugging
=========

.. code-block:: bash

   # Test input device
   evtest /dev/input/event0
   
   # List input devices
   cat /proc/bus/input/devices
   
   # Monitor events
   libinput debug-events
   
   # Test from kernel
   cat /dev/input/event0 | hexdump -C

See Also
========

- Linux_GPIO_Pinctrl.rst
- Linux_Driver_IRQ_Handling.rst
- Linux_I2C_Drivers.rst
- Linux_Platform_Drivers.rst

References
==========

- Documentation/input/
- include/linux/input.h
- include/uapi/linux/input-event-codes.h
