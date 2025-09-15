FROM python:3.11-slim

WORKDIR /serving_service

COPY serving_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files
COPY proto ./proto

# Copy service code
COPY serving_service/ .

# Copy shared proto package
COPY proto/ ./proto

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
