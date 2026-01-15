FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot_optimized.py .
COPY scanner_yfinance.py .

# Run bot
CMD ["python", "-u", "bot_optimized.py"]
