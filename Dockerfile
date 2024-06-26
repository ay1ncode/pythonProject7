FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Set environment variables (You should replace these with your actual keys)
ARG ALPACA_API_KEY
ARG ALPACA_API_SECRET
ARG OPENAI_API_KEY
ENV ALPACA_API_KEY=${ALPACA_API_KEY}
ENV ALPACA_API_SECRET=${ALPACA_API_SECRET}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/trading-cron

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/trading-cron

# Apply cron job
# RUN crontab /etc/cron.d/trading-cron

# Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# Run the cron service in the foreground
CMD ["cron", "-f"]
