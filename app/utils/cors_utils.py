#!/usr/bin/env python
#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Custom implementation of Cross-Origin Resource Sharing (CORS) functions to limit server requests
to a list of whitelisted domains as well as providing the proper response headers.
"""

import re

from flask import Request, Response
from app.utils import json_utils

LOCALHOST_PATTERN = '//localhost\\:'
LOCALHOST_IP_PATTERN = '//127\\.0\\.0\\.1\\:'

WHITELISTED_ORIGINS = [
    "https://my-first-app.com",
    "https://my-second-app.com",
    "https://my-third-app.com"
]
ALLOWED_HTTP_METHODS = ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT']


def get_cors_headers(current_request: Request) -> dict:
    """Return a dict of default CORS headers that should be applied to all cross-origin HTTP
    requests."""
    cors_headers = dict()
    cors_headers['Access-Control-Allow-Credentials'] = 'true'

    url = current_request.environ.get('HTTP_ORIGIN', 'unknown')
    if _url_is_safe(url):
        cors_headers['Access-Control-Allow-Origin'] = url

    cors_headers['Vary'] = 'Origin'
    # See: https://www.chromium.org/Home/chromium-security/corb-for-developers
    cors_headers['X-Content-Type-Options'] = 'nosniff'
    return cors_headers


def get_cors_headers_for_http_options_request(current_request: Request) -> dict:
    """Return a dict of CORS headers satisfying an HTTP OPTIONS pre-flight request."""
    cors_headers = get_cors_headers(current_request)
    cors_headers["Access-Control-Allow-Headers"] = ("Accept, Content-Type, Origin, "
        "Access-Control-Request-Method, Access-Control-Request-Headers")
    cors_headers["Access-Control-Allow-Methods"] = ",".join(ALLOWED_HTTP_METHODS)
    return cors_headers


def get_http_response_for_options_request(current_request: Request) -> Response:
    """Returns a Response object containing the required headers to respond to an cross-origin
    HTTP pre-flight OPTIONS request. If the `current_request` HTTP_ORIGIN is not whitelisted, an
    error Response will be returned. This helps to protect against Cross-Site Request Forgery
    (CSRF) attacks.
    """
    cors_headers = get_cors_headers_for_http_options_request(current_request)
    url = current_request.environ.get('HTTP_ORIGIN', 'unknown')

    if not _url_is_safe(url):
        origin = current_request.environ.get('HTTP_ORIGIN', 'unknown')
        error_response = Response(
            response=json_utils.dumps({
                'status': 'error',
                'message': f"Origin {origin} not allowed."
            }),
            status=500,
            mimetype='application/json'
        )
        for k, v in cors_headers.items():
            error_response.headers[k] = v
        return error_response

    okay_response = Response(
        response=None,
        status=200,
        mimetype='text/html')
    for k, v in cors_headers.items():
        okay_response.headers[k] = v
    return okay_response


def _url_is_safe(url: str) -> bool:
    return bool(url in WHITELISTED_ORIGINS or re.search(LOCALHOST_PATTERN, url)
                or re.search(LOCALHOST_IP_PATTERN, url))
