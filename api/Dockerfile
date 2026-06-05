# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

# Installation des dépendances dans un dossier temporaire
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

WORKDIR /app

# Copie des paquets depuis le builder
COPY --from=builder /root/.local /root/.local

# Ajout du PATH pour accéder à uvicorn
ENV PATH=/root/.local/bin:$PATH

# Copie du code source
COPY ./api ./api

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
