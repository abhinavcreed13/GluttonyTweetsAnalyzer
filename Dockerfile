# Use an official Python runtime as a parent image
FROM python:3.7-alpine

# Set the working directory to /app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 1313 available to the world outside this container
EXPOSE 1313

# Define environment variable
ENV NAME AppFrontendNew

# Run app.py when the container launches
CMD ["python3", "app.py"]
