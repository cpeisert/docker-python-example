#!/usr/bin/env python
#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Python application entry point."""

from flask import Flask

from app import app_init, env

LOCALHOST = "127.0.0.1"

app = Flask(env.app_name)
app_init.configure_flask_app(app)

if __name__ == '__main__':
    # This is used when running locally only. In production, a web-server such as
    # Gunicorn (or other cloud provider infrastructure) will serve the app.
    app.run(host=LOCALHOST, port=env.public_port)
