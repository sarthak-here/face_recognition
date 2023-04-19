# importing neccessary libraries
import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0)
classifier = cv2.CascadeClassifier(r"C:/Users/sarthak/mydtiproject/Face-Recognition-Attendance-Projects-main/Face-Recognition-Attendance-Projects-main/haarcascade_frontalface_alt2.xml")

name = input("Enter your name:\n")
frames = []
name_output = []

while True:
    success, frame = cap.read()
    if success:
        faces = classifier.detectMultiScale(frame)

        for face in faces:
            x, y, w, h = face
            if w > 100 and h > 100:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            Face_Cut = frame[y:y + h, x:x + w]
            fixed = cv2.resize(Face_Cut, (100, 100))
            grayscale = cv2.cvtColor(fixed, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Detected Face ", grayscale)


        print(faces)
        cv2.imshow("Viewpoint", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

    if key == ord("c"):
        cv2.imwrite(os.path.join(r"trained pics/",name + ".jpg"), frame )
        frames.append(grayscale.flatten())
        name_output.append([name])

# Creating Numpy arrays for stacking up data
x = np.array(frames)
y = np.array(name_output)

data = np.hstack([y, x])
# print(data.shape)

# saving the face data extracted as npy matrix/array
#face_name = (r"C:\Users\sarthak\Project-Hawkeye\Main projects\trained_data_numpy\face_Training_data.npy")

#if os.path.exists(face_name):
#    old_data = np.load(face_name, allow_pickle=True)
#    data = np.vstack([old_data,data]) 
#else:
#    np.save(face_name, data)

cap.release()
cv2.destroyAllWindows()