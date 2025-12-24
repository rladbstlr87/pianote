import os
import torch
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
transcriptor = PianoTranscription(device=device, checkpoint_path=None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<file_id>/<filename>')
def download_file(file_id, filename):
    safe_filename = secure_filename(filename)
    path = os.path.join(OUTPUT_FOLDER, f"{file_id}_{safe_filename}")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404
