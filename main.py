import os
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from dotenv import load_dotenv
from google import genai
import multipart

load_dotenv()

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "" or "your_google_gemini_api_key_here" in GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set or is invalid. Please set it in your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def serve_index():
    return FileResponse("static/index.html")

@app.post("/process")
async def process_video(file: UploadFile = File(...)):
    # Save uploaded file locally only
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"File saved to {file_path}"}

@app.post("/process_path")
def process_video_path(path: str = Body(..., embed=True)):
    if not os.path.isfile(path):
        return JSONResponse({"error": f"File not found: {path}"}, status_code=404)
    try:
        myfile = client.files.upload(file=path)
        # Wait for file to become ACTIVE before using it
        import time
        for _ in range(20):
            myfile = client.files.get(name=myfile.name)
            if getattr(myfile, "state", None) == "ACTIVE":
                break
            time.sleep(1)
        else:
            return JSONResponse({"error": f"File {myfile.name} did not become ACTIVE in time."}, status_code=500)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                myfile,
                "Summarize this video. Then create a quiz with an answer key based on the information in this video."
            ]
        )
        return {"result": response.text}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
