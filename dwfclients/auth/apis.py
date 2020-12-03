from flask import request, make_response, jsonify, g


class AuthException(BaseException):
    pass


def authenticate(token):
    # TODO
    return False


def check_bearer_token():
    try:
        # TJTAG TODO LOGGING and maybe something else... i guess just debug these tests
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@HEREHRHERHEREHER")
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ''
        # g.user = authenticate(token)
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
