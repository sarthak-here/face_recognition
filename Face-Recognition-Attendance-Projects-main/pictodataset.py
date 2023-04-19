import os
import face_recognition
import cv2

def recognize_and_save_faces(known_faces_folder, image_path, output_folder):
    # Load known face encodings
    known_faces_encodings = []
    known_faces_names = []

    for filename in os.listdir(known_faces_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            name, _ = os.path.splitext(filename)
            image = face_recognition.load_image_file(os.path.join(known_faces_folder, filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_faces_encodings.append(encoding)
            known_faces_names.append(name)

    # Load the image to recognize
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_image = cv2.resize(unknown_image, (1920, 1080))
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)
    unknown_face_locations = face_recognition.face_locations(unknown_image)

    # Convert the unknown image to OpenCV format
    unknown_image_cv = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)


    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recognize faces and save them
    for i, (encoding, (top, right, bottom, left)) in enumerate(zip(unknown_face_encodings, unknown_face_locations)):
        matches = face_recognition.compare_faces(known_faces_encodings, encoding)

        name = f"unknown_{i + 1}"

        if True in matches:
            match_index = matches.index(True)
            name = known_faces_names[match_index]

        face_image = unknown_image_cv[top:bottom, left:right]
        cv2.imwrite(f'{output_folder}/{name}.jpg', face_image)


if __name__ == "__main__":
    known_faces_folder_path = "Training_images"
    input_image_path = "input.jpg"


    output_folder_path = "folder"
    recognize_and_save_faces(known_faces_folder_path, input_image_path, output_folder_path)