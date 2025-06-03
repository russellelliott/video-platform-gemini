# Video Gemini Platform

A FastAPI app for uploading videos and chatting with Google Gemini about their content.

## Setup

Make a clean virtual python environment to avoid issues with dependencies
CMND + Shift + P -> "select pytohn interpreter" -> "create virtual environment"

1. **Install dependencies**  
   ```
   pip install fastapi uvicorn httpx python-dotenv python-multipart
   ```

2. **Create a `.env` file** in the project root with your Gemini API key:  
   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

3. **Run the server**  
   ```
   uvicorn main:app --reload
   ```

4. **Open your browser** and go to [http://localhost:8000](http://localhost:8000).

## Usage

- Upload a video file using the web interface.
- After upload, view the Gemini-generated summary.
- Use the chat interface to ask questions about the uploaded video.



Resources

Google Gemini

Video
https://ai.google.dev/gemini-api/docs/video-understanding
Can also do Youtube: https://ai.google.dev/gemini-api/docs/video-understanding#youtube


Files API?
https://ai.google.dev/gemini-api/docs/files

audio: https://ai.google.dev/gemini-api/docs/audio

image
https://ai.google.dev/gemini-api/docs/image-understanding




Speaker Diarization
https://medium.com/@samarrana407/geminis-hidden-power-the-ultimate-guide-to-speaker-diarization-audio-transcription-ad9a1a660244
https://cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery/samples/audio_audio_diarization_1



index.html; basic video upload
main.py; basic video upload

index2.html; basic chat interface (proof of concept)
main2.py; also has video upload, basic chat interface (proof of concept)

combo to use
- index.html for uploading file
- main2.py has endpoints for uploading the file and also processing a video at a given location

