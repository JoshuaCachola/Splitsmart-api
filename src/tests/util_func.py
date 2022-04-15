import json
from urllib.parse import urlencode

from flask import url_for


def json_dump_kwarg(**kwargs):
    return json.dumps(kwargs)


def url_string(app, **url_params):
    with app.test_request_context():
        string = url_for("graphql")

    if url_params:
        string += "?" + urlencode(url_params)

    return string


def response_json(response):
    return json.loads(response.data.decode())

