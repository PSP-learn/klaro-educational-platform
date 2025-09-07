# 🐳 Klaro Educational Platform - Docker Configuration
# Optimized for Railway deployment with Python 3.12

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (build tools + image libs needed by Pillow/ReportLab)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    postgresql-client \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libart-2.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Hint build system where to find freetype include dir for reportlab
ENV CFLAGS="-I/usr/include/freetype2"
ENV FREETYPE_DIR="/usr/include/freetype2"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start command using Python startup script
CMD ["python", "start.py"]
