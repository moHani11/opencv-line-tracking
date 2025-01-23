import cv2 as cv
import numpy as np
 
def green(roi,image, shift_down):
    # Initialize detection status
    GreenDetected = False

    # Convert to HSV format
    kernel = np.ones((3, 3), np.uint8)
    dilate_kernel = np.ones((7, 7), np.uint8)
    Green_HSV = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    Lower_Green = np.array([20, 70, 70])
    Upper_Green = np.array([80, 250, 255])
    green_mask = cv.inRange(Green_HSV, Lower_Green, Upper_Green)
    green_mask = cv.erode(green_mask, kernel, iterations=2)
    green_mask = cv.dilate(green_mask, dilate_kernel, iterations=6)

    # Find contours in the green mask
    contours, _ = cv.findContours(green_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Initialize movement instructions
    move_instructions = {"forward": False, "right": False, "left": False, "turn": False}

     # Check for the first contour and process it
    if len(contours) >= 1:
        GreenDetected = True
        x1, y1, w1, h1 = cv.boundingRect(contours[0])
        cv.rectangle(roi, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)


        x1_center = x1 + w1 // 2
        y1_center = y1 + h1 // 2

        # Define regions for checking black color
        left1 = x1_center - w1 // 2 - 10
        right1 = x1_center + w1 // 2 + 10
        top1 = y1_center - h1 // 2 - 10
        bottom1 = y1_center + h1 // 2 + 10

        # Process pixel colors around the first contour
        top1_black = is_black(image, top1 + shift_down, x1_center)
        bottom1_black = is_black(image, bottom1 + shift_down, x1_center)
        right1_black = is_black(image, y1_center + shift_down, right1)
        left1_black = is_black(image, y1_center + shift_down, left1)

        # Draw additional shapes
        draw_debug_shapes(roi, x1_center, y1_center, top1, bottom1, left1, right1)

    # Check for the second contour and process it
    if len(contours) >= 2:
        GreenDetected = True
        x2, y2, w2, h2 = cv.boundingRect(contours[1])
        cv.rectangle(roi, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)

        x2_center = x2 + w2 // 2
        y2_center = y2 + h2 // 2

        # Define regions for checking black color
        left2 = x2_center - w2 // 2 - 10
        right2 = x2_center + w2 // 2 + 10
        top2 = y2_center - h2 // 2 - 10
        bottom2 = y2_center + h2 // 2 + 10

        # Process pixel colors around the second contour
        top2_black = is_black(image, top2 + shift_down, x2_center)
        bottom2_black = is_black(image, bottom2 + shift_down, x2_center)
        right2_black = is_black(image, y2_center + shift_down, right2)
        left2_black = is_black(image, y2_center + shift_down, left2)

        # Draw additional shapes
        draw_debug_shapes(roi, x2_center, y2_center, top2, bottom2, left2, right2)

    # Decision-making logic
    if len(contours) >= 2 and top1_black and top2_black:
        move_instructions["turn"] = True
    elif len(contours) >= 1:
        if top1_black:
            move_instructions["right"] = left1_black and not right1_black
            move_instructions["left"] = right1_black and not left1_black
        if len(contours) >= 2 and top2_black:
            move_instructions["right"] |= left2_black and not right2_black
            move_instructions["left"] |= right2_black and not left2_black
    if not any(move_instructions.values()):
        move_instructions["forward"] = True

    return (move_instructions["forward"], move_instructions["right"], 
            move_instructions["left"], move_instructions["turn"], roi,green_mask,GreenDetected)


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
