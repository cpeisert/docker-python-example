#!/usr/bin/env python
#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Flask app initialization."""

import logging
import traceback

from flask import Flask, render_template, request, send_from_directory
from werkzeug.exceptions import (
    Forbidden, HTTPException, ImATeapot, NotFound, RequestTimeout, Unauthorized
)

from app.blueprints import app_info
from app import env
from app.utils import cors_utils, json_utils


def configure_flask_app(flask_app: Flask):
    environment = "production" if env.production else "development"
    debug = "True" if env.debug else "False"
    flask_app.config.update(
        DEBUG=debug,
        ENV=environment,
        MAX_CONTENT_LENGTH="8388608",
        PREFERRED_URL_SCHEME="http"
    )

    flask_app.register_blueprint(app_info.app_info)

    @flask_app.route("/")
    def root():
        return render_template(
            "index.html",
            version=env.app_version,
            environment=environment,
            private_port=env.private_port,
            public_port=env.public_port,
            debug=env.debug
        )

    @flask_app.route("/<path:path>", methods=["GET"])
    def static_proxy(path):
        return send_from_directory("./", path)

    #
    # ERROR HANDLERS
    # Note that the order of the handlers does not matter.
    #

    @flask_app.errorhandler(HTTPException)
    def http_exception_handler(e: HTTPException):
        """Handle Werkzeug HttpExceptions."""
        log_exception(e)
        return render_template(
            "error_http.html",
            error_type=type(e).__name__,
            description=e.description,
            code=e.code), e.code

        #
        # Alternatively, return a JSON response.
        #
        # return json_utils.json_response(
        #     json_data={"error": f"HTTP error {e.code}"},
        #     status_code=e.code,
        #     response_headers=cors_utils.get_cors_headers(request))

    @flask_app.errorhandler(Exception)
    def generic_exception_handler(e: Exception):
        log_exception(e)
        return render_template(
            "error_internal.html",
            error_type=type(e).__name__,
            description=_get_error_description(e),
            code=500), 500
        #
        # Alternatively, return a JSON response.
        #
        # return json_utils.json_response(
        #     json_data={"error": "An internal error occurred."},
        #     status_code=500,
        #     response_headers=cors_utils.get_cors_headers(request))


def log_exception(e: Exception):
    error_name = type(e).__name__
    stack_trace = ""
    if env.debug:
        stack_trace = "\n" + traceback.format_exc()

    error_description = f" - {_get_error_description(e)}"

    http_status_code = ""
    if isinstance(e, HTTPException):
        http_status_code = f"{e.code} "

    logger = logging.getLogger()
    message = f"{http_status_code}{error_name}{error_description}{stack_trace}"
    logger.log(level=logging.ERROR, msg=message)


def _get_error_description(e: Exception):
    if isinstance(e, HTTPException):
        return e.description
    elif hasattr(e, "args"):
        return e.args[0]
    return ""
