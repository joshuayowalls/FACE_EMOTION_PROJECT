"""
Emotion Detection Module
Detects emotions from facial expressions in images/frames using a pre-trained CNN model.
"""

import cv2
import numpy as np
from tensorflow.keras.models import load_model # pyright: ignore[reportMissingImports]
import os

# Configuration
MODEL_PATH = 'face_emotions_model.h5'
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' # pyright: ignore[reportAttributeAccessIssue]

# Emotion labels (7 classes)
EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
FACE_SIZE = 48

# Load model once at module import
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model from {MODEL_PATH}: {e}")
    model = None

# Load Haar Cascade for face detection
try:
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if face_cascade.empty():
        raise RuntimeError(f'Failed to load Haar cascade from {CASCADE_PATH}')
except Exception as e:
    print(f"Error loading face cascade: {e}")
    face_cascade = None

def is_model_available():
    """Check if model is loaded and available."""
    return model is not None and face_cascade is not None

def detect_emotion(frame, draw_box=True):
    """
    Detect emotion(s) in a frame/image with face(s).
    
    Args:
        frame (np.ndarray): Input image frame (BGR format from OpenCV)
        draw_box (bool): Whether to draw bounding box and label on frame (in-place)
    
    Returns:
        str: Detected emotion label (or 'No Face Detected' / 'Error' if failed)
    """
    
    if not is_model_available():
        print("Model or cascade not available")
        return "Error"
    
    try:
        # Validate input
        if frame is None or not isinstance(frame, np.ndarray):
            print("Invalid frame input")
            return "Error"
        
        if frame.size == 0:
            print("Empty frame")
            return "Error"
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Try multiple detection strategies for robustness
        faces = _detect_faces_multi_strategy(gray)
        
        if len(faces) == 0:
            print("No faces detected in frame")
            return "No Face Detected"
        
        # Process first detected face
        emotion, confidence = _predict_emotion_for_face(faces[0], gray)
        
        # Draw on frame if requested
        if draw_box and len(faces) > 0:
            _annotate_frame(frame, faces[0], emotion)
        
        return emotion
        
    except Exception as e:
        print(f"Error in detect_emotion: {e}")
        return "Error"

def _detect_faces_multi_strategy(gray_image):
    """
    Try multiple detection strategies to improve robustness.
    Returns list of detected faces as (x, y, w, h) tuples.
    """
    attempts = []
    
    # Strategy 1: Histogram equalization with tight parameters
    gray_eq = cv2.equalizeHist(gray_image)
    attempts.append({
        'img': gray_eq,
        'scaleFactor': 1.1,
        'minNeighbors': 5,
        'minSize': (30, 30)
    })
    
    # Strategy 2: Original grayscale with moderate parameters
    attempts.append({
        'img': gray_image,
        'scaleFactor': 1.05,
        'minNeighbors': 4,
        'minSize': (30, 30)
    })
    
    # Strategy 3: Original with default-ish parameters (fallback)
    attempts.append({
        'img': gray_image,
        'scaleFactor': 1.3,
        'minNeighbors': 5,
        'minSize': (30, 30)
    })
    
    faces = ()
    for attempt in attempts:
        try:
            faces = face_cascade.detectMultiScale( # pyright: ignore[reportOptionalMemberAccess]
                attempt['img'],
                scaleFactor=attempt['scaleFactor'],
                minNeighbors=attempt['minNeighbors'],
                minSize=attempt['minSize']
            )
            if len(faces) > 0:
                break
        except Exception as e:
            print(f"Detection attempt failed: {e}")
            continue
    
    return faces

def _predict_emotion_for_face(face_coords, gray_image):
    """
    Predict emotion for a detected face region.
    
    Args:
        face_coords (tuple): Face coordinates (x, y, w, h)
        gray_image (np.ndarray): Grayscale image
    
    Returns:
        tuple: (emotion_label, confidence_score)
    """
    try:
        x, y, w, h = face_coords
        
        # Extract face region
        face_roi = gray_image[y:y+h, x:x+w]
        
        if face_roi.size == 0:
            return "Error", 0.0
        
        # Resize to model input size
        face_resized = cv2.resize(face_roi, (FACE_SIZE, FACE_SIZE))
        
        # Normalize to [0, 1]
        face_normalized = face_resized.astype('float32') / 255.0
        
        # Reshape for model: (1, 48, 48, 1)
        face_input = np.expand_dims(face_normalized, axis=(0, -1))
        
        # Predict
        predictions = model.predict(face_input, verbose=0) # pyright: ignore[reportOptionalMemberAccess]
        confidence = float(np.max(predictions[0]))
        emotion_idx = int(np.argmax(predictions[0]))
        emotion_label = EMOTION_LABELS[emotion_idx]
        
        return emotion_label, confidence
        
    except Exception as e:
        print(f"Error predicting emotion: {e}")
        return "Error", 0.0

def _annotate_frame(frame, face_coords, emotion):
    """
    Annotate frame with face bounding box and emotion label.
    Modifies frame in-place.
    """
    try:
        x, y, w, h = face_coords
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Prepare text
        text = f'Emotion: {emotion}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        color = (0, 255, 0)  # Green
        
        # Get text size for background
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        
        # Position text above face (or below if not enough space)
        text_y = y - 10 if y - 10 > 20 else y + h + 25
        text_x = x
        
        # Draw background rectangle for text
        cv2.rectangle(
            frame,
            (text_x, text_y - text_size[1] - 5),
            (text_x + text_size[0] + 5, text_y + 5),
            (0, 0, 0),
            -1
        )
        
        # Draw text
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, font_thickness)
        
    except Exception as e:
        print(f"Error annotating frame: {e}")

def get_emotion_labels():
    """Return list of supported emotion labels."""
    return EMOTION_LABELS.copy()

def get_model_info():
    """Return information about the loaded model."""
    if model is None:
        return {'status': 'error', 'message': 'Model not loaded'}
    
    try:
        return {
            'status': 'loaded',
            'model_path': MODEL_PATH,
            'emotions': EMOTION_LABELS,
            'num_emotions': len(EMOTION_LABELS),
            'face_size': FACE_SIZE,
            'parameters': model.count_params()
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
