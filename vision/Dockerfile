FROM python:3.11-slim

# Install system dependencies for OpenCV, dlib, and AI libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1 \
    libxrender1 \
    libfontconfig1 \
    libice6 \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ============================================================
# STAGE 1: Install PyTorch CPU-only (much smaller than GPU version)
# Same models, same accuracy - free tier has no GPU anyway
# ============================================================
RUN pip install --no-cache-dir \
    torch==2.1.0+cpu \
    torchvision==0.16.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# ============================================================
# STAGE 2: Install TensorFlow CPU (installed separately to reduce peak memory)
# ============================================================
RUN pip install --no-cache-dir tensorflow-cpu==2.15.0

# ============================================================
# STAGE 3: Install remaining dependencies
# ============================================================
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --default-timeout=300 \
    --retries=5 \
    -r requirements.txt

# Copy application code
COPY . .

# Create directory for known faces database
RUN mkdir -p /app/known_faces

# Expose port
EXPOSE 8001

# Run the vision service
CMD ["python", "main.py"]
