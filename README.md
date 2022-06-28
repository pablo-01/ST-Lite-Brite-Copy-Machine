# ST-Lite-Brite-Copy-Machine

Sample of the program running: https://youtu.be/OHX3_yAcVGU

External libraries:
- numpy
- cv2
- pyautogui

Files included:
- reference.png (solved reference image)
- color_ref (color thresholds reference)  

Overview:  
    This program uses OpenCV to detect position and color of the
    circles from the solved Lite Brite board and then paints them  
    on the empty [iamhellsmaster.com](https://iamhellsmaster.com/) board.  

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
    
