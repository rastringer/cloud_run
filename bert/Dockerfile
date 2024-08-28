# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download and cache the model during the build process
RUN python -c "from transformers import AutoTokenizer, AutoModel; model_name='bert-base-uncased'; AutoTokenizer.from_pretrained(model_name); AutoModel.from_pretrained(model_name)"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "main.py"]