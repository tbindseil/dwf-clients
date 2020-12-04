import requests

from flask import request, make_response, jsonify, g

from dwfclients.auth.models import User


class AuthException(BaseException):
    pass


def authenticate(token):
    if token is None or token == "":
        raise AuthException("no token")

    # send request to auth service
    header = {'Authorization': 'Bearer ' + token}
    url = 'https://localhost:6901/auth/user'
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        raise AuthException("error authenticating")

    # parse response
    return User(response.json.username, response.json.admin)


def check_bearer_token():
    try:
        # TJTAG TODO LOGGING and maybe something else... i guess just debug these tests
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ''
        g.user = authenticate(token)
        return None
    except AuthException as e:
        responseObject = {
            'status': 'fail',
            'message': 'Invalid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


def configure_authenticated_blueprints(blueprints):
    for blueprint in blueprints:
        blueprint.before_request(check_bearer_token)
