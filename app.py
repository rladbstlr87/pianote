import os
import torch
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import imageio_ffmpeg
import uuid

# Add ffmpeg to PATH for moviepy and librosa/audioread
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_path)
if ffmpeg_dir not in os.environ['PATH']:
    os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ['PATH']
    print(f"Added ffmpeg to PATH: {ffmpeg_dir}")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
transcriptor = PianoTranscription(device=device, checkpoint_path=None)

import threading
import sys
import io

# Global storage for progress
# Format: { file_id: { "progress": 0, "status": "processing", "result": None, "error": None } }
transcription_tasks = {}

class ProgressCapture(io.StringIO):
    def __init__(self, file_id):
        super().__init__()
        self.file_id = file_id
        
    def write(self, s):
        # The library prints "Segment x / y" to stdout
        if "Segment" in s:
            try:
                parts = s.split()
                # Segment 5 / 35 -> ["Segment", "5", "/", "35"]
                current = int(parts[1])
                total = int(parts[3])
                percentage = int((current / total) * 100)
                transcription_tasks[self.file_id]["progress"] = percentage
            except:
                pass
        sys.__stdout__.write(s)
        return super().write(s)

def run_transcription(file_id, audio, output_path, temp_audio):
    try:
        # Capture stdout to track progress
        original_stdout = sys.stdout
        sys.stdout = ProgressCapture(file_id)
        
        try:
            transcriptor.transcribe(audio, output_path)
            transcription_tasks[file_id]["status"] = "completed"
            transcription_tasks[file_id]["progress"] = 100
        finally:
            sys.stdout = original_stdout

        if temp_audio and os.path.exists(temp_audio):
            os.remove(temp_audio)
            
    except Exception as e:
        print(f"Error during transcription: {e}")
        transcription_tasks[file_id]["status"] = "failed"
        transcription_tasks[file_id]["error"] = str(e)
        if temp_audio and os.path.exists(temp_audio):
            os.remove(temp_audio)

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
        
        # Initialize task
        transcription_tasks[file_id] = {
            "progress": 0,
            "status": "extracting",
            "midi_url": f"/download/{file_id}/{output_name}"
        }

        def process_thread():
            audio_path = input_path
            temp_audio = None
            try:
                if input_ext in VIDEO_EXTENSIONS:
                    video = VideoFileClip(input_path)
                    temp_audio = os.path.join(UPLOAD_FOLDER, f"{file_id}_temp_audio.wav")
                    video.audio.write_audiofile(temp_audio, logger=None)
                    audio_path = temp_audio
                
                transcription_tasks[file_id]["status"] = "transcribing"
                (audio, _) = load_audio(audio_path, sr=sample_rate, mono=True)
                run_transcription(file_id, audio, output_path, temp_audio)
                
            except Exception as e:
                transcription_tasks[file_id]["status"] = "failed"
                transcription_tasks[file_id]["error"] = str(e)

        threading.Thread(target=process_thread).start()
        
        return jsonify({"success": True, "file_id": file_id})

@app.route('/status/<file_id>')
def get_status(file_id):
    task = transcription_tasks.get(file_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route('/download/<file_id>/<filename>')
def download_file(file_id, filename):
    safe_filename = secure_filename(filename)
    path = os.path.join(OUTPUT_FOLDER, f"{file_id}_{safe_filename}")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=False, port=5000)
