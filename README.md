# Line Tracking With Camera

This project is a practical example of how a robot uses a camera to "see" and navigate a path. It combines Python for image processing and Arduino for hardware control.

## Project Overview

The robot captures video from a PiCamera, identifies a black line on the ground, and uses that information to steer its motors. It can also recognize green markers to perform specific maneuvers like turning at intersections.

## Key Parts of the Code

### 1. Image Processing
The robot doesn't look at the whole picture. It focuses on a **Region of Interest (ROI)**—the bottom half of the image—where the line is closest.
* **Color Filtering:** It looks for black pixels (the line) and green pixels (the signs).
* **Contours:** It draws a boundary around the colors it finds to locate their center point.



### 2. Steering Logic
The robot calculates an **Error** value. If the line is in the center of the camera, the error is zero. If the line moves to the left or right, the robot calculates how much to adjust the motor speeds to bring the line back to the center.

### 3. Communication
Because the Raspberry Pi is good at vision but the Arduino is better at controlling motors, they talk to each other via a **Serial (USB) cable**. The Pi sends a string of text like "30 30" to tell the Arduino the speeds for the left and right wheels.



## Hardware Requirements
* Raspberry Pi with PiCamera
* Arduino (connected via USB)
* L298N or similar motor driver
* Robot chassis with DC motors

## Software Setup
You will need to install these Python libraries:
```bash
pip install opencv-python numpy pyserial
