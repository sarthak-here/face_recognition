# Face Recognition Attendance System — System Design

## What It Does
An automated attendance system that uses a webcam to recognize faces in real time and logs attendance to a CSV file. Trained on photos of known individuals; unknown faces are flagged separately.

---

## Architecture

```
Training Photos (Training_images/)
        |
        v
+--------------------------------------------------+
|         face_trainer.py / face trainer.py        |
|  - Load each image                               |
|  - Detect face with Haar Cascade classifier      |
|  - Encode face -> 128-dim embedding vector       |
|  - Store: {name -> embedding} mapping            |
+--------------------------------------------------+
        |
    known_encodings.pkl (or in-memory)
        |
        v
+--------------------------------------------------+
|             main.py  (real-time recognition)     |
|  - Capture webcam frames (cv2.VideoCapture)      |
|  - Detect faces in frame (Haar Cascade)          |
|  - Encode each detected face                     |
|  - Compare with known encodings (euclidean dist) |
|  - Match -> person name OR "Unknown"             |
|  - Log to Attendance.csv if not already today    |
+--------------------------------------------------+
        |
        v
  Attendance.csv  (Name, Date, Time)
```

---

## Input

| Input | Detail |
|---|---|
| Training images | JPEG photos in Training_images/ folder, one folder per person |
| Live webcam | Real-time video via OpenCV |

---

## Data Flow

```
TRAINING PHASE (picstodataset.py / face_trainer.py):
  Training_images/sarthak.jpg, pragyan.jpg, Shagnik.jpg
        |
  cv2.imread() each image
        |
  haarcascade_frontalface_default.xml
  -> detect face bounding box in training photo
        |
  face_recognition.face_encodings(image, locations)
  -> 128-dimensional embedding vector per face
        |
  Store: known_names[] + known_encodings[]

RECOGNITION PHASE (main.py):
  Webcam frame
        |
  Resize to 1/4 resolution (speed optimization)
        |
  face_recognition.face_locations(frame)
  -> bounding boxes of all faces in frame
        |
  face_recognition.face_encodings(frame, locations)
  -> 128-dim vector per detected face
        |
  For each detected face:
    Compare to all known_encodings
    face_recognition.compare_faces()  (euclidean < threshold)
    face_recognition.face_distance()  -> pick closest match
        |
  If match found AND not marked today:
    Append to Attendance.csv: (Name, Date, Time)
    Display name label on bounding box
  If no match:
    Display "Unknown" label
    Save to folder/unknown_N.jpg for review
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| Haar Cascade for detection | Fast, CPU-only, no GPU required for a classroom system |
| 128-dim face_recognition embeddings | Pre-trained dlib model; robust to lighting and angle variation |
| Euclidean distance threshold | Tunable sensitivity; lower threshold = stricter matching |
| Quarter-resolution processing | Reduces latency from ~200ms to ~50ms per frame |
| CSV attendance log | Simple, portable, opens directly in Excel/Google Sheets |

---

## Interview Conclusion

This system implements the standard face recognition pipeline: enrollment (encode known faces once) followed by real-time identification (compare live faces to stored encodings). The key performance insight is the 4x downscaling before running face detection: face locations are computed on the small frame, then scaled back up for display on the full-resolution frame. This cuts per-frame processing time by roughly 16x with minimal accuracy loss. The use of the face_recognition library (built on dlib's ResNet model) gives 99.38% accuracy on the LFW benchmark, which is more than sufficient for a classroom attendance use case. If I were building a production version, I would replace CSV logging with a database, add anti-spoofing (liveness detection) to prevent photo attacks, and implement periodic re-enrollment to handle changes in appearance over time.
