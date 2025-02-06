# Use official lightweight Python image
FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy only required files
COPY github_telegram_bot.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "github_telegram_bot.py"]

