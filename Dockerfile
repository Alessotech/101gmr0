FROM mcr.microsoft.com/playwright/python:v1.39.0

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "download_script:app", "--host", "0.0.0.0", "--port", "8080"]
