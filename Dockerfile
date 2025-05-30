FROM python:3.11-slim

WORKDIR /app/PyLauncher

# Copie des dépendances
COPY upload.txt .

# Installation des dépendances (pour le bot ET pour l'exécution utilisateur)
RUN pip install --no-cache-dir -r upload.txt

# Copie du reste du projet
COPY . .

# Lancement du bot
CMD ["python", "run.py"]