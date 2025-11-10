# 🎭 Emotion Detection System

A sophisticated AI-powered web application that detects human emotions from facial expressions in real-time using a trained Convolutional Neural Network (CNN) model.

## 📋 Features

### Core Functionality
- **Live Webcam Streaming**: Real-time emotion detection from webcam feed
- **Image Upload**: Analyze emotions from uploaded images (PNG, JPG, JPEG, GIF)
- **Emotion Classification**: Detects 7 different emotions:
  - 😠 Angry
  - 😒 Disgust
  - 😨 Fear
  - 😊 Happy
  - 😢 Sad
  - 😲 Surprise
  - 😐 Neutral

### Data Management
- **SQLite Database**: Stores detection history with user names and timestamps
- **Capture & Save**: Save webcam frames with emotion predictions
- **History Tracking**: View past detections for each user
- **Statistics**: Analyze emotion distribution over time

### Technical Highlights
- Advanced face detection with multiple strategies for robustness
- Real-time video streaming using Flask and MJPEG
- Responsive web UI with modern styling
- Comprehensive error handling and logging
- RESTful API endpoints for all operations

## 🗂️ Project Structure

```
OLAWALE_23CG034125/
├── app.py                          # Flask web application (main backend)
├── model.py                        # CNN model training script
├── face_emotions.py                # Emotion detection module
├── database.py                     # SQLite database operations
├── face_emotions_model.h5          # Pre-trained model weights
├── requirements.txt                # Python dependencies
├── link_to_my_web_app.txt         # Hosting platform and URL
├── README.md                       # This file
├── templates/
│   └── index.html                 # Web UI (HTML)
├── static/
│   └── styles.css                 # Styling (CSS)
├── uploads/                        # Directory for uploaded images
└── emotion_detection_results.db    # SQLite database (auto-created)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Webcam (for live detection feature)
- Modern web browser

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Prepare Dataset (Optional - for retraining)

If you want to retrain the model, organize your dataset:
```
datasets/
└── train/
    ├── angry/
    ├── disgust/
    ├── fear/
    ├── happy/
    ├── sad/
    ├── surprise/
    └── neutral/
```

Each folder should contain grayscale images (48x48 pixels).

### Step 3: Train the Model (Optional)

```bash
python model.py
```

This will:
- Build the CNN architecture
- Load and augment training data
- Train the model for 25 epochs
- Save the trained model as `face_emotions_model.h5`

## 🎯 Running the Application

### Local Development

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Environment Variables

```bash
# Set port (default: 5000)
set PORT=8000

# Enable debug mode (default: False)
set DEBUG=True
```

### Deployment

For deployment on platforms like Render, Heroku, or Railway, ensure:
1. `requirements.txt` is present
2. `PORT` environment variable is supported
3. Webcam may not be available in remote environments (use image upload instead)

## 🌐 Web Interface

### Tabs

#### 1. **Live Webcam** 📹
- Real-time emotion detection from webcam
- Current emotion display
- Capture and save frames
- Live statistics

#### 2. **Upload Image** 📤
- Upload images for emotion analysis
- Drag-and-drop support
- Image preview
- Instant results

#### 3. **History** 📊
- View all detections
- Filter by user name
- View emotion statistics
- Historical data visualization

## 🔌 API Endpoints

### Webcam Feed
```
GET /video_feed
```
Returns MJPEG video stream from webcam

### Upload Image
```
POST /upload
Headers: Content-Type: multipart/form-data
Body:
  - file: Image file
  - user_name: String
Response: { success, emotion, user_name, timestamp, record_id, filename }
```

### Get Current Emotion
```
GET /api/emotion
Response: { emotion, confidence, timestamp }
```

### Capture Frame
```
POST /capture
Body: { user_name }
Response: { success, emotion, user_name, timestamp, record_id, filename }
```

### Get Detection History
```
GET /api/history?user_name=<name>&limit=<number>
Response: { success, records, total }
```

### Get Statistics
```
GET /api/statistics?user_name=<name>
Response: { success, statistics }
```

### Health Check
```
GET /health
Response: { status, camera_connected, timestamp }
```

## 🔧 Model Architecture

```
Input: 48x48 Grayscale Image
  ↓
Conv2D(32, 3x3) + ReLU → MaxPooling(2x2)
  ↓
Conv2D(64, 3x3) + ReLU → MaxPooling(2x2)
  ↓
Conv2D(128, 3x3) + ReLU → MaxPooling(2x2)
  ↓
Flatten
  ↓
Dense(256) + ReLU + Dropout(0.5)
  ↓
Dense(128) + ReLU + Dropout(0.3)
  ↓
Dense(7) + Softmax
  ↓
Output: Emotion Class (0-6)
```

## 📊 Database Schema

### emotion_detections Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_name | TEXT | User identifier |
| image_path | TEXT | Path to stored image |
| detected_emotion | TEXT | Emotion label |
| confidence | REAL | Prediction confidence |
| detection_method | TEXT | 'webcam' or 'upload' |
| timestamp | DATETIME | Detection time |
| notes | TEXT | Additional information |

## 🐛 Troubleshooting

### No Webcam Access
- Check browser permissions (chrome://settings/privacy/camera)
- Ensure webcam is not in use by another application
- On cloud servers, use image upload feature instead

### Model Not Loading
```
Error: Failed to load model
Solution: Ensure face_emotions_model.h5 exists in project root
```

### Database Errors
```
Error: Database locked
Solution: Close any other connections to the database
```

### Face Not Detected
- Ensure good lighting
- Face should be clearly visible and front-facing
- Try moving closer to camera
- Adjust lighting to reduce shadows

## 📈 Performance Tips

1. **Webcam**: Skip every other frame for faster processing
2. **Lighting**: Ensure adequate lighting for best detection
3. **Distance**: Maintain 30-60cm distance from camera
4. **Model Size**: Use CPU version of TensorFlow for web environments

## 🔐 Security Considerations

- Validate file uploads (type, size)
- Sanitize user inputs
- Store images securely with access controls
- Implement rate limiting for API endpoints
- Use HTTPS in production

## 📝 License

This project is created for academic purposes.

## 👥 Author

**Student ID**: 23CG034125  
**Name**: OLAWALE

## 🔗 Resources

- [TensorFlow Keras Documentation](https://keras.io/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FER2013 Dataset](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data)

## 📞 Support

For issues or questions, please refer to:
- Flask Deployment Documentation
- TensorFlow Troubleshooting Guide
- OpenCV Face Detection Guide

---

**Last Updated**: November 2025  
**Version**: 1.0.0
