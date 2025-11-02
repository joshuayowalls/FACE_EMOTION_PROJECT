import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('face_emotions_model.h5')

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if face_cascade.empty():
    raise RuntimeError('Failed to load Haar cascade for face detection')

def detect_emotion(frame):
    """Detect face(s) in `frame`, predict emotion for the first face found, and
    annotate the supplied frame in-place with the predicted emotion.

    Returns the predicted emotion string or 'No Face Detected'.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Try a few detection strategies to improve robustness
    attempts = []

    # 1) Equalized histogram (helps in varied lighting)
    gray_eq = cv2.equalizeHist(gray)
    attempts.append({'img': gray_eq, 'scaleFactor': 1.1, 'minNeighbors': 5})

    # 2) Original gray with tighter params
    attempts.append({'img': gray, 'scaleFactor': 1.05, 'minNeighbors': 4})

    # 3) Original gray with default-ish params (fallback)
    attempts.append({'img': gray, 'scaleFactor': 1.3, 'minNeighbors': 5})

    faces = ()
    for a in attempts:
        faces = face_cascade.detectMultiScale(a['img'], scaleFactor=a['scaleFactor'], minNeighbors=a['minNeighbors'], minSize=(30, 30))
        if len(faces) > 0:
            # Found at least one face
            # Use the detected image coordinates (x,y,w,h) from this attempt
            break

    if len(faces) == 0:
        # No face found after all attempts
        # For debugging, print so server logs show the failure for a sample
        print('detect_emotion: no faces found')
        return "No Face Detected"

    # Use first detected face
    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]
    try:
        face = cv2.resize(face, (48, 48))
    except Exception:
        # If resize fails, return safe response
        print('detect_emotion: failed to resize detected face')
        return 'No Face Detected'

    face = face.astype('float32') / 255.0  # Normalize
    face = np.expand_dims(face, axis=(0, -1))  # Shape -> (1,48,48,1)

    try:
        preds = model.predict(face, verbose=0)
        label = emotion_labels[int(np.argmax(preds[0]))]
    except Exception as e:
        print('detect_emotion: model prediction error:', e)
        return 'Error'

    # Annotate the original color frame with the result near the face
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(frame, f'Emotion: {label}', (x, y - 10 if y - 10 > 10 else y + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return label
