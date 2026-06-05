FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances minimales
RUN pip install --no-cache-dir streamlit httpx pandas

# Copie du code
COPY ./dashboard ./dashboard

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
