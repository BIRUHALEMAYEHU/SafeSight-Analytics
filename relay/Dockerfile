FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OpenCV and network tools
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py .

# Expose port (default for our script is 5000, but we'll use gunicorn to run it)
EXPOSE 5000

# Start command using gunicorn to run the Flask app
# Since video streams are long-lived long-polling processes, we need multiple threads/workers
CMD ["gunicorn", "-w", "1", "--threads", "4", "--timeout", "0", "-b", "0.0.0.0:5000", "main:app"]
