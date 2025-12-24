import os
import urllib.request

checkpoint_url = "https://zenodo.org/record/4034264/files/CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1"
data_dir = os.path.join(os.path.expanduser("~"), "piano_transcription_inference_data")
checkpoint_path = os.path.join(data_dir, "note_F1=0.9677_pedal_F1=0.9186.pth")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")

print(f"Downloading checkpoint from {checkpoint_url}...")
print(f"This may take a few minutes (165 MB)...")

try:
    urllib.request.urlretrieve(checkpoint_url, checkpoint_path)
    print(f"Successfully downloaded to: {checkpoint_path}")
except Exception as e:
    print(f"Error downloading: {e}")
