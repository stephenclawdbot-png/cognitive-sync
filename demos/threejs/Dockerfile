FROM python:3.11-slim

LABEL maintainer="COGNITIVE-SYNC Team"
LABEL description="EMG-driven thought visualization demo"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY demo_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    websockets==12.0 \
    numpy==1.24.0

# Create necessary directories
RUN mkdir -p /app/demo_app/web_ui \
    /app/SILENT-001/firmware \
    /app/COGNITIVE-SYNC/src

# Copy demo app files
COPY demo_app/ /app/demo_app/

# Copy SILENT simulator (read-only reference)
COPY SILENT-001/firmware/SILENT_SIMULATOR.py /app/SILENT-001/firmware/

# Copy COGNITIVE-SYNC core modules
COPY thought_node.py /app/COGNITIVE-SYNC/
COPY websocket_bridge.py /app/COGNITIVE-SYNC/
COPY src/ /app/COGNITIVE-SYNC/src/

# Set environment variables
ENV PYTHONPATH=/app:/app/COGNITIVE-SYNC:/app/SILENT-001/firmware
ENV PORT=8000

# Create non-root user
RUN useradd -m -u 1000 cognitive && chown -R cognitive:cognitive /app
USER cognitive

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# Run the server
CMD ["python", "-m", "uvicorn", "demo_app.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
