import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testadmin',
        email='testadmin@example.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True,
    )


# Admin Login - Username Required ============================================

def test_admin_login_requires_username_not_email(client, test_user):
    login_url = reverse('admin:login')

    # Try to login with email (should FAIL)
    response = client.post(
        login_url,
        {
            'email': 'testadmin@example.com',  # Using email
            'password': 'testpass123',
        },
        follow=True,
    )

    assert not response.wsgi_request.user.is_authenticated

    response = client.post(
        login_url,
        {
            'username': 'testadmin',  # Using username
            'password': 'testpass123',
        },
        follow=True,
    )

    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user.username == 'testadmin'

def test_admin_login_form_has_username_field(client):
    login_url = reverse('admin:login')
    response = client.get(login_url)
    content = response.content.decode('utf-8')

    assert 'name="username"' in content
    assert 'name="email"' not in content or 'type="password"' in content

# Profile Auto-Creation ======================================================

def test_profile_auto_created_on_user_creation(db):
    """Profile should be automatically created when user is created."""
    user = User.objects.create_user(
        username='profiletest',
        email='profiletest@example.com',
        password='test123',
    )

    # Profile should exist
    assert hasattr(user, 'profile')
    assert user.profile is not None
    assert user.profile.player_level == 1
    assert user.profile.experience_points == 0
