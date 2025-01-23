import cv2 as cv
import numpy as np
import math

SET_X = 900

def line(contours_blk,image):
    if not contours_blk:
        return None, None, None, None
    
    max_contour=max(contours_blk,key=cv.contourArea)
    contour_area = cv.contourArea(max_contour)
    black_box = cv.minAreaRect(max_contour)
    (x_min, y_min), (w_min, h_min), ang = black_box
    centerx_blk = x_min + (w_min / 2)
    centery_blk = y_min + (h_min / 2)
    
    if w_min > h_min:
        ang = ang - 90
    ang = int(ang)
    box = cv.boxPoints(black_box)
    box = np.intp(box)
    setpoint = SET_X // 2
    error = int(x_min - setpoint)
    cv.drawContours(image, [box], 0, (0, 0, 255), 3)
    cv.putText(image, str(ang), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv.putText(image, str(error), (int(x_min), int(y_min)), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return error, ang, centerx_blk, centery_blk, contour_area

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



def is_black(roi, y, x):
    """Check if a pixel is black."""
    if 0 <= y < roi.shape[0] and 0 <= x < roi.shape[1]:
        b, g, r = roi[y, x]
        return (r, g, b) <= (150, 150, 150)
    return False


def draw_debug_shapes(roi, x_center, y_center, top, bottom, left, right):
    """Draw debug shapes on the ROI."""
    cv.circle(roi, (x_center, top), 4, (0, 255, 53), 3)
    cv.circle(roi, (x_center, bottom), 4, (255, 0, 255), 3)
    cv.circle(roi, (left, y_center), 4, (0, 255, 53), 3)
    cv.circle(roi, (right, y_center), 4, (255, 0, 255), 3)
    cv.circle(roi, (x_center, y_center), 4, (0, 0, 255), 3)

