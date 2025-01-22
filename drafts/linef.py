import cv2 as cv
import numpy as np
import math

def line(contours_blk,image):
    if not contours_blk:
        return None, None, None, None
    max_contour=max(contours_blk,key=cv.contourArea)
    black_box = cv.minAreaRect(max_contour)
    (x_min, y_min), (w_min, h_min), ang = black_box
    centerx_blk = x_min + (w_min / 2)
    centery_blk = y_min + (h_min / 2)
    
    if w_min > h_min:
        ang = ang - 90
    ang = int(ang)
    box = cv.boxPoints(black_box)
    box = np.intp(box)
    setpoint = 465
    error = int(x_min - setpoint)
    cv.drawContours(image, [box], 0, (0, 0, 255), 3)
    cv.putText(image, str(ang), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv.putText(image, str(error), (int(x_min), int(y_min)), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return error, ang, centerx_blk, centery_blk

def steering(speed,steer):
    
#     steer = 0.4 *steer

    old_range = (-465, 465)
    new_range = (-130, 130)
    x = steer
     
    steer = map_range(x, old_range[0], old_range[1], new_range[0], new_range[1])
          

    
    lspeeed=(speed-(steer))
    rspeeed=(speed+(steer))
    
    if 0<lspeeed<20:
        lspeeed=20
        
    if 0<rspeeed<20:
        rspeeed=20


        
    lspeed=lspeeed
    rspeed=rspeeed
     
    return rspeed,lspeed


def map_range(x, old_min, old_max, new_min, new_max):
    return ((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


