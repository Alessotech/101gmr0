# Use Playwright base image
FROM mcr.microsoft.com/playwright/python:v1.39.0

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Expose the application port
EXPOSE 8080

# Start FastAPI with Uvicorn (NO xvfb-run)
CMD ["uvicorn", "download_script:app", "--host", "0.0.0.0", "--port", "8080"]
