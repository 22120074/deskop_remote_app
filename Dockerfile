# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Expose the port the server will run on
EXPOSE 8080

# Run the server.py script when the container launches
CMD ["python", "server.py"]
