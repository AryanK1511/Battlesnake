# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make the start script executable
COPY start_app.sh /app/start_app.sh
RUN chmod +x /app/start_app.sh

# Command to run your application
CMD ["./start_app.sh"]