# Use official Python 3.9 slim image (compatible with many Rasa versions)
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy your project files into container
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install your specific dependencies here, example:
RUN pip install rasa==3.6.21 \
    sanic==21.12.1 \
    tensorflow==2.11.0 \
    # add any other packages your project needs here

# Expose Rasa port
EXPOSE 5005

# Run Rasa server on container start
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
