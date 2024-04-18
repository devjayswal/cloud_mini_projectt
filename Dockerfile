# Use the official Python image as the base image
FROM python:3.11.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]



# There are two command  to build this image
#first to build 
# docker build -t app .
# secound  to run this docker image
#  docker run -v //c/Users/rdssj/Desktop/Work/cloud_mini:/app -p 5000:5000 app