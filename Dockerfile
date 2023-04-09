# используем базовый образ Python 3.9
FROM python:3.9

# устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# копируем наше приложение в образ
COPY ./app /app

# устанавливаем рабочую директорию
WORKDIR /app

# указываем порт, на котором будет работать наше приложение
EXPOSE 80

# запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]