import os
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

path_old = "/Users/russellelliott/Desktop/UCSC Grad School/Year 1/Spring 2025/CMPM290A/video-platform-gemini/uploaded_videos/e21e7572-eb03-4529-9b2e-44862a7f8bfa_Sensitive Data Detector.mp4"
path = "/Users/russellelliott/Desktop/UCSC Grad School/Year 1/Spring 2025/CMPM290A/video-platform-gemini/uploads/Plivo Demo (compressed).mp4"

myfile = client.files.upload(file=path)

# Wait for file to become ACTIVE before using it
import time
for _ in range(20):
    myfile = client.files.get(name=myfile.name)
    if getattr(myfile, "state", None) == "ACTIVE":
        break
    time.sleep(1)
else:
    raise RuntimeError(f"File {myfile.name} did not become ACTIVE in time.")

# Unlike OpenAI, Gemini doesn't have specific parameter to specify format of response. Format must be specified in the prompt.
prompt = (
    "Generate audio diarization for this interview. "
    "Use JSON format for the output, with the following keys: \"timestamp\", \"speaker\", \"transcription\". "
    "If you can infer the speaker, please do. If not, use speaker A, speaker B, etc."
)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[myfile, prompt]
)

print(response.text)