# Use official Python runtime as the base image
FROM python:3.11.8-slim

# Set working directory in container
WORKDIR /app
# Install required packages
RUN pip install discord.py aiohttp
# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy config file first
COPY config.json .
# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "main.py"]