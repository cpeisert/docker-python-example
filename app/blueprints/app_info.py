#!/usr/bin/env python
#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Flask blueprint example.

Note:
    The "OPTIONS" HTTP method is enabled in the endpoints below to support cross-origin resource
    sharing (CORS).

See also:
    * https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    * app/utils/cors_utils.py
"""

from flask import Blueprint, request
from werkzeug.exceptions import ImATeapot, Unauthorized
from werkzeug.wrappers import BaseResponse as Response

from app import env
from app.utils import cors_utils, json_utils


app_info = Blueprint("app_info", __name__)


@app_info.route("/app-info", methods=["GET", "OPTIONS"])
def get_app_info() -> Response:
    """Returns the application info. The HTTP Response object contains JSON formatted as:

    {
        "app-name": <app name>,
        "version": <version number>,
        "production": bool,
        "debug": bool
    }
    """
    if request.method == "OPTIONS":
        return cors_utils.get_http_response_for_options_request(request)
    return json_utils.json_response(
        {
            "app-name": env.app_name,
            "version": env.app_version,
            "production": env.production,
            "debug": env.debug
        },
        response_headers=cors_utils.get_cors_headers(request)
    )


@app_info.route("/exception", methods=["GET", "OPTIONS"])
def test_exception() -> Response:
    """Raises ValueError to test the Flask HTML template error_internal.html."""
    raise ValueError("testing exception handling")


@app_info.route("/teapot", methods=["GET", "OPTIONS"])
def test_teapot() -> Response:
    """Raises ImATeapot to test the Flask HTML template error_http.html.

    This server is a teapot and someone attempted to brew coffee with it.
    """
    raise ImATeapot()


@app_info.route("/secret", methods=["GET", "OPTIONS"])
def test_unauthorized() -> Response:
    """Raises an Unauthorized error to test the Flask HTML template error_http.html."""
    raise Unauthorized()
