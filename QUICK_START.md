# 🚀 Quick Start Guide

## Get Started in 5 Minutes

### Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application (30 sec)
```bash
python app.py
```

### Step 3: Open in Browser (30 sec)
```
http://localhost:5000
```

### Step 4: Allow Webcam Access (if prompted)
Click "Allow" when browser asks for camera permission

### Step 5: Start Using! (2 min)
- **Webcam Tab**: Live emotion detection
- **Upload Tab**: Analyze images
- **History Tab**: View your detections

---

## Features Overview

### 📹 Live Webcam Detection
1. Enter your name
2. Allow webcam access
3. See real-time emotion detection
4. Click "Capture & Save" to store frames

### 📤 Upload Images
1. Click "Upload Image" tab
2. Enter your name
3. Select or drag-drop an image
4. Click "Analyze Image"
5. View the detected emotion

### 📊 View History
1. Click "History" tab
2. Optionally filter by name
3. View all your detections
4. Check emotion statistics

---

## API Testing

### Test with cURL

```bash
# Get current emotion
curl http://localhost:5000/api/emotion

# Upload image
curl -F "file=@image.jpg" -F "user_name=John" http://localhost:5000/upload

# Get history
curl http://localhost:5000/api/history?user_name=John

# Get statistics
curl http://localhost:5000/api/statistics?user_name=John
```

---

## File Organization

```
OLAWALE_23CG034125/
├── app.py                      ← Start here
├── model.py                    ← For training
├── face_emotions.py            ← Emotion detection logic
├── database.py                 ← Database operations
├── requirements.txt            ← Dependencies
├── link_to_my_web_app.txt     ← Hosting link
├── README.md                   ← Full documentation
├── CODE_REVIEW_REPORT.md      ← Review details
├── QUICK_START.md             ← This file
├── templates/
│   └── index.html             ← Web interface
├── static/
│   └── styles.css             ← Styling
├── uploads/                   ← Uploaded images (auto-created)
├── __pycache__/               ← Python cache (auto-created)
└── emotion_detection_results.db ← Database (auto-created)
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "Failed to load model"
**Solution**: Ensure `face_emotions_model.h5` is in the project root

### Issue: Webcam not working
**Solution**: 
- Check browser permissions
- Close other apps using camera
- Refresh the page
- Use image upload instead

### Issue: "No faces detected"
**Solution**:
- Improve lighting
- Move closer to camera
- Ensure face is clearly visible
- Try multiple frames

---

## Deployment Links

### Render (Recommended - Free)
1. Go to https://render.com
2. Sign up and connect GitHub
3. Create new Web Service
4. Select your repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn app:app`
7. Deploy!

### Update link_to_my_web_app.txt
After deployment, update the file:
```
Render - https://your-app-name.onrender.com
```

---

## Database Location

SQLite database is automatically created at:
```
emotion_detection_results.db
```

### View Database Contents (Python)
```python
import sqlite3
conn = sqlite3.connect('emotion_detection_results.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM emotion_detections')
for row in cursor.fetchall():
    print(row)
conn.close()
```

---

## Environment Variables

### Local Development (Optional)
```bash
set PORT=5000
set DEBUG=True
python app.py
```

### Production
```bash
set PORT=8000
set DEBUG=False
gunicorn app:app
```

---

## Testing Emotions

Try these expressions for testing:

| Emotion | Expression |
|---------|-----------|
| Happy | 😊 Smile |
| Angry | 😠 Frown deeply |
| Sad | 😢 Pouty face |
| Surprised | 😲 Raise eyebrows |
| Disgust | 😒 Nose wrinkle |
| Fear | 😨 Eyes wide open |
| Neutral | 😐 Relaxed face |

---

## Tips for Best Results

1. **Lighting**: Ensure even, bright lighting
2. **Distance**: 30-60cm from camera
3. **Angle**: Face camera directly
4. **Expression**: Clear, exaggerated expressions
5. **Image Quality**: High-quality images for uploads
6. **Model**: Pre-trained model is provided (no retraining needed)

---

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run with different port
set PORT=8000 && python app.py

# Train model (if dataset available)
python model.py

# View git status
git status

# Add files to git
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main
```

---

## Next Steps

1. ✅ **Install & Run**: Get the app working locally
2. ✅ **Test Features**: Try webcam and upload
3. ✅ **Update Database**: Add test records
4. ✅ **Deploy Online**: Push to Render/Heroku
5. ✅ **Update Link**: Edit link_to_my_web_app.txt
6. ✅ **Push to GitHub**: Commit and push all changes
7. ✅ **Submit**: Upload to SCORAC

---

## Support Resources

- **Errors**: Check console output (F12 in browser)
- **API Issues**: Use `/health` endpoint to debug
- **Database**: Check `emotion_detection_results.db`
- **Logs**: Check terminal output from `python app.py`

---

**You're all set! 🎉 Start by running `python app.py`**
