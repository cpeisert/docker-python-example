# Docker Python Flask Example using the Gunicorn WSGI HTTP Server

This project demonstrates packaging a Python [Flask](https://flask.palletsprojects.com/en/1.1.x/)
app in a Linux [Docker](https://www.docker.com/) container and covers the following topics:

- Passing arguments to the Docker build process (for example, app version and environment).
- Serving the Flask app using [Gunicorn](https://gunicorn.org/) WSGI server running inside a Docker
  container.
- Deploying the Docker container to the cloud:
  - Amazon Web Services (AWS)
  - Microsoft Azure
- Testing the Flask app locally without using Docker:
  - Default Werkzeug HTTP server that comes bundled with Flask
  - Gunicorn WSGI HTTP server
- The Flask app includes examples of:
  - Blueprints to modularize the REST API
  - Jinja2 HTML templates
  - Exception handling and basic logging
  - Custom JSON encoder and decoder supporting Date and Datetime fields.
  - Cross-Origin Resource Sharing (CORS) HTTP header handling.

The Docker image of this project is available on Docker Hub at
[ldp2016 / docker-python-example](https://hub.docker.com/repository/docker/ldp2016/docker-python-example).


# Table of Contents

- [Recommended software](#recommended-software)
- [Notes on using npm scripts](#notes-on-npm-scripts)
- [Quick Start](#quick-start)
- [How to push the image to Docker Hub](#how-to-push-the-image-to-docker-hub)
- [How to run the Docker container on AWS](#how-to-run-the-docker-container-on-aws)
- [How to run the Docker container on Azure](#how-to-run-the-docker-container-on-azure)
- [How to run the app locally without Docker](#how-to-run-the-app-locally-without-docker)


## Recommended software

- bash shell [For Windows users, recommend
  [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/about)]
- [Docker Engine](https://docs.docker.com/engine/install/)
- (Optional) In order to use the npm scripts in "package.json", install
  [npm](https://www.npmjs.com/get-npm).
- (Optional) For VS Code users, recommend installing the Docker extension.
- (Optional) Python 3 installed locally enables testing the Flask app independent of Docker.

## Notes on npm scripts

- To simplify using the Docker commands and completing other actions such as cloud deployment,
  [npm](https://www.npmjs.com/get-npm) scripts may be found in "package.json".

- To run npm scripts, use:
  ```
  npm run <npm script name>
  ```

- npm scripts export each entry of "package.json" as an environment variable. To see the list of
  both "package" and "npm config" environment variables, run the command:
  ```
  npm run check-env
  ```

- The "package" environment variables may be referenced in scripts using the syntax
  `$npm_package_<KEY_NAME>`, where <KEY_NAME> is a JSON key from "package.json". Each JSON nesting
  level is separated by an underscore (`_`).

- The primary npm scripts are:
  - `app.serve` - removes unused Docker data, builds the Docker image for a production environment,
    and runs the container.
  - `app.serve.dev` - removes unused Docker data, builds the Docker image for a development
    environment, sets Flask debugging to `True`, and runs the container.
  - `app.shutdown` - stops the Docker container and deletes it.

- The Docker build options use the npm variables `app_name`, `version`, `docker_id`,
  `private_port`, and `public_port`. Changing these variables will update the Docker build process
  when using the npm scripts `app.serve` and `app.serve.dev`.


# Quick Start

## Step 1: Clone repository, install Docker, and install npm

- Clone [this repository](https://github.com/cpeisert/docker-python-example)
- Install [Docker Engine](https://docs.docker.com/engine/install/)
- (Optional) Install [npm](https://www.npmjs.com/get-npm)

## Step 2: Build the Docker image for a development environment

In this step, we will remove unused Docker data, build the Docker image for a development
environment, and run the container using the newly built image.

- In a bash terminal, open the cloned repository directory:
```
$ cd docker-python-example
```

- If using npm, run:
```
$ npm run app.serve.dev
```

- If not using npm, run:
```
$ docker system prune -f
$ docker build --rm -t docker-python-example:v0.0.1 --build-arg production=False \
    --build-arg debug=True --build-arg app_name=docker-python-example --build-arg version=0.0.1 \
    --build-arg private_port=8888 --build-arg public_port=8000 .
$ docker run --detach --publish 8000:8888 --name docker-python-example docker-python-example:v0.0.1
```

- Visit [http://localhost:8000](http://localhost:8000) to ensure that the app is being served by
  Gunicorn in the Docker container.

- Test exception handling:
  - Visit: [http://localhost:8000/secret](http://localhost:8000/secret) to raise an Unauthorized error.
  - Visit: [http://localhost:8000/exception](http://localhost:8000/exception) to create an internal server error.
  - To see the logger output for the internal server error, run:
  ```
  $ docker logs docker-python-example
  ```

- Test JSON response:
  - Visit: [http://localhost:8000/app-info](http://localhost:8000/app-info) to get the app name.

- To see the list of running Docker containers, use:
```
$ docker container list -a
```

- Attempting to rebuild the Docker image while the container is running will fail:
```
$ npm run app.serve.dev

docker-python-example is already running on http://localhost:8000. To rebuild, first shutdown using command: npm run app.shutdown
```

- If using npm, shutdown the Docker container with:
```
$ npm run app.shutdown
```

- If not using npm, shutdown the Docker container with:
```
$ docker container rm -f docker-python-example
```

## Step 3: Build the Docker image for a production environment

- If using npm, run:
```
$ npm run app.serve
```

- If not using npm, run:
```
$ docker system prune -f
$ docker build --rm -t docker-python-example:v0.0.1 --build-arg app_name=docker-python-example \
    --build-arg version=0.0.1 --build-arg private_port=8888 --build-arg public_port=8000 .
$ docker run --detach --publish 8000:8888 --name docker-python-example docker-python-example:v0.0.1
```

- Visit [http://localhost:8000](http://localhost:8000) to ensure that the app is being served by
  Gunicorn in the Docker container.

- Shutdown the Docker container:
```
$ npm run app.shutdown
```

- Or shutdown with:
```
$ docker container rm -f docker-python-example
```


# How to push the image to Docker Hub

## Step 1: Create a repository

- Sign in to [Docker Hub](https://hub.docker.com/)
- Click "Create Repository"
- Enter name: docker-python-example
- Under **Visibility**, select "Public" or "Private"
- Click "Create"

## Step 2: Update "package.json"

- Open "package.json" and change the value of "docker_id" from "ldp2016" to your Docker ID.

## Step 3: Push the image

- Push the production image by running the following command. When prompted for a password, enter
  your Docker Hub password.
```
$ npm run app.push
```

- If the process stalls after pushing the image, press Enter.


# How to run the Docker container on AWS

## Step 1: Install the AWS CLI version 2

- [Install AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)



# How to run the Docker container on Azure

## Step 1: Install the Azure CLI

- [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)



# How to run the app locally without Docker

During app development, it can be helpful to test on the local machine without using Docker to more
easily isolate bugs or other issues that are unrelated to the Docker configuration.

## Step 1: Install Python and requirements.txt

- Install Python 3
- Install the Python requirements.txt locally, using either a virtual environment or a conda
  environment. See steps below for each environment option (only choose one of the options).

**Virtual environment (option 1)**
- Create a virtual environment named `docker-python`:
```
$ python -m venv docker-python
```

- Activate it:
```
$ source docker-python/bin/activate
```

- Install requirements:
```
$ pip install pip -upgrade
$ pip install -r requirements.txt
```

**Conda environment (option 2)**
- Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
- Create a conda environment named `docker-python`:
```
$ conda create --name docker-python
```

- Activate it:
```
$ conda activate docker-python
```

- Install requirements:
```
$ conda install -c conda-forge --file requirements.txt
```

## Step 3: Test Flask app locally with Werkzeug server

- Test the app using the Werkzeug server that comes bundled with Flask:
```
$ npm run app.local.werkzeug
```

- Or run the Werkzeug server without the npm script:
```
$ python main.py
```

- Visit [http://localhost:8000](http://localhost:8000) to ensure that Werkzeug is serving the app.
  Note that port 8000 is the default public port assigned to the Docker container.

- Stop the Werkzeug server by pressing <kbd>Ctrl+c</kbd> in the terminal.

## Step 4: Test Flask app locally with Gunicorn WSGI HTTP server

- Test the app using the Gunicorn server:
```
$ npm run app.local.gunicorn
```

- Or run Gunicorn without the npm script:
```
$ python create_gunicorn_conf.py --bind=127.0.0.1:8000
$ gunicorn -c gunicorn.conf.py main:app
```

- Visit [http://localhost:8000](http://localhost:8000) to ensure that Gunicorn is serving the app.
  Note that port 8000 is the default public port assigned to the Docker container.

- Stop Gunicorn by pressing <kbd>Ctrl+c</kbd> in the terminal.
