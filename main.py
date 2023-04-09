from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, File
import uuid
import os
import datetime
import uvicorn

# инициализируем приложение
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# подключаемся к базе данных
link_to_files = 'files/'
SQLALCHEMY_DATABASE_URL = "sqlite:///./files.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# функция для генерации уникального имени файла
def generate_filename(file_extension: str) -> str:
    return str(uuid.uuid4()) + file_extension


# функция для сохранения файла на диск и добавления записи в базу данных
def save_file_to_disk(file: UploadFile) -> File:
    # генерируем уникальное имя файла
    filename = generate_filename(os.path.splitext(file.filename)[1])

    # сохраняем файл на диск
    with open(f"{link_to_files}{filename}", "wb") as f:
        f.write(file.file.read())

    # добавляем запись в базу данных
    db = SessionLocal()
    db_file = File(
        filename=filename,
        original_name=file.filename,
        created_date=datetime.datetime.now()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# функция для загрузки файла
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, request: Request):
    # сохраняем время начала загрузки
    start_time = datetime.datetime.now()

    # сохраняем файл на диск и добавляем запись в базу данных
    db_file = save_file_to_disk(file)

    # формируем ссылку на файл
    file_link = request.url_for("read_file", filename=db_file.filename)

    # получаем текущую дату и время
    upload_date = db_file.created_date.strftime("%Y-%m-%d")
    upload_time = db_file.created_date.strftime("%H:%M:%S")

    # вычисляем время загрузки
    end_time = datetime.datetime.now()
    upload_duration = (end_time - start_time).total_seconds()

    # возвращаем шаблон с данными о загруженном файле
    return {
        "file_link": file_link,
        "file_name": db_file.filename,
        "upload_date": upload_date,
        "upload_time": upload_time,
        "upload_duration": upload_duration
    }


# функция для скачивания файла по ссылке
@app.get("/files/{filename}")
async def read_file(filename: str):
    db = SessionLocal()
    db_file = db.query(File).filter(File.filename == filename).first()

    if not db_file:
        return {"error": "File not found."}

    file_path = f"{link_to_files}{filename}"
    if not os.path.isfile(file_path):
        return {"error": "File not found on disk."}

    return FileResponse(file_path)


if __name__ == "__main__":
    uvicorn.run('main:app', port=8016)