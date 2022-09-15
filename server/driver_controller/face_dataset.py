# Import OpenCV2 for image processing
import cv2
import os

# Start capturing video 
cam = cv2.VideoCapture(0)

cam.set(3,1080)
cam.set(4,720)

# Detect object in video stream using Haarcascade Frontal Face
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, one face id
face_id = "0013740260"

# Initialize sample face image
count = 0

# Start looping
while(True):

    # Capture video frame
    ret, img = cam.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loops for each faces
    for (x,y,w,h) in faces:

        # Crop the image frame into rectangle
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        
        # Increment sample face image
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
        cv2.imshow('frame', img)

    # To stop taking video, press 'q' for at least 100ms
    k=cv2.waitKey(100) and 0xff
    if k==27:
        break

    # If image taken reach 100, stop taking video
    elif count>50:
        break

# Stop video
cam.release()

# Close all started windows
cv2.destroyAllWindows()