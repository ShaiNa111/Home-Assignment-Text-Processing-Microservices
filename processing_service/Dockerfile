FROM python:3.11-slim

# Set working directory
WORKDIR /processing_service

# Copy requirements and install
COPY processing_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files from parent directory
COPY ../proto ./proto

# Copy service code
COPY processing_service .

# Download spaCy model
RUN python -m spacy download en_core_web_sm && \
    python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"

# Expose gRPC port
EXPOSE 50051

# Run gRPC server
CMD ["python", "main.py"]
