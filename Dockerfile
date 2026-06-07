FROM python:3.11-slim

WORKDIR /app

# Install system deps for ChromaDB + SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy root requirements for static site, then YonocyTech requirements for app
COPY requirements.txt YonocyTech/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose both ports: Streamlit (8501) + API (8000)
EXPOSE 8501 8000

# Start both services — PYTHONPATH ensures api.server resolves from YonocyTech/
ENV PYTHONPATH=/app/YonocyTech:$PYTHONPATH
CMD ["sh", "-c", "\
    uvicorn api.server:app --host 0.0.0.0 --port 8000 & \
    streamlit run YonocyTech/ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 \
"]
