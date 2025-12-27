# Multi-stage Docker build for Python calculator app

# Stage 1: Build stage with development dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage - minimal image
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY VERSION .

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Add labels for version tracking
ARG VERSION=unknown
LABEL version="${VERSION}"
LABEL maintainer="DevOps Team"
LABEL description="Calculator application with auto-versioning"

# Run the application
CMD ["python", "src/app.py"]
