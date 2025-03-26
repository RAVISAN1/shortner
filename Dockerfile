# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    ca-certificates \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome's official signing key and repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > /tmp/chrome-key.pub \
    && install -D -m 644 /tmp/chrome-key.pub /etc/apt/keyrings/google-chrome-keyring.pub \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome-keyring.pub] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && rm /tmp/chrome-key.pub

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver (version compatible with Chrome 123)
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/123.0.6312.86/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Copy project files
COPY requirements.txt .
COPY app.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
