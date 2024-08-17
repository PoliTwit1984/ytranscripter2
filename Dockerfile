# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
ENV YOUTUBE_API_KEY=AIzaSyD_dwAaIyvo9-3jOmC1dSKMM2TFGm5FvWo
ENV OPENROUTER_API_KEY=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

# Run the application
CMD ["python", "app.py"]
