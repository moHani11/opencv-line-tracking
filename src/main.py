from picamera2 import Picamera2, Preview
import cv2 as cv
import numpy as np
import time
import serial
from libcamera import controls
from linef import line, steering
import math
from green import green

# Initialize variables
lspeed = 0
rspeed = 0
error = 0
ang = 0
GreenDetected = False
RedDetected = False


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
camera_config = picam2.create_still_configuration(main={"size": (900, 860), "format": "RGB888"})
picam2.configure(camera_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()
start_time = time.time()


while True:
    try:
        start_time = time.time()
        image = picam2.capture_array()

        # Define Region of Interest (ROI)
        height, width, _ = image.shape
        roi = image[height // 2 + 100: height, :]  # Bottom half of the image

        # Detect black regions
        black = cv.inRange(image, (0, 0, 0), (120, 100, 120))
        kernel = np.ones((3, 3), np.uint8)
        black = cv.erode(black, kernel, iterations=2)
        black = cv.dilate(black, kernel, iterations=16)
        contours_blk, _ = cv.findContours(black, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        # Adjusting speed based on line detection
        if len(contours_blk) > 0 and not RedDetected:
            error, ang, centerx_blk, centery_blk,contour_area = line(contours_blk, image)
#             print(contour_area)
            lspeed = 0
            rspeed = 0
#             if contour_area>400000:
#                 ser.write(f"{50} {50}\n".encode('utf-8'))               
#                 time.sleep(0.1)
# 
#             if contour_area>200000:
#                 ser.write(f"{0} {0}\n".encode('utf-8'))
            
            if -20 < error + ang < 20:
                rspeed = 30
                lspeed = 30
            else:
                rspeed, lspeed = steering(20, error*1.2 + ang*2)

        if len(contours_blk) == 0 and not RedDetected:
            if error is not None:
                rspeed, lspeed = steering(70, error + ang*0)

        # Initialize move instructions
        move_instructions = {"forward": False, "right": False, "left": False, "turn": False}
        
        # Detect green objects in the ROI and update move instructions
        forward, right, left, turn, roi,green_mask,GreenDetected = green(roi, image, height //2 +100)
        move_instructions["forward"] = forward
        move_instructions["right"] = right
        move_instructions["left"] = left
        move_instructions["turn"] = turn

        if GreenDetected: 
            if move_instructions["right"]:
                cv.putText(image, "Turn Right", (600, 600), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                
                rspeed = 0
                lspeed = 50
                ser.write(f"{lspeed} {rspeed}\n".encode('utf-8'))
                print("Turn Right")
#                 time.sleep(0.8)
            elif move_instructions["left"]:
                rspeed = 50
                lspeed = 0
                ser.write(f"{lspeed} {rspeed}\n".encode('utf-8'))
                print("Turn Left")
#                 time.sleep(0.8)
            elif move_instructions["turn"]:
                cv.putText(image, "Return", (600, 600), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                print("Return")
                rspeed = 0
                lspeed = 0
                ser.write(f"{lspeed} {rspeed}\n".encode('utf-8'))
                print("Return")
#                 time.sleep(0.8)
                
            else:
                cv.putText(image, "-", (600, 600), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                print("--------")

        FPS = int(1 / (time.time() - start_time))
        cv.putText(image, f"FPS: {FPS}", (500, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(image, str(rspeed), (300, 500), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv.putText(image, str(lspeed), (600, 500), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        

        # Send motor speed data to Arduino via serial communication
        ser.write(f"{rspeed} {lspeed}\n".encode('utf-8'))
        # Display the image with detections
        cv.imshow('image', image)
        cv.imshow('black', black)
        cv.imshow('green',green_mask)

        if cv.waitKey(1) & 0xFF == ord('q'):
            ser.write(f"{0} {0}\n".encode('utf-8'))
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

cv.destroyAllWindows()
picam2.stop()
