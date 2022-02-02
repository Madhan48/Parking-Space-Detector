# Free Parking space detector
## Finding and marking the Positions of the parking spaces
#Importing necessary libraries
import cv2
import pickle

# If the pickle file has poslist,then that poslist is loaded or else an empty poslist is created
try:
    with open('CarPark', 'rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []
width,height = 107,48

def click(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    #If left mouse click occurs, x,y positions of the click is appended in poslist
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(poslist):
            x1,y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                poslist.pop(i)
    # If the cursor is placed inside the rectangle and right click that particular iteration will be removed or deleted
    with open('CarPark', 'wb') as f:
        pickle.dump(poslist,f)
    # CarPark pickle file is created and the poslist is stored in the pickle file

while True:
    img = cv2.imread('carParkImg.png')
    # Storing the image into img variable
    #cv2.rectangle(img,(50,192),(157,240),(100,0,255),2)
    # Identifies the size of the single parking slot
    for i in poslist:
        cv2.rectangle(img, (i),(i[0]+width,i[1]+height),(100,0,255),2)
    #creating a for loop in order to create a rectangle W.R.T the position of the mouse click stored in poslist
    cv2.imshow('Image',img)
    #Displays the image with the rectangle
    cv2.setMouseCallback("Image",click)
    # Detects the mouse click and click user defined function is called whenever the mouse click occurs.
    cv2.waitKey(1)
