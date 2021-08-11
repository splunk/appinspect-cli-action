# Container image that runs your code
FROM python:3.9.6

COPY requirements.txt /
RUN pip install --no-cache-dir --prefer-binary -r /requirements.txt

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /
COPY reporter.py /

# Code file to execute when the docker container starts up (`entrypoint.sh`)
WORKDIR /github/workspace
ENTRYPOINT ["/entrypoint.sh"]
