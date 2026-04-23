# Face Recognition Attendance System

> **[System Design](./systemdesign.md)** - Architecture, data flow, and how it works end-to-end

---


A real-time attendance system that uses facial recognition to automatically mark attendance via webcam.

## How It Works

1. Training images of known individuals are stored in the `Training_images/` folder
2. The system encodes each face on startup
3. Webcam feed is compared against known encodings in real time
4. When a match is found, the person's name and timestamp are logged to `Attendance.csv`

## Project Structure

```
├── Training_images/       # Known face images (one per person, named by person)
├── folder/                # Sample/test images
├── main.py                # Main script — runs webcam-based recognition
├── latest.py              # Updated version of main script
├── face trainer.py        # Script to train/encode faces
├── face_trainer.ipynb     # Jupyter notebook version of face trainer
├── picstodatacon.py       # Utility: image to dataset conversion
├── pictodataset.py        # Utility: picture to dataset helper
├── Attendance.csv         # Output — logs name and timestamp on recognition
├── haarcascade_frontalface_alt2.xml
└── haarcascade_frontalface_default.xml
```

## Setup

### Prerequisites

- Python 3.7+
- Webcam

### Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `dlib` installation may require CMake and Visual Studio Build Tools on Windows.

### Add Training Images

Place `.jpg` images of known people in the `Training_images/` folder. Name each file after the person:

```
Training_images/
  sarthak.jpg
  pragyan.jpg
  Shagnik.jpg
```

### Run

```bash
python main.py
```

The webcam will open and recognized faces will be highlighted with a green box and name label.

## Dependencies

Key libraries used:

- [face_recognition](https://github.com/ageitgey/face_recognition) — facial encoding and matching
- [OpenCV](https://opencv.org/) — webcam capture and image rendering
- [dlib](http://dlib.net/) — underlying face detection model
- NumPy

## Output

Attendance is saved to `Attendance.csv` with the format:

```
Name, Time
SARTHAK, 10:32:45
PRAGYAN, 10:33:01
```
