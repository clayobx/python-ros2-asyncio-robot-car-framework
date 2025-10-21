# python-ros2-asyncio-robot-car-framework
Python/Micropython framework for ROS2/asyncio robot car

This is a project I started about 6 years ago to create a framework and working examples of controlling robot cars based on either Raspberry Pi 3/4/5/zero, ESP32 and Raspberry Pi Pico. The base code runs on either full Python or on MicroPython with minimal changes.  I use RO2 for message communications using the ROS2-Bridge-Suite.  The Bridge Suite allows either platform (RPi, ESP32/Pico) to communicate with ROS2 nodes without installing ROS2 on the actual devices.

I initially tried pure ROS2 development but I just don't understand the development/build/debug environment of ROS2. I like the modern dev methods of VS Code on Windows/Linux (local and remote) and Thonny for ESP32/Pico devices. Seems to have a real complicated build process and is there a simple way to debug?   

So, my framework.  The framework uses Python/MicroPython Asyncio to break the code into tasks that communicate via messages over topics.  The framework allows for internal messaging or via the ROS2 bridge to external devices that are on the WiFi network.

My development environment is at least low cost as in free as far as software.  
  1. I use VS Code on Windows 11 for local and remote access to Ubuntu and RaspberryPi OS.
  2. For ESP32/Raspberry Pi Pico, I use Thonny either via USB or WebREPL
  3. For ROS2, I decided to use a spare Windows 11 machine to run VMware Workstation Pro 17.  I found the native support for Ubuntu on Hyper-V on desktop Windows 11 to be lacking in video resolution support.  VMWare works very well with Ubuntu. If anyone has a work around for Hyper-V, I would like to know as I prefer to use as minimal extra software as possible.
  4. On VMWare, I run Ubuntu 24.04 Desktop and then install ROS2 and the ROS2Bridge-Suite.  This handles the ROS2 side and by using the desktop, I can still use the visual tools of ROS2.
  5. To access my remote machines, Windows or Linux, I use MobaXterm.  Supports RDP, SSH and other protocols
  6. To easily move files to/from Windows to/from Linux, I use WinSCP.  Just lazy and makes it ease to to backup/restore files to/from my OneDrive account.
So I have a main dev machine which is a cheap Windows 11 laptop and for ROS2, a Mini-PC running Windows 11/VMWare/Ubuntu/ROS2  

I have created multiple versions of the hardware with minimal code changes.  Hardware related code is isolated from the framework for easy porting to other hardware.  Currently it supports these combintation: [details if anyone wants]

  1. ESP32 with I2C 4 DC motor controller (4WD), TT motors with speed disks and sensors
  2. Pico 2W with direct 4 DC motor controller (4WD), TT motors with builtin hall encoders
  3. ESP32 with L298N Motor Driver Controller (2WD), DC metal gear motors with hall encoders
  4. ESP32 with Yahboom I2C 4 DC Motor Controller (4WD), TT motors with builtin hall encoders
  5. RPi 4B with I2C 4 DC Motor Controller (4WD), TT motors with speed disks and sensors
  6. RPI 4B with Yahboom I2C 4 DC Motor Controller (4WD), DC metal gear motors with hall encoders
  7. Pico 2W with I2C 4 DC motor Controller (4WD), TT motors with speed disks and sensors

Other hardware with supported code:
  1. SR-04 Ultrasonic sensor
  2. MPU9250 gyro/accel/mag sensor
  3. TF-Luna Lidar
  4. I2C LED display
  5. and other...

In addition to the actual robot cars, I have used the framework to implement a few other devices that cooperate with the robot cars.
  1. ESP32 based 320x240 2.8" display.  This is used as a local display on the robot car.  Because it uses the framework, the robot car can publish messages on a topic that the ESP32 based display will recieve and display.  I used Peter Hinch's micropython-nano-gui.  The boards I use were supposed to be ILI9341 based but were actually 7789 based.  Took awhile to figure this out but i got it to work.  The ESP32 is a simple WROOM without PSRAM so memory is limited.  I used the 4-bit driver (16 colors) to derive a 2-bit driver (4 colors) and that cut the memory requirement for the framebuffer in half. With my framework, I have 44% free. I decided that 4 colors were enough for a simple disply on the actual robot care itself, basically displaying verious status and logs. I also modified the driver to support direct blitting a GUI element without fully redisplaying the entire screen.  Much faster display updates and half the memory, winner!  The display board only requires 2 wires to connect to any device, 5V and GND, as the display integrates into the ROS2 bridge/my framework.  Messages are sent to the display using WIFI.  Is this an overkill for a simple display?  They only cost $15 and use basically no resources or any code from the host device. I also implemented touch code to allow for buttons to send messages from the display to other devices. 
  2. I have a Python/QT (actually PySide6) application that runs on full Python.  This is the controller for the robot car.  It has a touch GUI and yet again, uses the framework to communicate with the robot car or other devices. This runs on Windows or Linux.
  3. I have another version of the above that uses a wireless game controller for sending messages to the robot car (no GUI) using pygame.  Real fun to use to drive around.
  4. I wanted to create a small, handheld version of the controller and started looking at hardware options.  To build a Raspberry Pi with a display would cost close to $200 with Raspberry Pi 4, case, display/touch, battery and power management.  Heck, you can buy a laptop for the same price.  So, I started thinking of an alternative (I get dangerous when I start thinking) and came up with this.  What is the cheapest device that has a fast processor, decent amout of memory (>=2GB), touch screen and battery powered?  An Android Tablet! I did a bunch of research and found this app, Termux/proot-distro, that allows a Android device to install a linux distribution without having root on the Android device.  I purchased a 8" Android 15 tablet for $38 with 4 GB of memeory and gave it a try.  Takes many steps, downloading a couple of APKs to an SD card and following a sequence of many commands, it works!.  I tried multiple versions of Linux with different levels of success.  My goal is to be able to use VS Code Remote to access the Android/termux device to develop my code on the device just like i do with all my other Liunx based devices.  I found that using proot-distro, only Ubuntu worked with VS Code remotely. Yeh! It works.  I installed QT and PySide6, all my code from the previous project, and boom, it also works!  Same code.  This is probably another project if anyone is interested.  You do not need to use my code but if you want a cheap Ubuntu 24.04 machine on the cheap, this is how to do it.
