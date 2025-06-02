FROM python:3.12-slim

WORKDIR /app/PyLauncher

COPY upload.txt .

RUN pip install --no-cache-dir -r upload.txt

COPY . .

CMD ["python", "run.py"]