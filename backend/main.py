import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import shutil
import uuid


from pdf_processor import delete_pages
from pdf_processor import merge_pdf
from fastapi.middleware.cors import CORSMiddleware

os.makedirs(
    "uploads",
    exist_ok=True
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/delete")
async def delete(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        pages_to_remove: str = Form(...)
):
    unique_name = (
        f"{uuid.uuid4()}_{file.filename}"
    )
    upload_path = f"uploads/{unique_name}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:
        pages_list = [
            int(page.strip()) - 1
            for page in pages_to_remove.split(",")
        ]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Page numbers must be integers separated by commas."
        )

    output_file = delete_pages(
        upload_path,
        pages_list
    )

    background_tasks.add_task(
        os.remove,
        upload_path
    )

    background_tasks.add_task(
        os.remove,
        output_file
    )

    return FileResponse(
        path=output_file,
        filename="edited.pdf",
        media_type="application/pdf"
    )


@app.post("/merge")
async def merge(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        half_cut: str = Form(...)
):
    unique_name = (
        f"{uuid.uuid4()}_{file.filename}"
    )
    upload_path = f"uploads/{unique_name}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    output_file = merge_pdf(
        upload_path,
        half_cut
    )

    background_tasks.add_task(
        os.remove,
        upload_path
    )

    background_tasks.add_task(
        os.remove,
        output_file
    )

    return FileResponse(
        path=output_file,
        filename="processed.pdf",
        media_type="application/pdf"
    )
