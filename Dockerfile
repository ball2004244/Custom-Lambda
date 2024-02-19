FROM python:3.11-slim

# Set up woking directory
WORKDIR /app
ADD . /app

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Open port 9999 on container
EXPOSE 9999

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9999"]