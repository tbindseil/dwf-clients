from unittest import TestCase

from mock import MagicMock

from dwfclients.auth.apis import configure_authenticated_blueprints


class ApisTest(TestCase):
    def test_configure_authenticated_blueprints_configures_all_always(self):
        mock_blueprint1 = MagicMock()
        mock_blueprint2 = MagicMock()
        mock_blueprint1.before_request = MagicMock()
        mock_blueprint2.before_request = MagicMock()
        blueprints = [mock_blueprint1, mock_blueprint2]
        configure_authenticated_blueprints(blueprints)

        mock_blueprint1.before_request.assert_called_once()
        mock_blueprint2.before_request.assert_called_once()
