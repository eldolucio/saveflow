# Use Python 3.12 slim image
FROM python:3.12-slim

# Install FFmpeg and other build tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port (default 5001, but usually overridden by cloud provider)
EXPOSE 5001

# Run the server
CMD ["python", "server.py"]
