import cv2
import mediapipe as mp
import time
import math


dist0 = 0
def openClose(frame, handLms, w, h):
    global dist0
    distcurr=utility(handLms, w, h)
    if(frame == 1):
        dist0 = distcurr
    if((frame%4 +1) == 1 and abs(handLms.landmark[mp.solutions.hands.HandLandmark.WRIST].x*w - w/2)<w/2 and abs(handLms.landmark[mp.solutions.hands.HandLandmark.WRIST].y*h - h/2)<h/2):
        change = dist0- distcurr
        dist = utility(handLms, w, h)
        # print(change)
        if(change>+50):
            print("Hand is closing ")
            return 1
        elif(change<-50):
            print("Hand is opening ")
            return 2
    return 0
    

time_left = time.time()
time_right = time.time()
left_taken = False
right_taken = False
def sliderHori(handLms, frame, w=1):
    global time_left
    global time_right
    global left_taken
    global right_taken
    for id, lm in enumerate(handLms.landmark):
        if(id==0):
            cx = int((lm.x)*w)
            if(cx < 80 and left_taken== False):
                time_left = time.time()
                left_taken = True
        
            if(cx > 200 and right_taken == False):
                time_right = time.time()
                right_taken = True
    if(time_left<time_right and right_taken and left_taken):
        print("Hand is moving LEFT")
        return 3
    if(time_right<time_left and right_taken and left_taken):
        print("Hand is moving RIGHT")
        return 4
    return 0

time_up = time.time()
time_down = time.time()
up_taken = False
down_taken = False
def sliderVer(handLms, frame, h=1):
    global time_up
    global time_down
    global up_taken
    global down_taken
    for id, lm in enumerate(handLms.landmark):
        if(id==0):
            cy = int((lm.y)*h)  
            if(cy < 90 and up_taken== False):
                time_up = time.time()
                up_taken = True
        
            if(cy > 180 and down_taken == False):
                time_down = time.time()
                down_taken = True
        # print("Y pos is ", cy)
    if(time_down<time_up and down_taken and up_taken):
        print("Hand is moving UP")
        return 5
    if(time_up<time_down and down_taken and up_taken):
        print("Hand is moving DOWN")
        return 6
    return 0


def eulcidian_distance(X, Y, x_0, y_0):
    sumX = 0
    sumY = 0
    for x in X:
        sumX = sumX+(x-x_0)**2
    for y in Y:
        sumY = sumY+(y-y_0)**2
    return math.sqrt(sumX+sumY)


def utility(handLms, w, h):
    dist = 0
    X = []
    Y = []
    x_0 = 0
    y_0 = 0
    for id, lm in enumerate(handLms.landmark):
        #print(id,lm)
        # Height, width and channel of image
        h, w, c = img.shape
        # X and Y coordinate 
        # their values in decimal so 
        # we have to convert into pixel
        cx, cy = int((lm.x)*w),int((lm.y)*h)
        if id==0:
            x_0 = cx
            y_0 = cy
        elif (id%4)==0:
            X.append(cx)
            Y.append(cy)
    return (eulcidian_distance(X, Y, x_0, y_0))


# Create Video object
cap = cv2.VideoCapture(0)
# Formality we have to write before start
# using this model 
mpHands = mp.solutions.hands
# Creating an object from class Hands
hands = mpHands.Hands(max_num_hands=1)
# creating an object to draw hand landmarks
mpDraw = mp.solutions.drawing_utils
# Previous time for frame rate
pTime = 0
# Current time for frame rate
cTime = 0
frame = 0
time_before_gesture = 0
time_vol = 0
while True:
    # Getting our Frame
    if((time.time() - time_before_gesture)>2.000):
        time_before_gesture = 0
    if((time.time() - time_vol)>0.1):
        time_vol = 0
    success, img = cap.read()
    img = cv2.resize(img,(500,500))
    # Convert image into RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Calling the hands object to the getting results
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    # Checking something is detected or not
    if results.multi_hand_landmarks :
        # Extracting the multiple hands 
        # Go through each hand
        for handLms in results.multi_hand_landmarks:
            frame = (frame+1)%31
            # Getting id(index number) and landmark of each hand
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                # Height, width and channel of image
                h, w, c = img.shape
                # X and Y coordinate 
                # their values in decimal so 
                # we have to convert into pixel
                cx, cy = int(lm.x*w),int(lm.y*h)
                #print(id, cx, cy)
                if id ==4:
                    cv2.circle(img, (cx, cy), 7, (255,0,255), cv2.FILLED)
            # Draw the landmarks and line of the each hands
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # openClose(frame, handLms)
            if(time_before_gesture == 0):
                hor = sliderHori(handLms, frame, w)
            if(time_vol == 0):
                ver = sliderVer(handLms, frame, h)
                # op = openClose(frame, handLms, w, h)
            if(hor>0):
                hor = 0
                time_before_gesture = time.time()
            if(ver>0):
                ver = 0
                time_vol = time.time()
            # if(op>0):
            #     op = 0
            #     time_before_gesture = time.time()
    else:
        left_taken = False
        right_taken = False
        up_taken = False
        down_taken = False            
    # Getting the current time
    cTime = time.time()
    # Getting frame per second 
    fps = 1/(cTime-pTime)
    # Previous time become current time
    pTime = cTime
    # Labeling the Frame rate 
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,
                            (255,0,255),3)

    cv2.imshow("image",img) # Show the frame
    cv2.waitKey(1) # Wait for 1 millisecond
