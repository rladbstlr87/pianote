import os
import torch
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
transcriptor = PianoTranscription(device=device, checkpoint_path=None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        input_ext = os.path.splitext(filename)[1].lower()
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{filename}")
        output_name = os.path.splitext(filename)[0] + ".mid"
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_{output_name}")
        file.save(input_path)
        
        audio_path = input_path
        temp_audio = None

        try:
            # Handle video files
            if input_ext in VIDEO_EXTENSIONS:
                print(f"Extracting audio from video: {filename}...")
                video = VideoFileClip(input_path)
                temp_audio = os.path.join(UPLOAD_FOLDER, f"{file_id}_temp_audio.wav")
                video.audio.write_audiofile(temp_audio, logger=None)
                audio_path = temp_audio

            # Load audio
            (audio, _) = load_audio(audio_path, sr=sample_rate, mono=True)
            
            # Transcribe
            print(f"Starting transcription for {filename}...")
            transcriptor.transcribe(audio, output_path)
            print(f"Transcription finished: {output_path}")

            # Cleanup
            if temp_audio and os.path.exists(temp_audio):
                os.remove(temp_audio)
            
            return jsonify({"success": True, "midi_url": f"/download/{file_id}/{output_name}"})
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            if temp_audio and os.path.exists(temp_audio):
                os.remove(temp_audio)
            return jsonify({"error": str(e)}), 500

@app.route('/download/<file_id>/<filename>')
def download_file(file_id, filename):
    safe_filename = secure_filename(filename)
    path = os.path.join(OUTPUT_FOLDER, f"{file_id}_{safe_filename}")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=False, port=5000)
