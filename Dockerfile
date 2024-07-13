# Use an official Python runtime as a parent image
FROM python:3.12.4-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary libraries for PyAudio and sqlite3
RUN apt-get update && apt-get install -y portaudio19-dev sqlite3

# Continue with the existing steps
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 8100

# Run app.py when the container launches
CMD ["python", "run.py"]