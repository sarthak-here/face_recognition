# Face Recognition Attendance System - System Design

## What It Does
An automated attendance system using a webcam to recognize faces in real time and log
attendance to a CSV file. Trained on photos of known individuals; unknown faces are
flagged and saved for review.

---

## Architecture

```
Training Photos (Training_images/)
        |
        v
+--------------------------------------------------+
|     face_trainer.py / pictodataset.py            |
|  - Load each photo                               |
|  - Detect face (Haar Cascade classifier)         |
|  - Encode face -> 128-dim embedding (dlib)       |
|  - Store: {name -> embedding} mapping            |
+--------------------------------------------------+
        |
  known_names[] + known_encodings[]
        |
        v
+--------------------------------------------------+
|             main.py (real-time recognition)      |
|  - Capture webcam frames (cv2.VideoCapture)      |
|  - Detect faces (Haar Cascade)                   |
|  - Encode each detected face (128-dim)           |
|  - Compare with known encodings (euclidean dist) |
|  - Match -> name  OR  "Unknown"                  |
|  - Mark attendance if not already logged today   |
+--------------------------------------------------+
        |
        v
  Attendance.csv  (Name, Date, Time)
  folder/unknown_N.jpg  (unrecognized faces)
```

---

## Data Flow

```
TRAINING PHASE:
  Training_images/sarthak.jpg, pragyan.jpg, Shagnik.jpg
        |
  cv2.imread() each photo
        |
  haarcascade_frontalface_default.xml
  -> detect face bounding box in training photo
        |
  face_recognition.face_encodings(img, locations)
  -> 128-dimensional embedding vector
        |
  Store: known_names[] + known_encodings[]

RECOGNITION PHASE:
  Webcam frame
        |
  Resize to 1/4 resolution (4x speed improvement)
        |
  face_recognition.face_locations(frame)
  -> bounding boxes of all faces in frame
        |
  face_recognition.face_encodings(frame, locations)
  -> 128-dim vector per detected face
        |
  For each detected face:
    compare_faces(known_encodings, face_encoding)
    face_distance() -> pick closest match
    If distance < threshold AND not marked today:
      Append to Attendance.csv: (Name, Date, Time)
      Draw name label on bounding box
    Else:
      Display "Unknown" + save to folder/unknown_N.jpg
```

---

## Key Design Decisions

| Decision                       | Reason                                           |
|--------------------------------|--------------------------------------------------|
| Haar Cascade for detection     | Fast, CPU-only, no GPU required                  |
| 128-dim dlib face embeddings   | Pre-trained ResNet; 99.38% accuracy on LFW benchmark|
| Euclidean distance threshold   | Tunable sensitivity for different lighting conditions|
| Quarter-resolution processing  | Cuts per-frame time from ~200ms to ~50ms         |
| CSV attendance log             | Portable; opens directly in Excel/Google Sheets  |

---

## Interview Conclusion

This system implements the standard face recognition pipeline: enrollment (encode known
faces once) then real-time identification (compare live faces to stored encodings). The
key performance insight is 4x downscaling before detection: locations computed on the
small frame are scaled back up for display, cutting processing time by ~16x with minimal
accuracy loss. The face_recognition library uses dlib's ResNet model (99.38% accuracy
on LFW), which is more than sufficient for classroom attendance. Production improvements:
add a database instead of CSV, anti-spoofing (liveness detection) to prevent photo
attacks, and periodic re-enrollment to handle changes in appearance over time.
