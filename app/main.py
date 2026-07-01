from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from app.config import UPLOAD_DIR, OUTPUT_DIR, BASE_DIR
from services.excel_service import ExcelService

app = FastAPI(title="USt-ID Finder Pro")

TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

excel_service = ExcelService()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    input_path = UPLOAD_DIR / file.filename

    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = OUTPUT_DIR / f"Ergebnis_{file.filename}"

    try:
        excel_service.process_file(
            input_path=input_path,
            output_path=output_path
        )

    except Exception as e:
        return {
            "error": str(e)
        }

    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
