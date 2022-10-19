import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    #live feed
    _, frame = cap.read()
    
    frame_color = frame

    """ ADJUSTING RESOLUTION AND FILTERING """
    #resizing
    #frame = cv2.resize(frame, (1366, 768))

    #downsampling two times - Gaussian pyramid
    for i in range(2):
        frame = cv2.pyrDown(frame)

    #applying bilateralFilters --> repeated application than one largefilter
    for i in range(50):
        frame = cv2.bilateralFilter(frame, 9, 9, 7)

    #upscaling to original Size
    for i in range(2):
        frame = cv2.pyrUp(frame)

    """ COLOUR CONVERSION AND BLURRING """
    #grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    #median blur
    frame = cv2.medianBlur(frame, 3)

    """ EDGE DETECTION AND ENHANCEMENT """
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

    """ CONVERT TO COLOR, BIT-ANDED WITH COLOR IMAGE"""
    (x, y, z) = frame_color.shape
    frame = cv2.resize(frame, (y, x))
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    frame = cv2.bitwise_and(frame_color, frame)

    cv2.imshow('Video Feed', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

