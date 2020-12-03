from unittest import TestCase

from mock import MagicMock, patch

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
    # @patch("dwfclients.auth.apis.request")
    def test_rebuild(self, mock_authenticate): #, mock_request):
        with app.test_request_context():
            self.patcher = patch('dwfclients.auth.apis.request')
            mock_request = self.patcher.start()

            mock_request.headers = MagicMock()
            mock_request.headers.get = MagicMock()
            mock_request.headers.get.return_value = "token token"

            mock_authenticate.return_value = self.user

            outcome = check_bearer_token()
            assert(outcome is None)



#    @patch("dwfclients.auth.apis.authenticate")
#    @patch("dwfclients.auth.apis.request")
#    @patch("dwfclients.auth.apis.g")
#    @patch("dwfclients.auth.apis.make_response")
#    def test_check_bearer_token_returns_none_on_valid_token(self, mock_authenticate, mock_request, mock_g, mock_make_response):
#        #with app.test_request_context():
#        with app.app_context():
#        #with app.test_request_context():
#            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ummmm")
#            mock_request.headers = MagicMock()
#            mock_request.headers.get = MagicMock()
#            mock_request.headers.get.return_value = "token token"
#
#            mock_authenticate.return_value = self.user
#
#            outcome = check_bearer_token()
#            assert(outcome is None)
#
#    def test_check_bearer_token_sets_user_on_valid_token(self):
#        return false
#
#    def test_check_bearer_token_returns_401_on_AuthException(self):
#        response = self.client.post(
#            '/picture-metadata/create',
#            data=self.title_data,
#            content_type='application/json',
#            headers=dict(
#                Authorization='Bearer ' + self.bad_token
#            )
#        )
#        data = json.loads(response.data.decode())
#        self.assertTrue(data['status'] == 'fail')
#        self.assertTrue(data['message'] == 'Invalid auth token.')
#        self.assertEqual(response.status_code, 401)
#        return false;
