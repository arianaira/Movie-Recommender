# Use a specific Python 3.10 base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Upgrade pip and install necessary system packages
# This line includes the FIX: "libgl1" instead of the old "libgl1-mesa-glx"
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip numpy
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Set the command to run your Streamlit app
CMD ["streamlit", "run", "app.py"]