from picamera2 import Picamera2, Preview
import cv2 as cv
import numpy as np
import time
import serial
from libcamera import controls
from linef import line, steering
from green import green
import math

# Initialize serial communication with Arduino
try:
    ser = serial.Serial('/dev/ttyACM1', 9600)
    time.sleep(2)  # Wait for the serial connection to initialize
    ser.reset_input_buffer()
except serial.SerialException as e:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)  # Wait for the serial connection to initialize
    ser.reset_input_buffer()
    print(f"Error opening serial port: {e}")

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (925, 860), "format": "RGB888"})
picam2.configure(camera_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()
start_time = time.time()

# Initialize variables
lspeed = 0
rspeed = 0
error = 0
ang = 0
GreenDetected = False
RedDetected = False

while True:
    try:
        start_time = time.time()
        image = picam2.capture_array()

        # Define Region of Interest (ROI)
        height, width, _ = image.shape
        roi = image[height // 2 : height, :]  # Bottom half of the image

        # Detect black regions
        black = cv.inRange(image, (10, 10, 10), (60, 60, 60))
        kernel = np.ones((3, 3), np.uint8)
        black = cv.erode(black, kernel, iterations=1)
        black = cv.dilate(black, kernel, iterations=10)
        contours_blk, _ = cv.findContours(black, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        # Adjusting speed based on line detection
        if len(contours_blk) > 0 and not RedDetected:
            error, ang, centerx_blk, centery_blk = line(contours_blk, image)
            if -20 < error + ang < 20:
                rspeed = 30
                lspeed = 30
            else:
                rspeed, lspeed = steering(20, error + ang)

        if len(contours_blk) == 0 and not RedDetected:
            if error is not None:
                rspeed, lspeed = steering(60, error + ang)

        # Initialize move instructions

        # Display FPS
        FPS = int(1 / (time.time() - start_time))
        cv.putText(image, f"FPS: {FPS}", (500, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(image, str(rspeed), (300, 500), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv.putText(image, str(lspeed), (600, 500), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        # Send motor speed data to Arduino via serial communication
        ser.write(f"{rspeed} {lspeed}\n".encode('utf-8'))

        # Display the image with detections
        cv.imshow('image', image)
        cv.imshow('Black', black)
        cv.imshow('green', roi)

        if cv.waitKey(1) & 0xFF == ord('q'):
            ser.write(f"{0} {0}\n".encode('utf-8'))
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

cv.destroyAllWindows()
picam2.stop()
