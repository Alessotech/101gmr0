# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install minimal system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    wget \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN python -m playwright install --with-deps

# Copy application files
COPY . .

# Expose the port
EXPOSE 8080

# Start the application
CMD ["uvicorn", "download_script:app", "--host", "0.0.0.0", "--port", "8080"]
