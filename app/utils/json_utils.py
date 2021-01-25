#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Implementations of json.dumps and json.loads that support serializing standard Python data types
including datetime and date.

The helper method json_response() is tailored to return Flask server JSON responses.
"""

import datetime
import json
import re
from typing import Any, Dict, Optional

import dateutil.parser as date_parser
from werkzeug.wrappers import BaseResponse as Response


def dumps(json_data: Any) -> str:
    """Custom implementation of JSON.dumps() that supports datetime as well as any object with a
    `to_json()` method."""
    return json.dumps(json_data, cls=_MyJSONEncoder)


def json_response(
    json_data: Any, status_code=200, response_headers: Optional[dict] = None
) -> Response:
    """Function to create an HTTP Response object containing JSON data.

    Args:
        json_data: The data to be serialized to a JSON string and sent back with the HTTP Response.
        status_code: The HTTP status code.
        response_headers: Optional; dictionary of response headers, where keys are the header names.

    Returns:
        New HTTP Response object.
    """
    if isinstance(json_data, str):
        data = json_data
    else:
        data = dumps(json_data)
    my_response = Response(
        response=data,
        status=status_code,
        mimetype='application/json; charset=UTF-8')

    if response_headers is not None:
        for k, v in response_headers.items():
            my_response.headers[k] = v

    return my_response


def loads(json_string: str) -> dict:
    """Custom implementation of JSON.loads() that supports datetime."""
    return json.loads(json_string, object_hook=_json_decoder)


class _MyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects and objects with a `to_json()` method."""

    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return json.JSONEncoder.default(self, obj)
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            if isinstance(obj, datetime.date):
                obj = datetime.datetime.fromordinal(obj.toordinal())
            return obj.isoformat()
        elif getattr(obj, 'to_json', False):
            return obj.to_json()
        else:
            raise TypeError(f"type '{type(obj).__name__}' is not json-serializable; value: {obj}")


# See: https://stackoverflow.com/questions/41129921/validate-an-iso-8601-datetime-string-in-python
_iso_regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
_match_iso8601 = re.compile(_iso_regex).match


def _is_valid_iso8601(str_val: str) -> bool:
    if _match_iso8601(str_val):
        return True
    return False


def _json_decoder(dct: Dict[Any, Any]) -> Dict[Any, Any]:
    """Custom JSON decoder that handles datetime objects."""
    for key, value in dct.items():
        if type(value) is str and _is_valid_iso8601(value):
            dct[key] = date_parser.parse(value)

    return dct
