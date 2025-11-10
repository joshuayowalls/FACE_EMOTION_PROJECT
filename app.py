"""
Emotion Detection Web Application
Detects emotions from webcam feed and uploaded images using a trained CNN model.
"""

from flask import Flask, render_template, Response, request, jsonify, send_file
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename
from PIL import Image
import io
from datetime import datetime
import json

# Import custom modules
from face_emotions import detect_emotion
from database import insert_detection, get_detections, get_emotion_statistics

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize webcam
camera = None
current_emotion = "Neutral"
current_confidence = 0.0

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_camera():
    """Get or initialize the camera."""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        # Set camera properties for better performance
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 30)
    return camera

def release_camera():
    """Release the camera resource."""
    global camera
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    """Generate frames from webcam for live streaming."""
    global current_emotion, current_confidence
    
    camera = get_camera()
    frame_count = 0
    
    while True:
        try:
            success, frame = camera.read()
            if not success:
                print("Failed to read from camera")
                break
            
            frame_count += 1
            
            # Process every nth frame to reduce computation
            if frame_count % 2 == 0:
                try:
                    emotion = detect_emotion(frame)
                    current_emotion = emotion
                except Exception as e:
                    print(f"Error detecting emotion: {e}")
                    emotion = "Error"
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
        except Exception as e:
            print(f"Error in frame generation: {e}")
            break

@app.route('/')
def index():
    """Render the main page."""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering index: {e}")
        return f"Error loading page: {str(e)}", 500

@app.route('/video_feed')
def video_feed():
    """Stream video feed from webcam."""
    try:
        return Response(generate_frames(), 
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error in video feed: {e}")
        return f"Error: {str(e)}", 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload for emotion detection.
    
    Expects:
        - file: Image file
        - user_name: Name of the user
    
    Returns:
        JSON with detection results
    """
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        if 'user_name' not in request.form or not request.form['user_name'].strip():
            return jsonify({'error': 'User name is required'}), 400
        
        file = request.files['file']
        user_name = request.form['user_name'].strip()
        
        # Validate file
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PNG, JPG, JPEG, GIF'}), 400
        
        # Save file
        filename = secure_filename(f"{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read image
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Failed to read image'}), 400
        
        # Detect emotion
        emotion = detect_emotion(image)
        
        # Store in database
        record_id = insert_detection(
            user_name=user_name,
            image_path=filepath,
            detected_emotion=emotion,
            detection_method='upload'
        )
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'user_name': user_name,
            'timestamp': datetime.now().isoformat(),
            'record_id': record_id,
            'filename': filename
        }), 200
        
    except Exception as e:
        print(f"Error in upload: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/emotion', methods=['GET'])
def get_current_emotion():
    """Get the current detected emotion from webcam."""
    try:
        return jsonify({
            'emotion': current_emotion,
            'confidence': current_confidence,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get detection history for a user."""
    try:
        user_name = request.args.get('user_name')
        limit = request.args.get('limit', default=20, type=int)
        
        records = get_detections(user_name, limit)
        
        history = []
        for record in records:
            history.append({
                'id': record[0],
                'user_name': record[1],
                'emotion': record[3],
                'timestamp': record[6],
                'method': record[5]
            })
        
        return jsonify({
            'success': True,
            'records': history,
            'total': len(history)
        }), 200
        
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_stats():
    """Get emotion statistics."""
    try:
        user_name = request.args.get('user_name')
        stats = get_emotion_statistics(user_name)
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/capture', methods=['POST'])
def capture_frame():
    """Capture and save current frame from webcam."""
    try:
        user_name = request.json.get('user_name') # type: ignore
        
        if not user_name or not user_name.strip():
            return jsonify({'error': 'User name is required'}), 400
        
        camera = get_camera()
        success, frame = camera.read()
        
        if not success:
            return jsonify({'error': 'Failed to capture frame'}), 400
        
        # Detect emotion
        emotion = detect_emotion(frame)
        
        # Save frame
        filename = secure_filename(f"{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_webcam.jpg")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv2.imwrite(filepath, frame)
        
        # Store in database
        record_id = insert_detection(
            user_name=user_name,
            image_path=filepath,
            detected_emotion=emotion,
            detection_method='webcam'
        )
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'user_name': user_name,
            'timestamp': datetime.now().isoformat(),
            'record_id': record_id,
            'filename': filename
        }), 200
        
    except Exception as e:
        print(f"Error capturing frame: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        camera = get_camera()
        camera_ok = camera is not None and camera.isOpened()
        
        return jsonify({
            'status': 'ok',
            'camera_connected': camera_ok,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

@app.teardown_appcontext
def cleanup(exception):
    """Cleanup resources on app shutdown."""
    release_camera()

if __name__ == '__main__':
    try:
        # Get port from environment or use default
        port = int(os.environ.get('PORT', 5000))
        debug_mode = os.environ.get('DEBUG', 'False') == 'True'
        
        print("=" * 60)
        print("Emotion Detection Web Application")
        print("=" * 60)
        print(f"Starting on http://0.0.0.0:{port}")
        print(f"Debug Mode: {debug_mode}")
        print("=" * 60)
        
        # Run app
        app.run(host='0.0.0.0', port=port, debug=debug_mode, threaded=True)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        release_camera()
