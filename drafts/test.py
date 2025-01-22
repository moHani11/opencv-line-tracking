import cv2 as cv
import numpy as np
import time
import serial
from linef import line, steering
from green import green
import math

# Initialize serial communication with Arduino


# Initialize Picamera2

start_time = time.time()

# Initialize variables
lspeed = 0
rspeed = 0
error = 0
ang = 0
GreenDetected = False
RedDetected = False

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    try:
        start_time = time.time()
        
        ret, image = cap.read()
        image = cv.resize(image, (465*2, 700))
        if not ret:
            print("Error: Could not read frame.")
            break

        # Define Region of Interest (ROI)
        height, width, _ = image.shape
        roi = image[height // 2 : height, :]  # Bottom half of the image

        # Detect black regions
        black = cv.inRange(image, (10, 10, 10), (80, 80, 80))
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
        # cv.putText(image, str(rspeed), (300, 500), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        # cv.putText(image, str(lspeed), (600, 500), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv.putText(image, f"anle: {ang}", (300, 500), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(image, f"error: {error}", (500, 500), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)



        # Send motor speed data to Arduino via serial communication

        # Display the image with detections
        cv.imshow('image', image)
        cv.imshow('Black', black)
        # cv.imshow('green', roi)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

cap.release()
cv.destroyAllWindows()