import os
import random

from fastapi import Depends, FastAPI, File, Form, Request, Response, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(
            random.randint(100000, 999999)
        )  # Generate a random integer session ID
    return session_id


@app.get("/{session_id}", response_class=HTMLResponse)
async def read_item(session_id: str, request: Request, response: Response):
    response.set_cookie(key="session_id", value=session_id, httponly=False)
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "message": "Hello from FastAPI", "session_id": session_id},
    )


@app.get("/", response_class=HTMLResponse)
async def main(
    request: Request, response: Response, session_id: str = Depends(get_session_id)
):
    response.set_cookie(
        key="session_id", value=session_id, httponly=False
    )  # Set httponly to False
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "message": "Hello from FastAPI", "session_id": session_id},
    )


@app.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...), session_id: str = Form(...)):
    print(f"session_id: {session_id}")
    file_location = f"audio_files/{session_id}_{audio.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(await audio.read())
    return {"info": f"file '{audio.filename}' saved at '{file_location}'"}


@app.get("/get-audio/{session_id}")
async def get_audio(session_id: str):
    file_location = f"audio_files/{session_id}_audio.wav"
    return FileResponse(file_location)
