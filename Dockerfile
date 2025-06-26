# Use official Python 3.9 slim image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Rasa default port (5005)
EXPOSE 5005

# Run Rasa server when container starts
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
