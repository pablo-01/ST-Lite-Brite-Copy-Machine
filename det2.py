import numpy as np
import cv2 as cv
import pyautogui as p 
import time


"""
Overview:
    This program uses OpenCV to detects position and color of the 
    circles from the solved Lite Brite board and then paints them 
    on the empty iamhellsmaster.com board.

    Solved image has to be aligned with the empty board manually. 
    (automatic alignment is not implemented yet but I'm testing some solutions SIFT/RANSAC).

    PyAutoGUI is used to move the mouse to the center of the circles and make clicks.

    Visual sample: https://youtu.be/OHX3_yAcVGU 

    What happens is:
    1. align images (manually for now) then run the program
    It will prompt you to move mouse to various positions. 
     - move mouse to: 
         - top left corner
         - top right corner
    3. calculates bottom left and bottom right corners of target area
    4. converts coordinates to x,y,w,h of target area
    5. Prompts to move mouse and record coordinates for each color
    6. Prompts to overlay target area with template image:
        - color detection happens here
        - circle detection happens here
    7. Prompts to minimize template window
    8. Starts painting circles for each color until all colors are painted 
    
"""

# board coordinates
class Board:
    x = 0
    y = 0
    w = 0
    h = 0

# color threshold values
class ColorThresholds:
    # define range of colors in HSV
    # hue, saturation, value (brightness)

    # BLUE
    lower_blue = np.array([90,50,200])
    upper_blue = np.array([120,255,255])

    # RED
    lower_red = np.array([0,50,200])
    upper_red = np.array([10,255,255])

    # GREEN
    lower_green = np.array([35,50,200])
    upper_green = np.array([80,255,255])

    # YELLOW
    lower_yellow = np.array([20,50,200])
    upper_yellow = np.array([30,255,255])

    # ORANGE
    lower_orange = np.array([10,50,200])
    upper_orange = np.array([20,255,255])

    # WHITE
    sensitivity = 20
    lower_white = np.array([0,0,255-sensitivity])
    upper_white = np.array([180,sensitivity,255])


### 1. Calibration ###

# board area
# returns: Board object with x,y,w,h coordinates
def calculate_game_area():
    print('#' * 30, "\n")
    print("STARTING CALIBRATION", "\n")
    print('#' * 30, "\n")
    
    # game board area prompt
    area_t_left = "top left"
    area_t_right = "top right"
    corners = [area_t_left, area_t_right]

    # top left / top right coordinates
    t_left = 0, 0
    t_right = 0, 0

    # top left/right are used to calculate bottom left/right
    coords = [t_left, t_right]

    # prompt to move mouse to 2 corners of target area 
    # record coordinates
    for i in range(len(corners)):
        print("Move to " + corners[i])
        time.sleep(6)
        coords[i] = p.position()
        print(coords[i], "\n")

    t_left = coords[0]
    t_right = coords[1]

    board = Board()
    # set x,y,w,h of target area
    board.x = t_left[0]
    board.y = t_left[1]
    board.w = t_right[0] - t_left[0]
    board.h = t_right[0] - t_left[0]

    return board

# returns dictionary with coordinates of each color box
def get_color_box_coord():  
    red_pos = [0,0]
    orange_pos = [0,0]
    yellow_pos = [0,0]
    blue_pos = [0,0]
    green_pos = [0,0]
    white_pos = [0,0]

    color_pos = { "red": red_pos, 
                    "orange": orange_pos, 
                    "yellow": yellow_pos,
                    "blue": blue_pos,
                    "green": green_pos,
                    "white": white_pos }

    # prompt to move mouse to each color of the pegs box
    # record coordinates
    for color in color_pos:
        print("Move to " + color)
        time.sleep(6)
        color_pos[color][0] = p.position()
        print(color_pos[color][0], "\n")

    return color_pos



### Color and Circle Detection ###

def detect_circles(board, color_box_coord):
    # prompt user to open the template image (must match position)
    print("\n\n\n")
    print("Overlay game board with template image...", "\n")
    time.sleep(6)

    # take a screenshot of the screen
    p.screenshot('screen.png')
    time.sleep(2)

    # read in the screenshot and mask it to the game-board area
    src_img = cv.imread('screen.png')

    # mask out the parts of the screen that aren't the game 
    # while keeping the parts that are the game unchanged
    mask = np.zeros(src_img.shape, dtype=np.uint8)
    mask[board.y:board.y+board.h, board.x:board.x+board.w] = src_img[board.y:board.y+board.h, 
                                                                    board.x:board.x+board.w]
    # save the masked image to inspect it
    #cv.imwrite('masked_game_board.png', mask)

    # convert the masked image to hsv color space
    hsv = cv.cvtColor(mask, cv.COLOR_BGR2HSV)

    c = ColorThresholds()

    # Threshold and bitwise_and to get the mask
    # for each color
    mask_blue = cv.inRange(hsv, c.lower_blue, c.upper_blue)
    res_blue = cv.bitwise_and(mask, mask, mask= mask_blue)

    mask_red = cv.inRange(hsv, c.lower_red, c.upper_red)
    res_red = cv.bitwise_and(mask, mask, mask= mask_red)

    mask_green = cv.inRange(hsv, c.lower_green, c.upper_green)
    res_green = cv.bitwise_and(mask, mask, mask= mask_green)

    mask_yellow = cv.inRange(hsv, c.lower_yellow, c.upper_yellow)
    res_yellow = cv.bitwise_and(mask, mask, mask= mask_yellow)


    mask_orange = cv.inRange(hsv, c.lower_orange, c.upper_orange)
    res_orange = cv.bitwise_and(mask, mask, mask= mask_orange)


    mask_white = cv.inRange(hsv, c.lower_white, c.upper_white)
    res_white = cv.bitwise_and(mask, mask, mask= mask_white)


    color_masks = { "blue": [res_blue, mask_blue], 
                    "red": [res_red, mask_red],
                    "green": [res_green, mask_green], 
                    "yellow": [res_yellow, mask_yellow], 
                    "orange": [res_orange, mask_orange], 
                    "white": [res_white, mask_white] }
    print("MINIMIZE TEMPLATE WINDOW", ", waiting 5 seconds...", "\n")
    time.sleep(5)    
    return color_masks



# main (TODO: refactor)
board = calculate_game_area()
color_box_pos = get_color_box_coord()
color_masks = detect_circles(board, color_box_pos)


for color in color_masks:
    print("#" * 30, "\n")
    print("Selecting: " + color, "\n")
    print("#" * 30, "\n")

    # click on color selector
    p.moveTo(color_box_pos[color][0][0], color_box_pos[color][0][1])
    p.click()
    
    selected_res = color_masks[color][0]
    selected_mask = color_masks[color][1] 

    # convert
    color_img = cv.cvtColor(selected_res , cv.COLOR_BGR2GRAY)

    # use HoughCircles to find the circles on the resulting image
    circles_img = cv.HoughCircles(selected_mask,cv.HOUGH_GRADIENT,1,20,
                                param1=20,param2=10,minRadius=0,maxRadius=27)


    # if no circles found 
    # break out of current iteration 
    # and go to the next color
    if circles_img is None:
        print("No circles found for " + color,)
        print("Moving on to next color...", "\n")
        continue

    # number of circles found
    n_of_circles = circles_img.shape[1]

    circles_img = np.uint16(np.around(circles_img))

    # draw circles
    for i in circles_img[0,:]:
        cv.circle(color_img,(i[0],i[1]),i[2],(0,255,0),2)
        cv.circle(color_img,(i[0],i[1]),2,(0,0,255),3)

    print("Found " + str(n_of_circles) + " " +  color + " circles.", "\n")

    # use coordinates of the center of the circles to move the mouse to the center of the circle
    for i in circles_img[0,:]:
        p.moveTo(i[0],i[1])
        p.click()

    print("All " + color + " circles have been painted.", "\n")
    print("Moving to next color...", "\n")
    time.sleep(1)
    