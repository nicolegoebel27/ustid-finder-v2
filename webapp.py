from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os

from excel import ExcelProcessor

app = FastAPI()

templates = Jinja2Templates(directory="templates")

processor = ExcelProcessor()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    upload_folder = "uploads"
    output_folder = "output"

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    input_file = os.path.join(upload_folder, file.filename)

    with open(input_file, "wb") as buffer:
        buffer.write(await file.read())

    output_file = os.path.join(
        output_folder,
        "Ergebnis_" + file.filename
    )

    processor.process_file(
        input_file=input_file,
        output_file=output_file
    )

    return FileResponse(
        output_file,
        filename=os.path.basename(output_file)
    )
