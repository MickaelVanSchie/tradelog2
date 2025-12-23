from unittest.mock import Mock


def test_homepage_http_status_ok(test_client, session):
    """
    Verify if the app can be started.
    """
    response = test_client.get('/')
    assert response.status_code == 200
