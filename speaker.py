import os
from pyannote.audio import Pipeline
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=hf_token)

# send pipeline to GPU (when available)
import torch
pipeline.to(torch.device("cpu"))

# apply pretrained pipeline
diarization = pipeline("audio.wav")

# print the result
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
# start=0.2s stop=1.5s speaker_0
# start=1.8s stop=3.9s speaker_1
# start=4.2s stop=5.7s speaker_0
# ...