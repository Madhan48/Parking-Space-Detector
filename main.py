import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')
# Storing the video file into cap

with open('CarPark','rb') as f:
    poslist = pickle.load(f)
# Loading the positions from the pickle file

width,height = 107,48
# Width and height of the parking slot rectangle

def carparkingpos(imgpro):
    spaceCounter = 0

    for pos in poslist:
        x,y = pos
        imgcrop = imgpro[y:y+height,x:x+width]
        # Crops the parking slots
        #cv2.imshow(str(x*y), imgcrop)
        count = cv2.countNonZero(imgcrop)
        # stores the pixel count of each and every cropped image
        if count < 920:
            color = (0,255,0)
            thickness = 2
            spaceCounter +=1
        # If the pixel count is greater than threshold(900), spacecounter will be increased by 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        #creates a rectangle with color and thickness respect to that of the pixel count
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=thickness, colorR=color, offset=0)
        # Creating a rectangle with pixel count as text inside it
    cvzone.putTextRect(img,f'Available:{spaceCounter}/{len(poslist)}',(65,65),scale=2,
                           thickness=2,offset=15,colorR=(0,190,0))
    # Displays the Free spaces out of total parking slots


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
# Resetting the frame to 0 if it reaches the end
    success, img = cap.read()
    imggrey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Converting the image into greyscale and gaussian blur is applied
    imgblur = cv2.GaussianBlur(imggrey,(3,3),1)
    imgthreshold = cv2.adaptiveThreshold(imgblur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    #converting the image into binary image using adaptive thresholding
    imgMedian = cv2.medianBlur(imgthreshold, 5)
    # Applying median blur to remove noises in the binary image
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    # The thickness or edges of the object is increased by dilation. This helps us to differentiate the empty spaces from the occupied ones
    carparkingpos(imgDilate)
    # creating a function to crop the parking slots into seperate images to count the number of parking slots and free spaces

    #cv2.imshow('Blur Image', imgblur)
    #cv2.imshow('Dilated Image', imgDilate)
    #cv2.imshow('Median Image', imgMedian)
    #cv2.imshow('Thres Image', imgthreshold)
    cv2.imshow('Image', img)

    cv2.waitKey(10)