FROM python:3.11-slim

# Harden pip to be more resilient in slower networks
ENV PIP_DEFAULT_TIMEOUT=120 \
	PIP_RETRIES=10 \
	PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create static directory
RUN mkdir -p static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
