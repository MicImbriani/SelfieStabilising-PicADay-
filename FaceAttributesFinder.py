#IMPORTS
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

# Constructs the argument parser and parses the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape_predictor", required=True, help="Path to facial mark predictor.")
ap.add_argument("-i", "--image", required=True, help="Path to input image.")
args = vars(ap.parse_args())



# Initializes dlib's face detector (HOG-based) and then creates the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])



# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width=1500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
rects = detector(gray, 1)


#Loops over each face in the detection
for (i, rect) in enumerate(rects):
    # 1)determine the facial landmarks for the current face
    # 2)convert the facial landmark (x,y)-coordinates to a NumPy array
    shape = predictor(gray,rect)
    shape = face_utils.shape_to_np(shape)

    # converts dlib rectangle to a OpenCV-style bounding box (x, y, w, h) then draws face
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # face ID
    cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # loop over the (x, y)-coordinates for the facial landmarks
    # and draw them on the image
    for (x, y) in shape:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

# show the output image with the face detections + facial landmarks
cv2.imshow("Output", image)
cv2.waitKey(0)