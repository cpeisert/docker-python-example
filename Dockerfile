#
# Copyright (c) Christopher Peisert. All rights reserved.
#
# Python support can be specified down to the minor or micro version (e.g. 3.6 or 3.6.3).
# @see https://hub.docker.com/r/library/python/ (all supported tags)
# @see https://github.com/docker-library/python
FROM python:3.8-slim-buster

# Command line arguments for the image build process.
# To set the environment variables, use docker `--build-arg` arguments:
#   $ docker build --build-arg production=False
ARG app_name="docker-python-example"
ARG version="0.0.1"
ARG production=True
ARG debug=False
ARG private_port=8888
ARG public_port=8000

LABEL Name=${app_name} Version=${version}
WORKDIR /

# Note: venv (or conda) is not necessary, since this container is only running one Python app.
RUN python3 -m pip install --upgrade pip

ADD requirements.txt /
RUN python3 -m pip install -r requirements.txt

ADD app /app
ADD create_gunicorn_conf.py /
ADD images /images
ADD LICENSE /
ADD main.py /
ADD styles.css /
ADD templates /templates


# Create new /app/env.py file.
RUN echo "\
app_name = '${app_name}'\n\
app_version = '${version}'\n\
production = ${production}\n\
debug = ${debug}\n\
public_port = ${public_port}\n\
private_port = ${private_port}\n" > /app/env.py

RUN python3 create_gunicorn_conf.py --bind=0.0.0.0:${private_port}

# If hosting on Azure, go to App Service > Settings > Configuration
# Add the following key value pair and save (if "8000" is not the public port number, then
# update accordingly):
#
# WEBSITES_PORT  8000
#
EXPOSE ${public_port}

CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]
