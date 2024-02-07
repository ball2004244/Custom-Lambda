# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9999 available to the world outside this container
EXPOSE 9999

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9999"]