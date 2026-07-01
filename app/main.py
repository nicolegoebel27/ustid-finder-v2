from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from services.excel_service import ExcelService

app = FastAPI(title="USt-ID Finder Pro")

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATE_DIR = BASE_DIR / "templates"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

excel_service = ExcelService()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    input_path = UPLOAD_DIR / file.filename

    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = OUTPUT_DIR / f"Ergebnis_{file.filename}"

    excel_service.process_file(
        input_path=input_path,
        output_path=output_path
    )

    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
