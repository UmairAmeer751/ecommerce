# Use official Python runtime as a parent image
# Optimization: Using a slim base image to reduce image size
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
# Optimization: Separating build/runtime dependencies, using caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
