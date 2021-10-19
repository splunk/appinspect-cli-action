# Container image that runs your code
FROM python:3.7.10

COPY requirements.txt /
RUN pip install --no-cache-dir --prefer-binary -r /requirements.txt

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /
COPY reporter.py /
COPY compare_checks.py /

# Code file to execute when the docker container starts up (`entrypoint.sh`)
WORKDIR /github/workspace
ENTRYPOINT ["bash", "-x", "/entrypoint.sh"]
