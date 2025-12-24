import os
import argparse
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import music21

def transcribe_audio_to_midi(audio_path, output_midi_path):
    print(f"Transcribing {audio_path}...")
    model_output, midi_data, note_events = predict(
        audio_path,
        ICASSP_2022_MODEL_PATH
    )
    midi_data.write(output_midi_path)
    print(f"MIDI saved to {output_midi_path}")
    return output_midi_path
