from flask import Flask, render_template, Response
import cv2
from face_emotions import detect_emotion

app = Flask(__name__)

# Note: the model and Haar cascade are loaded inside `face_emotions.py`.
# The server should not re-load the model to avoid duplicate heavy loads.
# Start video capture for the webcam
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Detect the emotion from the face in the frame. detect_emotion will
            # also annotate the frame with text. Wrap in try/except so a model
            # error doesn't kill the generator.
            try:
                emotion = detect_emotion(frame)
            except Exception as e:
                # On error, annotate the frame and continue streaming a safe message
                emotion = 'Error'
                cv2.putText(frame, 'Emotion: Error', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            # Convert the frame to bytes and return
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in the templates/ folder

# Route to stream the webcam feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start Flask server (local development)
if __name__ == '__main__':
    # Bind to 0.0.0.0 for easier local testing; port 5000 is the default.
    app.run(host='0.0.0.0', port=5000, debug=True)