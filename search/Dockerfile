# Use an official lightweight Python image
FROM python:3.12-slim

# Install Java (JDK, not just JRE!)
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python dependencies
RUN pip install -r server-requirements.txt

RUN python3 init

# Tell Docker that the app runs on port 5000
EXPOSE 5000

# Run your app
CMD ["python3", "-u", "-m", "main"]
# CMD ["sh", "-c", "python3 -m init && python3 -u -m main"]
