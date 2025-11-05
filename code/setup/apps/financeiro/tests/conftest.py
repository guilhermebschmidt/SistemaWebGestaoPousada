import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def auth_client(client, db):
    """Return a test client already authenticated with a simple user (name: auth_client)."""
    User = get_user_model()
    user = User.objects.create_user(username='testuser_fin', password='password')
    client.force_login(user)
    return client
