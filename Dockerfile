# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3

# Set the working directory to /usr/src/app.
WORKDIR /usr/app

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY . .

RUN /bin/bash -c "source /usr/app/scraper_env/bin/activate" \
    cd /usr/app

CMD ['python','auto_runner.py']
# COPY requirements.txt ./

# Install Scrapy specified in requirements.txt.
# RUN pip3 install --no-cache-dir -r requirements.txt

