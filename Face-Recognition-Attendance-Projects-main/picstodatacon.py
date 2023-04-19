import cv2
import os

# load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# create a folder to store the extracted faces
if not os.path.exists('faces'):
    os.makedirs('faces')

# read the input image
img = cv2.imread('input.jpg')

# convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# loop over each detected face
for (x, y, w, h) in faces:
    # extract the face region
    face = img[y:y+h, x:x+w]

    # save the face to the faces folder
    cv2.imwrite(f'faces/{x}_{y}_{w}_{h}.jpg', face)

    # draw a rectangle around the face in the original image
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

# show the original image with detected faces
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
