from flask import Flask, request, jsonify
import os
import threading
import pygame

app = Flask(__name__)

# Папка для загрузки файлов
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def play_audio(sound_path):
    try:
        print(f"Attempting to play audio from: {sound_path}")
        if os.path.exists(sound_path):
            pygame.mixer.init()
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
              pygame.time.Clock().tick(10)
        else:
            print(f"File does not exist: {sound_path}")
    except Exception as e:
        print(f"Error playing audio: {e}")

@app.route('/', methods=['POST'])
def start():
    return 'Hello'

@app.route('/play', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(f"Saving file to: {file_path}")
        file.save(file_path)
        threading.Thread(target=play_audio, args=(file_path,)).start()
        file.close()
        return jsonify({"message": f"File uploaded and playing: {file.filename}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)