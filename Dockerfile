# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python

# Set the working directory to /usr/src/app.
WORKDIR /usr/app

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt .

RUN  pip install --upgrade pip \
      pip install -r requirements.txt




COPY . .

CMD ['python3','auto_runner.py']


