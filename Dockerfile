# Use the official Python image with version 3.10 (or latest stable)
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the script and any additional required files
COPY delete_s3_versions_and_markers.py /app/delete_s3_versions_and_markers.py

# Install boto3 and other dependencies
RUN pip install --no-cache-dir boto3 argparse

# Command to run the script (environment variables are passed directly)
CMD ["python", "delete_s3_versions_and_markers.py"]
