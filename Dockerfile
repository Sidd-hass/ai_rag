# Use Python 3.12 slim for a smaller footprint
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for FAISS and PDF parsing
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Ensure necessary directories exist for persistence
RUN mkdir -p uploads vector_db

# Expose the FastAPI port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]