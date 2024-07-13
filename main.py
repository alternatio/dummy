from flask import Flask, request, jsonify
from audioplayer import AudioPlayer
import threading

app = Flask(__name__)

# method of play audio
def play_audio(sound_path):
  try:
    player = AudioPlayer(sound_path)
    player.play(block=True)
  except Exception as e:
    print(f"Error playing audio: {e}")

@app.rout('/')
def start():
  return 'Hello!'

# request to play sound
@app.route('/play', methods=['POST'])
def play():
  data = request.json
  sound_path = data.get('soundPath')
  if not sound_path:
    return jsonify({"error": "No sound path provided"}), 400
  
  # Create a new thread for playing the audio
  threading.Thread(target=play_audio, args=(sound_path,)).start()
  return jsonify({"message": f"Playing sound: {sound_path}"}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
