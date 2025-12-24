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
