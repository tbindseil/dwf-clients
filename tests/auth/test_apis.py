from unittest import TestCase

from mock import MagicMock, patch

import json
from flask import jsonify

from dwfclients.auth.apis import AuthException, authenticate, check_bearer_token, configure_authenticated_blueprints
from dwfclients.auth.models import User

from tests.auth import app

class ConfigureAuthenticatedBlueprintsTest(TestCase):
    def test_configure_authenticated_blueprints_configures_all_always(self):
        mock_blueprint1 = MagicMock()
        mock_blueprint2 = MagicMock()
        mock_blueprint1.before_request = MagicMock()
        mock_blueprint2.before_request = MagicMock()
        blueprints = [mock_blueprint1, mock_blueprint2]
        configure_authenticated_blueprints(blueprints)

        mock_blueprint1.before_request.assert_called_once()
        mock_blueprint2.before_request.assert_called_once()

class CheckBearerTokenTest(TestCase):
    authenticate_patcher = None
    mock_authenticate = None
    request_patcher = None
    mock_request = None

    user = User(
        username='user@test.com',
        admin=False
    )

    def setUp(self):
        self.authenticate_patcher = patch('dwfclients.auth.apis.authenticate')
        self.mock_authenticate = self.authenticate_patcher.start()

        # for some reason this had to be patched within the app.test_request_context
        with app.test_request_context():
            self.request_patcher = patch('dwfclients.auth.apis.request')
            self.mock_request = self.request_patcher.start()

    def tearDown(self):
        self.authenticate_patcher.stop()
        self.request_patcher.stop()

    def make_mock_request(self):
        self.mock_request.headers = MagicMock()
        self.mock_request.headers.get = MagicMock()
        self.mock_request.headers.get.return_value = "token token"

    def test_check_bearer_token_returns_none_on_valid_token(self):
        with app.test_request_context():
            self.make_mock_request()
            self.mock_authenticate.return_value = self.user

            outcome = check_bearer_token()
            assert(outcome is None)

    def test_check_bearer_token_sets_user_on_valid_token(self):
        with app.test_request_context():
            g_patcher = patch("dwfclients.auth.apis.g")
            mock_g = g_patcher.start()

            self.make_mock_request()

            self.mock_authenticate.return_value = self.user

            outcome = check_bearer_token()

            assert(mock_g.user is self.user)

    @patch("dwfclients.auth.apis.jsonify")
    @patch("dwfclients.auth.apis.make_response")
    def test_rebuild(self, mock_make_response, mock_jsonify):
        with app.test_request_context():
            self.make_mock_request()

            self.mock_authenticate.side_effect = AuthException

            expected_response_object = {
                'status': 'fail',
                'message': 'Invalid auth token.'
            }
            mock_jsonify.return_value = expected_response_object

            response, status = check_bearer_token()
            assert(status == 401)

            mock_make_response.assert_called_with(expected_response_object)


class AuthenticateTests(TestCase):
    @patch("dwfclients.auth.apis.requests.get")
    def test_authenticate_calls_get_user_api(self, mock_get):
        token = "token"

        mock_response = MagicMock()
        mock_response.status_code = 200
        def mock_get_side_effect(url, headers):
            assert(url == 'https://localhost:6901/auth/user')
            assert(headers['Authorization'] == ('Bearer ' + token))
            return mock_response
        mock_get.side_effect = mock_get_side_effect

        user = authenticate(token)
        mock_get.assert_called_once()

    def test_authenticate_throws_AuthException_when_no_token(self):
        with self.assertRaises(AuthException):
            token = ""
            authenticate(token)

        with self.assertRaises(AuthException):
            token = None
            authenticate(token)

    @patch("dwfclients.auth.apis.requests.get")
    def test_authenticate_throws_AuthException_when_invalid_token(self, mock_get):
        with self.assertRaises(AuthException):
            token = "token"

            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            authenticate(token)


    @patch("dwfclients.auth.apis.requests.get")
    def test_authenticate_returns_user_on_valid_token(self, mock_get):
        token = "token"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock()
        response_data = {'data': {'username': 'username', 'admin': 'admin'}}
        mock_response.json.return_value = response_data
        mock_get.return_value = mock_response

        user = authenticate(token)
        assert(user.username == "username")
        assert(user.admin == "admin")
