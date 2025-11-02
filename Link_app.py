import requests

def get_emotion_from_api(image_path):
    url = "http://127.0.0.1:5000/predict"
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    return response.json()
