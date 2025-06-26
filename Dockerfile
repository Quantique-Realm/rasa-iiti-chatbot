FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy your project files
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Rasa port
EXPOSE 5005

# Run Rasa server with API enabled and CORS allowed
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
