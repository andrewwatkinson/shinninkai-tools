# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# clone the repository
RUN git clone https://github.com/andrewwatkinson/shinninkai-tools.git /app

# Set the working directory in the container
WORKDIR /app

# list the contents of the directory
RUN ls -la

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app as a viewer rather than a developer
ENTRYPOINT ["streamlit", "run", "/app/Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=False", "--client.showErrorDetails=False", "--client.toolbarMode=viewer"]