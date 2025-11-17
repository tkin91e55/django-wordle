from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

def test_allauth_signup_generates_username(client, db):
    """Test that allauth signup auto-generates username."""
    response = client.post(
        reverse('account_signup'),
        {
            'email': 'john.doe@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        },
        follow=True
    )

    user = User.objects.get(email='john.doe@example.com')
    assert user.username == 'john_doe'

def test_user_save_generates_username_from_email(db):
    """Test that User.save() auto-generates username if missing."""
    user = User(email='john.doe@example.com')
    user.set_password('test123')
    user.save()

    assert user.username == 'john_doe'

    user2 = User(email='john.doe@example2.com')
    user2.set_password('test123')
    user2.save()

    assert user2.username == 'john_doe_1'

def test_populate_username_then_save_MyAccountAdaptor(db):
    """Test username generation via allauth adapter flow."""
    from users.custom_allauth import MyAccountAdapter

    adapter = MyAccountAdapter()
    user = User(email='john.doe@example.com')
    user.set_password('test123')

    adapter.populate_username(request=None, user=user)
    user.save()

    assert user.username == 'john_doe'

    user2 = User(email='john.doe@example2.com')
    user2.set_password('test123')
    adapter.populate_username(request=None, user=user2)
    user2.save()

    assert user2.username == 'john_doe_1'

def test_populate_username_then_save_MySocialAccountAdaptor(db):
    """Test username generation via allauth adapter flow."""
    from users.custom_allauth import MySocialAccountAdapter

    adapter = MySocialAccountAdapter()
    user = User(email='john.doe@example.com')
    user.set_password('test123')

    adapter.populate_username(request=None, user=user)
    user.save()

    assert user.username == 'john_doe'
