from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# Directory setup
UPLOAD_DIR = "uploads"
STATIC_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount the static directory (for serving other static assets if needed)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve index.html at "/"
@app.get("/", response_class=HTMLResponse)
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Upload endpoint
@app.post("/process")
async def process_video(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(content={
        "filename": file.filename,
        "saved_to": file_location,
        "message": "Upload successful"
    })
