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

def convert_midi_to_xml(midi_path, output_xml_path):
    print(f"Converting MIDI to MusicXML...")
    score = music21.converter.parse(midi_path)
    score.write('musicxml', fp=output_xml_path)
    print(f"MusicXML saved to {output_xml_path}")
    return output_xml_path
