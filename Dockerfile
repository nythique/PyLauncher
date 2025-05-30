# Utilise une image légère de python
FROM python:3.11-slim
# Dossier e travail
WORKDIR /app/PyLauncher
# Copy des dependances
COPY upload.txt .
# Installation des dependances
RUN pip install --no-cache-dir -r upload.txt
# Copy des tout les autres fichier et dossier du projet
COPY . .
# Execution du fichier primcipal
CMD ["python", "run.py"]