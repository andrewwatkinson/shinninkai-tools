# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/andrewwatkinson/shinninkai-tools.git .

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app as a viewer rather than a developer
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]