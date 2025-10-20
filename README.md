# python-ros2-asyncio-robot-car-framework
Python/Micropython framework for ROS2/asyncio robot car

This is a project I started about 6 years ago to create a framework and working examples of controlling robot cars based on either Raspberry Pi 3/4/5/zero, ESP32 and Raspberry Pi Pico. The base code runs on either full Python or on MicroPython with minimal changes.  I use RO2 for message communications using the ROS2-Bridge-Suite.  The Bridge Suite allows either platform (RPi, ESP32/Pico) to communicate with ROS2 nodes without installing ROS2 on the actual devices.

The framework uses Asyncio to break the code into tasks that communicate via messages over topics.  The framework allows for internal messaging (messages stay internal) or via the ROS2 bridge to external devices that are on the WiFi network.

I have created multiple versions of the hardware with minimal code changes.  Hardware related code is isolated from the framework for easy porting to other hardware.  Currently it supports these combintation:

  1. ESP32 with I2C 4 DC motor controller, TT motors with speed disks and sensors
  2. Pico 2W with direct 4 DC motor controller, TT motors with builtin hall encoders
  3. ESP32 with L298N Motor Driver Controller (2WD), DC metal gear motors with hall encoders
  4. ESP32 with Yahboom I2C 4 DC Motor Controller, TT motors with builtin hall encoders
  5. RPi 4B with I2C 4 DC Motor Controller, TT motors with speed disks and sensors
  6. RPI 4B with Yahboom I2C 4 DC Motor Controller, DC metal gear motors with hall encoders
  7. Pico 2W with I2C 4 DC motor Controller, TT motors with speed disks and sensors
     

  9.   
