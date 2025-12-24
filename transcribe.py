import os
import argparse
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import music21

def transcribe_audio_to_midi(audio_path, output_midi_path):
    print(f"Transcribing {audio_path}...")
    
    # Run the basic-pitch inference
    model_output, midi_data, note_events = predict(
        audio_path,
        ICASSP_2022_MODEL_PATH
    )
    
    # Save MIDI data
    midi_data.write(output_midi_path)
    print(f"MIDI saved to {output_midi_path}")
    return output_midi_path

def convert_midi_to_xml(midi_path, output_xml_path):
    print(f"Converting MIDI to MusicXML...")
    
    # Load MIDI file using music21
    score = music21.converter.parse(midi_path)
    
    # Save as MusicXML
    score.write('musicxml', fp=output_xml_path)
    print(f"MusicXML saved to {output_xml_path}")
    return output_xml_path

def main():
    parser = argparse.ArgumentParser(description="Pianote: Audio to Piano Sheet Music")
    parser.add_argument("input", help="Path to input audio file (.wav, .mp3, etc.)")
    parser.add_argument("--output_dir", default=".", help="Directory to save output files")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        return

    base_name = os.path.splitext(os.path.basename(args.input))[0]
    midi_output = os.path.join(args.output_dir, f"{base_name}.mid")
    xml_output = os.path.join(args.output_dir, f"{base_name}.musicxml")

    # 1. Transcribe Audio to MIDI
    transcribe_audio_to_midi(args.input, midi_output)
    
    # 2. Convert MIDI to MusicXML (for MuseScore)
    convert_midi_to_xml(midi_output, xml_output)
    
    print("\nTranscription complete!")
    print(f"Generated files:\n- MIDI: {midi_output}\n- MusicXML: {xml_output}")
    print("\nYou can now open the .musicxml file in MuseScore for fine-tuning.")

if __name__ == "__main__":
    main()
