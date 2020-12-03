from unittest import TestCase

from mock import MagicMock, patch

import json
from flask import jsonify

from dwfclients.auth.apis import AuthException, check_bearer_token, configure_authenticated_blueprints
from dwfclients.auth.models import User

from tests.auth import app

class ApisTest(TestCase):
    user = User(
        username='user@test.com',
        admin=False
    )

    def test_configure_authenticated_blueprints_configures_all_always(self):
        mock_blueprint1 = MagicMock()
        mock_blueprint2 = MagicMock()
        mock_blueprint1.before_request = MagicMock()
        mock_blueprint2.before_request = MagicMock()
        blueprints = [mock_blueprint1, mock_blueprint2]
        configure_authenticated_blueprints(blueprints)

        mock_blueprint1.before_request.assert_called_once()
        mock_blueprint2.before_request.assert_called_once()

    @patch("dwfclients.auth.apis.authenticate")
    def test_check_bearer_token_returns_none_on_valid_token(self, mock_authenticate):
        with app.test_request_context():
            # for some reason this had to be patched within the app.test_request_context
            request_patcher = patch('dwfclients.auth.apis.request')
            mock_request = request_patcher.start()
            request_patcher = patch('dwfclients.auth.apis.request')

            mock_request.headers = MagicMock()
            mock_request.headers.get = MagicMock()
            mock_request.headers.get.return_value = "token token"

            mock_authenticate.return_value = self.user

            outcome = check_bearer_token()
            assert(outcome is None)

    @patch("dwfclients.auth.apis.authenticate")
    def test_check_bearer_token_sets_user_on_valid_token(self, mock_authenticate):
        with app.test_request_context():
            # for some reason this had to be patched within the app.test_request_context
            request_patcher = patch('dwfclients.auth.apis.request')
            mock_request = request_patcher.start()
            g_patcher = patch("dwfclients.auth.apis.g")
            mock_g = g_patcher.start()

            mock_request.headers = MagicMock()
            mock_request.headers.get = MagicMock()
            mock_request.headers.get.return_value = "token token"

            mock_authenticate.return_value = self.user

            outcome = check_bearer_token()

            assert(mock_g.user is self.user)

    @patch("dwfclients.auth.apis.jsonify")
    @patch("dwfclients.auth.apis.make_response")
    @patch("dwfclients.auth.apis.authenticate")
    def test_rebuild(self, mock_authenticate, mock_make_response, mock_jsonify):
        with app.test_request_context():
            # for some reason this had to be patched within the app.test_request_context
            request_patcher = patch('dwfclients.auth.apis.request')
            mock_request = request_patcher.start()

            mock_request.headers = MagicMock()
            mock_request.headers.get = MagicMock()
            mock_request.headers.get.return_value = "token token"

            mock_authenticate.return_value = self.user
            mock_authenticate.side_effect = AuthException

            expected_response_object = {
                'status': 'fail',
                'message': 'Invalid auth token.'
            }
            mock_jsonify.return_value = expected_response_object

            response, status = check_bearer_token()
            assert(status == 401)

            mock_make_response.assert_called_with(expected_response_object)



    # TODO next
    # def tearDown(self):
        # self.request_patcher.stop()

