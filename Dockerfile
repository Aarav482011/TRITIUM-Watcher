# Use the official Playwright image which has Chromium pre-installed
FROM mcr.microsoft.com/playwright:v1.41.0-jammy

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables for Apify
ENV APIFY_CONTAINER_PORT=8000
EXPOSE 8000

# Start the MCP server
CMD ["python", "tritium_watcher.py"]
